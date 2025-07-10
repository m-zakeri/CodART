from functools import reduce
from codart.cfg_generator.src.antlr.gen.JavaParser import JavaParser
from codart.cfg_generator.src.antlr.gen.JavaParserVisitor import JavaParserVisitor
from codart.cfg_generator.src.data_structures.graph.networkx_builder import NxDiGraphBuilder as DiGraphBuilder
from codart.cfg_generator.src.cfg_extractor.language_structure.digraph_embedder import DiGraphEmbedder

class CFGExtractorVisitor(JavaParserVisitor):
    """
    The class includes a method for each non-terminal (i.e., selection, iteration, jump and try-catch statements)
    Each method builds a part of a CFG rooted at its corresponding non-terminal.
    The extracted sub-graph is saved using the `networkx` library.
    visit() is the first method of the class which is invoked initially by the main.
    """

    def __init__(self):
        """
        `functions` is a dictionary to keep each function signature and its CFG reference.
        Each CFG is kept as a `networkx.DiGraph`.
        """
        self.Class = {}
        self.functions = {}
        self.functionLastNode = {}
        self.catches = []

    def visitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        """
        Visits a method declaration and extracts its information into the PDG.
        """
        gin = self.visit(ctx.methodBody())
        name = self.get_method_signature(ctx)
        print("\t\t" + name)

        graph, self.functionLastNode[name] = DiGraphEmbedder.embed_in_function(gin, self.catches)

        self.functions[name] = graph.build()
        self.catches = []
    def get_method_signature(self, ctx: JavaParser.MethodDeclarationContext) -> str:
        """
        Extracts the method signature including method name and parameter types/names, excluding return type.
        """
        # Get the method name
        method_name = self.visit(ctx.methodHeader().methodDeclarator())

        # Get the parameter list
        parameters = []
        if ctx.methodHeader().methodDeclarator().formalParameterList():
            for param in ctx.methodHeader().methodDeclarator().formalParameterList().formalParameter():
                param_type = self.get_type_from_context(param.unannType())
                param_name = param.variableDeclaratorId().Identifier().getText()
                parameters.append(f"{param_type} {param_name}")

        # Construct the method signature
        return f"{method_name}({', '.join(parameters)})"
    def get_type_from_context(self, ctx) -> str:
        """
        Extracts the type from the context node.
        """
        return ctx.getText()

    def visitMethodHeader(self, ctx: JavaParser.MethodHeaderContext):
        return self.visit(ctx.methodDeclarator())

    def visitMethodDeclarator(self, ctx: JavaParser.MethodDeclaratorContext):
        return ctx.Identifier().getText()

    def visitBlock(self, ctx: JavaParser.BlockContext):
        if ctx.blockStatements() is not None:
            return self.visit(ctx.blockStatements())

    def visitBlockStatements(self, ctx: JavaParser.BlockStatementsContext):
        gins = (self.visit(block) for block in ctx.blockStatement())
        return reduce(DiGraphEmbedder.merge, gins)

    def visitIfThenStatement(self, ctx: JavaParser.IfThenStatementContext):
        condition = ctx.expression()
        then_part = ctx.statement()
        then_part_graph = self.visit(then_part)
        return DiGraphEmbedder.embed_in_if(condition, then_part_graph)

    def visitIfThenElseStatement(self, ctx: JavaParser.IfThenElseStatementContext):
        condition = ctx.expression()
        then_part = ctx.statementNoShortIf()
        else_part = ctx.statement()
        then_part_graph = self.visit(then_part)
        else_part_graph = self.visit(else_part)
        return DiGraphEmbedder.embed_in_if_else(condition, then_part_graph, else_part_graph)

    def visitSwitchStatement(self, ctx: JavaParser.SwitchStatementContext):
        switcher = ctx.expression()
        case_labels, case_bodies = zip(*self.visit(ctx.switchBlock()))
        return DiGraphEmbedder.embed_in_switch_case(switcher, case_labels, case_bodies)

    def visitSwitchBlock(self, ctx: JavaParser.SwitchBlockContext):
        return [self.visit(switch_group) for switch_group in ctx.switchBlockStatementGroup()]

    def visitSwitchBlockStatementGroup(self, ctx: JavaParser.SwitchBlockStatementGroupContext):
        case = ctx.switchLabel()
        block_graph = self.visit(ctx.blockStatements())
        return case, block_graph

    def visitBasicForStatement(self, ctx: JavaParser.BasicForStatementContext):
        initializer = ctx.forInit()
        condition = ctx.expression()
        successor = ctx.forUpdate()
        body_graph = self.visit(ctx.statement())
        return DiGraphEmbedder.embed_in_for(condition, initializer, successor, body_graph)

    def visitWhileStatement(self, ctx: JavaParser.WhileStatementContext):
        condition = ctx.expression()
        body_graph = self.visit(ctx.statement())
        return DiGraphEmbedder.embed_in_while(condition, body_graph)

    def visitDoStatement(self, ctx: JavaParser.DoStatementContext):
        condition = ctx.expression()
        do_body = ctx.statement()
        do_body_graph = self.visit(do_body)
        return DiGraphEmbedder.embed_in_do_while(condition, do_body_graph)

    def visitTryStatement(self, ctx: JavaParser.TryStatementContext):
        try_body = self.visit(ctx.block())
        catch_exceptions, catch_bodies = zip(*self.visit(ctx.catches()))
        embeded_graph, self.catches = DiGraphEmbedder.embed_in_try_catch(try_body, catch_exceptions, catch_bodies)
        return embeded_graph

    def visitCatches(self, ctx: JavaParser.CatchesContext):
        return [self.visit(catches) for catches in ctx.catchClause() if catches]

    def visitCatchClause(self, ctx: JavaParser.CatchClauseContext):
        catch_body = self.visit(ctx.block())
        exception = ctx.catchFormalParameter().catchType().getText()
        return exception, catch_body

    # def visitFinallyBlock(self, ctx: JavaParser.FinallyBlockContext):
    #     return self.visit(ctx.block())

    def visitExpressionStatement(self, ctx: JavaParser.ExpressionStatementContext):
        return DiGraphBuilder().add_node(value=[ctx])

    def visitLocalVariableDeclarationStatement(self, ctx: JavaParser.LocalVariableDeclarationStatementContext):
        return DiGraphBuilder().add_node(value=[ctx])

    def visitBreakStatement(self, ctx: JavaParser.BreakStatementContext):
        return DiGraphBuilder().add_node(value=[ctx])

    def visitLocalVariableDeclaration(self, ctx: JavaParser.LocalVariableDeclarationContext):
        return DiGraphBuilder().add_node(value=[ctx])

    def visitContinueStatement(self, ctx: JavaParser.ContinueStatementContext):
        return DiGraphBuilder().add_node(value=[ctx])

    def visitThrowStatement(self, ctx: JavaParser.ThrowStatementContext):
        return DiGraphBuilder().add_node(value=[ctx])

    def visitReturnStatement(self, ctx: JavaParser.ReturnStatementContext):
        return DiGraphBuilder().add_node(value=[ctx])

    def visitEmptyStatement_(self, ctx: JavaParser.EmptyStatement_Context):
        return DiGraphBuilder().add_node(value=[ctx])
