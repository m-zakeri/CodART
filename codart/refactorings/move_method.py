"""
Enhanced Move Method refactoring with comprehensive memory monitoring and improved method lookup
"""

import os
import os.path
import subprocess
import signal
import time
import psutil
import gc
from pathlib import Path
from functools import wraps
from contextlib import contextmanager
import threading
import traceback
from typing import Optional, List, Dict, Any

from antlr4.TokenStreamRewriter import TokenStreamRewriter

try:
    import understand as und
except ImportError as e:
    print(e)

from codart.gen.JavaParserLabeled import JavaParserLabeled
from codart.gen.JavaParserLabeledListener import JavaParserLabeledListener
from codart.refactorings.move_field import CheckCycleListener
from codart.symbol_table import parse_and_walk
from codart.learner.sbr_initializer.utils.utility import logger, config
from codart.utility.directory_utils import git_restore

STATIC = "Static Method"
DEFAULT_TIMEOUT = 60  # 60 seconds timeout for refactoring operations


def log_memory_usage(stage_name: str, detailed: bool = False):
    """
    Enhanced memory logging with more details
    """
    try:
        process = psutil.Process()
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

        if detailed:
            # Additional memory details
            try:
                memory_full_info = process.memory_full_info()
                logger.info(f"  Process USS: {memory_full_info.uss / 1024 / 1024:.1f} MB")
                logger.info(f"  Process PSS: {memory_full_info.pss / 1024 / 1024:.1f} MB")
            except:
                pass

        # Warning if memory usage is high
        if memory_percent > 80 or system_memory.percent > 90:
            logger.warning(f"[MEMORY WARNING] High memory usage detected!")
            logger.warning(f"  Process: {memory_percent:.1f}%, System: {system_memory.percent:.1f}%")
            return True  # Indicate high memory usage

        return False

    except Exception as e:
        logger.error(f"[MEMORY] Failed to get memory info for {stage_name}: {e}")
        return False


def force_cleanup():
    """
    Enhanced memory cleanup with more aggressive garbage collection
    """
    logger.debug("[CLEANUP] Starting enhanced memory cleanup...")

    # Multiple rounds of garbage collection
    for i in range(3):
        collected = gc.collect()
        logger.debug(f"[CLEANUP] Round {i+1}: Collected {collected} objects")

    # Force cleanup of specific object types
    try:
        import sys
        logger.debug(f"[CLEANUP] Reference count before cleanup: {sys.gettotalrefcount()}")
    except:
        pass

    # Get memory usage after cleanup
    try:
        process = psutil.Process()
        memory_after = process.memory_info()
        logger.debug(f"[CLEANUP] Memory after cleanup: {memory_after.rss / 1024 / 1024:.1f} MB RSS")
    except Exception as e:
        logger.debug(f"[CLEANUP] Could not get memory info after cleanup: {e}")


class TimeoutError(Exception):
    """Custom timeout exception"""
    pass


@contextmanager
def timeout_context(seconds):
    """Context manager for timeout operations"""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds} seconds")

    # Set the signal handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        # Restore the old signal handler
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


