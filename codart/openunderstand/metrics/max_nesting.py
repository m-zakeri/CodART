from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MaxNesting(JavaParserLabeledListener):
    def __init__(self):
        self.stack = []
        self.max_nesting = 0
        self.is_in_else_if = False
        self.number_of_else_if = 0

    def push_to_stack(self):
        self.stack.append(0)
        if len(self.stack) > self.max_nesting:
            self.max_nesting = len(self.stack)

    def pop_from_stack(self):
        self.stack.pop()

    # if statement
    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        self.push_to_stack()
        # i=0
        # for child in ctx.children:
        #     i += 1
        #     if(child.getText()=="else"):
        #         try:
        #             if(ctx.children[1].children[0].getText()=="if"):
        #                 self.number_of_else_if+=1
        #                 self.is_in_else_if=True
        #         except:
        #             x=0

    # if statement
    def exitStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        self.pop_from_stack()

    # while statement
    def enterStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        self.push_to_stack()

    # while statement
    def exitStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        self.pop_from_stack()

    # do while statement
    def enterStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        self.push_to_stack()

    # do while statement
    def exitStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        self.pop_from_stack()

    # for statement
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        self.push_to_stack()

    # for statement
    def exitStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        self.pop_from_stack()

    # switch case statement
    def enterStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.push_to_stack()

    # switch case statement
    def exitStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.pop_from_stack()
