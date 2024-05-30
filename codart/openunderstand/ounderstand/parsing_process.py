from openunderstand.ounderstand.project import Project
from openunderstand.ounderstand.listeners_and_parsers import ListenersAndParsers
import os
from openunderstand.utils.utilities import setup_config
from fnmatch import fnmatch


def get_files(dirName: str = ""):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_files(fullPath)
        # checks whether the fullPath content is a .java or not
        elif fnmatch(fullPath, "*.java"):
            allFiles.append(fullPath)
    return allFiles


def process_file(file_address):
    p = Project()
    lap = ListenersAndParsers()
    tree, parse_tree, file_ent = lap.parser(file_address=file_address, p=p)
    if tree is None and parse_tree is None and file_ent is None:
        return
    entity_generator = lap.entity_gen(file_address=file_address, parse_tree=parse_tree)
    listeners = [
        lap.create_listener,
        lap.type_listener,
        lap.define_listener,
        lap.declare_listener,
        lap.override_listener,
        lap.callby_listener,
        lap.couple_listener,
        lap.useby_listener,
        lap.setby_listener,
        lap.setinitby_listener,
        lap.setbypartialby_listener,
        lap.dotref_listener,
        lap.throws_listener,
        lap.extend_coupled_listener,
        lap.variable_listener,
        lap.callbyNonDynamic_listener,
        lap.cast_by_listener,
        lap.contain_in_listener,
        lap.extend_implict_listener,
        lap.import_demand_listener,
        lap.import_listener,
        lap.open_by_listener,
        lap.use_module_listener,
    ]
    lap.modify_listener(
        entity_generator=entity_generator,
        parse_tree=parse_tree,
        file_address=file_address,
        p=p,
    )
    for listener in listeners:
        listener(file_address=file_address, p=p, file_ent=file_ent, tree=tree)
