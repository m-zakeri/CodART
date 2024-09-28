import random
import json
from abc import abstractmethod, ABCMeta


def handle_index_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return None, None, None

    return wrapper


class DynamicAbstractMetaInitializeRefactoringMethods(ABCMeta):

    def create_not_implemented_method(self, method_name):
        def not_implemented_method(self):
            raise NotImplementedError(f"Method {method_name} not implemented.")

        return not_implemented_method

    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)

        if "refactoring_types" in namespace:
            for refactoring in namespace["refactoring_types"]:
                method_name = f"init_{refactoring.strip()}"
                setattr(
                    new_class,
                    method_name,
                    abstractmethod(cls.create_not_implemented_method(method_name)),
                )
                method_name = f"load_{refactoring.strip()}_candidates"
                setattr(
                    new_class,
                    method_name,
                    abstractmethod(cls.create_not_implemented_method(method_name)),
                )

        return new_class


class Utils(object):
    def __init__(self, logger, population, initializers):
        self.logger = logger
        self.population = population
        self.initializers = initializers

    @handle_index_error
    def select_random(self):
        initializer = random.choice(self.initializers)
        self.logger.debug(f">>> Randomly selected refactoring: {initializer.__name__}")
        main_function, params, name = initializer
        if main_function is None:
            print(f"Inside the select_random method {name}")
            return self.select_random()
        else:
            return main_function, params, name

    def dump_population(self, path=None):
        if self.population is None or len(self.population) == 0:
            return
        population_trimmed = []
        for chromosome in self.population:
            chromosome_new = []
            for gene_ in chromosome:
                chromosome_new.append((gene_[2], gene_[1]))
            population_trimmed.append(chromosome_new)
        # config.logger.debug(population_trimmed)

        with open(path, mode="w", encoding="utf-8") as fp:
            json.dump(population_trimmed, fp, indent=4)

        self.logger.debug(f"The initial population was saved into {path}")

    def get_move_method_location(self, row):
        class_info, method_info = row.split("::")
        class_info = class_info.split(".")
        source_package = ".".join(class_info[:-1])
        source_class = class_info[-1]
        method_name = method_info.split("(")[0]
        return source_package, source_class, method_name
