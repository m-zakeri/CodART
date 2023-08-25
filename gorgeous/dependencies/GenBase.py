from pymoo.core.crossover import Crossover
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from pymoo.termination.default import DefaultMultiObjectiveTermination
from pymoo.core.mutation import Mutation
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.util.normalization import denormalize
from pymoo.core.sampling import Sampling
import numpy as np
from datetime import datetime
import random
from pymoo.algorithms.soo.nonconvex.ga import GA
from copy import deepcopy
from gorgeous.dependencies.Utils import *
from dotenv import dotenv_values
from gorgeous.dependencies.ClsUDBMetrics import (
    ClsUDB_Metrics,
    DesignQualityAttributes,
    Similarity,
)
from gorgeous.dependencies.Grammer import GrammarClass

final_list = []
actor_list = []

udb_path = (
    "Resources/und_db/" + dotenv_values().get("RESOURCES_PATH").split(" ")[0] + ".und"
)
project_path = (
    "Resources/projects/" + dotenv_values().get("RESOURCES_PATH").split(" ")[0]
)


def calc_qmood_objectives(arr_):
    qmood_quality_attributes = DesignQualityAttributes(udb_path=udb_path)
    arr_[0] = qmood_quality_attributes.quality


class ProblemSingleObjective(Problem):
    """
    The CodART single-objective optimization work with only one objective, testability:
    """

    def __init__(
        self,
        n_objectives=1,
        mode: int = 2,  # 'multi'
    ):
        """
        Args:
            n_objectives (int): Number of objectives
            mode (str): 'single' or 'multi'
        """

        super(ProblemSingleObjective, self).__init__(n_var=1, n_obj=1, n_constr=0)

        self.mode = mode
        self.n_obj_virtual = n_objectives

    def _evaluate(self, x, out, *args, **kwargs):  #
        """
        This method iterate over a population, execute the refactoring operations in each individual sequentially,
        and compute quality attributes for the refactored version of the program, as objectives of the search
        Args:
            x (Population): x is a matrix where each row is an individual, and each column a variable.\
                We have one variable of type list (Individual) ==> x.shape = (len(Population), 1)
        """
        cls_udb_metric_obj = ClsUDB_Metrics()
        objective_values = []
        print("TEST X : ", x.shape)
        # Stage 0: Git restore
        print("Executing git restore.")
        git_restore(project_path)
        print("Updating understand database after git restore.")
        cls_udb_metric_obj.update_understand_database(udb_path=udb_path)
        # Stage 1: Execute all refactoring operations in the sequence x
        print(f"Reached Individual with Size {len(x)}")
        actor_list = []
        gc_obj = None
        # for refactoring_operation in x:
        for c, item in enumerate(x):
            for z, j in enumerate(item[0]):
                print("z : ", z)
                print("j : ", j)
                print(j[0])
                gc_obj = GrammarClass(
                    project_path=project_path,
                    udb_path=udb_path,
                    chromosome=j[1:],
                )

                actor_list.append(
                    {
                        "id": j[0],
                        "obj": deepcopy(gc_obj._procedure()),
                        "score": 0.0,
                    }
                )
                # Update Understand DB
                if actor_list is not None:
                    for i, item in enumerate(actor_list):
                        try:
                            for j in item["obj"]:
                                print(
                                    f"Updating understand database after {i} - \n REFACTORING : {j.refactoring} \n NAME : {j.name} \n TYPE : {j.type} \n SOURCE : {j.source} \n TARGET : {j.target} \n"
                                )
                        except:
                            continue
                else:
                    print(f"not found any refactoring in {x} chromosome")

            cls_udb_metric_obj.update_understand_database(udb_path=udb_path)
            if self.mode == 2:
                # calculate similarity and mq together
                sim = 0.0
                s = Similarity(
                    mode=int(dotenv_values().get("MODE_SIM")),
                    actors=actor_list,
                    udb_path=udb_path,
                )
                sim = s.sim()
                qmood_quality_attributes = DesignQualityAttributes(udb_path=udb_path)
                o1 = 0.5 * (qmood_quality_attributes.quality + sim)
            else:
                # just calculate mq
                qmood_quality_attributes = DesignQualityAttributes(udb_path=udb_path)
                o1 = qmood_quality_attributes.quality
            del qmood_quality_attributes
            print("o1 : ", o1)
            print("o1 : ", type(o1))
            score = o1

            actor_list[len(actor_list) - 1]["score"] = deepcopy(score)
            print("last actor : ", actor_list[len(actor_list) - 1])
            # Stage 3: Marshal objectives into vector
            objective_values.append([-1 * score])
            print(f"Objective values for individual : {[-1 * score]}")

            # Stage 4: Marshal all objectives into out dictionary
            final_list.append(actor_list)
            out["F"] = np.array(objective_values, dtype=int)


