import os
import errno
import argparse
import understand as und
from antlr4 import *

from gen.java.JavaParser import JavaParser
from gen.java.JavaLexer import JavaLexer
# from refactorings.field_refactorings.IncreaseFieldVisibility import DecreaseFieldVisibilityRefactoringListener, \
#     IncreaseFieldVisibilityRefactoringListener
from refactorings.class_refactorings.CollapseHierarchy import CollapsHierarchyRefactoring_GetFieldText_Listener, \
    CollapsHierarchyRefactoring_GetMethodText_Listener, CollapssHierarchyRefactoringListener, \
    PropagationCollapssHierarchyListener
from refactorings.class_refactorings.MakeAbstractClass import MakeAbstractClassRefactoringListener
from refactorings.class_refactorings.MakeClassFinal import MakeFinalClassRefactoringListener
from refactorings.class_refactorings.MakeClassNonFinal import MakeNonFinalClassRefactoringListener
from refactorings.class_refactorings.MakeConcreteClass import MakeConcreteClassRefactoringListener
from refactorings.class_refactorings.RemoveClass import RemoveClassRefactoringListener
from refactorings.class_refactorings.RemoveInterface import RemoveInterfaceRefactoringListener
from refactorings.class_refactorings.extract_Subclass import myExtractSubClassRefactoringListener
from refactorings.extract_class_migrated import myExtractClassRefactoringListener
from refactorings.field_refactorings.DecreaseFieldVisibility import DecreaseFieldVisibilityRefactoringListener
# from refactorings.field_refactorings.IncreaseFieldVisibility import IncreaseFieldVisibilityRefactoringListener, \
#     PropagationIncreaseFieldVisibility_GetObjects_RefactoringListener, \
#     PropagationIncreaseFieldVisibilityRefactoringListener
from refactorings.field_refactorings.IncreaseFieldVisibility import IncreaseFieldVisibilityRefactoringListener, \
    PropagationIncreaseFieldVisibility_GetObjects_RefactoringListener, \
    PropagationIncreaseFieldVisibilityRefactoringListener
from refactorings.field_refactorings.MakeFieldFinal import MakeFieldFinalRefactoringListener
from refactorings.field_refactorings.MakeFieldNonFinal import MakeFieldNonFinalRefactoringListener
from refactorings.field_refactorings.MakeFieldNonStatic import MakeFieldNonStaticRefactoringListener
from refactorings.field_refactorings.MakeFieldStatic import MakeFieldStaticRefactoringListener
from refactorings.field_refactorings.RemoveField import RemoveFieldRefactoringListener
from refactorings.field_refactorings.movefielddown import PropagationMovefieldDownRefactoringListener, \
    movefielddownRefactoringListener, movefield_down_gettextfield_Listener
from refactorings.field_refactorings.movefieldup import PropagationMovefieldUpRefactoringListener, \
    movefieldupRefactoringListener, movefieldup_gettextfield_Listener
# from refactorings.method_refactorings.IncreaseMethodVisibility import DecreaseMethodVisibilityRefactoringListener
from refactorings.method_refactorings.DecreaseMethodVisibility import DecreaseMethodVisibilityRefactoringListener
from refactorings.method_refactorings.IncreaseMethodVisibility import IncreaseMethodVisibilityRefactoringListener
from refactorings.method_refactorings.MakeMethodFinal import MakeMethodFinalRefactoringListener
from refactorings.method_refactorings.MakeMethodNonFinal import MakeMethodNonFinalRefactoringListener
from refactorings.method_refactorings.MakeMethodNonStatic import MakeMethodNonStaticRefactoringListener
from refactorings.method_refactorings.MakeMethodStatic import MakeMethodStaticRefactoringListener
from refactorings.method_refactorings.MoveMethodDown import PropagationMoveMethodDownRefactoringListener, \
    MoveMethodDownRefactoringListener, MoveMethodDownRefactoring_GetMethodText_Listener
from refactorings.method_refactorings.MoveMethodUp import PropagationMoveMethodUpRefactoringListener, \
    MoveMethodUpRefactoringListener, GetMethodTextMoveMethodUpRefactoringListener
from refactorings.method_refactorings.RemoveMethod import RemoveMethodRefactoringListener


