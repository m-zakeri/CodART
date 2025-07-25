"""
Utilities related to project directory with memory monitoring and optimization.
"""

__author__ = 'Morteza Zakeri'
__version__ = '0.5.2'

import datetime
import os
import subprocess
import psutil
import gc
import time
from multiprocessing.dummy import Pool, Process, Manager
from codart.learner.sbr_initializer.utils.utility import logger, config
from antlr4 import FileStream
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from joblib import Parallel, delayed

import understand as und
from antlr4 import FileStream, CommonTokenStream
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from codart.gen.JavaLexer import JavaLexer
from codart.gen.JavaParserLabeled import JavaParserLabeled


def log_memory_usage(stage_name, pid=None):
    """
    Log current memory usage for debugging memory issues.

    Args:
        stage_name (str): Name of the current stage/operation
        pid (int, optional): Process ID to monitor. If None, monitors current process.
    """
    try:
        if pid is None:
            process = psutil.Process()
        else:
            process = psutil.Process(pid)

        memory_info = process.memory_info()
        memory_percent = process.memory_percent()

        # Get system memory info
        system_memory = psutil.virtual_memory()

        logger.info(f"[MEMORY] {stage_name}:")
        logger.info(f"  Process RSS: {memory_info.rss / 1024 / 1024:.1f} MB")
        logger.info(f"  Process VMS: {memory_info.vms / 1024 / 1024:.1f} MB")
        logger.info(f"  Process Memory %: {memory_percent:.1f}%")
        logger.info(f"  System Available: {system_memory.available / 1024 / 1024:.1f} MB")
        logger.info(f"  System Used %: {system_memory.percent:.1f}%")

        # Warning if memory usage is high
        if memory_percent > 80 or system_memory.percent > 90:
            logger.warning(f"[MEMORY WARNING] High memory usage detected!")
            logger.warning(f"  Process: {memory_percent:.1f}%, System: {system_memory.percent:.1f}%")

        return {
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'process_percent': memory_percent,
            'system_percent': system_memory.percent,
            'system_available_mb': system_memory.available / 1024 / 1024
        }

    except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
        logger.error(f"[MEMORY] Failed to get memory info for {stage_name}: {e}")
        return None


def force_cleanup():
    """
    Force garbage collection and cleanup to free memory.
    """
    logger.debug("[CLEANUP] Starting memory cleanup...")

    # Force garbage collection
    collected = gc.collect()
    logger.debug(f"[CLEANUP] Garbage collected {collected} objects")

    # Get memory usage after cleanup
    try:
        process = psutil.Process()
        memory_after = process.memory_info()
        logger.debug(f"[CLEANUP] Memory after cleanup: {memory_after.rss / 1024 / 1024:.1f} MB RSS")
    except Exception as e:
        logger.debug(f"[CLEANUP] Could not get memory info after cleanup: {e}")


def run_subprocess_with_monitoring(cmd, cwd=None, timeout=3600, stage_name="subprocess"):
    """
    Run subprocess with memory monitoring and proper cleanup.

    Args:
        cmd (list): Command to execute
        cwd (str): Working directory
        timeout (int): Timeout in seconds
        stage_name (str): Name for logging

    Returns:
        tuple: (success, process_result)
    """
    logger.debug(f"[SUBPROCESS] Starting {stage_name}: {' '.join(cmd)}")
    log_memory_usage(f"Before {stage_name}")

    process = None
    try:
        # Start process with proper configuration
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered to reduce memory usage
            universal_newlines=True
        )

        # Monitor process with timeout
        start_time = time.time()
        while process.poll() is None:
            # Check timeout
            if time.time() - start_time > timeout:
                logger.error(f"[SUBPROCESS] {stage_name} timed out after {timeout}s")
                process.terminate()
                time.sleep(2)
                if process.poll() is None:
                    process.kill()
                return False, None

            # Monitor memory every 5 seconds
            if int(time.time() - start_time) % 5 == 0:
                try:
                    log_memory_usage(f"During {stage_name}", process.pid)
                except:
                    pass

            time.sleep(1)

        # Get final result
        stdout, stderr = process.communicate()
        returncode = process.returncode

        if returncode == 0:
            logger.debug(f"[SUBPROCESS] {stage_name} completed successfully")
            return True, {'stdout': stdout, 'stderr': stderr, 'returncode': returncode}
        else:
            logger.error(f"[SUBPROCESS] {stage_name} failed with code {returncode}")
            logger.error(f"[SUBPROCESS] Error: {stderr}")
            return False, {'stdout': stdout, 'stderr': stderr, 'returncode': returncode}

    except subprocess.TimeoutExpired:
        logger.error(f"[SUBPROCESS] {stage_name} communication timed out")
        if process:
            process.kill()
        return False, None

    except Exception as e:
        logger.error(f"[SUBPROCESS] {stage_name} failed with exception: {e}")
        if process and process.poll() is None:
            try:
                process.terminate()
                time.sleep(2)
                if process.poll() is None:
                    process.kill()
            except:
                pass
        return False, None

    finally:
        # Cleanup
        if process:
            try:
                if process.poll() is None:
                    process.terminate()
            except:
                pass

        log_memory_usage(f"After {stage_name}")
        force_cleanup()


