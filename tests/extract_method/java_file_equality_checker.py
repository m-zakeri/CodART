from antlr4 import *
from codart.gen.JavaLexer import JavaLexer


def is_equal(file1, file2):
    input_stream1 = FileStream(file1)
    lexer1 = JavaLexer(input_stream1)

    input_stream2 = FileStream(file2)
    lexer2 = JavaLexer(input_stream2)

    token1 = lexer1.nextToken()
    token2 = lexer2.nextToken()

    params1 = set([])
    params2 = set([])
    add_to_params = False

    while token1.type != Token.EOF and token2.type != Token.EOF:

        if token1.type == lexer1.LINE_COMMENT or token1.type == lexer1.COMMENT or token1.type == lexer1.WS:
            token1 = lexer1.nextToken()
            continue

        if token2.type == lexer2.LINE_COMMENT or token2.type == lexer2.COMMENT or token2.type == lexer2.WS:
            token2 = lexer2.nextToken()
            continue

        if token1.text != token2.text:
            if token1.type == lexer1.THROWS:
                while token1.type != lexer1.LBRACE:
                    token1 = lexer1.nextToken()
            elif add_to_params:
                params1.add(token1.text)
                params2.add(token2.text)
            else:
                print(token1.line)
                print(token2.line)
                print(token1.text, '!=', token2.text, ' = ', token1.text != token2.text)
                return False

        elif token1.type == lexer1.LPAREN:
            add_to_params = True
        elif token1.type == lexer1.RPAREN:
            add_to_params = False
            if len(params1) != len(params2):
                return False
            for param in params1:
                if not params2.__contains__(param):
                    return False

        token1 = lexer1.nextToken()
        token2 = lexer2.nextToken()

    return True