class Main_Refactors_Action_for_big_project():
    def __init__(self):
        self.x = 2

    def convert(self, set):
        return list(set)

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def main_IncreaseFieldVisibility(self, Root_path_udb_project, source_class, field_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "/"
        print(roorpath)
        file_list_include_file_name_that_edited = ""
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        file_list_to_be_propagate = set()
        propagate_classes = set()
        db = und.open(Root_path_udb_project)
        for field in db.ents("public variable"):
            if (str(field) == str(source_class + "." + field_name)):
                print("==================================\nfield =", field.longname())
                print(field.parent().parent().relname())
                # get path file include this field.
                if (field.parent().parent().relname() is not None):
                    mainfile = field.parent().parent().relname()
                    mainfile = '/'.join(mainfile.split('/')[2:])
                else:
                    for ref in field.refs("Definein"):
                        mainfile = (ref.file().relname())
                        mainfile = '/'.join(mainfile.split('/')[2:])
                # get propagate class and their file
                for ref in field.refs("Setby , Useby"):
                    if not (str(ref.ent()) == str(field.parent())
                            or str(ref.ent().parent()) == str(field.parent())):
                        propagate_classes.add(str(ref.ent().parent()))
                        file_list_to_be_propagate.add("src/" + ref.file().relname())

                #     pr
        file_list_to_be_propagate = self.convert(file_list_to_be_propagate)
        propagate_classes = self.convert(propagate_classes)

        # [[[[[[[[[
        flag_file_is_refatored = False
        corpus = open(
            r"filename_status_database.txt", encoding="utf-8").read()
        if corpus.find("name:" + mainfile) == -1:
            with open("filename_status_database.txt", mode='w', encoding="utf-8", newline='') as f:
                f.write(corpus + "\nname:" + mainfile)
                f.flush()
                os.fsync(f.fileno())
            file_list_include_file_name_that_edited += mainfile + "\n"
        else:
            flag_file_is_refatored = True
            print("file already edited")
        # ]]]]]]]]
        mainfile = "src/" + mainfile
        mainfiletemp = mainfile
        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        print("LOG 0:", mainfile)
        file_main = roorpath + mainfile
        print("LOG 1:", file_main)
        print("LOG 2:", roorpath)

        argparser = argparse.ArgumentParser()
        # [[[
        if (flag_file_is_refatored):
            argparser.add_argument('-n', '--file', help='Input source',
                                   default="files_refactored/" + mainfiletemp)
        else:
            argparser.add_argument('-n', '--file', help='Input source',
                                   default=file_main)
            print("LOG 6", file_main)

        # ]]]
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
        my_listener = IncreaseFieldVisibilityRefactoringListener(common_token_stream=token_stream,
                                                                 source_class=source_class,
                                                                 field_name=field_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        print("file to be saved most be :", "files_refactored/" + mainfile)
        with open("files_refactored/" + mainfile, mode='w', encoding="utf-8", newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())
            f.flush()
            os.fsync(f.fileno())
        # propagate start$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        print("file_list_to_be_propagate:", file_list_to_be_propagate)
        for file in file_list_to_be_propagate:
            #
            file = '/'.join(file.split('/')[2:])
            print("LOG 5", file)
            flag_file_edited = False
            corpus = open(
                r"filename_status_database.txt", encoding="utf-8").read()
            if (corpus.find("name:" + file) == -1):

                with open("filename_status_database.txt", mode='w', encoding="utf-8", newline='') as f:
                    f.write(corpus + "\nname:" + file)
                    f.flush()
                    os.fsync(f.fileno())
                file_list_include_file_name_that_edited += file + "\n"
            else:
                flag_file_edited = True
            #
            argparser = argparse.ArgumentParser()
            if (flag_file_edited):
                argparser.add_argument('-n', '--file', help='Input source', default="files_refactored/" + file)
            else:
                argparser.add_argument('-n', '--file', help='Input source', default=roorpath + file)

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
            parse_tree = parser.compilationUnit()

            # get object
            my_listener_get_object = PropagationIncreaseFieldVisibility_GetObjects_RefactoringListener(token_stream,
                                                                                                       source_class=source_class,
                                                                                                       propagated_class_name=propagate_classes)
            walker = ParseTreeWalker()
            walker.walk(t=parse_tree, listener=my_listener_get_object)

            my_listener = PropagationIncreaseFieldVisibilityRefactoringListener(common_token_stream=token_stream,
                                                                                using_field_name=field_name,
                                                                                object_name=my_listener_get_object.objects,
                                                                                propagated_class_name=propagate_classes)
            walker = ParseTreeWalker()
            walker.walk(t=parse_tree, listener=my_listener)

            filename = "files_refactored/" + file
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open("files_refactored/" + file, mode='w', encoding="utf-8", newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText())
                f.flush()
                os.fsync(f.fileno())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_ExtractSubclasse(self, Root_path_udb_project, source_class, moved_methods, moved_fields):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        father_path_file = ""
        file_list_to_be_propagate = set()
        propagate_classes = set()

        db = und.open(Root_path_udb_project)

        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                father_path_file = cls.parent().relname()
                print(cls.refs())
                for ref in cls.refs("Coupleby"):
                    # print(ref.ent().longname())
                    propagate_classes.add(ref.ent().longname())
                    # print(ref.ent().parent().relname())
                    # file_list_to_be_propagate.add(ref.ent().parent().relname())
            # if(cls.longname()==fatherclass):
            #     print(cls.parent().relname())
            #     father_path_file=cls.parent().relname()

        print("propagate_classes :", propagate_classes)
        print("file_list_to_be_propagate:", file_list_to_be_propagate)
        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        print("mainfile:", father_path_file)
        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + father_path_file
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
        # elf, common_token_stream: CommonTokenStream = None,
        # source_class: str = None, new_class: str = None,
        # moved_fields = None, moved_methods = None):
        my_listener = myExtractSubClassRefactoringListener(common_token_stream=token_stream,
                                                           source_class=source_class
                                                           , new_class=source_class + "extracted",
                                                           moved_fields=moved_fields, moved_methods=moved_methods)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)
        filename = "files_refactored/" + father_path_file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + father_path_file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_Extractclasse(self, Root_path_udb_project, source_class, moved_methods, moved_fields):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        father_path_file = ""
        file_list_to_be_propagate = set()
        propagate_classes = set()

        db = und.open(Root_path_udb_project)

        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                father_path_file = cls.parent().relname()
                print(cls.refs())
                for ref in cls.refs("Coupleby"):
                    # print(ref.ent().longname())
                    propagate_classes.add(ref.ent().longname())
                    # print(ref.ent().parent().relname())
                    # file_list_to_be_propagate.add(ref.ent().parent().relname())
            # if(cls.longname()==fatherclass):
            #     print(cls.parent().relname())
            #     father_path_file=cls.parent().relname()

        print("propagate_classes :", propagate_classes)
        print("file_list_to_be_propagate:", file_list_to_be_propagate)
        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        print("mainfile:", father_path_file)
        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + father_path_file
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
        # elf, common_token_stream: CommonTokenStream = None,
        # source_class: str = None, new_class: str = None,
        # moved_fields = None, moved_methods = None):
        my_listener = myExtractClassRefactoringListener(common_token_stream=token_stream,
                                                        source_class=source_class
                                                        , new_class=source_class + "extracted",
                                                        moved_fields=moved_fields, moved_methods=moved_methods)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)
        filename = "files_refactored/" + father_path_file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + father_path_file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_CollapsHierarchy(self, Root_path_udb_project, childclass, fatherclass):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        child_path_file = ""
        father_path_file = ""
        file_list_to_be_propagate = set()
        propagate_classes = set()
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == childclass):
                print(cls.parent().relname())
                child_path_file = cls.parent().relname()
                print(cls.refs())
                for ref in cls.refs("Coupleby"):
                    propagate_classes.add(ref.ent().longname())
                    file_list_to_be_propagate.add(ref.ent().parent().relname())
            if (cls.longname() == fatherclass):
                print(cls.parent().relname())
                father_path_file = cls.parent().relname()

        print("propagate_classes :", propagate_classes)
        print("file_list_to_be_propagate:", file_list_to_be_propagate)

        file_list_to_be_propagate = self.convert(file_list_to_be_propagate)
        propagate_classes = self.convert(propagate_classes)

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        print("mainfile:", child_path_file)
        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + child_path_file
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
        my_listenerfieldtext = CollapsHierarchyRefactoring_GetFieldText_Listener(common_token_stream=token_stream,
                                                                                 child_class=childclass)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listenerfieldtext)
        fieldcode = my_listenerfieldtext.fieldcode
        print("fieldcode ::", fieldcode)

        my_listener_method_text = CollapsHierarchyRefactoring_GetMethodText_Listener(common_token_stream=token_stream,
                                                                                     child_class=childclass)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener_method_text)
        methods_code = my_listener_method_text.methodcode

        print("methods_code:", methods_code)

        #     remove child class
        my_listener_remove_childclass = RemoveClassRefactoringListener(common_token_stream=token_stream,
                                                                       class_name=childclass)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener_remove_childclass)
        filename = "files_refactored/" + child_path_file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + child_path_file, mode='w', newline='') as f:
            f.write(my_listener_remove_childclass.token_stream_rewriter.getDefaultText())
        #     refactored begin#######################################
        file_main = roorpath + father_path_file
        argparser = argparse.ArgumentParser()
        if (father_path_file == child_path_file):
            argparser.add_argument('-n', '--file', help='Input source', default="files_refactored/" + child_path_file)
        else:
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
        my_listenerrefactor_Action = CollapssHierarchyRefactoringListener(common_token_stream=token_stream
                                                                          , parent_class=fatherclass,
                                                                          child_class=childclass,
                                                                          field_text=fieldcode,
                                                                          method_text=methods_code)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listenerrefactor_Action)

        filename = "files_refactored/" + father_path_file
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + father_path_file, mode='w', newline='') as f:
            f.write(my_listenerrefactor_Action.token_stream_rewriter.getDefaultText())
        # beging of propagate*********************************************************
        print("file_list_to_be_propagate::::::::", file_list_to_be_propagate)
        for file in file_list_to_be_propagate:
            argparser = argparse.ArgumentParser()
            if (file in [child_path_file, father_path_file]):
                argparser.add_argument('-n', '--file', help='Input source', default="files_refactored/" + file)
            else:
                argparser.add_argument('-n', '--file', help='Input source', default=roorpath + file)
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
            parse_tree = parser.compilationUnit()
            my_listener_propagate = PropagationCollapssHierarchyListener(token_stream_rewriter=token_stream,
                                                                         old_class_name=childclass,
                                                                         new_class_name=fatherclass,
                                                                         propagated_class_name=propagate_classes)
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

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_RemoveInterface(self, Root_path_udb_project, source_class):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")
        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("Interface"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        print("mainfile:", mainfile)
        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = RemoveInterfaceRefactoringListener(common_token_stream=token_stream,
                                                         interface_name=source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_RemoveClass(self, Root_path_udb_project, source_class):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = RemoveClassRefactoringListener(common_token_stream=token_stream,
                                                     class_name=source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_MakeClassConcrete(self, Root_path_udb_project, source_class):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeConcreteClassRefactoringListener(common_token_stream=token_stream,
                                                           class_name=source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_MakeClassNonFinal(self, Root_path_udb_project, source_class):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeNonFinalClassRefactoringListener(common_token_stream=token_stream,
                                                           class_name=source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_MakeClassFinal(self, Root_path_udb_project, source_class):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeFinalClassRefactoringListener(common_token_stream=token_stream,
                                                        class_name=source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_MakeAbstractClass(self, Root_path_udb_project, source_class):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeAbstractClassRefactoringListener(common_token_stream=token_stream,
                                                           class_name=source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_RemoveMethod(self, Root_path_udb_project, source_class, method_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = RemoveMethodRefactoringListener(common_token_stream=token_stream,
                                                      source_class=source_class,
                                                      method_name=method_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_MakeMethodStatic(self, Root_path_udb_project, source_class, method_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeMethodStaticRefactoringListener(common_token_stream=token_stream,
                                                          source_class=source_class,
                                                          method_name=method_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_MakeMethodNonStatic(self, Root_path_udb_project, source_class, method_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeMethodNonStaticRefactoringListener(common_token_stream=token_stream,
                                                             source_class=source_class,
                                                             method_name=method_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_MakeMethodNONFinal(self, Root_path_udb_project, source_class, method_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeMethodNonFinalRefactoringListener(common_token_stream=token_stream,
                                                            source_class=source_class,
                                                            method_name=method_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_MakeMethodFinal(self, Root_path_udb_project, source_class, method_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeMethodFinalRefactoringListener(common_token_stream=token_stream,
                                                         source_class=source_class,
                                                         method_name=method_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_IncreaseMethodVisibility(self, Root_path_udb_project, source_class, method_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//src//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = IncreaseMethodVisibilityRefactoringListener(common_token_stream=token_stream,
                                                                  source_class=source_class,
                                                                  method_name=method_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def main_DecreaseMethodVisibility(self, Root_path_udb_project, source_class, method_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = DecreaseMethodVisibilityRefactoringListener(common_token_stream=token_stream,
                                                                  source_class=source_class,
                                                                  method_name=method_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def main_DecreaseFieldVisibility(self, Root_path_udb_project, source_class, field_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = DecreaseFieldVisibilityRefactoringListener(common_token_stream=token_stream,
                                                                 source_class=source_class,
                                                                 field_name=field_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_Remove_Field(self, Root_path_udb_project, source_class, field_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = RemoveFieldRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                     field_name=field_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def main_Make_Field_Static(self, Root_path_udb_project, source_class, field_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeFieldStaticRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                         field_name=field_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def main_Make_Field_Non_Static(self, Root_path_udb_project, source_class, field_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeFieldNonStaticRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                            field_name=field_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def main_Make_Field_Non_Final(self, Root_path_udb_project, source_class, field_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)
        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeFieldNonFinalRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                           field_name=field_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def main_Make_Field_Final(self, Root_path_udb_project, source_class, field_name):
        roorpath = ""
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")

        roorpath = new_string + "//"
        print(roorpath)
        # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        mainfile = ""
        db = und.open(Root_path_udb_project)

        for cls in db.ents("class"):
            if (cls.longname() == source_class):
                print(cls.parent().relname())
                mainfile = cls.parent().relname()

        #     ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        file_main = roorpath + mainfile
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
        my_listener = MakeFieldFinalRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                        field_name=field_name)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        filename = "files_refactored/" + mainfile
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("files_refactored/" + mainfile, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def main_movefileddown(self, Root_path_udb_project, source_class, moved_fields):
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
        mainfile = ""
        db = und.open(Root_path_udb_project)

        for field in db.ents("Java Variable"):
            if (field.longname() == source_class + "." + moved_fields[0]):
                print(field.refs())
                print("mainfile : ", field.parent().parent().relname())
                mainfile = field.parent().parent().relname()
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

        fileslist_to_be_propagate = self.convert(fileslist_to_be_propagate)
        propagation_classes = self.convert(propagation_classes)
        children_class = self.convert(children_class)
        fileslist_to_be_rafeactored = self.convert(fileslist_to_be_rafeactored)
        print("==============================================================================")
        # ]]]

        # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text

        file_main = roorpath + mainfile
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
        get_text = movefield_down_gettextfield_Listener(common_token_stream=token_stream, father=source_class,
                                                        field=moved_fields[0])
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=get_text)

        field_text = get_text.field_text
        print(field_text)
        # ]]]]]]]end get text
        # Step 1: Load input source into stream
        # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{begin refatored
        for file in fileslist_to_be_rafeactored:
            argparser = argparse.ArgumentParser()
            argparser.add_argument('-n', '--file', help='Input source', default=roorpath + file)
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

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def main_MoveMethodDown(self, Root_path_udb_project, source_class, moved_methods):
        a_string = Root_path_udb_project
        new_string = a_string.replace(".udb", "")
        roorpath = new_string + "//"
        print(roorpath)

        # initialize with undrestand
        mainfile = ""
        fileslist_to_be_propagate = set()
        propagation_classes = set()
        children_class = set()
        fileslist_to_be_rafeactored = set()
        db = und.open(Root_path_udb_project)
        for mth in db.ents("Java Method"):
            if (mth.longname() == source_class + "." + moved_methods):
                print(mth.parent())
                for childcls in mth.parent().refs("Extendby"):
                    children_class.add(childcls.ent().longname())
                    fileslist_to_be_rafeactored.add(childcls.ent().parent().relname())
                print(mth.longname())
                print(mth.refs())
                print("mainfile : ", mth.parent().parent().relname())
                mainfile = mth.parent().parent().relname()
                for ref in mth.refs("Java Callby"):
                    fileslist_to_be_propagate.add(ref.ent().parent().parent().relname())
                    propagation_classes.add(ref.ent().parent().longname())

        print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
        print("propagation_classes : ", propagation_classes)
        print("children_class :", children_class)
        print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)
        fileslist_to_be_propagate = self.convert(fileslist_to_be_propagate)
        propagation_classes = self.convert(propagation_classes)
        children_class = self.convert(children_class)
        fileslist_to_be_rafeactored = self.convert(fileslist_to_be_rafeactored)
        print("==============================================================================")

        # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text
        file_main = roorpath + mainfile
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
        # listener get text
        get_text = MoveMethodDownRefactoring_GetMethodText_Listener(common_token_stream=token_stream,
                                                                    source_class=source_class,
                                                                    moved_method=moved_methods)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=get_text)

        method_text = get_text.method_text
        print(method_text)
        # }}}}}end get text

        # /{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{begin refarore

        for file in fileslist_to_be_rafeactored:
            argparser = argparse.ArgumentParser()
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
            # Step 5: Create parse tree
            # 1. Python backend --> Low speed
            # parse_tree = parser.compilationUnit()

            # 2. C++ backend --> high speed

            parse_tree = parser.compilationUnit()

            my_listener = MoveMethodDownRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                            children_class=children_class, moved_methods=moved_methods,
                                                            method_text=method_text)
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

        # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{beging of propagate

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
            my_listener = PropagationMoveMethodDownRefactoringListener(token_stream_rewriter=token_stream,
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

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def main_MoveMethodUp(self, Root_path_udb_project, children_class, moved_methods):
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
            for child in children_class:
                if (mth.longname() == child + "." + moved_methods):
                    mainfile = mth.parent().parent().relname()
                    fileslist_to_be_rafeactored.add(mth.parent().parent().relname())
                    for fth in mth.parent().refs("Extend"):
                        destination_class = fth.ent().longname()
                        fileslist_to_be_rafeactored.add(fth.ent().parent().relname())
                    for ref in mth.refs("Java Callby"):
                        propagation_classes.add(ref.ent().parent().longname())
                        fileslist_to_be_propagate.add(ref.ent().parent().parent().relname())
        print("=========================================")
        print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
        print("propagation_classes : ", propagation_classes)
        print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)
        print("father class :", destination_class)
        print("main file:", mainfile)

        fileslist_to_be_rafeactored = self.convert(fileslist_to_be_rafeactored)
        fileslist_to_be_propagate = self.convert(fileslist_to_be_propagate)
        propagation_class = self.convert(propagation_classes)
        print("----------------------------------------------------------------------------")

        # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text
        file_main = roorpath + mainfile
        print("file_main:", file_main)
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
        print("method_text:", method_text)
        # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}end get text

        # ////////////////////////////////////////////////////////////////////////
        # refactored start
        for file in fileslist_to_be_rafeactored:
            argparser = argparse.ArgumentParser()
            argparser.add_argument('-n', '--file', help='Input source', default=roorpath + file)
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
            parse_tree = parser.compilationUnit()

            my_listener_refactor = MoveMethodUpRefactoringListener(common_token_stream=token_stream,
                                                                   destination_class=destination_class,
                                                                   children_class=children_class,
                                                                   moved_methods=moved_methods,
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

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def main_movefiledUp(self, Root_path_udb_project, children_class, moved_fields):
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
                    if (i == 0):
                        mainfile = field.parent().parent().relname()
                    i += 1
                    fileslist_to_be_rafeactored.add(field.parent().parent().relname())
                    for fth in field.parent().refs("Extend"):
                        father_class = fth.ent().longname()
                        fileslist_to_be_rafeactored.add(fth.ent().parent().relname())
                    for ref in field.refs("Setby , Useby"):
                        propagation_classes.add(ref.ent().parent().longname())
                        fileslist_to_be_propagate.add(ref.ent().parent().parent().relname())
        print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
        print("propagation_classes : ", propagation_classes)
        print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)
        print("father class :", father_class)
        print("main file:", mainfile)

        print("===========================================================================================")

        fileslist_to_be_propagate = self.convert(fileslist_to_be_propagate)
        propagation_classes = self.convert(propagation_classes)
        fileslist_to_be_rafeactored = self.convert(fileslist_to_be_rafeactored)
        # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text
        # print(children_class[0])
        # print(moved_fields[0])
        file_main = roorpath + mainfile
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
        print(
            "************************************************************************************************************")
        # get text
        get_text = movefieldup_gettextfield_Listener(common_token_stream=token_stream, child=children_class,
                                                     field=moved_fields[0])
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=get_text)

        field_text = get_text.field_text
        print("field_text:", field_text)
        # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}end get text
        for file in fileslist_to_be_rafeactored:
            argparser = argparse.ArgumentParser()
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
            # refator listener
            my_listener = movefieldupRefactoringListener(common_token_stream=token_stream,
                                                         destination_class=father_class,
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
            # propagate listener
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

        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        # def main_movefiledUp(self, Root_path_udb_project, children_class, moved_fields):
        #     roorpath = ""
        #     a_string = Root_path_udb_project
        #     new_string = a_string.replace(".udb", "")
        #
        #     roorpath = new_string + "\\"
        #     print(roorpath)
        #     # initialize with undrestand [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
        #     fileslist_to_be_propagate = set()
        #     propagation_classes = set()
        #     father_class = ""
        #     fileslist_to_be_rafeactored = set()
        #     mainfile = ""
        #     db = und.open(Root_path_udb_project)
        #     i = 0
        #     for field in db.ents("Java Variable"):
        #         for child in children_class:
        #             if (field.longname() == child + "." + moved_fields[0]):
        #                 # print(field.parent().parent().relname())
        #                 if (i == 0):
        #                     mainfile = field.parent().parent().relname()
        #                 i += 1
        #
        #                 # print(field.parent().parent().relname())
        #                 fileslist_to_be_rafeactored.add(field.parent().parent().relname())
        #                 # print(field.parent().refs())
        #                 for fth in field.parent().refs("Extend"):
        #                     # print("father_class:", fth.ent().longname())
        #                     father_class = fth.ent().longname()
        #                     # print(fth.ent().parent().relname())
        #                     fileslist_to_be_rafeactored.add(fth.ent().parent().relname())
        #                 # print("==================================")
        #                 for ref in field.refs("Setby , Useby"):
        #                     # pri
        #                     print("child=:", child)
        #                     print(ref.ent().longname())
        #                     print(ref.ent().longname())
        #                     if (ref.ent().longname() == child):
        #                         continue
        #
        #                     # print(ref.ent().parent())
        #
        #                     propagation_classes.add(ref.ent().parent().longname())
        #                     # print(ref.ent().parent().parent().relname())
        #                     print(ref.ent().parent().relname())
        #                     fileslist_to_be_propagate.add(ref.ent().parent().parent().relname())
        #     # print("=========================================")
        #     print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
        #     print("propagation_classes : ", propagation_classes)
        #     print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)
        #     print("father class :", father_class)
        #     print("main file:", mainfile)
        #
        #     print("===========================================================================================")
        #
        #     fileslist_to_be_propagate = self.convert(fileslist_to_be_propagate)
        #     propagation_classes = self.convert(propagation_classes)
        #     fileslist_to_be_rafeactored = self.convert(fileslist_to_be_rafeactored)
        #     # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text
        #     # print(children_class[0])
        #     # print(moved_fields[0])
        #     file_main = roorpath + "\\src\\" + mainfile
        #
        #     # C:\Users\saeed\Desktop\prg\JHotDraw7_0_6\src\org\jhotdraw\app\action
        #     # C:\Users\saeed\Desktop\prg\JHotDraw7_0_6\src\org\jhotdraw\app\action\ClearAction.java
        #     # C:\Users\saeed\Desktop\prg\JHotDraw7_0_6\org\jhotdraw\app\action\ClearAction.java
        #     # file_main = file_main.replace("\\", "//")
        #
        #     print("file_main:::", file_main)
        #     # print(file_main)
        #     # print(moved_fields[0])
        #     argparser = argparse.ArgumentParser()
        #     argparser.add_argument('-n', '--file', help='Input source', default=file_main)
        #     args = argparser.parse_args()
        #     stream = FileStream(args.file, encoding='utf8')
        #     # Step 2: Create an instance of AssignmentStLexer
        #     lexer = JavaLexer(stream)
        #     # Step 3: Convert the input source into a list of tokens
        #     token_stream = CommonTokenStream(lexer)
        #     # Step 4: Create an instance of the AssignmentStParser
        #     parser = JavaParser(token_stream)
        #     parser.getTokenStream()
        #     parse_tree = parser.compilationUnit()
        #     print(
        #         "************************************************************************************************************")
        #     get_text = movefieldup_gettextfield_Listener(common_token_stream=token_stream, child=children_class,
        #                                                  field=moved_fields[0])
        #     walker = ParseTreeWalker()
        #     walker.walk(t=parse_tree, listener=get_text)
        #
        #     field_text = get_text.field_text
        #     print("field_text:", field_text)
        #     # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}end get text
        #     for file in fileslist_to_be_rafeactored:
        #         argparser = argparse.ArgumentParser()
        #         argparser.add_argument('-n', '--file', help='Input source', default=roorpath + file)
        #         args = argparser.parse_args()
        #         # //////////////////////////////////////////////////////////////////////////
        #         stream = FileStream(args.file, encoding='utf8')
        #         # input_stream = StdinStream()
        #         # Step 2: Create an instance of AssignmentStLexer
        #         lexer = JavaLexer(stream)
        #         # Step 3: Convert the input source into a list of tokens
        #         token_stream = CommonTokenStream(lexer)
        #         # Step 4: Create an instance of the AssignmentStParser
        #         parser = JavaParser(token_stream)
        #         parser.getTokenStream()
        #         # Step 5: Create parse tree
        #         # 1. Python backend --> Low speed
        #         # parse_tree = parser.compilationUnit()
        #
        #         # 2. C++ backend --> high speed
        #
        #         # parse_tree = sa_java9_v2.parse(stream, 'compilationUnit', None)
        #         # print("before")
        #         parse_tree = parser.compilationUnit()
        #
        #         # Step 6: Create an instance of AssignmentStListener
        #
        #         # gettext = movefield_gettextfield_Listener(common_token_stream=token_stream,child=["B"],field='a' )
        #         # walker = ParseTreeWalker()
        #         # walker.walk(t=parse_tree, listener=gettext)
        #         # print("====================================",gettext.field_text)
        #
        #         my_listener = movefieldupRefactoringListener(common_token_stream=token_stream,
        #                                                      destination_class=father_class,
        #                                                      children_class=children_class, moved_fields=moved_fields,
        #                                                      fieldtext=field_text)
        #         walker = ParseTreeWalker()
        #         walker.walk(t=parse_tree, listener=my_listener)
        #
        #         filename = "files_refactored/" + file
        #         if not os.path.exists(os.path.dirname(filename)):
        #             try:
        #                 os.makedirs(os.path.dirname(filename))
        #             except OSError as exc:  # Guard against race condition
        #                 if exc.errno != errno.EEXIST:
        #                     raise
        #         # print("fileeeeeee:",file)
        #         with open("files_refactored/" + file, mode='w', newline='') as f:
        #             f.write(my_listener.token_stream_rewriter.getDefaultText())
        #         # ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]end refactor
        #
        #     # beging of propagate
        #
        #     for file in fileslist_to_be_propagate:
        #         argparser = argparse.ArgumentParser()
        #         if (file in fileslist_to_be_rafeactored):
        #             argparser.add_argument('-n', '--file', help='Input source', default="files_refactored/" + file)
        #         else:
        #             argparser.add_argument('-n', '--file', help='Input source', default=roorpath + file)
        #         args = argparser.parse_args()
        #         # //////////////////////////////////////////////////////////////////////////
        #         stream = FileStream(args.file, encoding='utf8')
        #         # input_stream = StdinStream()
        #         # Step 2: Create an instance of AssignmentStLexer
        #         lexer = JavaLexer(stream)
        #         # Step 3: Convert the input source into a list of tokens
        #         token_stream = CommonTokenStream(lexer)
        #         # Step 4: Create an instance of the AssignmentStParser
        #         parser = JavaParser(token_stream)
        #         parser.getTokenStream()
        #         parse_tree = parser.compilationUnit()
        #         my_listener = PropagationMovefieldUpRefactoringListener(token_stream_rewriter=token_stream,
        #                                                                 old_class_name=children_class,
        #                                                                 new_class_name=father_class,
        #                                                                 propagated_class_name=propagation_classes)
        #         walker = ParseTreeWalker()
        #         walker.walk(t=parse_tree, listener=my_listener)
        #
        #         filename = "files_refactored/" + file
        #         if not os.path.exists(os.path.dirname(filename)):
        #             try:
        #                 os.makedirs(os.path.dirname(filename))
        #             except OSError as exc:  # Guard against race condition
        #                 if exc.errno != errno.EEXIST:
        #                     raise
        #         with open("files_refactored/" + file, mode='w', newline='') as f:
        #             f.write(my_listener.token_stream_rewriter.getDefaultText())
