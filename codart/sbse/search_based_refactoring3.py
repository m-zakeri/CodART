"""

## Module description

This module implements the search-based refactoring with various search strategy
using pymoo framework.

### Classes

Gene, RefactoringOperation: One refactoring with params

Individual: A list of RefactoringOperation

PureRandomInitialization: Population, list of Individual


## References

[1] https://pymoo.org/customization/custom.html

[2] https://pymoo.org/misc/reference_directions.html


## Changelog

### version 0.2.4
    1. Fix objective parameters of the problem classes

### version 0.2.3
    1. Fix PEP 8 warnings

### version 0.2.2
    1. Add a separate log directory for each execution
    2. Add possibility to resume algorithm

### version 0.2.1
    1. minor updates
    2. fix bugs
    3. rename variables names

### version 0.2.0
    1. Crossover function is added.
    2. Termination criteria are added.
    3. Computation of highly trade-off points is added.
    4. Tournament-selection is added.
    5. _evaluate function in NSGA-III is now works on population instead of an individual
        (population-based versus element-wise).
    6. Other setting for NSGA-III including adding energy-references point instead of Das and Dennis approach.

===

"""

__version__ = '0.2.4'
__author__ = 'Morteza Zakeri'

import os
import random
import json
from copy import deepcopy
from datetime import datetime
from multiprocessing import Process, Array
from typing import List

import numpy as np
import pandas as pd

from pymoo.core.callback import Callback
from pymoo.core.crossover import Crossover
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from pymoo.core.mutation import Mutation
from pymoo.core.problem import Problem
from pymoo.core.sampling import Sampling

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
# New
from pymoo.algorithms.moo.rnsga3 import RNSGA3
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.algorithms.moo.age import AGEMOEA


from pymoo.factory import get_reference_directions, get_decision_making

from pymoo.operators.selection.tournament import TournamentSelection
from pymoo.optimize import minimize
from pymoo.util.termination.default import MultiObjectiveDefaultTermination

from codart.metrics.qmood import DesignQualityAttributes
from codart.metrics.modularity import main as modularity_main
# from codart.metrics.testability_prediction2 import main as testability_main
# New
from codart.metrics.distance_metric import main as distance_main

from codart.metrics.testability_prediction3 import main as testability_main

from codart.utility.directory_utils import update_understand_database, git_restore, reset_project
from codart.sbse.initialize import RandomInitialization, SmellInitialization, Initialization
from codart import config
from codart.config import logger

POPULATION = []


class Gene:
    """

    The base class for the Gene in genetic algorithms.

    """

    def __init__(self, **kwargs):
        """

        Args:

            name (str): Refactoring operation name

            params (dict): Refactoring operation parameters

            main (function): Refactoring operation main function (API)

        """

        self.name = kwargs.get('name')
        self.params = kwargs.get('params')
        self.main = kwargs.get('main')

    def __str__(self):
        parameters = '('
        for param in self.params:
            parameters += str(param) + ', '
        return self.name + parameters[:-2] + ')'


class RefactoringOperation(Gene):
    """

    The class define a data structure (dictionary) to hold a refactoring operation

    Each refactoring operation hold as a dictionary contains the required parameters.

        Example:

            ```
            make_field_static refactoring is marshaled as the following dict:
            params = {
                'refactoring_name': 'make_field_static'
                'api': 'main_function'
                'source_class': 'name_of_source_class'
                'field_name': 'name_of_the_field_to_be_static'
            }
            ```

    """

    def __init__(self, **kwargs):
        """

        Args:

            name (str): Refactoring operation name

            params (dict): Refactoring operation parameters

            main (function): Refactoring operation main function (API)

        """
        super(RefactoringOperation, self).__init__(**kwargs)

    def __str__(self):
        return f'{self.name}({self.params})\n'

    def __repr__(self):
        return self.__str__()

    def do_refactoring(self):
        """

        Check preconditions and apply refactoring operation to source code

        Returns:

            result (boolean): The result statues of the applied refactoring

        """

        logger.info(f"Running {self.name}")
        logger.info(f"Parameters {self.params}")
        try:
            res = self.main(**self.params)
            logger.debug(f"Executed refactoring with result {res}")
            return res
        except Exception as e:
            logger.error(f"Unexpected error in executing refactoring:\n {e}")
            return False


class Individual(List):
    """

    The class define a data structure (list) to hold an individual during the search process.
    Each individual (also called, chromosome or solution in the context of genetic programming)
    is an array of refactoring operations where the order of their execution is accorded by
    their positions in the array.

    """

    def __init__(self):
        """

        Args:


        """
        super(Individual, self).__init__()
        self.refactoring_operations = []

    def __iter__(self):
        for ref in self.refactoring_operations:
            yield ref

    def __len__(self):
        return len(self.refactoring_operations)

    def __getitem__(self, item):
        return self.refactoring_operations[item]

    def __delitem__(self, key):
        del self.refactoring_operations[key]

    def __setitem__(self, key, value):
        self.refactoring_operations[key] = value

    def __str__(self):
        return str(self.refactoring_operations)

    def insert(self, __index: int, __object: RefactoringOperation) -> None:
        self.refactoring_operations.insert(__index, __object)

    def append(self, __object: RefactoringOperation) -> None:
        self.insert(len(self.refactoring_operations), __object)


# ---------------------- Defines objectives calculation functions -----------------------
def calc_qmood_objectives(arr_):
    qmood_quality_attributes = DesignQualityAttributes(udb_path=config.UDB_PATH)
    arr_[0] = qmood_quality_attributes.reusability
    arr_[1] = qmood_quality_attributes.understandability
    arr_[2] = qmood_quality_attributes.flexibility
    arr_[3] = qmood_quality_attributes.functionality
    arr_[4] = qmood_quality_attributes.effectiveness
    arr_[5] = qmood_quality_attributes.extendability


def calc_testability_objective(path_, arr_):
    arr_[6] = testability_main(
        path_,
        initial_value=config.CURRENT_METRICS.get("TEST", 1.0)
    )


def calc_modularity_objective(path_, arr_):
    arr_[7] = modularity_main(
        path_,
        initial_value=config.CURRENT_METRICS.get("MODULE", 1.0)
    )


