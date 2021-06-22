import os
import subprocess
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir, get_program_with_field_usage
from refactorings.utils.utils_listener_fast import TokensInfo, Field, Class, Method, LocalVariable, ClassImport, Program
from antlr4.TokenStreamRewriter import TokenStreamRewriter


class UnResolvedMetaError(Exception):
    pass


class NonStaticFieldRefactorError(Exception):
    pass


class MoveFieldRefactoring:
    def __init__(self, source_filenames: list, package_name: str,
                 class_name: str, field_name: str, target_class_name: str,
                 target_package_name: str, filename_mapper=None):
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_name = class_name
        self.field_name = field_name
        self.target_class_name = target_class_name
        self.target_package_name = target_package_name
        self.formatter = os.path.abspath(
            "../assets/formatter/google-java-format-1.10.0-all-deps.jar")
        if filename_mapper is None:
            self.filename_mapper = lambda x: f"{os.path.dirname(x)}/{os.path.splitext(os.path.basename(x))[0]}.java"
            return

        self.filename_mapper = filename_mapper

    def get_metadata(self, program):
        """
        :param program: The program which is extracted from the get_program() method
        :return: The source class, target_class and the field which is to be moved
        if there are no such classes or fields or packages in the program, KeyError will be raised
        """
        class_name = program.packages[self.package_name].classes[self.class_name]
        target_class = program.packages[self.target_package_name].classes[self.target_class_name]
        field = program.packages[self.package_name].classes[self.class_name].fields[self.field_name]

        return class_name, target_class, field

    @staticmethod
    def __stringify(tokens, start, end):
        """
        :param tokens: a list of tokens
        :param start: the index of the first token you want
        :param end: the index of the last token you want
        :return: String of the desired tokens
        Converts list of tokens into strings
        """
        string = ""
        for t in tokens[start: end]:
            if t.text != ' ':
                string += t.text

        return string

    def __is_field_in_class(self, field, target_class):
        """
        :param field: The field which is to be checked
        :param target_class: The target class name
        :return: Whether the field is in the target class or not
        """
        class_fields = target_class.fields
        for f in class_fields:
            if f == field.name:
                return True

        return False

    def should_add_import(self, klass: Class):
        # we don't need to handle target class
        if klass.name == self.target_class_name:
            return False

        # check package imports
        for package_import in klass.file_info.package_imports:
            if package_import.package_name == self.target_package_name:
                return False

        # if target class not imported as package then check class imports
        for class_import in klass.file_info.class_imports:
            if class_import.class_name == self.target_class_name:
                return False

        # if target class is not imported add the import
        return True

    def __propagate(self, program: Program, rewriter: Rewriter):
        """
        :param rewriter: The rewriter object which is going to rewrite the files
        :param usages: the usages of the field in the program
        :return: void
        Propagates the changes made to the files and the field
        """
        modified_files = []

        for pkg in program.packages.values():
            for klass in pkg.classes.values():
                if not hasattr(klass, "usages"):
                    continue

                modified_files.append(self.filename_mapper(klass.filename))
                for usage in klass.usages:
                    tokens_info = TokensInfo(usage)
                    token_stream = usage.parser.getTokenStream()
                    if token_stream not in rewriter.token_streams.keys():
                        rewriter.token_streams[token_stream] = (
                            usage["meta_data"].filename,
                            TokenStreamRewriter(token_stream),
                            usage["meta_data"].filename
                        )
                    rewriter.replace(tokens_info, f'{self.target_class_name}.{self.field_name}')

                if klass.name == self.target_class_name:
                    continue

                if self.should_add_import(klass):
                    self.__add_import(klass, rewriter)

        return modified_files

    def move(self):
        """
        :return: Whether the refactoring is completed or not
        Performs the move field refactoring
        """
        # usages, program = self.__get_usage()
        program = get_program_with_field_usage(
            self.source_filenames, self.field_name, self.class_name)
        source_package = program.packages[self.package_name]
        target_package = program.packages[self.target_package_name]
        source_class = source_package.classes[self.class_name]
        target_class = target_package.classes[self.target_class_name]
        field = source_class.fields[self.field_name]
        rewriter = Rewriter(program, self.filename_mapper)

        self.__remove_field_from_src(field, rewriter)
        self.__move_field_to_dst(target_class, field, rewriter)
        modified_files = self.__propagate(program, rewriter)
        rewriter.apply()
        self.__reformat(modified_files)

        return True

    def __remove_field_from_src(self, field: Field, rewriter: Rewriter):
        """
        :param field: The field which is to be moved in the refactoring
        :param rewriter: The rewriter object which is going to rewrite the files
        :return: void
        Remove the field from the source class
        """
        tokens = TokensInfo(field.parser_context)
        tokens.stop += 1
        rewriter.replace(tokens, "")

        for mod_ctx in field.modifiers_parser_contexts:
            mod_tokens = TokensInfo(mod_ctx)
            mod_tokens.stop += 1
            rewriter.replace(mod_tokens, "")

    def __move_field_to_dst(self, target: Class, field: Field, rewriter: Rewriter):
        """
        :param target: The target class that the field is going to be moved to
        :param field: The field which is to be moved in the refactoring
        :param rewriter: The rewriter object which is going to rewrite the files
        :return: void
        Move the field from the source to the target class
        """
        # this nasty if is because the grammar sucks. converts new SomeClass() to newSomeClass()
        if field.initializer is not None and field.initializer.startswith("new"):
            field.initializer = field.initializer.replace("new", "new ", 1)

        self.__modify_access_modifiers(field)

        new_field = f'\n\t{" ".join(field.modifiers)} {field.datatype} {field.name}{f" = {field.initializer};" if field.initializer else ";"}\n'
        target_class_tokens = TokensInfo(target.body_context)
        rewriter.insert_after_start(target_class_tokens, new_field)

    def __modify_access_modifiers(self, field: Field):
        """
        :param field: The field which is going to be modified
        :return: void
        Changes the moving field's access modifiers
        """
        index = -1
        for i, mod in enumerate(field.modifiers):
            if mod == "private" or mod == "protected" or mod == "public":
                index = i
                break

        if index != -1:
            field.modifiers.pop(index)

        field.modifiers.insert(0, "public")

    def __reformat(self, modified_files: list):
        """
        :param modified_files: The files that have been modified since the refactoring
        :return: void
        reformats the java files based on google's java pretty format
        """
        cmd = ["java", "-jar", self.formatter, "--replace"]
        cmd.extend(modified_files)
        subprocess.call(cmd)

    def __add_import(self, klass: Class, rewriter):
        """
        :param klass: The class where the import should be added to
        :param rewriter: The rewriter object which is going to rewrite the files
        :return: void
        Adds the imports that are needed in the file since the refactorings
        """
        # if there are no imports in the class appends before the start of class
        import_line = f"import {self.target_package_name}.{self.target_class_name};\n"
        if len(klass.file_info.all_imports) == 0:
            tokens_info = TokensInfo(klass.parser_context)
            tokens_info.start -= len(klass.modifiers_parser_contexts) * 2
            tokens_info.stop += 1
            rewriter.insert_before_start(tokens_info, import_line)
            return

        # if however we have some imports append new import at the end of last import
        tokens_info = TokensInfo(klass.file_info.all_imports[-1].parser_context)
        tokens_info.stop += 1
        rewriter.insert_after(tokens_info, import_line)


def clean_up_dir(files: list) -> list:

    """
    :param files: List of files in the project directory
    :return: list

    Cleans up trashed files and gives original files
    """

    original_files = list()
    for file in files:
        if "rewritten.java" in file:
            os.remove(file)
        else:
            original_files.append(file)
    return original_files


if __name__ == '__main__':
    path = "/data/Dev/JavaSample/"
    my_list = get_filenames_in_dir(path)

    filtered = clean_up_dir(my_list)

    refactoring = MoveFieldRefactoring(filtered, 'my_package', 'Source', 'number', 'Target', 'my_package')

    result = refactoring.move()
    print(result)
