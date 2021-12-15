import os
import logging

POPULATION_SIZE = os.environ.get("POPULATION_SIZE", 100)
INDIVIDUAL_SIZE = os.environ.get("INDIVIDUAL_SIZE", 3)
MAX_ITERATIONS = 1000
LOWER_BAND = 2
UPPER_BAND = 4
UDB_PATH = "D:\Final Project\IdeaProjects\JSON20201115\JSON20201115.und"
PROJECT_PATH = "D:\Final Project\IdeaProjects\JSON20201115"
PROJECT_NAME = os.path.basename(PROJECT_PATH)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(f'./logs/{PROJECT_NAME}.log'),
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
