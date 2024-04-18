from abc import ABC, abstractmethod

class Refactoring(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def main(self, udb_path:str = "", file_path:str = "", source_class:str = "", moved_fields:str = "", moved_methods:str = "", *args, **kwargs) -> bool:
        raise NotImplementedError("main not implement")