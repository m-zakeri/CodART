"""
This module implements the search-based refactoring with various search strategy
using pymoo framework.

## Changelog
### version 2
    1. Crossover function is added.
    2. Termination criteria are added.
    3. Computation of highly trade-off points is added.
    4. Tournament-selection is added.
    5. _evaluate function in NSGA-III is now works on population instead of an individual (population-based versus element-wise).
    6. Other setting for NSGA-III including adding energy-references point instead of Das and Dennis approach.
    ===

Gene, RefactoringOperation: One refactoring with params
Individual: A list of RefactoringOperation
PureRandomInitialization: Population, list of Individual

## References
[1] https://pymoo.org/customization/custom.html
[2] https://pymoo.org/misc/reference_directions.html

"""

__version__ = '0.2.0'
__author__ = 'Morteza Zakeri, Seyyed Ali Ayati'

import random
from copy import deepcopy
from multiprocessing import Process, Array
from typing import List

import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.crossover import Crossover
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from pymoo.core.mutation import Mutation
from pymoo.core.problem import ElementwiseProblem, Problem
from pymoo.core.sampling import Sampling
from pymoo.factory import get_reference_directions, get_decision_making
from pymoo.operators.selection.tournament import TournamentSelection
from pymoo.optimize import minimize
from pymoo.util.termination.default import MultiObjectiveDefaultTermination

from metrics.modularity import main as modularity_main
from metrics.testability_prediction import main as testability_main
from sbse import config
from sbse.config import logger
from sbse.initialize import RandomInitialization
from sbse.objectives import Objectives
from utilization.directory_utils import update_understand_database, git_restore


