"""
Utilities related to project directory.
"""

__author__ = 'Morteza Zakeri'
__version__ = '0.5.2'

import datetime
import os
import subprocess
from multiprocessing.dummy import Pool, Process, Manager

from antlr4 import FileStream
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from joblib import Parallel, delayed

import understand as und

# from java8speedy.parser import sa_javalabeled

from codart import config


def git_restore(project_dir):
    """
    This function returns a git supported project back to the initial commit

    Args:

        project_dir (str): The absolute path of project's directory.

    Returns:

        None

    """
    print(project_dir)
    assert os.path.isdir(project_dir)
    assert os.path.isdir(os.path.join(project_dir, '.git'))
    subprocess.Popen(["git", "restore", "."], cwd=project_dir, stdout=open(os.devnull, 'wb')).wait()
    subprocess.Popen(["git", "clean", "-f", "-d"], cwd=project_dir, stdout=open(os.devnull, 'wb')).wait()


def create_understand_database(project_dir: str = None, db_dir: str = None):
    """
    This function creates understand database for the given project directory.

    Args:

        project_dir (str): The absolute path of project's directory.

        db_dir (str): The absolute directory path to save Understand database (.udb or .und binary file)

    Returns:

        str: Understand database path

    """
    assert os.path.isdir(project_dir)
    db_name = os.path.basename(os.path.normpath(project_dir)) + ".und"
    db_path = os.path.join(db_dir, db_name)
    # print(project_dir, db_name, db_path)
    # quit()
    if os.path.exists(db_path):
        return db_path
    # An example of command-line is:
    # und create -languages c++ add @myFiles.txt analyze -all myDb.udb

    understand_5_cmd = ['und', 'create', '-languages', 'Java', 'add', project_dir, 'analyze', '-all', db_path]
    understand_6_cmd = ['und', 'create', '-db', db_path, '-languages', 'java']
    result = subprocess.run(understand_6_cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    if result.returncode != 0:
        error_ = result.stderr.decode('utf-8')
        config.logger.debug(f'return code: {result.returncode} msg: {error_}')
    else:
        config.logger.debug(f'Understand project was created successfully!')
    return db_path


def update_understand_database2(udb_path):
    """
    This function updates database due to file changes.
    Error message raised by understand 6.x:
    Error: The Analysis cannot be performed because the database is locked or read only

    Arges:

        udb_path (str): The absolute path of understand database.

    Return:

        None

    """
    understand_5_cmd = ['und', 'analyze', '-rescan', '-changed', udb_path]
    understand_6_cmd = ['und', 'analyze', '-changed', udb_path]  # -rescan option is not required for understand >= 6.0

    subprocess.Popen(
        understand_6_cmd,
        stdout=open(os.devnull, 'wb')
    ).wait()


def update_understand_database(udb_path):
    """
    This function updates database due to file changes.
    If any error, such as database is locked or read only, occurred it tries again and again to update db.

    Arges:

        udb_path (str): The absolute path of understand database.

    Return:

        None

    """
    understand_5_cmd = ['und', 'analyze', '-rescan', '-changed', udb_path]
    understand_6_cmd = ['und', 'analyze', '-changed', udb_path]  # -rescan option is not required for understand >= 6.0

    result = subprocess.run(understand_6_cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    # info_ = result.stdout.decode('utf-8')
    # error_ = result.stderr.decode('utf-8')
    # print(info_[:85])
    # print(f'return code: {result.returncode} --- error: {error_}')
    trials = 0
    while result.returncode != 0:
        try:
            db: und.Db = und.open(config.UDB_PATH)
            db.close()
        except:
            pass
        finally:

            result = subprocess.run(understand_6_cmd,  #
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            # info_ = result.stdout.decode('utf-8')
            error_ = result.stderr.decode('utf-8')
            # print(info_[:85])
            config.logger.debug(f'return code: {result.returncode} msg: {error_}')
            trials += 1
            if trials > 5:
                break

    # Try to close und.exe process if it has not been killed automatically
    result = subprocess.run(['taskkill', '/f', '/im', 'und.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        config.logger.debug('The und.exe process is not running')
    else:
        config.logger.debug('The und.exe process killed manually')


def export_understand_dependencies_csv2(csv_path: str, db_path: str):
    """
    Exports understand dependencies into a csv file.

    :param csv_path: The absolute address of csv file to generate.
    :param db_path: The absolute address of project path.
    :return: None
    """
    command = ['und', 'export', '-format', 'long', '-dependencies', 'class', 'csv', csv_path, db_path]
    subprocess.Popen(
        command,
        stdout=open(os.devnull, 'wb')
    ).wait()
    config.logger.debug("Modular dependency graph (MDG.csv) was exported.")


def export_understand_dependencies_csv(csv_path: str, db_path: str):
    """
    Exports understand dependencies into a csv file.

    :param csv_path: The absolute address of csv file to generate.
    :param db_path: The absolute address of project path.
    :return: None
    """
    command = ['und', 'export', '-format', 'long', '-dependencies', 'class', 'csv', csv_path, db_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    trials = 0
    while result.returncode != 0:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error_ = result.stderr.decode('utf-8')
        config.logger.debug(f'return code: {result.returncode} msg: {error_}')
        trials += 1
        if trials > 5:
            break
    config.logger.debug("Modular dependency graph (MDG.csv) was exported.")
    # Try to close und.exe process if it has not been killed automatically
    result = subprocess.run(['taskkill', '/f', '/im', 'und.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        config.logger.debug('The und.exe process is not running')
    else:
        config.logger.debug('The und.exe process killed manually')


def reset_project(quit_=False):
    # Stage 0: Git restore
    config.logger.debug("Executing git restore.")
    # git restore .
    # git clean -f -d
    git_restore(config.PROJECT_PATH)
    config.logger.debug("Updating understand database after git restore.")
    update_understand_database(config.UDB_PATH)
    if quit_:
        quit()


# -----------------------------------------------
# trees = []
shared_set = set()


def get_java_files(directory):
    if not os.path.isdir(directory):
        raise ValueError("directory should be an absolute path of a directory!")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split('.')[-1] == 'java':
                yield os.path.join(root, file)  # , file
                # print(os.path.join(root, file), file)
                # yield FileStream(os.path.join(root, file), encoding="utf8")


def create_project_parse_tree(java_file_path):
    tree = None
    rewriter = None
    try:
        file_stream = FileStream(java_file_path, encoding='utf-8', errors='ignore')
        sa_javalabeled.USE_CPP_IMPLEMENTATION = config.USE_CPP_BACKEND
        tree = sa_javalabeled.parse(file_stream, 'compilationUnit')
        tokens = tree.parser.getInputStream()
        rewriter = TokenStreamRewriter(tokens)
    except Exception as e:
        print(f'Encounter a parsing error on file {java_file_path}')
        print(e)
    return tree, rewriter


def parallel_parsing(directory):
    trees = list()
    input_files = [java_file for java_file in get_java_files(directory)]
    # pool = Pool(processes=8)
    # x = pool.apply_async(create_project_parse_tree, args=(input_files[0], trees))

    # for java_file in get_java_files(directory):
    #     res = pool.apply_async(create_project_parse_tree, (java_file,))  # runs in *only* one process
    #     print(type(res.get(timeout=1)))  #

    # num = Value('d', 0.0)
    # arr = Array('i', range(500))
    with Manager() as manager:
        d = manager.dict()
        q = manager.Queue(10)
        p = Process(target=create_project_parse_tree, args=(input_files[0], q))
        p.start()
        p.join()
        print(q)

    # x.ready()
    # print(len(x.get()))
    # print(arr[0])


def parallel_parsing2(directory):
    for java_file in get_java_files(directory):
        print(java_file)
        p = Process(target=create_project_parse_tree, args=(java_file,))
        p.start()
        # p.join()


def parallel_parsing3(directory):
    d1 = datetime.datetime.now()
    pool = Pool()
    x = pool.map(create_project_parse_tree, get_java_files(directory))
    d2 = datetime.datetime.now()
    print(d2 - d1, len(x))
    return x


# @wrap_non_picklable_objects
def parallel_parsing4(directory):
    d1 = datetime.datetime.now()
    res = Parallel(n_jobs=8, )(
        delayed(create_project_parse_tree)(java_file) for java_file in get_java_files(directory)
    )
    print(res)
    d2 = datetime.datetime.now()
    print(d2 - d1)
    return []


def typical_parsing(directory):
    d1 = datetime.datetime.now()
    x = []
    for java_file in get_java_files(directory):
        x.append(create_project_parse_tree(java_file))
    d2 = datetime.datetime.now()
    print(d2 - d1, len(x))
    return x


# Test methods
def test_typyical_and_parallel_parsing():
    # directory = r'D:/IdeaProjects/JSON20201115/'
    # directory = r'D:/IdeaProjects/jvlt-1.3.2/'
    # directory = r'D:/IdeaProjects/ganttproject_1_11_1_original/'
    # directory = r'D:/IdeaProjects/105_freemind/'
    # directory = r'D:/IdeaProjects/jfreechart-master_original/'
    directory = r'D:/IdeaProjects/107_weka/'
    # directory = r'D:/IdeaProjects/104_vuze/'
    # directory = r'D:/IdeaProjects/Zarebin/'

    # trees = parallel_parsing4(directory)
    # trees = parallel_parsing3(directory)
    trees = typical_parsing(directory)

    # trees = typical_parsing(directory)
    print(f'parse successfully {len(trees)} trees')


def test_understand_update():
    db: und.Db = und.open(config.UDB_PATH)
    for i in range(0, 10):
        lnx = db.language()
        # print(lnx)
        update_understand_database(config.UDB_PATH)


if __name__ == '__main__':
    # test_typyical_and_parallel_parsing()
    test_understand_update()
