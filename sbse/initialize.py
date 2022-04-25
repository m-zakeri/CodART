"""
This module implements finding candidates for the genetic algorithms!

Initialization: The abstract class and common utility functions.
RandomInitialization: For initialling random candidates.
"""

__version__ = '0.3.2'
__author__ = 'Morteza Zakeri'

import os
import re
import codecs
import random
import json
from collections import Counter
from pathlib import Path

import pandas

import understand as und

from codart.utility.directory_utils import reset_project, update_understand_database

from refactorings import make_field_static, make_field_non_static, make_method_static2, make_method_non_static2, \
    move_field, move_method, move_class, \
    extract_method, extract_class, extract_interface2, \
    pullup_field, pushdown_field2, pullup_method, pushdown_method, pullup_constructor, \
    increase_field_visibility, decrease_field_visibility, increase_method_visibility, decrease_method_visibility

from sbse import config

logger = config.logger

REFACTORING_MAIN_MAP = {
    'Make Field Non-Static': make_field_non_static.main,  # RO1
    'Make Field Static': make_field_static.main,  # RO2
    'Make Method Static': make_method_static2.main,  # RO3
    'Make Method Non-Static': make_method_non_static2.main,  # RO4

    'Pull Up Field': pullup_field.main,  # RO5
    'Push Down Field': pushdown_field2.main,  # # RO6, 0
    'Pull Up Method': pullup_method.main,  # # RO7, 0
    'Pull Up Constructor': pullup_constructor.main,  # RO8, 0
    'Push Down Method': pushdown_method.main,  # # RO9, 0

    'Move Field': move_field.main,  # RO10
    'Move Method': move_method.main,  # RO11
    'Move Class': move_class.main,  # RO12

    'Extract Class': extract_class.main,  # RO13
    'Extract Method': extract_method.main,  # RO14
    'Extract Interface': extract_interface2.main,  # RO15

    'Increase Field Visibility': increase_field_visibility.main,  # RO16
    'Increase Method Visibility': increase_method_visibility.main,  # RO17
    'Decrease Field Visibility': decrease_field_visibility.main,  # RO18
    'Decrease Method Visibility': decrease_method_visibility.main,  # RO19
}


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
    def __init__(self, udb_path, population_size=50, lower_band=10, upper_band=50):
        """
        The superclass of initialization contains init_refactoring modules
        :param udb_path: Path for understand database file.
        :param population_size: The length of population for GA.
        :param lower_band: The minimum length of individual for GA.
        :param upper_band: The maximum length of individual for GA.
        """
        random.seed(None)
        self.udb_path = udb_path
        self.population_size = population_size
        self.lower_band = lower_band
        self.upper_band = upper_band
        self.population = []

        self.initializers = (
            self.init_make_field_non_static,  # 0
            self.init_make_field_static,  # 1
            self.init_make_method_static,  # 2
            self.init_make_method_non_static,  # 3

            self.init_pullup_field,  # 4
            self.init_move_field,  # 5

            self.init_move_method,  # 6
            self.init_move_method,  # 6.2

            self.init_move_class,  # 7
            self.init_move_class,  # 7.2

            self.init_push_down_field,  # 8

            self.init_extract_class,  # 9
            self.init_extract_class,  # 9.2

            self.init_pullup_method,  # 10
            self.init_push_down_method,  # 11
            self.init_pullup_constructor,  # 12

            self.init_decrease_field_visibility,  # 13
            self.init_increase_field_visibility,  # 14
            self.init_decrease_method_visibility,  # 15
            self.init_increase_method_visibility,  # 16

            self.init_extract_interface,  # 17
            self.init_extract_interface,  # 17.2

            # self.init_extract_method,  # 18
        )

        self._variables = self.get_all_variables()
        self._static_variables = self.get_all_variables(static=True)
        self._methods = self.get_all_methods()
        self._static_methods = self.get_all_methods(static=True)
        self._pullup_field_candidates = self.find_pullup_field_candidates()
        self._push_down_field_candidates = self.find_push_down_field_candidates()
        self._pullup_method_candidates = self.find_pullup_method_candidates()
        self._pullup_constructor_candidates = self.find_pullup_constructor_candidates()
        self._push_down_method_candidates = self.find_push_down_method_candidates()
        self._extract_interface_candidates = self.find_extract_interface_candidate()

    def __del__(self):
        # logger.info("Understand database closed after initialization.")
        # self._und.close()
        pass

    def get_all_methods(self, static=False):
        _db = und.open(self.udb_path)
        candidates = []
        if static:
            query = _db.ents("Static Method")
            blacklist = ('abstract', 'unknown', 'constructor',)
        else:
            query = _db.ents("Method")
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

            is_public = ent.kind().check('public')
            is_private = ent.kind().check('private')
            external_references = 0
            for ref in ent.refs('Callby, Overrideby'):
                if '.'.join(long_name[:-1]) not in ref.ent().longname():
                    external_references += 1

            candidates.append(
                {
                    'source_package': source_package, 'source_class': source_class, 'method_name': method_name,
                    'is_public': is_public, 'is_private': is_private, 'external_references': external_references
                }
            )
        _db.close()
        return candidates

    def get_all_variables(self, static=False):
        _db = und.open(self.udb_path)
        candidates = []
        if static:
            query = _db.ents("Static Variable")
            blacklist = ()
        else:
            query = _db.ents("Variable")
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

            is_public = ent.kind().check('public')
            is_private = ent.kind().check('private')
            external_references = 0
            for ref in ent.refs('Setby, Useby'):
                if '.'.join(long_name[:-1]) not in ref.ent().longname():
                    external_references += 1
            candidates.append(
                {
                    'source_package': source_package, 'source_class': source_class, 'field_name': field_name,
                    'is_public': is_public, 'is_private': is_private, 'external_references': external_references
                }
            )
        _db.close()
        return candidates

    # def get_all_class_entities(self, filter_="class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static"):
    #     query = self._und.ents(filter_)
    #     class_entities = []
    #     for ent in query:
    #         class_entities.append(ent)
    #     return class_entities
    #     return query

    def find_pullup_field_candidates(self):
        _db = und.open(self.udb_path)
        candidates = []
        class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")
        for ent in class_entities:
            for ref in ent.refs("Define", "Variable"):
                candidate = {
                    "package_name": get_package_from_class(ent.longname()),
                    "children_class": ent.simplename(),
                    "field_name": ref.ent().simplename()
                }
                candidates.append(candidate)
        _db.close()
        return candidates

    def find_push_down_field_candidates(self):
        _db = und.open(self.udb_path)
        candidates = []
        class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")

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
        _db.close()
        return candidates

    def find_pullup_method_candidates(self):
        _db = und.open(self.udb_path)
        candidates = []
        class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")
        common_methods = []

        for ent in class_entities:
            children = []
            class_method_dict = {}
            father_methods = []

            for met_ref in ent.refs("Define", "Method ~Override"):
                method = met_ref.ent()
                father_methods.append(method.simplename())

            for ref in ent.refs("Extendby"):
                child = ref.ent()
                if not child.kind().check("public class"):
                    continue
                child_name = child.simplename()
                children.append(child_name)
                if child_name not in class_method_dict:
                    class_method_dict[child_name] = []

                for met_ref in child.refs("Define", "Method"):
                    method = met_ref.ent()
                    method_name = method.simplename()

                    if method.ents("Override"):
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
        _db.close()
        return candidates

    def find_pullup_constructor_candidates(self):
        _db = und.open(self.udb_path)
        candidates = []
        class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")

        for ent in class_entities:
            children = []
            params = {}

            for ref in ent.refs("Extendby"):
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
        _db.close()
        return candidates

    def find_push_down_method_candidates(self):
        _db = und.open(self.udb_path)
        candidates = []
        class_entities = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")

        for ent in class_entities:
            params = {
                "source_class": "",
                "source_package": "",
                "method_name": "",
                "target_classes": []
            }
            method_names = []

            for ref in ent.refs("Extendby ~Implicit", "Public Class"):
                params["source_class"] = ent.simplename()
                ln = ent.longname().split(".")
                params["source_package"] = ln[0] if len(ln) > 1 else ""
                params["target_classes"].append(ref.ent().simplename())

            for ref in ent.refs("Define", "Method"):
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

        _db.close()
        return candidates

    def find_extract_interface_candidate(self):
        _db = und.open(config.UDB_PATH)
        extract_interface_refactoring_candidates = []
        classes = _db.ents("Type Class Public ~Generic ~Interface ~Enum ~Unknown ~Anonymous ~TypeVariable")
        for class_entity in classes:
            class_path = class_entity.parent().longname()
            if os.path.exists(class_path):
                filter_inherited_attrs = 'Java Extend Couple ~Implicit, Java Implement Couple ~Implicit'
                filter_inherited_attrs = 'Java Implement Couple ~Implicit'
                inherited_entities = class_entity.ents(filter_inherited_attrs)
                if len(inherited_entities) == 0:
                    public_methods = len(class_entity.ents("Define", "Java Method Member ~Private ~Static"))
                    if public_methods > 0:
                        extract_interface_refactoring_candidates.append(class_path)
        _db.close()
        return extract_interface_refactoring_candidates

    def init_make_field_non_static(self):
        pass

    def init_make_field_static(self):
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

    def init_decrease_field_visibility(self):
        pass

    def init_decrease_method_visibility(self):
        pass

    def init_increase_field_visibility(self):
        pass

    def init_increase_method_visibility(self):
        pass

    def init_extract_interface(self):
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
        logger.debug(f'>>> Randomly selected refactoring: {initializer.__name__}')
        main_function, params, name = handle_index_error(initializer)()
        if main_function is None:
            print(f'Inside the select_random method {name}')
            return self.select_random()
        else:
            return main_function, params, name

    def generate_population2(self):
        population = []
        for _ in range(self.population_size):
            individual = []
            individual_size = random.randint(self.lower_band, self.upper_band)
            for j in range(individual_size):
                main, params, name = self.select_random()
                individual.append((main, params, name))
                # print(f'Append a refactoring "{name}" to "{j}th" gene of the individual {_}.')

            population.append(individual)
            # print(f'Append individual {_} to population, s')

        # self._und.close()
        # logger.debug("Database closed after initialization.")
        return population

    def generate_population(self):
        config.logger.debug(f'Generating initial population ...')
        for _ in range(0, self.population_size):
            individual = []
            individual_size = random.randint(self.lower_band, self.upper_band)
            for j in range(individual_size):
                main, params, name = self.select_random()
                logger.debug(f'Refactoring name: {name}')
                logger.debug(f'Refactoring params: {params}')
                is_correct_refactoring = main(**params)
                while is_correct_refactoring is False:
                    reset_project()
                    main, params, name = self.select_random()
                    logger.debug(f'Refactoring name: {name}')
                    logger.debug(f'Refactoring params: {params}')
                    is_correct_refactoring = main(**params)

                ####
                # update_understand_database(self.udb_path)
                # quit()
                ####

                individual.append((main, params, name))
                logger.debug(f'Append a refactoring "{name}" to "{j}th" gene of the individual {_}.')
                reset_project()
                logger.debug('-' * 100)

            self.population.append(individual)
            logger.debug(f'Append individual {_} to population, s')

        logger.debug('=' * 100)
        initial_pop_path = f'{config.PROJECT_LOG_DIR}initial_population_{config.global_execution_start_time}.json'
        self.dump_population(path=initial_pop_path)
        config.logger.debug(f'Generating initial population finished.')
        return self.population

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

        with open(path, mode='w', encoding='utf-8') as fp:
            json.dump(population_trimmed, fp, indent=4)

        config.logger.debug(f'The initial population was saved into {path}')

    def load_population(self, path=None):
        if len(self.population) > 0:
            return

        with open(path, 'r', encoding='utf-8') as fp:
            population_trimmed = json.load(fp)

        for chromosome in population_trimmed:
            chromosome_new = []
            for gene_ in chromosome:
                chromosome_new.append((REFACTORING_MAIN_MAP[gene_[0]], gene_[1], gene_[0]))
            self.population.append(chromosome_new)
        # config.logger.debug(self.population)
        config.logger.debug(f'The initial population was loaded into "population field" from {path}')


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

    def init_make_field_static(self):
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
        refactoring_main = make_method_static2.main
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
        refactoring_main = make_method_non_static2.main
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
        # params = {"project_dir": str(Path(self.udb_path).parent)}
        params = {"project_dir": config.PROJECT_PATH}
        candidates = self._pullup_field_candidates
        params.update(random.choice(candidates))
        return refactoring_main, params, 'Pull Up Field'

    def init_push_down_field(self):
        refactoring_main = pushdown_field2.main
        params = {"udb_path": str(Path(self.udb_path))}
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
        _db = und.open(self.udb_path)
        refactoring_main = move_field.main
        params = {"udb_path": str(Path(self.udb_path))}
        random_field = random.choice(self._variables)
        params.update(random_field)
        classes = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")
        random_class = (random.choice(classes)).longname().split(".")
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
        _db.close()
        return refactoring_main, params, 'Move Field'

    def init_move_field2(self):
        refactoring_main = move_field.main
        params = {"udb_path": str(Path(self.udb_path))}
        classes_fields = []
        random_field = random.choice(classes_fields)
        params.update(random_field)

        related_entities = random_field.ents(
            "Set, Setby, Contain, Containin, Use, Useby, Create, Createby, DotRef, DotRefby, Define, Definein",
            "Type ~Unknown ~Anonymous"
            # "Package"
        )
        print('Parameters', params)
        print("related_entities", related_entities)
        for e in related_entities:
            print(e.longname(), e.kind())
        if related_entities is not None and len(related_entities) > 0:
            selected_entity = random.choice(related_entities)
            package_list = selected_entity.ents('Containin', 'Java Package')
            while not package_list and selected_entity.parent() is not None:
                package_list = selected_entity.parent().ents('Containin', 'Java Package')
                selected_entity = selected_entity.parent()
            if len(package_list) < 1:
                params.update({"target_package": "(Unnamed_Package)"})
            else:
                params.update({"target_package": package_list[0].longname()})

    def init_move_method(self):
        """
        Finds methods with a class to move

        Returns: refactoring main method and its parameters.
        """
        _db = und.open(self.udb_path)
        refactoring_main = move_method.main
        params = {"udb_path": str(Path(self.udb_path))}
        random_method = random.choice(self._methods)
        params.update(random_method)
        classes = _db.ents("Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static")
        random_class = (random.choice(classes)).longname().split(".")
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
        _db.close()
        return refactoring_main, params, 'Move Method'

    def init_move_class2(self):
        refactoring_main = move_class.main
        print('BP#1')
        print(random.choice(self.get_all_class_entities()).longname())
        random_class = random.choice(self.get_all_class_entities()).longname().split(".")
        print('BP#2')
        random_class_2 = random.choice(self.get_all_class_entities()).longname().split(".")
        print('BP#3')
        params = {"udb_path": str(Path(self.udb_path))}
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
        print('BP#4')
        if len(random_class_2) == 1:
            params.update({
                "target_package": ""
            })
        else:
            params.update({
                "target_package": ".".join(random_class[:-1])
            })
        return refactoring_main, params, 'Move Class'

    def init_move_class(self):
        _db = und.open(self.udb_path)
        refactoring_main = move_class.main
        params = {"udb_path": str(Path(self.udb_path))}
        classes = _db.ents("Java Class Public ~TypeVariable ~Anonymous ~Unknown ~Unresolved ~Private ~Static")
        selected_class = random.choice(classes)
        package_list = selected_class.ents('Containin', 'Java Package')
        while not package_list and selected_class.parent() is not None:
            package_list = selected_class.parent().ents('Containin', 'Java Package')
            selected_class = selected_class.parent()
        # print(package_list)
        params.update({"class_name": selected_class.simplename()})
        if len(package_list) < 1:
            params.update({"source_package": "(Unnamed_Package)"})
        else:
            params.update({"source_package": package_list[0].longname()})

        related_entities = selected_class.ents(
            "Import, Importby, Contain, Containin, Couple, Coupleby, Create, Createby, DotRef, DotRefby, Declare, Declarein, Define, Definein",
            "Type ~Unknown ~Anonymous"
            # "Package"
        )
        # print('Parameters', params)
        # print("related_entities", related_entities)
        # for e in related_entities:
        #     print(e.longname(), e.kind())
        trials = 0
        while trials < 25:
            if related_entities is not None and len(related_entities) > 0:
                selected_entity = random.choice(related_entities)
                package_list = selected_entity.ents('Containin', 'Java Package')
                while not package_list and selected_entity.parent() is not None:
                    package_list = selected_entity.parent().ents('Containin', 'Java Package')
                    selected_entity = selected_entity.parent()
                if len(package_list) < 1:
                    params.update({"target_package": "(Unnamed_Package)"})
                else:
                    params.update({"target_package": package_list[0].longname()})
            else:
                packages = _db.ents("Package ~Unknown ~Unresolved ~Unnamed")
                if packages is not None and len(packages) > 0:
                    selected_package = random.choice(packages)
                    params.update({"target_package": selected_package.longname()})
                else:
                    params.update({"target_package": "(Unnamed_Package)"})
            # print(params['source_package'], params['target_package'])
            if params['source_package'] != params['target_package'] and params['target_package'] != '(Unnamed_Package)':
                break
            trials += 1

        _db.close()
        return refactoring_main, params, 'Move Class'

    def init_extract_class(self):
        _db = und.open(self.udb_path)
        refactoring_main = extract_class.main
        params = {"udb_path": str(Path(self.udb_path))}
        classes = _db.ents("Type Class ~Unknown ~Anonymous")
        random_class = random.choice(classes)
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
        _db.close()
        return refactoring_main, params, 'Extract Class'

    def init_extract_method(self):
        pass

    def init_extract_interface(self):
        _db = und.open(self.udb_path)
        refactoring_main = extract_interface2.main
        # params = {"udb_path": str(Path(self.udb_path))}
        random_class = random.choice(self._extract_interface_candidates)
        params = {'class_path': random_class}

        return refactoring_main, params, 'Extract Interface'

    def init_increase_field_visibility(self):
        """
        Finds a private field to increase its visibility to public.
        Returns:
            the refactoring main func, its parameters and its name
        """
        refactoring_main = increase_field_visibility.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = list(filter(lambda d: d['is_public'] is False, self._variables))
        field = random.choice(candidates)
        params.update({
            "source_package": field["source_package"],
            "source_class": field["source_class"],
            "source_field": field["field_name"],
        })
        return refactoring_main, params, 'Increase Field Visibility'

    def init_decrease_field_visibility(self):
        """
        Finds a none-external-reference-public field to decrease its visibility to private.
        Returns:
            the refactoring main func, its parameters and its name
        """
        refactoring_main = decrease_field_visibility.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = list(filter(lambda d: d['is_private'] is False and d['external_references'] == 0, self._variables))
        # print(candidates)
        field = random.choice(candidates)
        params.update({
            "source_package": field["source_package"],
            "source_class": field["source_class"],
            "source_field": field["field_name"],
        })
        return refactoring_main, params, 'Decrease Field Visibility'

    def init_increase_method_visibility(self):
        """
        Finds a private method to increase its visibility to public.
        Returns:
            the refactoring main func, its parameters and its name
        """
        refactoring_main = increase_method_visibility.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = list(filter(lambda d: d['is_public'] is False, self._methods))
        method = random.choice(candidates)
        params.update({
            "source_package": method["source_package"],
            "source_class": method["source_class"],
            "source_method": method["method_name"],
        })
        return refactoring_main, params, 'Increase Method Visibility'

    def init_decrease_method_visibility(self):
        """
        Finds a none-external-reference-public method to decrease its visibility to private.
        Returns:
            the refactoring main func, its parameters and its name
        """
        refactoring_main = decrease_method_visibility.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = list(filter(lambda d: d['is_private'] is False and d['external_references'] == 0, self._methods))
        method = random.choice(candidates)
        params.update({
            "source_package": method["source_package"],
            "source_class": method["source_class"],
            "source_method": method["method_name"],
        })
        return refactoring_main, params, 'Decrease Method Visibility'


