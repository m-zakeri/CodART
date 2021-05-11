from pymoo.algorithms.so_genetic_algorithm import GA
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from initialize import make_field_non_static
from initialize import make_field_static
from initialize import make_method_static_2
from initialize import make_method_non_static_2

problem = get_problem(make_method_non_static_2, make_field_non_static, make_field_static, make_method_static_2)


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
