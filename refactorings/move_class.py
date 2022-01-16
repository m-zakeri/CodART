import logging
import os

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from refactorings.utils.utils2 import parse_and_walk

try:
    import understand as und
except ImportError as e:
    print(e)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)

ROOT_PACKAGE = "(Unnamed_Package)"


class UpdateImportsListener(JavaParserLabeledListener):
    def __init__(self, rewriter: TokenStreamRewriter, source_package: str, target_package: str, class_name: str):
        self.rewriter = rewriter
        self.source_package = source_package
        self.target_package = target_package
        self.class_name = class_name
        self.current_package = None

        self.imported = False
        self.import_loc = None

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.current_package = ctx.qualifiedName().getText()

    def exitPackageDeclaration(self, ctx:JavaParserLabeled.PackageDeclarationContext):
        self.import_loc = ctx.stop

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        # import source_package.Sample;
        if self.target_package in ctx.getText():
            self.imported = True
            if self.class_name in ctx.getText():
                if self.target_package == self.current_package:
                    replace_text = ""
                else:
                    replace_text = f"import {self.target_package}.{self.class_name};\n"

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

    def exitCompilationUnit(self, ctx:JavaParserLabeled.CompilationUnitContext):
        if not self.imported and self.current_package != self.target_package:
            self.rewriter.insertAfterToken(
                token=self.import_loc,
                text=f"\nimport {self.target_package}.{self.class_name};\n",
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME
            )


class MoveClassAPI:
    def __init__(self, udb_path: str, source_package: str, target_package: str, class_name: str):
        self.udb_path = udb_path
        self.source_package = source_package
        self.target_package = target_package
        self.class_name = class_name

        self.source_package_dir = None
        self.target_package_dir = None
        self.class_dir = None
        self.class_content = None
        self.usages = None
        self.new_class_path = None

    def check_preconditions(self) -> bool:
        if self.source_package == self.target_package:
            logger.error("Source and target packages are same.")
            return False

        if self.source_package == ROOT_PACKAGE or self.target_package == ROOT_PACKAGE:
            logger.error("Can not move package to/from root package.")
            return False

        # Get package directories
        source_package_dir, target_package_dir = self.get_package_directories()
        if source_package_dir is None or target_package_dir is None:
            logger.error("Package entity does not exists.")
            return False

        if not os.path.exists(os.path.join(source_package_dir, f"{self.class_name}.java")):
            logger.error("Class does not exists in source package.")
            return False

        # Get class directory
        class_dir, class_content, usages = self.get_class_info()
        if class_dir is None or class_content is None:
            logger.error("Class entity does not exists.")
            return False

        new_class_path = os.path.join(target_package_dir, f"{self.class_name}.java")
        if os.path.exists(new_class_path):
            logger.error("Class already exists in target package.")
            return False

        self.source_package_dir = source_package_dir
        self.target_package_dir = target_package_dir
        self.class_dir = class_dir
        self.class_content = class_content
        self.usages = usages
        self.new_class_path = new_class_path

        return True

    def get_package_directories(self):
        db = und.open(self.udb_path)
        sp = None
        tp = None
        for ent in db.ents("Package"):
            long_name = ent.longname()
            if long_name == self.source_package and sp is None:
                sp = os.path.dirname(ent.parent().longname())
            if long_name == self.target_package and tp is None:
                tp = os.path.dirname(ent.parent().longname())
        db.close()
        return sp, tp

    def get_class_info(self):
        db = und.open(self.udb_path)
        class_path = None
        class_contents = None
        usages = set()

        for ent in db.ents("Class"):
            simple_name = ent.simplename()
            if simple_name == self.class_name and class_path is None:
                class_contents = ent.contents()
                class_path = ent.parent().longname()

                for ref in ent.refs():
                    if ref.file().simplename() != f"{simple_name}.java":
                        usages.add(ref.file().longname())
                break
        db.close()
        return class_path, class_contents, usages

    def do_refactor(self):
        if not self.check_preconditions():
            logger.error("Pre conditions failed.")
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
        os.remove(self.class_dir)

        # Write the new class
        with open(self.new_class_path, 'w') as f:
            package = ""
            if self.target_package != ROOT_PACKAGE:
                package = f"package {self.target_package};\n\n"
            imports = ""
            if self.source_package != ROOT_PACKAGE:
                imports = f"import {self.source_package}.*;\n\n"

            f.write(package + imports + self.class_content)

        return True


def main(udb_path: str, source_package: str, target_package: str, class_name: str, *args, **kwargs):
    return MoveClassAPI(
        udb_path, source_package, target_package, class_name
    ).do_refactor()


if __name__ == '__main__':
    main(
        udb_path="D:\\Dev\\JavaSample\\JavaSample\\JavaSample.und",
        class_name="Sample",
        source_package="source_package",
        target_package="target_package",  # "(Unnamed_Package)"
    )
