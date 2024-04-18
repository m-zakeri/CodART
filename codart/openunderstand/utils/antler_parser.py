import ctypes
from os.path import join
from os import getcwd
from antlr4 import InputStream, Token
from antlr4.tree.Tree import ParseTree
from antlr4.error.ErrorListener import ErrorListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class SA_ErrorListener:
    """
    Base callback class to handle Antlr syntax errors.

    Not able to do a 1-to-1 bridge of Antlr's error listener
    Instead, this class provides roughly equivalent functionality.

    """

    def syntaxError(
        self,
        input_stream: InputStream,
        offendingSymbol: Token,
        char_index: int,
        line: int,
        column: int,
        msg: str,
    ):
        """
        Called when lexer or parser encountered a syntax error.

        Parameters
        ----------
        input_stream:InputStream
            Reference to the original input stream that this error is from

        offendingSymbol:Token
            If available, denotes the erronous token

        char_index:int
            Character offset of the error within the input stream

        line:int
            Line number of the error

        column:int
            Character offset within the line

        msg:str
            Antlr error message
        """
        pass


# antlr_lib = ctypes.cdll.LoadLibrary(
#     join(
#         getcwd(),
#         "gen",
#         "java8speedy",
#         "antlr4-runtime",
#         "src",
#         "sa_javalabeled.cpython-310-x86_64-linux-gnu.so",
#     )
# )  # Replace with the actual path to your shared library
# from .sa_javalabeled_cpp_parser import JavaLabeledParser
import sa_javalabeled

antlr_lib = sa_javalabeled


def _cpp_parse(
    stream: InputStream,
    entry_rule_name: str = "compilationUnit",
    sa_err_listener: ErrorListener = None,
    java_parser_labeld: SA_ErrorListener = None,
) -> ParseTree:
    # Validate input types here before handing over to C++
    if not isinstance(stream, InputStream):
        raise TypeError("'stream' shall be an Antlr InputStream")
    if not isinstance(entry_rule_name, str):
        raise TypeError("'entry_rule_name' shall be a string")
    if sa_err_listener is not None and not isinstance(
        sa_err_listener, SA_ErrorListener
    ):
        raise TypeError(
            "'sa_err_listener' shall be an instance of SA_ErrorListener or None"
        )
    print(dir(antlr_lib))
    return antlr_lib.do_parse(
        java_parser_labeld, stream, entry_rule_name, sa_err_listener
    )
