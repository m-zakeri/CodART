# Generated from F:/IUST_4001/Compiler/Project/OpenUnderstand/OpenUnderstand/grammars\JavaLabeledParser.g4 by ANTLR 4.9.1
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .JavaParserLabeled import JavaParserLabeled
else:
    from JavaParserLabeled import JavaParserLabeled

# This class defines a complete generic visitor for a parse tree produced by JavaParserLabeled.


class JavaParserLabeledVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JavaParserLabeled#compilationUnit.
    def visitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#packageDeclaration.
    def visitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#importDeclaration.
    def visitImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeDeclaration.
    def visitTypeDeclaration(self, ctx: JavaParserLabeled.TypeDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#modifier.
    def visitModifier(self, ctx: JavaParserLabeled.ModifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classOrInterfaceModifier.
    def visitClassOrInterfaceModifier(
        self, ctx: JavaParserLabeled.ClassOrInterfaceModifierContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#variableModifier.
    def visitVariableModifier(self, ctx: JavaParserLabeled.VariableModifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classDeclaration.
    def visitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeParameters.
    def visitTypeParameters(self, ctx: JavaParserLabeled.TypeParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeParameter.
    def visitTypeParameter(self, ctx: JavaParserLabeled.TypeParameterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeBound.
    def visitTypeBound(self, ctx: JavaParserLabeled.TypeBoundContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#enumDeclaration.
    def visitEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#enumConstants.
    def visitEnumConstants(self, ctx: JavaParserLabeled.EnumConstantsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#enumConstant.
    def visitEnumConstant(self, ctx: JavaParserLabeled.EnumConstantContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#enumBodyDeclarations.
    def visitEnumBodyDeclarations(
        self, ctx: JavaParserLabeled.EnumBodyDeclarationsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceDeclaration.
    def visitInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classBody.
    def visitClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceBody.
    def visitInterfaceBody(self, ctx: JavaParserLabeled.InterfaceBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classBodyDeclaration0.
    def visitClassBodyDeclaration0(
        self, ctx: JavaParserLabeled.ClassBodyDeclaration0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classBodyDeclaration1.
    def visitClassBodyDeclaration1(
        self, ctx: JavaParserLabeled.ClassBodyDeclaration1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classBodyDeclaration2.
    def visitClassBodyDeclaration2(
        self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration0.
    def visitMemberDeclaration0(self, ctx: JavaParserLabeled.MemberDeclaration0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration1.
    def visitMemberDeclaration1(self, ctx: JavaParserLabeled.MemberDeclaration1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration2.
    def visitMemberDeclaration2(self, ctx: JavaParserLabeled.MemberDeclaration2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration3.
    def visitMemberDeclaration3(self, ctx: JavaParserLabeled.MemberDeclaration3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration4.
    def visitMemberDeclaration4(self, ctx: JavaParserLabeled.MemberDeclaration4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration5.
    def visitMemberDeclaration5(self, ctx: JavaParserLabeled.MemberDeclaration5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration6.
    def visitMemberDeclaration6(self, ctx: JavaParserLabeled.MemberDeclaration6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration7.
    def visitMemberDeclaration7(self, ctx: JavaParserLabeled.MemberDeclaration7Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#memberDeclaration8.
    def visitMemberDeclaration8(self, ctx: JavaParserLabeled.MemberDeclaration8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#methodDeclaration.
    def visitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#methodBody.
    def visitMethodBody(self, ctx: JavaParserLabeled.MethodBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeTypeOrVoid.
    def visitTypeTypeOrVoid(self, ctx: JavaParserLabeled.TypeTypeOrVoidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#genericMethodDeclaration.
    def visitGenericMethodDeclaration(
        self, ctx: JavaParserLabeled.GenericMethodDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#genericConstructorDeclaration.
    def visitGenericConstructorDeclaration(
        self, ctx: JavaParserLabeled.GenericConstructorDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#constructorDeclaration.
    def visitConstructorDeclaration(
        self, ctx: JavaParserLabeled.ConstructorDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#fieldDeclaration.
    def visitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceBodyDeclaration.
    def visitInterfaceBodyDeclaration(
        self, ctx: JavaParserLabeled.InterfaceBodyDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMemberDeclaration0.
    def visitInterfaceMemberDeclaration0(
        self, ctx: JavaParserLabeled.InterfaceMemberDeclaration0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMemberDeclaration1.
    def visitInterfaceMemberDeclaration1(
        self, ctx: JavaParserLabeled.InterfaceMemberDeclaration1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMemberDeclaration2.
    def visitInterfaceMemberDeclaration2(
        self, ctx: JavaParserLabeled.InterfaceMemberDeclaration2Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMemberDeclaration3.
    def visitInterfaceMemberDeclaration3(
        self, ctx: JavaParserLabeled.InterfaceMemberDeclaration3Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMemberDeclaration4.
    def visitInterfaceMemberDeclaration4(
        self, ctx: JavaParserLabeled.InterfaceMemberDeclaration4Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMemberDeclaration5.
    def visitInterfaceMemberDeclaration5(
        self, ctx: JavaParserLabeled.InterfaceMemberDeclaration5Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMemberDeclaration6.
    def visitInterfaceMemberDeclaration6(
        self, ctx: JavaParserLabeled.InterfaceMemberDeclaration6Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#constDeclaration.
    def visitConstDeclaration(self, ctx: JavaParserLabeled.ConstDeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#constantDeclarator.
    def visitConstantDeclarator(self, ctx: JavaParserLabeled.ConstantDeclaratorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMethodDeclaration.
    def visitInterfaceMethodDeclaration(
        self, ctx: JavaParserLabeled.InterfaceMethodDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#interfaceMethodModifier.
    def visitInterfaceMethodModifier(
        self, ctx: JavaParserLabeled.InterfaceMethodModifierContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#genericInterfaceMethodDeclaration.
    def visitGenericInterfaceMethodDeclaration(
        self, ctx: JavaParserLabeled.GenericInterfaceMethodDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#variableDeclarators.
    def visitVariableDeclarators(
        self, ctx: JavaParserLabeled.VariableDeclaratorsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#variableDeclarator.
    def visitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#variableDeclaratorId.
    def visitVariableDeclaratorId(
        self, ctx: JavaParserLabeled.VariableDeclaratorIdContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#variableInitializer0.
    def visitVariableInitializer0(
        self, ctx: JavaParserLabeled.VariableInitializer0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#variableInitializer1.
    def visitVariableInitializer1(
        self, ctx: JavaParserLabeled.VariableInitializer1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#arrayInitializer.
    def visitArrayInitializer(self, ctx: JavaParserLabeled.ArrayInitializerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classOrInterfaceType.
    def visitClassOrInterfaceType(
        self, ctx: JavaParserLabeled.ClassOrInterfaceTypeContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeArgument0.
    def visitTypeArgument0(self, ctx: JavaParserLabeled.TypeArgument0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#qualifiedNameList.
    def visitQualifiedNameList(self, ctx: JavaParserLabeled.QualifiedNameListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#formalParameters.
    def visitFormalParameters(self, ctx: JavaParserLabeled.FormalParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#formalParameterList0.
    def visitFormalParameterList0(
        self, ctx: JavaParserLabeled.FormalParameterList0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#formalParameterList1.
    def visitFormalParameterList1(
        self, ctx: JavaParserLabeled.FormalParameterList1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#formalParameter.
    def visitFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#lastFormalParameter.
    def visitLastFormalParameter(
        self, ctx: JavaParserLabeled.LastFormalParameterContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#qualifiedName.
    def visitQualifiedName(self, ctx: JavaParserLabeled.QualifiedNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#literal0.
    def visitLiteral0(self, ctx: JavaParserLabeled.Literal0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#literal1.
    def visitLiteral1(self, ctx: JavaParserLabeled.Literal1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#literal2.
    def visitLiteral2(self, ctx: JavaParserLabeled.Literal2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#literal3.
    def visitLiteral3(self, ctx: JavaParserLabeled.Literal3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#literal4.
    def visitLiteral4(self, ctx: JavaParserLabeled.Literal4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#literal5.
    def visitLiteral5(self, ctx: JavaParserLabeled.Literal5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#integerLiteral.
    def visitIntegerLiteral(self, ctx: JavaParserLabeled.IntegerLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#floatLiteral.
    def visitFloatLiteral(self, ctx: JavaParserLabeled.FloatLiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#altAnnotationQualifiedName.
    def visitAltAnnotationQualifiedName(
        self, ctx: JavaParserLabeled.AltAnnotationQualifiedNameContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotation.
    def visitAnnotation(self, ctx: JavaParserLabeled.AnnotationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#elementValuePairs.
    def visitElementValuePairs(self, ctx: JavaParserLabeled.ElementValuePairsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#elementValuePair.
    def visitElementValuePair(self, ctx: JavaParserLabeled.ElementValuePairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#elementValue0.
    def visitElementValue0(self, ctx: JavaParserLabeled.ElementValue0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#elementValue1.
    def visitElementValue1(self, ctx: JavaParserLabeled.ElementValue1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#elementValue2.
    def visitElementValue2(self, ctx: JavaParserLabeled.ElementValue2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#elementValueArrayInitializer.
    def visitElementValueArrayInitializer(
        self, ctx: JavaParserLabeled.ElementValueArrayInitializerContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationTypeDeclaration.
    def visitAnnotationTypeDeclaration(
        self, ctx: JavaParserLabeled.AnnotationTypeDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationTypeBody.
    def visitAnnotationTypeBody(self, ctx: JavaParserLabeled.AnnotationTypeBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationTypeElementDeclaration.
    def visitAnnotationTypeElementDeclaration(
        self, ctx: JavaParserLabeled.AnnotationTypeElementDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationTypeElementRest0.
    def visitAnnotationTypeElementRest0(
        self, ctx: JavaParserLabeled.AnnotationTypeElementRest0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationTypeElementRest1.
    def visitAnnotationTypeElementRest1(
        self, ctx: JavaParserLabeled.AnnotationTypeElementRest1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationTypeElementRest2.
    def visitAnnotationTypeElementRest2(
        self, ctx: JavaParserLabeled.AnnotationTypeElementRest2Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationTypeElementRest3.
    def visitAnnotationTypeElementRest3(
        self, ctx: JavaParserLabeled.AnnotationTypeElementRest3Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationTypeElementRest4.
    def visitAnnotationTypeElementRest4(
        self, ctx: JavaParserLabeled.AnnotationTypeElementRest4Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationMethodOrConstantRest0.
    def visitAnnotationMethodOrConstantRest0(
        self, ctx: JavaParserLabeled.AnnotationMethodOrConstantRest0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationMethodOrConstantRest1.
    def visitAnnotationMethodOrConstantRest1(
        self, ctx: JavaParserLabeled.AnnotationMethodOrConstantRest1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationMethodRest.
    def visitAnnotationMethodRest(
        self, ctx: JavaParserLabeled.AnnotationMethodRestContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#annotationConstantRest.
    def visitAnnotationConstantRest(
        self, ctx: JavaParserLabeled.AnnotationConstantRestContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#defaultValue.
    def visitDefaultValue(self, ctx: JavaParserLabeled.DefaultValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#block.
    def visitBlock(self, ctx: JavaParserLabeled.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#blockStatement0.
    def visitBlockStatement0(self, ctx: JavaParserLabeled.BlockStatement0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#blockStatement1.
    def visitBlockStatement1(self, ctx: JavaParserLabeled.BlockStatement1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#blockStatement2.
    def visitBlockStatement2(self, ctx: JavaParserLabeled.BlockStatement2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#localVariableDeclaration.
    def visitLocalVariableDeclaration(
        self, ctx: JavaParserLabeled.LocalVariableDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#localTypeDeclaration.
    def visitLocalTypeDeclaration(
        self, ctx: JavaParserLabeled.LocalTypeDeclarationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement0.
    def visitStatement0(self, ctx: JavaParserLabeled.Statement0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement1.
    def visitStatement1(self, ctx: JavaParserLabeled.Statement1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement2.
    def visitStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement3.
    def visitStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement4.
    def visitStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement5.
    def visitStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement6.
    def visitStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement7.
    def visitStatement7(self, ctx: JavaParserLabeled.Statement7Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement8.
    def visitStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement9.
    def visitStatement9(self, ctx: JavaParserLabeled.Statement9Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement10.
    def visitStatement10(self, ctx: JavaParserLabeled.Statement10Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement11.
    def visitStatement11(self, ctx: JavaParserLabeled.Statement11Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement12.
    def visitStatement12(self, ctx: JavaParserLabeled.Statement12Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement13.
    def visitStatement13(self, ctx: JavaParserLabeled.Statement13Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement14.
    def visitStatement14(self, ctx: JavaParserLabeled.Statement14Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement15.
    def visitStatement15(self, ctx: JavaParserLabeled.Statement15Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#statement16.
    def visitStatement16(self, ctx: JavaParserLabeled.Statement16Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#catchClause.
    def visitCatchClause(self, ctx: JavaParserLabeled.CatchClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#catchType.
    def visitCatchType(self, ctx: JavaParserLabeled.CatchTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#finallyBlock.
    def visitFinallyBlock(self, ctx: JavaParserLabeled.FinallyBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#resourceSpecification.
    def visitResourceSpecification(
        self, ctx: JavaParserLabeled.ResourceSpecificationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#resources.
    def visitResources(self, ctx: JavaParserLabeled.ResourcesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#resource.
    def visitResource(self, ctx: JavaParserLabeled.ResourceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#switchBlockStatementGroup.
    def visitSwitchBlockStatementGroup(
        self, ctx: JavaParserLabeled.SwitchBlockStatementGroupContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#switchLabel.
    def visitSwitchLabel(self, ctx: JavaParserLabeled.SwitchLabelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#forControl0.
    def visitForControl0(self, ctx: JavaParserLabeled.ForControl0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#forControl1.
    def visitForControl1(self, ctx: JavaParserLabeled.ForControl1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#forInit0.
    def visitForInit0(self, ctx: JavaParserLabeled.ForInit0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#forInit1.
    def visitForInit1(self, ctx: JavaParserLabeled.ForInit1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#enhancedForControl.
    def visitEnhancedForControl(self, ctx: JavaParserLabeled.EnhancedForControlContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#parExpression.
    def visitParExpression(self, ctx: JavaParserLabeled.ParExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expressionList.
    def visitExpressionList(self, ctx: JavaParserLabeled.ExpressionListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#methodCall0.
    def visitMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#methodCall1.
    def visitMethodCall1(self, ctx: JavaParserLabeled.MethodCall1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#methodCall2.
    def visitMethodCall2(self, ctx: JavaParserLabeled.MethodCall2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression8.
    def visitExpression8(self, ctx: JavaParserLabeled.Expression8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression10.
    def visitExpression10(self, ctx: JavaParserLabeled.Expression10Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression9.
    def visitExpression9(self, ctx: JavaParserLabeled.Expression9Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression12.
    def visitExpression12(self, ctx: JavaParserLabeled.Expression12Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression11.
    def visitExpression11(self, ctx: JavaParserLabeled.Expression11Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression14.
    def visitExpression14(self, ctx: JavaParserLabeled.Expression14Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression13.
    def visitExpression13(self, ctx: JavaParserLabeled.Expression13Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression16.
    def visitExpression16(self, ctx: JavaParserLabeled.Expression16Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression15.
    def visitExpression15(self, ctx: JavaParserLabeled.Expression15Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression18.
    def visitExpression18(self, ctx: JavaParserLabeled.Expression18Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression17.
    def visitExpression17(self, ctx: JavaParserLabeled.Expression17Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression19.
    def visitExpression19(self, ctx: JavaParserLabeled.Expression19Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression6.
    def visitExpression6(self, ctx: JavaParserLabeled.Expression6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression7.
    def visitExpression7(self, ctx: JavaParserLabeled.Expression7Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression4.
    def visitExpression4(self, ctx: JavaParserLabeled.Expression4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression5.
    def visitExpression5(self, ctx: JavaParserLabeled.Expression5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression2.
    def visitExpression2(self, ctx: JavaParserLabeled.Expression2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression3.
    def visitExpression3(self, ctx: JavaParserLabeled.Expression3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression0.
    def visitExpression0(self, ctx: JavaParserLabeled.Expression0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression1.
    def visitExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression21.
    def visitExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression20.
    def visitExpression20(self, ctx: JavaParserLabeled.Expression20Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression23.
    def visitExpression23(self, ctx: JavaParserLabeled.Expression23Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression22.
    def visitExpression22(self, ctx: JavaParserLabeled.Expression22Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression25.
    def visitExpression25(self, ctx: JavaParserLabeled.Expression25Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#expression24.
    def visitExpression24(self, ctx: JavaParserLabeled.Expression24Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#lambdaExpression.
    def visitLambdaExpression(self, ctx: JavaParserLabeled.LambdaExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#lambdaParameters0.
    def visitLambdaParameters0(self, ctx: JavaParserLabeled.LambdaParameters0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#lambdaParameters1.
    def visitLambdaParameters1(self, ctx: JavaParserLabeled.LambdaParameters1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#lambdaParameters2.
    def visitLambdaParameters2(self, ctx: JavaParserLabeled.LambdaParameters2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#lambdaBody0.
    def visitLambdaBody0(self, ctx: JavaParserLabeled.LambdaBody0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#lambdaBody1.
    def visitLambdaBody1(self, ctx: JavaParserLabeled.LambdaBody1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#primary0.
    def visitPrimary0(self, ctx: JavaParserLabeled.Primary0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#primary1.
    def visitPrimary1(self, ctx: JavaParserLabeled.Primary1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#primary2.
    def visitPrimary2(self, ctx: JavaParserLabeled.Primary2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#primary3.
    def visitPrimary3(self, ctx: JavaParserLabeled.Primary3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#primary4.
    def visitPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#primary5.
    def visitPrimary5(self, ctx: JavaParserLabeled.Primary5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#primary6.
    def visitPrimary6(self, ctx: JavaParserLabeled.Primary6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classType.
    def visitClassType(self, ctx: JavaParserLabeled.ClassTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#creator0.
    def visitCreator0(self, ctx: JavaParserLabeled.Creator0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#creator1.
    def visitCreator1(self, ctx: JavaParserLabeled.Creator1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#createdName0.
    def visitCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#createdName1.
    def visitCreatedName1(self, ctx: JavaParserLabeled.CreatedName1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#innerCreator.
    def visitInnerCreator(self, ctx: JavaParserLabeled.InnerCreatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#arrayCreatorRest.
    def visitArrayCreatorRest(self, ctx: JavaParserLabeled.ArrayCreatorRestContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#classCreatorRest.
    def visitClassCreatorRest(self, ctx: JavaParserLabeled.ClassCreatorRestContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#explicitGenericInvocation.
    def visitExplicitGenericInvocation(
        self, ctx: JavaParserLabeled.ExplicitGenericInvocationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeArgumentsOrDiamond.
    def visitTypeArgumentsOrDiamond(
        self, ctx: JavaParserLabeled.TypeArgumentsOrDiamondContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#nonWildcardTypeArgumentsOrDiamond.
    def visitNonWildcardTypeArgumentsOrDiamond(
        self, ctx: JavaParserLabeled.NonWildcardTypeArgumentsOrDiamondContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#nonWildcardTypeArguments.
    def visitNonWildcardTypeArguments(
        self, ctx: JavaParserLabeled.NonWildcardTypeArgumentsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeList.
    def visitTypeList(self, ctx: JavaParserLabeled.TypeListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeType.
    def visitTypeType(self, ctx: JavaParserLabeled.TypeTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#primitiveType.
    def visitPrimitiveType(self, ctx: JavaParserLabeled.PrimitiveTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#typeArguments.
    def visitTypeArguments(self, ctx: JavaParserLabeled.TypeArgumentsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#superSuffix0.
    def visitSuperSuffix0(self, ctx: JavaParserLabeled.SuperSuffix0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#superSuffix1.
    def visitSuperSuffix1(self, ctx: JavaParserLabeled.SuperSuffix1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#explicitGenericInvocationSuffix0.
    def visitExplicitGenericInvocationSuffix0(
        self, ctx: JavaParserLabeled.ExplicitGenericInvocationSuffix0Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#explicitGenericInvocationSuffix1.
    def visitExplicitGenericInvocationSuffix1(
        self, ctx: JavaParserLabeled.ExplicitGenericInvocationSuffix1Context
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by JavaParserLabeled#arguments.
    def visitArguments(self, ctx: JavaParserLabeled.ArgumentsContext):
        return self.visitChildren(ctx)


del JavaParserLabeled
