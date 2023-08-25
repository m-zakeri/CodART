# Generated from JavaLabeledParser.g4 by ANTLR 4.9.3
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .JavaLabeledParser import JavaLabeledParser
else:
    from JavaLabeledParser import JavaLabeledParser

# This class defines a complete generic visitor for a parse tree produced by JavaLabeledParser.


class JavaLabeledParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JavaLabeledParser#compilationUnit.
    def visitCompilationUnit(self, ctx: JavaLabeledParser.CompilationUnitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#packageDeclaration.
    def visitPackageDeclaration(self, ctx: JavaLabeledParser.PackageDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#importDeclaration.
    def visitImportDeclaration(self, ctx: JavaLabeledParser.ImportDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx: JavaLabeledParser.TypeDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#modifier.
    def visitModifier(self, ctx: JavaLabeledParser.ModifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classOrInterfaceModifier.
    def visitClassOrInterfaceModifier(
        self, ctx: JavaLabeledParser.ClassOrInterfaceModifierContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#variableModifier.
    def visitVariableModifier(self, ctx: JavaLabeledParser.VariableModifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classDeclaration.
    def visitClassDeclaration(self, ctx: JavaLabeledParser.ClassDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeParameters.
    def visitTypeParameters(self, ctx: JavaLabeledParser.TypeParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeParameter.
    def visitTypeParameter(self, ctx: JavaLabeledParser.TypeParameterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeBound.
    def visitTypeBound(self, ctx: JavaLabeledParser.TypeBoundContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx: JavaLabeledParser.EnumDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#enumConstants.
    def visitEnumConstants(self, ctx: JavaLabeledParser.EnumConstantsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#enumConstant.
    def visitEnumConstant(self, ctx: JavaLabeledParser.EnumConstantContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#enumBodyDeclarations.
    def visitEnumBodyDeclarations(
        self, ctx: JavaLabeledParser.EnumBodyDeclarationsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceDeclaration.
    def visitInterfaceDeclaration(
        self, ctx: JavaLabeledParser.InterfaceDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classBody.
    def visitClassBody(self, ctx: JavaLabeledParser.ClassBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceBody.
    def visitInterfaceBody(self, ctx: JavaLabeledParser.InterfaceBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classBodyDeclaration0.
    def visitClassBodyDeclaration0(
        self, ctx: JavaLabeledParser.ClassBodyDeclaration0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classBodyDeclaration1.
    def visitClassBodyDeclaration1(
        self, ctx: JavaLabeledParser.ClassBodyDeclaration1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classBodyDeclaration2.
    def visitClassBodyDeclaration2(
        self, ctx: JavaLabeledParser.ClassBodyDeclaration2Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration0.
    def visitMemberDeclaration0(self, ctx: JavaLabeledParser.MemberDeclaration0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration1.
    def visitMemberDeclaration1(self, ctx: JavaLabeledParser.MemberDeclaration1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration2.
    def visitMemberDeclaration2(self, ctx: JavaLabeledParser.MemberDeclaration2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration3.
    def visitMemberDeclaration3(self, ctx: JavaLabeledParser.MemberDeclaration3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration4.
    def visitMemberDeclaration4(self, ctx: JavaLabeledParser.MemberDeclaration4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration5.
    def visitMemberDeclaration5(self, ctx: JavaLabeledParser.MemberDeclaration5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration6.
    def visitMemberDeclaration6(self, ctx: JavaLabeledParser.MemberDeclaration6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration7.
    def visitMemberDeclaration7(self, ctx: JavaLabeledParser.MemberDeclaration7Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#memberDeclaration8.
    def visitMemberDeclaration8(self, ctx: JavaLabeledParser.MemberDeclaration8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx: JavaLabeledParser.MethodDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#methodBody.
    def visitMethodBody(self, ctx: JavaLabeledParser.MethodBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeTypeOrVoid.
    def visitTypeTypeOrVoid(self, ctx: JavaLabeledParser.TypeTypeOrVoidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#genericMethodDeclaration.
    def visitGenericMethodDeclaration(
        self, ctx: JavaLabeledParser.GenericMethodDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#genericConstructorDeclaration.
    def visitGenericConstructorDeclaration(
        self, ctx: JavaLabeledParser.GenericConstructorDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#constructorDeclaration.
    def visitConstructorDeclaration(
        self, ctx: JavaLabeledParser.ConstructorDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx: JavaLabeledParser.FieldDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceBodyDeclaration.
    def visitInterfaceBodyDeclaration(
        self, ctx: JavaLabeledParser.InterfaceBodyDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMemberDeclaration0.
    def visitInterfaceMemberDeclaration0(
        self, ctx: JavaLabeledParser.InterfaceMemberDeclaration0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMemberDeclaration1.
    def visitInterfaceMemberDeclaration1(
        self, ctx: JavaLabeledParser.InterfaceMemberDeclaration1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMemberDeclaration2.
    def visitInterfaceMemberDeclaration2(
        self, ctx: JavaLabeledParser.InterfaceMemberDeclaration2Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMemberDeclaration3.
    def visitInterfaceMemberDeclaration3(
        self, ctx: JavaLabeledParser.InterfaceMemberDeclaration3Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMemberDeclaration4.
    def visitInterfaceMemberDeclaration4(
        self, ctx: JavaLabeledParser.InterfaceMemberDeclaration4Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMemberDeclaration5.
    def visitInterfaceMemberDeclaration5(
        self, ctx: JavaLabeledParser.InterfaceMemberDeclaration5Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMemberDeclaration6.
    def visitInterfaceMemberDeclaration6(
        self, ctx: JavaLabeledParser.InterfaceMemberDeclaration6Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#constDeclaration.
    def visitConstDeclaration(self, ctx: JavaLabeledParser.ConstDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#constantDeclarator.
    def visitConstantDeclarator(self, ctx: JavaLabeledParser.ConstantDeclaratorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMethodDeclaration.
    def visitInterfaceMethodDeclaration(
        self, ctx: JavaLabeledParser.InterfaceMethodDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#interfaceMethodModifier.
    def visitInterfaceMethodModifier(
        self, ctx: JavaLabeledParser.InterfaceMethodModifierContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#genericInterfaceMethodDeclaration.
    def visitGenericInterfaceMethodDeclaration(
        self, ctx: JavaLabeledParser.GenericInterfaceMethodDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#variableDeclarators.
    def visitVariableDeclarators(
        self, ctx: JavaLabeledParser.VariableDeclaratorsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#variableDeclarator.
    def visitVariableDeclarator(self, ctx: JavaLabeledParser.VariableDeclaratorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#variableDeclaratorId.
    def visitVariableDeclaratorId(
        self, ctx: JavaLabeledParser.VariableDeclaratorIdContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#variableInitializer0.
    def visitVariableInitializer0(
        self, ctx: JavaLabeledParser.VariableInitializer0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#variableInitializer1.
    def visitVariableInitializer1(
        self, ctx: JavaLabeledParser.VariableInitializer1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#arrayInitializer.
    def visitArrayInitializer(self, ctx: JavaLabeledParser.ArrayInitializerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classOrInterfaceType.
    def visitClassOrInterfaceType(
        self, ctx: JavaLabeledParser.ClassOrInterfaceTypeContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeArgument0.
    def visitTypeArgument0(self, ctx: JavaLabeledParser.TypeArgument0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#qualifiedNameList.
    def visitQualifiedNameList(self, ctx: JavaLabeledParser.QualifiedNameListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#formalParameters.
    def visitFormalParameters(self, ctx: JavaLabeledParser.FormalParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#formalParameterList0.
    def visitFormalParameterList0(
        self, ctx: JavaLabeledParser.FormalParameterList0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#formalParameterList1.
    def visitFormalParameterList1(
        self, ctx: JavaLabeledParser.FormalParameterList1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#formalParameter.
    def visitFormalParameter(self, ctx: JavaLabeledParser.FormalParameterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#lastFormalParameter.
    def visitLastFormalParameter(
        self, ctx: JavaLabeledParser.LastFormalParameterContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#qualifiedName.
    def visitQualifiedName(self, ctx: JavaLabeledParser.QualifiedNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#literal0.
    def visitLiteral0(self, ctx: JavaLabeledParser.Literal0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#literal1.
    def visitLiteral1(self, ctx: JavaLabeledParser.Literal1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#literal2.
    def visitLiteral2(self, ctx: JavaLabeledParser.Literal2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#literal3.
    def visitLiteral3(self, ctx: JavaLabeledParser.Literal3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#literal4.
    def visitLiteral4(self, ctx: JavaLabeledParser.Literal4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#literal5.
    def visitLiteral5(self, ctx: JavaLabeledParser.Literal5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#integerLiteral.
    def visitIntegerLiteral(self, ctx: JavaLabeledParser.IntegerLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#floatLiteral.
    def visitFloatLiteral(self, ctx: JavaLabeledParser.FloatLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#altAnnotationQualifiedName.
    def visitAltAnnotationQualifiedName(
        self, ctx: JavaLabeledParser.AltAnnotationQualifiedNameContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotation.
    def visitAnnotation(self, ctx: JavaLabeledParser.AnnotationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#elementValuePairs.
    def visitElementValuePairs(self, ctx: JavaLabeledParser.ElementValuePairsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#elementValuePair.
    def visitElementValuePair(self, ctx: JavaLabeledParser.ElementValuePairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#elementValue0.
    def visitElementValue0(self, ctx: JavaLabeledParser.ElementValue0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#elementValue1.
    def visitElementValue1(self, ctx: JavaLabeledParser.ElementValue1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#elementValue2.
    def visitElementValue2(self, ctx: JavaLabeledParser.ElementValue2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#elementValueArrayInitializer.
    def visitElementValueArrayInitializer(
        self, ctx: JavaLabeledParser.ElementValueArrayInitializerContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationTypeDeclaration.
    def visitAnnotationTypeDeclaration(
        self, ctx: JavaLabeledParser.AnnotationTypeDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationTypeBody.
    def visitAnnotationTypeBody(self, ctx: JavaLabeledParser.AnnotationTypeBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationTypeElementDeclaration.
    def visitAnnotationTypeElementDeclaration(
        self, ctx: JavaLabeledParser.AnnotationTypeElementDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationTypeElementRest0.
    def visitAnnotationTypeElementRest0(
        self, ctx: JavaLabeledParser.AnnotationTypeElementRest0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationTypeElementRest1.
    def visitAnnotationTypeElementRest1(
        self, ctx: JavaLabeledParser.AnnotationTypeElementRest1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationTypeElementRest2.
    def visitAnnotationTypeElementRest2(
        self, ctx: JavaLabeledParser.AnnotationTypeElementRest2Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationTypeElementRest3.
    def visitAnnotationTypeElementRest3(
        self, ctx: JavaLabeledParser.AnnotationTypeElementRest3Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationTypeElementRest4.
    def visitAnnotationTypeElementRest4(
        self, ctx: JavaLabeledParser.AnnotationTypeElementRest4Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationMethodOrConstantRest0.
    def visitAnnotationMethodOrConstantRest0(
        self, ctx: JavaLabeledParser.AnnotationMethodOrConstantRest0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationMethodOrConstantRest1.
    def visitAnnotationMethodOrConstantRest1(
        self, ctx: JavaLabeledParser.AnnotationMethodOrConstantRest1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationMethodRest.
    def visitAnnotationMethodRest(
        self, ctx: JavaLabeledParser.AnnotationMethodRestContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#annotationConstantRest.
    def visitAnnotationConstantRest(
        self, ctx: JavaLabeledParser.AnnotationConstantRestContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#defaultValue.
    def visitDefaultValue(self, ctx: JavaLabeledParser.DefaultValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#block.
    def visitBlock(self, ctx: JavaLabeledParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#blockStatement0.
    def visitBlockStatement0(self, ctx: JavaLabeledParser.BlockStatement0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#blockStatement1.
    def visitBlockStatement1(self, ctx: JavaLabeledParser.BlockStatement1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#blockStatement2.
    def visitBlockStatement2(self, ctx: JavaLabeledParser.BlockStatement2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#localVariableDeclaration.
    def visitLocalVariableDeclaration(
        self, ctx: JavaLabeledParser.LocalVariableDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#localTypeDeclaration.
    def visitLocalTypeDeclaration(
        self, ctx: JavaLabeledParser.LocalTypeDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement0.
    def visitStatement0(self, ctx: JavaLabeledParser.Statement0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement1.
    def visitStatement1(self, ctx: JavaLabeledParser.Statement1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement2.
    def visitStatement2(self, ctx: JavaLabeledParser.Statement2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement3.
    def visitStatement3(self, ctx: JavaLabeledParser.Statement3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement4.
    def visitStatement4(self, ctx: JavaLabeledParser.Statement4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement5.
    def visitStatement5(self, ctx: JavaLabeledParser.Statement5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement6.
    def visitStatement6(self, ctx: JavaLabeledParser.Statement6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement7.
    def visitStatement7(self, ctx: JavaLabeledParser.Statement7Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement8.
    def visitStatement8(self, ctx: JavaLabeledParser.Statement8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement9.
    def visitStatement9(self, ctx: JavaLabeledParser.Statement9Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement10.
    def visitStatement10(self, ctx: JavaLabeledParser.Statement10Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement11.
    def visitStatement11(self, ctx: JavaLabeledParser.Statement11Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement12.
    def visitStatement12(self, ctx: JavaLabeledParser.Statement12Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement13.
    def visitStatement13(self, ctx: JavaLabeledParser.Statement13Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement14.
    def visitStatement14(self, ctx: JavaLabeledParser.Statement14Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement15.
    def visitStatement15(self, ctx: JavaLabeledParser.Statement15Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#statement16.
    def visitStatement16(self, ctx: JavaLabeledParser.Statement16Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#catchClause.
    def visitCatchClause(self, ctx: JavaLabeledParser.CatchClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#catchType.
    def visitCatchType(self, ctx: JavaLabeledParser.CatchTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#finallyBlock.
    def visitFinallyBlock(self, ctx: JavaLabeledParser.FinallyBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#resourceSpecification.
    def visitResourceSpecification(
        self, ctx: JavaLabeledParser.ResourceSpecificationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#resources.
    def visitResources(self, ctx: JavaLabeledParser.ResourcesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#resource.
    def visitResource(self, ctx: JavaLabeledParser.ResourceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#switchBlockStatementGroup.
    def visitSwitchBlockStatementGroup(
        self, ctx: JavaLabeledParser.SwitchBlockStatementGroupContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#switchLabel.
    def visitSwitchLabel(self, ctx: JavaLabeledParser.SwitchLabelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#forControl0.
    def visitForControl0(self, ctx: JavaLabeledParser.ForControl0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#forControl1.
    def visitForControl1(self, ctx: JavaLabeledParser.ForControl1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#forInit0.
    def visitForInit0(self, ctx: JavaLabeledParser.ForInit0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#forInit1.
    def visitForInit1(self, ctx: JavaLabeledParser.ForInit1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#enhancedForControl.
    def visitEnhancedForControl(self, ctx: JavaLabeledParser.EnhancedForControlContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#parExpression.
    def visitParExpression(self, ctx: JavaLabeledParser.ParExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expressionList.
    def visitExpressionList(self, ctx: JavaLabeledParser.ExpressionListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#methodCall0.
    def visitMethodCall0(self, ctx: JavaLabeledParser.MethodCall0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#methodCall1.
    def visitMethodCall1(self, ctx: JavaLabeledParser.MethodCall1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#methodCall2.
    def visitMethodCall2(self, ctx: JavaLabeledParser.MethodCall2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression8.
    def visitExpression8(self, ctx: JavaLabeledParser.Expression8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression10.
    def visitExpression10(self, ctx: JavaLabeledParser.Expression10Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression9.
    def visitExpression9(self, ctx: JavaLabeledParser.Expression9Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression12.
    def visitExpression12(self, ctx: JavaLabeledParser.Expression12Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression11.
    def visitExpression11(self, ctx: JavaLabeledParser.Expression11Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression14.
    def visitExpression14(self, ctx: JavaLabeledParser.Expression14Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression13.
    def visitExpression13(self, ctx: JavaLabeledParser.Expression13Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression16.
    def visitExpression16(self, ctx: JavaLabeledParser.Expression16Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression15.
    def visitExpression15(self, ctx: JavaLabeledParser.Expression15Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression18.
    def visitExpression18(self, ctx: JavaLabeledParser.Expression18Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression17.
    def visitExpression17(self, ctx: JavaLabeledParser.Expression17Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression19.
    def visitExpression19(self, ctx: JavaLabeledParser.Expression19Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression6.
    def visitExpression6(self, ctx: JavaLabeledParser.Expression6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression7.
    def visitExpression7(self, ctx: JavaLabeledParser.Expression7Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression4.
    def visitExpression4(self, ctx: JavaLabeledParser.Expression4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression5.
    def visitExpression5(self, ctx: JavaLabeledParser.Expression5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression2.
    def visitExpression2(self, ctx: JavaLabeledParser.Expression2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression3.
    def visitExpression3(self, ctx: JavaLabeledParser.Expression3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression0.
    def visitExpression0(self, ctx: JavaLabeledParser.Expression0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression1.
    def visitExpression1(self, ctx: JavaLabeledParser.Expression1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression21.
    def visitExpression21(self, ctx: JavaLabeledParser.Expression21Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression20.
    def visitExpression20(self, ctx: JavaLabeledParser.Expression20Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression23.
    def visitExpression23(self, ctx: JavaLabeledParser.Expression23Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression22.
    def visitExpression22(self, ctx: JavaLabeledParser.Expression22Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression25.
    def visitExpression25(self, ctx: JavaLabeledParser.Expression25Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#expression24.
    def visitExpression24(self, ctx: JavaLabeledParser.Expression24Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#lambdaExpression.
    def visitLambdaExpression(self, ctx: JavaLabeledParser.LambdaExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#lambdaParameters0.
    def visitLambdaParameters0(self, ctx: JavaLabeledParser.LambdaParameters0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#lambdaParameters1.
    def visitLambdaParameters1(self, ctx: JavaLabeledParser.LambdaParameters1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#lambdaParameters2.
    def visitLambdaParameters2(self, ctx: JavaLabeledParser.LambdaParameters2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#lambdaBody0.
    def visitLambdaBody0(self, ctx: JavaLabeledParser.LambdaBody0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#lambdaBody1.
    def visitLambdaBody1(self, ctx: JavaLabeledParser.LambdaBody1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#primary0.
    def visitPrimary0(self, ctx: JavaLabeledParser.Primary0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#primary1.
    def visitPrimary1(self, ctx: JavaLabeledParser.Primary1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#primary2.
    def visitPrimary2(self, ctx: JavaLabeledParser.Primary2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#primary3.
    def visitPrimary3(self, ctx: JavaLabeledParser.Primary3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#primary4.
    def visitPrimary4(self, ctx: JavaLabeledParser.Primary4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#primary5.
    def visitPrimary5(self, ctx: JavaLabeledParser.Primary5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#primary6.
    def visitPrimary6(self, ctx: JavaLabeledParser.Primary6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classType.
    def visitClassType(self, ctx: JavaLabeledParser.ClassTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#creator0.
    def visitCreator0(self, ctx: JavaLabeledParser.Creator0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#creator1.
    def visitCreator1(self, ctx: JavaLabeledParser.Creator1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#createdName0.
    def visitCreatedName0(self, ctx: JavaLabeledParser.CreatedName0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#createdName1.
    def visitCreatedName1(self, ctx: JavaLabeledParser.CreatedName1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#innerCreator.
    def visitInnerCreator(self, ctx: JavaLabeledParser.InnerCreatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#arrayCreatorRest.
    def visitArrayCreatorRest(self, ctx: JavaLabeledParser.ArrayCreatorRestContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#classCreatorRest.
    def visitClassCreatorRest(self, ctx: JavaLabeledParser.ClassCreatorRestContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#explicitGenericInvocation.
    def visitExplicitGenericInvocation(
        self, ctx: JavaLabeledParser.ExplicitGenericInvocationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeArgumentsOrDiamond.
    def visitTypeArgumentsOrDiamond(
        self, ctx: JavaLabeledParser.TypeArgumentsOrDiamondContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#nonWildcardTypeArgumentsOrDiamond.
    def visitNonWildcardTypeArgumentsOrDiamond(
        self, ctx: JavaLabeledParser.NonWildcardTypeArgumentsOrDiamondContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#nonWildcardTypeArguments.
    def visitNonWildcardTypeArguments(
        self, ctx: JavaLabeledParser.NonWildcardTypeArgumentsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeList.
    def visitTypeList(self, ctx: JavaLabeledParser.TypeListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeType.
    def visitTypeType(self, ctx: JavaLabeledParser.TypeTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#primitiveType.
    def visitPrimitiveType(self, ctx: JavaLabeledParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#typeArguments.
    def visitTypeArguments(self, ctx: JavaLabeledParser.TypeArgumentsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#superSuffix0.
    def visitSuperSuffix0(self, ctx: JavaLabeledParser.SuperSuffix0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#superSuffix1.
    def visitSuperSuffix1(self, ctx: JavaLabeledParser.SuperSuffix1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#explicitGenericInvocationSuffix0.
    def visitExplicitGenericInvocationSuffix0(
        self, ctx: JavaLabeledParser.ExplicitGenericInvocationSuffix0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#explicitGenericInvocationSuffix1.
    def visitExplicitGenericInvocationSuffix1(
        self, ctx: JavaLabeledParser.ExplicitGenericInvocationSuffix1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaLabeledParser#arguments.
    def visitArguments(self, ctx: JavaLabeledParser.ArgumentsContext):
        return self.visitChildren(ctx)


del JavaLabeledParser
