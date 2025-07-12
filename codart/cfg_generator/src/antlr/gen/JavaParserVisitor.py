# Generated from G:/OpenUnderstand/cfg_generator/grammar/JavaParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser

# This class defines a complete generic visitor for a parse tree produced by JavaParser.

class JavaParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JavaParser#start_.
    def visitStart_(self, ctx:JavaParser.Start_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#literal.
    def visitLiteral(self, ctx:JavaParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeIdentifier.
    def visitTypeIdentifier(self, ctx:JavaParser.TypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unqualifiedMethodIdentifier.
    def visitUnqualifiedMethodIdentifier(self, ctx:JavaParser.UnqualifiedMethodIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primitiveType.
    def visitPrimitiveType(self, ctx:JavaParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#numericType.
    def visitNumericType(self, ctx:JavaParser.NumericTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#integralType.
    def visitIntegralType(self, ctx:JavaParser.IntegralTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#floatingPointType.
    def visitFloatingPointType(self, ctx:JavaParser.FloatingPointTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#referenceType.
    def visitReferenceType(self, ctx:JavaParser.ReferenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#coit.
    def visitCoit(self, ctx:JavaParser.CoitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classOrInterfaceType.
    def visitClassOrInterfaceType(self, ctx:JavaParser.ClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classType.
    def visitClassType(self, ctx:JavaParser.ClassTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceType.
    def visitInterfaceType(self, ctx:JavaParser.InterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeVariable.
    def visitTypeVariable(self, ctx:JavaParser.TypeVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayType.
    def visitArrayType(self, ctx:JavaParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#dims.
    def visitDims(self, ctx:JavaParser.DimsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeParameter.
    def visitTypeParameter(self, ctx:JavaParser.TypeParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeParameterModifier.
    def visitTypeParameterModifier(self, ctx:JavaParser.TypeParameterModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeBound.
    def visitTypeBound(self, ctx:JavaParser.TypeBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#additionalBound.
    def visitAdditionalBound(self, ctx:JavaParser.AdditionalBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArguments.
    def visitTypeArguments(self, ctx:JavaParser.TypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArgumentList.
    def visitTypeArgumentList(self, ctx:JavaParser.TypeArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArgument.
    def visitTypeArgument(self, ctx:JavaParser.TypeArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#wildcard.
    def visitWildcard(self, ctx:JavaParser.WildcardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#wildcardBounds.
    def visitWildcardBounds(self, ctx:JavaParser.WildcardBoundsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#moduleName.
    def visitModuleName(self, ctx:JavaParser.ModuleNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#packageName.
    def visitPackageName(self, ctx:JavaParser.PackageNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeName.
    def visitTypeName(self, ctx:JavaParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#packageOrTypeName.
    def visitPackageOrTypeName(self, ctx:JavaParser.PackageOrTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expressionName.
    def visitExpressionName(self, ctx:JavaParser.ExpressionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodName.
    def visitMethodName(self, ctx:JavaParser.MethodNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#ambiguousName.
    def visitAmbiguousName(self, ctx:JavaParser.AmbiguousNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#compilationUnit.
    def visitCompilationUnit(self, ctx:JavaParser.CompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#ordinaryCompilationUnit.
    def visitOrdinaryCompilationUnit(self, ctx:JavaParser.OrdinaryCompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#modularCompilationUnit.
    def visitModularCompilationUnit(self, ctx:JavaParser.ModularCompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#packageDeclaration.
    def visitPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#packageModifier.
    def visitPackageModifier(self, ctx:JavaParser.PackageModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#importDeclaration.
    def visitImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#singleTypeImportDeclaration.
    def visitSingleTypeImportDeclaration(self, ctx:JavaParser.SingleTypeImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeImportOnDemandDeclaration.
    def visitTypeImportOnDemandDeclaration(self, ctx:JavaParser.TypeImportOnDemandDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#singleStaticImportDeclaration.
    def visitSingleStaticImportDeclaration(self, ctx:JavaParser.SingleStaticImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#staticImportOnDemandDeclaration.
    def visitStaticImportOnDemandDeclaration(self, ctx:JavaParser.StaticImportOnDemandDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#topLevelClassOrInterfaceDeclaration.
    def visitTopLevelClassOrInterfaceDeclaration(self, ctx:JavaParser.TopLevelClassOrInterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#moduleDeclaration.
    def visitModuleDeclaration(self, ctx:JavaParser.ModuleDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#moduleDirective.
    def visitModuleDirective(self, ctx:JavaParser.ModuleDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#requiresModifier.
    def visitRequiresModifier(self, ctx:JavaParser.RequiresModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classDeclaration.
    def visitClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#normalClassDeclaration.
    def visitNormalClassDeclaration(self, ctx:JavaParser.NormalClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classModifier.
    def visitClassModifier(self, ctx:JavaParser.ClassModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeParameters.
    def visitTypeParameters(self, ctx:JavaParser.TypeParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeParameterList.
    def visitTypeParameterList(self, ctx:JavaParser.TypeParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classExtends.
    def visitClassExtends(self, ctx:JavaParser.ClassExtendsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classImplements.
    def visitClassImplements(self, ctx:JavaParser.ClassImplementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceTypeList.
    def visitInterfaceTypeList(self, ctx:JavaParser.InterfaceTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classPermits.
    def visitClassPermits(self, ctx:JavaParser.ClassPermitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classBody.
    def visitClassBody(self, ctx:JavaParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classBodyDeclaration.
    def visitClassBodyDeclaration(self, ctx:JavaParser.ClassBodyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classMemberDeclaration.
    def visitClassMemberDeclaration(self, ctx:JavaParser.ClassMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#fieldModifier.
    def visitFieldModifier(self, ctx:JavaParser.FieldModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclaratorList.
    def visitVariableDeclaratorList(self, ctx:JavaParser.VariableDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclarator.
    def visitVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclaratorId.
    def visitVariableDeclaratorId(self, ctx:JavaParser.VariableDeclaratorIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableInitializer.
    def visitVariableInitializer(self, ctx:JavaParser.VariableInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unannType.
    def visitUnannType(self, ctx:JavaParser.UnannTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unannPrimitiveType.
    def visitUnannPrimitiveType(self, ctx:JavaParser.UnannPrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unannReferenceType.
    def visitUnannReferenceType(self, ctx:JavaParser.UnannReferenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unannClassOrInterfaceType.
    def visitUnannClassOrInterfaceType(self, ctx:JavaParser.UnannClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#uCOIT.
    def visitUCOIT(self, ctx:JavaParser.UCOITContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unannClassType.
    def visitUnannClassType(self, ctx:JavaParser.UnannClassTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unannInterfaceType.
    def visitUnannInterfaceType(self, ctx:JavaParser.UnannInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unannTypeVariable.
    def visitUnannTypeVariable(self, ctx:JavaParser.UnannTypeVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unannArrayType.
    def visitUnannArrayType(self, ctx:JavaParser.UnannArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodModifier.
    def visitMethodModifier(self, ctx:JavaParser.MethodModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodHeader.
    def visitMethodHeader(self, ctx:JavaParser.MethodHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#result.
    def visitResult(self, ctx:JavaParser.ResultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodDeclarator.
    def visitMethodDeclarator(self, ctx:JavaParser.MethodDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#receiverParameter.
    def visitReceiverParameter(self, ctx:JavaParser.ReceiverParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#formalParameterList.
    def visitFormalParameterList(self, ctx:JavaParser.FormalParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#formalParameter.
    def visitFormalParameter(self, ctx:JavaParser.FormalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableArityParameter.
    def visitVariableArityParameter(self, ctx:JavaParser.VariableArityParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableModifier.
    def visitVariableModifier(self, ctx:JavaParser.VariableModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#throwsT.
    def visitThrowsT(self, ctx:JavaParser.ThrowsTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#exceptionTypeList.
    def visitExceptionTypeList(self, ctx:JavaParser.ExceptionTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#exceptionType.
    def visitExceptionType(self, ctx:JavaParser.ExceptionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodBody.
    def visitMethodBody(self, ctx:JavaParser.MethodBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#instanceInitializer.
    def visitInstanceInitializer(self, ctx:JavaParser.InstanceInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#staticInitializer.
    def visitStaticInitializer(self, ctx:JavaParser.StaticInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constructorModifier.
    def visitConstructorModifier(self, ctx:JavaParser.ConstructorModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constructorDeclarator.
    def visitConstructorDeclarator(self, ctx:JavaParser.ConstructorDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#simpleTypeName.
    def visitSimpleTypeName(self, ctx:JavaParser.SimpleTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constructorBody.
    def visitConstructorBody(self, ctx:JavaParser.ConstructorBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#explicitConstructorInvocation.
    def visitExplicitConstructorInvocation(self, ctx:JavaParser.ExplicitConstructorInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:JavaParser.EnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumBody.
    def visitEnumBody(self, ctx:JavaParser.EnumBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumConstantList.
    def visitEnumConstantList(self, ctx:JavaParser.EnumConstantListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumConstant.
    def visitEnumConstant(self, ctx:JavaParser.EnumConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumConstantModifier.
    def visitEnumConstantModifier(self, ctx:JavaParser.EnumConstantModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumBodyDeclarations.
    def visitEnumBodyDeclarations(self, ctx:JavaParser.EnumBodyDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordDeclaration.
    def visitRecordDeclaration(self, ctx:JavaParser.RecordDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordHeader.
    def visitRecordHeader(self, ctx:JavaParser.RecordHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordComponentList.
    def visitRecordComponentList(self, ctx:JavaParser.RecordComponentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordComponent.
    def visitRecordComponent(self, ctx:JavaParser.RecordComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableArityRecordComponent.
    def visitVariableArityRecordComponent(self, ctx:JavaParser.VariableArityRecordComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordComponentModifier.
    def visitRecordComponentModifier(self, ctx:JavaParser.RecordComponentModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordBody.
    def visitRecordBody(self, ctx:JavaParser.RecordBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordBodyDeclaration.
    def visitRecordBodyDeclaration(self, ctx:JavaParser.RecordBodyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#compactConstructorDeclaration.
    def visitCompactConstructorDeclaration(self, ctx:JavaParser.CompactConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceDeclaration.
    def visitInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#normalInterfaceDeclaration.
    def visitNormalInterfaceDeclaration(self, ctx:JavaParser.NormalInterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceModifier.
    def visitInterfaceModifier(self, ctx:JavaParser.InterfaceModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceExtends.
    def visitInterfaceExtends(self, ctx:JavaParser.InterfaceExtendsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfacePermits.
    def visitInterfacePermits(self, ctx:JavaParser.InterfacePermitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceBody.
    def visitInterfaceBody(self, ctx:JavaParser.InterfaceBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def visitInterfaceMemberDeclaration(self, ctx:JavaParser.InterfaceMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constantDeclaration.
    def visitConstantDeclaration(self, ctx:JavaParser.ConstantDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constantModifier.
    def visitConstantModifier(self, ctx:JavaParser.ConstantModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def visitInterfaceMethodDeclaration(self, ctx:JavaParser.InterfaceMethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMethodModifier.
    def visitInterfaceMethodModifier(self, ctx:JavaParser.InterfaceMethodModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationInterfaceDeclaration.
    def visitAnnotationInterfaceDeclaration(self, ctx:JavaParser.AnnotationInterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationInterfaceBody.
    def visitAnnotationInterfaceBody(self, ctx:JavaParser.AnnotationInterfaceBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationInterfaceMemberDeclaration.
    def visitAnnotationInterfaceMemberDeclaration(self, ctx:JavaParser.AnnotationInterfaceMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationInterfaceElementDeclaration.
    def visitAnnotationInterfaceElementDeclaration(self, ctx:JavaParser.AnnotationInterfaceElementDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationInterfaceElementModifier.
    def visitAnnotationInterfaceElementModifier(self, ctx:JavaParser.AnnotationInterfaceElementModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#defaultValue.
    def visitDefaultValue(self, ctx:JavaParser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotation.
    def visitAnnotation(self, ctx:JavaParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#normalAnnotation.
    def visitNormalAnnotation(self, ctx:JavaParser.NormalAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValuePairList.
    def visitElementValuePairList(self, ctx:JavaParser.ElementValuePairListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValuePair.
    def visitElementValuePair(self, ctx:JavaParser.ElementValuePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValue.
    def visitElementValue(self, ctx:JavaParser.ElementValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValueArrayInitializer.
    def visitElementValueArrayInitializer(self, ctx:JavaParser.ElementValueArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValueList.
    def visitElementValueList(self, ctx:JavaParser.ElementValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#markerAnnotation.
    def visitMarkerAnnotation(self, ctx:JavaParser.MarkerAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#singleElementAnnotation.
    def visitSingleElementAnnotation(self, ctx:JavaParser.SingleElementAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayInitializer.
    def visitArrayInitializer(self, ctx:JavaParser.ArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableInitializerList.
    def visitVariableInitializerList(self, ctx:JavaParser.VariableInitializerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#block.
    def visitBlock(self, ctx:JavaParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#blockStatements.
    def visitBlockStatements(self, ctx:JavaParser.BlockStatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#blockStatement.
    def visitBlockStatement(self, ctx:JavaParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localClassOrInterfaceDeclaration.
    def visitLocalClassOrInterfaceDeclaration(self, ctx:JavaParser.LocalClassOrInterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx:JavaParser.LocalVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localVariableType.
    def visitLocalVariableType(self, ctx:JavaParser.LocalVariableTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localVariableDeclarationStatement.
    def visitLocalVariableDeclarationStatement(self, ctx:JavaParser.LocalVariableDeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statement.
    def visitStatement(self, ctx:JavaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statementNoShortIf.
    def visitStatementNoShortIf(self, ctx:JavaParser.StatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statementWithoutTrailingSubstatement.
    def visitStatementWithoutTrailingSubstatement(self, ctx:JavaParser.StatementWithoutTrailingSubstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#emptyStatement_.
    def visitEmptyStatement_(self, ctx:JavaParser.EmptyStatement_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#labeledStatement.
    def visitLabeledStatement(self, ctx:JavaParser.LabeledStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#labeledStatementNoShortIf.
    def visitLabeledStatementNoShortIf(self, ctx:JavaParser.LabeledStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expressionStatement.
    def visitExpressionStatement(self, ctx:JavaParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statementExpression.
    def visitStatementExpression(self, ctx:JavaParser.StatementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#ifThenStatement.
    def visitIfThenStatement(self, ctx:JavaParser.IfThenStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#ifThenElseStatement.
    def visitIfThenElseStatement(self, ctx:JavaParser.IfThenElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#ifThenElseStatementNoShortIf.
    def visitIfThenElseStatementNoShortIf(self, ctx:JavaParser.IfThenElseStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#assertStatement.
    def visitAssertStatement(self, ctx:JavaParser.AssertStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchStatement.
    def visitSwitchStatement(self, ctx:JavaParser.SwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchBlock.
    def visitSwitchBlock(self, ctx:JavaParser.SwitchBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchRule.
    def visitSwitchRule(self, ctx:JavaParser.SwitchRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchBlockStatementGroup.
    def visitSwitchBlockStatementGroup(self, ctx:JavaParser.SwitchBlockStatementGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchLabel.
    def visitSwitchLabel(self, ctx:JavaParser.SwitchLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#caseConstant.
    def visitCaseConstant(self, ctx:JavaParser.CaseConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#whileStatement.
    def visitWhileStatement(self, ctx:JavaParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#whileStatementNoShortIf.
    def visitWhileStatementNoShortIf(self, ctx:JavaParser.WhileStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#doStatement.
    def visitDoStatement(self, ctx:JavaParser.DoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forStatement.
    def visitForStatement(self, ctx:JavaParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forStatementNoShortIf.
    def visitForStatementNoShortIf(self, ctx:JavaParser.ForStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#basicForStatement.
    def visitBasicForStatement(self, ctx:JavaParser.BasicForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#basicForStatementNoShortIf.
    def visitBasicForStatementNoShortIf(self, ctx:JavaParser.BasicForStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forInit.
    def visitForInit(self, ctx:JavaParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forUpdate.
    def visitForUpdate(self, ctx:JavaParser.ForUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statementExpressionList.
    def visitStatementExpressionList(self, ctx:JavaParser.StatementExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enhancedForStatement.
    def visitEnhancedForStatement(self, ctx:JavaParser.EnhancedForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enhancedForStatementNoShortIf.
    def visitEnhancedForStatementNoShortIf(self, ctx:JavaParser.EnhancedForStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#breakStatement.
    def visitBreakStatement(self, ctx:JavaParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#continueStatement.
    def visitContinueStatement(self, ctx:JavaParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#returnStatement.
    def visitReturnStatement(self, ctx:JavaParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#throwStatement.
    def visitThrowStatement(self, ctx:JavaParser.ThrowStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#synchronizedStatement.
    def visitSynchronizedStatement(self, ctx:JavaParser.SynchronizedStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#tryStatement.
    def visitTryStatement(self, ctx:JavaParser.TryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catches.
    def visitCatches(self, ctx:JavaParser.CatchesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchClause.
    def visitCatchClause(self, ctx:JavaParser.CatchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchFormalParameter.
    def visitCatchFormalParameter(self, ctx:JavaParser.CatchFormalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchType.
    def visitCatchType(self, ctx:JavaParser.CatchTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#finallyBlock.
    def visitFinallyBlock(self, ctx:JavaParser.FinallyBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#tryWithResourcesStatement.
    def visitTryWithResourcesStatement(self, ctx:JavaParser.TryWithResourcesStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resourceSpecification.
    def visitResourceSpecification(self, ctx:JavaParser.ResourceSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resourceList.
    def visitResourceList(self, ctx:JavaParser.ResourceListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resource.
    def visitResource(self, ctx:JavaParser.ResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableAccess.
    def visitVariableAccess(self, ctx:JavaParser.VariableAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#yieldStatement.
    def visitYieldStatement(self, ctx:JavaParser.YieldStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#pattern.
    def visitPattern(self, ctx:JavaParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typePattern.
    def visitTypePattern(self, ctx:JavaParser.TypePatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expression.
    def visitExpression(self, ctx:JavaParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primary.
    def visitPrimary(self, ctx:JavaParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primaryNoNewArray.
    def visitPrimaryNoNewArray(self, ctx:JavaParser.PrimaryNoNewArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#pNNA.
    def visitPNNA(self, ctx:JavaParser.PNNAContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classLiteral.
    def visitClassLiteral(self, ctx:JavaParser.ClassLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classInstanceCreationExpression.
    def visitClassInstanceCreationExpression(self, ctx:JavaParser.ClassInstanceCreationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unqualifiedClassInstanceCreationExpression.
    def visitUnqualifiedClassInstanceCreationExpression(self, ctx:JavaParser.UnqualifiedClassInstanceCreationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classOrInterfaceTypeToInstantiate.
    def visitClassOrInterfaceTypeToInstantiate(self, ctx:JavaParser.ClassOrInterfaceTypeToInstantiateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def visitTypeArgumentsOrDiamond(self, ctx:JavaParser.TypeArgumentsOrDiamondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayCreationExpression.
    def visitArrayCreationExpression(self, ctx:JavaParser.ArrayCreationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayCreationExpressionWithoutInitializer.
    def visitArrayCreationExpressionWithoutInitializer(self, ctx:JavaParser.ArrayCreationExpressionWithoutInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayCreationExpressionWithInitializer.
    def visitArrayCreationExpressionWithInitializer(self, ctx:JavaParser.ArrayCreationExpressionWithInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#dimExprs.
    def visitDimExprs(self, ctx:JavaParser.DimExprsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#dimExpr.
    def visitDimExpr(self, ctx:JavaParser.DimExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayAccess.
    def visitArrayAccess(self, ctx:JavaParser.ArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#fieldAccess.
    def visitFieldAccess(self, ctx:JavaParser.FieldAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodInvocation.
    def visitMethodInvocation(self, ctx:JavaParser.MethodInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#argumentList.
    def visitArgumentList(self, ctx:JavaParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodReference.
    def visitMethodReference(self, ctx:JavaParser.MethodReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#postfixExpression.
    def visitPostfixExpression(self, ctx:JavaParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#pfE.
    def visitPfE(self, ctx:JavaParser.PfEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#postIncrementExpression.
    def visitPostIncrementExpression(self, ctx:JavaParser.PostIncrementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#postDecrementExpression.
    def visitPostDecrementExpression(self, ctx:JavaParser.PostDecrementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unaryExpression.
    def visitUnaryExpression(self, ctx:JavaParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#preIncrementExpression.
    def visitPreIncrementExpression(self, ctx:JavaParser.PreIncrementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#preDecrementExpression.
    def visitPreDecrementExpression(self, ctx:JavaParser.PreDecrementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unaryExpressionNotPlusMinus.
    def visitUnaryExpressionNotPlusMinus(self, ctx:JavaParser.UnaryExpressionNotPlusMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#castExpression.
    def visitCastExpression(self, ctx:JavaParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:JavaParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:JavaParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#shiftExpression.
    def visitShiftExpression(self, ctx:JavaParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#relationalExpression.
    def visitRelationalExpression(self, ctx:JavaParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#equalityExpression.
    def visitEqualityExpression(self, ctx:JavaParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#andExpression.
    def visitAndExpression(self, ctx:JavaParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#exclusiveOrExpression.
    def visitExclusiveOrExpression(self, ctx:JavaParser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#inclusiveOrExpression.
    def visitInclusiveOrExpression(self, ctx:JavaParser.InclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#conditionalAndExpression.
    def visitConditionalAndExpression(self, ctx:JavaParser.ConditionalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#conditionalOrExpression.
    def visitConditionalOrExpression(self, ctx:JavaParser.ConditionalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:JavaParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:JavaParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#assignment.
    def visitAssignment(self, ctx:JavaParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#leftHandSide.
    def visitLeftHandSide(self, ctx:JavaParser.LeftHandSideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:JavaParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaExpression.
    def visitLambdaExpression(self, ctx:JavaParser.LambdaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaParameters.
    def visitLambdaParameters(self, ctx:JavaParser.LambdaParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaParameterList.
    def visitLambdaParameterList(self, ctx:JavaParser.LambdaParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaParameter.
    def visitLambdaParameter(self, ctx:JavaParser.LambdaParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaParameterType.
    def visitLambdaParameterType(self, ctx:JavaParser.LambdaParameterTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaBody.
    def visitLambdaBody(self, ctx:JavaParser.LambdaBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchExpression.
    def visitSwitchExpression(self, ctx:JavaParser.SwitchExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constantExpression.
    def visitConstantExpression(self, ctx:JavaParser.ConstantExpressionContext):
        return self.visitChildren(ctx)



del JavaParser