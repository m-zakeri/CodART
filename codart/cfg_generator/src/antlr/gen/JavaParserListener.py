# Generated from G:/OpenUnderstand/cfg_generator/grammar/JavaParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser

# This class defines a complete listener for a parse tree produced by JavaParser.
class JavaParserListener(ParseTreeListener):

    # Enter a parse tree produced by JavaParser#start_.
    def enterStart_(self, ctx:JavaParser.Start_Context):
        pass

    # Exit a parse tree produced by JavaParser#start_.
    def exitStart_(self, ctx:JavaParser.Start_Context):
        pass


    # Enter a parse tree produced by JavaParser#literal.
    def enterLiteral(self, ctx:JavaParser.LiteralContext):
        pass

    # Exit a parse tree produced by JavaParser#literal.
    def exitLiteral(self, ctx:JavaParser.LiteralContext):
        pass


    # Enter a parse tree produced by JavaParser#typeIdentifier.
    def enterTypeIdentifier(self, ctx:JavaParser.TypeIdentifierContext):
        pass

    # Exit a parse tree produced by JavaParser#typeIdentifier.
    def exitTypeIdentifier(self, ctx:JavaParser.TypeIdentifierContext):
        pass


    # Enter a parse tree produced by JavaParser#unqualifiedMethodIdentifier.
    def enterUnqualifiedMethodIdentifier(self, ctx:JavaParser.UnqualifiedMethodIdentifierContext):
        pass

    # Exit a parse tree produced by JavaParser#unqualifiedMethodIdentifier.
    def exitUnqualifiedMethodIdentifier(self, ctx:JavaParser.UnqualifiedMethodIdentifierContext):
        pass


    # Enter a parse tree produced by JavaParser#primitiveType.
    def enterPrimitiveType(self, ctx:JavaParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#primitiveType.
    def exitPrimitiveType(self, ctx:JavaParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#numericType.
    def enterNumericType(self, ctx:JavaParser.NumericTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#numericType.
    def exitNumericType(self, ctx:JavaParser.NumericTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#integralType.
    def enterIntegralType(self, ctx:JavaParser.IntegralTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#integralType.
    def exitIntegralType(self, ctx:JavaParser.IntegralTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#floatingPointType.
    def enterFloatingPointType(self, ctx:JavaParser.FloatingPointTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#floatingPointType.
    def exitFloatingPointType(self, ctx:JavaParser.FloatingPointTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#referenceType.
    def enterReferenceType(self, ctx:JavaParser.ReferenceTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#referenceType.
    def exitReferenceType(self, ctx:JavaParser.ReferenceTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#coit.
    def enterCoit(self, ctx:JavaParser.CoitContext):
        pass

    # Exit a parse tree produced by JavaParser#coit.
    def exitCoit(self, ctx:JavaParser.CoitContext):
        pass


    # Enter a parse tree produced by JavaParser#classOrInterfaceType.
    def enterClassOrInterfaceType(self, ctx:JavaParser.ClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#classOrInterfaceType.
    def exitClassOrInterfaceType(self, ctx:JavaParser.ClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#classType.
    def enterClassType(self, ctx:JavaParser.ClassTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#classType.
    def exitClassType(self, ctx:JavaParser.ClassTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceType.
    def enterInterfaceType(self, ctx:JavaParser.InterfaceTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceType.
    def exitInterfaceType(self, ctx:JavaParser.InterfaceTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#typeVariable.
    def enterTypeVariable(self, ctx:JavaParser.TypeVariableContext):
        pass

    # Exit a parse tree produced by JavaParser#typeVariable.
    def exitTypeVariable(self, ctx:JavaParser.TypeVariableContext):
        pass


    # Enter a parse tree produced by JavaParser#arrayType.
    def enterArrayType(self, ctx:JavaParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayType.
    def exitArrayType(self, ctx:JavaParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#dims.
    def enterDims(self, ctx:JavaParser.DimsContext):
        pass

    # Exit a parse tree produced by JavaParser#dims.
    def exitDims(self, ctx:JavaParser.DimsContext):
        pass


    # Enter a parse tree produced by JavaParser#typeParameter.
    def enterTypeParameter(self, ctx:JavaParser.TypeParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameter.
    def exitTypeParameter(self, ctx:JavaParser.TypeParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#typeParameterModifier.
    def enterTypeParameterModifier(self, ctx:JavaParser.TypeParameterModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameterModifier.
    def exitTypeParameterModifier(self, ctx:JavaParser.TypeParameterModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#typeBound.
    def enterTypeBound(self, ctx:JavaParser.TypeBoundContext):
        pass

    # Exit a parse tree produced by JavaParser#typeBound.
    def exitTypeBound(self, ctx:JavaParser.TypeBoundContext):
        pass


    # Enter a parse tree produced by JavaParser#additionalBound.
    def enterAdditionalBound(self, ctx:JavaParser.AdditionalBoundContext):
        pass

    # Exit a parse tree produced by JavaParser#additionalBound.
    def exitAdditionalBound(self, ctx:JavaParser.AdditionalBoundContext):
        pass


    # Enter a parse tree produced by JavaParser#typeArguments.
    def enterTypeArguments(self, ctx:JavaParser.TypeArgumentsContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArguments.
    def exitTypeArguments(self, ctx:JavaParser.TypeArgumentsContext):
        pass


    # Enter a parse tree produced by JavaParser#typeArgumentList.
    def enterTypeArgumentList(self, ctx:JavaParser.TypeArgumentListContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArgumentList.
    def exitTypeArgumentList(self, ctx:JavaParser.TypeArgumentListContext):
        pass


    # Enter a parse tree produced by JavaParser#typeArgument.
    def enterTypeArgument(self, ctx:JavaParser.TypeArgumentContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArgument.
    def exitTypeArgument(self, ctx:JavaParser.TypeArgumentContext):
        pass


    # Enter a parse tree produced by JavaParser#wildcard.
    def enterWildcard(self, ctx:JavaParser.WildcardContext):
        pass

    # Exit a parse tree produced by JavaParser#wildcard.
    def exitWildcard(self, ctx:JavaParser.WildcardContext):
        pass


    # Enter a parse tree produced by JavaParser#wildcardBounds.
    def enterWildcardBounds(self, ctx:JavaParser.WildcardBoundsContext):
        pass

    # Exit a parse tree produced by JavaParser#wildcardBounds.
    def exitWildcardBounds(self, ctx:JavaParser.WildcardBoundsContext):
        pass


    # Enter a parse tree produced by JavaParser#moduleName.
    def enterModuleName(self, ctx:JavaParser.ModuleNameContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleName.
    def exitModuleName(self, ctx:JavaParser.ModuleNameContext):
        pass


    # Enter a parse tree produced by JavaParser#packageName.
    def enterPackageName(self, ctx:JavaParser.PackageNameContext):
        pass

    # Exit a parse tree produced by JavaParser#packageName.
    def exitPackageName(self, ctx:JavaParser.PackageNameContext):
        pass


    # Enter a parse tree produced by JavaParser#typeName.
    def enterTypeName(self, ctx:JavaParser.TypeNameContext):
        pass

    # Exit a parse tree produced by JavaParser#typeName.
    def exitTypeName(self, ctx:JavaParser.TypeNameContext):
        pass


    # Enter a parse tree produced by JavaParser#packageOrTypeName.
    def enterPackageOrTypeName(self, ctx:JavaParser.PackageOrTypeNameContext):
        pass

    # Exit a parse tree produced by JavaParser#packageOrTypeName.
    def exitPackageOrTypeName(self, ctx:JavaParser.PackageOrTypeNameContext):
        pass


    # Enter a parse tree produced by JavaParser#expressionName.
    def enterExpressionName(self, ctx:JavaParser.ExpressionNameContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionName.
    def exitExpressionName(self, ctx:JavaParser.ExpressionNameContext):
        pass


    # Enter a parse tree produced by JavaParser#methodName.
    def enterMethodName(self, ctx:JavaParser.MethodNameContext):
        pass

    # Exit a parse tree produced by JavaParser#methodName.
    def exitMethodName(self, ctx:JavaParser.MethodNameContext):
        pass


    # Enter a parse tree produced by JavaParser#ambiguousName.
    def enterAmbiguousName(self, ctx:JavaParser.AmbiguousNameContext):
        pass

    # Exit a parse tree produced by JavaParser#ambiguousName.
    def exitAmbiguousName(self, ctx:JavaParser.AmbiguousNameContext):
        pass


    # Enter a parse tree produced by JavaParser#compilationUnit.
    def enterCompilationUnit(self, ctx:JavaParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by JavaParser#compilationUnit.
    def exitCompilationUnit(self, ctx:JavaParser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by JavaParser#ordinaryCompilationUnit.
    def enterOrdinaryCompilationUnit(self, ctx:JavaParser.OrdinaryCompilationUnitContext):
        pass

    # Exit a parse tree produced by JavaParser#ordinaryCompilationUnit.
    def exitOrdinaryCompilationUnit(self, ctx:JavaParser.OrdinaryCompilationUnitContext):
        pass


    # Enter a parse tree produced by JavaParser#modularCompilationUnit.
    def enterModularCompilationUnit(self, ctx:JavaParser.ModularCompilationUnitContext):
        pass

    # Exit a parse tree produced by JavaParser#modularCompilationUnit.
    def exitModularCompilationUnit(self, ctx:JavaParser.ModularCompilationUnitContext):
        pass


    # Enter a parse tree produced by JavaParser#packageDeclaration.
    def enterPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#packageDeclaration.
    def exitPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#packageModifier.
    def enterPackageModifier(self, ctx:JavaParser.PackageModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#packageModifier.
    def exitPackageModifier(self, ctx:JavaParser.PackageModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#importDeclaration.
    def exitImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#singleTypeImportDeclaration.
    def enterSingleTypeImportDeclaration(self, ctx:JavaParser.SingleTypeImportDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#singleTypeImportDeclaration.
    def exitSingleTypeImportDeclaration(self, ctx:JavaParser.SingleTypeImportDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#typeImportOnDemandDeclaration.
    def enterTypeImportOnDemandDeclaration(self, ctx:JavaParser.TypeImportOnDemandDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#typeImportOnDemandDeclaration.
    def exitTypeImportOnDemandDeclaration(self, ctx:JavaParser.TypeImportOnDemandDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#singleStaticImportDeclaration.
    def enterSingleStaticImportDeclaration(self, ctx:JavaParser.SingleStaticImportDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#singleStaticImportDeclaration.
    def exitSingleStaticImportDeclaration(self, ctx:JavaParser.SingleStaticImportDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#staticImportOnDemandDeclaration.
    def enterStaticImportOnDemandDeclaration(self, ctx:JavaParser.StaticImportOnDemandDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#staticImportOnDemandDeclaration.
    def exitStaticImportOnDemandDeclaration(self, ctx:JavaParser.StaticImportOnDemandDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#topLevelClassOrInterfaceDeclaration.
    def enterTopLevelClassOrInterfaceDeclaration(self, ctx:JavaParser.TopLevelClassOrInterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#topLevelClassOrInterfaceDeclaration.
    def exitTopLevelClassOrInterfaceDeclaration(self, ctx:JavaParser.TopLevelClassOrInterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#moduleDeclaration.
    def enterModuleDeclaration(self, ctx:JavaParser.ModuleDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleDeclaration.
    def exitModuleDeclaration(self, ctx:JavaParser.ModuleDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#moduleDirective.
    def enterModuleDirective(self, ctx:JavaParser.ModuleDirectiveContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleDirective.
    def exitModuleDirective(self, ctx:JavaParser.ModuleDirectiveContext):
        pass


    # Enter a parse tree produced by JavaParser#requiresModifier.
    def enterRequiresModifier(self, ctx:JavaParser.RequiresModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#requiresModifier.
    def exitRequiresModifier(self, ctx:JavaParser.RequiresModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classDeclaration.
    def exitClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#normalClassDeclaration.
    def enterNormalClassDeclaration(self, ctx:JavaParser.NormalClassDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#normalClassDeclaration.
    def exitNormalClassDeclaration(self, ctx:JavaParser.NormalClassDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#classModifier.
    def enterClassModifier(self, ctx:JavaParser.ClassModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#classModifier.
    def exitClassModifier(self, ctx:JavaParser.ClassModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#typeParameters.
    def enterTypeParameters(self, ctx:JavaParser.TypeParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameters.
    def exitTypeParameters(self, ctx:JavaParser.TypeParametersContext):
        pass


    # Enter a parse tree produced by JavaParser#typeParameterList.
    def enterTypeParameterList(self, ctx:JavaParser.TypeParameterListContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameterList.
    def exitTypeParameterList(self, ctx:JavaParser.TypeParameterListContext):
        pass


    # Enter a parse tree produced by JavaParser#classExtends.
    def enterClassExtends(self, ctx:JavaParser.ClassExtendsContext):
        pass

    # Exit a parse tree produced by JavaParser#classExtends.
    def exitClassExtends(self, ctx:JavaParser.ClassExtendsContext):
        pass


    # Enter a parse tree produced by JavaParser#classImplements.
    def enterClassImplements(self, ctx:JavaParser.ClassImplementsContext):
        pass

    # Exit a parse tree produced by JavaParser#classImplements.
    def exitClassImplements(self, ctx:JavaParser.ClassImplementsContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceTypeList.
    def enterInterfaceTypeList(self, ctx:JavaParser.InterfaceTypeListContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceTypeList.
    def exitInterfaceTypeList(self, ctx:JavaParser.InterfaceTypeListContext):
        pass


    # Enter a parse tree produced by JavaParser#classPermits.
    def enterClassPermits(self, ctx:JavaParser.ClassPermitsContext):
        pass

    # Exit a parse tree produced by JavaParser#classPermits.
    def exitClassPermits(self, ctx:JavaParser.ClassPermitsContext):
        pass


    # Enter a parse tree produced by JavaParser#classBody.
    def enterClassBody(self, ctx:JavaParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#classBody.
    def exitClassBody(self, ctx:JavaParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#classBodyDeclaration.
    def enterClassBodyDeclaration(self, ctx:JavaParser.ClassBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classBodyDeclaration.
    def exitClassBodyDeclaration(self, ctx:JavaParser.ClassBodyDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#classMemberDeclaration.
    def enterClassMemberDeclaration(self, ctx:JavaParser.ClassMemberDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classMemberDeclaration.
    def exitClassMemberDeclaration(self, ctx:JavaParser.ClassMemberDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#fieldModifier.
    def enterFieldModifier(self, ctx:JavaParser.FieldModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#fieldModifier.
    def exitFieldModifier(self, ctx:JavaParser.FieldModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#variableDeclaratorList.
    def enterVariableDeclaratorList(self, ctx:JavaParser.VariableDeclaratorListContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclaratorList.
    def exitVariableDeclaratorList(self, ctx:JavaParser.VariableDeclaratorListContext):
        pass


    # Enter a parse tree produced by JavaParser#variableDeclarator.
    def enterVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclarator.
    def exitVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        pass


    # Enter a parse tree produced by JavaParser#variableDeclaratorId.
    def enterVariableDeclaratorId(self, ctx:JavaParser.VariableDeclaratorIdContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclaratorId.
    def exitVariableDeclaratorId(self, ctx:JavaParser.VariableDeclaratorIdContext):
        pass


    # Enter a parse tree produced by JavaParser#variableInitializer.
    def enterVariableInitializer(self, ctx:JavaParser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#variableInitializer.
    def exitVariableInitializer(self, ctx:JavaParser.VariableInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#unannType.
    def enterUnannType(self, ctx:JavaParser.UnannTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#unannType.
    def exitUnannType(self, ctx:JavaParser.UnannTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#unannPrimitiveType.
    def enterUnannPrimitiveType(self, ctx:JavaParser.UnannPrimitiveTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#unannPrimitiveType.
    def exitUnannPrimitiveType(self, ctx:JavaParser.UnannPrimitiveTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#unannReferenceType.
    def enterUnannReferenceType(self, ctx:JavaParser.UnannReferenceTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#unannReferenceType.
    def exitUnannReferenceType(self, ctx:JavaParser.UnannReferenceTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#unannClassOrInterfaceType.
    def enterUnannClassOrInterfaceType(self, ctx:JavaParser.UnannClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#unannClassOrInterfaceType.
    def exitUnannClassOrInterfaceType(self, ctx:JavaParser.UnannClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#uCOIT.
    def enterUCOIT(self, ctx:JavaParser.UCOITContext):
        pass

    # Exit a parse tree produced by JavaParser#uCOIT.
    def exitUCOIT(self, ctx:JavaParser.UCOITContext):
        pass


    # Enter a parse tree produced by JavaParser#unannClassType.
    def enterUnannClassType(self, ctx:JavaParser.UnannClassTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#unannClassType.
    def exitUnannClassType(self, ctx:JavaParser.UnannClassTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#unannInterfaceType.
    def enterUnannInterfaceType(self, ctx:JavaParser.UnannInterfaceTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#unannInterfaceType.
    def exitUnannInterfaceType(self, ctx:JavaParser.UnannInterfaceTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#unannTypeVariable.
    def enterUnannTypeVariable(self, ctx:JavaParser.UnannTypeVariableContext):
        pass

    # Exit a parse tree produced by JavaParser#unannTypeVariable.
    def exitUnannTypeVariable(self, ctx:JavaParser.UnannTypeVariableContext):
        pass


    # Enter a parse tree produced by JavaParser#unannArrayType.
    def enterUnannArrayType(self, ctx:JavaParser.UnannArrayTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#unannArrayType.
    def exitUnannArrayType(self, ctx:JavaParser.UnannArrayTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#methodModifier.
    def enterMethodModifier(self, ctx:JavaParser.MethodModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#methodModifier.
    def exitMethodModifier(self, ctx:JavaParser.MethodModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#methodHeader.
    def enterMethodHeader(self, ctx:JavaParser.MethodHeaderContext):
        pass

    # Exit a parse tree produced by JavaParser#methodHeader.
    def exitMethodHeader(self, ctx:JavaParser.MethodHeaderContext):
        pass


    # Enter a parse tree produced by JavaParser#result.
    def enterResult(self, ctx:JavaParser.ResultContext):
        pass

    # Exit a parse tree produced by JavaParser#result.
    def exitResult(self, ctx:JavaParser.ResultContext):
        pass


    # Enter a parse tree produced by JavaParser#methodDeclarator.
    def enterMethodDeclarator(self, ctx:JavaParser.MethodDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#methodDeclarator.
    def exitMethodDeclarator(self, ctx:JavaParser.MethodDeclaratorContext):
        pass


    # Enter a parse tree produced by JavaParser#receiverParameter.
    def enterReceiverParameter(self, ctx:JavaParser.ReceiverParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#receiverParameter.
    def exitReceiverParameter(self, ctx:JavaParser.ReceiverParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#formalParameterList.
    def enterFormalParameterList(self, ctx:JavaParser.FormalParameterListContext):
        pass

    # Exit a parse tree produced by JavaParser#formalParameterList.
    def exitFormalParameterList(self, ctx:JavaParser.FormalParameterListContext):
        pass


    # Enter a parse tree produced by JavaParser#formalParameter.
    def enterFormalParameter(self, ctx:JavaParser.FormalParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#formalParameter.
    def exitFormalParameter(self, ctx:JavaParser.FormalParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#variableArityParameter.
    def enterVariableArityParameter(self, ctx:JavaParser.VariableArityParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#variableArityParameter.
    def exitVariableArityParameter(self, ctx:JavaParser.VariableArityParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#variableModifier.
    def enterVariableModifier(self, ctx:JavaParser.VariableModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#variableModifier.
    def exitVariableModifier(self, ctx:JavaParser.VariableModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#throwsT.
    def enterThrowsT(self, ctx:JavaParser.ThrowsTContext):
        pass

    # Exit a parse tree produced by JavaParser#throwsT.
    def exitThrowsT(self, ctx:JavaParser.ThrowsTContext):
        pass


    # Enter a parse tree produced by JavaParser#exceptionTypeList.
    def enterExceptionTypeList(self, ctx:JavaParser.ExceptionTypeListContext):
        pass

    # Exit a parse tree produced by JavaParser#exceptionTypeList.
    def exitExceptionTypeList(self, ctx:JavaParser.ExceptionTypeListContext):
        pass


    # Enter a parse tree produced by JavaParser#exceptionType.
    def enterExceptionType(self, ctx:JavaParser.ExceptionTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#exceptionType.
    def exitExceptionType(self, ctx:JavaParser.ExceptionTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#methodBody.
    def enterMethodBody(self, ctx:JavaParser.MethodBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#methodBody.
    def exitMethodBody(self, ctx:JavaParser.MethodBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#instanceInitializer.
    def enterInstanceInitializer(self, ctx:JavaParser.InstanceInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#instanceInitializer.
    def exitInstanceInitializer(self, ctx:JavaParser.InstanceInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#staticInitializer.
    def enterStaticInitializer(self, ctx:JavaParser.StaticInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#staticInitializer.
    def exitStaticInitializer(self, ctx:JavaParser.StaticInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#constructorDeclaration.
    def enterConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#constructorDeclaration.
    def exitConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#constructorModifier.
    def enterConstructorModifier(self, ctx:JavaParser.ConstructorModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#constructorModifier.
    def exitConstructorModifier(self, ctx:JavaParser.ConstructorModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#constructorDeclarator.
    def enterConstructorDeclarator(self, ctx:JavaParser.ConstructorDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#constructorDeclarator.
    def exitConstructorDeclarator(self, ctx:JavaParser.ConstructorDeclaratorContext):
        pass


    # Enter a parse tree produced by JavaParser#simpleTypeName.
    def enterSimpleTypeName(self, ctx:JavaParser.SimpleTypeNameContext):
        pass

    # Exit a parse tree produced by JavaParser#simpleTypeName.
    def exitSimpleTypeName(self, ctx:JavaParser.SimpleTypeNameContext):
        pass


    # Enter a parse tree produced by JavaParser#constructorBody.
    def enterConstructorBody(self, ctx:JavaParser.ConstructorBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#constructorBody.
    def exitConstructorBody(self, ctx:JavaParser.ConstructorBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#explicitConstructorInvocation.
    def enterExplicitConstructorInvocation(self, ctx:JavaParser.ExplicitConstructorInvocationContext):
        pass

    # Exit a parse tree produced by JavaParser#explicitConstructorInvocation.
    def exitExplicitConstructorInvocation(self, ctx:JavaParser.ExplicitConstructorInvocationContext):
        pass


    # Enter a parse tree produced by JavaParser#enumDeclaration.
    def enterEnumDeclaration(self, ctx:JavaParser.EnumDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#enumDeclaration.
    def exitEnumDeclaration(self, ctx:JavaParser.EnumDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#enumBody.
    def enterEnumBody(self, ctx:JavaParser.EnumBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#enumBody.
    def exitEnumBody(self, ctx:JavaParser.EnumBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#enumConstantList.
    def enterEnumConstantList(self, ctx:JavaParser.EnumConstantListContext):
        pass

    # Exit a parse tree produced by JavaParser#enumConstantList.
    def exitEnumConstantList(self, ctx:JavaParser.EnumConstantListContext):
        pass


    # Enter a parse tree produced by JavaParser#enumConstant.
    def enterEnumConstant(self, ctx:JavaParser.EnumConstantContext):
        pass

    # Exit a parse tree produced by JavaParser#enumConstant.
    def exitEnumConstant(self, ctx:JavaParser.EnumConstantContext):
        pass


    # Enter a parse tree produced by JavaParser#enumConstantModifier.
    def enterEnumConstantModifier(self, ctx:JavaParser.EnumConstantModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#enumConstantModifier.
    def exitEnumConstantModifier(self, ctx:JavaParser.EnumConstantModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#enumBodyDeclarations.
    def enterEnumBodyDeclarations(self, ctx:JavaParser.EnumBodyDeclarationsContext):
        pass

    # Exit a parse tree produced by JavaParser#enumBodyDeclarations.
    def exitEnumBodyDeclarations(self, ctx:JavaParser.EnumBodyDeclarationsContext):
        pass


    # Enter a parse tree produced by JavaParser#recordDeclaration.
    def enterRecordDeclaration(self, ctx:JavaParser.RecordDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#recordDeclaration.
    def exitRecordDeclaration(self, ctx:JavaParser.RecordDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#recordHeader.
    def enterRecordHeader(self, ctx:JavaParser.RecordHeaderContext):
        pass

    # Exit a parse tree produced by JavaParser#recordHeader.
    def exitRecordHeader(self, ctx:JavaParser.RecordHeaderContext):
        pass


    # Enter a parse tree produced by JavaParser#recordComponentList.
    def enterRecordComponentList(self, ctx:JavaParser.RecordComponentListContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponentList.
    def exitRecordComponentList(self, ctx:JavaParser.RecordComponentListContext):
        pass


    # Enter a parse tree produced by JavaParser#recordComponent.
    def enterRecordComponent(self, ctx:JavaParser.RecordComponentContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponent.
    def exitRecordComponent(self, ctx:JavaParser.RecordComponentContext):
        pass


    # Enter a parse tree produced by JavaParser#variableArityRecordComponent.
    def enterVariableArityRecordComponent(self, ctx:JavaParser.VariableArityRecordComponentContext):
        pass

    # Exit a parse tree produced by JavaParser#variableArityRecordComponent.
    def exitVariableArityRecordComponent(self, ctx:JavaParser.VariableArityRecordComponentContext):
        pass


    # Enter a parse tree produced by JavaParser#recordComponentModifier.
    def enterRecordComponentModifier(self, ctx:JavaParser.RecordComponentModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponentModifier.
    def exitRecordComponentModifier(self, ctx:JavaParser.RecordComponentModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#recordBody.
    def enterRecordBody(self, ctx:JavaParser.RecordBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#recordBody.
    def exitRecordBody(self, ctx:JavaParser.RecordBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#recordBodyDeclaration.
    def enterRecordBodyDeclaration(self, ctx:JavaParser.RecordBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#recordBodyDeclaration.
    def exitRecordBodyDeclaration(self, ctx:JavaParser.RecordBodyDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#compactConstructorDeclaration.
    def enterCompactConstructorDeclaration(self, ctx:JavaParser.CompactConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#compactConstructorDeclaration.
    def exitCompactConstructorDeclaration(self, ctx:JavaParser.CompactConstructorDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceDeclaration.
    def enterInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceDeclaration.
    def exitInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#normalInterfaceDeclaration.
    def enterNormalInterfaceDeclaration(self, ctx:JavaParser.NormalInterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#normalInterfaceDeclaration.
    def exitNormalInterfaceDeclaration(self, ctx:JavaParser.NormalInterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceModifier.
    def enterInterfaceModifier(self, ctx:JavaParser.InterfaceModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceModifier.
    def exitInterfaceModifier(self, ctx:JavaParser.InterfaceModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceExtends.
    def enterInterfaceExtends(self, ctx:JavaParser.InterfaceExtendsContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceExtends.
    def exitInterfaceExtends(self, ctx:JavaParser.InterfaceExtendsContext):
        pass


    # Enter a parse tree produced by JavaParser#interfacePermits.
    def enterInterfacePermits(self, ctx:JavaParser.InterfacePermitsContext):
        pass

    # Exit a parse tree produced by JavaParser#interfacePermits.
    def exitInterfacePermits(self, ctx:JavaParser.InterfacePermitsContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceBody.
    def enterInterfaceBody(self, ctx:JavaParser.InterfaceBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceBody.
    def exitInterfaceBody(self, ctx:JavaParser.InterfaceBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def enterInterfaceMemberDeclaration(self, ctx:JavaParser.InterfaceMemberDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def exitInterfaceMemberDeclaration(self, ctx:JavaParser.InterfaceMemberDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#constantDeclaration.
    def enterConstantDeclaration(self, ctx:JavaParser.ConstantDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#constantDeclaration.
    def exitConstantDeclaration(self, ctx:JavaParser.ConstantDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#constantModifier.
    def enterConstantModifier(self, ctx:JavaParser.ConstantModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#constantModifier.
    def exitConstantModifier(self, ctx:JavaParser.ConstantModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def enterInterfaceMethodDeclaration(self, ctx:JavaParser.InterfaceMethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def exitInterfaceMethodDeclaration(self, ctx:JavaParser.InterfaceMethodDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceMethodModifier.
    def enterInterfaceMethodModifier(self, ctx:JavaParser.InterfaceMethodModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMethodModifier.
    def exitInterfaceMethodModifier(self, ctx:JavaParser.InterfaceMethodModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationInterfaceDeclaration.
    def enterAnnotationInterfaceDeclaration(self, ctx:JavaParser.AnnotationInterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationInterfaceDeclaration.
    def exitAnnotationInterfaceDeclaration(self, ctx:JavaParser.AnnotationInterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationInterfaceBody.
    def enterAnnotationInterfaceBody(self, ctx:JavaParser.AnnotationInterfaceBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationInterfaceBody.
    def exitAnnotationInterfaceBody(self, ctx:JavaParser.AnnotationInterfaceBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationInterfaceMemberDeclaration.
    def enterAnnotationInterfaceMemberDeclaration(self, ctx:JavaParser.AnnotationInterfaceMemberDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationInterfaceMemberDeclaration.
    def exitAnnotationInterfaceMemberDeclaration(self, ctx:JavaParser.AnnotationInterfaceMemberDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationInterfaceElementDeclaration.
    def enterAnnotationInterfaceElementDeclaration(self, ctx:JavaParser.AnnotationInterfaceElementDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationInterfaceElementDeclaration.
    def exitAnnotationInterfaceElementDeclaration(self, ctx:JavaParser.AnnotationInterfaceElementDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationInterfaceElementModifier.
    def enterAnnotationInterfaceElementModifier(self, ctx:JavaParser.AnnotationInterfaceElementModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationInterfaceElementModifier.
    def exitAnnotationInterfaceElementModifier(self, ctx:JavaParser.AnnotationInterfaceElementModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#defaultValue.
    def enterDefaultValue(self, ctx:JavaParser.DefaultValueContext):
        pass

    # Exit a parse tree produced by JavaParser#defaultValue.
    def exitDefaultValue(self, ctx:JavaParser.DefaultValueContext):
        pass


    # Enter a parse tree produced by JavaParser#annotation.
    def enterAnnotation(self, ctx:JavaParser.AnnotationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotation.
    def exitAnnotation(self, ctx:JavaParser.AnnotationContext):
        pass


    # Enter a parse tree produced by JavaParser#normalAnnotation.
    def enterNormalAnnotation(self, ctx:JavaParser.NormalAnnotationContext):
        pass

    # Exit a parse tree produced by JavaParser#normalAnnotation.
    def exitNormalAnnotation(self, ctx:JavaParser.NormalAnnotationContext):
        pass


    # Enter a parse tree produced by JavaParser#elementValuePairList.
    def enterElementValuePairList(self, ctx:JavaParser.ElementValuePairListContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValuePairList.
    def exitElementValuePairList(self, ctx:JavaParser.ElementValuePairListContext):
        pass


    # Enter a parse tree produced by JavaParser#elementValuePair.
    def enterElementValuePair(self, ctx:JavaParser.ElementValuePairContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValuePair.
    def exitElementValuePair(self, ctx:JavaParser.ElementValuePairContext):
        pass


    # Enter a parse tree produced by JavaParser#elementValue.
    def enterElementValue(self, ctx:JavaParser.ElementValueContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValue.
    def exitElementValue(self, ctx:JavaParser.ElementValueContext):
        pass


    # Enter a parse tree produced by JavaParser#elementValueArrayInitializer.
    def enterElementValueArrayInitializer(self, ctx:JavaParser.ElementValueArrayInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValueArrayInitializer.
    def exitElementValueArrayInitializer(self, ctx:JavaParser.ElementValueArrayInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#elementValueList.
    def enterElementValueList(self, ctx:JavaParser.ElementValueListContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValueList.
    def exitElementValueList(self, ctx:JavaParser.ElementValueListContext):
        pass


    # Enter a parse tree produced by JavaParser#markerAnnotation.
    def enterMarkerAnnotation(self, ctx:JavaParser.MarkerAnnotationContext):
        pass

    # Exit a parse tree produced by JavaParser#markerAnnotation.
    def exitMarkerAnnotation(self, ctx:JavaParser.MarkerAnnotationContext):
        pass


    # Enter a parse tree produced by JavaParser#singleElementAnnotation.
    def enterSingleElementAnnotation(self, ctx:JavaParser.SingleElementAnnotationContext):
        pass

    # Exit a parse tree produced by JavaParser#singleElementAnnotation.
    def exitSingleElementAnnotation(self, ctx:JavaParser.SingleElementAnnotationContext):
        pass


    # Enter a parse tree produced by JavaParser#arrayInitializer.
    def enterArrayInitializer(self, ctx:JavaParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayInitializer.
    def exitArrayInitializer(self, ctx:JavaParser.ArrayInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#variableInitializerList.
    def enterVariableInitializerList(self, ctx:JavaParser.VariableInitializerListContext):
        pass

    # Exit a parse tree produced by JavaParser#variableInitializerList.
    def exitVariableInitializerList(self, ctx:JavaParser.VariableInitializerListContext):
        pass


    # Enter a parse tree produced by JavaParser#block.
    def enterBlock(self, ctx:JavaParser.BlockContext):
        pass

    # Exit a parse tree produced by JavaParser#block.
    def exitBlock(self, ctx:JavaParser.BlockContext):
        pass


    # Enter a parse tree produced by JavaParser#blockStatements.
    def enterBlockStatements(self, ctx:JavaParser.BlockStatementsContext):
        pass

    # Exit a parse tree produced by JavaParser#blockStatements.
    def exitBlockStatements(self, ctx:JavaParser.BlockStatementsContext):
        pass


    # Enter a parse tree produced by JavaParser#blockStatement.
    def enterBlockStatement(self, ctx:JavaParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#blockStatement.
    def exitBlockStatement(self, ctx:JavaParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#localClassOrInterfaceDeclaration.
    def enterLocalClassOrInterfaceDeclaration(self, ctx:JavaParser.LocalClassOrInterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#localClassOrInterfaceDeclaration.
    def exitLocalClassOrInterfaceDeclaration(self, ctx:JavaParser.LocalClassOrInterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#localVariableDeclaration.
    def enterLocalVariableDeclaration(self, ctx:JavaParser.LocalVariableDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#localVariableDeclaration.
    def exitLocalVariableDeclaration(self, ctx:JavaParser.LocalVariableDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#localVariableType.
    def enterLocalVariableType(self, ctx:JavaParser.LocalVariableTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#localVariableType.
    def exitLocalVariableType(self, ctx:JavaParser.LocalVariableTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#localVariableDeclarationStatement.
    def enterLocalVariableDeclarationStatement(self, ctx:JavaParser.LocalVariableDeclarationStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#localVariableDeclarationStatement.
    def exitLocalVariableDeclarationStatement(self, ctx:JavaParser.LocalVariableDeclarationStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#statement.
    def enterStatement(self, ctx:JavaParser.StatementContext):
        pass

    # Exit a parse tree produced by JavaParser#statement.
    def exitStatement(self, ctx:JavaParser.StatementContext):
        pass


    # Enter a parse tree produced by JavaParser#statementNoShortIf.
    def enterStatementNoShortIf(self, ctx:JavaParser.StatementNoShortIfContext):
        pass

    # Exit a parse tree produced by JavaParser#statementNoShortIf.
    def exitStatementNoShortIf(self, ctx:JavaParser.StatementNoShortIfContext):
        pass


    # Enter a parse tree produced by JavaParser#statementWithoutTrailingSubstatement.
    def enterStatementWithoutTrailingSubstatement(self, ctx:JavaParser.StatementWithoutTrailingSubstatementContext):
        pass

    # Exit a parse tree produced by JavaParser#statementWithoutTrailingSubstatement.
    def exitStatementWithoutTrailingSubstatement(self, ctx:JavaParser.StatementWithoutTrailingSubstatementContext):
        pass


    # Enter a parse tree produced by JavaParser#emptyStatement_.
    def enterEmptyStatement_(self, ctx:JavaParser.EmptyStatement_Context):
        pass

    # Exit a parse tree produced by JavaParser#emptyStatement_.
    def exitEmptyStatement_(self, ctx:JavaParser.EmptyStatement_Context):
        pass


    # Enter a parse tree produced by JavaParser#labeledStatement.
    def enterLabeledStatement(self, ctx:JavaParser.LabeledStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#labeledStatement.
    def exitLabeledStatement(self, ctx:JavaParser.LabeledStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#labeledStatementNoShortIf.
    def enterLabeledStatementNoShortIf(self, ctx:JavaParser.LabeledStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by JavaParser#labeledStatementNoShortIf.
    def exitLabeledStatementNoShortIf(self, ctx:JavaParser.LabeledStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by JavaParser#expressionStatement.
    def enterExpressionStatement(self, ctx:JavaParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionStatement.
    def exitExpressionStatement(self, ctx:JavaParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#statementExpression.
    def enterStatementExpression(self, ctx:JavaParser.StatementExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#statementExpression.
    def exitStatementExpression(self, ctx:JavaParser.StatementExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#ifThenStatement.
    def enterIfThenStatement(self, ctx:JavaParser.IfThenStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#ifThenStatement.
    def exitIfThenStatement(self, ctx:JavaParser.IfThenStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#ifThenElseStatement.
    def enterIfThenElseStatement(self, ctx:JavaParser.IfThenElseStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#ifThenElseStatement.
    def exitIfThenElseStatement(self, ctx:JavaParser.IfThenElseStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#ifThenElseStatementNoShortIf.
    def enterIfThenElseStatementNoShortIf(self, ctx:JavaParser.IfThenElseStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by JavaParser#ifThenElseStatementNoShortIf.
    def exitIfThenElseStatementNoShortIf(self, ctx:JavaParser.IfThenElseStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by JavaParser#assertStatement.
    def enterAssertStatement(self, ctx:JavaParser.AssertStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#assertStatement.
    def exitAssertStatement(self, ctx:JavaParser.AssertStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#switchStatement.
    def enterSwitchStatement(self, ctx:JavaParser.SwitchStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#switchStatement.
    def exitSwitchStatement(self, ctx:JavaParser.SwitchStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#switchBlock.
    def enterSwitchBlock(self, ctx:JavaParser.SwitchBlockContext):
        pass

    # Exit a parse tree produced by JavaParser#switchBlock.
    def exitSwitchBlock(self, ctx:JavaParser.SwitchBlockContext):
        pass


    # Enter a parse tree produced by JavaParser#switchRule.
    def enterSwitchRule(self, ctx:JavaParser.SwitchRuleContext):
        pass

    # Exit a parse tree produced by JavaParser#switchRule.
    def exitSwitchRule(self, ctx:JavaParser.SwitchRuleContext):
        pass


    # Enter a parse tree produced by JavaParser#switchBlockStatementGroup.
    def enterSwitchBlockStatementGroup(self, ctx:JavaParser.SwitchBlockStatementGroupContext):
        pass

    # Exit a parse tree produced by JavaParser#switchBlockStatementGroup.
    def exitSwitchBlockStatementGroup(self, ctx:JavaParser.SwitchBlockStatementGroupContext):
        pass


    # Enter a parse tree produced by JavaParser#switchLabel.
    def enterSwitchLabel(self, ctx:JavaParser.SwitchLabelContext):
        pass

    # Exit a parse tree produced by JavaParser#switchLabel.
    def exitSwitchLabel(self, ctx:JavaParser.SwitchLabelContext):
        pass


    # Enter a parse tree produced by JavaParser#caseConstant.
    def enterCaseConstant(self, ctx:JavaParser.CaseConstantContext):
        pass

    # Exit a parse tree produced by JavaParser#caseConstant.
    def exitCaseConstant(self, ctx:JavaParser.CaseConstantContext):
        pass


    # Enter a parse tree produced by JavaParser#whileStatement.
    def enterWhileStatement(self, ctx:JavaParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#whileStatement.
    def exitWhileStatement(self, ctx:JavaParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#whileStatementNoShortIf.
    def enterWhileStatementNoShortIf(self, ctx:JavaParser.WhileStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by JavaParser#whileStatementNoShortIf.
    def exitWhileStatementNoShortIf(self, ctx:JavaParser.WhileStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by JavaParser#doStatement.
    def enterDoStatement(self, ctx:JavaParser.DoStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#doStatement.
    def exitDoStatement(self, ctx:JavaParser.DoStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#forStatement.
    def enterForStatement(self, ctx:JavaParser.ForStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#forStatement.
    def exitForStatement(self, ctx:JavaParser.ForStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#forStatementNoShortIf.
    def enterForStatementNoShortIf(self, ctx:JavaParser.ForStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by JavaParser#forStatementNoShortIf.
    def exitForStatementNoShortIf(self, ctx:JavaParser.ForStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by JavaParser#basicForStatement.
    def enterBasicForStatement(self, ctx:JavaParser.BasicForStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#basicForStatement.
    def exitBasicForStatement(self, ctx:JavaParser.BasicForStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#basicForStatementNoShortIf.
    def enterBasicForStatementNoShortIf(self, ctx:JavaParser.BasicForStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by JavaParser#basicForStatementNoShortIf.
    def exitBasicForStatementNoShortIf(self, ctx:JavaParser.BasicForStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by JavaParser#forInit.
    def enterForInit(self, ctx:JavaParser.ForInitContext):
        pass

    # Exit a parse tree produced by JavaParser#forInit.
    def exitForInit(self, ctx:JavaParser.ForInitContext):
        pass


    # Enter a parse tree produced by JavaParser#forUpdate.
    def enterForUpdate(self, ctx:JavaParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by JavaParser#forUpdate.
    def exitForUpdate(self, ctx:JavaParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by JavaParser#statementExpressionList.
    def enterStatementExpressionList(self, ctx:JavaParser.StatementExpressionListContext):
        pass

    # Exit a parse tree produced by JavaParser#statementExpressionList.
    def exitStatementExpressionList(self, ctx:JavaParser.StatementExpressionListContext):
        pass


    # Enter a parse tree produced by JavaParser#enhancedForStatement.
    def enterEnhancedForStatement(self, ctx:JavaParser.EnhancedForStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#enhancedForStatement.
    def exitEnhancedForStatement(self, ctx:JavaParser.EnhancedForStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#enhancedForStatementNoShortIf.
    def enterEnhancedForStatementNoShortIf(self, ctx:JavaParser.EnhancedForStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by JavaParser#enhancedForStatementNoShortIf.
    def exitEnhancedForStatementNoShortIf(self, ctx:JavaParser.EnhancedForStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by JavaParser#breakStatement.
    def enterBreakStatement(self, ctx:JavaParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#breakStatement.
    def exitBreakStatement(self, ctx:JavaParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#continueStatement.
    def enterContinueStatement(self, ctx:JavaParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#continueStatement.
    def exitContinueStatement(self, ctx:JavaParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#returnStatement.
    def enterReturnStatement(self, ctx:JavaParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#returnStatement.
    def exitReturnStatement(self, ctx:JavaParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#throwStatement.
    def enterThrowStatement(self, ctx:JavaParser.ThrowStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#throwStatement.
    def exitThrowStatement(self, ctx:JavaParser.ThrowStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#synchronizedStatement.
    def enterSynchronizedStatement(self, ctx:JavaParser.SynchronizedStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#synchronizedStatement.
    def exitSynchronizedStatement(self, ctx:JavaParser.SynchronizedStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#tryStatement.
    def enterTryStatement(self, ctx:JavaParser.TryStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#tryStatement.
    def exitTryStatement(self, ctx:JavaParser.TryStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#catches.
    def enterCatches(self, ctx:JavaParser.CatchesContext):
        pass

    # Exit a parse tree produced by JavaParser#catches.
    def exitCatches(self, ctx:JavaParser.CatchesContext):
        pass


    # Enter a parse tree produced by JavaParser#catchClause.
    def enterCatchClause(self, ctx:JavaParser.CatchClauseContext):
        pass

    # Exit a parse tree produced by JavaParser#catchClause.
    def exitCatchClause(self, ctx:JavaParser.CatchClauseContext):
        pass


    # Enter a parse tree produced by JavaParser#catchFormalParameter.
    def enterCatchFormalParameter(self, ctx:JavaParser.CatchFormalParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#catchFormalParameter.
    def exitCatchFormalParameter(self, ctx:JavaParser.CatchFormalParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#catchType.
    def enterCatchType(self, ctx:JavaParser.CatchTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#catchType.
    def exitCatchType(self, ctx:JavaParser.CatchTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#finallyBlock.
    def enterFinallyBlock(self, ctx:JavaParser.FinallyBlockContext):
        pass

    # Exit a parse tree produced by JavaParser#finallyBlock.
    def exitFinallyBlock(self, ctx:JavaParser.FinallyBlockContext):
        pass


    # Enter a parse tree produced by JavaParser#tryWithResourcesStatement.
    def enterTryWithResourcesStatement(self, ctx:JavaParser.TryWithResourcesStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#tryWithResourcesStatement.
    def exitTryWithResourcesStatement(self, ctx:JavaParser.TryWithResourcesStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#resourceSpecification.
    def enterResourceSpecification(self, ctx:JavaParser.ResourceSpecificationContext):
        pass

    # Exit a parse tree produced by JavaParser#resourceSpecification.
    def exitResourceSpecification(self, ctx:JavaParser.ResourceSpecificationContext):
        pass


    # Enter a parse tree produced by JavaParser#resourceList.
    def enterResourceList(self, ctx:JavaParser.ResourceListContext):
        pass

    # Exit a parse tree produced by JavaParser#resourceList.
    def exitResourceList(self, ctx:JavaParser.ResourceListContext):
        pass


    # Enter a parse tree produced by JavaParser#resource.
    def enterResource(self, ctx:JavaParser.ResourceContext):
        pass

    # Exit a parse tree produced by JavaParser#resource.
    def exitResource(self, ctx:JavaParser.ResourceContext):
        pass


    # Enter a parse tree produced by JavaParser#variableAccess.
    def enterVariableAccess(self, ctx:JavaParser.VariableAccessContext):
        pass

    # Exit a parse tree produced by JavaParser#variableAccess.
    def exitVariableAccess(self, ctx:JavaParser.VariableAccessContext):
        pass


    # Enter a parse tree produced by JavaParser#yieldStatement.
    def enterYieldStatement(self, ctx:JavaParser.YieldStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#yieldStatement.
    def exitYieldStatement(self, ctx:JavaParser.YieldStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#pattern.
    def enterPattern(self, ctx:JavaParser.PatternContext):
        pass

    # Exit a parse tree produced by JavaParser#pattern.
    def exitPattern(self, ctx:JavaParser.PatternContext):
        pass


    # Enter a parse tree produced by JavaParser#typePattern.
    def enterTypePattern(self, ctx:JavaParser.TypePatternContext):
        pass

    # Exit a parse tree produced by JavaParser#typePattern.
    def exitTypePattern(self, ctx:JavaParser.TypePatternContext):
        pass


    # Enter a parse tree produced by JavaParser#expression.
    def enterExpression(self, ctx:JavaParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#expression.
    def exitExpression(self, ctx:JavaParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#primary.
    def enterPrimary(self, ctx:JavaParser.PrimaryContext):
        pass

    # Exit a parse tree produced by JavaParser#primary.
    def exitPrimary(self, ctx:JavaParser.PrimaryContext):
        pass


    # Enter a parse tree produced by JavaParser#primaryNoNewArray.
    def enterPrimaryNoNewArray(self, ctx:JavaParser.PrimaryNoNewArrayContext):
        pass

    # Exit a parse tree produced by JavaParser#primaryNoNewArray.
    def exitPrimaryNoNewArray(self, ctx:JavaParser.PrimaryNoNewArrayContext):
        pass


    # Enter a parse tree produced by JavaParser#pNNA.
    def enterPNNA(self, ctx:JavaParser.PNNAContext):
        pass

    # Exit a parse tree produced by JavaParser#pNNA.
    def exitPNNA(self, ctx:JavaParser.PNNAContext):
        pass


    # Enter a parse tree produced by JavaParser#classLiteral.
    def enterClassLiteral(self, ctx:JavaParser.ClassLiteralContext):
        pass

    # Exit a parse tree produced by JavaParser#classLiteral.
    def exitClassLiteral(self, ctx:JavaParser.ClassLiteralContext):
        pass


    # Enter a parse tree produced by JavaParser#classInstanceCreationExpression.
    def enterClassInstanceCreationExpression(self, ctx:JavaParser.ClassInstanceCreationExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#classInstanceCreationExpression.
    def exitClassInstanceCreationExpression(self, ctx:JavaParser.ClassInstanceCreationExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#unqualifiedClassInstanceCreationExpression.
    def enterUnqualifiedClassInstanceCreationExpression(self, ctx:JavaParser.UnqualifiedClassInstanceCreationExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#unqualifiedClassInstanceCreationExpression.
    def exitUnqualifiedClassInstanceCreationExpression(self, ctx:JavaParser.UnqualifiedClassInstanceCreationExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#classOrInterfaceTypeToInstantiate.
    def enterClassOrInterfaceTypeToInstantiate(self, ctx:JavaParser.ClassOrInterfaceTypeToInstantiateContext):
        pass

    # Exit a parse tree produced by JavaParser#classOrInterfaceTypeToInstantiate.
    def exitClassOrInterfaceTypeToInstantiate(self, ctx:JavaParser.ClassOrInterfaceTypeToInstantiateContext):
        pass


    # Enter a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def enterTypeArgumentsOrDiamond(self, ctx:JavaParser.TypeArgumentsOrDiamondContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def exitTypeArgumentsOrDiamond(self, ctx:JavaParser.TypeArgumentsOrDiamondContext):
        pass


    # Enter a parse tree produced by JavaParser#arrayCreationExpression.
    def enterArrayCreationExpression(self, ctx:JavaParser.ArrayCreationExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayCreationExpression.
    def exitArrayCreationExpression(self, ctx:JavaParser.ArrayCreationExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#arrayCreationExpressionWithoutInitializer.
    def enterArrayCreationExpressionWithoutInitializer(self, ctx:JavaParser.ArrayCreationExpressionWithoutInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayCreationExpressionWithoutInitializer.
    def exitArrayCreationExpressionWithoutInitializer(self, ctx:JavaParser.ArrayCreationExpressionWithoutInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#arrayCreationExpressionWithInitializer.
    def enterArrayCreationExpressionWithInitializer(self, ctx:JavaParser.ArrayCreationExpressionWithInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayCreationExpressionWithInitializer.
    def exitArrayCreationExpressionWithInitializer(self, ctx:JavaParser.ArrayCreationExpressionWithInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#dimExprs.
    def enterDimExprs(self, ctx:JavaParser.DimExprsContext):
        pass

    # Exit a parse tree produced by JavaParser#dimExprs.
    def exitDimExprs(self, ctx:JavaParser.DimExprsContext):
        pass


    # Enter a parse tree produced by JavaParser#dimExpr.
    def enterDimExpr(self, ctx:JavaParser.DimExprContext):
        pass

    # Exit a parse tree produced by JavaParser#dimExpr.
    def exitDimExpr(self, ctx:JavaParser.DimExprContext):
        pass


    # Enter a parse tree produced by JavaParser#arrayAccess.
    def enterArrayAccess(self, ctx:JavaParser.ArrayAccessContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayAccess.
    def exitArrayAccess(self, ctx:JavaParser.ArrayAccessContext):
        pass


    # Enter a parse tree produced by JavaParser#fieldAccess.
    def enterFieldAccess(self, ctx:JavaParser.FieldAccessContext):
        pass

    # Exit a parse tree produced by JavaParser#fieldAccess.
    def exitFieldAccess(self, ctx:JavaParser.FieldAccessContext):
        pass


    # Enter a parse tree produced by JavaParser#methodInvocation.
    def enterMethodInvocation(self, ctx:JavaParser.MethodInvocationContext):
        pass

    # Exit a parse tree produced by JavaParser#methodInvocation.
    def exitMethodInvocation(self, ctx:JavaParser.MethodInvocationContext):
        pass


    # Enter a parse tree produced by JavaParser#argumentList.
    def enterArgumentList(self, ctx:JavaParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by JavaParser#argumentList.
    def exitArgumentList(self, ctx:JavaParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by JavaParser#methodReference.
    def enterMethodReference(self, ctx:JavaParser.MethodReferenceContext):
        pass

    # Exit a parse tree produced by JavaParser#methodReference.
    def exitMethodReference(self, ctx:JavaParser.MethodReferenceContext):
        pass


    # Enter a parse tree produced by JavaParser#postfixExpression.
    def enterPostfixExpression(self, ctx:JavaParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#postfixExpression.
    def exitPostfixExpression(self, ctx:JavaParser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#pfE.
    def enterPfE(self, ctx:JavaParser.PfEContext):
        pass

    # Exit a parse tree produced by JavaParser#pfE.
    def exitPfE(self, ctx:JavaParser.PfEContext):
        pass


    # Enter a parse tree produced by JavaParser#postIncrementExpression.
    def enterPostIncrementExpression(self, ctx:JavaParser.PostIncrementExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#postIncrementExpression.
    def exitPostIncrementExpression(self, ctx:JavaParser.PostIncrementExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#postDecrementExpression.
    def enterPostDecrementExpression(self, ctx:JavaParser.PostDecrementExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#postDecrementExpression.
    def exitPostDecrementExpression(self, ctx:JavaParser.PostDecrementExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#unaryExpression.
    def enterUnaryExpression(self, ctx:JavaParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#unaryExpression.
    def exitUnaryExpression(self, ctx:JavaParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#preIncrementExpression.
    def enterPreIncrementExpression(self, ctx:JavaParser.PreIncrementExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#preIncrementExpression.
    def exitPreIncrementExpression(self, ctx:JavaParser.PreIncrementExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#preDecrementExpression.
    def enterPreDecrementExpression(self, ctx:JavaParser.PreDecrementExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#preDecrementExpression.
    def exitPreDecrementExpression(self, ctx:JavaParser.PreDecrementExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#unaryExpressionNotPlusMinus.
    def enterUnaryExpressionNotPlusMinus(self, ctx:JavaParser.UnaryExpressionNotPlusMinusContext):
        pass

    # Exit a parse tree produced by JavaParser#unaryExpressionNotPlusMinus.
    def exitUnaryExpressionNotPlusMinus(self, ctx:JavaParser.UnaryExpressionNotPlusMinusContext):
        pass


    # Enter a parse tree produced by JavaParser#castExpression.
    def enterCastExpression(self, ctx:JavaParser.CastExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#castExpression.
    def exitCastExpression(self, ctx:JavaParser.CastExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:JavaParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:JavaParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:JavaParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:JavaParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#shiftExpression.
    def enterShiftExpression(self, ctx:JavaParser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#shiftExpression.
    def exitShiftExpression(self, ctx:JavaParser.ShiftExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#relationalExpression.
    def enterRelationalExpression(self, ctx:JavaParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#relationalExpression.
    def exitRelationalExpression(self, ctx:JavaParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#equalityExpression.
    def enterEqualityExpression(self, ctx:JavaParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#equalityExpression.
    def exitEqualityExpression(self, ctx:JavaParser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#andExpression.
    def enterAndExpression(self, ctx:JavaParser.AndExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#andExpression.
    def exitAndExpression(self, ctx:JavaParser.AndExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#exclusiveOrExpression.
    def enterExclusiveOrExpression(self, ctx:JavaParser.ExclusiveOrExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#exclusiveOrExpression.
    def exitExclusiveOrExpression(self, ctx:JavaParser.ExclusiveOrExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#inclusiveOrExpression.
    def enterInclusiveOrExpression(self, ctx:JavaParser.InclusiveOrExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#inclusiveOrExpression.
    def exitInclusiveOrExpression(self, ctx:JavaParser.InclusiveOrExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#conditionalAndExpression.
    def enterConditionalAndExpression(self, ctx:JavaParser.ConditionalAndExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#conditionalAndExpression.
    def exitConditionalAndExpression(self, ctx:JavaParser.ConditionalAndExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#conditionalOrExpression.
    def enterConditionalOrExpression(self, ctx:JavaParser.ConditionalOrExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#conditionalOrExpression.
    def exitConditionalOrExpression(self, ctx:JavaParser.ConditionalOrExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:JavaParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:JavaParser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:JavaParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:JavaParser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#assignment.
    def enterAssignment(self, ctx:JavaParser.AssignmentContext):
        pass

    # Exit a parse tree produced by JavaParser#assignment.
    def exitAssignment(self, ctx:JavaParser.AssignmentContext):
        pass


    # Enter a parse tree produced by JavaParser#leftHandSide.
    def enterLeftHandSide(self, ctx:JavaParser.LeftHandSideContext):
        pass

    # Exit a parse tree produced by JavaParser#leftHandSide.
    def exitLeftHandSide(self, ctx:JavaParser.LeftHandSideContext):
        pass


    # Enter a parse tree produced by JavaParser#assignmentOperator.
    def enterAssignmentOperator(self, ctx:JavaParser.AssignmentOperatorContext):
        pass

    # Exit a parse tree produced by JavaParser#assignmentOperator.
    def exitAssignmentOperator(self, ctx:JavaParser.AssignmentOperatorContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaExpression.
    def enterLambdaExpression(self, ctx:JavaParser.LambdaExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaExpression.
    def exitLambdaExpression(self, ctx:JavaParser.LambdaExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaParameters.
    def enterLambdaParameters(self, ctx:JavaParser.LambdaParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaParameters.
    def exitLambdaParameters(self, ctx:JavaParser.LambdaParametersContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaParameterList.
    def enterLambdaParameterList(self, ctx:JavaParser.LambdaParameterListContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaParameterList.
    def exitLambdaParameterList(self, ctx:JavaParser.LambdaParameterListContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaParameter.
    def enterLambdaParameter(self, ctx:JavaParser.LambdaParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaParameter.
    def exitLambdaParameter(self, ctx:JavaParser.LambdaParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaParameterType.
    def enterLambdaParameterType(self, ctx:JavaParser.LambdaParameterTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaParameterType.
    def exitLambdaParameterType(self, ctx:JavaParser.LambdaParameterTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaBody.
    def enterLambdaBody(self, ctx:JavaParser.LambdaBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaBody.
    def exitLambdaBody(self, ctx:JavaParser.LambdaBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#switchExpression.
    def enterSwitchExpression(self, ctx:JavaParser.SwitchExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#switchExpression.
    def exitSwitchExpression(self, ctx:JavaParser.SwitchExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#constantExpression.
    def enterConstantExpression(self, ctx:JavaParser.ConstantExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#constantExpression.
    def exitConstantExpression(self, ctx:JavaParser.ConstantExpressionContext):
        pass



del JavaParser