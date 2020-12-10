from antlr4_java9.Java9Parser import *
from antlr4_java9.Java9Listener import *

class UtilsListener(Java9Listener):
    package_name = None

    current_class_identifier = None
    current_class_identifier_temp = None
    nest_count = 0

    def enterPackageDeclaration(self, ctx:Java9Parser.PackageDeclarationContext):
        print(ctx.packageName().getText())
        self.package_name = ctx.packageName().getText()

    def enterNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        print(ctx.identifier().getText())
        if self.current_class_identifier is None and self.nest_count == 0:
            self.current_class_identifier = ctx.identifier().getText()
        else:
            if self.nest_count == 0:
                self.current_class_identifier_temp = self.current_class_identifier
                self.current_class_identifier = None
            self.nest_count += 1

    def exitNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        if self.current_class_identifier is not None:
            if self.nest_count > 0:
                self.nest_count -= 1
                if self.nest_count == 0:
                    self.current_class_identifier = self.current_class_identifier_temp
                    self.current_class_identifier_temp = None
            else:
                self.current_class_identifier = None