def with_timeout(timeout_seconds=DEFAULT_TIMEOUT):
    """Decorator to add timeout to functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)

            if thread.is_alive():
                logger.error(f"Function {func.__name__} timed out after {timeout_seconds} seconds")
                raise TimeoutError(f"Function {func.__name__} timed out after {timeout_seconds} seconds")

            if exception[0]:
                raise exception[0]

            return result[0]
        return wrapper
    return decorator


class DatabaseManager:
    """Context manager for safe database operations with memory monitoring"""

    def __init__(self, udb_path: str):
        self.udb_path = udb_path
        self.db = None

    def __enter__(self):
        log_memory_usage("Before database open")
        try:
            self.db = und.open(self.udb_path)
            log_memory_usage("After database open")
            return self.db
        except Exception as e:
            logger.error(f"Failed to open database {self.udb_path}: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db is not None:
            try:
                self.db.close()
                log_memory_usage("After database close")
            except Exception as e:
                logger.warning(f"Error closing database: {e}")
        force_cleanup()


class EnhancedMethodLookup:
    """Enhanced method lookup with multiple strategies and validation"""

    def __init__(self, db: und.Db):
        self.db = db

    def debug_method_lookup(self, class_name: str, method_name: str, package_name: str = "") -> bool:
        """
        Comprehensive method lookup with debugging information
        """
        logger.info(f"[METHOD_LOOKUP] Starting lookup for: {package_name}.{class_name}.{method_name}")
        log_memory_usage("Method lookup start")

        try:
            # Strategy 1: Direct method lookup
            full_method_name = f"{package_name}.{class_name}.{method_name}" if package_name else f"{class_name}.{method_name}"
            logger.debug(f"[METHOD_LOOKUP] Strategy 1: Direct lookup for {full_method_name}")

            method_entities = self.db.lookup(full_method_name, "Method")
            if method_entities:
                method_ent = method_entities[0]
                logger.info(f"[METHOD_LOOKUP] ✓ Direct lookup successful: {method_ent.longname()}")
                return method_ent

            # Strategy 2: Class-based lookup
            logger.debug(f"[METHOD_LOOKUP] Strategy 2: Class-based lookup")
            class_entities = self._find_class_entities(class_name, package_name)

            for class_ent in class_entities:
                logger.debug(f"[METHOD_LOOKUP] Searching in class: {class_ent.longname()}")

                # List all methods in class for debugging
                methods = list(class_ent.refs("Define", "Method"))
                logger.debug(f"[METHOD_LOOKUP] Available methods in {class_ent.simplename()}:")
                for method_ref in methods:
                    method = method_ref.ent()
                    logger.debug(f"  - {method.simplename()} (kind: {method.kindname()})")

                # Search for target method
                for method_ref in methods:
                    method = method_ref.ent()
                    if method.simplename() == method_name:
                        logger.info(f"[METHOD_LOOKUP] ✓ Class-based lookup successful: {method.longname()}")
                        return method

            # Strategy 3: Fuzzy search with different naming patterns
            logger.debug(f"[METHOD_LOOKUP] Strategy 3: Fuzzy search")
            fuzzy_matches = self._fuzzy_method_search(method_name, class_name, package_name)
            if fuzzy_matches:
                method_ent = fuzzy_matches[0]
                logger.info(f"[METHOD_LOOKUP] ✓ Fuzzy search successful: {method_ent.longname()}")
                return method_ent

            logger.error(f"[METHOD_LOOKUP] ✗ Method not found after all strategies: {full_method_name}")
            return None

        except Exception as e:
            logger.error(f"[METHOD_LOOKUP] Error during lookup: {e}")
            logger.error(f"[METHOD_LOOKUP] Traceback: {traceback.format_exc()}")
            return None
        finally:
            log_memory_usage("Method lookup end")
            force_cleanup()

    def _find_class_entities(self, class_name: str, package_name: str = "") -> List[Any]:
        """Find class entities with multiple strategies"""
        class_entities = []

        try:
            # Try with full package name
            if package_name:
                full_class_name = f"{package_name}.{class_name}"
                entities = self.db.lookup(full_class_name, "Class")
                class_entities.extend(entities)
                logger.debug(f"[CLASS_LOOKUP] Found {len(entities)} classes with full name: {full_class_name}")

            # Try without package name
            entities = self.db.lookup(class_name, "Class")
            class_entities.extend(entities)
            logger.debug(f"[CLASS_LOOKUP] Found {len(entities)} classes with simple name: {class_name}")

            # Filter to find the correct class (prefer the one in the right package)
            if package_name:
                filtered_entities = []
                for ent in class_entities:
                    ent_package = ".".join(ent.longname().split(".")[:-1])
                    if ent_package == package_name:
                        filtered_entities.append(ent)

                if filtered_entities:
                    logger.debug(f"[CLASS_LOOKUP] Filtered to {len(filtered_entities)} classes in correct package")
                    return filtered_entities

            # Remove duplicates
            unique_entities = []
            seen_ids = set()
            for ent in class_entities:
                if ent.id() not in seen_ids:
                    unique_entities.append(ent)
                    seen_ids.add(ent.id())

            return unique_entities

        except Exception as e:
            logger.error(f"[CLASS_LOOKUP] Error finding class entities: {e}")
            return []

    def _fuzzy_method_search(self, method_name: str, class_name: str, package_name: str = "") -> List[Any]:
        """Fuzzy search for methods with similar names or patterns"""
        matches = []

        try:
            # Search all methods in the database
            all_methods = self.db.ents("Method")

            for method in all_methods:
                # Check if method name matches (case insensitive)
                if method.simplename().lower() == method_name.lower():
                    # Check if it's in the right class
                    parent = method.parent()
                    if parent and parent.simplename() == class_name:
                        matches.append(method)
                        logger.debug(f"[FUZZY_SEARCH] Found fuzzy match: {method.longname()}")

            return matches

        except Exception as e:
            logger.error(f"[FUZZY_SEARCH] Error in fuzzy search: {e}")
            return []


# Keep all your existing listener classes but add memory monitoring
class CutMethodListener(JavaParserLabeledListener):
    def __init__(self, class_name: str, instance_name: str, method_name: str, is_static: bool, import_statement: str,
                 rewriter: TokenStreamRewriter):
        log_memory_usage("CutMethodListener init")
        self.class_name = class_name
        self.method_name = method_name
        self.is_static = is_static
        self.rewriter = rewriter
        self.import_statement = import_statement
        self.instance_name = instance_name
        self.is_member = False
        self.do_delete = False
        self.method_text = ""
        self.imports = ""

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        self.imports += self.rewriter.getText(
            program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
            start=ctx.start.tokenIndex,
            stop=ctx.stop.tokenIndex
        ) + "\n"

    def exitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if self.import_statement:
            self.rewriter.insertAfterToken(
                token=ctx.stop,
                text=self.import_statement,
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME
            )
            self.import_statement = None

    def enterMemberDeclaration0(self, ctx: JavaParserLabeled.MemberDeclaration0Context):
        self.is_member = True

    def exitMemberDeclaration0(self, ctx: JavaParserLabeled.MemberDeclaration0Context):
        self.is_member = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_member and ctx.IDENTIFIER().getText() == self.method_name:
            self.do_delete = True

    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.do_delete:
            self.method_text = self.rewriter.getText(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.start.tokenIndex,
                stop=ctx.stop.tokenIndex
            )
            if self.is_static:
                replace_text = f"public static {self.class_name} {self.instance_name} = new {self.class_name}();"
            else:
                replace_text = f"public {self.class_name} {self.instance_name} = new {self.class_name}();"
            self.rewriter.replace(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex,
                text=replace_text
            )
            self.do_delete = False

    def __del__(self):
        """Cleanup method to ensure memory is freed"""
        try:
            # Clear large text fields
            self.method_text = ""
            self.imports = ""
            self.rewriter = None
        except:
            pass


class PasteMethodListener(JavaParserLabeledListener):
    def __init__(self, method_text: str, method_map: dict, imports: str, source_class: str,
                 rewriter: TokenStreamRewriter):
        log_memory_usage("PasteMethodListener init")
        self.method_text = method_text
        self.method_map = method_map
        self.source_class = source_class
        self.imports = imports
        self.rewriter = rewriter
        self.fields = None
        self.has_package = False
        self.has_empty_cons = False

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.has_package = True

    def exitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if self.has_package and self.imports:
            self.rewriter.insertAfter(
                index=ctx.stop.tokenIndex,
                text="\n" + self.imports,
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME
            )

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        if not self.has_package and self.imports:
            self.rewriter.insertBefore(
                index=ctx.start.tokenIndex,
                text="\n" + self.imports,
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME
            )

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        self.rewriter.insertAfterToken(
            token=ctx.start,
            text="\n" + self.method_text + "\n",
            program_name=self.rewriter.DEFAULT_PROGRAM_NAME
        )

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        params = ctx.formalParameters().getText()
        if params == "()":
            self.has_empty_cons = True

    def __del__(self):
        """Cleanup method"""
        try:
            self.method_text = ""
            self.imports = ""
            self.rewriter = None
        except:
            pass


class ReferenceInjectorAndConstructorListener(PasteMethodListener):
    def __init__(self, *args, **kwargs):
        self.has_empty_cons = kwargs.pop("has_empty_cons", False)
        self.class_name = ""
        super(ReferenceInjectorAndConstructorListener, self).__init__(*args, **kwargs)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name = ctx.IDENTIFIER().getText()

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if not self.has_empty_cons:
            self.rewriter.insertAfterToken(
                token=ctx.start,
                text="\n" + f"public {self.class_name}()" + "{}\n",
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME
            )

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        identifier = ctx.IDENTIFIER()
        self.fields = self.method_map.get(identifier.getText())
        if self.fields:
            if ctx.formalParameters().getText() == "()":
                text = f"{self.source_class} ref"
            else:
                text = f", {self.source_class} ref"
            self.rewriter.insertBeforeToken(
                token=ctx.formalParameters().stop,
                text=text,
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME
            )

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.fields = None

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        if self.fields and ctx.expression().getText() == "this":
            for field in self.fields:
                if field in ctx.getText():
                    self.rewriter.replaceSingleToken(
                        token=ctx.expression().primary().start,
                        text="ref"
                    )

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        if self.fields:
            field_name = ctx.getText()
            if field_name in self.fields:
                self.fields.remove(field_name)
                self.rewriter.insertBeforeToken(
                    token=ctx.start,
                    text="ref."
                )


class PropagateListener(JavaParserLabeledListener):
    def __init__(self, method_name: str, new_name: str, lines: list, is_in_target_class: bool, method_map: dict,
                 rewriter: TokenStreamRewriter):
        log_memory_usage("PropagateListener init")
        self.method_name = method_name
        self.new_name = new_name
        self.lines = lines
        self.method_map = method_map
        self.fields = None
        self.rewriter = rewriter
        self.is_in_target_class = is_in_target_class

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        identifier = ctx.IDENTIFIER()
        self.fields = self.method_map.get(identifier.getText())
        if identifier and ctx.start.line in self.lines and identifier.getText() == self.method_name:
            if self.fields:
                parent = ctx.parentCtx
                caller = parent.children[0]
                caller = self.rewriter.getText(
                    program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                    start=caller.start.tokenIndex,
                    stop=caller.stop.tokenIndex
                )

                if ctx.expressionList():
                    self.rewriter.insertAfterToken(
                        token=ctx.expressionList().stop,
                        text=", " + caller,
                        program_name=self.rewriter.DEFAULT_PROGRAM_NAME
                    )
                else:
                    self.rewriter.insertAfter(
                        index=ctx.stop.tokenIndex - 1,
                        text=caller,
                        program_name=self.rewriter.DEFAULT_PROGRAM_NAME
                    )

            if self.is_in_target_class:
                self.rewriter.replaceSingleToken(
                    token=ctx.parentCtx.start,
                    text="this"
                )
            else:
                self.rewriter.replaceSingleToken(
                    token=ctx.start,
                    text=self.new_name
                )

    def exitMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        self.fields = None

    def __del__(self):
        """Cleanup method"""
        try:
            self.rewriter = None
        except:
            pass


def execute_git_restore_with_utility(project_dir):
    """Execute git restore using the standardized utility method with memory monitoring"""
    try:
        logger.debug(f"Attempting to restore project: {project_dir}")
        log_memory_usage("Before git restore")
        git_restore(project_dir=project_dir)
        log_memory_usage("After git restore")
        logger.info(f"Successfully restored: {project_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to restore project {project_dir}: {str(e)}")
        return False
    finally:
        force_cleanup()


def kill_understand_processes():
    """Kill any running understand processes to release file locks"""
    try:
        subprocess.run(["pkill", "-f", "und"], capture_output=True, timeout=10)
        logger.debug("The und process was killed successfully using pkill")
    except Exception as e:
        logger.warning(f"Failed to kill understand processes: {str(e)}")


def get_source_class_map(db, source_class: str):
    """Get source class mapping with memory monitoring"""
    log_memory_usage("Source class map start")

    try:
        method_usage_map = {}
        class_ents = db.lookup(source_class, "Class")
        class_ent = None

        for ent in class_ents:
            if ent.parent() is not None:
                if Path(ent.parent().longname()).name == f"{source_class}.java":
                    class_ent = ent
                    break

        if class_ent is None:
            return None, None

        for ref in class_ent.refs("Define", "Method"):
            method_ent = ref.ent()
            method_usage_map[method_ent.simplename()] = set()
            for use in method_ent.refs("SetBy UseBy ModifyBy, Call", "Variable ~Unknown, Method ~Unknown"):
                method_usage_map[method_ent.simplename()].add(use.ent().simplename())

        return method_usage_map, class_ent

    except Exception as e:
        logger.error(f"Error getting source class map: {e}")
        return None, None
    finally:
        log_memory_usage("Source class map end")
        force_cleanup()


@with_timeout(30)  # 30 second timeout for parse_and_walk operations
def safe_parse_and_walk(file_path, listener_class, **kwargs):
    """Wrapper for parse_and_walk with timeout protection and memory monitoring"""
    logger.debug(f"Starting parse_and_walk for {file_path} with {listener_class.__name__}")
    log_memory_usage(f"Before parse_and_walk - {listener_class.__name__}")
    start_time = time.time()

    try:
        result = parse_and_walk(
            file_path=file_path,
            listener_class=listener_class,
            **kwargs
        )
        elapsed = time.time() - start_time
        logger.debug(f"Completed parse_and_walk for {file_path} in {elapsed:.2f} seconds")
        log_memory_usage(f"After parse_and_walk - {listener_class.__name__}")
        return result
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"parse_and_walk failed for {file_path} after {elapsed:.2f} seconds: {str(e)}")
        raise
    finally:
        force_cleanup()


def cleanup_and_restore(db, project_dir):
    """Centralized cleanup and restore function with enhanced memory cleanup"""
    logger.info("[CLEANUP] Starting cleanup and restore process")
    log_memory_usage("Before cleanup")

    # Close database if open
    if db is not None:
        try:
            db.close()
            logger.debug("[CLEANUP] Database closed")
        except:
            pass

    # Kill understand processes
    kill_understand_processes()

    # Force memory cleanup
    force_cleanup()

    # Execute git restore
    if project_dir:
        execute_git_restore_with_utility(project_dir)
    else:
        logger.warning("No project_dir provided, skipping git restore")

    log_memory_usage("After cleanup")
    logger.info("[CLEANUP] Cleanup and restore completed")


def validate_inputs(source_class, source_package, target_class, target_package, method_name, udb_path, project_dir):
    """Validate all input parameters"""
    logger.debug("[VALIDATION] Starting input validation")

    # Check required parameters
    if not all([source_class, source_package, target_class, target_package, method_name]):
        logger.error("[VALIDATION] Missing required parameters")
        return False, "Missing required parameters"

    # Check if source and target are the same
    if source_package == target_package and source_class == target_class:
        logger.error("[VALIDATION] Cannot move method to the same class")
        return False, "Cannot move method to the same class"

    # Check if UDB file exists
    if not os.path.exists(udb_path):
        logger.error(f"[VALIDATION] UDB file does not exist: {udb_path}")
        return False, f"UDB file does not exist: {udb_path}"

    # Check if project directory exists
    if project_dir and not os.path.exists(project_dir):
        logger.error(f"[VALIDATION] Project directory does not exist: {project_dir}")
        return False, f"Project directory does not exist: {project_dir}"

    logger.debug("[VALIDATION] Input validation passed")
    return True, "Validation successful"


def main(source_class, source_package, target_class, target_package, method_name, udb_path, project_dir=None, *args, **kwargs):
    """
    Enhanced move method with comprehensive memory monitoring and improved error handling
    Returns True on success, False on failure (never None)
    """
    result = False
    db = None
    overall_start_time = time.time()

    try:
        logger.info(f"[MOVE_METHOD] Starting move method refactoring with comprehensive monitoring")
        logger.info(f"[MOVE_METHOD] Moving {method_name} from {source_package}.{source_class} to {target_package}.{target_class}")
        log_memory_usage("Move method start", detailed=True)

        # 1. Validate input parameters
        is_valid, validation_message = validate_inputs(
            source_class, source_package, target_class, target_package,
            method_name, udb_path, project_dir
        )

        if not is_valid:
            logger.error(f"[MOVE_METHOD] Validation failed: {validation_message}")
            return False

        # 2. Open database with monitoring
        try:
            with DatabaseManager(udb_path) as database:
                db = database

                # 3. Enhanced method lookup with debugging
                method_lookup = EnhancedMethodLookup(db)
                method_ent = method_lookup.debug_method_lookup(source_class, method_name, source_package)

                if not method_ent:
                    logger.error(f"[MOVE_METHOD] Method not found: {source_package}.{source_class}.{method_name}")
                    cleanup_and_restore(None, project_dir)
                    return False

                # 4. Validate the found method
                if method_ent.simplename() != method_name:
                    logger.error(f"[MOVE_METHOD] Method name mismatch. Found: {method_ent.simplename()}, Expected: {method_name}")
                    cleanup_and_restore(None, project_dir)
                    return False

                if method_name == source_class:
                    logger.error("[MOVE_METHOD] Cannot move constructor method")
                    cleanup_and_restore(None, project_dir)
                    return False

                # 5. Get class files with validation
                try:
                    log_memory_usage("Before file lookup")

                    src_class_files = db.lookup(f"{source_package}.{source_class}.java", "File")
                    if not src_class_files:
                        src_class_files = db.lookup(f"{source_class}.java", "File")
                        if not src_class_files:
                            logger.error(f"[MOVE_METHOD] Source class file not found")
                            cleanup_and_restore(None, project_dir)
                            return False
                    src_class_file = src_class_files[0].longname()

                    target_class_files = db.lookup(f"{target_package}.{target_class}.java", "File")
                    if not target_class_files:
                        target_class_files = db.lookup(f"{target_class}.java", "File")
                        if not target_class_files:
                            logger.error(f"[MOVE_METHOD] Target class file not found")
                            cleanup_and_restore(None, project_dir)
                            return False
                    target_class_file = target_class_files[0].longname()

                    # Validate file paths exist
                    if not os.path.exists(src_class_file):
                        logger.error(f"[MOVE_METHOD] Source file does not exist: {src_class_file}")
                        cleanup_and_restore(None, project_dir)
                        return False

                    if not os.path.exists(target_class_file):
                        logger.error(f"[MOVE_METHOD] Target file does not exist: {target_class_file}")
                        cleanup_and_restore(None, project_dir)
                        return False

                    log_memory_usage("After file lookup")

                except (IndexError, AttributeError) as e:
                    logger.error(f"[MOVE_METHOD] Error accessing class files: {str(e)}")
                    cleanup_and_restore(None, project_dir)
                    return False

                # 6. Get source class mapping with memory monitoring
                log_memory_usage("Before source class mapping")
                method_map, class_ent = get_source_class_map(db, source_class)
                if class_ent is None:
                    logger.warning(f"[MOVE_METHOD] Could not find class entity for {source_class}, using empty method map")
                    method_map = {}
                log_memory_usage("After source class mapping")

                # 7. Check if method is static
                is_static = "Static" in method_ent.kindname()
                logger.debug(f"[MOVE_METHOD] Method {method_name} is static: {is_static}")

                # 8. Find method usages with timeout and memory monitoring
                usages = {}
                try:
                    log_memory_usage("Before usage analysis")
                    with timeout_context(15):  # 15 second timeout for usage analysis
                        usage_count = 0
                        for ref in method_ent.refs("Callby"):
                            file = ref.file().longname()
                            if file in usages:
                                usages[file].append(ref.line())
                            else:
                                usages[file] = [ref.line()]
                            usage_count += 1

                            # Check memory every 100 usages
                            if usage_count % 100 == 0:
                                high_memory = log_memory_usage(f"Usage analysis - {usage_count} usages")
                                if high_memory:
                                    logger.warning("[MOVE_METHOD] High memory usage during usage analysis")
                                    force_cleanup()

                    log_memory_usage("After usage analysis")
                except TimeoutError:
                    logger.error("[MOVE_METHOD] Usage analysis timed out")
                    cleanup_and_restore(None, project_dir)
                    return False

                logger.debug(f"[MOVE_METHOD] Found {len(usages)} files with method calls")

                # 9. Determine import statement
                import_statement = None
                if source_package != target_package:
                    import_statement = f"\nimport {target_package}.{target_class};"

                instance_name = target_class.lower() + "ByCodArt"

                # Close database before file operations to free memory
                db.close()
                db = None
                force_cleanup()

                # 10. Perform the refactoring operations with timeouts and memory monitoring
                logger.info("[MOVE_METHOD] Starting refactoring operations...")
                log_memory_usage("Before refactoring operations")

                # Propagate changes to all usage sites with individual timeouts
                for i, file in enumerate(usages.keys()):
                    try:
                        logger.debug(f"[MOVE_METHOD] Processing usage file {i+1}/{len(usages)}: {file}")
                        log_memory_usage(f"Before propagation {i+1}")

                        public_class_name = os.path.basename(file).split(".")[0]
                        is_in_target_class = public_class_name == target_class

                        listener = safe_parse_and_walk(
                            file_path=file,
                            listener_class=PropagateListener,
                            has_write=True,
                            method_name=method_name,
                            new_name=f"{instance_name}.{method_name}",
                            lines=usages[file],
                            is_in_target_class=is_in_target_class,
                            method_map=method_map,
                        )

                        # Explicitly delete listener to free memory
                        del listener
                        force_cleanup()

                        log_memory_usage(f"After propagation {i+1}")
                        logger.debug(f"[MOVE_METHOD] ✓ Updated usage in {file}")

                    except (TimeoutError, Exception) as e:
                        logger.error(f"[MOVE_METHOD] Error updating usage in {file}: {str(e)}")
                        logger.error(f"[MOVE_METHOD] Traceback: {traceback.format_exc()}")
                        cleanup_and_restore(None, project_dir)
                        return False

                # Cut the method from source class with timeout and memory monitoring
                try:
                    logger.debug("[MOVE_METHOD] Cutting method from source class...")
                    log_memory_usage("Before method cutting")

                    listener = safe_parse_and_walk(
                        file_path=src_class_file,
                        listener_class=CutMethodListener,
                        has_write=True,
                        class_name=target_class,
                        instance_name=instance_name,
                        method_name=method_name,
                        is_static=is_static,
                        import_statement=import_statement,
                    )
                    method_text = listener.method_text
                    imports = getattr(listener, 'imports', '')

                    if not method_text.strip():
                        logger.error("[MOVE_METHOD] Failed to extract method text")
                        cleanup_and_restore(None, project_dir)
                        return False

                    # Explicitly delete listener to free memory
                    del listener
                    force_cleanup()
                    log_memory_usage("After method cutting")
                    logger.debug("[MOVE_METHOD] ✓ Successfully cut method from source class")

                except (TimeoutError, Exception) as e:
                    logger.error(f"[MOVE_METHOD] Error cutting method from source class: {str(e)}")
                    logger.error(f"[MOVE_METHOD] Traceback: {traceback.format_exc()}")
                    cleanup_and_restore(None, project_dir)
                    return False

                # Paste the method to target class with timeout and memory monitoring
                try:
                    logger.debug("[MOVE_METHOD] Pasting method to target class...")
                    log_memory_usage("Before method pasting")

                    listener = safe_parse_and_walk(
                        file_path=target_class_file,
                        listener_class=PasteMethodListener,
                        has_write=True,
                        method_text=method_text,
                        source_class=source_class,
                        method_map=method_map,
                        imports=imports,
                    )
                    has_empty_cons = getattr(listener, 'has_empty_cons', False)

                    # Explicitly delete listener to free memory
                    del listener
                    force_cleanup()
                    log_memory_usage("After method pasting")
                    logger.debug("[MOVE_METHOD] ✓ Successfully pasted method to target class")

                except (TimeoutError, Exception) as e:
                    logger.error(f"[MOVE_METHOD] Error pasting method to target class: {str(e)}")
                    logger.error(f"[MOVE_METHOD] Traceback: {traceback.format_exc()}")
                    cleanup_and_restore(None, project_dir)
                    return False

                # Post-paste: Reference injection and constructor handling
                try:
                    logger.debug("[MOVE_METHOD] Injecting references and handling constructors...")
                    log_memory_usage("Before reference injection")

                    listener = safe_parse_and_walk(
                        file_path=target_class_file,
                        listener_class=ReferenceInjectorAndConstructorListener,
                        has_write=True,
                        method_text=method_text,
                        source_class=source_class,
                        method_map=method_map,
                        imports=None,
                        has_empty_cons=has_empty_cons,
                    )

                    # Explicitly delete listener to free memory
                    del listener
                    force_cleanup()
                    log_memory_usage("After reference injection")
                    logger.debug("[MOVE_METHOD] ✓ Successfully injected references and handled constructors")

                except (TimeoutError, Exception) as e:
                    logger.warning(f"[MOVE_METHOD] Error in reference injection: {str(e)} - refactoring may still be successful")
                    # Don't fail here as the basic move might have worked

                elapsed = time.time() - overall_start_time
                result = True
                logger.info(f"[MOVE_METHOD] ✓ Move method refactoring completed successfully in {elapsed:.2f} seconds")
                log_memory_usage("Move method completion", detailed=True)

        except TimeoutError as e:
            logger.error(f"[MOVE_METHOD] Move method refactoring timed out: {str(e)}")
            cleanup_and_restore(db, project_dir)
            result = False

        except Exception as e:
            logger.error(f"[MOVE_METHOD] Move method refactoring failed with exception: {str(e)}")
            logger.error(f"[MOVE_METHOD] Traceback: {traceback.format_exc()}")
            cleanup_and_restore(db, project_dir)
            result = False

    except Exception as e:
        logger.error(f"[MOVE_METHOD] Outer exception in move method: {str(e)}")
        logger.error(f"[MOVE_METHOD] Traceback: {traceback.format_exc()}")
        cleanup_and_restore(db, project_dir)
        result = False

    finally:
        # Ensure database is closed and cleanup is performed
        if db is not None:
            try:
                db.close()
            except:
                pass

        # Final cleanup
        force_cleanup()

    final_result = bool(result)
    elapsed = time.time() - overall_start_time
    logger.info(f"[MOVE_METHOD] Returning {final_result} after {elapsed:.2f} seconds")
    log_memory_usage("Final move method memory state", detailed=True)

    return final_result


# Additional utility functions for debugging method lookup issues

def diagnose_method_lookup_issues(udb_path: str, source_class: str, method_name: str, source_package: str = ""):
    """
    Diagnostic function to help identify method lookup issues
    """
    logger.info(f"[DIAGNOSIS] Starting method lookup diagnosis for {source_package}.{source_class}.{method_name}")

    try:
        with DatabaseManager(udb_path) as db:
            # 1. Check if database is working
            logger.info(f"[DIAGNOSIS] Database opened successfully: {udb_path}")

            # 2. List all entities to see what's available
            all_classes = list(db.ents("Class"))
            logger.info(f"[DIAGNOSIS] Total classes in database: {len(all_classes)}")

            # 3. Find classes matching the source class name
            matching_classes = [c for c in all_classes if source_class in c.simplename()]
            logger.info(f"[DIAGNOSIS] Classes matching '{source_class}': {len(matching_classes)}")

            for cls in matching_classes[:5]:  # Show first 5 matches
                logger.info(f"[DIAGNOSIS]   - {cls.longname()} (kind: {cls.kindname()})")

            # 4. Look for methods with matching names
            all_methods = list(db.ents("Method"))
            matching_methods = [m for m in all_methods if method_name in m.simplename()]
            logger.info(f"[DIAGNOSIS] Methods matching '{method_name}': {len(matching_methods)}")

            for method in matching_methods[:10]:  # Show first 10 matches
                parent = method.parent()
                parent_name = parent.simplename() if parent else "No parent"
                logger.info(f"[DIAGNOSIS]   - {method.longname()} in class {parent_name}")

            # 5. Check files
            java_files = list(db.ents("File"))
            java_files = [f for f in java_files if f.longname().endswith('.java')]
            logger.info(f"[DIAGNOSIS] Java files in database: {len(java_files)}")

            matching_files = [f for f in java_files if source_class in f.longname()]
            logger.info(f"[DIAGNOSIS] Files matching '{source_class}': {len(matching_files)}")

            for file in matching_files[:5]:
                logger.info(f"[DIAGNOSIS]   - {file.longname()}")

    except Exception as e:
        logger.error(f"[DIAGNOSIS] Error during diagnosis: {e}")
        logger.error(f"[DIAGNOSIS] Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    # Example usage for testing
    pass