class Gene:
    """
    The base class for the Gene in genetic algorithms
    """

    def __init__(self, **kwargs):
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
    """

    def __init__(self, **kwargs):
        """
        Each refactoring operation hold as a dictionary contains the required parameters.

        Example:
            make_field_static refactoring is marshaled as the following dict:
            params = {
                'refactoring_name': 'make_field_static'
                'api': 'main_function'
                'source_class': 'name_of_source_class'
                'field_name': 'name_of_the_field_to_be_static'
            }

        """
        super(RefactoringOperation, self).__init__(**kwargs)

    def __str__(self):
        return f'{self.name}({self.params})\n'

    def __repr__(self):
        return self.__str__()

    def do_refactoring(self):
        """ Check preconditions and apply refactoring operation to source code"""
        logger.info(f"Running {self.name}")
        logger.info(f"Parameters {self.params}")
        try:
            self.main(**self.params)
        except Exception as e:
            logger.error(f"Error in executing refactoring:\n {e}")

    @classmethod
    def generate_randomly(cls):
        initializer = RandomInitialization(udb_path=config.UDB_PATH)
        item = initializer.select_random()
        return cls(
            name=item[2],
            params=item[1],
            main=item[0]
        )


class Individual(List):
    """
    The class define a data structure (list) to hold an individual during the search process.
    Each individual (also called, chromosome or solution in the context of genetic programming)
    is an array of refactoring operations
    where the order of their execution is accorded by their positions in the array.
    """

    def __init__(self):
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


class ProblemSingleObjective(ElementwiseProblem):
    """
        The CodART single-objective optimization work with only one objective, testability:
        """

    def __init__(self, n_refactorings_lowerbound=50, n_refactorings_upperbound=75):
        super(ProblemSingleObjective, self).__init__(n_var=1,
                                                     n_obj=1,
                                                     n_constr=0)
        self.n_refactorings_lowerbound = n_refactorings_lowerbound
        self.n_refactorings_upperbound = n_refactorings_upperbound

    def _evaluate(self,
                  x,  #
                  out,
                  *args,
                  **kwargs):
        """
        This method iterate over an Individual, execute the refactoring operation sequentially,
        and compute quality attributes for the refactored version of the program, as objectives of the search

        params:
        x[0] (Individual): x[0] is an instance of Individual (i.e., a list of refactoring operations)

        """
        # Stage 0: Git restore
        logger.debug("Executing git restore.")
        git_restore(config.PROJECT_PATH)
        update_understand_database(config.UDB_PATH)
        # Stage 1: Execute all refactoring operations in the sequence x
        logger.debug(f"Reached Individual with Size {len(x[0])}")
        for refactoring_operation in x[0]:
            refactoring_operation.do_refactoring()
            # Update Understand DB
            update_understand_database(config.UDB_PATH)
        # Stage 2: Computing quality attributes
        score = testability_main(
            config.UDB_PATH,
            initial_value=config.CURRENT_METRICS.get("TEST", 1.0)
        )
        logger.info(f"Testability Score: {score}")
        # Stage 3: Marshal objectives into vector
        out["F"] = np.array([-1 * score], dtype=float)


class ProblemMultiObjective(ElementwiseProblem):
    """
    The CodART multi-objective optimization work with three objective:
        Objective 1: Mean value of QMOOD metrics
        Objective 2: Testability
        Objective 3: Modularity
    """

    def __init__(self, n_refactorings_lowerbound=50, n_refactorings_upperbound=75):
        super(ProblemMultiObjective, self).__init__(n_var=1,
                                                    n_obj=3,
                                                    n_constr=0)
        self.n_refactorings_lowerbound = n_refactorings_lowerbound
        self.n_refactorings_upperbound = n_refactorings_upperbound

    def _evaluate(self,
                  x,  #
                  out,
                  *args,
                  **kwargs):
        """
        This method iterate over an Individual, execute the refactoring operation sequentially,
        and compute quality attributes for the refactored version of the program, as objectives of the search

        params:
        x (Individual): x is an instance of Individual (i.e., a list of refactoring operations)

        """
        # Stage 0: Git restore
        logger.debug("Executing git restore.")
        git_restore(config.PROJECT_PATH)
        update_understand_database(config.UDB_PATH)
        # Stage 1: Execute all refactoring operations in the sequence x
        logger.debug(f"Reached Individual with Size {len(x[0])}")
        for refactoring_operation in x[0]:
            refactoring_operation.do_refactoring()
            # Update Understand DB
            update_understand_database(config.UDB_PATH)

        # Stage 2: Computing quality attributes
        obj = Objectives(udb_path=config.UDB_PATH)
        o1 = obj.average
        del obj
        o2 = testability_main(
            config.UDB_PATH,
            initial_value=config.CURRENT_METRICS.get("TEST", 1.0)
        )
        o3 = modularity_main(
            config.UDB_PATH,
            initial_value=config.CURRENT_METRICS.get("MODULE", 1.0)
        )
        logger.info(f"QMOOD AVG Score: {o1}")
        logger.info(f"Testability Score: {o2}")
        logger.info(f"Modularity Score: {o3}")
        # Stage 3: Marshal objectives into vector
        out["F"] = np.array([-1 * o1, -1 * o2, -1 * o3], dtype=float)


def calc_qmood_objectives(arr_):
    qmood = Objectives(udb_path=config.UDB_PATH)
    arr_[0] = qmood.reusability
    arr_[1] = qmood.understandability
    arr_[2] = qmood.flexibility
    arr_[3] = qmood.functionality
    arr_[4] = qmood.effectiveness
    arr_[5] = qmood.extendability


def calc_testability_objective(path_, initial_value, arr_):
    arr_[6] = testability_main(
        path_,
        initial_value=config.CURRENT_METRICS.get("TEST", 1.0)
    )


def calc_modularity_objective(path_, arr_):
    arr_[7] = modularity_main(
        path_,
        initial_value=config.CURRENT_METRICS.get("MODULE", 1.0)
    )


class ProblemManyObjective(Problem):
    """
    The CodART many-objective optimization work with eight objective:
        Objective 1 to 6: QMOOD metrics
        Objective 7: Testability
        Objective 8: Modularity
    """

    def __init__(self, n_refactorings_lowerbound=50, n_refactorings_upperbound=75):
        super(ProblemManyObjective, self).__init__(n_var=1,
                                                   n_obj=8,
                                                   n_constr=0)
        self.n_refactorings_lowerbound = n_refactorings_lowerbound
        self.n_refactorings_upperbound = n_refactorings_upperbound

    def _evaluate(self,
                  x,  #
                  out,
                  *args,
                  **kwargs):
        """
        By default, elementwise_evaluation is set to False, which implies the _evaluate retrieves a set of solutions.

        params:
            x (Population): x is a matrix where each row is an individual, and each column a variable.
            We have one variable of type list (Individual) ==> x.shape = (len(Population), 1)

        """

        objective_values = []
        for k, individual_ in enumerate(x):
            # Stage 0: Git restore
            logger.debug("Executing git restore.")
            git_restore(config.PROJECT_PATH)
            update_understand_database(config.UDB_PATH)

            # Stage 1: Execute all refactoring operations in the sequence x
            logger.debug(f"Reached an Individual with size {len(individual_[0])}")
            for refactoring_operation in individual_[0]:
                refactoring_operation.do_refactoring()
                # Update Understand DB
                update_understand_database(config.UDB_PATH)

            # Stage 2: Computing quality attributes in parallel
            arr = Array('d', range(8))
            p1 = Process(target=calc_qmood_objectives, args=(arr,))
            p2 = Process(target=calc_testability_objective, args=(config.UDB_PATH, arr,))
            p3 = Process(target=calc_modularity_objective, args=(config.UDB_PATH, arr,))
            p1.start(), p2.start(), p3.start()
            p1.join(), p2.join(), p3.join()

            # qmood = Objectives(udb_path=config.UDB_PATH)
            # o1 = qmood.reusability
            # o2 = qmood.understandability
            # o3 = qmood.flexibility
            # o4 = qmood.functionality
            # o5 = qmood.effectiveness
            # o6 = qmood.extendability
            # del qmood
            # o7 = testability_main(config.UDB_PATH)
            # o8 = modularity_main(config.UDB_PATH)

            # logger.info(f'Reusability Score: {o1}')
            # logger.info(f'Understandability Score: {o2}')
            # logger.info(f'Flexibility Score: {o3}')
            # logger.info(f'Functionality Score: {o4}')
            # logger.info(f'Effectiveness Score: {o5}')
            # logger.info(f'Extendability Score: {o6}')
            # logger.info(f'Testability Score: {o7}')
            # logger.info(f'Modularity Score: {o8}')

            # Stage 3: Marshal objectives into vector
            # objective_values.append([-1 * o1, -1 * o2, -1 * o3, -1 * o4, -1 * o5, -1 * o6, -1 * o7, -1 * o8, ])
            objective_values.append([-1 * i for i in arr])
            logger.info(f"Objective values for individual {k}: {[i for i in arr]}")

        # Stage 4: Marshal all objectives into out dictionary
        out['F'] = np.array(objective_values, dtype=float)
        # print('OUT', out['F'])


class PureRandomInitialization(Sampling):
    """
    This class create the initial population, X, consists of n_samples, pop_size.
    For each refactoring operation, a set of controlling parameters (e.g., actors and roles) is picked based on
    existing code smells in the program to be refactored.
    The selected refactoring operations are randomly arranged in each individual.
    Assigning randomly a sequence of refactorings to certain code fragments generates the initial population
    """

    def _do(self, problem, n_samples, **kwargs):
        """
        Since the problem having only one variable, we return a matrix with the shape (n,1)
        Params:

            n_samples (int): the same population size, pop_size

        """

        X = np.full((n_samples, 1), None, dtype=Individual)
        population = RandomInitialization(
            udb_path=config.UDB_PATH,
            population_size=n_samples,
            lower_band=problem.n_refactorings_lowerbound,
            upper_band=problem.n_refactorings_upperbound
        ).generate_population()

        for i in range(n_samples):
            individual_object = []  # list of refactoring operations (Temporarily used instead of Individual class)
            for ref in population[i]:
                individual_object.append(
                    RefactoringOperation(
                        name=ref[2],
                        params=ref[1],
                        main=ref[0]
                    )
                )
            X[i, 0] = individual_object
        return X


class AdaptiveSinglePointCrossover(Crossover):
    """
    This class implements solution variation, the adaptive one-point or single-point crossover operator.
    The crossover operator combines parents to create offsprings.
    It starts by selecting and splitting at random two parent solutions or individuals.
    Then, this operator creates two child solutions by putting, for the first child,
    the first part of the first parent with the second part of the second parent,
    and vice versa for the second child.

    Note 1: In the pymoo framework, the crossover operator retrieves the input already with predefined matings.
    The default parent selection algorithm is TournamentSelection.

    Note 2: It is better to create children that are close to their parents to have a more efficient search process,
    a so-called __adaptive crossover__, specifically in many-objective optimization.
    Therefore, the cutting point of the one-point crossover operator are controlled by restricting its position
    to be either belonging to the first tier of the refactoring sequence or belonging to the last tier.

    Params:
        prob (float): crossover probability
    """

    def __init__(self, prob=0.9):

        # Define the crossover: number of parents, number of offsprings, and cross-over probability
        super().__init__(n_parents=2, n_offsprings=2, prob=prob)

    def _do(self, problem, X, **kwargs):
        """
        For population X
        """
        print("Running crossover")
        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, n_var = X.shape

        # The output will be with the shape (n_offsprings, n_matings, n_var)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=object)

        # print(X.shape)
        # print(X)
        print('=' * 50)

        # for each mating provided
        for k in range(n_matings):
            # get the first and the second parent (a and b are instance of individuals)
            a, b = X[0, k, 0], X[1, k, 0]
            # print('### a', a)
            # print('### b', b)
            # print('len a', len(a))
            # print('len b', len(b))

            len_min = min(len(a), len(b))
            print(' int(len_min*0.30)', int(len_min * 0.30))
            print(' int(len_min*0.70)', int(len_min * 0.70))
            cross_point_1 = random.randint(1, int(len_min * 0.30))
            cross_point_2 = random.randint(int(len_min * 0.70), len_min - 1)
            if random.random() < 0.5:
                cross_point_final = cross_point_1
            else:
                cross_point_final = cross_point_2
            print('cross_point_final', cross_point_final)
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
    if x<0.2 we change the refactoring operation in that dimension, otherwise no change is took into account.

    """

    def __init__(self, prob=0.2):
        super().__init__()
        self.mutation_probability = prob

    def _do(self, problem, X, **kwargs):
        for i, individual in enumerate(X):
            r = np.random.random()
            # with a probability of `mutation_probability` replace the refactoring operation with new one
            if r < self.mutation_probability:
                # j is a random index in individual
                j = random.randint(0, len(individual[0]) - 1)
                random_refactoring_operation = RefactoringOperation.generate_randomly()
                X[i][0][j] = random_refactoring_operation

        return X