def calc_distance_objective(path_, arr_):
    arr_[8] = distance_main(
        path_,
        initial_value=config.CURRENT_METRICS.get("DISTANCE", 1.0)
    )

# ---------------------- Defines problems ----------------------------
class ProblemSingleObjective(Problem):
    """

    The CodART single-objective optimization work with only one objective, testability:

    """

    def __init__(self,
                 n_objectives=1,
                 n_refactorings_lowerbound=10,
                 n_refactorings_upperbound=50,
                 evaluate_in_parallel=False,
                 mode='single'  # 'multi'
                 ):
        """

        Args:

            n_objectives (int): Number of objectives

            n_refactorings_lowerbound (int): The lower bound of the refactoring sequences

            n_refactorings_upperbound (int): The upper bound of the refactoring sequences

            mode (str): 'single' or 'multi'

        """

        super(ProblemSingleObjective, self).__init__(n_var=1, n_obj=1, n_constr=0)
        self.n_refactorings_lowerbound = n_refactorings_lowerbound
        self.n_refactorings_upperbound = n_refactorings_upperbound
        self.evaluate_in_parallel = evaluate_in_parallel
        self.mode = mode
        self.n_obj_virtual = n_objectives

    def _evaluate(self,
                  x,  #
                  out,
                  *args,
                  **kwargs):
        """

        This method iterate over a population, execute the refactoring operations in each individual sequentially,
        and compute quality attributes for the refactored version of the program, as objectives of the search

        Args:

            x (Population): x is a matrix where each row is an individual, and each column a variable.\
                We have one variable of type list (Individual) ==> x.shape = (len(Population), 1)

        """

        objective_values = []
        for k, individual_ in enumerate(x):
            # Stage 0: Git restore
            logger.debug("Executing git restore.")
            git_restore(config.PROJECT_PATH)
            logger.debug("Updating understand database after git restore.")
            update_understand_database(config.UDB_PATH)

            # Stage 1: Execute all refactoring operations in the sequence x
            logger.debug(f"Reached Individual with Size {len(individual_[0])}")
            for refactoring_operation in individual_[0]:
                refactoring_operation.do_refactoring()
                # Update Understand DB
                logger.debug(f"Updating understand database after {refactoring_operation.name}.")
                update_understand_database(config.UDB_PATH)

            # Stage 2:
            if self.mode == 'single':
                # Stage 2 (Single objective mode): Considering only one quality attribute, e.g., testability
                score = testability_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("TEST", 1.0))
            else:
                # Stage 2 (Multi-objective mode): Considering one objective based on average of 8 objective
                arr = Array('d', range(self.n_obj_virtual))
                if self.evaluate_in_parallel:
                    # Stage 2 (Multi-objective mode, parallel): Computing quality attributes
                    p1 = Process(target=calc_qmood_objectives, args=(arr,))
                    if self.n_obj_virtual == 9:
                        p2 = Process(target=calc_testability_objective, args=(config.UDB_PATH, arr,))
                        p3 = Process(target=calc_modularity_objective, args=(config.UDB_PATH, arr,))
                        p4 = Process(target=calc_distance_objective(), args=(config.UDB_PATH, arr,))
                        p1.start(), p2.start(), p3.start(), p4.start()
                        p1.join(), p2.join(), p3.join(), p4.join()
                    else:
                        p1.start()
                        p1.join()
                    score = sum([i for i in arr]) / self.n_obj_virtual
                else:
                    # Stage 2 (Multi-objective mode, sequential): Computing quality attributes
                    qmood_quality_attributes = DesignQualityAttributes(udb_path=config.UDB_PATH)
                    o1 = qmood_quality_attributes.average_sum
                    if self.n_obj_virtual == 9:
                        o2 = testability_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("TEST", 1.0))
                        o3 = modularity_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("MODULE", 1.0))
                        o4 = distance_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("DISTANCE", 1.0))
                    else:
                        o2 = 0
                        o3 = 0
                        o4 = 0
                    del qmood_quality_attributes
                    score = (o1 * 6. + o2 + o3 + o4) / self.n_obj_virtual

            # Stage 3: Marshal objectives into vector
            objective_values.append([-1 * score])
            logger.info(f"Objective values for individual {k} in mode {self.mode}: {[-1 * score]}")

        # Stage 4: Marshal all objectives into out dictionary
        out['F'] = np.array(objective_values, dtype=float)


