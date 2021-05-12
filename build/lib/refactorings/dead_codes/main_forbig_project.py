"""

The main module of CodART

-changelog
-- Add C++ backend support

"""

__version__ = '0.2.0'
__author__ = 'Morteza'

from utilization.understand_install_test import *

try:
    import understand as und
except ModuleNotFoundError:
    # Error handling
    pass


print(und.version())

from antlr4 import *

# from refactorings.extract_class import ExtractClassRefactoringListener
from gen.java9.Java9_v2Parser import Java9_v2Parser
# from refactorings.Main_refactorings_action_module import Main_Refactors_Action
# from refactorings.Main_refactorings_action_module import Main_Refactors_Action
# from refactorings.Refactoring_action_module_for_big_project import Main_Refactors_Action_for_big_project
from refactorings.dead_codes.Refactoring_action_module_for_big_project import Main_Refactors_Action_for_big_project
from refactorings.extract_class_migrated import myExtractClassRefactoringListener
from refactorings.field_refactorings.MoveFieldUp_Main import main_movefiledUp
from refactorings.method_refactorings.main_MoveMethodDown import main_MoveMethodDown
from refactorings.method_refactorings.main_MoveMoethodUp import main_MoveMethodUp
# from refactorings.Refactoring_action_module import Main_Refactors_Action

from speedy.src.java9speedy.parser import sa_java9_v2
#
import argparse

from antlr4 import *

from gen.java.JavaLexer import JavaLexer
from refactorings.extract_class_migrated import myExtractClassRefactoringListener


#

# def main_movefiledup(source_class,children_class,moved_fields,mainfile,fileslist):
#     # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ get text
#     file_main = mainfile
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
#     get_text = movefield_down_gettextfield_Listener(common_token_stream=token_stream, father="father", field='f')
#     walker = ParseTreeWalker()
#     walker.walk(t=parse_tree, listener=get_text)
#
#     field_text = get_text.field_text
# }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}end get text
#     ==============================================================================================================================
def get_addres(field):
    # str = "Java Definein - RELATIVE:\JHotDraw7_0_6\src\org\jhotdraw\draw\action\SwingWorker.java - RELATIVE:\JHotDraw7_0_6\src\org\jhotdraw\draw\action\SwingWorker.java(19,6)"
    str = field
    start = str.find('RELATIVE:')
    end = str.find('.java')
    out = ""
    for i in range(int(start) + 10, int(end) + 5):
        out += str[i]
    b = out.find('\\')
    e = out.find('.java')
    r = ""
    for j in range(int(b), int(e) + 5):
        r += out[j]
    # print(r)
    return r


