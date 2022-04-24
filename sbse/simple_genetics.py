"""
Search-based refactoring with genetic algorithm

"""

__version__ = '0.1.'
__author__ = 'Morteza Zakeri'

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from initialize import make_field_non_static
from initialize import make_field_static
from initialize import make_method_static2
from initialize import make_method_non_static2

problem = get_problem(make_method_non_static2, make_field_non_static, make_field_static, make_method_static2)


def genetic_algorithm():
    algorithm = GA(
        population_size=100,
        individual_size=2,
        eliminate_duplicates=True)

    res = minimize(problem,
                   algorithm,
                   seed=1,
                   verbose=False)

    print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))


if __name__ == '__main__':
    genetic_algorithm()