class ProblemMultiObjective(Problem):
    """

    The CodART multi-objective optimization work with three objective:

    * Objective 1: Mean value of QMOOD metrics

    * Objective 2: Testability

    * Objective 3: Modularity

    * Objective 4: Distance

    """

    def __init__(self, n_objectives=9,
                 n_refactorings_lowerbound=10,
                 n_refactorings_upperbound=50,
                 evaluate_in_parallel=False
                 ):
        """
        Args:

            n_objectives (int): Number of objectives

            n_refactorings_lowerbound (int): The lower bound of the refactoring sequences

            n_refactorings_upperbound (int): The upper bound of the refactoring sequences

            evaluate_in_parallel (bool): Whether the objectives evaluate in parallel

        """
        super(ProblemMultiObjective, self).__init__(n_var=1, n_obj=3, n_constr=0)
        self.n_refactorings_lowerbound = n_refactorings_lowerbound
        self.n_refactorings_upperbound = n_refactorings_upperbound
        self.evaluate_in_parallel = evaluate_in_parallel
        self.n_obj_virtual = n_objectives

    def _evaluate(self,
                  x,  #
                  out,
                  *args,
                  **kwargs):
        """

        This method iterate over a population, execute the refactoring operations in each individual sequentially,
        and compute quality attributes for the refactored version of the program, as objectives of the search

        Args:

            x (Population): x is a matrix where each row is an individual, and each column a variable. \
            We have one variable of type list (Individual) ==> x.shape = (len(Population), 1)


        """
        objective_values = []
        for k, individual_ in enumerate(x):
            # Stage 0: Git restore
            logger.debug("Executing git restore.")
            git_restore(config.PROJECT_PATH)
            logger.debug("Updating understand database after git restore.")
            update_understand_database(config.UDB_PATH)

            # Stage 1: Execute all refactoring operations in the sequence x
            logger.debug(f"Reached Individual with Size {len(individual_[0])}")
            for refactoring_operation in individual_[0]:
                refactoring_operation.do_refactoring()
                # Update Understand DB
                logger.debug(f"Updating understand database after {refactoring_operation.name}.")
                update_understand_database(config.UDB_PATH)

            # Stage 2:
            arr = Array('d', range(self.n_obj_virtual))
            if self.evaluate_in_parallel:
                # Stage 2 (parallel mood): Computing quality attributes
                p1 = Process(target=calc_qmood_objectives, args=(arr,))
                p2 = Process(target=calc_testability_objective, args=(config.UDB_PATH, arr,))
                p3 = Process(target=calc_modularity_objective, args=(config.UDB_PATH, arr,))
                p4 = Process(target=calc_distance_objective(), args=(config.UDB_PATH, arr,))
                p1.start(), p2.start(), p3.start(), p4.start()
                p1.join(), p2.join(), p3.join(), p4.join()
                o1 = sum([i for i in arr[:6]]) / 6.
                o2 = arr[6]
                o3 = arr[7]
                o4 = arr[8]
            else:
                # Stage 2 (sequential mood): Computing quality attributes
                qmood_quality_attributes = DesignQualityAttributes(udb_path=config.UDB_PATH)
                o1 = qmood_quality_attributes.average_sum
                o2 = testability_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("TEST", 1.0))
                o3 = modularity_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("MODULE", 1.0))
                o4 = distance_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("DISTANCE", 1.0))
                del qmood_quality_attributes

            # Stage 3: Marshal objectives into vector
            objective_values.append([-1 * o1, -1 * o2, -1 * o3, -1 * o4])
            logger.info(f"Objective values for individual {k}: {[-1 * o1, -1 * o2, -1 * o3, -1 * o4]}")

        # Stage 4: Marshal all objectives into out dictionary
        out['F'] = np.array(objective_values, dtype=float)


class ProblemManyObjective(Problem):
    """

    The CodART many-objective optimization work with eight objective:

    * Objective 1 to 6: QMOOD design quality attributes

    * Objective 7: Testability prediction model

    * Objective 8: Modularity complex network

    * Objective 9: Distance metric

    """

    def __init__(self, n_objectives=9, n_refactorings_lowerbound=10, n_refactorings_upperbound=50,
                 evaluate_in_parallel=False, verbose_design_metrics=False,
                 ):
        """

        Args:

            n_objectives (int): Number of objectives

            n_refactorings_lowerbound (int): The lower bound of the refactoring sequences

            n_refactorings_upperbound (int): The upper bound of the refactoring sequences

            evaluate_in_parallel (bool): Whether the objectives computed in parallel or not

            verbose_design_metrics (bool): Whether log the design metrics for each refactoring sequences or not

        """
        super(ProblemManyObjective, self).__init__(n_var=1, n_obj=n_objectives, n_constr=0, )
        self.n_refactorings_lowerbound = n_refactorings_lowerbound
        self.n_refactorings_upperbound = n_refactorings_upperbound
        self.evaluate_in_parallel = evaluate_in_parallel
        self.verbose_design_metrics = verbose_design_metrics

    def _evaluate(self, x, out, *args, **kwargs):
        """

        This method iterate over a population, execute the refactoring operations in each individual sequentially,
        and compute quality attributes for the refactored version of the program, as objectives of the search.
        By default, elementwise_evaluation is set to False, which implies the _evaluate retrieves a set of solutions.

        Args:

            x (Population): x is a matrix where each row is an individual, and each column a variable.\
            We have one variable of type list (Individual) ==> x.shape = (len(Population), 1)


        """

        objective_values = []
        for k, individual_ in enumerate(x):
            # Stage 0: Git restore
            logger.debug("Executing git restore.")
            git_restore(config.PROJECT_PATH)
            logger.debug("Updating understand database after git restore.")
            update_understand_database(config.UDB_PATH)

            # Stage 1: Execute all refactoring operations in the sequence x
            logger.debug(f"Reached an Individual with size {len(individual_[0])}")
            for refactoring_operation in individual_[0]:
                res = refactoring_operation.do_refactoring()
                # Update Understand DB
                logger.debug(f"Updating understand database after {refactoring_operation.name}.")
                update_understand_database(config.UDB_PATH)

            # Stage 2:
            arr = Array('d', range(self.n_obj))
            if self.evaluate_in_parallel:
                # Stage 2 (parallel mood): Computing quality attributes
                p1 = Process(target=calc_qmood_objectives, args=(arr,))
                if self.n_obj == 9:
                    p2 = Process(target=calc_testability_objective, args=(config.UDB_PATH, arr,))
                    p3 = Process(target=calc_modularity_objective, args=(config.UDB_PATH, arr,))
                    p4 = Process(target=calc_distance_objective(), args=(config.UDB_PATH, arr,))
                    p1.start(), p2.start(), p3.start(), p4.start()
                    p1.join(), p2.join(), p3.join(), p4.join()
                else:
                    p1.start()
                    p1.join()
            else:
                # Stage 2 (sequential mood): Computing quality attributes
                qmood_quality_attributes = DesignQualityAttributes(udb_path=config.UDB_PATH)
                arr[0] = qmood_quality_attributes.reusability
                arr[1] = qmood_quality_attributes.understandability
                arr[2] = qmood_quality_attributes.flexibility
                arr[3] = qmood_quality_attributes.functionality
                arr[4] = qmood_quality_attributes.effectiveness
                arr[5] = qmood_quality_attributes.extendability
                if self.n_obj == 9:
                    arr[6] = testability_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("TEST", 1.0))
                    arr[7] = modularity_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("MODULE", 1.0))
                    arr[8] = distance_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("DISTANCE", 1.0))

                if self.verbose_design_metrics:
                    design_metrics = {
                        "DSC": [qmood_quality_attributes.DSC],
                        "NOH": [qmood_quality_attributes.NOH],
                        "ANA": [qmood_quality_attributes.ANA],
                        "MOA": [qmood_quality_attributes.MOA],
                        "DAM": [qmood_quality_attributes.DAM],
                        "CAMC": [qmood_quality_attributes.CAMC],
                        "CIS": [qmood_quality_attributes.CIS],
                        "NOM": [qmood_quality_attributes.NOM],
                        "DCC": [qmood_quality_attributes.DCC],
                        "MFA": [qmood_quality_attributes.MFA],
                        "NOP": [qmood_quality_attributes.NOP]
                    }
                    self.log_design_metrics(design_metrics)

                del qmood_quality_attributes

            # Stage 3: Marshal objectives into vector
            objective_values.append([-1 * i for i in arr])
            logger.info(f"Objective values for individual {k}: {[i for i in arr]}")

        # Stage 4: Marshal all objectives into out dictionary
        out['F'] = np.array(objective_values, dtype=float)
        # print('OUT', out['F'])

    def log_design_metrics(self, design_metrics):
        design_metrics_path = os.path.join(
            config.PROJECT_LOG_DIR,
            f'{config.PROJECT_NAME}_design_metrics_log_{config.global_execution_start_time}.csv'
        )

        df_design_metrics = pd.DataFrame(data=design_metrics)
        if os.path.exists(design_metrics_path):
            df = pd.read_csv(design_metrics_path, index_col=False)
            df_result = pd.concat([df, df_design_metrics], ignore_index=True)
            df_result.to_csv(design_metrics_path, index=False)
        else:
            df_design_metrics.to_csv(design_metrics_path, index=False)


