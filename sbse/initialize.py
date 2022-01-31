"""
This module implements finding candidates for the genetic algorithms!

Initialization: The abstract class and common utility functions.
RandomInitialization: For initialling random candidates.
"""

__author__ = 'Seyyed Ali Ayati'
try:
    import understand as und
except ImportError as e:
    print(e)
    quit()

import codecs
import random
from collections import Counter
from pathlib import Path

import pandas
import progressbar

from refactorings import make_field_non_static, make_field_static, make_method_static_2, \
    make_method_non_static_2, pullup_field, move_field, move_method, move_class, pushdown_field, \
    extract_class, pullup_method, pushdown_method, extract_method, pullup_constructor, decrease_method_visibility, \
    increase_method_visibility, decrease_field_visibility, increase_field_visibility
from sbse import config

logger = config.logger


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
        random.seed(None)
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
            self.init_decrease_field_visibility,
            self.init_increase_field_visibility,
            self.init_decrease_method_visibility,
            self.init_increase_method_visibility
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

    # def __del__(self):
    #     logger.info("Understand database closed after initialization.")
    #     self._und.close()

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

            is_public = ent.kind().check('public')
            is_private = ent.kind().check('private')
            external_references = 0
            for ref in ent.refs('CallBy, OverrideBy'):
                if '.'.join(long_name[:-1]) not in ref.ent().longname():
                    external_references += 1

            candidates.append(
                {
                    'source_package': source_package, 'source_class': source_class, 'method_name': method_name,
                    'is_public': is_public, 'is_private': is_private, 'external_references': external_references
                }
            )
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

            is_public = ent.kind().check('public')
            is_private = ent.kind().check('private')
            external_references = 0
            for ref in ent.refs('SetBy, UseBy'):
                if '.'.join(long_name[:-1]) not in ref.ent().longname():
                    external_references += 1
            candidates.append(
                {
                    'source_package': source_package, 'source_class': source_class, 'field_name': field_name,
                    'is_public': is_public, 'is_private': is_private, 'external_references': external_references
                }
            )
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

    def init_decrease_field_visibility(self):
        pass

    def init_decrease_method_visibility(self):
        pass

    def init_increase_field_visibility(self):
        pass

    def init_increase_method_visibility(self):
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

    def init_extract_method(self):
        raise IndexError

    def init_increase_field_visibility(self):
        """
        Finds a private field to increase its visibility to public.
        Returns:
            the refactoring main func, its parameters and its name
        """
        refactoring_main = increase_field_visibility.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = list(filter(lambda d: d['is_private'] is True, self._variables))
        field = random.choice(candidates)
        params.update({
            "source_package": field["source_package"],
            "source_class": field["source_class"],
            "source_field": field["field_name"],
        })
        return refactoring_main, params, 'Increase Field Visibility'

    def init_increase_method_visibility(self):
        """
        Finds a private method to increase its visibility to public.
        Returns:
            the refactoring main func, its parameters and its name
        """
        refactoring_main = increase_method_visibility.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = list(filter(lambda d: d['is_private'] is True, self._methods))
        method = random.choice(candidates)
        params.update({
            "source_package": method["source_package"],
            "source_class": method["source_class"],
            "source_method": method["method_name"],
        })
        return refactoring_main, params, 'Increase Method Visibility'

    def init_decrease_field_visibility(self):
        """
        Finds a none-external-reference-public field to decrease its visibility to private.
        Returns:
            the refactoring main func, its parameters and its name
        """
        refactoring_main = decrease_field_visibility.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = list(filter(lambda d: d['is_public'] is True and d['external_references'] == 0, self._variables))
        field = random.choice(candidates)
        params.update({
            "source_package": field["source_package"],
            "source_class": field["source_class"],
            "source_field": field["field_name"],
        })
        return refactoring_main, params, 'Decrease Field Visibility'

    def init_decrease_method_visibility(self):
        """
        Finds a none-external-reference-public method to decrease its visibility to private.
        Returns:
            the refactoring main func, its parameters and its name
        """
        refactoring_main = decrease_method_visibility.main
        params = {"udb_path": str(Path(self.udb_path))}
        candidates = list(filter(lambda d: d['is_public'] is True and d['external_references'] == 0, self._methods))
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
        self.extract_method_candidates = self.load_extract_method_candidates()

    def load_extract_class_candidates(self):
        god_classes = pandas.read_csv(
            config.GOD_CLASS_PATH, sep="\t"
        )
        candidates = []
        for index, row in god_classes.iterrows():
            moved_fields, moved_methods = [], []
            class_file = self._und.lookup(row[0].strip(), "Class")[0].parent().longname()
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
        long_methods = pandas.read_csv(
            config.LONG_METHOD_PATH, sep='\t', engine='python'
        )
        candidates = []
        for index, row in long_methods.iterrows():
            lines = {}
            class_info = row[0].strip().split(".")[-1]
            class_file = self._und.lookup(class_info + ".java", "File")
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
        return candidates

    def init_move_method(self):
        params = random.choice(self.move_method_candidates)
        params["udb_path"] = self.udb_path
        main = move_method.main
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
        return main, params, "Extract Class"


if __name__ == '__main__':
    rand_pop = RandomInitialization(
        config.UDB_PATH,
        population_size=config.POPULATION_SIZE,
        lower_band=config.LOWER_BAND,
        upper_band=config.UPPER_BAND
    )
    main, params, name = rand_pop.init_increase_method_visibility()
    print(f"Running {name}")
    print(params)
    main(**params)
