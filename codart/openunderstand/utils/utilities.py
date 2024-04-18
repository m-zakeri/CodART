import time
import logging
import configparser
from os.path import basename
from openunderstand.gen.javaLabeled import JavaParserLabeled


class ClassTypeData:
    def __init__(self):
        self.parentClass = None
        self.childClass = None
        self.file_path: str = ""
        self.package_name: str = ""
        self.line: int = -1
        self.column: int = -1
        self.prefixes: list = []

    def set_child_class(self, child):
        self.childClass = child

    def set_parent_class(self, parent):
        self.parentClass = parent

    def set_file_path(self, file_path: str):
        self.file_path = file_path

    def set_package_name(self, name: str):
        self.package_name = name

    def set_line(self, line: int):
        self.line = line

    def set_column(self, column: int):
        self.column = column

    def set_prefixes(self, prefix_list: list):
        self.prefixes = prefix_list

    def get_long_name(self) -> str:
        return self.package_name + "." + self.childClass.getText()

    def get_type(self) -> str:
        return "extends" + " " + self.parentClass

    def get_name(self) -> str:
        return str(self.childClass.IDENTIFIER())

    def get_contents(self) -> str:
        return self.childClass.getText()

    def get_prefixes(self) -> list:
        return self.prefixes


def timer_decorator():
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            logger = setup_logger()
            start_time = time.time()
            file_address = kwargs.get("file_address")
            result = func(self, *args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(
                f"The function '{func.__name__}' with file address '{basename(file_address)}' took {elapsed_time:.2f} seconds to execute."
            )
            return result

        return wrapper

    return decorator


import os


def setup_config():
    config = configparser.ConfigParser()
    config.read(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", "config.ini"
        )
    )
    return config


def setup_logger():
    # Read configurations from config.ini file
    config = setup_config()

    # Create logger object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create file handler and set the log level based on the configuration
    file_handler = logging.FileHandler(config["Logging"]["filename"])
    file_handler.setLevel(getattr(logging, config["Logging"]["level"].upper()))

    # Create log formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add file handler to the logger
    logger.addHandler(file_handler)

    return logger