class PopulationInitialization(Sampling):
    """
    This class create the initial population, x, consists of n_samples, pop_size.
    For each refactoring operation, a set of controlling parameters (e.g., actors and roles) is picked based on
    existing code smells in the program to be refactored.
    The selected refactoring operations are randomly arranged in each individual.
    Assigning randomly a sequence of refactorings to certain code fragments generates the initial population

    """

    def __init__(self, initializer: Initialization = None):
        """
        Args:

            initializer (Initialization): An  initializer object to be used for generating initial population

        """
        super(PopulationInitialization, self).__init__()
        self._initializer = initializer

    def _do(self, problem, n_samples, **kwargs):
        """
        Since the problem having only one variable, we return a matrix with the shape (n,1)

        Args:

            problem (Problem): An instance of pymoo Problem class to be optimized.

            n_samples (int): The same population size, pop_size.

        """
        if os.path.exists(config.INIT_POP_FILE):
            self._initializer.load_population(path=config.INIT_POP_FILE)
            population = self._initializer.population
            initial_pop_path = f'{config.PROJECT_LOG_DIR}initial_population_{config.global_execution_start_time}.json'
            if config.NGEN == 0:
                self._initializer.dump_population(path=initial_pop_path)
        else:
            population = self._initializer.generate_population()

        x = np.full((n_samples, 1), None, dtype=Individual)

        # New
        if config.PROBLEM == 3:
            for i in range(n_samples):
                individual_object = []  # list of refactoring operations (Temporarily used instead of Individual class)
                if i < config.POPULATION_SIZE:
                    for ref in population[i]:
                        individual_object.append(RefactoringOperation(name=ref[2], params=ref[1], main=ref[0]))
                    x[i, 0] = deepcopy(individual_object)
                else:
                    # for ref in population[i]:
                    individual_object.append(RefactoringOperation(name=ref[2], params=ref[1], main=ref[0]))
                    x[i, 0] = deepcopy(individual_object)
            return x
        else:
            # ------------------------
            for i in range(n_samples):
                individual_object = []  # list of refactoring operations (Temporarily used instead of Individual class)
                for ref in population[i]:
                    individual_object.append(RefactoringOperation(name=ref[2], params=ref[1], main=ref[0]))
                x[i, 0] = deepcopy(individual_object)
            return x


class AdaptiveSinglePointCrossover(Crossover):
    """

    This class implements solution variation, the adaptive one-point or single-point crossover operator.
    The crossover operator combines parents to create offsprings.
    It starts by selecting and splitting at random two parent solutions or individuals.
    Then, this operator creates two child solutions by putting, for the first child,
    the first part of the first parent with the second part of the second parent,
    and vice versa for the second child.

    * Note 1: In the pymoo framework, the crossover operator retrieves the input already with predefined matings.
    The default parent selection algorithm is TournamentSelection.

    * Note 2: It is better to create children that are close to their parents to have a more efficient search process,
    a so-called __adaptive crossover__, specifically in many-objective optimization.
    Therefore, the cutting point of the one-point crossover operator are controlled by restricting its position
    to be either belonging to the first tier of the refactoring sequence or belonging to the last tier.

    """

    def __init__(self, prob=0.9):
        """

        Args:

        prob (float): crossover probability

        """

        # Define the crossover: number of parents, number of offsprings, and cross-over probability
        super().__init__(n_parents=2, n_offsprings=2, prob=prob)

    def _do(self, problem, X, **kwargs):
        """

        For population X

        Args:

            problem (Problem): An instance of pymoo Problem class to be optimized.

            X (np.array): Population

        """

        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, n_var = X.shape

        # The output will be with the shape (n_offsprings, n_matings, n_var)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=object)

        # print(X.shape)
        # print(X)

        # for each mating provided
        for k in range(n_matings):
            # get the first and the second parent (a and b are instance of individuals)
            a, b = X[0, k, 0], X[1, k, 0]
            # print('### a', a)
            # print('### b', b)
            # print('len a', len(a))
            # print('len b', len(b))

            len_min = min(len(a), len(b))
            cross_point_1 = random.randint(1, int(len_min * 0.30))
            cross_point_2 = random.randint(int(len_min * 0.70), len_min - 1)
            if random.random() < 0.5:
                cross_point_final = cross_point_1
            else:
                cross_point_final = cross_point_2
            logger.info(f'cross_point_final: {cross_point_final}')
            offspring_a = []
            offspring_b = []
            for i in range(0, cross_point_final):
                offspring_a.append(deepcopy(a[i]))
                offspring_b.append(deepcopy(b[i]))

            for i in range(cross_point_final, len_min):
                offspring_a.append(deepcopy(b[i]))
                offspring_b.append(deepcopy(a[i]))

            if len(b) > len(a):
                for i in range(len(a), len(b)):
                    offspring_a.append(deepcopy(b[i]))
            else:
                for i in range(len(b), len(a)):
                    offspring_b.append(deepcopy(a[i]))

            # print('$$$ offspring_a', offspring_a)
            # print('$$$ offspring_b', offspring_b)
            # print('len offspring_a', len(offspring_a))
            # print('len offspring_b', len(offspring_b))

            # Join offsprings to offspring population Y
            Y[0, k, 0], Y[1, k, 0] = offspring_a, offspring_b
            # quit()

        return Y


