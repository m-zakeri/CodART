import os

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer


# This is the class for detecting all of the types.
class DetectCodeClass(JavaParserLabeledListener):
    def __init__(self):
        self.Variables = []
        self.Fields = []
        self.MethodParameters = []
        self.Methods = []
        self.Classes = []

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        self.Variables.append(str(ctx.variableDeclaratorId().IDENTIFIER()))

    def exitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        pass

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.Methods.append(str(ctx.IDENTIFIER()))
        self.MethodParameters.append(str(ctx.formalParameters()))

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        pass

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.Classes.append(str(ctx.IDENTIFIER()))

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        pass


# This is the class for detecting dead codes.
class DetectDeadCodeClass(JavaParserLabeledListener):
    def __init__(self):
        self.DeadVariables = []
        self.DeadMethodParameters = []
        self.Fields = []
        self.DeadMethods = []
        self.DeadClasses = []

    pass


# This is the class to remove dead codes.
class RemoveDeadCodeClass(JavaParserLabeledListener):
    def __init__(self, Tokens: CommonTokenStream = None, Identifier: {} = None):
        self.Class = False
        self.Method = False
        self.Field = False
        self.Variable = False
        self.Parameter = False

        self.Classes = Identifier["Classes"]
        self.ClassIndex = 0

        self.Methods = Identifier["Methods"]
        self.MethodIndex = 0
        self.IsSourceClassForMethods = [None] * len(self.Methods)

        self.Fields = Identifier["Fields"]
        self.FieldIndex = 0
        self.IsSourceClassForFields = [None] * len(self.Fields)

        self.Variables = Identifier["Variables"]
        self.VariableIndex = 0
        self.IsSourceClassForVariables = [None] * len(self.Variables)
        self.IsSourceMethodForVariables = [None] * len(self.Variables)

        self.Parameters = Identifier["Parameters"]
        self.ParameterIndex = 0
        self.IsSourceClassForParameters = [None] * len(self.Parameters)
        self.IsSourceMethodForParameters = [None] * len(self.Parameters)

        if len(Identifier["Classes"]) != 0:
            self.Class = True

        if len(Identifier["Methods"]) != 0:
            self.Method = True

        if len(Identifier["Fields"]) != 0:
            self.Field = True
        if len(Identifier["Variables"]) != 0:
            self.Variable = True

        if len(Identifier["Parameters"]) != 0:
            self.Parameter = True

        if Tokens is not None:
            self.CodeRewrite = TokenStreamRewriter(Tokens)
        else:
            raise TypeError('Tokens is None')

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        classIdentifier = ctx.IDENTIFIER().getText()
        ctxParent = ctx.parentCtx
        if self.Method:
            for i in range(len(self.Methods)):
                if self.Methods[i].split('/')[0] == classIdentifier:
                    self.IsSourceClassForMethods[i] = True

        if self.Field:
            for i in range(len(self.Fields)):
                if self.Fields[i].split('/')[0] == classIdentifier:
                    self.IsSourceClassForFields[i] = True

        if self.Variable:
            for i in range(len(self.Variables)):
                if self.Variables[i].split('/')[0] == classIdentifier:
                    self.IsSourceClassForVariables[i] = True

        if self.Parameter:
            for i in range(len(self.Parameters)):
                if self.Parameters[i].split('/')[0] == classIdentifier:
                    self.IsSourceClassForParameters[i] = True

        if self.Class and self.ClassIndex < len(self.Classes) and self.Classes[self.ClassIndex] == classIdentifier:
            startIndex = ctxParent.start.tokenIndex
            stopIndex = ctxParent.stop.tokenIndex

            self.CodeRewrite.delete(
                self.CodeRewrite.DEFAULT_PROGRAM_NAME,
                startIndex,
                stopIndex
            )
            self.ClassIndex += 1

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        pass

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        methodIdentifier = ctx.IDENTIFIER().getText()
        if self.Variable:
            for i in range(len(self.Variables)):
                if self.IsSourceClassForVariables[i] and self.Variables[i].split('/')[1] == methodIdentifier:
                    self.IsSourceMethodForVariables[i] = True

        if self.Parameter:
            for i in range(len(self.Parameters)):
                if self.IsSourceClassForParameters[i] and self.Parameters[i].split('/')[1] == methodIdentifier:
                    self.IsSourceMethodForParameters[i] = True
        pass

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        grandParentCtx = ctx.parentCtx.parentCtx
        methodIdentifier = ctx.IDENTIFIER().getText()
        if self.Method and self.MethodIndex < len(self.Methods) and self.Methods[self.MethodIndex].split('/')[
            1] == methodIdentifier:
            if self.IsSourceClassForMethods[self.MethodIndex]:
                self.CodeRewrite.delete(
                    self.CodeRewrite.DEFAULT_PROGRAM_NAME,
                    grandParentCtx.start.tokenIndex,
                    grandParentCtx.stop.tokenIndex
                )
                self.MethodIndex += 1

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        pass

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        fieldIdentifier = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        grandParentCtx = ctx.parentCtx.parentCtx

        if self.Field and self.FieldIndex < len(self.Fields) and self.Fields[self.FieldIndex].split('/')[
            1] == fieldIdentifier:
            if self.IsSourceClassForFields[self.FieldIndex]:
                self.CodeRewrite.delete(
                    self.CodeRewrite.DEFAULT_PROGRAM_NAME,
                    grandParentCtx.start.tokenIndex,
                    grandParentCtx.stop.tokenIndex
                )
                self.FieldIndex += 1

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        pass

    def exitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        variableIdentifier = ctx.variableDeclaratorId().IDENTIFIER().getText()
        grandParentCtx = ctx.parentCtx.parentCtx.parentCtx
        if self.Variable and self.VariableIndex < len(self.Variables) and self.Variables[self.VariableIndex].split('/')[2] == variableIdentifier:
            if self.IsSourceClassForVariables[self.VariableIndex] and self.IsSourceMethodForVariables[
                self.VariableIndex]:
                self.CodeRewrite.delete(
                    self.CodeRewrite.DEFAULT_PROGRAM_NAME,
                    grandParentCtx.start.tokenIndex,
                    grandParentCtx.stop.tokenIndex
                )
                self.VariableIndex += 1

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        pass

    def exitFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        parameterIdentifier = ctx.variableDeclaratorId().IDENTIFIER().getText()
        grandParentCtx = ctx
        Parent = ctx.parentCtx.children
        # for i in range(len(Parent)):
        #     print(Parent[i].variableDeclaratorId().IDENTIFIER().getText())

        start = grandParentCtx.start.tokenIndex
        stop = grandParentCtx.stop.tokenIndex
        if self.Parameter and self.ParameterIndex < len(self.Parameters) and self.Parameters[self.ParameterIndex].split('/')[2] == parameterIdentifier:
            if self.IsSourceClassForParameters[self.ParameterIndex] and self.IsSourceMethodForParameters[
                self.ParameterIndex]:
                self.CodeRewrite.delete(
                    self.CodeRewrite.DEFAULT_PROGRAM_NAME,
                    start,
                    stop
                )
                self.ParameterIndex += 1

    def enterMethodCall0(self, ctx:JavaParserLabeled.MethodCall0Context):
        parametersList = ctx.expressionList()
        # print(parametersList.parentCtx.IDENTIFIER().getText())
        if self.Parameter and parametersList.parentCtx.IDENTIFIER().getText() in self.Parameters:
            pass

    def exitMethodCall0(self, ctx:JavaParserLabeled.MethodCall0Context):
        pass


