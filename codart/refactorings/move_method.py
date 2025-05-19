"""
## Introduction

The module implements Move Method refactoring operation

## Pre and post-conditions

### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions

"""

__version__ = '0.1.0'
__author__ = 'Morteza Zakeri'

import os
import os.path
from pathlib import Path
# import logging

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

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__file__)

STATIC = "Static Method"


class CutMethodListener(JavaParserLabeledListener):
    """


    """

    def __init__(self, class_name: str, instance_name: str, method_name: str, is_static: bool, import_statement: str,
                 rewriter: TokenStreamRewriter):
        """


        """

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


def get_source_class_map(db, source_class: str):
    method_usage_map = {}
    class_ents = db.lookup(source_class, "Class")
    class_ent = None
    for ent in class_ents:
        if ent.parent() is not None:
            # print(source_class)
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


def main(source_class: str, source_package: str, target_class: str, target_package: str, method_name: str,
         udb_path: str, *args, **kwargs):
    """


    """

    import_statement = None
    if source_package != target_package:
        import_statement = f"\nimport {target_package}.{target_class};"
    instance_name = target_class.lower() + "ByCodArt"
    db = und.open(udb_path)
    method_map, class_ent = get_source_class_map(db, source_class)
    if class_ent is None:
        logger.error("Class entity is None")
        return False

    # Strong overlay precondition
    # if class_ent.refs("Extend ~Implicit, ExtendBy, Implement"):
    #     logger.error("Class is in inheritance or implements an interface.")
    #     db.close()
    #     return False

    # Check if method is static
    method_ent = db.lookup(f"{source_package}.{source_class}.{method_name}", "Method")
    if len(method_ent) >= 1:
        method_ent = method_ent[0]
    else:
        logger.error("Entity not found.")
        db.close()
        return False

    if method_ent.simplename() != method_name:
        logger.error("Can not move method duo to duplicated entities.")
        logger.info(f"{method_ent}, {method_ent.kindname()}")
        db.close()
        return False

    if source_package == target_package and source_class == target_class:
        logger.error("Can not move to self.")
        db.close()
        return False

    is_static = STATIC in method_ent.kindname()
    # Find usages
    usages = {}

    for ref in method_ent.refs("Callby"):
        file = ref.file().longname()
        if file in usages:
            usages[file].append(ref.line())
        else:
            usages[file] = [ref.line(), ]

    try:
        src_class_file = db.lookup(f"{source_package}.{source_class}.java", "File")[0].longname()
        target_class_file = db.lookup(f"{target_package}.{target_class}.java", "File")[0].longname()
    except IndexError:
        logger.error("This is a nested method.")
        logger.info(f"{source_package}.{source_class}.java")
        logger.info(f"{target_package}.{target_class}.java")
        db.close()
        return False

    db.close()

    # Check if there is an cycle
    listener = parse_and_walk(
        file_path=target_class_file,
        listener_class=CheckCycleListener,
        class_name=source_class
    )

    if not listener.is_valid:
        logger.error(f"Can not move method because there is a cycle between {source_class}, {target_class}")
        # db.close()
        return False

    # Propagate Changes
    for file in usages.keys():
        public_class_name = os.path.basename(file).split(".")[0]
        is_in_target_class = public_class_name == target_class
        parse_and_walk(
            file_path=file,
            listener_class=PropagateListener,
            has_write=True,
            method_name=method_name,
            new_name=f"{instance_name}.{method_name}",
            lines=usages[file],
            is_in_target_class=is_in_target_class,
            method_map=method_map,
        )
    # exit(-1)
    # Do the cut and paste!
    # Cut
    listener = parse_and_walk(
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

    # Paste
    listener = parse_and_walk(
        file_path=target_class_file,
        listener_class=PasteMethodListener,
        has_write=True,
        method_text=method_text,
        source_class=source_class,
        method_map=method_map,
        imports=listener.imports,
    )

    # Post-Paste: Reference Injection
    parse_and_walk(
        file_path=target_class_file,
        listener_class=ReferenceInjectorAndConstructorListener,
        has_write=True,
        method_text=method_text,
        source_class=source_class,
        method_map=method_map,
        imports=None,
        has_empty_cons=listener.has_empty_cons,
    )
    # db.close()
    return True


# # Tests
# if __name__ == '__main__':
#     from codart.utility.directory_utils import update_understand_database
#
#     update_understand_database("C:/Users/Administrator/Downloads/udbs/jvlt-1.3.2.udb")
#     main(
#         source_class="XMLFormatter",
#         source_package="net.sourceforge.jvlt.io",
#         target_class="Entry",
#         target_package="net.sourceforge.jvlt.core",
#         method_name="getXMLForEntryInfo",
#         udb_path="C:/Users/Administrator/Downloads/udbs/jvlt-1.3.2.udb"
#     )