class BitStringMutation(Mutation):
    """

    This class implements solution variation, a bit-string mutation operator.
    The bit-string mutation operator that picks probabilistically one or more refactoring operations from its
    or their associated sequence and replaces them by other ones from the initial list of possible refactorings.

    Each chromosome dimension would be changed according to the mutation probability.
    For example, for a mutation probability of 0.2, for each dimension, we generate randomly a number x between 0 and 1,
    if `x < mutation_probability` (e.g., 0.2) we change the refactoring operation in that dimension,
    otherwise no changes are taken into account.

    """

    def __init__(self, prob=0.2, initializer: Initialization = None):
        """

        Args:

             prob (float): mutation probability

        """

        super().__init__()
        self.mutation_probability = prob
        self._initializer = initializer

    def _do(self, problem, X, **kwargs):
        for i, individual in enumerate(X):
            for j, ro in enumerate(individual):
                r = np.random.random()
                # with a probability of `mutation_probability` replace the refactoring operation with new one
                if r < self.mutation_probability:
                    random_chromosome = random.choice(self._initializer.population)
                    item = random.choice(random_chromosome)
                    X[i][0][j] = deepcopy(RefactoringOperation(name=item[2], params=item[1], main=item[0]))
        return X


class BitStringMutation2(Mutation):
    """

        Select an individual to mutate with mutation probability.
        Only flip one refactoring operation in the selected individual.

    """

    def __init__(self, prob=0.2, initializer: Initialization = None):
        """

        Args:

            prob (float): mutation probability

        """

        super().__init__()
        self.mutation_probability = prob
        self._initializer = initializer
        self._initializer.load_population()

    def _do(self, problem, X, **kwargs):
        for i, individual in enumerate(X):
            r = np.random.random()
            # with a probability of `mutation_probability` replace the refactoring operation with new one
            if r < self.mutation_probability:
                # j is a random index in individual
                j = random.randint(0, len(individual[0]) - 1)
                random_chromosome = random.choice(self._initializer.population)
                item = random.choice(random_chromosome)
                X[i][0][j] = deepcopy(RefactoringOperation(name=item[2], params=item[1], main=item[0]))

        return X


class LogCallback(Callback):
    """

    Logging useful information after each iteration of the search algorithms

    """

    def __init__(self) -> None:
        super().__init__()
        # self.data["best"] = []

    def notify(self, algorithm, **kwargs):
        # self.data["best"].append(algorithm.pop.get("F").min())
        logger.info(f'Generation #{algorithm.n_gen + config.NGEN} was finished:')
        # logger.info(f'Best solution:')
        # logger.info(f'{algorithm.pop.get("F")}')
        # logger.info(f'Pareto-front solutions:')
        # logger.info(f'{algorithm.pf}')

        X, F, CV, G = algorithm.opt.get("X", "F", "CV", "G")
        logger.info(f'Optimum solutions:')
        logger.info(f'{F}')

        # Log evolved population at end of each generation
        generation_log_path = f'{config.PROJECT_LOG_DIR}generations_logs/'
        if not os.path.exists(generation_log_path):
            os.makedirs(generation_log_path)

        generation_endof_date_time = config.dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        population_log_file_path = os.path.join(
            generation_log_path,
            f'pop_gen{algorithm.n_gen + config.NGEN}_{generation_endof_date_time}.json'
        )
        pop_opt_log_file_path = os.path.join(
            generation_log_path,
            f'pop_opt_gen{algorithm.n_gen + config.NGEN}_{generation_endof_date_time}.json'
        )

        pop_opt_objective_value_log = os.path.join(
            config.PROJECT_LOG_DIR,
            f'{config.PROJECT_NAME}_objectives_log_{config.global_execution_start_time}.csv'
        )

        population_trimmed = []
        for chromosome in algorithm.pop:
            chromosome_new = []
            for gene_ in chromosome.X[0]:
                chromosome_new.append((gene_.name, gene_.params))
            population_trimmed.append(chromosome_new)

        with open(population_log_file_path, 'w', encoding='utf-8') as fp:
            json.dump(population_trimmed, fp, indent=4)

        population_trimmed = []
        objective_values_content = ''
        for chromosome in algorithm.opt:
            chromosome_new = []
            for gene_ in chromosome.X[0]:
                chromosome_new.append((gene_.name, gene_.params))
            population_trimmed.append(chromosome_new)

            objective_values_content += f'{algorithm.n_gen + config.NGEN},'
            for gene_objective_ in chromosome.F:
                objective_values_content += f'{gene_objective_},'
            objective_values_content += '\n'

        with open(pop_opt_log_file_path, mode='w', encoding='utf-8') as fp:
            json.dump(population_trimmed, fp, indent=4)

        if not os.path.exists(pop_opt_objective_value_log):
            writing_mode = 'w'
        else:
            writing_mode = 'a'
        with open(pop_opt_objective_value_log, mode=writing_mode, encoding='utf-8') as fp:
            fp.write(objective_values_content)

        logger.info('-' * 100)
        logger.info(' ')
        # quit()


# Calling the equal method of individual class
def is_equal_2_refactorings_list(a, b):
    """

    This method implement is_equal method which should return True if two instances of Individual class are equal.
    Otherwise, it returns False.
    The duplicate instances are removed from population at each generation.
    Only one instance is held to speed up the search algorithm

    """

    if len(a.X[0]) != len(b.X[0]):
        return False
    for i, ro in enumerate(a.X[0]):
        if ro.name != b.X[0][i].name:
            return False
        if ro.params != b.X[0][i].params:
            return False
    return True


