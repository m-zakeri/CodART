from antlr4 import *
from antlr4 import CommonTokenStream, FileStream
from cfg_generator.src.antlr.gen.JavaLexer import JavaLexer
from cfg_generator.src.antlr.gen.JavaParser import JavaParser
from cfg_generator.src.cfg_extractor.cfg_extractor_visitor import CFGExtractorVisitor
from cfg_generator.src.graph.visual import draw_CFG
import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def extract(stream):
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParser(token_stream)
    parse_tree = parser.compilationUnit()
    cfg_extractor = CFGExtractorVisitor()
    cfg_extractor.visit(parse_tree)
    funcs = cfg_extractor.functions
    LastNodes = cfg_extractor.functionLastNode
    return funcs, token_stream, LastNodes


def makedir(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as error:
        print(error)


def main(file_path):

    is_verbose = True


    absolute_path = os.path.abspath(file_path)


    print(f"Processing file: {absolute_path}")


    stream = FileStream(absolute_path, encoding="utf8")
    funcs, token_stream, end_nodes = extract(stream)

    output_list = []

    for method_name, cfg in funcs.items():
        output_dir = os.path.join(ROOT_DIR, f"..\\test_output\\{Path(absolute_path).stem}\\{method_name}")
        makedir(output_dir)

        method_output = []

        draw_CFG(cfg, end_nodes.get(method_name, []),
                 os.path.join(output_dir, f"{method_name}"),
                 token_stream, verbose=is_verbose, function_name=method_name, output_list=method_output)

        output_list.append(method_output)

    print(output_list)
    return output_list


if __name__ == '__main__':
    input_file = "C:\\Users\\Lenovo\\Desktop\\cfg_test\\19_jmca\\ASTNode.java"
    # input_file = "G:\\OpenUnderstand\\cfg_generator\\test_source\\if.java"
    main(input_file)