def get_move_method_location(row):
    class_info, method_info = row.split("::")
    class_info = class_info.split(".")
    source_package = ".".join(class_info[:-1])
    source_class = class_info[-1]
    method_name = method_info.split("(")[0]
    return source_package, source_class, method_name


class SmellInitialization(RandomInitialization):
    def __init__(self, *args, **kwargs):
        super(SmellInitialization, self).__init__(*args, **kwargs)
        # Load csv files
        self.move_method_candidates = self.load_move_method_candidates()
        self.extract_class_candidates = self.load_extract_class_candidates()
        # self.extract_method_candidates = self.load_extract_method_candidates()  # We leave extract method for now.

    def load_extract_class_candidates(self):
        _db = und.open(self.udb_path)
        god_classes = pandas.read_csv(config.GOD_CLASS_PATH, sep="\t")
        candidates = []
        for index, row in god_classes.iterrows():
            moved_fields, moved_methods = [], []
            # print(row[0].strip())
            try:
                class_file = _db.lookup(re.compile(row[0].strip() + r'$'), "Class")[0].parent().longname()
                # print(class_file)
            except:
                # print('Class file not found')
                continue
            source_class = row[0].split(".")[-1]
            data = row[1][1:-1]  # skip [ and ]
            data = data.split(",")
            for field_or_method in data:
                field_or_method = field_or_method.strip()
                if "(" in field_or_method:
                    # Method
                    moved_methods.append(
                        field_or_method.split("::")[1].split("(")[0]
                    )
                elif len(field_or_method.split(" ")) == 2:
                    # Field
                    moved_fields.append(
                        field_or_method.split(" ")[-1]
                    )
            candidates.append(
                {
                    "source_class": source_class,
                    "moved_fields": moved_fields,
                    "moved_methods": moved_methods,
                    "file_path": class_file
                }
            )
        # print(candidates)
        # quit()
        _db.close()
        return candidates

    def load_move_method_candidates(self):
        feature_envies = pandas.read_csv(
            config.FEATURE_ENVY_PATH, sep=None, engine='python'
        )
        candidates = []
        for index, row in feature_envies.iterrows():
            source_package, source_class, method_name = get_move_method_location(row[1])
            target_info = row[2].split(".")
            target_package = ".".join(target_info[:-1])
            target_class = target_info[-1]
            candidates.append({
                "source_package": source_package,
                "source_class": source_class,
                "method_name": method_name,
                "target_package": target_package,
                "target_class": target_class
            })
        return candidates

    def load_extract_method_candidates(self):
        _db = und.open(self.udb_path)
        long_methods = pandas.read_csv(
            config.LONG_METHOD_PATH, sep='\t', engine='python'
        )
        candidates = []
        for index, row in long_methods.iterrows():
            lines = {}
            class_info = row[0].strip().split(".")[-1]
            class_file = _db.lookup(class_info + ".java", "File")
            if class_file:
                class_file = class_file[0].longname()
            else:
                continue
            _bytes = open(class_file, mode='rb').read()
            file_content = codecs.decode(_bytes, errors='strict')
            lines_info = row[5]
            for i in lines_info.split(")"):
                if i == '':
                    continue
                values = i.split(",")
                char_number = values[0][1:].strip()
                length = values[1].strip()
                should_copy = False if values[2].strip() == 'F' else True
                if char_number and length:
                    char_number = int(char_number)
                    length = char_number + int(length)
                    start = len(file_content[:char_number].split("\n"))
                    stop = len(file_content[:length].split("\n"))
                    for line in range(start, stop + 1):
                        lines[line] = should_copy
            candidates.append({
                "file_path": class_file,
                "lines": lines
            })

        _db.close()
        return candidates

    def init_move_method(self):
        params = random.choice(self.move_method_candidates)
        params["udb_path"] = self.udb_path
        main = move_method.main
        # print(params)
        return main, params, "Move Method"

    def init_extract_class(self):
        main = extract_class.main
        params = random.choice(self.extract_class_candidates)
        params["udb_path"] = self.udb_path
        return main, params, "Extract Class"

    def init_extract_method(self):
        main = extract_method.main
        params = random.choice(self.extract_method_candidates)
        params["udb_path"] = self.udb_path
        return main, params, "Extract Method"


