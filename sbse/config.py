import logging
import os

from dotenv import load_dotenv

load_dotenv()

POPULATION_SIZE = int(os.environ.get("POPULATION_SIZE"))  # Should be set to 190, 193, 200 for NSGA-III
MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS"))  # Should be set to 700 or 1000 or 1400 for NSGA-III
LOWER_BAND = int(os.environ.get("LOWER_BAND"))
UPPER_BAND = int(os.environ.get("UPPER_BAND"))

PROJECT_ROOT_DIR = os.environ.get("PROJECT_ROOT_DIR")
CSV_ROOT_DIR = os.environ.get("CSV_ROOT_DIR")
BENCHMARK_INDEX = 5
BENCHMARKS = {
    # Project Path
    'PROJ': ['JSON20201115',
             '105_freemind',
             '107_weka',
             'ganttproject_1_11_1_original',
             'jfreechart-master',
             'jvlt-1.3.2',
             '104_vuze',
             ],
    # Understand DB Path
    'UDB': ['JSON20201115\\JSON20201115.und',
            '105_freemind\\105_freemind.und',
            '107_weka\\107_weka.und',
            'ganttproject_1_11_1_original\\ganttproject_1_11_1_original.und',
            'jfreechart-master\\jfreechart-master.und',
            'jvlt-1.3.2\\jvlt-1.3.2.und',
            '104_vuze\\104_vuze.und',
            ],
    # CSV File Path
    'LONG_METHOD': [
        'JSON20201115\\Long-Method2_JASON-20201115.csv',
        'FreeMind-0.9.0\\Long-Method2_FreeMind-0.9.0.csv',
        'Weka-3.8\\Long-Method2-Weka3.8.csv',
        'GanttProject-1.11.1\\Long-Method2_ganttproject-1.11.1.csv',
        'JFreeChart-1.0.19\\Long-Method2_JFreeChart-1.0.19.csv',
        'jVLT-1.3.2\\Long-Method2_jvlt-1.3.2.csv',
    ],
    'GOD_CLASS': [
        'JSON20201115\\God-Class_JASON-20201115.csv',
        'FreeMind-0.9.0\\God-Class_FreeMind-0.9.0.csv',
        'Weka-3.8\\God-Class-Weka3.8.csv',
        'GanttProject-1.11.1\\God-Class_ganttproject-1.11.1.csv',
        'JFreeChart-1.0.19\\God-Class-JFreeChart-1.0.19.csv',
        'jVLT-1.3.2\\God-Class_jvlt-1.3.2.csv',
    ],
    'FEATURE_ENVY': [
        'JSON20201115\\Feature-Envy2_JASON-20201115.csv',
        'FreeMind-0.9.0\\Feature-Envy2_FreeMind-0.9.0.csv',
        'Weka-3.8\\Feature-Envy2-Weka3.8.csv',
        'GanttProject-1.11.1\\Feature-Envy2_ganttproject-1.11.1.csv',
        'JFreeChart-1.0.19\\Feature-Envy2-JFreeChart-1.0.19.csv',
        'jVLT-1.3.2\\Feature-Envy_jvlt-1.3.2.csv',
    ],
}

PROJECT_PATH = os.path.join(PROJECT_ROOT_DIR, BENCHMARKS['PROJ'][BENCHMARK_INDEX])
UDB_PATH = os.path.join(PROJECT_ROOT_DIR, BENCHMARKS['UDB'][BENCHMARK_INDEX])
FEATURE_ENVY_PATH = os.path.join(CSV_ROOT_DIR, BENCHMARKS['FEATURE_ENVY'][BENCHMARK_INDEX])
GOD_CLASS_PATH = os.path.join(CSV_ROOT_DIR, BENCHMARKS['GOD_CLASS'][BENCHMARK_INDEX])
LONG_METHOD_PATH = os.path.join(CSV_ROOT_DIR, BENCHMARKS['LONG_METHOD'][BENCHMARK_INDEX])

PROJECT_NAME = os.path.basename(PROJECT_PATH)

