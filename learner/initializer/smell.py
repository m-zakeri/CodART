import re
import random
from configparser import ConfigParser
import logging
from codart.utility.directory_utils import reset_project, update_understand_database2
from codart.sbse.initialize import RandomInitialization
import understand as und
import pandas as pd
import codecs


config = ConfigParser()


logger = logging.getLogger()

class SmellInitialization(RandomInitialization):
    def __init__(self, *args, **kwargs):
        super(SmellInitialization, self).__init__(*args, **kwargs)
        self.move_method_candidates = self.load_move_method_candidates()
        self.extract_class_candidates = self.load_extract_class_candidates()

    def get_move_method_location(self, row):
        class_info, method_info = row.split("::")
        class_info = class_info.split(".")
        source_package = ".".join(class_info[:-1])
        source_class = class_info[-1]
        method_name = method_info.split("(")[0]
        return source_package, source_class, method_name

    def generate_population(self):
        logger.debug(f'Generating a biased initial population ...')
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
                update_understand_database2(self.udb_path)
                individual.append((main, params, name))
                logger.debug(f'Append a refactoring "{name}" to "{j}th" gene of the individual {_}.')
                reset_project()
                logger.debug('-' * 100)

            self.population.append(individual)
            logger.debug(f'Append individual {_} to population, s')

        logger.debug('=' * 100)
        initial_pop_path = f'{config.PROJECT_LOG_DIR}initial_population_{config.global_execution_start_time}.json'
        self.dump_population(path=initial_pop_path)
        config.logger.debug(f'Generating a biased initial population was finished.')
        return self.population
    def load_extract_class_candidates(self):
        _db = und.open(self.udb_path)
        god_classes = pd.read_csv(config.GOD_CLASS_PATH, sep="\t")
        candidates = []
        for index, row in god_classes.iterrows():
            moved_fields, moved_methods = [], []
            try:
                class_file = _db.lookup(re.compile(row[0].strip() + r'$'), "Class")[0].parent().longname()
            except Exception as e:
                continue
            source_class = row[0].split(".")[-1]
            data = row[1][1:-1]
            data = data.split(",")
            for field_or_method in data:
                field_or_method = field_or_method.strip()
                if "(" in field_or_method:
                    moved_methods.append(
                        field_or_method.split("::")[1].split("(")[0]
                    )
                elif len(field_or_method.split(" ")) == 2:
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
        _db.close()
        return candidates

    def load_move_method_candidates(self):
        feature_envies = pd.read_csv(
            config.FEATURE_ENVY_PATH, sep=None, engine='python'
        )
        candidates = []
        for index, row in feature_envies.iterrows():
            source_package, source_class, method_name = self.get_move_method_location(row[1])
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
        long_methods = pd.read_csv(
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