def git_restore(project_dir: str = ""):
    """
    This function returns a git supported project back to the initial commit
    with comprehensive memory monitoring and error handling.

    Args:
        project_dir (str): The absolute path of project's directory.

    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"[GIT_RESTORE] Starting git restore for: {project_dir}")
    log_memory_usage("Git restore start")

    # Validate input
    if not project_dir:
        logger.error("[GIT_RESTORE] No project directory provided")
        return False

    if not os.path.isdir(project_dir):
        logger.error(f"[GIT_RESTORE] Project directory does not exist: {project_dir}")
        return False

    # Find actual git repository
    actual_project_dir = project_dir
    git_dir = os.path.join(project_dir, '.git')

    logger.debug(f"[GIT_RESTORE] Checking for git repository in: {project_dir}")

    if not os.path.isdir(git_dir):
        logger.debug("[GIT_RESTORE] No .git directory found, checking subdirectories...")

        try:
            # Get subdirectories efficiently
            subdirs = []
            for item in os.listdir(project_dir):
                item_path = os.path.join(project_dir, item)
                if os.path.isdir(item_path) and not item.startswith('.'):
                    subdirs.append(item)

            log_memory_usage("After listing subdirectories")

            git_found = False
            for subdir in subdirs:
                subdir_path = os.path.join(project_dir, subdir)
                subdir_git = os.path.join(subdir_path, '.git')

                if os.path.isdir(subdir_git):
                    actual_project_dir = subdir_path
                    git_dir = subdir_git
                    git_found = True
                    logger.info(f"[GIT_RESTORE] Found git repository in subdirectory: {actual_project_dir}")
                    break

            if not git_found:
                logger.warning(f"[GIT_RESTORE] No git repository found, initializing new one")
                success = initialize_git_repository(project_dir)
                if success:
                    actual_project_dir = project_dir
                else:
                    return False
            else:
                # Configure safe directory for found repository
                configure_safe_directory(actual_project_dir)

        except Exception as e:
            logger.error(f"[GIT_RESTORE] Error while searching for git repository: {e}")
            return False
    else:
        logger.debug("[GIT_RESTORE] Git repository found")
        configure_safe_directory(actual_project_dir)

    # Perform git restore operations
    logger.info(f"[GIT_RESTORE] Performing git restore in: {actual_project_dir}")

    try:
        # Git restore
        success, result = run_subprocess_with_monitoring(
            ["git", "restore", "."],
            cwd=actual_project_dir,
            stage_name="git restore"
        )

        if not success:
            logger.error("[GIT_RESTORE] Git restore command failed")
            return False

        # Git clean
        success, result = run_subprocess_with_monitoring(
            ["git", "clean", "-f", "-d"],
            cwd=actual_project_dir,
            stage_name="git clean"
        )

        if not success:
            logger.error("[GIT_RESTORE] Git clean command failed")
            return False

        logger.info(f"[GIT_RESTORE] Git restore completed successfully for {actual_project_dir}")
        log_memory_usage("Git restore completion")

        return True

    except Exception as e:
        logger.error(f"[GIT_RESTORE] Git restore failed for {actual_project_dir}: {e}")
        return False

    finally:
        # Final cleanup
        force_cleanup()


def configure_safe_directory(project_dir):
    """
    Configure git safe directory to avoid dubious ownership errors.

    Args:
        project_dir (str): Project directory to configure
    """
    try:
        success, result = run_subprocess_with_monitoring(
            ["git", "config", "--global", "--add", "safe.directory", project_dir],
            stage_name="git config safe directory"
        )

        if success:
            logger.debug(f"[GIT_RESTORE] Configured safe directory: {project_dir}")
        else:
            logger.debug(f"[GIT_RESTORE] Could not configure safe directory: {project_dir}")

    except Exception as e:
        logger.debug(f"[GIT_RESTORE] Error configuring safe directory: {e}")


def initialize_git_repository(project_dir):
    """
    Initialize a new git repository with proper error handling.

    Args:
        project_dir (str): Directory to initialize git repository in

    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"[GIT_RESTORE] Initializing git repository in {project_dir}")

    try:
        # Configure safe directory first
        configure_safe_directory(project_dir)

        # Initialize git repository
        success, result = run_subprocess_with_monitoring(
            ["git", "init"],
            cwd=project_dir,
            stage_name="git init"
        )

        if not success:
            logger.error("[GIT_RESTORE] Failed to initialize git repository")
            return False

        # Add all files
        success, result = run_subprocess_with_monitoring(
            ["git", "add", "."],
            cwd=project_dir,
            stage_name="git add"
        )

        if not success:
            logger.error("[GIT_RESTORE] Failed to add files to git repository")
            return False

        # Create initial commit
        success, result = run_subprocess_with_monitoring(
            ["git", "commit", "-m", "Initial commit"],
            cwd=project_dir,
            stage_name="git commit"
        )

        if not success:
            logger.error("[GIT_RESTORE] Failed to create initial commit")
            return False

        logger.info(f"[GIT_RESTORE] Git repository initialized successfully in {project_dir}")
        return True

    except Exception as e:
        logger.error(f"[GIT_RESTORE] Failed to initialize git repository: {e}")
        return False


