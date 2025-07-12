"""
Enhanced Move Method refactoring with timeout handling and better error recovery
"""

import os
import os.path
import subprocess
import signal
import time
from pathlib import Path
from functools import wraps
from contextlib import contextmanager
import threading

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


class CutMethodListener(JavaParserLabeledListener):
    def __init__(self, class_name: str, instance_name: str, method_name: str, is_static: bool, import_statement: str,
                 rewriter: TokenStreamRewriter):
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


class PasteMethodListener(JavaParserLabeledListener):
    def __init__(self, method_text: str, method_map: dict, imports: str, source_class: str,
                 rewriter: TokenStreamRewriter):
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


def execute_git_restore_with_utility(project_dir):
    """Execute git restore using the standardized utility method"""
    try:
        logger.debug(f"Attempting to restore project: {project_dir}")
        git_restore(project_dir=project_dir)
        logger.info(f"Successfully restored: {project_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to restore project {project_dir}: {str(e)}")
        return False


def kill_understand_processes():
    """Kill any running understand processes to release file locks"""
    try:
        subprocess.run(["pkill", "-f", "und"], capture_output=True, timeout=10)
        logger.debug("The und process was killed successfully using pkill")
    except Exception as e:
        logger.warning(f"Failed to kill understand processes: {str(e)}")


def get_source_class_map(db, source_class: str):
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


@with_timeout(30)  # 30 second timeout for parse_and_walk operations
def safe_parse_and_walk(file_path, listener_class, **kwargs):
    """Wrapper for parse_and_walk with timeout protection"""
    logger.debug(f"Starting parse_and_walk for {file_path} with {listener_class.__name__}")
    start_time = time.time()

    try:
        result = parse_and_walk(
            file_path=file_path,
            listener_class=listener_class,
            **kwargs
        )
        elapsed = time.time() - start_time
        logger.debug(f"Completed parse_and_walk for {file_path} in {elapsed:.2f} seconds")
        return result
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"parse_and_walk failed for {file_path} after {elapsed:.2f} seconds: {str(e)}")
        raise


def cleanup_and_restore(db, project_dir):
    """Centralized cleanup and restore function"""
    # Close database if open
    if db is not None:
        try:
            db.close()
        except:
            pass

    # Kill understand processes
    kill_understand_processes()

    # Execute git restore
    if project_dir:
        execute_git_restore_with_utility(project_dir)
    else:
        logger.warning("No project_dir provided, skipping git restore")


