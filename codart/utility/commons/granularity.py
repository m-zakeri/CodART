from enum import Enum

class Granularity(Enum):
    """
    Refactoring level enum
    """
    METHOD = 1
    CLASS = 2
    FILE = 3