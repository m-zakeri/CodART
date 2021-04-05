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


if __name__ == '__main__':
    git_restore("/home/ali/Desktop/code/TestProject/")
