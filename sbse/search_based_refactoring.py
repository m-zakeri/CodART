"""
This module implements the search-based refactoring with various search strategy
using pymoo framework.

Gene, RefactoringOperation: One refactoring with params
Individual: A list of RefactoringOperation
SudoRandomInitialization: Population, list of Individual

## References
[1] https://pymoo.org/customization/custom.html
[2] https://pymoo.org/misc/reference_directions.html

"""

__version__ = '0.1.0'
__author__ = 'Morteza Zakeri, Seyyed Ali Ayati'

import logging
import os
import random
from typing import List

import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.factory import get_reference_directions, get_crossover
from pymoo.core.crossover import Crossover
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from pymoo.core.mutation import Mutation
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.sampling import Sampling
from pymoo.optimize import minimize

from sbse import config
from sbse.initialize import RandomInitialization
from sbse.objectives import Objectives
from metrics.testability_prediction import main as testability_main
from metrics.modularity import main as modularity_main
from utilization.directory_utils import update_understand_database, git_restore

# Config logging
logging.basicConfig(filename='codart_result.log', level=logging.DEBUG)
logger = logging.getLogger(os.path.basename(__file__))


class Gene:
    """
    The base class for the Gene in genetic algorithms
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.params = kwargs.get('params')
        self.main = kwargs.get('main')

    def __str__(self):
        return self.name


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

    def do_refactoring(self):
        logger.info(f"Running {self.name}")
        logger.info(f"Parameters {self.params}")
        try:
            self.main(**self.params)
        except Exception as e:
            logger.error(f"Error in executing refactoring:\n {e}")

    @classmethod
    def generate_randomly(cls):
        initializer = RandomInitialization(udb_path=config.UDB_PATH)
        item = random.choice(initializer.initializers)()
        initializer.und.close()
        logger.info("Database close after generating a single refactoring.")
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
        # Stage 1: Execute all refactoring operations in the sequence x
        logger.debug(f"Individual size is {len(x[0])}")
        for refactoring_operation in x[0]:
            refactoring_operation.do_refactoring()
            # Update Understand DB
            update_understand_database(config.UDB_PATH)
        # Stage 2: Computing quality attributes
        # TODO: Add testability and modularity objectives
        score = Objectives(udb_path=config.UDB_PATH).reusability
        logger.info(f"Reusability score is {score}")
        # Stage 3: Marshal objectives into vector
        # out["F"] = np.array([-1 * o1], dtype=float)
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
        git_restore(config.PROJECT_PATH)
        # Stage 1: Execute all refactoring operations in the sequence x
        for refactoring_operation in x[0]:
            refactoring_operation.do_refactoring()
            # Update Understand DB
            update_understand_database(config.UDB_PATH)

        # Stage 2: Computing quality attributes
        # Todo: Add testability and modularity objectives
        # Todo: Normalize objective values in a standard range
        # Todo: Reduce QMOOD metrics to one objective by averaging them
        o1 = Objectives.reusability
        o2 = Objectives.understandability
        # o1 = 1/6 * sum qmood metrics
        # o2 = testability  ## Our new objective
        # o3 = modularity   ## Our new objective

        # Stage 3: Marshal objectives into vector
        out["F"] = np.array([-1 * o1, -1 * o2], dtype=float)


class ProblemManyObjective(ElementwiseProblem):
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
        This method iterate over an Individual, execute the refactoring operation sequentially,
        and compute quality attributes for the refactored version of the program, as objectives of the search

        params:
        x (Individual): x is an instance of Individual (i.e., a list of refactoring operations)

        """
        # Git restore
        git_restore(config.PROJECT_PATH)
        # Stage 1: Execute all refactoring operations in the sequence x
        for refactoring_operation in x[0]:
            refactoring_operation.do_refactoring()
            # Update Understand DB
            update_understand_database(config.UDB_PATH)

        # Stage 2: Computing quality attributes
        # Todo: Add testability and modularity objectives
        # Todo: Normalize objective values in a standard range
        qmood = Objectives(udb_path=config.UDB_PATH)
        o1 = qmood.reusability
        o2 = qmood.understandability
        o3 = qmood.flexibility
        o4 = qmood.functionality
        o5 = qmood.effectiveness
        o6 = qmood.extendability
        o7 = testability_main(config.UDB_PATH)
        o8 = modularity_main(config.UDB_PATH)

        # Stage 3: Marshal objectives into vector
        out["F"] = np.array([-1 * o1, -1 * o2, -1 * o3, -1 * o4, -1 * o5, -1 * o6, -1 * o7, -1 * o8, ], dtype=float)