INITIAL_METRICS = {
    "JSON20201115": {
        "DSC": 26,
        "NOH": 2,
        "ANA": 0.5,
        "MOA": 1.2,
        "DAM": 0.3055555555555556,
        "CAMC": 0.8486666666666667,
        "CIS": 9.5,
        "NOM": 10.9,
        "DCC": 2.8666666666666667,
        "MFA": 0.099846547314578,
        "NOP": 6.566666666666666,
        "TEST": 0.4748841147083056,
        "MODULE": 1,
    },
    "104_vuze": {
        "DSC": 8040,
        "NOH": 157,
        "ANA": 0.6034383954154727,
        "MOA": 0.9767908309455587,
        "DAM": 0.2741500639139978,
        "CAMC": 0.8217435530085977,
        "CIS": 4.06676217765043,
        "NOM": 5.139828080229226,
        "DCC": 1.5714899713467048,
        "MFA": 0.2091017384211249,
        "NOP": 4.3729226361031515,
        "TEST": 0.4748841147083056,
        "MODULE": 0.20544581966389708,
    },
    "105_freemind": {
        "DSC": 1074,
        "NOH": 23,
        "ANA": 1.0050813008130082,
        "MOA": 1.6747967479674797,
        "DAM": 0.4325461206997841,
        "CAMC": 0.7525609756097558,
        "CIS": 4.728658536585366,
        "NOM": 6.087398373983739,
        "DCC": 2.9430894308943087,
        "MFA": 0.1718928794350772,
        "NOP": 5.1138211382113825,
        "TEST": 0.3752525309440714,
        "MODULE": 0.28767512755806884,
    },
    "107_weka": {
        "DSC": 2338,
        "NOH": 81,
        "ANA": 0.9378711740520785,
        "MOA": 2.3129282777523983,
        "DAM": 0.4333987889293128,
        "CAMC": 0.7152581087254457,
        "CIS": 6.7907720420283235,
        "NOM": 8.088624942896299,
        "DCC": 2.385107354956601,
        "MFA": 0.17212621102262438,
        "NOP": 7.14846962083143,
        "TEST": 0.4865105816109613,
        "MODULE": 0.32787710443044066,
    },
    "ganttproject_1_11_1_original": {
        "DSC": 555,
        "NOH": 33,
        "ANA": 0.6971544715447154,
        "MOA": 1.508130081300813,
        "DAM": 0.4831759334621796,
        "CAMC": 0.736524390243902,
        "CIS": 3.8536585365853657,
        "NOM": 4.953252032520325,
        "DCC": 2.680894308943089,
        "MFA": 0.14711823738179727,
        "NOP": 4.1971544715447155,
        "TEST": 0.5029896831173097,
        "MODULE": 0.34926607015973216,
    },
    "jfreechart-master": {
        "DSC": 674,
        "NOH": 36,
        "ANA": 1.0040160642570282,
        "MOA": 4.546184738955823,
        "DAM": 0.5328309085326908,
        "CAMC": 0.7099598393574299,
        "CIS": 10.238286479250334,
        "NOM": 11.46318607764391,
        "DCC": 3.317269076305221,
        "MFA": 0.2586029996567078,
        "NOP": 10.210174029451139,
        "TEST": 0.4820787549441007,
        "MODULE": 0.23642449145114441,
    },
    "jvlt-1.3.2": {
        "DSC": 420,
        "NOH": 17,
        "ANA": 0.8073170731707318,
        "MOA": 2.4,
        "DAM": 0.6101752259758623,
        "CAMC": 0.7478780487804875,
        "CIS": 4.021951219512195,
        "NOM": 4.8951219512195125,
        "DCC": 2.5585365853658537,
        "MFA": 0.22910838294407537,
        "NOP": 4.131707317073171,
        "TEST": 0.42116082618406314,
        "MODULE": 0.20757585289828134,
    },
}

CURRENT_METRICS = INITIAL_METRICS.get(PROJECT_NAME)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(f'../sbse/logs/{PROJECT_NAME}.log'),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger()


def log_project_info():
    logger.info("============ Configuration ============")
    logger.info(f"Understand DB Path: f{UDB_PATH}")
    logger.info(f"Project Directory: f{PROJECT_PATH}")
    logger.info(f"Population Size: {POPULATION_SIZE}")
    logger.info(f"Individual Lower Band: {LOWER_BAND}")
    logger.info(f"Individual Upper Band: {UPPER_BAND}")
    logger.info(f"Max Iterations: {MAX_ITERATIONS}")
    logger.info("============ End of Configuration ============")
