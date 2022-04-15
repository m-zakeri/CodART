import sys
import os
import datetime as dt
import logging
# from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

PROBLEM = int(os.environ.get("PROBLEM"))  # 0: Genetic (Single), 1: NSGA-II (Multi), 2: NSGA-III (Many)
NUMBER_OBJECTIVES = int(os.environ.get("NUMBER_OBJECTIVES"))  # Only required for NSGA-III (to set ref-points)

POPULATION_SIZE = int(os.environ.get("POPULATION_SIZE"))  # Should be set to 50 for NSGA-III
MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS"))  # Should be set to 50 for NSGA-III

LOWER_BAND = int(os.environ.get("LOWER_BAND"))
UPPER_BAND = int(os.environ.get("UPPER_BAND"))

MUTATION_PROBABILITY = float(os.environ.get("MUTATION_PROBABILITY"))
CROSSOVER_PROBABILITY = float(os.environ.get("CROSSOVER_PROBABILITY"))

WARM_START = bool(int(os.environ.get("WARM_START")))

USE_CPP_BACKEND = bool(int(os.environ.get("USE_CPP_BACKEND")))

PROJECT_ROOT_DIR = os.environ.get("PROJECT_ROOT_DIR")
CSV_ROOT_DIR = os.environ.get("CSV_ROOT_DIR")
UDB_ROOT_DIR = os.environ.get("UDB_ROOT_DIR")
INIT_POP_FILE = os.environ.get("INIT_POP_FILE")
BENCHMARK_INDEX = int(os.environ.get("BENCHMARK_INDEX", 0))

EXPERIMENTER = os.environ.get("EXPERIMENTER")
SCRIPT = os.environ.get("SCRIPT")
DESCRIPTION = os.environ.get("DESCRIPTION")

BENCHMARKS = {
    # Project Path
    'PROJ': [
        '10_water-simulator',
        '61_noen',
        '88_jopenchart',
        '104_vuze',  # Not ready
        '105_freemind',
        '107_weka',
        'commons-codec',
        'ganttproject_1_11_1_original',
        'jfreechart-master',
        'JSON20201115',
        'jvlt-1.3.2',
        'tabula-java',
    ],

    # Understand DB Path
    'UDB': [
        # '10_water-simulator.udb',
        '10_water-simulator.und',
        # '61_noen.udb',
        '61_noen.und',
        # '88_jopenchart.udb',
        '88_jopenchart.und',
        # '104_vuze.udb',  # Not ready
        '104_vuze.und',  # Not ready
        # '105_freemind.udb',
        '105_freemind.und',
        # '107_weka.udb',
        '107_weka.und',
        # 'commons-codec.udb',
        'commons-codec.und',
        # 'ganttproject_1_11_1_original.udb',
        'ganttproject_1_11_1_original.und',
        # 'jfreechart-master.udb',
        'jfreechart-master.und',
        # 'JSON20201115.udb',
        'JSON20201115.und',
        # 'jvlt-1.3.2.udb',
        'jvlt-1.3.2.und',
        # 'tabula-java.udb',
        'tabula-java.und',
    ],

    # CSV files path containing code smells identified by JDeodorant
    'LONG_METHOD': [
        '10_water-simulator/fake.csv',
        '61_noen/fake.csv',
        '88_jopenchart/fake.csv',
        '104_vuze/fake.csv',
        '105_freemind/Long-Method2_FreeMind-0.9.0.csv',
        '107_weka/Long-Method2-Weka3.8.csv',
        'commons-codec/fake.csv',
        'ganttproject_1_11_1_original/Long-Method2_ganttproject-1.11.1.csv',
        'jfreechart-master/Long-Method2_JFreeChart-1.0.19.csv',
        'JSON20201115/Long-Method2_JASON-20201115.csv',
        'jVLT-1.3.2/Long-Method2_jvlt-1.3.2.csv',
        'tabula-java/fake.csv',
    ],

    'FEATURE_ENVY': [
        '10_water-simulator/Feature-Envy_10_water-simulator-v2.csv',
        '61_noen/Feature-Envy_Noen-v0.1.csv',
        '88_jopenchart/Feature-Envy_JOpenChart-v0.94.csv',
        '104_vuze/Feature-Envy_104_vuze.csv',
        '105_freemind/Feature-Envy2_FreeMind-0.9.0.csv',
        '107_weka/Feature-Envy2-Weka3.8.csv',
        'commons-codec/Feature-Envy_Commons-codec-v1.15.csv',
        'ganttproject_1_11_1_original/Feature-Envy2_ganttproject-1.11.1.csv',
        'jfreechart-master/Feature-Envy2-JFreeChart-1.0.19.csv',
        'JSON20201115/Feature-Envy2_JASON-20201115.csv',
        'jVLT-1.3.2/Feature-Envy_jvlt-1.3.2.csv',
        'tabula-java/Feature-Envy-Tabula-v1.0.6.csv',
    ],

    'GOD_CLASS': [
        '10_water-simulator/God-Class_10_water-simulator-v2.csv',
        '61_noen/God-Class_Noen-v0.1.csv',
        '88_jopenchart/God-Class_JOpenChart-v0.94.csv',
        '104_vuze/God-Class_104_vuze.csv',
        '105_freemind/God-Class_FreeMind-0.9.0.csv',
        '107_weka/God-Class-Weka3.8.csv',
        'commons-codec/God-Class_Commons-codec-v1.15.csv',
        'ganttproject_1_11_1_original/God-Class_ganttproject-1.11.1.csv',
        'jfreechart-master/God-Class-JFreeChart-1.0.19.csv',
        'JSON20201115/God-Class_JASON-20201115.csv',
        'jVLT-1.3.2/God-Class_jvlt-1.3.2.csv',
        'tabula-java/God-Class-Tabula-v1.0.6.csv',
    ],
}

