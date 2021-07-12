import random
from pathlib import Path
import progressbar
from config import *
from utilization.setup_understand import *
from refactorings import make_field_non_static, make_field_static, make_method_static_2, make_method_non_static, \
    make_method_non_static_2, pullup_field
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
        self._pullup_field_candidates = self.find_pullup_field_candidates()

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
            parent = ent.parent()
            if parent is None:
                continue
            if not parent.kind().check("class") or parent.kind().check("anonymous"):
                continue
            source_class = parent.simplename()
            method_name = ent.simplename()
            # print("Method", source_class, parent.kindname(), method_name)
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
            parent = ent.parent()
            if parent is None:
                continue
            if not parent.kind().check("class") or parent.kind().check("anonymous"):
                continue
            source_class = parent.simplename()
            field_name = ent.simplename()
            # print("Variable", source_class, parent.kindname(), field_name)
            candidates.append({'source_class': source_class, 'field_name': field_name})
        return candidates

    def get_all_class_entities(self):
        query = self._und.ents("class ~Unknown ~Anonymous ~TypeVariable")
        class_entities = []
        for ent in query:
            class_entities.append(ent)
        return class_entities

    def find_pullup_field_candidates(self):
        candidates = []
        class_entities = self.get_all_class_entities()
        for ent in class_entities:
            for ref in ent.refs("define", "variable"):
                candidate = {
                    "package_name": ent.parent().simplename(),
                    "children_class": ent.simplename(),
                    "field_name": ref.ent().simplename()
                }
                candidates.append(candidate)
        return candidates

    def init_make_field_non_static(self):
        pass

    def inti_make_field_static(self):
        pass

    def init_make_method_static(self):
        pass

    def init_make_method_non_static(self):
        pass

    def init_pullup_field(self):
        pass

    def generate_population(self):
        initializers = (
            self.init_make_field_non_static,
            self.inti_make_field_static,
            # self.init_make_method_static,
            # self.init_make_method_non_static,
            # self.init_pullup_field,
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

    def init_pullup_field(self):
        """
        Find all classes with their attributes and package names, then chooses randomly one of them!
        :return:  refactoring main method and its parameters.
        """
        refactoring_main = pullup_field.main
        params = {"project_dir": str(Path(self.udb_path).parent)}
        candidates = self._pullup_field_candidates
        params.update(random.choice(candidates))
        return refactoring_main, params

if __name__ == '__main__':
    rand_pop = RandomInitialization(
        "/data/Dev/CodART/benchmark_projects/JSON/JSON.udb",
        population_size=POPULATION_SIZE,
        individual_size=INDIVIDUAL_SIZE
    )
    rand_pop.find_pullup_field_candidates()
    population = rand_pop.generate_population()

