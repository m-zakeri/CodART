from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
import os
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

import ntpath
switches = []
switch_type = ""
variables = []
notfound = []
methods = []
returntype = []
clas = []
found_class = []
found_func = []
params = ""

class ReplaceConditionalWithPolymorphism(JavaParserLabeledListener):

    def __init__(self, file_path: str, class_name: str, method_name: str):

        self.found_class = False
        self.found_func = False
        if file_path is None:
            self.file = "../tests/replace_conditional_with_polymorphism/sample.java"
        else:
            self.file = file_path
        if class_name is None:
            self.class_name = "SwitchDemo"
        else:
            self.class_name = class_name
        if method_name is None:
            self.method_name = "myMethod"
        else:
            self.method_name = method_name

    def get_java_files(directory):
        """
        A generator that gives you all java files (*.java) in a specific directory.
        :param directory: The directory's absolute path you want to traverse.
        :return: Yields a *.java that exists in the directory
        """
        if not os.path.isdir(directory):
            raise ValueError("directory should be an absolute path of a directory!")
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.split('.')[-1] == 'java':
                    yield os.path.join(root, file)

    def enterSwitchBlockStatementGroup(self, ctx: JavaParserLabeled.SwitchBlockStatementGroupContext):
        switches.append(ctx.getText())
        notfound.append("doo")

    def enterVariableDeclarators(self, ctx:JavaParserLabeled.VariableDeclaratorsContext):
        if len(notfound) == 0:
            variables.append(ctx.getText().split('=')[0])

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        methods.append(f"{ctx.IDENTIFIER()} ")

        returntype.append(ctx.typeTypeOrVoid().getText())
        if ctx.IDENTIFIER().getText() == self.method_name:
            found_func.append(ctx.IDENTIFIER())

    def enterFormalParameter(self, ctx:JavaParserLabeled.FormalParameterList0Context):
        global params
        params=ctx.getText()
        if "String" in params:
            params=params.replace("String", " String ")

        if "int" in params:
            params=params.replace("int", " int ")

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        clas.append(ctx.getText())
        if ctx.IDENTIFIER().getText() == self.class_name:

            found_class.append(ctx.IDENTIFIER().getText())