def binary_tournament(pop, P, **kwargs):
    """

    Implements the binary tournament selection algorithm

    """

    # The P input defines the tournaments and competitors
    n_tournaments, n_competitors = P.shape
    if n_competitors != 2:
        raise Exception("Only pressure=2 allowed for binary tournament!")
    S = np.full(n_tournaments, -1, dtype=np.int64)

    # Now do all the tournaments
    for i in range(n_tournaments):
        a, b = P[i]
        # If the first individual is better, choose it
        if pop[a].F.all() <= pop[a].F.all():
            S[i] = a
        # Otherwise, take the other individual
        else:
            S[i] = b

    return S


def log_project_info(reset_=True, design_metrics_path=None, quality_attributes_path=None,
                     generation=0, testability_verbose=True, testability_log_path=None):
    """

    Logging project metrics and information

    """

    if reset_:
        reset_project()
    if quality_attributes_path is None:
        quality_attributes_path = os.path.join(config.PROJECT_LOG_DIR, 'quality_attrs_initial_values.csv')
    if design_metrics_path is None:
        design_metrics_path = os.path.join(config.PROJECT_LOG_DIR, 'design_metrics.csv')

    design_quality_attribute = DesignQualityAttributes(config.UDB_PATH)
    avg_, sum_ = design_quality_attribute.average_sum
    predicted_testability = testability_main(
        config.UDB_PATH,
        initial_value=config.CURRENT_METRICS.get("TEST", 1.0),
        verbose=testability_verbose,
        log_path=testability_log_path
    )
    mdg_modularity = modularity_main(
        config.UDB_PATH,
        initial_value=config.CURRENT_METRICS.get("MODULE", 1.0)
    )
    mdg_distance = distance_main(
        config.UDB_PATH,
        initial_value=config.CURRENT_METRICS.get("DISTANCE", 1.0)
    )

    design_metrics = {
        "DSC": [design_quality_attribute.DSC],
        "NOH": [design_quality_attribute.NOH],
        "ANA": [design_quality_attribute.ANA],
        "MOA": [design_quality_attribute.MOA],
        "DAM": [design_quality_attribute.DAM],
        "CAMC": [design_quality_attribute.CAMC],
        "CIS": [design_quality_attribute.CIS],
        "NOM": [design_quality_attribute.NOM],
        "DCC": [design_quality_attribute.DCC],
        "MFA": [design_quality_attribute.MFA],
        "NOP": [design_quality_attribute.NOP]
    }

    quality_objectives = {
        "generation": [generation],
        "reusability": [design_quality_attribute.reusability],
        "understandability": [design_quality_attribute.understandability],
        "flexibility": [design_quality_attribute.flexibility],
        "functionality": [design_quality_attribute.functionality],
        "effectiveness": [design_quality_attribute.effectiveness],
        "extendability": [design_quality_attribute.extendability],
        "testability": [predicted_testability],
        "modularity": [mdg_modularity],
        "distance": [mdg_distance],
    }

    logger.info('QMOOD design metrics (N):')
    logger.info(design_metrics)

    logger.info('Objectives:')
    logger.info(quality_objectives)

    logger.info('QMOOD quality attributes sum:')
    logger.info(sum_)
    logger.info('QMOOD quality attributes mean:')
    logger.info(avg_)

    df_quality_attributes = pd.DataFrame(data=quality_objectives)
    if os.path.exists(quality_attributes_path):
        df = pd.read_csv(quality_attributes_path, index_col=False)
        df_result = pd.concat([df, df_quality_attributes], ignore_index=True)
        df_result.to_csv(quality_attributes_path, index=False)
    else:
        df_quality_attributes.to_csv(quality_attributes_path, index=False)

    df_design_metrics = pd.DataFrame(data=design_metrics)
    if os.path.exists(design_metrics_path):
        df = pd.read_csv(design_metrics_path, index_col=False)
        df_results = pd.concat([df, df_design_metrics], ignore_index=True)
        # df = df.append(df_design_metrics, ignore_index=True)
        df_results.to_csv(design_metrics_path, index=False)
    else:
        df_design_metrics.to_csv(design_metrics_path, index=False)