#  Module tests
def test_generate_population():
    reset_project()

    initializer_ = SmellInitialization(
        config.UDB_PATH,
        population_size=config.POPULATION_SIZE,
        lower_band=config.LOWER_BAND,
        upper_band=config.UPPER_BAND
    )
    population_ = initializer_.generate_population()
    print(population_)
    # initializer_.dump_population(config.PROJECT_PATH + '_population.json')


def test_load_population():
    reset_project()

    initializer_ = SmellInitialization(
        config.UDB_PATH,
        population_size=config.POPULATION_SIZE,
        lower_band=config.LOWER_BAND,
        upper_band=config.UPPER_BAND
    )

    initializer_.load_population(config.PROJECT_PATH + '_population.json')


def test_refactoring_operations_initialization():
    initializer_ = SmellInitialization(
        config.UDB_PATH,
        population_size=config.POPULATION_SIZE,
        lower_band=config.LOWER_BAND,
        upper_band=config.UPPER_BAND
    )
    main, params, name = initializer_.init_increase_method_visibility()
    main, params, name = initializer_.init_make_field_non_static()
    print(f"Running {name}")
    print(params)
    main(**params)
    quit()

    for i in range(0, 100):
        print(initializer_.init_move_class())


if __name__ == '__main__':
    test_generate_population()
    # test_refactoring_operations_initialization()
    # test_load_population()