def is_equal_2_refactorings_list(a, b):
    """
    This method implement is_equal method which should return True if two instances of Individual class are equal.
    Otherwise, it returns False.
    The duplicate instances are removed from population at each generation.
    Only one instance is held to speed up the search algorithm
    < procedure >: := < rtype > < procedure > | < rtype >
    < rtype >: := < extractClass > | < moveMethod > | < pullUpMethod > | < pushDownMethod >
    """

    a = a.X
    b = b.X

    if len(a.tolist()) != len(b.tolist()):
        return False
    for i in range(1, len(a)):
        if len(actor_list) > 0:
            if (actor_list[a[0]] is not None) and (actor_list[b[0]] is not None):
                if a[i] == b[i] and actor_list[a[0]] is actor_list[b[0]]:
                    return True
    return False


class IntegerMutation(Mutation):
    """
    Select an individual to mutate with mutation probability.
    Only flip one refactoring operation in the selected individual.
    """

    def __init__(self, prob=0.01, initializer: list = None):
        """
        Args:
            prob (float): mutation probability
        """

        super().__init__()
        self.mutation_probability = prob
        self._initializer = initializer

    def _do(self, problem, X, **kwargs):
        for i, individual in enumerate(X[:]):
            for j, ro in enumerate(individual):
                r = np.random.random()
                # with a probability of `mutation_probability` replace the refactoring operation with new one
                if r < self.mutation_probability:
                    # j is a random index in individual
                    id = deepcopy(X[i][0][len(X[i][0]) - 1][0])
                    random_chromosome = random.choice(self._initializer)
                    random_chromosome.insert(0, int(id) + 1)
                    X[i][0][j] = deepcopy(random_chromosome)
        return X


class SinglePointCrossover(Crossover):
    def __init__(self, prob=0.9):
        # Define the crossover: number of parents, number of offsprings, and cross-over probability
        super().__init__(n_parents=2, n_offsprings=2, prob=prob)

    def _do(self, problem, X, **kwargs):
        # print("in single point =============================")
        # The input of has the following shape (n_parents, n_matings, n_var)

        # X = np.array(X)
        print("X.shape : ", X.shape)
        n_offsprings, n_matings, n_var = X.shape
        # print("n_matings : ", n_matings)
        # print("n_var : ", n_var)
        # The output will be with the shape (n_offsprings, n_matings, n_var, n_chromosome)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=object)

        for k in range(n_matings):

            # get the first and the second parent (a and b are instance of individuals)
            a, b = X[0, k, 0], X[1, k, 0]
            # print("### a", a)
            # print("### b", b)
            # print("len a", len(a))
            # print("len b", len(b))

            len_min = min(len(a), len(b))

            if int(len_min * 0.30) <= 1:
                cross_point_1 = 1
            else:
                cross_point_1 = random.randint(1, int(len_min * 0.30))
            cross_point_2 = random.randint(int(len_min * 0.70), len_min - 1)
            if random.random() < 0.5:
                cross_point_final = cross_point_1
            else:
                cross_point_final = cross_point_2
            # print(f"cross_point_final: {cross_point_final}")
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
            # print("$$$ offspring_a", offspring_a)
            # print("$$$ offspring_b", offspring_b)
            # print("len offspring_a", len(offspring_a))
            # print("len offspring_b", len(offspring_b))

            # Join offsprings to offspring population Y
            print("len(offspring_a) : ", len(offspring_a))
            print("len(offspring_b) : ", len(offspring_b))
            Y[0, k, 0], Y[1, k, 0] = offspring_a, offspring_b

            # quit()

        print(Y.shape)
        return Y


class FloatRandomSampling(Sampling):
    def random_by_bounds(self, n_var, xl, xu, n_samples=20):
        val = np.random.random((n_samples, n_var))
        return denormalize(val, xl, xu)

    def random_between(self, n_var, xl, xu, n_samples=20):
        val = np.random.uniform(low=2.0, high=100.0, size=(100, n_samples))
        return denormalize(val, xl, xu)

    def random(self, problem, n_samples=20):
        return self.random_between(
            problem.n_var, problem.xl, problem.xu, n_samples=n_samples
        )

    def _do(self, problem, n_samples, **kwargs):
        return self.random(problem, n_samples=n_samples)