def main():
    Path = "../tests/remove_dead_code"
    FolderPath = os.listdir(Path)

    Identifier = [
        {"Classes": ["Airplane"],
                   "Methods": ["Car/Fly", "Engine/main2"],
                   "Fields": ["Car/noway", "Engine/model"],
                   "Variables": [],
                   "Parameters": []},

        {"Classes": [],
                   "Methods": [],
                   "Fields": [],
                   "Variables": ["Car/main/dead", "Car/Run/number", "Engine/SetName/what",
                                 "Engine/main2/variable", "Engine/main2/dead"],
                   "Parameters": ["Car/Drive/wheels", "Engine/main/k", "Engine/SetName/last"]},

        {"Classes": ["Airplane"],
                   "Methods": ["Car/Fly", "Engine/main2"],
                   "Fields": ["Car/noway", "Engine/model"],
                   "Variables": ["Car/main/dead", "Car/Run/number", "Engine/SetName/what",
                                 "Engine/main2/variable", "Engine/main2/dead"],
                   "Parameters": ["Car/Drive/wheels", "Engine/main/k", "Engine/SetName/last"]}
                  ]

    i = 0
    for File in FolderPath:
        # We have all of the java files in this folder now
        if File.endswith('.java'):
            EachFilePath = Path + "\\" + File
            # Step 1: Load input source into stream
            EachFile = FileStream(str(EachFilePath))

            # Step 2: Create an instance of AssignmentStLexer
            Lexer = JavaLexer(EachFile)

            # Step 3: Convert the input source into a list of tokens
            TokenStream = CommonTokenStream(Lexer)

            # Step 4: Create an instance of the AssignmentStParser
            Parser = JavaParserLabeled(TokenStream)

            # Step 5: Create parse tree
            Tree = Parser.compilationUnit()

            # ListenerForDetection = DetectCodeClass()
            # ListenerForDeadCodeDetection = DetectDeadCodeClass()

            if i < len(Identifier):
                # This is a new Java file which is the result
                Refactored = open(os.path.join(Path, File + "_Refactored.java"), mode='w', newline='')

                # Step 6: Create an instance of AssignmentStListener
                ListenerForRemovingDeadCode = RemoveDeadCodeClass(TokenStream, Identifier[i])

                Walker = ParseTreeWalker()

                # Walk
                # Walker.walk(Listener, Tree)
                # Walker.walk(ListenerOnMainCode, Tree)

                Walker.walk(ListenerForRemovingDeadCode, Tree)

                NewCode = str(ListenerForRemovingDeadCode.CodeRewrite.getDefaultText())
                Refactored.write(NewCode)
            i += 1


if __name__ == "__main__":
    main()
