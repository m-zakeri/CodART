import os
import logging

POPULATION_SIZE = os.environ.get("POPULATION_SIZE", 10)
INDIVIDUAL_SIZE = os.environ.get("INDIVIDUAL_SIZE", 3)
MAX_ITERATIONS = 5
LOWER_BAND = 2
UPPER_BAND = 4
UDB_PATH = "D:\Final Project\IdeaProjects\JSON20201115\JSON20201115.und"
PROJECT_PATH = "D:\Final Project\IdeaProjects\JSON20201115"
PROJECT_NAME = os.path.basename(PROJECT_PATH)

INITIAL_QMOOD_METRICS = {
    "JSON20201115": {
        "DSC": 26,
        "NOH": 16,
        "ANA": 1.5,
        "MOA": 40,
        "DAM": 0.26666666666666666,
        "CAMC": 0.8486666666666667,
        "CIS": 9.5,
        "NOM": 10.9,
        "DCC": 7.366666666666666,
        "MFA": 0.3665132139812447,
        "NOP": 6.566666666666666,
    },
    "104_vuze": {
        "DSC": 8040,
        "NOH": 3431,
        "ANA": 1.6034383954154727,
        "MOA": 6937,
        "DAM": 0.2549243334033765,
        "CAMC": 0.8217435530085977,
        "CIS": 4.06676217765043,
        "NOM": 5.139828080229226,
        "DCC": 5.484670487106017,
        "MFA": 0.2185573258136751,
        "NOP": 4.3729226361031515,
    },
    "105_freemind": {
        "DSC": 1074,
        "NOH": 285,
        "ANA": 2.005081300813008,
        "MOA": 1648,
        "DAM": 0.40350070743229816,
        "CAMC": 0.7525609756097558,
        "CIS": 4.728658536585366,
        "NOM": 6.087398373983739,
        "DCC": 8.002032520325203,
        "MFA": 0.17595792008548367,
        "NOP": 5.1138211382113825,
    },
    "107_weka": {
        "DSC": 2338,
        "NOH": 448,
        "ANA": 1.9378711740520786,
        "MOA": 5064,
        "DAM": 0.9378711740520786,
        "CAMC": 0.7152581087254457,
        "CIS": 6.7907720420283235,
        "NOM": 8.088624942896299,
        "DCC": 8.204202832343535,
        "MFA": 0.17989231426611463,
        "NOP": 7.14846962083143,
    },
    "ganttproject_1_11_1_original": {
        "DSC": 555,
        "NOH": 200,
        "ANA": 1.6971544715447155,
        "MOA": 742,
        "DAM": 0.47448694793941704,
        "CAMC": 0.736524390243902,
        "CIS": 3.8536585365853657,
        "NOM": 4.953252032520325,
        "DCC": 6.524390243902439,
        "MFA": 0.15728083900781353,
        "NOP": 4.1971544715447155,
    },
    "jfreechart-master": {
        "DSC": 674,
        "NOH": 232,
        "ANA": 2.004016064257028,
        "MOA": 3475,
        "DAM": 0.49966532797858104,
        "CAMC": 0.7099598393574299,
        "CIS": 10.238286479250334,
        "NOM": 11.46318607764391,
        "DCC": 9.890227576974565,
        "MFA": 0.5022442312497467,
        "NOP": 10.210174029451139,
    },
    "jvlt-1.3.2": {
        "DSC": 420,
        "NOH": 152,
        "ANA": 1.8073170731707318,
        "MOA": 987,
        "DAM": 0.5634146341463414,
        "CAMC": 0.7478780487804875,
        "CIS": 4.021951219512195,
        "NOM": 4.8951219512195125,
        "DCC": 8.629268292682926,
        "MFA": 0.25105960245627046,
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
    logger.info(f"Individual Size: {INDIVIDUAL_SIZE}")
    logger.info(f"Individual Lower Band: {LOWER_BAND}")
    logger.info(f"Individual Upper Band: {UPPER_BAND}")
    logger.info(f"Max Iterations: {MAX_ITERATIONS}")
    logger.info("============ End of Configuration ============")
