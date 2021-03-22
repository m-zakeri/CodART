import argparse

from antlr4 import *

# from refactorings.extract_class import ExtractClassRefactoringListener
from gen.java9 import Java9_v2Lexer
from gen.java9.Java9_v2Parser import Java9_v2Parser
from refactorings.extract_class_migrated import myExtractClassRefactoringListener
from refactorings.field_refactorings.movefielddown import movefielddownRefactoringListener, \
    movefield_down_gettextfield_Listener
from refactorings.field_refactorings.movefieldup import movefieldupRefactoringListener, \
    movefieldup_gettextfield_Listener, PropagationMovefieldUpRefactoringListener

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
def convert(set):
	return list(set)
# def main_movefiledUp(source_class, children_class, moved_fields, mainfile, fileslist,propagation_class,fileslist_to_be_propagate):
def main_movefiledUp(Root_path_udb_project,children_class, moved_fields):
    roorpath = ""
    a_string = Root_path_udb_project
    new_string = a_string.replace(".udb", "")

    roorpath = new_string + "//"
    print(roorpath)
    # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
    fileslist_to_be_propagate = set()
    propagation_classes = set()
    father_class = ""
    fileslist_to_be_rafeactored = set()
    mainfile = ""
    db = und.open(Root_path_udb_project)
    i = 0
    for field in db.ents("Java Variable"):
        for child in children_class:
            if (field.longname() == child + "." + moved_fields[0]):
                # print(field.parent().parent().relname())
                if(i==0):
                    mainfile = field.parent().parent().relname()
                i+=1

                # print(field.parent().parent().relname())
                fileslist_to_be_rafeactored.add(field.parent().parent().relname())
                # print(field.parent().refs())
                for fth in field.parent().refs("Extend"):
                    # print("father_class:", fth.ent().longname())
                    father_class = fth.ent().longname()
                    # print(fth.ent().parent().relname())
                    fileslist_to_be_rafeactored.add(fth.ent().parent().relname())
                # print("==================================")
                for ref in field.refs("Setby , Useby"):
                    # print(ref)
                    # print(ref.ent().parent())
                    propagation_classes.add(ref.ent().parent().longname())
                    # print(ref.ent().parent().parent().relname())
                    fileslist_to_be_propagate.add(ref.ent().parent().parent().relname())
    # print("=========================================")
    print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
    print("propagation_classes : ", propagation_classes)
    print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)
    print("father class :", father_class)
    print("main file:", mainfile)

    print("===========================================================================================")

    fileslist_to_be_propagate = convert(fileslist_to_be_propagate)
    propagation_classes=convert(propagation_classes)
    fileslist_to_be_rafeactored=convert(fileslist_to_be_rafeactored)
    # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text
    # print(children_class[0])
    # print(moved_fields[0])
    file_main = roorpath+mainfile
    # print(file_main)
    # print(moved_fields[0])
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
    print("************************************************************************************************************")
    get_text = movefieldup_gettextfield_Listener(common_token_stream=token_stream, child=children_class, field=moved_fields[0])
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=get_text)

    field_text = get_text.field_text
    print("field_text:",field_text)
    # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}end get text
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

        # parse_tree = sa_java9_v2.parse(stream, 'compilationUnit', None)
        # print("before")
        parse_tree = parser.compilationUnit()


        # Step 6: Create an instance of AssignmentStListener





        # gettext = movefield_gettextfield_Listener(common_token_stream=token_stream,child=["B"],field='a' )
        # walker = ParseTreeWalker()
        # walker.walk(t=parse_tree, listener=gettext)
        # print("====================================",gettext.field_text)

        my_listener = movefieldupRefactoringListener(common_token_stream=token_stream, destination_class=father_class,
                                                       children_class=children_class, moved_fields=moved_fields,fieldtext=field_text)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        # print("fileeeeeee:",file)
        with open("files_refactored/" + file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())
        # ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]end refactor

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
        my_listener = PropagationMovefieldUpRefactoringListener(token_stream_rewriter=token_stream,
                                                     old_class_name=children_class,
                                                     new_class_name=father_class,
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