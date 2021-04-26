import random
import progressbar
from config import *
from utilization.setup_understand import *
from refactorings import make_field_non_static, make_field_static, make_method_static_2, make_method_non_static, \
    make_method_non_static_2
from utilization.directory_utils import update_understand_database


# TODO: check pymoo (framework) if possible
# TODO: Simple GA

class Initialization(object):
    def __init__(self, udb_path, population_size=50, individual_size=4):
        """
        The superclass of initialization contains init_refactoring modules
        :param udb_path: Path for understand database file.
        :param population_size: The length of population for GA.
        :param individual_size: The length of individual for GA.
        """
        self.udb_path = udb_path
        self.population_size = population_size
        self.individual_size = individual_size

        self._und = und.open(self.udb_path)
        self._variables = self.get_all_variables()
        self._static_variables = self.get_all_variables(static=True)
        self._methods = self.get_all_methods()
        self._static_methods = self.get_all_methods(static=True)

    def get_all_methods(self, static=False):
        candidates = []
        if static:
            query = self._und.ents("static method")
            blacklist = ('abstract', 'unknown', 'constructor',)
        else:
            query = self._und.ents("method")
            blacklist = ('constructor', 'static', 'abstract', 'unknown',)
        for ent in query:
            kind_name = ent.kindname().lower()
            if any(word in kind_name for word in blacklist):
                continue
            source_class, method_name = ent.name().split('.')
            candidates.append({'source_class': source_class, 'method_name': method_name})
        return candidates

    def get_all_variables(self, static=False):
        candidates = []
        if static:
            query = self._und.ents("static variable")
            blacklist = ()
        else:
            query = self._und.ents("variable")
            blacklist = ('static',)
        for ent in query:
            kind_name = ent.kindname().lower()
            if any(word in kind_name for word in blacklist):
                continue
            source_class, field_name = ent.name().split('.')
            candidates.append({'source_class': source_class, 'field_name': field_name})
        return candidates

    def init_make_field_non_static(self):
        pass

    def inti_make_field_static(self):
        pass

    def init_make_method_static(self):
        pass

    def init_make_method_non_static(self):
        pass

    def generate_population(self):
        initializers = (
            self.init_make_field_non_static,
            self.inti_make_field_static,
            self.init_make_method_static,
            self.init_make_method_non_static,
        )
        population = []
        for _ in progressbar.progressbar(range(self.population_size)):
            individual = []
            for j in range(self.individual_size):
                individual.append(
                    random.choice(initializers)()
                )
            population.append(individual)
        print(f"len of population is: {len(population)}")
        return population


class RandomInitialization(Initialization):
    def init_make_field_non_static(self):
        """
        Finds all static fields and randomly chooses one of them
        :return: refactoring main method and its parameters.
        """
        refactoring_main = make_field_non_static.main
        params = {"udb_path": self.udb_path}
        candidates = self._static_variables
        params.update(random.choice(candidates))
        return refactoring_main, params

    def inti_make_field_static(self):
        """
        Finds all non-static fields and randomly chooses one of them
        :return: refactoring main method and its parameters.
        """
        refactoring_main = make_field_static.main
        params = {"udb_path": self.udb_path}
        candidates = self._variables
        params.update(random.choice(candidates))
        return refactoring_main, params

    def init_make_method_static(self):
        """
        Finds all non-static methods and randomly chooses one of them
        :return: refactoring main method and its parameters.
        """
        refactoring_main = make_method_static_2.main
        params = {"udb_path": self.udb_path}
        candidates = self._methods
        params.update(random.choice(candidates))
        return refactoring_main, params

    def init_make_method_non_static(self):
        """
        Finds all static methods and randomly chooses one of them
        :return: refactoring main method and its parameters.
        """
        refactoring_main = make_method_non_static_2.main
        params = {"udb_path": self.udb_path}
        candidates = self._static_methods
        params.update(random.choice(candidates))
        return refactoring_main, params


if __name__ == '__main__':
    rand_pop = RandomInitialization(
        "/home/ali/Desktop/code/TestProject/TestProject.udb",
        population_size=POPULATION_SIZE,
        individual_size=INDIVIDUAL_SIZE
    ).generate_population()
