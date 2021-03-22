import argparse

from antlr4 import *

# from refactorings.extract_class import ExtractClassRefactoringListener
from gen.java9 import Java9_v2Lexer
from gen.java9.Java9_v2Parser import Java9_v2Parser
from refactorings.extract_class_migrated import myExtractClassRefactoringListener
from refactorings.field_refactorings.movefielddown import movefielddownRefactoringListener, \
    movefield_down_gettextfield_Listener, PropagationMovefieldDownRefactoringListener
from refactorings.field_refactorings.movefieldup import movefieldupRefactoringListener, movefieldup_gettextfield_Listener

from speedy.src.java9speedy.parser import sa_java9_v2
#
import os
import errno
import argparse
import understand as und
from antlr4 import *

from gen.java.JavaParser import JavaParser
from gen.java.JavaLexer import JavaLexer
from refactorings.extract_class_migrated import myExtractClassRefactoringListener
#
# def get_information(Root_path_project,source_class,move_field):
def convert(set):
	return list(set)
# def main_movefileddown(source_class, children_class, moved_fields, mainfile, fileslist_to_be_rafeactored, propagation_classes, fileslist_to_be_propagate):
def main_movefileddown(Root_path_udb_project, source_class, moved_fields):
    roorpath = ""
    a_string = Root_path_udb_project
    new_string = a_string.replace(".udb", "")

    roorpath = new_string + "//"
    print(roorpath)
    # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
    fileslist_to_be_propagate = set()
    propagation_classes = set()
    children_class = set()
    fileslist_to_be_rafeactored = set()
    mainfile=""
    db = und.open(Root_path_udb_project)

    for field in db.ents("Java Variable"):
        if (field.longname() == source_class + "." + moved_fields[0]):
            print(field.refs())
            print("mainfile : ", field.parent().parent().relname())
            mainfile=field.parent().parent().relname()
            for ref in field.refs("Java Setby , Useby"):
                fileslist_to_be_propagate.add(ref.ent().parent().parent().relname())
                propagation_classes.add(ref.ent().parent().longname())
    print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
    print("propagation_classes : ", propagation_classes)

    for classname in db.ents("class"):
        if (classname.longname() == source_class):
            for childcls in classname.refs("Extendby"):
                children_class.add(childcls.ent().longname())
                fileslist_to_be_rafeactored.add(childcls.ent().parent().relname())
    print("children_class :", children_class)
    print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)

    fileslist_to_be_propagate=convert(fileslist_to_be_propagate)
    propagation_classes = convert(propagation_classes)
    children_class = convert(children_class)
    fileslist_to_be_rafeactored = convert(fileslist_to_be_rafeactored)
    print("==============================================================================")
    # ]]]

    # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text



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
    get_text = movefield_down_gettextfield_Listener(common_token_stream=token_stream, father=source_class, field=moved_fields[0])
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=get_text)

    field_text = get_text.field_text
    print(field_text)
    # ]]]]]]]end get text
    # Step 1: Load input source into stream
    # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{begin refatored
    for file in fileslist_to_be_rafeactored:
        argparser = argparse.ArgumentParser()
        argparser.add_argument('-n', '--file', help='Input source', default=roorpath+file)
        args = argparser.parse_args()
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

        # parse_tree = sa_java9_v2.parse(stream, 'compilationUnit', None)
        parse_tree = parser.compilationUnit()
        my_listener = movefielddownRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                       children_class=children_class, moved_fields=moved_fields,
                                                       fieldtext=field_text)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())
        # ]]]end of refactored

    # beging of propagate{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{

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
        my_listener = PropagationMovefieldDownRefactoringListener(token_stream_rewriter=token_stream,
                                                                old_class_name=source_class,
                                                                new_class_name=children_class[0],
                                                                propagated_class_name=propagation_classes)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())