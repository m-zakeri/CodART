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
        'ANA': 0.56,
        'CAMC': 0.5844,
        'CIS': 3.21333,
        'DAM': 0.96952,
        'DCC': 4.61333,
        'DSC': 72.0,
        'MFA': 0.04934,
        'MOA': 1.69333,
        'NOH': 1.0,
        'NOM': 1.25333,
        'NOP': 3.86667,
        'MODULE': 0.22967,
        'TEST': 22.71451,  # Obtained by testability_prediction2
        'TEST3': 0.3702604117198275  # Obtained by testability_prediction3
    },
    "61_noen": {  # 1
        'ANA': 0.498777506,
        'CAMC': 0.688801956,
        'CIS': 4.471882641,
        'DAM': 0.757864181,
        'DCC': 1.696821516,
        'DSC': 428.0,
        'MFA': 0.12371425,
        'MOA': 1.701711491,
        'NOH': 15.0,
        'NOM': 4.951100244,
        'NOP': 4.523227384,
        'MODULE': 0.3743241335376458,
        'TEST2': 0.5581233625170191,  # Obtained by testability_prediction2
        'TEST': 0.5295360105264939  # Obtained by testability_prediction3
    },
    "88_jopenchart": {  # 2
        'ANA': 0.692307692,
        'CAMC': 0.577692308,
        'CIS': 8.025641026,
        'DAM': 0.529107312,
        'DCC': 2.358974359,
        'DSC': 46.0,
        'MFA': 0.270584931,
        'MOA': 0.923076923,
        'NOH': 4.0,
        'NOM': 8.615384615,
        'NOP': 8.076923077,
        'MODULE': 0.20512820512820512,
        'TEST2': 0.5516735761315649,  # Obtained by testability_prediction2
        'TEST': 0.4817706859946628  # Obtained by testability_prediction3
    },
    "104_vuze": {  # 3 Not ready
        'ANA': 0.647412982,
        'CAMC': 0.803941675,
        'CIS': 4.467732832,
        'DAM': 0.305707086,
        'DCC': 1.729444967,
        'DSC': 6221.0,
        'MFA': 0.206624442,
        'MOA': 1.029162747,
        'NOH': 130.0,
        'NOM': 5.634995296,
        'NOP': 4.751834431,
        "MODULE": 0,
        "TEST2": 0,  # Obtained by testability_prediction2
        'TEST': 0  # Obtained by testability_prediction3
    },
      "105_freemind": {  # 4
        'ANA': 0.94783,
        'CAMC': 0.69098,
        'CIS': 5.91957,
        'DAM': 0.94725,
        'DCC': 3.36957,
        'DSC': 455.0,
        'MFA': 0.19461,
        'MOA': 1.8913,
        'NOH': 17.0,
        'NOM': 2.59565,
        'NOP': 5.63478,
        'MODULE': 0.25276,
        'TEST2': 107.59553,  # Obtained by testability_prediction2
        'TEST': 156.83146530439788,  # Obtained by testability_prediction3
      },
    "107_weka": {  # 5
        'ANA': 0.94025,
        'CAMC': 0.4844,
        'CIS': 11.48631,
        'DAM': 0.92378,
        'DCC': 3.35519,
        'DSC': 1145.0,
        'MFA': 0.25965,
        'MOA': 3.92033,
        'NOH': 70.0,
        'NOM': 5.34357,
        'NOP': 10.98091,
        'MODULE': 0.26754,
        'TEST2': 1,  # Obtained by testability_prediction2
        'TEST': 412.9319579700542,  # Obtained by testability_prediction3
    },
    "commons-codec": {  # 6
        'ANA': 0.32,
        'CAMC': 0.7213,
        'CIS': 6.92,
        'DAM': 0.597956349,
        'DCC': 1.85,
        'DSC': 108.0,
        'MFA': 0.125396441,
        'MOA': 0.54,
        'NOH': 7.0,
        'NOM': 9.15,
        'NOP': 4.18,
        'MODULE': 0.4198853053622194,
        'TEST2': 0,  # Obtained by testability_prediction2
        'TEST': 0.4653682475404442  # Obtained by testability_prediction3
    },
    "ganttproject_1_11_1_original": {  # 7
        'ANA': 0.574285714,
        'CAMC': 0.730228571,
        'CIS': 4.157142857,
        'DAM': 0.5197205,
        'DCC': 2.74,
        'DSC': 407.0,
        'MFA': 0.156224894,
        'MOA': 1.577142857,
        'NOH': 28.0,
        'NOM': 5.491428571,
        'NOP': 4.645714286,
        "MODULE": 0.33473127930074126,
        "TEST2": 0,  # Obtained by testability_prediction2
        "TEST": 0.4426126215132276,  # Obtained by testability_prediction3

    },
    "jfreechart-master": {  # 8
        'ANA': 1.036723164,
        'CAMC': 0.709943503,
        'CIS': 9.950564972,
        'DAM': 0.544492767,
        'DCC': 3.433615819,
        'DSC': 633.0,
        'MFA': 0.270958496,
        'MOA': 2.892655367,
        'NOH': 27.0,
        'NOM': 11.211864407,
        'NOP': 9.991525424,
        "MODULE": 0.2544013611666677,
        "TEST2": 0,  # Obtained by testability_prediction2
        "TEST": 0.470488065430968,  # Obtained by testability_prediction3

    },
    "JSON20201115": {  # 9
        'ANA': 0.5,
        'CAMC': 0.848666667,
        'CIS': 9.5,
        'DAM': 0.305555556,
        'DCC': 2.866666667,
        'DSC': 26.0,
        'MFA': 0.099846547,
        'MOA': 1.2,
        'NOH': 2.0,
        'NOM': 10.9,
        'NOP': 7.266666667,
        "MODULE": 0.0,  # JASON project have no packages
        "TEST2": 0,  # Obtained by testability_prediction2
        "TEST": 0.4713493233566381,  # Obtained by testability_prediction3
    },
    "jvlt-1.3.2": {  # 10
        'ANA': 0.763513514,
        'CAMC': 0.710135135,
        'CIS': 4.966216216,
        'DAM': 0.659427284,
        'DCC': 2.148648649,
        'DSC': 160.0,
        'MFA': 0.297960026,
        'MOA': 1.75,
        'NOH': 11.0,
        'NOM': 5.418918919,
        'NOP': 4.797297297,
        "MODULE": 0.3051931655584547,
        "TEST2": 0,  # Obtained by testability_prediction2
        "TEST": 0.4787325664033668,  # Obtained by testability_prediction3
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


def log_project_info():
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
