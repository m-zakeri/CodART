"""
## Introduction

The module implements Move Class refactoring operation

## Pre and post-conditions

### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions

"""

__version__ = '0.1.0'
__author__ = 'Morteza Zakeri'

import os
os.add_dll_directory("C:\\Program Files\\SciTools\\bin\\pc-win64")

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.JavaParserLabeled import JavaParserLabeled
from codart.gen.JavaParserLabeledListener import JavaParserLabeledListener
from codart.symbol_table import parse_and_walk
from codart.learner.sbr_initializer.utils.utility import logger, config

ROOT_PACKAGE = "(Unnamed_Package)"


class UpdateImportsListener(JavaParserLabeledListener):
    """


    """

    def __init__(self, rewriter: TokenStreamRewriter, source_package: str, target_package: str, class_name: str):
        """


        """

        self.rewriter = rewriter
        self.source_package = source_package
        self.target_package = target_package
        self.class_name = class_name
        self.current_package = None

        self.imported = False
        self.import_loc = None

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.current_package = ctx.qualifiedName().getText()

    def exitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.import_loc = ctx.stop

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        # import source_package.Sample;
        if self.target_package in ctx.getText():
            self.imported = True
            if self.class_name in ctx.getText():
                if self.target_package == self.current_package:
                    replace_text = ""
                else:
                    replace_text = f"\nimport {self.target_package}.{self.class_name};\n"

                self.rewriter.replaceRangeTokens(
                    from_token=ctx.start,
                    to_token=ctx.stop,
                    text=replace_text,
                    program_name=self.rewriter.DEFAULT_PROGRAM_NAME
                )
        elif f"{self.source_package}.{self.class_name}" in ctx.getText():
            self.rewriter.delete(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex
            )

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        if not self.imported and self.current_package != self.target_package:
            self.rewriter.insertAfterToken(
                token=self.import_loc,
                text=f"\nimport {self.target_package}.{self.class_name};\n",
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME
            )


class MoveClassAPI:
    def __init__(self, udb_path: str, source_package: str, target_package: str, class_name: str, project_path: str):
        self.udb_path = udb_path
        self.source_package = source_package
        self.target_package = target_package
        self.class_name = class_name
        self.project_path = os.path.normpath(project_path)

        self.source_package_dir = None
        self.target_package_dir = None
        self._class_current_path = None
        self.class_content = None
        self.usages = None
        self._class_new_path = None

    def check_preconditions(self) -> bool:
        if self.source_package == self.target_package:
            print("Error: Source and target packages are the same.")
            return False

        if self.source_package == ROOT_PACKAGE or self.target_package == ROOT_PACKAGE:
            print("Error: Cannot move package to/from root package.")
            return False

        # Get package directories
        source_package_dir, target_package_dir = self.get_package_directories()
        if source_package_dir is None or target_package_dir is None:
            print("Error: Package does not exist.")
            return False

        # Normalize paths for comparison
        source_package_dir = os.path.normpath(source_package_dir)
        target_package_dir = os.path.normpath(target_package_dir)

        # Check if project_path is a parent directory of the package directories
        if not target_package_dir.startswith(self.project_path):
            print(f"Error: Target package path {target_package_dir} cannot be resolved.")
            return False

        if not source_package_dir.startswith(self.project_path):
            print(f"Error: Source package path {source_package_dir} cannot be resolved.")
            return False

        class_full_path = os.path.join(source_package_dir, f"{self.class_name}.java")
        if not os.path.exists(class_full_path):
            print(f'Error: Class "{self.class_name}" does not exist in source package "{source_package_dir}".')
            return False

        # Get class directory
        class_path, class_content, usages = self.get_class_info()
        if class_path is None or class_content is None:
            print("Error: Class does not exist.")
            return False

        class_new_path = os.path.join(target_package_dir, f"{self.class_name}.java")
        if os.path.exists(class_new_path):
            print("Error: Class already exists in target package.")
            return False

        self.source_package_dir = source_package_dir
        self.target_package_dir = target_package_dir
        self._class_current_path = class_path
        self.class_content = class_content
        self.usages = usages
        self._class_new_path = class_new_path

        return True
    def get_package_directories(self):
        db = und.open(self.udb_path)
        source_package_path = None
        target_package_path = None
        packages = db.ents("Java Package")
        for ent_ in packages:
            if ent_.longname() == self.source_package:
                if ent_.parent() is not None:
                    name_ = ent_.parent().longname()
                    if os.path.exists(name_):
                        source_package_path = os.path.dirname(name_)
                        break

        for ent_ in packages:
            if ent_.longname() == self.target_package:
                if ent_.parent() is not None:
                    name_ = ent_.parent().longname()
                    if os.path.exists(name_):
                        target_package_path = os.path.dirname(name_)
                        break

        db.close()
        return source_package_path, target_package_path

    def get_class_info(self):
        db = und.open(self.udb_path)
        class_path = None
        class_contents = None
        usages = set()

        classes = db.ents("Class ~Unresolved ~Unknown ~Anonymous")
        for ent_ in classes:
            simple_name = ent_.simplename()
            if simple_name == self.class_name and class_path is None and ent_.parent() is not None:
                class_contents = ent_.contents()
                class_path = ent_.parent().longname()

                for ref_ in ent_.refs():
                    if ref_.file().simplename() != f"{simple_name}.java":
                        usages.add(ref_.file().longname())
                break
        db.close()
        return class_path, class_contents, usages

    def do_refactor(self):
        if not self.check_preconditions():
            config.logger.error("Pre conditions failed.")
            return False

        # Update usages
        for file_path in self.usages:
            parse_and_walk(
                file_path=file_path,
                listener_class=UpdateImportsListener,
                has_write=True,
                source_package=self.source_package,
                target_package=self.target_package,
                class_name=self.class_name
            )

        # Delete source class
        # config.logger.debug(f'Current class path to be removed: {self._class_current_path}')
        os.remove(self._class_current_path)

        # Write the new class
        package = ""
        if self.target_package != ROOT_PACKAGE:
            package = f"package {self.target_package};\n"
        imports = ""
        if self.source_package != ROOT_PACKAGE:
            imports = f"import {self.source_package}.*;\n"

        # logger.debug(f'New class path to be added: {self._class_new_path}')
        with open(self._class_new_path, mode='w', encoding='utf8', errors='ignore') as f:
            f.write(package + imports + self.class_content)

        return True


def main(udb_path: str, source_package: str, target_package: str, class_name: str, project_path: str, *args, **kwargs):
    """
    The main API for Move Class refactoring
    """
    move_class = MoveClassAPI(udb_path, source_package, target_package, class_name, project_path)
    res = move_class.do_refactor()
    return res


# Tests
# def test2():
#     res = main(
#         udb_path="C:/Users/Lenovo/Desktop/sample_project/sample_project.und",
#         project_path="C:/Users/Lenovo/Desktop/sample_project",
#         class_name="HelperClass",
#         source_package="net.example.utils",
#         target_package="net.example.main"
#     )
#     print(res)
#     assert res


if __name__ == '__main__':
    main(
        udb_path="C:/Users/Lenovo/Desktop/sample_project/sample_project.und",
        project_path="C:/Users/Lenovo/Desktop/sample_project",
        class_name="HelperClass",
        source_package="net.example.utils",
        target_package="net.example.main"
        # C:\Users\Lenovo\Desktop\sample_project\net\example\main
    )