# Keep the rest of your existing functions but add memory monitoring to critical ones

def update_understand_database(udb_path):
    """
    This function updates database due to file changes with memory monitoring.
    If any error, such as database is locked or read only, occurred it tries again.

    Args:
        udb_path (str): The absolute path of understand database.

    Return:
        bool: True if successful, False otherwise
    """
    logger.info(f"[UDB_UPDATE] Starting database update: {udb_path}")
    log_memory_usage("UDB update start")

    if not os.path.exists(udb_path):
        logger.error(f"[UDB_UPDATE] Database file does not exist: {udb_path}")
        return False

    understand_6_cmd = ['und', 'analyze', '-changed', udb_path]
    max_trials = 5
    trials = 0

    while trials < max_trials:
        logger.debug(f"[UDB_UPDATE] Attempt {trials + 1}/{max_trials}")

        success, result = run_subprocess_with_monitoring(
            understand_6_cmd,
            stage_name=f"und analyze (attempt {trials + 1})"
        )

        if success:
            logger.info(f"[UDB_UPDATE] Database updated successfully after {trials + 1} attempts")
            cleanup_understand_processes()
            log_memory_usage("UDB update completion")
            return True

        trials += 1

        if trials < max_trials:
            logger.warning(f"[UDB_UPDATE] Attempt {trials} failed, retrying...")

            # Try to close and reopen database
            try:
                db = und.open(udb_path)
                db.close()
                logger.debug("[UDB_UPDATE] Reopened database connection")
            except Exception as e:
                logger.debug(f"[UDB_UPDATE] Could not reopen database: {e}")

            # Wait before retry
            time.sleep(2)
            force_cleanup()

    logger.error(f"[UDB_UPDATE] Failed to update database after {max_trials} attempts")
    cleanup_understand_processes()
    return False


