from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer

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


class ClassNameListener(JavaParserLabeledListener):

    def enterSwitchBlockStatementGroup(self, ctx: JavaParserLabeled.SwitchBlockStatementGroupContext):
        switches.append(ctx.getText())
        notfound.append("doo")

    def enterVariableDeclarators(self, ctx:JavaParserLabeled.VariableDeclaratorsContext):
        if len(notfound) == 0:
            variables.append(ctx.getText().split('=')[0])

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        methods.append(f"{ctx.IDENTIFIER()} ")
        returntype.append(ctx.typeTypeOrVoid().getText())

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        clas.append(ctx.getText())


if __name__ == '__main__':
    stream = FileStream("../tests/replace_conditional_with_polymorphism/sample.java")
    classname = "SwitchDemo"
    func = "myMethod"
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()
    listener = ClassNameListener()
    walker = ParseTreeWalker()
    walker.walk(
        listener=listener,
        t=tree
    )
    token = lexer.reset()
    token = lexer.nextToken()
    not_switch = True
    opening = ""
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
    #print(f"swich_type : {switch_type} , cases : {switches} , variables : {variables} , mehthod: {methods} , return : {returntype[0]}")
    #print(opening)
    answer = open('../tests/replace_conditional_with_polymorphism/test_results', 'w')
    first = str(clas[0])
    second = "switch(mnth){"
    for i in switches:
        second +=i
    second += '}'
    ind = first.find("switch")
    sw = first[0:ind]
    val = "default"
    try:
        f = sw.rfind(switch_type+'=')

        sw = sw.split('=')
        o = sw[1].find(';')
        val = sw[1][0:o]
        #print(val)

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
    if "return" in last:
        last.replace("return", " return ")\
    #print(last)
    opening += classname+"_"+val + " chosen = " "new "+classname+"_"+val+"()"+'\n'+'\t'+'\t'
    opening += "chosen."+func+"(this);"+'\n'+'\t'+'\t'+last
    answer.write(opening)
    answer.write("abstract class " + "parent" + classname + '\n' + '{' + '\n')
    answer.write('\t'+"public " + "parent" + classname + "()" + '{' + '\n' + '\t' + '}' + '\n')

    method_type = "void"
    if 'return' in switches[0]:
        method_type = returntype[0]
    answer.write('\t' + "abstract public "+method_type+" "+ func + "(" + classname + ' input_class ' + ") ;" + '\n'+"}")

    for case in switches:
        answer.write('\n')
        ar = case.split(':')
        if "case" in ar[0]:
            ar[0] = ar[0].removeprefix("case")
        answer.write("class "+classname+"_"+ar[0]+" extends parent"+classname+'\n'+'{'+'\n')
        answer.write('\t'+"public " + classname+"_"+ar[0] + "()" + '{' + '\n' + '\t' + '}' + '\n')

        answer.write('\t'+"public "+returntype[0]+" "+func+"("+classname+' input_class '+") {"+'\n')
        index = case.find(':')
        rp = " {" + '\n'+'\t'+'\t'+'\t'
        case = case.replace('{', rp)
        rp = " ;" + '\n'+'\t'+'\t'
        case = case.replace(';', rp)
        rp = "}" + '\n'+'\t'+'\t'+'\t'
        case = case.replace('}', rp)
        rp = " ) "
        case = case.replace(')', rp)
        rp = " ( "
        case = case.replace('(', rp)
        rp = " % "
        case = case.replace('%', rp)

        for i in variables:
            if i in case:
                case = case.replace(i, "input_class."+i)

        if "this." in case:
            case = case.replace("this.", " ")
        answer.write('\t'+'\t'+case[index+1:-1]+'\n'+'\t'+'}'+'\n'+'}')