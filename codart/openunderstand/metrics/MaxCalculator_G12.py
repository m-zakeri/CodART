from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from openunderstand.oudb.models import EntityModel
import os
from fnmatch import fnmatch
from openunderstand.metrics.Cyclomatic_G12 import CyclomaticListener
from openunderstand.metrics.Essential_G12 import EssentialMetricListener
from openunderstand.metrics.CyclomaticModified_G12 import CyclomaticModifiedListener
from openunderstand.metrics.CyclomaticStrict_G12 import CyclomaticStrictListener


def get_parse_tree(file_path):
    file = FileStream(file_path)
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)

    return parser.compilationUnit()


def MyMain(file_path):
    tree = get_parse_tree(file_path)
    listener = CyclomaticListener("")
    walker = ParseTreeWalker()
    walker.walk(listener, tree)


# create the list of files of a specific project
def getListOfFiles(file_path):
    list_of_file = os.listdir(file_path)
    all_files = list()
    for entry in list_of_file:
        # Create full path
        full_path = os.path.join(file_path, entry)
        if os.path.isdir(full_path):
            all_files = all_files + getListOfFiles(full_path)
        elif fnmatch(full_path, "*.java"):
            all_files.append(full_path)

    return all_files


class MaxCyclomatic:
    def __init__(self, my_listener):
        self.maxvalue = 0
        self.packages = {}
        self.files = {}
        self.listener = my_listener

    @property
    def return_max(self):
        return self.maxvalue

    def calculate_classes_value(self, input: str = ""):
        content = InputStream(input)
        lexer = JavaLexer(content)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        tree = parser.compilationUnit()
        walker = ParseTreeWalker()
        walker.walk(self.listener, tree)
        return self.listener.get_classes, self.listener.get_packagename

    def MaxClass(self, class_name, file_path):

        if file_path in self.files:
            classes = self.files[file_path][0]
            if class_name in classes:

                print(f"class {class_name} : {classes[class_name]}")
                return classes[class_name]
            else:
                return "the class is not found"

        else:
            return "the class is not in package"

    def MaxFile(self, content: str = ""):

        tuple_ = self.calculate_classes_value(content)
        package = tuple_[1]
        classes = tuple_[0]
        values = classes.values()
        value_list = list(values)
        if len(value_list) != 0:
            max_value = max(value_list)
        else:
            max_value = 0
        self.files[file] = (classes, max_value)
        if package not in self.packages:
            self.packages[package] = max_value
        else:
            prev_val = self.packages[package]
            if max_value > prev_val:
                self.packages[package] = max_value

        return package, max_value

    def return_all_class_maxes(self, classes, file_path):
        for cls in classes:
            self.MaxClass(cls, file_path)

    def return_package_max(self, content: str = "") -> int:
        try:
            v = self.MaxFile(content=content)
            package = v[0]
            max_v = v[1]
            if self.maxvalue < max_v:
                self.maxvalue = max_v
            print("class information:")
            self.return_all_class_maxes(self.files[file][0], file)
        except Exception as e:
            print("Error", e)

        print("package information:")
        package = sorted(self.packages)
        for p in package:
            print(f"in package {p} : {self.packages[p]}")

        value_of_proj = self.packages.values()
        list_values = list(value_of_proj)
        max_val = 0
        if len(list_values) != 0:
            max_val = max(list_values)

        return self.maxvalue


# using database(not working properly)
class MaxValue:
    def __init__(self):
        self.max_classes_values = 0
        self.packagename = " "
        self.max_package_Value = 0

    def Max_class_value(self, class_name, file_path):
        print("longname", class_name)
        entity = EntityModel.get_or_none(_longname=class_name)
        tree = get_parse_tree(file_path)
        print("entity", entity)
        if entity:
            listener = CyclomaticListener(entity._name)
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            print(f"for class {class_name}  : {listener.get_max_value}")
            self.packagename = listener.get_packagename
            return listener.get_max_value

        else:
            print("the class does not exist!")
            return 0

    # stop until here to find the bug
    def Max_package_Value(self, path_):
        entity = EntityModel.get_or_none(_longname=path_)
        print("fileEntity", entity)
        classes = EntityModel.select().where(EntityModel.parent == entity)
        for cls in classes:
            try:

                if str(cls._kind).__contains__("Class") and cls._longname != "":
                    print("kind", cls._kind)
                    print("longname", cls._longname)
                    print("parent", cls._parent)
                    value = self.Max_class_value(cls._longname, path)

                    if self.max_classes_values < value != 0:
                        self.max_classes_values = value
            except Exception as e:
                print("An Error occurred", e)

        print(
            f"The maxvalue of package {self.packagename} with value {self.max_classes_values}"
        )
        return self.max_classes_values

    def max_project_value(self, files_, projectname):
        for file in files_:
            value = self.Max_package_Value(file)
            if self.max_package_Value < value:
                self.max_package_Value = value

        print(
            f"the max value of the main project {projectname} is {self.max_package_Value}"
        )


def run_with_database(path_):
    max_cyclomatic_ = MaxValue()
    max_cyclomatic_.max_project_value(files_, "calculator_Project")


def max_cyclomatic_modified(ent_model=None) -> int:
    Cyclomatic_listener = CyclomaticModifiedListener(ent_model.contents())
    max_cyclomatic_ = MaxCyclomatic(Cyclomatic_listener)
    return max_cyclomatic_.return_package_max(content=ent_model.contents())


def max_cyclomatic_stricts(ent_model=None) -> int:
    Cyclomatic_listener = CyclomaticStrictListener(ent_model.contents())
    max_cyclomatic_ = MaxCyclomatic(Cyclomatic_listener)
    return max_cyclomatic_.return_package_max(content=ent_model.contents())


def max_essential(ent_model=None) -> int:
    Cyclomatic_listener = EssentialMetricListener(ent_model.contents())
    max_cyclomatic_ = MaxCyclomatic(Cyclomatic_listener)
    return max_cyclomatic_.return_package_max(content=ent_model.contents())


def max_cyclomatic(ent_model=None) -> int:
    Cyclomatic_listener = CyclomaticListener(ent_model.contents())
    max_cyclomatic_ = MaxCyclomatic(Cyclomatic_listener)
    return max_cyclomatic_.return_package_max(content=ent_model.contents())
