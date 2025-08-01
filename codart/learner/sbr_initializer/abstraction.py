from abc import ABC, abstractmethod
from codart.learner.sbr_initializer.utils.utility import (DynamicAbstractMetaInitializeRefactoringMethods)
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
        project_name: str = "",
        version_id: str = "",
        *args,
        **kwargs,
    ):
        self.udb_path = udb_path
        self.project_name = project_name
        self.version_id = version_id
        self.population = []
        self.lower_band = lower_band
        self.upper_band = upper_band
        self.population_size = population_size
        self.refactoring_types = ["extract_class","move_method","pull_up_method","push_down_method","extract_method"]
        self.initializers = tuple(
            (
                getattr(self, f"init_{refactoring.strip()}"),
                {},
                f"{refactoring.strip().replace('_', ' ').title()}",
            )
            for refactoring in self.refactoring_types
        )

    @abstractmethod
    def generate_population(self):
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def generate_an_action(self):
        raise NotImplementedError(f"{type(self).__name__} not implement")
