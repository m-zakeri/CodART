import re
import random
from configparser import ConfigParser
import logging
from codart.utility.directory_utils import reset_project, update_understand_database2
from codart.learner.sbr_initializer.abstraction import Initializer
import understand as und
import pandas as pd
import codecs
import os
from codart.learner.sbr_initializer.utils.utility import Utils, logger, config
from collections import Counter
import time
from codart.refactorings import (
    move_method,
    extract_method,
    extract_class,
    pullup_method,
    pushdown_method2,
)


class SmellInitialization(Initializer):

    def __init__(self, *args, **kwargs):
        super(SmellInitialization, self).__init__(
            udb_path=os.path.join(
                config["Config"]["db_address"], config["Config"]["db_name"]
            ),
            upper_band=int(config["Config"]["UPPER_BAND"]),
            lower_band=int(config["Config"]["LOWER_BAND"]),
            population_size=int(config["Config"]["POPULATION_SIZE"]),
            *args,
            **kwargs,
        )
        self.utils = Utils(
            logger=logger, initializers=self.initializers, population=self.population
        )

    def generate_population(self):
        logger.debug(f"Generating a biased initial population ...")
        for _ in range(0, self.population_size):
            individual = []
            individual_size = random.randint(self.lower_band, self.upper_band)
            for j in range(individual_size):
                main, params, name = self.utils.select_random()
                logger.debug(f"Refactoring name: {name}")
                logger.debug(f"Refactoring params: {params}")
                is_correct_refactoring = main(**params)
                while is_correct_refactoring is False:
                    reset_project()
                    main, params, name = self.utils.select_random()
                    logger.debug(f"Refactoring name: {name}")
                    logger.debug(f"Refactoring params: {params}")
                    is_correct_refactoring = main(**params)
                update_understand_database2(self.udb_path)
                individual.append((main, params, name))
                logger.debug(
                    f'Append a refactoring "{name}" to "{j}th" gene of the individual {_}.'
                )
                reset_project()
                logger.debug("-" * 100)
            self.population.append(individual)
            logger.debug(f"Append individual {_} to population, s")
        logger.debug("=" * 100)
        initial_pop_path = f"{config['Config']['PROJECT_LOG_DIR']}initial_population_{time.time()}.json"
        self.utils.dump_population(path=initial_pop_path)
        logger.debug(f"Generating a biased initial population was finished.")
        return self.population

    def generate_an_action(self):
        logger.debug("Generating one random refactor ...")
        main, params, name = self.utils.select_random()
        logger.debug(f"Selected refactoring name: {name}")
        logger.debug(f"Selected refactoring params: {params}")
        is_correct_refactoring = main(**params)
        while not is_correct_refactoring:
            reset_project()
            main, params, name = self.utils.select_random()
            logger.debug(f"Retry with refactoring name: {name}")
            logger.debug(f"Retry with refactoring params: {params}")
            is_correct_refactoring = main(**params)

        # Optionally update the understand database if needed
        update_understand_database2(self.udb_path)
        logger.debug(f"Successfully generated refactor: {name}")
        reset_project()
        logger.debug("-" * 100)
        return main, params, name

    def load_extract_class_candidates(self):
        _db = und.open(self.udb_path)
        god_classes = pd.read_csv(config["RELATIONS"]["GOD_CLASS_PATH"], sep="\t")
        candidates = []
        for index, row in god_classes.iterrows():
            moved_fields, moved_methods = [], []
            try:
                class_file = (
                    _db.lookup(re.compile(row[0].strip() + r"$"), "Class")[0]
                    .parent()
                    .longname()
                )
            except Exception as e:
                continue
            source_class = row[0].split(".")[-1]
            data = row[1][1:-1]
            data = data.split(",")
            for field_or_method in data:
                field_or_method = field_or_method.strip()
                if "(" in field_or_method:
                    moved_methods.append(field_or_method.split("::")[1].split("(")[0])
                elif len(field_or_method.split(" ")) == 2:
                    moved_fields.append(field_or_method.split(" ")[-1])
            candidates.append(
                {
                    "source_class": source_class,
                    "moved_fields": moved_fields,
                    "moved_methods": moved_methods,
                    "file_path": class_file,
                }
            )
        _db.close()
        return candidates

    def load_move_method_candidates(self):
        feature_envies = pd.read_csv(
            config["RELATIONS"]["FEATURE_ENVY_PATH"], sep=None, engine="python"
        )
        candidates = []
        for index, row in feature_envies.iterrows():
            source_package, source_class, method_name = (
                self.utils.get_move_method_location(row[1])
            )
            target_info = row[2].split(".")
            target_package = ".".join(target_info[:-1])
            target_class = target_info[-1]
            candidates.append(
                {
                    "source_package": source_package,
                    "source_class": source_class,
                    "method_name": method_name,
                    "target_package": target_package,
                    "target_class": target_class,
                }
            )
        return candidates

    def load_extract_method_candidates(self):
        _db = und.open(self.udb_path)
        long_methods = pd.read_csv(
            config["RELATIONS"]["LONG_METHOD_PATH"], sep="\t", engine="python"
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
            _bytes = open(class_file, mode="rb").read()
            file_content = codecs.decode(_bytes, errors="strict")
            lines_info = row[5]
            for i in lines_info.split(")"):
                if i == "":
                    continue
                values = i.split(",")
                char_number = values[0][1:].strip()
                length = values[1].strip()
                should_copy = False if values[2].strip() == "F" else True
                if char_number and length:
                    char_number = int(char_number)
                    length = char_number + int(length)
                    start = len(file_content[:char_number].split("\n"))
                    stop = len(file_content[:length].split("\n"))
                    for line in range(start, stop + 1):
                        lines[line] = should_copy
            candidates.append({"file_path": class_file, "lines": lines})

        _db.close()
        return candidates

    def load_push_down_method_candidates(self):
        _db = und.open(self.udb_path)
        candidates = []
        class_entities = _db.ents(
            "Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static"
        )

        for ent in class_entities:
            params = {
                "source_class": "",
                "source_package": "",
                "method_name": "",
                "target_classes": [],
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

    def load_pull_up_method_candidates(self):
        _db = und.open(self.udb_path)
        candidates = []
        class_entities = _db.ents(
            "Class ~Unknown ~Anonymous ~TypeVariable ~Private ~Static"
        )
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
                children = [
                    k for k, v in class_method_dict.items() if random_method in v
                ]
                if len(children) > 1:
                    candidates.append(
                        {
                            "method_name": random.choice(common_methods),
                            "children_classes": children,
                        }
                    )
        _db.close()
        return candidates

    def init_move_method(self):
        params = random.choice(self.load_move_method_candidates())
        params["udb_path"] = self.udb_path
        main = move_method.main
        return main, params, "Move Method"

    def init_extract_class(self):
        main = extract_class.main
        params = random.choice(self.load_extract_class_candidates())
        params["udb_path"] = self.udb_path
        return main, params, "Extract Class"

    def init_extract_method(self):
        main = extract_method.main
        params = random.choice(self.load_extract_class_candidates())
        params["udb_path"] = self.udb_path
        return main, params, "Extract Method"

    def init_pull_up_method(self):
        main = pullup_method.main
        params = random.choice(self.load_pull_up_method_candidates())
        params["udb_path"] = self.udb_path
        return main, params, "PullUp Method"

    def init_push_down_method(self):
        main = pushdown_method2.main
        params = random.choice(self.load_push_down_method_candidates())
        params["udb_path"] = self.udb_path
        return main, params, "PushDown Method"
