import random

from utilization.setup_understand import *
from refactorings import make_field_non_static

from utilization.directory_utils import update_understand_database


def init_make_field_non_static(udb_path):
    """
    Randomly selects a candidate for this refactoring.
    :param udb_path: Path for understand database file.
    :return: refactoring main method and its parameters.
    """
    refactoring_main = make_field_non_static.main
    params = {
        "udb_path": udb_path,
        "source_class": "random",
        "field_name": "random"
    }
    udb = und.open(udb_path)
    candidates = []
    for ent in sorted(udb.ents("static variable"), key=lambda ent: ent.name()):
        source_class, field_name = ent.name().split('.')
        candidates.append({'source_class': source_class, 'field_name': field_name})
    params.update(random.choice(candidates))
    return refactoring_main, params


if __name__ == '__main__':
    update_understand_database("/home/ali/Desktop/code/TestProject/TestProject.udb")
    print(init_make_field_non_static("/home/ali/Desktop/code/TestProject/TestProject.udb"))
