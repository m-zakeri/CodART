import os

POPULATION_SIZE = os.environ.get("POPULATION_SIZE", 100)
INDIVIDUAL_SIZE = os.environ.get("INDIVIDUAL_SIZE", 3)
MAX_ITERATIONS = 1000