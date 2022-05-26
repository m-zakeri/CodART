"""
Simple search-based refactoring with random-search algorithm

"""

__version__ = '0.1.'
__author__ = 'Morteza Zakeri'


import random

from initialize import RandomInitialization
from codart.metrics.qmood import DesignQualityAttributes
from codart.utility.directory_utils import update_understand_database, git_restore
from codart.config import *

# udb_path = "D:\Dev\ganttproject\ganttproject.udb"
# project_dir = "D:\Dev\ganttproject"
udb_path = "D:\Dev\JavaSample\JavaSample1.udb"
project_dir = "D:\Dev\JavaSample"

rand_init = RandomInitialization(
        udb_path=udb_path,
        population_size=POPULATION_SIZE,
        lower_band=LOWER_BAND,
        upper_band=UPPER_BAND
    )
rand_pop = rand_init.generate_population()
score = DesignQualityAttributes(udb_path=udb_path).reusability
k = 0
limit = len(rand_pop)
best_answer = None
print("Reusability before starting the algorithm:", score)
# Random search for improving reusability
while k < MAX_ITERATIONS and limit > 0:
    print("Iteration No.", k)
    index = random.randint(0, limit-1)
    limit -= 1
    print(f"index is {index}")
    individual = rand_pop.pop(index)
    print(f"len(individual) is {len(individual)}")
    # git restore prev changes
    git_restore(project_dir)
    # execute individual
    for refactoring, params in individual:
        print(params)
        try:
            refactoring(**params)
        except Exception as e:
            print(e)
        # update understand database
        update_understand_database(udb_path)
    # calculate objective
    obj_score = DesignQualityAttributes(udb_path=udb_path).reusability
    print("Objective Score", obj_score)
    if obj_score < score:
        score = obj_score
        best_answer = individual
    k += 1

print("=" * 75)
print("Best Score", score)
print("Best Answer", best_answer)
