"""
This module implements the search-based refactoring with various search strategy
using pymoo framework

## References
[1] https://pymoo.org/customization/custom.html
[2] https://pymoo.org/misc/reference_directions.html

"""

__version__ = '0.1.0'
__author__ = 'Morteza Zakeri'


import os
import random
import string
from abc import ABC, abstractmethod
from typing import List


import numpy as np

from pymoo.algorithms.nsga2 import NSGA2
from pymoo.algorithms.nsga3 import NSGA3
from pymoo.factory import get_problem, get_reference_directions
from pymoo.model.crossover import Crossover
from pymoo.model.duplicate import ElementwiseDuplicateElimination
from pymoo.model.mutation import Mutation
from pymoo.model.problem import Problem
from pymoo.model.sampling import Sampling
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

from sbse.objectives import Objectives

class Gene:
    """
    The base class for the Gene in genetic algorithms
    """
    def __init__(self, **kwargs):
        self.params = kwargs


class RefactoringOperation(Gene):
    """
    The class define a data structure (dictionary) to hold a refactoring operation
    """
    def __init__(self, **kwargs):
        """
        Each refactoring operation hold as a dictionary contains the required parameters.

        Example:

            params = {
            'refactoring_name': 'make_field_static'
            'api': 'main_function'
            'source_class': 'name_of_source_class'
            'field_name': 'name_of_the_field_to_be_static'
            }

        """

        super(RefactoringOperation, self).__init__(**kwargs)

    def do_refactoring(self):
        if self.params['refactoring_name'] == 'make_field_static':
            self.params['api'](source_class=self.params['source_class'], )
        elif self.params['refactoring_name'] == 'make_field_non_static':
            pass


class Individual(List):
    """
    The class define a data structure (list) to hold an individual during the search process
    """
    def __init__(self):
        super(Individual, self).__init__()
        self.refactoring_operations = list()





class MyProblem(Problem):
    def __init__(self, n_refactorings=10):
        super(MyProblem, self).__init__(n_var=1,
                                        n_obj=2,
                                        n_constr=0,
                                        elementwise_evaluation=True)
        self.n_refactorings = n_refactorings
        self.ALPHABET = [c for c in string.ascii_lowercase]

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
        # Stage 1: Execute all refactoring operations in the sequence x
        for refactoring_operation in x.refactoring_operations:
            refactoring_operation.do_refactoring()

        # Stage 2: Computing quality attributes
        o1 = Objectives.reusability
        o2 = Objectives.understandability

        # Stage 3: Marshal objectives into vector
        out["F"] = np.array([-1*o1, -1*o2], dtype=float)


class MySampling(Sampling):
    """
    This class create the initial population, X
    """
    def _do(self, problem, n_samples, **kwargs):
        """
        Since the problem having only one variable, we return a matrix with the shape (n,1)
        Params:

            n_samples (int): the same population size, pop_size

        """
        X = np.full((n_samples, 1), None, dtype=np.object)

        for i in range(n_samples):

            X[i, 0] = "".join([np.random.choice(problem.ALPHABET) for _ in range(problem.n_characters)])

        return X



class MyCrossover(Crossover):
    def __init__(self, prob=0.9):

        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2, prob=prob)

    def _do(self, problem, X, **kwargs):

        # The input of has the following shape (n_parents, n_matings, n_var)
        # print(X.shape)
        # print(X)
        # print('='*50)
        _, n_matings, n_var = X.shape

        # The output owith the shape (n_offsprings, n_matings, n_var)
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


class MyMutation(Mutation):
    def __init__(self):
        super().__init__()

    def _do(self, problem, X, **kwargs):

        # for each individual
        for i in range(len(X)):

            r = np.random.random()

            # with a probability of 40% - change the order of characters
            if r < 0.4:
                perm = np.random.permutation(problem.n_characters)
                X[i, 0] = "".join(np.array([e for e in X[i, 0]])[perm])

            # also with a probability of 40% - change a character randomly
            elif r < 0.8:
                prob = 1 / problem.n_characters
                mut = [c if np.random.random() > prob
                       else np.random.choice(problem.ALPHABET) for c in X[i, 0]]
                X[i, 0] = "".join(mut)

        return X


class MyDuplicateElimination(ElementwiseDuplicateElimination):
    """
    This class implement is_equal method which should return True if two instances of Individual are equal.
    Otherwise it return False.

    The duplicate instances are removed from population at each generation.
    Only one instance is held to speed up the search algorithm

    """
    def is_equal(self, a, b):
        return a.X[0] == b.X[0]


def main():
    algorithm = NSGA2(pop_size=11,
                      sampling=MySampling(),
                      crossover=MyCrossover(prob=0.8),
                      mutation=MyMutation(),
                      eliminate_duplicates=MyDuplicateElimination()
                      )

    ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=12)
    algorithm = NSGA3(ref_dirs=None,  ##
                      pop_size=100,
                      sampling=MySampling(),
                      crossover=MyCrossover(prob=0.8),
                      mutation=MyMutation(),
                      eliminate_duplicates=MyDuplicateElimination()
                      )

    res = minimize(problem=MyProblem(),
                   algorithm=algorithm,
                   termination=('n_gen', 100),
                   seed=1,
                   verbose=True)

    Scatter().add(res.F).show()

    results = res.X[np.argsort(res.F[:, 0])]
    count = [np.sum([e == "a" for e in r]) for r in results[:, 0]]
    print(np.column_stack([results, count]))


