import argparse

from antlr4 import *

# from refactorings.extract_class import ExtractClassRefactoringListener
from gen.java9 import Java9_v2Lexer
from gen.java9.Java9_v2Parser import Java9_v2Parser
from refactorings.extract_class_migrated import myExtractClassRefactoringListener
from refactorings.field_refactorings.movefielddown import movefielddownRefactoringListener, \
    movefield_down_gettextfield_Listener
from refactorings.field_refactorings.movefieldup import movefieldupRefactoringListener, movefieldup_gettextfield_Listener
from refactorings.method_refactorings.MoveMethodDown import MoveMethodDownRefactoring_GetMethodText_Listener, \
    MoveMethodDownRefactoringListener
from refactorings.method_refactorings.MoveMethodUp import GetMethodTextMoveMethodUpRefactoringListener, \
    MoveMethodUpRefactoringListener, PropagationMoveMethodUpRefactoringListener

from speedy.src.java9speedy.parser import sa_java9_v2
#
import argparse
import os
import errno
import argparse
import understand as und
from antlr4 import *

from gen.java.JavaParser import JavaParser
from gen.java.JavaLexer import JavaLexer
from refactorings.extract_class_migrated import myExtractClassRefactoringListener
#
def convert(set):
	return list(set)
# def main_MoveMethodUp(destination_class, children_class, moved_methods, mainfile, fileslist_to_be_rafeactored, propagation_class, fileslist_to_be_propagate):
def main_MoveMethodUp(Root_path_udb_project,children_class, moved_methods):
    a_string = Root_path_udb_project
    new_string = a_string.replace(".udb", "")
    roorpath = new_string + "//"
    print(roorpath)
    # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
    destination_class = ""
    mainfile = ""
    fileslist_to_be_rafeactored = set()
    fileslist_to_be_propagate = set()
    propagation_classes = set()

    db = und.open(Root_path_udb_project)
    i = 0
    for mth in db.ents("Java Method"):
        # print(mth)
        for child in children_class:

            if (mth.longname() == child + "." + moved_methods):
                # print(child, "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
                # print("main file:", mth.parent().parent().relname())
                if (i == 0):
                    mainfile = mth.parent().parent().relname()
                i += 1
                fileslist_to_be_rafeactored.add(mth.parent().parent().relname())
                # print("mth.parent():", mth.parent())
                # print(mth.parent().refs())
                for fth in mth.parent().refs("Extend"):
                    # print("father_class:", fth.ent().longname())
                    destination_class = fth.ent().longname()
                    # print(fth.ent().parent().relname())
                    fileslist_to_be_rafeactored.add(fth.ent().parent().relname())
                # print("============")
                for ref in mth.refs("Java Callby"):
                    # print("ref:",ref)
                    # print("ref.ent().parent():", ref.ent().parent())
                    propagation_classes.add(ref.ent().parent().longname())
                    # print("ref.ent().parent().parent().relname():", ref.ent().parent().parent().relname())
                    fileslist_to_be_propagate.add(ref.ent().parent().parent().relname())
    print("=========================================")
    print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
    print("propagation_classes : ", propagation_classes)
    print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)
    print("father class :", destination_class)
    print("main file:", mainfile)

    fileslist_to_be_rafeactored = convert(fileslist_to_be_rafeactored)
    fileslist_to_be_propagate = convert(fileslist_to_be_propagate)
    propagation_class = convert(propagation_classes)
    print("----------------------------------------------------------------------------")

    # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text
    file_main = roorpath+mainfile
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-n', '--file', help='Input source', default=file_main)
    args = argparser.parse_args()
    stream = FileStream(args.file, encoding='utf8')
    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParser(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    get_text = GetMethodTextMoveMethodUpRefactoringListener(common_token_stream=token_stream,
                                                                child_class=children_class, moved_methods=moved_methods)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=get_text)

    method_text = get_text.method_text
    print("method_text:",method_text)
    # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}end get text

    # ////////////////////////////////////////////////////////////////////////
    # filelist=["javatest1.java","javatest2.java"]
    for file in fileslist_to_be_rafeactored:
        argparser = argparse.ArgumentParser()
        argparser.add_argument('-n', '--file', help='Input source', default=roorpath+file)
        args = argparser.parse_args()
        # //////////////////////////////////////////////////////////////////////////
        stream = FileStream(args.file, encoding='utf8')
        # input_stream = StdinStream()
        # Step 2: Create an instance of AssignmentStLexer
        lexer = JavaLexer(stream)
        # Step 3: Convert the input source into a list of tokens
        token_stream = CommonTokenStream(lexer)
        # Step 4: Create an instance of the AssignmentStParser
        parser = JavaParser(token_stream)
        parser.getTokenStream()
        # Step 5: Create parse tree
        # 1. Python backend --> Low speed
        # parse_tree = parser.compilationUnit()

        # 2. C++ backend --> high speed

        parse_tree = parser.compilationUnit()

        my_listener_refactor = MoveMethodUpRefactoringListener(common_token_stream=token_stream, destination_class=destination_class,
                                                        children_class=children_class, moved_methods=moved_methods,
                                                        method_text=method_text)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener_refactor)

        filename = "files_refactored/" + file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + file, mode='w', newline='') as f:
            f.write(my_listener_refactor.token_stream_rewriter.getDefaultText())
        # ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]end refactoring
    # beging of propagate

    for file in fileslist_to_be_propagate:
        argparser = argparse.ArgumentParser()
        if (file in fileslist_to_be_rafeactored):
            argparser.add_argument('-n', '--file', help='Input source', default="files_refactored/" + file)
        else:
            argparser.add_argument('-n', '--file', help='Input source', default=roorpath + file)
        args = argparser.parse_args()
        # //////////////////////////////////////////////////////////////////////////
        stream = FileStream(args.file, encoding='utf8')
        # input_stream = StdinStream()
        # Step 2: Create an instance of AssignmentStLexer
        lexer = JavaLexer(stream)
        # Step 3: Convert the input source into a list of tokens
        token_stream = CommonTokenStream(lexer)
        # Step 4: Create an instance of the AssignmentStParser
        parser = JavaParser(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener_propagate = PropagationMoveMethodUpRefactoringListener(token_stream_rewriter=token_stream,
                                                                old_class_name=children_class,
                                                                new_class_name=destination_class,
                                                                propagated_class_name=propagation_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener_propagate)

        filename = "files_refactored/" + file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + file, mode='w', newline='') as f:
            f.write(my_listener_propagate.token_stream_rewriter.getDefaultText())