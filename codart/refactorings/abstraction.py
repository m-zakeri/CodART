from abc import ABC, abstractmethod
from codart.utility.commons.granularity import Granularity


class Refactoring(ABC):
    """
        God class of refactoring activities
    """

    def __init__(self, name: str = "", granularity: Granularity = Granularity.METHOD):
        self.name = name
        self.granularity = granularity


    @abstractmethod
    def do_refactoring(self,
                       udb_path: str = "",
                       file_path: str = "",
                       *args, **kwargs) -> bool:
        self.detect_smell()
        self.identify_opportunities()
        self.check_precondition()
        self.apply_refactoring()
        self.check_post_condition()

    @abstractmethod
    def detect_smell(self, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def identify_opportunities(self, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def check_precondition(self, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def apply_refactoring(self, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def check_post_condition(self, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")