def get_information(Root_path_project, source_class, move_field):
    father_path_file = ""
    file_list_to_be_propagate = set()
    propagate_classes = set()
    isNotnonecounter = 0
    isnonecouner = 0;
    class_counte = 0
    isnon = 0
    isnotnon = 0

    file_main = ""
    db = und.open(Root_path_project)
    for field in db.ents("public variable"):
        #
        if (field.parent() is not None and str(field.parent().kind()).find(
                'Class') != -1):  # public variabel  ممکنه شامل متغیرهای شمارشی enum  نیز باشند
            print("=========================================")
            print("fieldname:", field.longname())
            print("field parent cldass:", field.parent())
            print("field parent kind:", field.parent().kind())
            print("field file name :", field.refs("Java Definein")[0].file().relname())
            print("refrence ::::::::::::::::::::::")
            for ref in field.refs("Setby , Useby"):
                if not (str(ref.ent()) == str(field.parent()) or str(ref.ent().parent()) == str(field.parent())):
                    print(ref)
                    print(ref.ent().kind())
                    if (str(ref.ent().parent().kind()).find('Class') == -1):
                        propagate_classes.add(str(ref.ent().parent()))
                        print((ref.ent().parent()))
                        file_list_to_be_propagate.add(ref.file().relname())
                        print(ref.file().relname())
                    #     print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    propagate_classes.add(str(ref.ent().parent()))
                    file_list_to_be_propagate.add(ref.file().relname())
                    print("ref file name   :", ref.file().relname())
                    print("field file name :", field.refs("Java Definein")[0].file().relname())
                    print("+")
                # else:print("    in father class ref is:",ref)

    print(propagate_classes)
    print(file_list_to_be_propagate)
    # print(field)
    # print(source_class+"."+move_field)
    # if(str(field)==str(source_class+"."+move_field)):
    #      print("==================================\nfield =",field.longname())
    #      print(field.parent().parent().relname())
    #      file_main=field.parent().parent().relname()
    # print("refrences:",field.refs())
    # for ref in field.refs():
    #    print(ref)
    #    print(ref.lexeme())

    # print("parent:",field.parent())
    #
    # print(field.refs("Setby , Useby"))
    # for ref in field.refs("Setby , Useby"):
    #     if( ref.ent().parent()!=field.parent()  and str(ref.ent().parent().kind())!="File"):
    #         print("ref parent :",ref.ent().parent() )
    #         print("kind ref :",ref.ent().parent().kind())
    #         print(ref)
    """
    db = und.open(Root_path_project)
    for cls in db.ents("Java Class"):
        if ( not cls.contents() == ""): # اگر متن کلاس مخالف تهی بود یعنی کلاس لایبرری نیست

            # print("=============================\nlongname :",cls.longname())
            # print(cls.ents('Define',"Java Method"))
            # print("\t","Definein:", cls.refs("Definein"))
            # if(cls.library()!=""):
            #     print("library:",cls.library())
            #
            # print(cls.dependsby())
            # library()) != "Standard"
            # print("relname :", cls.parent().relname())
            # print("templist:", cls.refs("Java Definein")[0].file().relname())
            # if(len(cls.refs("Definein"))>0):
            #     print("templist:",cls.refs("Java Definein")[0].file().relname())

            if(len(cls.refs("Java Extendby"))>0   and len(cls.ents("define","variable"))>0):

                print("====================================================================\nlongname :", cls.longname())
                print(len(cls.refs("Java Extendby")), cls.refs("Java Extendby"))
                if (len(cls.refs("Definein")) > 0):
                    print("templist:", cls.refs("Java Definein")[0].file().relname())
                print(len(cls.ents("define","variable")),cls.ents("define","variable"))
                print("--------------------------------")
                for field in cls.ents("define","variable"):
                    print("field ::::::::::::::::::::::::",field.name())
                    refactorable=True
                    for ref in field.refs("Setby , Useby"):
                        if(ref.ent().parent() is not None): # 6 ta isnon hastan va 979 ta isnot non
                            # print("++++++")

                            if(ref.ent().parent().longname()==cls.longname() ):#  اگر پدر اون رفرنس برابر خود( کلاس شامل فیلد)نبود
                                print("true")
                                print("ref.ent().parent().longname():",ref.ent().parent().longname())
                                print("cls.longname()               :",cls.longname())

                                print("ref.ent().longname()::",ref.ent().longname())
                                print("ref parent(ref.ent().parent()) :",ref.ent().parent())
                                # if( ref.ent().longname()==source_class):
                                #     print("okkkkkkkkkkkkkkkkkkkkkkkk")
                                print(" ref:",ref)
                                print("file ref ref.file().relname() :",ref.file().relname())
                                print("++++++")
                        else:
                            print("[[[[[[[[[[[[",ref,"]]]]]]]]]]]]]]")

            # print(cls.refs("Java Extendby"))


        # print(isnon)
        # print(isnotnon)

        # for ref in cls.refs("Definein"):
        #     print("ref.file:",ref.file().relname())




        # \JHotDraw7_0_6\src\org\jhotdraw\draw\BezierLabelLocator.java
        # \JHotDraw7_0_6\src\org\jhotdraw\draw\BezierLabelLocator.java
        # if(cls.longname()=="org.jhotdraw.gui.saeed.vahid"):
        #     print(cls.parent().relname())
        # if(cls.parent().relname() is None):
        #     print("{{{{{{{")
            # print(cls.refs("Definein"))
            # print("longname :", cls.longname())
            # print(cls.parent().relname())
            # if(len(cls.refs("Definein"))==1):
        #         print("********************************")
        #         print(cls.refs("Definein"))
        #         for ref in print(cls.refs("Definein")):
        #             print(ref)

            # print("}}}}}}}\n")







        # if(not(cls.parent().relname() is None)):
        #     print("longname :", cls.longname())
        #     print("\t",cls.parent().relname())
        #     isNotnonecounter+=1
        # else:
        #     isnonecouner+=1



    # for field in db.ents("Java Variable"):
    #
    #     reflist=field.refs("Java Setby , Useby")
    #     if(len(reflist)==10):
    #         print(field.parent().parent().parent().relname())
    #         print(field.longname())
    #         print(reflist)
    #         print()
        # for ref in field.refs("Java Setby , Useby"):



    # for cls in db.ents("class"):
    #     # print(cls.longname())
    #     if(cls.longname()==source_class):
    #          print(cls.parent().relname())
    #          father_path_file=cls.parent().relname()
    #          print(cls.refs())
    #          for ref in cls.refs("Extendby"):
    #              print(ref.ent().longname())
    #              propagate_classes.add(ref.ent().longname())
    #              print(ref.ent().parent().relname())
                 # file_list_to_be_propagate.add(ref.ent().parent().relname())
        # if(cls.longname()==fatherclass):
        #     print(cls.parent().relname())
        #     father_path_file=cls.parent().relname()

    # print("propagate_classes :",propagate_classes)
    # print("file_list_to_be_propagate:",file_list_to_be_propagate)


    """


