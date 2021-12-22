"""
This module implements finding candidates for the genetic algorithms!

Initialization: The abstract class and common utility functions.
RandomInitialization: For initialling random candidates.
"""

__author__ = 'Seyyed Ali Ayati'

import random
from collections import Counter
from pathlib import Path

import progressbar

from candidate_reader import CandidateReader
from config import *
from refactorings import make_field_non_static, make_field_static, make_method_static_2, \
    make_method_non_static_2, pullup_field, move_field, move_method, move_class, pushdown_field, \
    extract_class, pullup_method, pushdown_method, extract_method, pullup_constructor
from utilization.setup_understand import *


def get_package_from_class(class_longname: str):
    parts = class_longname.split(".")
    if len(parts) > 1:
        parts = parts[:-1]
        return ".".join(parts)
    else:
        return ""


def handle_index_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return None, None, None
    return wrapper


class Initialization(object):
    def __init__(self, udb_path, population_size=50, lower_band=50, upper_band=75):
        """
        The superclass of initialization contains init_refactoring modules
        :param udb_path: Path for understand database file.
        :param population_size: The length of population for GA.
        :param individual_size: The length of individual for GA.
        """
        self.udb_path = udb_path
        self.population_size = population_size
        self.lower_band = lower_band
        self.upper_band = upper_band
        self.initializers = (
            self.init_make_field_non_static,
            self.inti_make_field_static,
            self.init_make_method_static,
            self.init_make_method_non_static,
            self.init_pullup_field,
            self.init_move_field,
            self.init_move_method,
            self.init_move_class,
            self.init_push_down_field,
            self.init_extract_class,
            self.init_pullup_method,
            self.init_push_down_method,
            # self.init_extract_method,
            self.init_pullup_constructor,
        )

        self._und = und.open(self.udb_path)
        self._variables = self.get_all_variables()
        self._static_variables = self.get_all_variables(static=True)
        self._methods = self.get_all_methods()
        self._static_methods = self.get_all_methods(static=True)
        self._pullup_field_candidates = self.find_pullup_field_candidates()
        self._push_down_field_candidates = self.find_push_down_field_candidates()
        self._pullup_method_candidates = self.find_pullup_method_candidates()
        self._pullup_constructor_candidates = self.find_pullup_constructor_candidates()
        self._push_down_method_candidates = self.find_push_down_method_candidates()

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
            long_name = parent.longname().split('.')
            method_name = ent.simplename()
            if len(long_name) == 1:
                source_class = long_name[-1]
                source_package = None
            elif len(long_name) > 1:
                source_class = long_name[-1]
                source_package = ".".join(long_name[:-1])
            else:
                continue
            candidates.append(
                {'source_package': source_package, 'source_class': source_class, 'method_name': method_name})
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
            source_package = None
            long_name = ent.longname().split(".")
            if len(long_name) >= 3:
                source_package = '.'.join(long_name[:-2])
                source_class, field_name = long_name[-2:]
            elif len(long_name) == 2:
                source_class, field_name = long_name
            else:
                continue
            candidates.append(
                {'source_package': source_package, 'source_class': source_class, 'field_name': field_name})
        return candidates

    def get_all_class_entities(self, filter="class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static"):
        query = self._und.ents(filter)
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
                    "package_name": get_package_from_class(ent.longname()),
                    "children_class": ent.simplename(),
                    "field_name": ref.ent().simplename()
                }
                candidates.append(candidate)
        return candidates

    def find_push_down_field_candidates(self):
        candidates = []
        class_entities = self.get_all_class_entities()

        for ent in class_entities:
            params = {
                "source_class": "",
                "source_package": "",
                "field_name": "",
                "target_classes": []
            }
            field_names = []

            for ref in ent.refs("ExtendBy ~Implicit"):
                params["source_class"] = ent.simplename()
                params["source_package"] = get_package_from_class(ent.longname())
                if len(params["target_classes"]) >= 1:
                    rnd = random.randint(0, 1)
                    if rnd == 0:
                        params["target_classes"].append(ref.ent().simplename())
                else:
                    params["target_classes"].append(ref.ent().simplename())

            for ref in ent.refs("define", "variable"):
                field_names.append(ref.ent().simplename())

            if field_names:
                params["field_name"] = random.choice(field_names)
            else:
                continue
            if params["source_class"] != "":
                candidates.append(params)
        return candidates

    def find_pullup_method_candidates(self):
        candidates = []
        class_entities = self.get_all_class_entities()
        common_methods = []

        for ent in class_entities:
            children = []
            class_method_dict = {}
            father_methods = []

            for met_ref in ent.refs("define", "method ~override"):
                method = met_ref.ent()
                father_methods.append(method.simplename())

            for ref in ent.refs("extendby"):
                child = ref.ent()
                if not child.kind().check("public class"):
                    continue
                child_name = child.simplename()
                children.append(child_name)
                if child_name not in class_method_dict:
                    class_method_dict[child_name] = []

                for met_ref in child.refs("define", "method"):
                    method = met_ref.ent()
                    method_name = method.simplename()

                    if method.ents("override"):
                        continue

                    if method_name not in father_methods:
                        common_methods.append(method_name)
                        class_method_dict[child_name].append(method_name)

            counts = Counter(common_methods)
            common_methods = [value for value, count in counts.items() if count > 1]
            if len(common_methods) > 0:
                random_method = random.choice(common_methods)
                children = [k for k, v in class_method_dict.items() if random_method in v]
                if len(children) > 1:
                    candidates.append({
                        "method_name": random.choice(common_methods),
                        "children_classes": children
                    })
        return candidates

    def find_pullup_constructor_candidates(self):
        candidates = []
        class_entities = self.get_all_class_entities()

        for ent in class_entities:
            children = []
            params = {}

            for ref in ent.refs("extendby"):
                child = ref.ent()
                if not child.kind().check("public class"):
                    continue
                child_name = child.simplename()
                children.append(child_name)

            ln = ent.longname().split(".")
            params["source_package"] = ".".join(ln[:-1]) if len(ln) > 1 else ""
            params["target_class"] = ent.simplename()
            if len(children) >= 2:
                params["class_names"] = random.sample(children, random.randint(2, len(children)))
                candidates.append(params)
        return candidates

    def find_push_down_method_candidates(self):
        candidates = []
        class_entities = self.get_all_class_entities()

        for ent in class_entities:
            params = {
                "source_class": "",
                "source_package": "",
                "method_name": "",
                "target_classes": []
            }
            method_names = []

            for ref in ent.refs("ExtendBy ~Implicit", "public class"):
                params["source_class"] = ent.simplename()
                ln = ent.longname().split(".")
                params["source_package"] = ln[0] if len(ln) > 1 else ""
                params["target_classes"].append(ref.ent().simplename())

            for ref in ent.refs("define", "method"):
                method_names.append(ref.ent().simplename())

            if method_names:
                params["method_name"] = random.choice(method_names)
            else:
                continue

            if params["target_classes"]:
                params["target_classes"] = [random.choice(params["target_classes"])]
            else:
                continue

            if params["source_class"] != "":
                candidates.append(params)

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

    def init_push_down_field(self):
        pass

    def init_pullup_method(self):
        pass

    def init_pullup_constructor(self):
        pass

    def init_push_down_method(self):
        pass

    def init_move_field(self):
        pass

    def init_move_method(self):
        pass

    def init_move_class(self):
        pass

    def init_extract_class(self):
        pass

    def init_extract_method(self):
        pass

    def select_random(self):
        """
        Randomly selects a refactoring. If there are no candidates it tries again!

        Returns:
            main_function: function
            params: dict
            name: str
        """
        initializer = random.choice(self.initializers)
        main_function, params, name = handle_index_error(initializer)()
        if main_function is None:
            return self.select_random()
        else:
            return main_function, params, name

    def generate_population(self):
        population = []
        for _ in progressbar.progressbar(range(self.population_size)):
            individual = []
            individual_size = random.randint(self.lower_band, self.upper_band)
            for j in range(individual_size):
                individual.append(
                    self.select_random()
                )
            population.append(individual)
        self._und.close()
        logger.debug("Database closed after initialization.")
        return population

    @property
    def und(self):
        return self._und


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
        params.pop("source_package")
        return refactoring_main, params, 'Make Field Non-Static'

    def inti_make_field_static(self):
        """
        Finds all non-static fields and randomly chooses one of them
        :return: refactoring main method and its parameters.
        """
        refactoring_main = make_field_static.main
        params = {"udb_path": self.udb_path}
        candidates = self._variables
        params.update(random.choice(candidates))
        params.pop("source_package")
        return refactoring_main, params, 'Make Field Static'

    def init_make_method_static(self):
        """
        Finds all non-static methods and randomly chooses one of them
        :return: refactoring main method and its parameters.
        """
        refactoring_main = make_method_static_2.main
        params = {"udb_path": self.udb_path}
        candidates = self._methods
        params.update(random.choice(candidates))
        params.pop("source_package")
        return refactoring_main, params, 'Make Method Static'

    def init_make_method_non_static(self):
        """
        Finds all static methods and randomly chooses one of them
        :return: refactoring main method and its parameters.
        """
        refactoring_main = make_method_non_static_2.main
        params = {"udb_path": self.udb_path}
        candidates = self._static_methods
        params.update(random.choice(candidates))
        params.pop("source_package")
        return refactoring_main, params, 'Make Method Non-Static'

    def init_pullup_field(self):
        """
        Find all classes with their attributes and package names, then chooses randomly one of them!
        :return:  refactoring main method and its parameters.
        """
        refactoring_main = pullup_field.main
        params = {"project_dir": str(Path(self.udb_path).parent)}
        candidates = self._pullup_field_candidates
        params.update(random.choice(candidates))
        return refactoring_main, params, 'Pull Up Field'

    def init_push_down_field(self):
        refactoring_main = pushdown_field.main
        params = {"project_dir": str(Path(self.udb_path).parent)}
        candidates = self._push_down_field_candidates
        params.update(random.choice(candidates))
        return refactoring_main, params, 'Push Down Field'

    def init_pullup_method(self):
        refactoring_main = pullup_method.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = self._pullup_method_candidates
        params.update(random.choice(candidates))
        return refactoring_main, params, 'Pull Up Method'

    def init_pullup_constructor(self):
        refactoring_main = pullup_constructor.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = self._pullup_constructor_candidates
        params.update(random.choice(candidates))
        return refactoring_main, params, 'Pull Up Constructor'

    def init_push_down_method(self):
        refactoring_main = pushdown_method.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = self._push_down_method_candidates
        params.update(random.choice(candidates))
        return refactoring_main, params, 'Push Down Method'

    def init_move_field(self):
        """
        Finds fields with a class to move

        Returns: refactoring main method and its parameters.
        """
        refactoring_main = move_field.main
        params = {"udb_path": str(Path(self.udb_path))}
        random_field = random.choice(self._variables)
        params.update(random_field)
        random_class = random.choice(self.get_all_class_entities()).longname().split(".")
        target_package = None
        """
        target_class: str, target_package: str,
        """
        if len(random_class) == 1:
            target_class = random_class[0]
        elif len(random_class) > 1:
            target_package = '.'.join(random_class[:-1])
            target_class = random_class[-1]
        else:
            return self.init_move_field()
        params.update({
            "target_class": target_class,
            "target_package": target_package
        })
        return refactoring_main, params, 'Move Field'

    def init_move_method(self):
        """
        Finds methods with a class to move

        Returns: refactoring main method and its parameters.
        """
        refactoring_main = move_method.main
        params = {"udb_path": str(Path(self.udb_path))}
        random_method = random.choice(self._methods)
        params.update(random_method)
        random_class = random.choice(self.get_all_class_entities()).longname().split(".")
        target_package = None
        """
        target_class: str, target_package: str,
        """
        if len(random_class) == 1:
            target_class = random_class[0]
        elif len(random_class) > 1:
            target_package = '.'.join(random_class[:-1])
            target_class = random_class[-1]
        else:
            return self.init_move_field()
        params.update({
            "target_class": target_class,
            "target_package": target_package
        })
        return refactoring_main, params, 'Move Method'

    def init_move_class(self):
        refactoring_main = move_class.main
        params = {"udb_path": str(Path(self.udb_path))}
        random_class = random.choice(self.get_all_class_entities()).longname().split(".")
        random_class_2 = random.choice(self.get_all_class_entities()).longname().split(".")
        if len(random_class) == 1:
            params.update({
                "class_name": random_class[0],
                "source_package": ""
            })
        else:
            params.update({
                "class_name": random_class[-1],
                "source_package": ".".join(random_class[:-1])
            })

        if len(random_class_2) == 1:
            params.update({
                "target_package": ""
            })
        else:
            params.update({
                "target_package": ".".join(random_class[:-1])
            })
        return refactoring_main, params, 'Move Class'

    def init_extract_class(self):
        refactoring_main = extract_class.main
        params = {"udb_path": str(Path(self.udb_path))}
        random_class = random.choice(self.get_all_class_entities())
        params.update(
            {
                "source_class": random_class.simplename(),
                "file_path": random_class.parent().longname()
            }
        )
        class_fields = []
        class_methods = []

        for ref in random_class.refs("define", "variable"):
            class_fields.append(ref.ent())

        for ref in random_class.refs("define", "method"):
            class_methods.append(ref.ent())

        params.update(
            {
                "moved_fields": [ent.simplename() for ent in
                                 random.sample(class_fields, random.randint(0, len(class_fields)))],
                "moved_methods": [ent.simplename() for ent in
                                  random.sample(class_methods, random.randint(0, len(class_methods)))],
            }
        )
        return refactoring_main, params, 'Extract Class'

    def init_extract_method(self, file_path="C:\\Users\\RGY\\Desktop\\Long-Method.csv"):
        """
        Uses jDodorant csv output and candidate_reader.py
        """
        refactoring_main = extract_method.main
        candidates = []
        cr = CandidateReader(file_path)
        for i in range(len(cr)):
            params = {}
            conf = cr.get_conf(i)
            longname = conf.get("target_file")
            lookup = self._und.lookup(longname + ".java", "File")
            if lookup and os.path.basename(lookup[0].longname()) == longname.split(".")[-1] + ".java":
                params["file_path"] = lookup[0].longname()
                params["lines"] = conf.get("lines", [])
                candidates.append(params)
            else:
                continue
        params = random.choice(candidates)
        return refactoring_main, params, 'Extract Method'


if __name__ == '__main__':
    rand_pop = RandomInitialization(
        "D:\Final Project\IdeaProjects\JSON20201115\JSON20201115.und",
        population_size=POPULATION_SIZE,
        lower_band=LOWER_BAND,
        upper_band=UPPER_BAND
    )
    population = rand_pop.generate_population()
    print(population)