def main(source_class, source_package, target_class, target_package, method_name, udb_path, project_dir=None, *args, **kwargs):
    """
    Enhanced move method with timeout handling and comprehensive error recovery
    Returns True on success, False on failure (never None)
    """
    result = False
    db = None
    overall_start_time = time.time()

    try:
        logger.debug(f"Starting move method refactoring with timeout protection")
        logger.debug(f"Attempting to move method {method_name} from {source_package}.{source_class} to {target_package}.{target_class}")

        # Open database with timeout
        try:
            with timeout_context(10):  # 10 second timeout for database operations
                db = und.open(udb_path)
        except TimeoutError:
            logger.error("Database opening timed out")
            return False

        # 1. Validate input parameters
        if not all([source_class, source_package, target_class, target_package, method_name]):
            logger.error("Missing required parameters")
            cleanup_and_restore(db, project_dir)
            return False

        # 2. Check if source and target are the same
        if source_package == target_package and source_class == target_class:
            logger.error("Cannot move method to the same class")
            cleanup_and_restore(db, project_dir)
            return False

        # 3. Method existence check with timeout
        try:
            with timeout_context(15):  # 15 second timeout for method lookup
                full_method_name = f"{source_package}.{source_class}.{method_name}"
                method_entities = db.lookup(full_method_name, "Method")

                # Alternative lookup strategies if direct lookup fails
                if len(method_entities) == 0:
                    logger.warning(f"Direct method lookup failed for: {full_method_name}")

                    # Strategy 1: Look up class first, then find method
                    class_entities = db.lookup(f"{source_package}.{source_class}", "Class")
                    method_ent = None

                    for class_ent in class_entities:
                        for ref in class_ent.refs("Define", "Method"):
                            candidate_method = ref.ent()
                            if candidate_method.simplename() == method_name:
                                method_ent = candidate_method
                                break
                        if method_ent:
                            break

                    # Strategy 2: Try without package
                    if not method_ent:
                        class_entities = db.lookup(source_class, "Class")
                        for class_ent in class_entities:
                            if class_ent.parent() and Path(class_ent.parent().longname()).name == f"{source_class}.java":
                                for ref in class_ent.refs("Define", "Method"):
                                    candidate_method = ref.ent()
                                    if candidate_method.simplename() == method_name:
                                        method_ent = candidate_method
                                        break
                                if method_ent:
                                    break

                    if method_ent:
                        method_entities = [method_ent]
                    else:
                        logger.error(f"Method not found after all lookup strategies: {full_method_name}")
                        cleanup_and_restore(db, project_dir)
                        return False

        except TimeoutError:
            logger.error("Method lookup timed out")
            cleanup_and_restore(db, project_dir)
            return False

        # 4. Validate the found method
        method_ent = method_entities[0]

        if method_ent.simplename() != method_name:
            logger.error(f"Method name mismatch. Found: {method_ent.simplename()}, Expected: {method_name}")
            cleanup_and_restore(db, project_dir)
            return False

        if method_name == source_class:
            logger.error("Cannot move constructor method")
            cleanup_and_restore(db, project_dir)
            return False

        # 5. Get class files with timeout
        try:
            with timeout_context(10):
                src_class_files = db.lookup(f"{source_package}.{source_class}.java", "File")
                if not src_class_files:
                    src_class_files = db.lookup(f"{source_class}.java", "File")
                    if not src_class_files:
                        logger.error(f"Source class file not found")
                        cleanup_and_restore(db, project_dir)
                        return False
                src_class_file = src_class_files[0].longname()

                target_class_files = db.lookup(f"{target_package}.{target_class}.java", "File")
                if not target_class_files:
                    target_class_files = db.lookup(f"{target_class}.java", "File")
                    if not target_class_files:
                        logger.error(f"Target class file not found")
                        cleanup_and_restore(db, project_dir)
                        return False
                target_class_file = target_class_files[0].longname()

        except (TimeoutError, IndexError, AttributeError) as e:
            logger.error(f"Error accessing class files: {str(e)}")
            cleanup_and_restore(db, project_dir)
            return False

        # 6. Get source class mapping
        method_map, class_ent = get_source_class_map(db, source_class)
        if class_ent is None:
            logger.warning(f"Could not find class entity for {source_class}, using empty method map")
            method_map = {}

        # 7. Check if method is static
        is_static = "Static" in method_ent.kindname()
        logger.debug(f"Method {method_name} is static: {is_static}")

        # 8. Find method usages with timeout
        usages = {}
        try:
            with timeout_context(10):
                for ref in method_ent.refs("Callby"):
                    file = ref.file().longname()
                    if file in usages:
                        usages[file].append(ref.line())
                    else:
                        usages[file] = [ref.line()]
        except (TimeoutError, Exception) as e:
            logger.warning(f"Error finding method usages: {str(e)}")
            usages = {}

        logger.debug(f"Found {len(usages)} files with method calls")

        # 9. Determine import statement
        import_statement = None
        if source_package != target_package:
            import_statement = f"\nimport {target_package}.{target_class};"

        instance_name = target_class.lower() + "ByCodArt"

        # Close database before file operations
        db.close()
        db = None

        # 10. Perform the refactoring operations with timeouts
        logger.debug("Starting refactoring operations...")

        # Propagate changes to all usage sites with individual timeouts
        for file in usages.keys():
            try:
                public_class_name = os.path.basename(file).split(".")[0]
                is_in_target_class = public_class_name == target_class

                safe_parse_and_walk(
                    file_path=file,
                    listener_class=PropagateListener,
                    has_write=True,
                    method_name=method_name,
                    new_name=f"{instance_name}.{method_name}",
                    lines=usages[file],
                    is_in_target_class=is_in_target_class,
                    method_map=method_map,
                )
                logger.debug(f"Updated usage in {file}")
            except (TimeoutError, Exception) as e:
                logger.error(f"Error updating usage in {file}: {str(e)}")
                # For propagation errors, restore and fail
                cleanup_and_restore(None, project_dir)
                return False

        # Cut the method from source class with timeout
        try:
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

            if not method_text.strip():
                logger.error("Failed to extract method text")
                cleanup_and_restore(None, project_dir)
                return False

            logger.debug("Successfully cut method from source class")
        except (TimeoutError, Exception) as e:
            logger.error(f"Error cutting method from source class: {str(e)}")
            cleanup_and_restore(None, project_dir)
            return False

        # Paste the method to target class with timeout
        try:
            listener = safe_parse_and_walk(
                file_path=target_class_file,
                listener_class=PasteMethodListener,
                has_write=True,
                method_text=method_text,
                source_class=source_class,
                method_map=method_map,
                imports=getattr(listener, 'imports', ''),
            )
            logger.debug("Successfully pasted method to target class")
        except (TimeoutError, Exception) as e:
            logger.error(f"Error pasting method to target class: {str(e)}")
            cleanup_and_restore(None, project_dir)
            return False

        # Post-paste: Reference injection and constructor handling with timeout
        try:
            safe_parse_and_walk(
                file_path=target_class_file,
                listener_class=ReferenceInjectorAndConstructorListener,
                has_write=True,
                method_text=method_text,
                source_class=source_class,
                method_map=method_map,
                imports=None,
                has_empty_cons=getattr(listener, 'has_empty_cons', False),
            )
            logger.debug("Successfully injected references and handled constructors")
        except (TimeoutError, Exception) as e:
            logger.warning(f"Error in reference injection: {str(e)} - refactoring may still be successful")
            # Don't fail here as the basic move might have worked

        elapsed = time.time() - overall_start_time
        result = True
        logger.debug(f"Move method refactoring completed successfully in {elapsed:.2f} seconds")

    except TimeoutError as e:
        logger.error(f"Move method refactoring timed out: {str(e)}")
        cleanup_and_restore(db, project_dir)
        result = False

    except Exception as e:
        logger.error(f"Move method refactoring failed with exception: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        cleanup_and_restore(db, project_dir)
        result = False

    finally:
        # Ensure database is closed
        if db is not None:
            try:
                db.close()
            except:
                pass

    final_result = bool(result)
    elapsed = time.time() - overall_start_time
    logger.debug(f"Move Method returning {final_result} after {elapsed:.2f} seconds")
    return final_result