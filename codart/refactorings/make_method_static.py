"""
## Introduction

The module implements make method static refactoring operation

## Pre and post-conditions

### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions


"""

__version__ = '0.1.0'
__author__ = 'Morteza Zakeri'

import os

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.javaLabeled.JavaLexer import JavaLexer
from codart.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from codart.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MakeMethodStaticRefactoringListener(JavaParserLabeledListener):
    """

    To implement make method static refactoring based on its actors.

    """

    def __init__(
            self, common_token_stream: CommonTokenStream = None,
            target_class: str = None, target_methods: list = None):
        """


        """

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if target_class is None:
            raise ValueError("source_class is None")
        else:
            self.target_class = target_class
        if target_methods is None or len(target_methods) == 0:
            raise ValueError("target method must have one method name")
        else:
            self.target_methods = target_methods

        self.is_target_class = False
        self.detected_instance_of_target_class = []
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.target_class:
            self.is_target_class = True
        else:
            self.is_target_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_target_class:
            self.is_target_class = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_target_class:
            if ctx.IDENTIFIER().getText() in self.target_methods:
                if 'this.' in ctx.getText():
                    raise ValueError("this method can not refactor")
                grand_parent_ctx = ctx.parentCtx.parentCtx
                if grand_parent_ctx.modifier():
                    if len(grand_parent_ctx.modifier()) == 2:
                        return None
                    else:
                        self.token_stream_rewriter.insertAfter(
                            index=grand_parent_ctx.modifier(0).stop.tokenIndex,
                            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                            text=" static"
                        )
                else:
                    self.token_stream_rewriter.insertBeforeIndex(
                        index=ctx.start.tokenIndex,
                        text="static "
                    )

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        if ctx.typeType().getText() == self.target_class:
            self.detected_instance_of_target_class.append(
                ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText())
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex + 1
            )

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        if ctx.IDENTIFIER().getText() in self.target_methods:
            if ctx.parentCtx.expression().getText() in self.detected_instance_of_target_class:
                self.token_stream_rewriter.replace(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=ctx.parentCtx.expression().start.tokenIndex,
                    to_idx=ctx.parentCtx.expression().stop.tokenIndex,
                    text=self.target_class
                )


def main(udb_path, target_class, target_methods):
    """


    """

    main_file = None
    db = und.open(udb_path)
    classes = db.ents("Class")
    for cls in classes:
        if cls.simplename() == target_class:
            if cls.parent() is not None:
                temp_file = str(cls.parent().longname(True))
                if os.path.isfile(temp_file):
                    main_file = temp_file
                    break

    if main_file is None:
        db.close()
        return False

    db.close()
    stream = FileStream(main_file, encoding='utf8', errors='ignore')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = MakeMethodStaticRefactoringListener(common_token_stream=token_stream, target_class=target_class,
                                                      target_methods=target_methods)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', encoding='utf8', errors='ignore', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())

    return True


# Tests
if __name__ == '__main__':
    udb_path_ = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    target_class_ = "Website"
    target_methods_ = "HELLO_FROM_STUDENT_WEBSITE"
    # initialize with understand
    main(udb_path_, target_class_, target_methods_)