if __name__ == '__main__':
    listener = ReplaceConditionalWithPolymorphism("../tests/replace_conditional_with_polymorphism/sample.java",
                                                  "SwitchDemo", "myMethod")
    try:
        stream = FileStream(listener.file)
    except:
        print("Path not found")
        pass
    classname = listener.class_name
    func = listener.method_name
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()
    walker = ParseTreeWalker()
    walker.walk(
        listener=listener,
        t=tree
    )
    token = lexer.reset()
    if len(found_class)>0 and len(found_func) > 0:
        token = lexer.nextToken()
        not_switch = True
        opening = ""
        whole = ""
        while token.type != Token.EOF:
            if not_switch:
                if token.type != lexer.SWITCH:
                    opening += token.text
            if token.type == lexer.SWITCH:
                not_switch = False
                token = lexer.nextToken()
                while token.type == lexer.LPAREN or token.type == lexer.WS:
                    token = lexer.nextToken()
                switch_type = token.text.rstrip("\n")
            token = lexer.nextToken()
       # print(f"swich_type : {switch_type} , cases : {switches} , variables : {variables} , mehthod: {methods} , return : {returntype[0]}")
        #print(opening)
        # answer = open('../tests/replace_conditional_with_polymorphism/test_results.java', 'w')
        first = str(clas[0])
        second = "switch(mnth){"
        for i in switches:
            second += i
        second += '}'
        ind = first.find("switch")
        sw = first[0:ind]
        val = "default"
        try:
            f = sw.rfind(switch_type + '=')

            sw = sw.split('=')
            o = sw[1].find(';')
            val = sw[1][0:o]
            # print(val)

        except:
            val = "default"

        first = first[ind:]
        last = first.replace(second, "")
        lcl = " {" + '\n' + '\t' + '\t' + '\t'
        last = last.replace('{', lcl)
        lcl = " ;" + '\n' + '\t' + '\t'
        last = last.replace(';', lcl)
        lcl = "}" + '\n' + '\t' + '\t' + '\t'
        last = last.replace('}', lcl)
        lcl = " ) "
        last = last.replace(')', lcl)
        lcl = " ( "
        last = last.replace('(', lcl)
        if "int" in last:
            last = last.replace("int", " int ")
        if "String" in last:
            last = last.replace("String", " String ")
        if "return" in last:
            last.replace("return", " return ") \
                # print(last)
        opening += classname + "_" + val + " chosen = " "new " + classname + "_" + val + "()" + '\n' + '\t' + '\t'
        opening += "chosen." + func + "(this);" + '\n' + '\t' + '\t' + last
        # print(opening)
        # answer.write(opening)
        #opening.rstrip("\n")
        ii = len(opening)
        cnt = 0
        while cnt < 2:
            ii -= 1
            if opening[ii] == '}':
                cnt += 1
                ii -= 1

        #print(opening[0:ii]+'}'+'\n'+'}'+'\n')
        whole += opening[0:ii]+'}'+'\n'+'}'+'\n'
        # answer.write("abstract class " + "parent" + classname + '\n' + '{' + '\n')
        whole += "abstract class " + "parent" + classname + '\n' + '{' + '\n'
        # answer.write('\t' + "public " + "parent" + classname + "()" + '{' + '\n' + '\t' + '}' + '\n')
        whole +='\t' + "public " + "parent" + classname + "()" + '{' + '\n' + '\t' + '}' + '\n'
        method_type = "void"
        if 'return' in switches[0]:
            method_type = returntype[0]
        # answer.write('\t' + "abstract public " + method_type + " " + func + "(" + classname + ' input_class ' + ") ;" + '\n' + "}")
        whole += '\t' + "abstract public " + method_type + " " + func + "(" + classname + ' input_class '+ "," +params + ") ;" + '\n' + "}"
        for case in switches:
            # answer.write('\n')
            whole += '\n'
            ar = case.split(':')
            if "case" in ar[0]:
                ar[0] = ar[0].removeprefix("case")
            # answer.write("class " + classname + "_" + ar[0] + " extends parent" + classname + '\n' + '{' + '\n')
            whole += "class " + classname + "_" + ar[0] + " extends parent" + classname + '\n' + '{' + '\n'
            # answer.write('\t' + "public " + classname + "_" + ar[0] + "()" + '{' + '\n' + '\t' + '}' + '\n')
            whole += '\t' + "public " + classname + "_" + ar[0] + "()" + '{' + '\n' + '\t' + '}' + '\n'
            # answer.write('\t' + "public " + returntype[0] + " " + func + "(" + classname + ' input_class ' + ") {" + '\n')
            whole += '\t' + "public " + returntype[0] + " " + func + "(" + classname + ' input_class '+','+params + ") {" + '\n'
            index = case.find(':')
            rp = " {" + '\n' + '\t' + '\t' + '\t'
            case = case.replace('{', rp)
            rp = " ;" + '\n' + '\t' + '\t'
            case = case.replace(';', rp)
            rp = "}" + '\n' + '\t' + '\t' + '\t'
            case = case.replace('}', rp)
            rp = " ) "
            case = case.replace(')', rp)
            rp = " ( "
            case = case.replace('(', rp)
            rp = " % "
            case = case.replace('%', rp)
            if "String" in case:
                case = case.replace("String", " String ")
            if "int" in case:
                case=case.replace("int", " int ")
            blue=case

            if "return" in case:
                rr = case.find("return")
                blue = case[0:rr]+" return "+ case[rr+6:]
                #print(blue)

            case = blue

            for i in variables:
                if i in case and len(i) != 1:
                    case = case.replace(i, "input_class." + i)

            if "this." in case:
                case = case.replace("this.", " ")
            # answer.write('\t' + '\t' + case[index + 1:-1] + '\n' + '\t' + '}' + '\n' + '}')
            whole += '\t' + '\t' + case[index + 1:-1] + '\n' + '\t' + '}' + '\n' + '}'
            #print(whole)
            answer = open('../tests/replace_conditional_with_polymorphism/test_results.java', 'w')
            answer.write(whole)
            answer.close()

#fixed some issues like failure in recognizing some syntax in cases and replacing them.
#a few issues are stil remaining for ohase 3 due to complexity of homework,multiple exams and shortage of time