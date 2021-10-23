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


def create_understand_database(project_dir):
    """
    This function creates understand database for the given project directory.
    :param und_path: The path of und binary file for executing understand command-line
    :param project_dir: The absolute path of project's directory.
    :return: String path of created database.
    """
    assert os.path.isdir(project_dir)
    db_name = os.path.basename(os.path.normpath(project_dir)) + ".udb"
    db_path = os.path.join(project_dir, db_name)
    assert os.path.exists(db_path) is False
    # An example of command-line is:
    # und create -languages c++ add @myFiles.txt analyze -all myDb.udb
    process = subprocess.Popen(
        ['und', 'create', '-languages', 'Java', 'add', project_dir, 'analyze', '-all', db_path],
        stdout=open(os.devnull, 'wb')
    )
    process.communicate()
    return db_path


def update_understand_database(udb_path):
    """
    This function updates database due to file changes.
    :param udb_path: The absolute path of understand database.
    :return: None
    """

    process = subprocess.Popen(
        ['und', 'analyze', '-all', udb_path],
        stdout=open(os.devnull, 'wb')
    )
    process.communicate()
    print("Finished updating...")