if __name__ == '__main__':
    # print(timestamp())
    with open("../../filename_status_database.txt", mode='w', encoding="utf-8", newline='') as f:
        f.write(
            "This file contains the list of Java files that were refracted, and if the Java file name was in this file, you must read it from the(files_refactord) folder.\n")
    refactor_action = Main_Refactors_Action_for_big_project()

    # increrase field:
    #     Root_path_project = "C:\\Users\\saeed\\Desktop\\prg\\JHotDraw7_0_6.udb"
    #     source_class="SelectAllAction"
    #     moved_fields="ID"
    # get_information(Root_path_project, source_class, moved_fields)
    #
    # Path
    # os.path
    Root_path_project = "/home/ali/Documents/compiler/Research/advanced_compiler_updated_projects/esmaili/refactoring_project_and_document/prg/JHotDraw7_0_6.udb"
    print(os.path.isfile(Root_path_project))
    mylist = list()
    db = und.open(Root_path_project)
    i = 0
    j = 0
    for cls in db.ents("class"):
        if (cls.contents() != ""):
            j += 1
    print("len class:", j)
    print("len class cc:", len(db.ents("class")))

    for field in db.ents("public variable"):
        if (field.parent() is not None and str(field.parent().kind()).find('Class') != -1):
            mysplit = (str(field).split("."))
            # print(mysplit)
            mylist.append("")
            mylist[i] = list()
            mylist[i].append(mysplit[0])
            mylist[i].append(mysplit[1])
            i += 1
    k = 0
    print(len(mylist))
    for item in mylist:
        refactor_action.main_IncreaseFieldVisibility(Root_path_project, mylist[k][0], mylist[k][1])
        k += 1
        print("==================================================================================")

# move field down parameters{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{
#     source_class = 'org.jhotdraw.app.action.SaveAction'
#     moved_fields = ['ID']
#     Root_path_project="C://Users//saeed//Desktop//prg//JHotDraw7_0_6.udb"
#     get_information(Root_path_project,source_class,moved_fields[0])
# refactor_action.main_movefileddown(Root_path_project, source_class, moved_fields)


# move method down parameter{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{
#     source_class = 'father'
#     moved_methods = 'method1'
#     Root_path_project = "C://Users//saeed//Desktop//prg//testprobagation_java.udb"
#     # main_MoveMethodDown(Root_path_project, source_class, moved_methods)
#     # refactor_action.main_MoveMethodDown(Root_path_project, source_class, moved_methods)


# """move field Up parameter{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{
#     children_class = ["child1", "child2"]
#     moved_fields = ['k']
#     Root_path_project = "C://Users//saeed//Desktop//prg//testprobagation_java.udb"
#     # main_movefiledUp(Root_path_project,children_class, moved_fields)
#     refactor_action.main_movefiledUp(Root_path_project,children_class, moved_fields)

# move method up parameter{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{
#     children_class = ["child1", "child2"]
#     moved_methods='display2'
#     Root_path_project = "C://Users//saeed//Desktop//prg//testprobagation_java.udb"
#     refactor_action.main_MoveMethodUp(Root_path_project, children_class, moved_methods)


# help='Input source', default=r'../grammars/Test.java')
