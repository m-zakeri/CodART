from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from openunderstand.metrics.max_inheritance import FindAllInheritances
from openunderstand.metrics.max_inheritance import FindAllClasses
from openunderstand.metrics.max_nesting import MaxNesting
from openunderstand.metrics.min_max_essential_knots import MinEssentialKnots
import os
from fnmatch import fnmatch
import argparse


def get_max_inheritance(inheritances, key):
    current_classs = key
    level = 0
    while True:
        if not current_classs in inheritances.keys():
            break
        elif len(inheritances[current_classs]) == 0:
            break
        else:
            level += 1
            current_classs = inheritances[current_classs][0]

    return level


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        elif fnmatch(fullPath, "*.java"):
            allFiles.append(fullPath)

    return allFiles


def get_knot_inheritance_nested(ent_model=None):

    classes = {}
    class_names = []

    try:
        # at first we should Stream text from input file
        inputfile = InputStream(ent_model.contents(), encoding="utf8")
        # then we must use lexer
        lex = JavaLexer(inputfile)
        # then we should tokenize that
        toked = CommonTokenStream(lex)
        # at last we should parse tokenized
        parsed = JavaParserLabeled(toked)
        ptree = parsed.compilationUnit()

        listener = FindAllClasses()
        treewalker = ParseTreeWalker()
        treewalker.walk(t=ptree, listener=listener)
        for n in listener.class_names:
            class_names.append(n)

    except Exception as e:
        print("An Error occurred in file:" + ent_model.longname() + "\n" + str(e))

    for c in class_names:
        classes.update({c: []})

    inputfile = InputStream(ent_model.contents(), encoding="utf8")
    # then we must use lexer
    lex = JavaLexer(inputfile)
    # then we should tokenize that
    toked = CommonTokenStream(lex)
    # at last we should parse tokenized
    parsed = JavaParserLabeled(toked)
    ptree = parsed.compilationUnit()
    listener2 = FindAllInheritances(classes)
    treewalker2 = ParseTreeWalker()
    treewalker2.walk(t=ptree, listener=listener2)

    classes = listener2.classes

    max_inheritances = {}
    for key in classes.keys():
        max_inheritances.update({key: get_max_inheritance(classes, key)})

    print(f"Class Name = {max_inheritances}")

    inputfile = FileStream(ent_model.contents(), encoding="utf8")
    # then we must use lexer
    lex = JavaLexer(inputfile)
    # then we should tokenize that
    toked = CommonTokenStream(lex)
    # at last we should parse tokenized
    parsed = JavaParserLabeled(toked)
    ptree = parsed.compilationUnit()
    listener3 = MaxNesting()
    treewalker3 = ParseTreeWalker()
    treewalker3.walk(t=ptree, listener=listener3)
    print("Max Nesting of", file_address, " is: ", listener3.max_nesting)

    inputfile = InputStream(ent_model.contents(), encoding="utf8")
    # then we must use lexer
    lex = JavaLexer(inputfile)
    # then we should tokenize that
    toked = CommonTokenStream(lex)
    # at last we should parse tokenized
    parsed = JavaParserLabeled(toked)
    ptree = parsed.compilationUnit()
    listener4 = MinEssentialKnots()
    treewalker4 = ParseTreeWalker()
    treewalker4.walk(t=ptree, listener=listener4)
    return listener4.counter
