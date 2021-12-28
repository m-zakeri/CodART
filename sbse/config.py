import os
import logging

POPULATION_SIZE = os.environ.get("POPULATION_SIZE", 10)  # Should be set to 190, 193, 200 for NSGA-III
MAX_ITERATIONS = 10  # Should be set to 700 or 1000 or 1400 for NSGA-III
LOWER_BAND = 5
UPPER_BAND = 6

root_dir = 'D:/IdeaProjects/'
benchmarks = {'PROJ': ['JSON20201115',
                      'jvlt-1.3.2',
                      'ganttproject_1_11_1_original'],

             'UDB': ['JSON20201115/JSON.und',
                     'jvlt-1.3.2/src.und',
                     'ganttproject_1_11_1_original/ganttproject_1_11_1_original.und']}

PROJECT_PATH = root_dir + benchmarks['PROJ'][0]
UDB_PATH = root_dir + benchmarks['UDB'][0]


PROJECT_NAME = os.path.basename(PROJECT_PATH)

INITIAL_QMOOD_METRICS = {
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
    },
}

CURRENT_QMOOD_METRICS = INITIAL_QMOOD_METRICS.get(PROJECT_NAME)

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
