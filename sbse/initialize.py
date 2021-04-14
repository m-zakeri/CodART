import random, progressbar

from utilization.setup_understand import *
from refactorings import make_field_non_static, make_field_static, make_method_static_2, make_method_non_static

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


def inti_make_field_static(udb_path):
    """
    Randomly selects a candidate for this refactoring.
    :param udb_path: Path for understand database file.
    :return: refactoring main method and its parameters.
    """
    refactoring_main = make_field_static.main
    params = {
        "udb_path": udb_path,
        "source_class": "random",
        "field_name": "random"
    }
    udb = und.open(udb_path)
    candidates = []
    for ent in sorted(udb.ents("variable"), key=lambda ent: ent.name()):
        if 'static' in ent.kindname().lower():
            continue
        source_class, field_name = ent.name().split('.')
        candidates.append({'source_class': source_class, 'field_name': field_name})
    params.update(random.choice(candidates))
    return refactoring_main, params


def init_make_method_static(udb_path):
    """
    Randomly selects a candidate for this refactoring.
    :param udb_path: Path for understand database file.
    :return: refactoring main method and its parameters.
    """
    refactoring_main = make_method_static_2.main
    params = {
        "udb_path": udb_path,
        "source_class": "random",
        "method_name": "random"
    }
    udb = und.open(udb_path)
    candidates = []
    blacklist = ('constructor', 'static', 'abstract', 'unknown',)
    for ent in sorted(udb.ents("method"), key=lambda ent: ent.name()):
        kind_name = ent.kindname().lower()
        if any(word in kind_name for word in blacklist):
            continue
        source_class, method_name = ent.name().split('.')
        candidates.append({'source_class': source_class, 'method_name': method_name})
    params.update(random.choice(candidates))
    return refactoring_main, params


def init_make_method_non_static(udb_path):
    """
    Randomly selects a candidate for this refactoring.
    :param udb_path: Path for understand database file.
    :return: refactoring main method and its parameters.
    """
    refactoring_main = make_method_non_static.main
    params = {
        "udb_path": udb_path,
        "source_class": "random",
        "method_name": "random"
    }
    udb = und.open(udb_path)
    candidates = []
    blacklist = ('abstract', 'unknown', 'constructor',)
    for ent in sorted(udb.ents("static method"), key=lambda ent: ent.name()):
        kind_name = ent.kindname().lower()
        if any(word in kind_name for word in blacklist):
            continue
        source_class, method_name = ent.name().split('.')
        candidates.append({'source_class': source_class, 'method_name': method_name})
    params.update(random.choice(candidates))
    return refactoring_main, params


def generate_population(udb_path, population_size=50, gene_size=4):
    initializers = (
        init_make_field_non_static,
        inti_make_field_static,
        init_make_method_static,
        init_make_method_non_static,
    )
    population = []
    for i in progressbar.progressbar(range(population_size)):
        genes = []
        for j in range(gene_size):
            genes.append(random.choice(initializers)("/home/ali/Desktop/code/TestProject/TestProject.udb"))
        population.append(genes)

    print(f"len of population is: {len(population)}")
    return population


if __name__ == '__main__':
    print(generate_population(
        "/home/ali/Desktop/code/TestProject/TestProject.udb",
        population_size=10
    ))
