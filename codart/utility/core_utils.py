from enum import Enum
from configparser import ConfigParser


class Core(Enum):
    UNDERSTAND = 0
    OPEN_UNDERSTAND = 1

def read_config_core()->int:
    config = ConfigParser()
    config.read("config.ini")
    try:
        return int(config["CORE"]["option"])
    except Exception as e:
        raise Exception("config value is not an integer !!!")