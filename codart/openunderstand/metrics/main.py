from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from metric import DSCmetric, DSCmetric2
from pathlib import Path
import argparse
import os.path
import numpy as np
import json
from halstead import main_


def main(args):
    stream = FileStream(args.file, encoding="utf8")
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parse_tree = parser.compilationUnit()

    my_listener = DSCmetric()

    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    res = my_listener.get_name
    res2 = my_listener.get_arr
    res3 = my_listener.get_tmp
    res4 = my_listener.get_mmd
    val = []

    print("Method names: ")
    print(res)
    print("Used Variables: ")
    print(res4)
    print("Returned Variables: ")
    print(res3)
    print("Use Return: ")
    temp = np.intersect1d(res3, res4)
    print(temp)

    try:
        for i in range(len(res)):
            index = res3.index(temp[i])
            val.append(res[index])

            if len(val) == len(temp):
                zip_iterator = zip(val, temp)
                a_dictionary = dict(zip_iterator)

                print("final result: ")
                print(a_dictionary)

    except:
        pass


def main2(args, file_path):
    stream = FileStream(args.file, encoding="utf8")
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parse_tree = parser.compilationUnit()

    my_listener = DSCmetric2(file_path)

    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    my_listener.get_res


if __name__ == "__main__":
    inp = str(input("Enter the path to the Java project:"))
    # C:\Users\Roozbeh\PycharmProjects\pythonProject\Software Metrics

    try:
        dir = os.listdir(inp)

    except:
        print("Invalid Path")

    for dirpath, dirnames, filenames in os.walk(inp):
        for filename in [f for f in filenames if f.endswith(".java")]:
            argparser = argparse.ArgumentParser()
            print(filename)
            argparser.add_argument(
                "-n",
                "--file",
                help="Input source",
                default=os.path.join(dirpath, filename),
            )
            args = argparser.parse_args()
            # main(args)
            filepath = inp + "\\" + filename
            main2(args, filepath)