PROJECT_PATH = os.path.join(PROJECT_ROOT_DIR, BENCHMARKS['PROJ'][BENCHMARK_INDEX]).replace('/', '\\')
UDB_PATH = os.path.join(UDB_ROOT_DIR, BENCHMARKS['UDB'][BENCHMARK_INDEX]).replace('/', '\\')

FEATURE_ENVY_PATH = os.path.join(CSV_ROOT_DIR, BENCHMARKS['FEATURE_ENVY'][BENCHMARK_INDEX])
GOD_CLASS_PATH = os.path.join(CSV_ROOT_DIR, BENCHMARKS['GOD_CLASS'][BENCHMARK_INDEX])
LONG_METHOD_PATH = os.path.join(CSV_ROOT_DIR, BENCHMARKS['LONG_METHOD'][BENCHMARK_INDEX])

PROJECT_NAME = os.path.basename(PROJECT_PATH)

# Initial value of QMOOD design metrics, testability and modularity used in objective-normalization process
INITIAL_METRICS = {
    "10_water-simulator": {  # 0
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "61_noen": {  # 1
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "88_jopenchart": {  # 2
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "104_vuze": {  # 3 Not ready
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
      "105_freemind": {  # 4
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
      },
    "107_weka": {  # 5
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "commons-codec": {  # 6
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "ganttproject_1_11_1_original": {  # 7
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "jfreechart-master": {  # 8
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "JSON20201115": {  # 9
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "jvlt-1.3.2": {  # 10
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
    "tabula-java": {  # 11
        'ANA': 1.,
        'CAMC': 1.,
        'CIS': 1.,
        'DAM': 1.,
        'DCC': 1.,
        'DSC': 1.,
        'MFA': 1.,
        'MOA': 1.,
        'NOH': 1.,
        'NOM': 1.,
        'NOP': 1.,
        'MODULE': 1.,
        'TEST': 1.,  # Obtained by testability_prediction2
        'TEST3': 1.  # Obtained by testability_prediction3
    },
}

CURRENT_METRICS = INITIAL_METRICS.get(PROJECT_NAME)
date_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
dirname = os.path.dirname(__file__)
LOG_FILE = os.path.join(dirname, f'./logs/{PROJECT_NAME}-{date_time}.log')
FORMATTER = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')


# logging.basicConfig(
#     format='%(asctime)s %(levelname)-8s %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
#     level=logging.DEBUG,  # DEBUG
#     handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_FILE)],
# )


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger_ = logging.getLogger(logger_name)
    logger_.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger_.addHandler(get_console_handler())
    logger_.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger_.propagate = False
    return logger_


logger = get_logger(__name__)


# print(logger.handlers)


def log_experiment_info():
    logger.info("============ Configuration/Setup ============")
    logger.info(f"Project root directory: {PROJECT_PATH}")
    logger.info(f"Understand database file path: {UDB_PATH}")
    logger.info(f"Problem: {PROBLEM}")
    logger.info(f"Number of objectives: {NUMBER_OBJECTIVES}")
    logger.info(f"Population size: {POPULATION_SIZE}")
    logger.info(f"Individual lower band: {LOWER_BAND}")
    logger.info(f"Individual upper band: {UPPER_BAND}")
    logger.info(f"Max iterations: {MAX_ITERATIONS}")
    logger.info(f"Crossover probability: {CROSSOVER_PROBABILITY}")
    logger.info(f"Mutation probability: {MUTATION_PROBABILITY}")
    logger.info(f"Warm start mode: {WARM_START}")
    logger.info(f"CPP back-end mode: {USE_CPP_BACKEND}")
    logger.info(f"Experimenter: {EXPERIMENTER}")
    logger.info(f"Main script running the experiments: {SCRIPT}")
    logger.info(f"Experiment description: {DESCRIPTION}")
    logger.info("============ End of Configuration/Setup ============")

