"""
## Introduction

The module implements a light-weight version of make method static refactoring operation
described in `make_method_static`.

## Pre and post-conditions

### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions

"""

__version__ = "0.2.0"
__author__ = "Morteza Zakeri"

import os

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from sbse import config


class MakeMethodStaticRefactoringListener(JavaParserLabeledListener):
    """

    To implement make method static (version 2).

    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None, method_name: str = None):
        """


        """

        if method_name is None:
            self.method_name = ""
        else:
            self.method_name = method_name

        if source_class is None:
            self.source_class = ""
        else:
            self.source_class = source_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False
        self.is_static = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
        else:
            self.is_source_class = False

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        method_identifier = ctx.IDENTIFIER().getText()
        if self.method_name in method_identifier:
            if grand_parent_ctx.modifier() is None or len(grand_parent_ctx.modifier()) == 0:
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.typeTypeOrVoid().start.tokenIndex,
                    to_idx=ctx.typeTypeOrVoid().stop.tokenIndex,
                    text='static ' + ctx.typeTypeOrVoid().getText()
                )
            else:
                for i in range(0, len(grand_parent_ctx.modifier())):
                    if grand_parent_ctx.modifier(i).getText() == 'static':
                        self.is_static = True
                        break
                if not self.is_static:
                    self.token_stream_rewriter.replaceRange(
                        from_idx=grand_parent_ctx.modifier(0).start.tokenIndex,
                        to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex,
                        text=grand_parent_ctx.modifier(0).getText() + ' static'
                    )


def main(udb_path, source_class, method_name, *args, **kwargs):
    """


    """

    main_file = None
    db = und.open(udb_path)
    classes = db.ents("Class")
    for cls in classes:
        if cls.simplename() == source_class:
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
    my_listener = MakeMethodStaticRefactoringListener(common_token_stream=token_stream,
                                                      source_class=source_class,
                                                      method_name=method_name)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', encoding='utf8', errors='ignore', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())

    return True


if __name__ == '__main__':
    udb_path_ = "/TestProject/TestProject.udb"
    source_class_ = "App"
    method_name_ = "testMethod"
    # initialize with understand
    main(udb_path_, source_class_, method_name_)