class IntegerRandomSampling(FloatRandomSampling):
    def _do(self, problem, n_samples, **kwargs):
        X = super()._do(problem, n_samples, **kwargs)
        mylist = np.round(X).astype(int)
        for i, item in enumerate(mylist):
            mylist[i, 0] = i
        n_samples = 4
        x = np.empty((n_samples, 1), dtype=object)
        for i in range(n_samples):
            x[i, 0] = deepcopy(random.choices(population=mylist, k=2))
        print(x)
        return x


class GenBase:
    """
    MODE = 1
    RANDOM POPULATION
    ==================================
    MODE = 2
    CUSTOM
    """

    RANDOM_MODE = 1

    def __init__(
        self,
        mod: int = 1,
        pop_size: int = 21,
        ge_fitness_evaluations: int = 10000,
        crossover_operator: str = "SP",
        crossover_probability: float = 0.9,
        mutation_operator: str = "INT",
        mutation: float = 0.01,
        pruning: float = 0.01,
        duplication_probabilities: float = 0.01,
        selection_operator: str = "BT",
        maximum_gene_size: int = 20,
        **kwargs,
    ):
        self.mode = mod
        if self.mode == 1:
            self.pop_size = pop_size
            self.population = (
                np.around(
                    denormalize(
                        np.random.uniform(low=2.0, high=100.0, size=(100, 20)),
                        None,
                        None,
                    )
                )
                .astype(int)
                .tolist()
            )
            # for i in range(self.pop_size)

            # for i in range(len(self.population)):
            #     self.population[i].insert(0, i)
            self.ge_fitness_evaluations = ge_fitness_evaluations
            self.crossover_operator = crossover_operator
            self.mutation_operator = mutation_operator
            self.mutation = mutation
            self.pruning = pruning
            self.duplication_probabilities = duplication_probabilities
            self.selection_operator = selection_operator
            self.maximum_gene_size = maximum_gene_size
            self.crossover_probability = crossover_probability

    def run(self):
        if self.mode == 1:
            ga = GA(
                pop_size=self.pop_size,
                sampling=IntegerRandomSampling(),
                crossover=SinglePointCrossover(prob=self.crossover_probability),
                mutation=IntegerMutation(
                    prob=self.mutation, initializer=self.population
                ),
                eliminate_duplicates=ElementwiseDuplicateElimination(
                    cmp_func=is_equal_2_refactorings_list
                ),
                n_gen=self.maximum_gene_size,
            )

            my_termination = DefaultMultiObjectiveTermination(
                xtol=0.0005, cvtol=1e-8, ftol=0.0015, n_skip=5
            )

            # Do optimization for various problems with various algorithms
            # MODE 2 mq + sim | MODE 1 mq => read mode from .env file
            res = minimize(
                problem=ProblemSingleObjective(mode=int(dotenv_values().get("MODE"))),
                algorithm=ga,
                termination=my_termination,
                seed=1,
                verbose=False,
                copy_algorithm=True,
                copy_termination=True,
                save_history=False,
            )
            for ac in final_list.reverse():
                for i, item in enumerate(ac):
                    try:
                        print("+" * 50)
                        print("ID : ", item["id"])
                        print("SCORE : ", item["score"])
                        for j in item["obj"]:
                            print(
                                f"REFACTORING : {j.refactoring} \n NAME : {j.name} \n TYPE : {j.type} \n SOURCE : {j.source} \n TARGET : {j.target} \n",
                                "*" * 50,
                            )

                    except Exception as e:
                        print("WARNING : ", e)

            print(
                f"***** Algorithm was finished in {res.algorithm.n_gen + 20} generations *****"
            )
            print(" ")
            print("============ time information ============")
            print(
                f"Start time: {datetime.fromtimestamp(res.start_time).strftime('%Y-%m-%d %H:%M:%S')}"
            )
            print(
                f"End time: {datetime.fromtimestamp(res.end_time).strftime('%Y-%m-%d %H:%M:%S')}"
            )
            print(f"Execution time in seconds: {res.exec_time}")
            print(f"Execution time in minutes: {res.exec_time / 60}")
            print(f"Execution time in hours: {res.exec_time / (60 * 60)}")