def main():
    """

    Optimization module main driver

    """

    # Define initialization objects
    initializer_class = SmellInitialization if config.WARM_START else RandomInitialization
    initializer_object = initializer_class(
        udb_path=config.UDB_PATH,
        population_size=config.POPULATION_SIZE,
        lower_band=config.LOWER_BAND,
        upper_band=config.UPPER_BAND
    )

    # -------------------------------------------
    # Define optimization problems
    problems = list()  # 0: Genetic (Single), 1: NSGA-II (Multi), 2: NSGA-III (Many), 3: RNSGA-III (Many), 4: UNSGA-III (Many), 5: AGEMOEA (Many) objectives problems
    problems.append(
        ProblemSingleObjective(
            n_objectives=config.NUMBER_OBJECTIVES,
            n_refactorings_lowerbound=config.LOWER_BAND,
            n_refactorings_upperbound=config.UPPER_BAND,
            evaluate_in_parallel=False,
        )
    )
    problems.append(
        ProblemMultiObjective(
            n_objectives=config.NUMBER_OBJECTIVES,
            n_refactorings_lowerbound=config.LOWER_BAND,
            n_refactorings_upperbound=config.UPPER_BAND,
            evaluate_in_parallel=False,
        )
    )
    problems.append(
        ProblemManyObjective(
            n_objectives=config.NUMBER_OBJECTIVES,
            n_refactorings_lowerbound=config.LOWER_BAND,
            n_refactorings_upperbound=config.UPPER_BAND,
            evaluate_in_parallel=False,
            verbose_design_metrics=True,
        )
    )
    # New
    problems.append(
        ProblemManyObjective(
            n_objectives=config.NUMBER_OBJECTIVES,
            n_refactorings_lowerbound=config.LOWER_BAND,
            n_refactorings_upperbound=config.UPPER_BAND,
            evaluate_in_parallel=False,
            verbose_design_metrics=True,
        )
    )
    problems.append(
        ProblemManyObjective(
            n_objectives=config.NUMBER_OBJECTIVES,
            n_refactorings_lowerbound=config.LOWER_BAND,
            n_refactorings_upperbound=config.UPPER_BAND,
            evaluate_in_parallel=False,
            verbose_design_metrics=True,
        )
    )
    problems.append(
        ProblemManyObjective(
            n_objectives=config.NUMBER_OBJECTIVES,
            n_refactorings_lowerbound=config.LOWER_BAND,
            n_refactorings_upperbound=config.UPPER_BAND,
            evaluate_in_parallel=False,
            verbose_design_metrics=True,
        )
    )

    # Define search algorithms
    algorithms = list()
    # 1: GA
    alg1 = GA(
        pop_size=config.POPULATION_SIZE,
        sampling=PopulationInitialization(initializer_object),
        crossover=AdaptiveSinglePointCrossover(prob=config.CROSSOVER_PROBABILITY),
        # crossover=get_crossover("real_k_point", n_points=2),
        mutation=BitStringMutation(prob=config.MUTATION_PROBABILITY, initializer=initializer_object),
        eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list),
        n_gen=config.NGEN,
    )
    algorithms.append(alg1)

    # 2: NSGA-II
    alg2 = NSGA2(
        pop_size=config.POPULATION_SIZE,
        sampling=PopulationInitialization(initializer_object),
        crossover=AdaptiveSinglePointCrossover(prob=config.CROSSOVER_PROBABILITY),
        # crossover=get_crossover("real_k_point", n_points=2),
        mutation=BitStringMutation(prob=config.MUTATION_PROBABILITY, initializer=initializer_object),
        eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list),
        n_gen=config.NGEN,
    )
    algorithms.append(alg2)

    # 3: NSGA-III
    # pop_size must be equal or larger than the number of reference directions
    number_of_references_points = config.POPULATION_SIZE - int(config.POPULATION_SIZE * 0.20)
    ref_dirs = get_reference_directions(
        'energy',  # algorithm
        config.NUMBER_OBJECTIVES,  # number of objectives
        number_of_references_points,  # number of reference directions
        seed=1
    )
    alg3 = NSGA3(
        ref_dirs=ref_dirs,
        pop_size=config.POPULATION_SIZE,  # 200
        sampling=PopulationInitialization(initializer_object),
        selection=TournamentSelection(func_comp=binary_tournament),
        crossover=AdaptiveSinglePointCrossover(prob=config.CROSSOVER_PROBABILITY, ),
        # crossover=get_crossover("real_k_point", n_points=2),
        mutation=BitStringMutation(prob=config.MUTATION_PROBABILITY, initializer=initializer_object),
        eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list),
        n_gen=config.NGEN,
    )
    algorithms.append(alg3)

    # # New
    # 4: RNSGA-III
    # pop_size must be equal or larger than the number of reference directions
    number_of_references_points = config.POPULATION_SIZE - int(config.POPULATION_SIZE * 0.20)
    ref_dirs = get_reference_directions(
        'energy',  # algorithm
        config.NUMBER_OBJECTIVES,  # number of objectives
        number_of_references_points,  # number of reference directions
        seed=1
    )

    alg4 = RNSGA3(
        # ref_points=np.array([[0.3, 0.4, 0.1, 0.5, 0.7, 0, 0.1, 0.6], [0.8, 0.5, 0.2, 0.1, 0.8, 0.5, 0.2, 0.1]]),
        # ref_dirs=ref_dirs,
        # pop_size=config.POPULATION_SIZE,  # 200
        ref_points=ref_dirs,
        pop_per_ref_point=config.POPULATION_SIZE,  # 50
        sampling=PopulationInitialization(initializer_object),
        selection=TournamentSelection(func_comp=binary_tournament),
        crossover=AdaptiveSinglePointCrossover(prob=config.CROSSOVER_PROBABILITY, ),
        # crossover=get_crossover("real_k_point", n_points=2),
        mutation=BitStringMutation(prob=config.MUTATION_PROBABILITY, initializer=initializer_object),
        eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list),
        n_gen=config.NGEN,
        # mu=0.1,
    )
    algorithms.append(alg4)

    # 5:UNSGA-III
    # pop_size must be equal or larger than the number of reference directions
    number_of_references_points = config.POPULATION_SIZE - int(config.POPULATION_SIZE * 0.20)
    ref_dirs = get_reference_directions(
        'energy',  # algorithm
        config.NUMBER_OBJECTIVES,  # number of objectives
        number_of_references_points,  # number of reference directions
        seed=1
    )
    alg4 = UNSGA3(
        ref_dirs=ref_dirs,
        pop_size=config.POPULATION_SIZE,  # 200
        sampling=PopulationInitialization(initializer_object),
        selection=TournamentSelection(func_comp=binary_tournament),
        crossover=AdaptiveSinglePointCrossover(prob=config.CROSSOVER_PROBABILITY, ),
        # crossover=get_crossover("real_k_point", n_points=2),
        mutation=BitStringMutation(prob=config.MUTATION_PROBABILITY, initializer=initializer_object),
        eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list),
        n_gen=config.NGEN,
    )
    algorithms.append(alg4)

    # 6: AGEMOEA
    alg5 = AGEMOEA(
        #ref_dirs=ref_dirs,
        pop_size=config.POPULATION_SIZE,  # 200
        sampling=PopulationInitialization(initializer_object),
        selection=TournamentSelection(func_comp=binary_tournament),
        crossover=AdaptiveSinglePointCrossover(prob=config.CROSSOVER_PROBABILITY, ),
        # crossover=get_crossover("real_k_point", n_points=2),
        mutation=BitStringMutation(prob=config.MUTATION_PROBABILITY, initializer=initializer_object),
        eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list),
        n_gen=config.NGEN,
    )
    algorithms.append(alg5)


    # Termination of algorithms
    my_termination = MultiObjectiveDefaultTermination(
        x_tol=None,
        cv_tol=None,
        f_tol=0.0015,
        nth_gen=5,
        n_last=5,
        n_max_gen=config.MAX_ITERATIONS,  # about 1000 - 1400
        n_max_evals=1e6
    )

    # Do optimization for various problems with various algorithms
    res = minimize(
        problem=problems[config.PROBLEM],
        algorithm=algorithms[config.PROBLEM],
        termination=my_termination,
        seed=1,
        verbose=False,
        copy_algorithm=True,
        copy_termination=True,
        save_history=False,
        callback=LogCallback(),
    )
    # np.save('checkpoint', res.algorithm)

    # Log results
    logger.info(f"***** Algorithm was finished in {res.algorithm.n_gen + config.NGEN} generations *****")
    logger.info(" ")
    logger.info("============ time information ============")
    logger.info(f"Start time: {datetime.fromtimestamp(res.start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"End time: {datetime.fromtimestamp(res.end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Execution time in seconds: {res.exec_time}")
    logger.info(f"Execution time in minutes: {res.exec_time / 60}")
    logger.info(f"Execution time in hours: {res.exec_time / (60 * 60)}")
    # logger.info(f"Number of generations: {res.algorithm.n_gen}")
    # logger.info(f"Number of generations", res.algorithm.termination)

    # Log optimum solutions
    logger.info("============ All opt solutions ============")
    for i, ind in enumerate(res.opt):
        logger.info(f'Opt refactoring sequence {i}:')
        logger.info(ind.X)
        logger.info(f'Opt refactoring sequence corresponding objectives vector {i}:')
        logger.info(ind.F)
        logger.info("-" * 75)

    # Log best refactorings
    logger.info("============ Best refactoring sequences (a set of non-dominated solutions) ============")
    for i, ind in enumerate(res.X):
        logger.info(f'Best refactoring sequence {i}:')
        logger.info(ind)
        logger.info("-" * 75)
    logger.info("============ Best objective values (a set of non-dominated solutions) ============")
    for i, ind_objective in enumerate(res.F):
        logger.info(f'Best refactoring sequence corresponding objectives vector {i}:')
        logger.info(ind_objective)
        logger.info("-" * 75)

    # Save best refactorings
    population_trimmed = []
    objective_values_content = ''
    for chromosome in res.X:
        chromosome_new = []
        if config.PROBLEM == 0:  # i.e., single objective problem
            for gene_ in chromosome:
                chromosome_new.append((gene_.name, gene_.params))
        else:
            for gene_ in chromosome[0]:
                chromosome_new.append((gene_.name, gene_.params))
        population_trimmed.append(chromosome_new)

    for objective_vector in res.F:
        objective_values_content += f'{res.algorithm.n_gen + config.NGEN},'
        if config.PROBLEM == 0:
            objective_values_content += f'{objective_vector},'
        else:
            for objective_ in objective_vector:
                objective_values_content += f'{objective_},'
        objective_values_content += '\n'

    best_refactoring_sequences_path = os.path.join(
        config.PROJECT_LOG_DIR,
        f'best_refactoring_sequences_after_{res.algorithm.n_gen + config.NGEN}gens.json'
    )
    with open(best_refactoring_sequences_path, mode='w', encoding='utf-8') as fp:
        json.dump(population_trimmed, fp, indent=4)

    best_refactoring_sequences_objectives_path = os.path.join(
        config.PROJECT_LOG_DIR,
        f'best_refactoring_sequences_objectives_after_{res.algorithm.n_gen + config.NGEN}gens.csv'
    )
    with open(best_refactoring_sequences_objectives_path, mode='w', encoding='utf-8') as fp:
        fp.write(objective_values_content)

    try:
        pf = res.F
        # dm = HighTradeoffPoints()
        dm = get_decision_making("high-tradeoff")
        I = dm.do(pf)

        logger.info("============ High-tradeoff points refactoring sequences ============")
        for i, ind in enumerate(res.X[I]):
            logger.info(f'High tradeoff points refactoring sequence {i}:')
            logger.info(ind)
            logger.info("-" * 75)
        logger.info("============ High-tradeoff points objective values  ============")
        for i, ind_objective in enumerate(pf[I]):
            logger.info(f'High-tradeoff points refactoring sequence corresponding objectives vector {i}:')
            logger.info(ind_objective)
            logger.info("-" * 75)

        logger.info("High-tradeoff points mean:")
        logger.info(np.mean(pf[I], axis=0))
        logger.info("High-tradeoff points median:")
        logger.info(np.median(pf[I], axis=0))

        # Save high-tradeoff refactorings
        population_trimmed = []
        objective_values_content = ''
        for chromosome in res.X[I]:
            chromosome_new = []
            if config.PROBLEM == 0:  # i.e., single objective problem
                for gene_ in chromosome:
                    chromosome_new.append((gene_.name, gene_.params))
            else:
                for gene_ in chromosome[0]:
                    chromosome_new.append((gene_.name, gene_.params))
            population_trimmed.append(chromosome_new)

        for objective_vector in pf[I]:
            objective_values_content += f'{res.algorithm.n_gen + config.NGEN},'
            if config.PROBLEM == 0:
                objective_values_content += f'{objective_vector},'
            else:
                for objective_ in objective_vector:
                    objective_values_content += f'{objective_},'
            objective_values_content += '\n'

        high_tradeoff_path = os.path.join(
            config.PROJECT_LOG_DIR,
            f'high_tradeoff_points_refactoring_after_{res.algorithm.n_gen + config.NGEN}gens.json'
        )
        with open(high_tradeoff_path, mode='w', encoding='utf-8') as fp:
            json.dump(population_trimmed, fp, indent=4)

        high_tradeoff_path_objectives_path = os.path.join(
            config.PROJECT_LOG_DIR,
            f'high_tradeoff_points_after_{res.algorithm.n_gen + config.NGEN}gens.csv'
        )
        with open(high_tradeoff_path_objectives_path, mode='w', encoding='utf-8') as fp:
            fp.write(objective_values_content)

    except:
        logger.error("No multi-optimal solutions (error in computing high tradeoff points)!")


# CodART search-based refactoring module main driver
if __name__ == '__main__':
    # print(logger.handlers)
    config.log_experiment_info()
    logger.info('============ Objectives values before Refactoring ============')
    log_project_info(reset_=True)
    # quit()
    main()