# Calling the equal method of individual class
def is_equal_2_refactorings_list(a, b):
    """
    This method implement is_equal method which should return True if two instances of Individual class are equal.
    Otherwise it return False.
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
    # The P input defines the tournaments and competitors
    n_tournaments, n_competitors = P.shape
    if n_competitors != 2:
        raise Exception("Only pressure=2 allowed for binary tournament!")
    S = np.full(n_tournaments, -1, dtype=np.int64)

    # now do all the tournaments
    for i in range(n_tournaments):
        a, b = P[i]
        # if the first individual is better, choose it
        if pop[a].F.all() <= pop[a].F.all():
            S[i] = a
        # otherwise take the other individual
        else:
            S[i] = b

    return S


def main():
    # Define search algorithms
    algorithms = list()
    # 1: GA
    algorithm = GA(pop_size=config.POPULATION_SIZE,
                   sampling=PureRandomInitialization(),
                   crossover=AdaptiveSinglePointCrossover(prob=0.9),
                   # crossover=get_crossover("real_k_point", n_points=2),
                   mutation=BitStringMutation(prob=0.1),
                   eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list)
                   )
    algorithms.append(algorithm)

    # 2: NSGA II
    algorithm = NSGA2(pop_size=config.POPULATION_SIZE,
                      sampling=PureRandomInitialization(),
                      crossover=AdaptiveSinglePointCrossover(prob=0.9),
                      # crossover=get_crossover("real_k_point", n_points=2),
                      mutation=BitStringMutation(prob=0.1),
                      eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list)
                      )
    algorithms.append(algorithm)

    # 3: NSGA III
    # pop_size must be equal or larger than the number of reference directions
    number_of_references_points = config.POPULATION_SIZE - int(config.POPULATION_SIZE * 0.20)
    ref_dirs = get_reference_directions('energy',  # algorithm
                                        8,  # number of objectives
                                        number_of_references_points,  # number of reference directions
                                        seed=1)
    algorithm = NSGA3(ref_dirs=ref_dirs,
                      pop_size=config.POPULATION_SIZE,  # 200
                      sampling=PureRandomInitialization(),
                      selection=TournamentSelection(func_comp=binary_tournament),
                      crossover=AdaptiveSinglePointCrossover(prob=0.8),
                      # crossover=get_crossover("real_k_point", n_points=2),
                      mutation=BitStringMutation(prob=0.2),
                      eliminate_duplicates=ElementwiseDuplicateElimination(cmp_func=is_equal_2_refactorings_list)
                      )
    algorithms.append(algorithm)

    # -------------------------------------------
    # Define problems
    problems = list()
    problems.append(ProblemSingleObjective(n_refactorings_lowerbound=config.LOWER_BAND,
                                           n_refactorings_upperbound=config.UPPER_BAND))
    problems.append(ProblemMultiObjective(n_refactorings_lowerbound=config.LOWER_BAND,
                                          n_refactorings_upperbound=config.UPPER_BAND))
    problems.append(ProblemManyObjective(n_refactorings_lowerbound=config.LOWER_BAND,
                                         n_refactorings_upperbound=config.UPPER_BAND))

    # Termination of algorithms
    my_termination = MultiObjectiveDefaultTermination(
        x_tol=None,
        cv_tol=None,
        f_tol=0.0015,
        nth_gen=10,
        n_last=20,
        n_max_gen=config.MAX_ITERATIONS,  # about 1000 - 1400
        n_max_evals=1e6
    )

    # Do optimization for various problems with various algorithms
    res = minimize(problem=problems[2],
                   algorithm=algorithms[2],
                   termination=my_termination,
                   seed=1,
                   verbose=False,
                   copy_algorithm=True,
                   copy_termination=True,
                   save_history=False,
                   )
    # np.save('checkpoint', res.algorithm)

    # Log results
    logger.info("\n** FINISHED **\n")
    logger.info("Best refactoring sequences (a set of non-dominated solutions):")
    logger.info(res.X)
    logger.info("Best objective values (a set of non-dominated solutions):")
    logger.info(res.F)

    logger.info("=" * 75)
    logger.info("Other solutions:")
    for ind in res.opt:
        logger.info(ind.X)
        logger.info(ind.F)
        logger.info("-" * 50)
    logger.info("=" * 75)

    logger.info(f"Start time: {res.start_time}")
    logger.info(f"End time: {res.end_time}")
    logger.info(f"Execution time in seconds: {res.exec_time}")
    logger.info(f"Execution time in minutes: {res.exec_time / 60}")
    logger.info(f"Execution time in hours: {res.exec_time / (60 * 60)}")
    logger.info(f"Number of generations: {res.algorithm.n_gen}")
    # logger.info(f"Number of generations", res.algorithm.termination)

    pf = res.F
    # dm = HighTradeoffPoints()
    dm = get_decision_making("high-tradeoff")
    try:
        I = dm.do(pf)
        logger.info(f"High tradeoff points: {pf[I][0]}")
        logger.info(f"High tradeoff points corresponding refactorings: {res.X[I]}")
        logger.info(f"The mean improvement of quality attributes: {np.mean(pf[I][0], axis=0)}")
        logger.info(f"The median improvement of quality attributes: {np.median(pf[I][0], axis=0)}")
    except:
        logger.info("No multi optimal solutions (error in computing high tradeoff points)!")


# Test driver
if __name__ == '__main__':
    config.log_project_info()
    main()
