import antlr4

from .parser import sa_javalabeled


class ExampleErrorListener(sa_javalabeled.SA_ErrorListener):
    def syntaxError(
        self,
        input_stream,
        offendingSymbol,
        char_index: int,
        line: int,
        column: int,
        msg: str,
    ):
        print("Syntax Error!")
        print("    input_stream:", repr(input_stream))
        print("    offendingSymbol:", offendingSymbol, type(offendingSymbol))
        print("    char_index:", char_index)
        print("    line:", line)
        print("    column:", column)
        print("    msg:", msg)


def print_tree(input_file: str):
    if sa_javalabeled.USE_CPP_IMPLEMENTATION:
        print("Using C++ implementation of parser")
    else:
        print("Using Python implementation of parser")

    # Optional: Override default error listener with my own
    sa_err_listener = ExampleErrorListener()

    # Create an Antlr InputStream and parse it!
    stream = antlr4.FileStream(input_file)
    tree = sa_javalabeled.parse(stream, "compilationUnit", sa_err_listener)

    print(tree.toStringTree())
