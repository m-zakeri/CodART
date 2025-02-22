from abc import ABC, abstractmethod
from codart.learner.sbr_initializer.utils.utility import (
    DynamicAbstractMetaInitializeRefactoringMethods,
)
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")


class Initializer(ABC, metaclass=DynamicAbstractMetaInitializeRefactoringMethods):
    def __init__(
        self,
        udb_path: str = "",
        lower_band: int = 0,
        upper_band: int = 50,
        population_size: int = 50,
        *args,
        **kwargs,
    ):
        self.udb_path = udb_path
        self.population = []
        self.lower_band = lower_band
        self.upper_band = upper_band
        self.population_size = population_size
        self.refactoring_types = config["REFACTORING"]["types"].split(",")
        self.initializers = tuple(
            (getattr(self, f"init_{refactoring.strip()}"), {}, f"{refactoring.strip().replace('_', ' ').title()}")
            for refactoring in self.refactoring_types
        )

    @abstractmethod
    def generate_population(self):
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def generate_an_action(self):
        raise NotImplementedError(f"{type(self).__name__} not implement")

