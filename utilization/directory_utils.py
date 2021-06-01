"""
Utilities related to project directory.
"""

import os
import subprocess


def git_restore(project_dir):
    """
    This function executes "git restore ." on the given project directory.
    :param project_dir: A string and Absolute path of the project's directory.
    :return: None
    """
    assert os.path.isdir(project_dir)
    process = subprocess.Popen(["git", "restore", "."], cwd=project_dir)
    process.wait()


def create_understand_database(project_dir, und_path='/data/Dev/scitools/bin/linux64'):
    """
    This function creates understand database for the given project directory.
    :param und_path: The path of und binary file for executing understand command-line
    :param project_dir: The absolute path of project's directory.
    :return: String path of created database.
    """
    assert os.path.isdir(project_dir)
    assert os.path.isdir(und_path)
    db_name = os.path.basename(os.path.normpath(project_dir)) + ".udb"
    db_path = os.path.join(project_dir, db_name)
    assert os.path.exists(db_path) is False
    # An example of command-line is:
    # und create -languages c++ add @myFiles.txt analyze -all myDb.udb
    process = subprocess.Popen(
        ['und', 'create', '-db', db_path, '-languages',
            'Java', 'add', project_dir, 'analyze', '-all'],
        cwd=und_path
    )
    process.wait()
    return db_path


def update_understand_database(udb_path, project_dir=None, und_path='/data/Dev/scitools/bin/linux64'):
    """
    This function updates database due to file changes.
    :param project_dir: If understand database file is not in project directory you can specify the project directory.
    :param und_path: The path of und binary file for executing understand command-line
    :param udb_path: The absolute path of understand database.
    :return: None
    """
    assert os.path.isfile(udb_path)
    assert os.path.isdir(und_path)
    if project_dir is None:
        project_dir = os.path.dirname(os.path.normpath(udb_path))

    process = subprocess.Popen(
        ['und', 'analyze', '-all', udb_path],
        cwd=und_path
    )
    process.wait()