def cleanup_understand_processes():
    """
    Clean up any lingering Understand processes to prevent memory leaks.
    """
    logger.debug("[CLEANUP] Cleaning up Understand processes")

    commands_to_try = [
        {
            'check': ['which', 'pkill'],
            'execute': ['pkill', '-f', 'und'],
            'success_msg': 'Understand processes killed with pkill'
        },
        {
            'check': ['which', 'killall'],
            'execute': ['killall', 'und'],
            'success_msg': 'Understand processes killed with killall'
        }
    ]

    for cmd_info in commands_to_try:
        try:
            # Check if command exists
            check_result = subprocess.run(
                cmd_info['check'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if check_result.returncode == 0:
                # Execute kill command
                kill_result = subprocess.run(
                    cmd_info['execute'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                if kill_result.returncode == 0:
                    logger.debug(f"[CLEANUP] {cmd_info['success_msg']}")
                    break
                else:
                    logger.debug("[CLEANUP] No Understand processes found to kill")

        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            logger.debug(f"[CLEANUP] Kill command failed: {e}")
            continue

    force_cleanup()


def reset_project(quit_=False, project_path: str = "", udb_path: str = ""):
    """
    Reset project with comprehensive memory monitoring.

    Args:
        quit_ (bool): Whether to quit after reset
        project_path (str): Project directory path
        udb_path (str): Understand database path

    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("[RESET] Starting project reset")
    log_memory_usage("Project reset start")

    try:
        # Stage 1: Git restore
        logger.info("[RESET] Stage 1: Git restore")
        git_success = git_restore(project_dir=project_path)

        if not git_success:
            logger.error("[RESET] Git restore failed")
            return False

        # Stage 2: Update Understand database
        logger.info("[RESET] Stage 2: Updating understand database")
        udb_success = update_understand_database(udb_path=udb_path)

        if not udb_success:
            logger.error("[RESET] Understand database update failed")
            return False

        logger.info("[RESET] Project reset completed successfully")
        log_memory_usage("Project reset completion")

        if quit_:
            logger.info("[RESET] Quitting as requested")
            quit()

        return True

    except Exception as e:
        logger.error(f"[RESET] Project reset failed: {e}")
        return False

    finally:
        force_cleanup()


def create_understand_database(project_dir: str = None, db_dir: str = None):
    """
    Create understand database for the given project directory.

    Args:
        project_dir (str): The absolute path of project's directory.
        db_dir (str): The absolute directory path to save Understand database

    Returns:
        str: Understand database path
    """
    assert os.path.isdir(project_dir), f"Project directory does not exist: {project_dir}"

    db_name = os.path.basename(os.path.normpath(project_dir))
    db_path = os.path.join(db_dir, f"{db_name}")  # Added .udb extension

    if os.path.exists(db_path):
        return db_path

    create_cmd = [
        'und',
        'create',
        '-languages',
        'java',
        db_path
    ]
    db_path = db_path + '.und'
    # Second command: Add project files
    add_cmd = [
        'und',
        'add',
        project_dir,
        '-db',
        db_path,
    ]

    # Third command: Analyze the database
    analyze_cmd = [
        'und',
        'analyze',
        '-db',
        db_path,
        '-all'
    ]

    commands = [create_cmd, add_cmd, analyze_cmd]

    try:
        for cmd in commands:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True  # This will raise CalledProcessError if return code is non-zero
            )
            print(f'Successfully executed: {" ".join(cmd)}')
            print(f'Output: {result.stdout}')

        print('Understand project was created and analyzed successfully!')
        return db_path

    except subprocess.CalledProcessError as e:
        print(f'Command failed with return code {e.returncode}')
        print(f'Error output: {e.stderr}')
        raise RuntimeError(f"Failed to process Understand database: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


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
    logger.debug("Modular dependency graph (MDG.csv) was exported.")


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
        logger.debug(f'return code: {result.returncode} msg: {error_}')
        trials += 1
        if trials > 5:
            break
    logger.debug("Modular dependency graph (MDG.csv) was exported.")
    # Try to close und.exe process if it has not been killed automatically
    result = subprocess.run(['taskkill', '/f', '/im', 'und.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logger.debug('The und.exe process is not running')
    else:
        logger.debug('The und.exe process killed manually')

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
    """
    Creates a parse tree for a Java file using ANTLR4.

    Args:
        java_file_path (str): Path to the Java file to parse

    Returns:
        tuple: (parse_tree, token_stream_rewriter)
    """
    tree = None
    rewriter = None
    try:
        # Create a file stream to read the Java file
        file_stream = FileStream(java_file_path, encoding='utf-8', errors='ignore')

        # Create a lexer that feeds off of the file stream
        lexer = JavaLexer(file_stream)

        # Create a token stream from the lexer
        token_stream = CommonTokenStream(lexer)

        # Create a parser that feeds off of the token stream
        parser = JavaParserLabeled(token_stream)

        # Begin parsing at the compilationUnit rule
        tree = parser.compilationUnit()

        # Create a token stream rewriter for modifying the source code
        rewriter = TokenStreamRewriter(token_stream)

    except Exception as e:
        print(f'Encounter a parsing error on file {java_file_path}')
        print(e)

    return tree, rewriter


# def create_project_parse_tree(java_file_path):
#     tree = None
#     rewriter = None
#     try:
#         file_stream = FileStream(java_file_path, encoding='utf-8', errors='ignore')
#         # sa_javalabeled.USE_CPP_IMPLEMENTATION = config.USE_CPP_BACKEND
#         # sa_javalabeled.USE_CPP_IMPLEMENTATION = 0
#         tree = sa_javalabeled.parse(file_stream, 'compilationUnit')
#         tokens = tree.parser.getInputStream()
#         rewriter = TokenStreamRewriter(tokens)
#     except Exception as e:
#         print(f'Encounter a parsing error on file {java_file_path}')
#         print(e)
#     return tree, rewriter


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
    db: und.Db = und.open(str(os.path.join(config["Config"]["UDB_PATH"], config["Config"]["db_name"])))
    for i in range(0, 10):
        lnx = db.language()
        # print(lnx)
        update_understand_database(str(os.path.join(config["Config"]["UDB_PATH"], config["Config"]["db_name"])))


# if __name__ == '__main__':
#     # test_typyical_and_parallel_parsing()
#     test_understand_update()
