from abc import ABC, abstractmethod
from codart.utility.commons.granularity import Granularity
from pydantic import BaseModel
from pydantic.types import Dict
import torch

class RefactoringModel(BaseModel):
    name: str
    params:  Dict[str, Dict[str, str]]


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



class RefactoringOperation(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def get_refactoring(self, *args, **kwargs) -> RefactoringModel:
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @property
    @abstractmethod
    def shape(self):
        """Returns the shape of the action."""
        return torch.Size([1])

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the operation does not have meaningful data."""
        raise NotImplementedError(f"{type(self).__name__} does not implement is_empty.")