class SudoRandomInitialization(Sampling):
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
            individual_object = []  # list of refactoring operations
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
        Todo: Implementing adaptive single-point-cross-over
        """
        print("Running crossover")
        # The input of has the following shape (n_parents, n_matings, n_var)
        # print(X.shape)
        # print(X)
        # print('='*50)
        _, n_matings, n_var = X.shape

        # The output will be with the shape (n_offsprings, n_matings, n_var)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=np.object)

        # for each mating provided
        for k in range(n_matings):

            # get the first and the second parent
            a, b = X[0, k, 0], X[1, k, 0]

            # prepare the offsprings
            off_a = ["_"] * problem.n_characters
            off_b = ["_"] * problem.n_characters

            for i in range(problem.n_characters):
                if np.random.random() < 0.5:
                    off_a[i] = a[i]
                    off_b[i] = b[i]
                else:
                    off_a[i] = b[i]
                    off_b[i] = a[i]

            # join the character list and set the output
            Y[0, k, 0], Y[1, k, 0] = "".join(off_a), "".join(off_b)

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
                j = random.randint(0, len(individual[0]))
                random_refactoring_operation = RefactoringOperation.generate_randomly()
                X[i][0][j] = random_refactoring_operation

        return X


class RefactoringSequenceDuplicateElimination(ElementwiseDuplicateElimination):
    """
    This class implement is_equal method which should return True if two instances of Individual are equal.
    Otherwise it return False.

    The duplicate instances are removed from population at each generation.
    Only one instance is held to speed up the search algorithm

    """

    def is_equal(self, a, b):
        """
        # Calling the equal method of individual class
        """
        return a.X[0] == b.X[0]


def main():
    # Define search algorithms
    algorithms = list()
    # 1: GA
    algorithm = GA(
        pop_size=config.POPULATION_SIZE,
        sampling=SudoRandomInitialization(),
        # crossover=AdaptiveSinglePointCrossover(prob=0.8),
        crossover=get_crossover("real_k_point", n_points=2),
        mutation=BitStringMutation(),
        eliminate_duplicates=RefactoringSequenceDuplicateElimination()
    )
    algorithms.append(algorithm)

    # 2: NSGA II
    algorithm = NSGA2(pop_size=config.POPULATION_SIZE,
                      sampling=SudoRandomInitialization(),
                      # crossover=AdaptiveSinglePointCrossover(prob=0.8),
                      crossover=get_crossover("real_k_point", n_points=2),
                      mutation=BitStringMutation(),
                      eliminate_duplicates=RefactoringSequenceDuplicateElimination()
                      )
    algorithms.append(algorithm)

    # 3: NSGA III
    # Todo: Ask for best practices in determining ref_dirs
    ref_dirs = get_reference_directions("energy", 8, 90, seed=1)
    algorithm = NSGA3(ref_dirs=ref_dirs,
                      pop_size=config.POPULATION_SIZE,
                      sampling=SudoRandomInitialization(),
                      # crossover=AdaptiveSinglePointCrossover(prob=0.8),
                      crossover=get_crossover("real_k_point", n_points=2),
                      mutation=BitStringMutation(),
                      eliminate_duplicates=RefactoringSequenceDuplicateElimination()
                      )
    algorithms.append(algorithm)

    # Define problems
    problems = list()
    problems.append(
        ProblemSingleObjective(n_refactorings_lowerbound=config.LOWER_BAND, n_refactorings_upperbound=config.UPPER_BAND)
    )
    problems.append(
        ProblemMultiObjective(n_refactorings_lowerbound=config.LOWER_BAND, n_refactorings_upperbound=config.UPPER_BAND)
    )
    problems.append(
        ProblemManyObjective(n_refactorings_lowerbound=config.LOWER_BAND, n_refactorings_upperbound=config.UPPER_BAND)
    )

    # Do optimization for various problems with various algorithms
    res = minimize(problem=problems[2],
                   algorithm=algorithms[2],
                   termination=('n_gen', config.MAX_ITERATIONS),
                   seed=1,
                   verbose=True)

    # Scatter().add(res.F).show()

    results = res.X[np.argsort(res.F[:, 0])]
    count = [np.sum([e == "a" for e in r]) for r in results[:, 0]]
    print(np.column_stack([results, count]))


if __name__ == '__main__':
    main()
