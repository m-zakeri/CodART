# Generated from Java9.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Java9Parser import Java9Parser
else:
    from Java9Parser import Java9Parser

# This class defines a complete listener for a parse tree produced by Java9Parser.
class Java9Listener(ParseTreeListener):

    # Enter a parse tree produced by Java9Parser#literal.
    def enterLiteral(self, ctx:Java9Parser.LiteralContext):
        pass

    # Exit a parse tree produced by Java9Parser#literal.
    def exitLiteral(self, ctx:Java9Parser.LiteralContext):
        pass


    # Enter a parse tree produced by Java9Parser#primitiveType.
    def enterPrimitiveType(self, ctx:Java9Parser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#primitiveType.
    def exitPrimitiveType(self, ctx:Java9Parser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#numericType.
    def enterNumericType(self, ctx:Java9Parser.NumericTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#numericType.
    def exitNumericType(self, ctx:Java9Parser.NumericTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#integralType.
    def enterIntegralType(self, ctx:Java9Parser.IntegralTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#integralType.
    def exitIntegralType(self, ctx:Java9Parser.IntegralTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#floatingPointType.
    def enterFloatingPointType(self, ctx:Java9Parser.FloatingPointTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#floatingPointType.
    def exitFloatingPointType(self, ctx:Java9Parser.FloatingPointTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#referenceType.
    def enterReferenceType(self, ctx:Java9Parser.ReferenceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#referenceType.
    def exitReferenceType(self, ctx:Java9Parser.ReferenceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#classOrInterfaceType.
    def enterClassOrInterfaceType(self, ctx:Java9Parser.ClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#classOrInterfaceType.
    def exitClassOrInterfaceType(self, ctx:Java9Parser.ClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#classType.
    def enterClassType(self, ctx:Java9Parser.ClassTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#classType.
    def exitClassType(self, ctx:Java9Parser.ClassTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#classType_lf_classOrInterfaceType.
    def enterClassType_lf_classOrInterfaceType(self, ctx:Java9Parser.ClassType_lf_classOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#classType_lf_classOrInterfaceType.
    def exitClassType_lf_classOrInterfaceType(self, ctx:Java9Parser.ClassType_lf_classOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#classType_lfno_classOrInterfaceType.
    def enterClassType_lfno_classOrInterfaceType(self, ctx:Java9Parser.ClassType_lfno_classOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#classType_lfno_classOrInterfaceType.
    def exitClassType_lfno_classOrInterfaceType(self, ctx:Java9Parser.ClassType_lfno_classOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceType.
    def enterInterfaceType(self, ctx:Java9Parser.InterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceType.
    def exitInterfaceType(self, ctx:Java9Parser.InterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceType_lf_classOrInterfaceType.
    def enterInterfaceType_lf_classOrInterfaceType(self, ctx:Java9Parser.InterfaceType_lf_classOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceType_lf_classOrInterfaceType.
    def exitInterfaceType_lf_classOrInterfaceType(self, ctx:Java9Parser.InterfaceType_lf_classOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceType_lfno_classOrInterfaceType.
    def enterInterfaceType_lfno_classOrInterfaceType(self, ctx:Java9Parser.InterfaceType_lfno_classOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceType_lfno_classOrInterfaceType.
    def exitInterfaceType_lfno_classOrInterfaceType(self, ctx:Java9Parser.InterfaceType_lfno_classOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeVariable.
    def enterTypeVariable(self, ctx:Java9Parser.TypeVariableContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeVariable.
    def exitTypeVariable(self, ctx:Java9Parser.TypeVariableContext):
        pass


    # Enter a parse tree produced by Java9Parser#arrayType.
    def enterArrayType(self, ctx:Java9Parser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#arrayType.
    def exitArrayType(self, ctx:Java9Parser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#dims.
    def enterDims(self, ctx:Java9Parser.DimsContext):
        pass

    # Exit a parse tree produced by Java9Parser#dims.
    def exitDims(self, ctx:Java9Parser.DimsContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeParameter.
    def enterTypeParameter(self, ctx:Java9Parser.TypeParameterContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeParameter.
    def exitTypeParameter(self, ctx:Java9Parser.TypeParameterContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeParameterModifier.
    def enterTypeParameterModifier(self, ctx:Java9Parser.TypeParameterModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeParameterModifier.
    def exitTypeParameterModifier(self, ctx:Java9Parser.TypeParameterModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeBound.
    def enterTypeBound(self, ctx:Java9Parser.TypeBoundContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeBound.
    def exitTypeBound(self, ctx:Java9Parser.TypeBoundContext):
        pass


    # Enter a parse tree produced by Java9Parser#additionalBound.
    def enterAdditionalBound(self, ctx:Java9Parser.AdditionalBoundContext):
        pass

    # Exit a parse tree produced by Java9Parser#additionalBound.
    def exitAdditionalBound(self, ctx:Java9Parser.AdditionalBoundContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeArguments.
    def enterTypeArguments(self, ctx:Java9Parser.TypeArgumentsContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeArguments.
    def exitTypeArguments(self, ctx:Java9Parser.TypeArgumentsContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeArgumentList.
    def enterTypeArgumentList(self, ctx:Java9Parser.TypeArgumentListContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeArgumentList.
    def exitTypeArgumentList(self, ctx:Java9Parser.TypeArgumentListContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeArgument.
    def enterTypeArgument(self, ctx:Java9Parser.TypeArgumentContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeArgument.
    def exitTypeArgument(self, ctx:Java9Parser.TypeArgumentContext):
        pass


    # Enter a parse tree produced by Java9Parser#wildcard.
    def enterWildcard(self, ctx:Java9Parser.WildcardContext):
        pass

    # Exit a parse tree produced by Java9Parser#wildcard.
    def exitWildcard(self, ctx:Java9Parser.WildcardContext):
        pass


    # Enter a parse tree produced by Java9Parser#wildcardBounds.
    def enterWildcardBounds(self, ctx:Java9Parser.WildcardBoundsContext):
        pass

    # Exit a parse tree produced by Java9Parser#wildcardBounds.
    def exitWildcardBounds(self, ctx:Java9Parser.WildcardBoundsContext):
        pass


    # Enter a parse tree produced by Java9Parser#moduleName.
    def enterModuleName(self, ctx:Java9Parser.ModuleNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#moduleName.
    def exitModuleName(self, ctx:Java9Parser.ModuleNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#packageName.
    def enterPackageName(self, ctx:Java9Parser.PackageNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#packageName.
    def exitPackageName(self, ctx:Java9Parser.PackageNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeName.
    def enterTypeName(self, ctx:Java9Parser.TypeNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeName.
    def exitTypeName(self, ctx:Java9Parser.TypeNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#packageOrTypeName.
    def enterPackageOrTypeName(self, ctx:Java9Parser.PackageOrTypeNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#packageOrTypeName.
    def exitPackageOrTypeName(self, ctx:Java9Parser.PackageOrTypeNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#expressionName.
    def enterExpressionName(self, ctx:Java9Parser.ExpressionNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#expressionName.
    def exitExpressionName(self, ctx:Java9Parser.ExpressionNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodName.
    def enterMethodName(self, ctx:Java9Parser.MethodNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodName.
    def exitMethodName(self, ctx:Java9Parser.MethodNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#ambiguousName.
    def enterAmbiguousName(self, ctx:Java9Parser.AmbiguousNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#ambiguousName.
    def exitAmbiguousName(self, ctx:Java9Parser.AmbiguousNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#compilationUnit.
    def enterCompilationUnit(self, ctx:Java9Parser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by Java9Parser#compilationUnit.
    def exitCompilationUnit(self, ctx:Java9Parser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by Java9Parser#ordinaryCompilation.
    def enterOrdinaryCompilation(self, ctx:Java9Parser.OrdinaryCompilationContext):
        pass

    # Exit a parse tree produced by Java9Parser#ordinaryCompilation.
    def exitOrdinaryCompilation(self, ctx:Java9Parser.OrdinaryCompilationContext):
        pass


    # Enter a parse tree produced by Java9Parser#modularCompilation.
    def enterModularCompilation(self, ctx:Java9Parser.ModularCompilationContext):
        pass

    # Exit a parse tree produced by Java9Parser#modularCompilation.
    def exitModularCompilation(self, ctx:Java9Parser.ModularCompilationContext):
        pass


    # Enter a parse tree produced by Java9Parser#packageDeclaration.
    def enterPackageDeclaration(self, ctx:Java9Parser.PackageDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#packageDeclaration.
    def exitPackageDeclaration(self, ctx:Java9Parser.PackageDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#packageModifier.
    def enterPackageModifier(self, ctx:Java9Parser.PackageModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#packageModifier.
    def exitPackageModifier(self, ctx:Java9Parser.PackageModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#importDeclaration.
    def enterImportDeclaration(self, ctx:Java9Parser.ImportDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#importDeclaration.
    def exitImportDeclaration(self, ctx:Java9Parser.ImportDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#singleTypeImportDeclaration.
    def enterSingleTypeImportDeclaration(self, ctx:Java9Parser.SingleTypeImportDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#singleTypeImportDeclaration.
    def exitSingleTypeImportDeclaration(self, ctx:Java9Parser.SingleTypeImportDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeImportOnDemandDeclaration.
    def enterTypeImportOnDemandDeclaration(self, ctx:Java9Parser.TypeImportOnDemandDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeImportOnDemandDeclaration.
    def exitTypeImportOnDemandDeclaration(self, ctx:Java9Parser.TypeImportOnDemandDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#singleStaticImportDeclaration.
    def enterSingleStaticImportDeclaration(self, ctx:Java9Parser.SingleStaticImportDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#singleStaticImportDeclaration.
    def exitSingleStaticImportDeclaration(self, ctx:Java9Parser.SingleStaticImportDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#staticImportOnDemandDeclaration.
    def enterStaticImportOnDemandDeclaration(self, ctx:Java9Parser.StaticImportOnDemandDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#staticImportOnDemandDeclaration.
    def exitStaticImportOnDemandDeclaration(self, ctx:Java9Parser.StaticImportOnDemandDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:Java9Parser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:Java9Parser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#moduleDeclaration.
    def enterModuleDeclaration(self, ctx:Java9Parser.ModuleDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#moduleDeclaration.
    def exitModuleDeclaration(self, ctx:Java9Parser.ModuleDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#moduleDirective.
    def enterModuleDirective(self, ctx:Java9Parser.ModuleDirectiveContext):
        pass

    # Exit a parse tree produced by Java9Parser#moduleDirective.
    def exitModuleDirective(self, ctx:Java9Parser.ModuleDirectiveContext):
        pass


    # Enter a parse tree produced by Java9Parser#requiresModifier.
    def enterRequiresModifier(self, ctx:Java9Parser.RequiresModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#requiresModifier.
    def exitRequiresModifier(self, ctx:Java9Parser.RequiresModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#classDeclaration.
    def enterClassDeclaration(self, ctx:Java9Parser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#classDeclaration.
    def exitClassDeclaration(self, ctx:Java9Parser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#normalClassDeclaration.
    def enterNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#normalClassDeclaration.
    def exitNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#classModifier.
    def enterClassModifier(self, ctx:Java9Parser.ClassModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#classModifier.
    def exitClassModifier(self, ctx:Java9Parser.ClassModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeParameters.
    def enterTypeParameters(self, ctx:Java9Parser.TypeParametersContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeParameters.
    def exitTypeParameters(self, ctx:Java9Parser.TypeParametersContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeParameterList.
    def enterTypeParameterList(self, ctx:Java9Parser.TypeParameterListContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeParameterList.
    def exitTypeParameterList(self, ctx:Java9Parser.TypeParameterListContext):
        pass


    # Enter a parse tree produced by Java9Parser#superclass.
    def enterSuperclass(self, ctx:Java9Parser.SuperclassContext):
        pass

    # Exit a parse tree produced by Java9Parser#superclass.
    def exitSuperclass(self, ctx:Java9Parser.SuperclassContext):
        pass


    # Enter a parse tree produced by Java9Parser#superinterfaces.
    def enterSuperinterfaces(self, ctx:Java9Parser.SuperinterfacesContext):
        pass

    # Exit a parse tree produced by Java9Parser#superinterfaces.
    def exitSuperinterfaces(self, ctx:Java9Parser.SuperinterfacesContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceTypeList.
    def enterInterfaceTypeList(self, ctx:Java9Parser.InterfaceTypeListContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceTypeList.
    def exitInterfaceTypeList(self, ctx:Java9Parser.InterfaceTypeListContext):
        pass


    # Enter a parse tree produced by Java9Parser#classBody.
    def enterClassBody(self, ctx:Java9Parser.ClassBodyContext):
        pass

    # Exit a parse tree produced by Java9Parser#classBody.
    def exitClassBody(self, ctx:Java9Parser.ClassBodyContext):
        pass


    # Enter a parse tree produced by Java9Parser#classBodyDeclaration.
    def enterClassBodyDeclaration(self, ctx:Java9Parser.ClassBodyDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#classBodyDeclaration.
    def exitClassBodyDeclaration(self, ctx:Java9Parser.ClassBodyDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#classMemberDeclaration.
    def enterClassMemberDeclaration(self, ctx:Java9Parser.ClassMemberDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#classMemberDeclaration.
    def exitClassMemberDeclaration(self, ctx:Java9Parser.ClassMemberDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:Java9Parser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx:Java9Parser.FieldDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#fieldModifier.
    def enterFieldModifier(self, ctx:Java9Parser.FieldModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#fieldModifier.
    def exitFieldModifier(self, ctx:Java9Parser.FieldModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#variableDeclaratorList.
    def enterVariableDeclaratorList(self, ctx:Java9Parser.VariableDeclaratorListContext):
        pass

    # Exit a parse tree produced by Java9Parser#variableDeclaratorList.
    def exitVariableDeclaratorList(self, ctx:Java9Parser.VariableDeclaratorListContext):
        pass


    # Enter a parse tree produced by Java9Parser#variableDeclarator.
    def enterVariableDeclarator(self, ctx:Java9Parser.VariableDeclaratorContext):
        pass

    # Exit a parse tree produced by Java9Parser#variableDeclarator.
    def exitVariableDeclarator(self, ctx:Java9Parser.VariableDeclaratorContext):
        pass


    # Enter a parse tree produced by Java9Parser#variableDeclaratorId.
    def enterVariableDeclaratorId(self, ctx:Java9Parser.VariableDeclaratorIdContext):
        pass

    # Exit a parse tree produced by Java9Parser#variableDeclaratorId.
    def exitVariableDeclaratorId(self, ctx:Java9Parser.VariableDeclaratorIdContext):
        pass


    # Enter a parse tree produced by Java9Parser#variableInitializer.
    def enterVariableInitializer(self, ctx:Java9Parser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by Java9Parser#variableInitializer.
    def exitVariableInitializer(self, ctx:Java9Parser.VariableInitializerContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannType.
    def enterUnannType(self, ctx:Java9Parser.UnannTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannType.
    def exitUnannType(self, ctx:Java9Parser.UnannTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannPrimitiveType.
    def enterUnannPrimitiveType(self, ctx:Java9Parser.UnannPrimitiveTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannPrimitiveType.
    def exitUnannPrimitiveType(self, ctx:Java9Parser.UnannPrimitiveTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannReferenceType.
    def enterUnannReferenceType(self, ctx:Java9Parser.UnannReferenceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannReferenceType.
    def exitUnannReferenceType(self, ctx:Java9Parser.UnannReferenceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannClassOrInterfaceType.
    def enterUnannClassOrInterfaceType(self, ctx:Java9Parser.UnannClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannClassOrInterfaceType.
    def exitUnannClassOrInterfaceType(self, ctx:Java9Parser.UnannClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannClassType.
    def enterUnannClassType(self, ctx:Java9Parser.UnannClassTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannClassType.
    def exitUnannClassType(self, ctx:Java9Parser.UnannClassTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannClassType_lf_unannClassOrInterfaceType.
    def enterUnannClassType_lf_unannClassOrInterfaceType(self, ctx:Java9Parser.UnannClassType_lf_unannClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannClassType_lf_unannClassOrInterfaceType.
    def exitUnannClassType_lf_unannClassOrInterfaceType(self, ctx:Java9Parser.UnannClassType_lf_unannClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannClassType_lfno_unannClassOrInterfaceType.
    def enterUnannClassType_lfno_unannClassOrInterfaceType(self, ctx:Java9Parser.UnannClassType_lfno_unannClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannClassType_lfno_unannClassOrInterfaceType.
    def exitUnannClassType_lfno_unannClassOrInterfaceType(self, ctx:Java9Parser.UnannClassType_lfno_unannClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannInterfaceType.
    def enterUnannInterfaceType(self, ctx:Java9Parser.UnannInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannInterfaceType.
    def exitUnannInterfaceType(self, ctx:Java9Parser.UnannInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannInterfaceType_lf_unannClassOrInterfaceType.
    def enterUnannInterfaceType_lf_unannClassOrInterfaceType(self, ctx:Java9Parser.UnannInterfaceType_lf_unannClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannInterfaceType_lf_unannClassOrInterfaceType.
    def exitUnannInterfaceType_lf_unannClassOrInterfaceType(self, ctx:Java9Parser.UnannInterfaceType_lf_unannClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannInterfaceType_lfno_unannClassOrInterfaceType.
    def enterUnannInterfaceType_lfno_unannClassOrInterfaceType(self, ctx:Java9Parser.UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannInterfaceType_lfno_unannClassOrInterfaceType.
    def exitUnannInterfaceType_lfno_unannClassOrInterfaceType(self, ctx:Java9Parser.UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannTypeVariable.
    def enterUnannTypeVariable(self, ctx:Java9Parser.UnannTypeVariableContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannTypeVariable.
    def exitUnannTypeVariable(self, ctx:Java9Parser.UnannTypeVariableContext):
        pass


    # Enter a parse tree produced by Java9Parser#unannArrayType.
    def enterUnannArrayType(self, ctx:Java9Parser.UnannArrayTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#unannArrayType.
    def exitUnannArrayType(self, ctx:Java9Parser.UnannArrayTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:Java9Parser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:Java9Parser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodModifier.
    def enterMethodModifier(self, ctx:Java9Parser.MethodModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodModifier.
    def exitMethodModifier(self, ctx:Java9Parser.MethodModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodHeader.
    def enterMethodHeader(self, ctx:Java9Parser.MethodHeaderContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodHeader.
    def exitMethodHeader(self, ctx:Java9Parser.MethodHeaderContext):
        pass


    # Enter a parse tree produced by Java9Parser#result.
    def enterResult(self, ctx:Java9Parser.ResultContext):
        pass

    # Exit a parse tree produced by Java9Parser#result.
    def exitResult(self, ctx:Java9Parser.ResultContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodDeclarator.
    def enterMethodDeclarator(self, ctx:Java9Parser.MethodDeclaratorContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodDeclarator.
    def exitMethodDeclarator(self, ctx:Java9Parser.MethodDeclaratorContext):
        pass


    # Enter a parse tree produced by Java9Parser#formalParameterList.
    def enterFormalParameterList(self, ctx:Java9Parser.FormalParameterListContext):
        pass

    # Exit a parse tree produced by Java9Parser#formalParameterList.
    def exitFormalParameterList(self, ctx:Java9Parser.FormalParameterListContext):
        pass


    # Enter a parse tree produced by Java9Parser#formalParameters.
    def enterFormalParameters(self, ctx:Java9Parser.FormalParametersContext):
        pass

    # Exit a parse tree produced by Java9Parser#formalParameters.
    def exitFormalParameters(self, ctx:Java9Parser.FormalParametersContext):
        pass


    # Enter a parse tree produced by Java9Parser#formalParameter.
    def enterFormalParameter(self, ctx:Java9Parser.FormalParameterContext):
        pass

    # Exit a parse tree produced by Java9Parser#formalParameter.
    def exitFormalParameter(self, ctx:Java9Parser.FormalParameterContext):
        pass


    # Enter a parse tree produced by Java9Parser#variableModifier.
    def enterVariableModifier(self, ctx:Java9Parser.VariableModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#variableModifier.
    def exitVariableModifier(self, ctx:Java9Parser.VariableModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#lastFormalParameter.
    def enterLastFormalParameter(self, ctx:Java9Parser.LastFormalParameterContext):
        pass

    # Exit a parse tree produced by Java9Parser#lastFormalParameter.
    def exitLastFormalParameter(self, ctx:Java9Parser.LastFormalParameterContext):
        pass


    # Enter a parse tree produced by Java9Parser#receiverParameter.
    def enterReceiverParameter(self, ctx:Java9Parser.ReceiverParameterContext):
        pass

    # Exit a parse tree produced by Java9Parser#receiverParameter.
    def exitReceiverParameter(self, ctx:Java9Parser.ReceiverParameterContext):
        pass


    # Enter a parse tree produced by Java9Parser#throws_.
    def enterThrows_(self, ctx:Java9Parser.Throws_Context):
        pass

    # Exit a parse tree produced by Java9Parser#throws_.
    def exitThrows_(self, ctx:Java9Parser.Throws_Context):
        pass


    # Enter a parse tree produced by Java9Parser#exceptionTypeList.
    def enterExceptionTypeList(self, ctx:Java9Parser.ExceptionTypeListContext):
        pass

    # Exit a parse tree produced by Java9Parser#exceptionTypeList.
    def exitExceptionTypeList(self, ctx:Java9Parser.ExceptionTypeListContext):
        pass


    # Enter a parse tree produced by Java9Parser#exceptionType.
    def enterExceptionType(self, ctx:Java9Parser.ExceptionTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#exceptionType.
    def exitExceptionType(self, ctx:Java9Parser.ExceptionTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodBody.
    def enterMethodBody(self, ctx:Java9Parser.MethodBodyContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodBody.
    def exitMethodBody(self, ctx:Java9Parser.MethodBodyContext):
        pass


    # Enter a parse tree produced by Java9Parser#instanceInitializer.
    def enterInstanceInitializer(self, ctx:Java9Parser.InstanceInitializerContext):
        pass

    # Exit a parse tree produced by Java9Parser#instanceInitializer.
    def exitInstanceInitializer(self, ctx:Java9Parser.InstanceInitializerContext):
        pass


    # Enter a parse tree produced by Java9Parser#staticInitializer.
    def enterStaticInitializer(self, ctx:Java9Parser.StaticInitializerContext):
        pass

    # Exit a parse tree produced by Java9Parser#staticInitializer.
    def exitStaticInitializer(self, ctx:Java9Parser.StaticInitializerContext):
        pass


    # Enter a parse tree produced by Java9Parser#constructorDeclaration.
    def enterConstructorDeclaration(self, ctx:Java9Parser.ConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#constructorDeclaration.
    def exitConstructorDeclaration(self, ctx:Java9Parser.ConstructorDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#constructorModifier.
    def enterConstructorModifier(self, ctx:Java9Parser.ConstructorModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#constructorModifier.
    def exitConstructorModifier(self, ctx:Java9Parser.ConstructorModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#constructorDeclarator.
    def enterConstructorDeclarator(self, ctx:Java9Parser.ConstructorDeclaratorContext):
        pass

    # Exit a parse tree produced by Java9Parser#constructorDeclarator.
    def exitConstructorDeclarator(self, ctx:Java9Parser.ConstructorDeclaratorContext):
        pass


    # Enter a parse tree produced by Java9Parser#simpleTypeName.
    def enterSimpleTypeName(self, ctx:Java9Parser.SimpleTypeNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#simpleTypeName.
    def exitSimpleTypeName(self, ctx:Java9Parser.SimpleTypeNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#constructorBody.
    def enterConstructorBody(self, ctx:Java9Parser.ConstructorBodyContext):
        pass

    # Exit a parse tree produced by Java9Parser#constructorBody.
    def exitConstructorBody(self, ctx:Java9Parser.ConstructorBodyContext):
        pass


    # Enter a parse tree produced by Java9Parser#explicitConstructorInvocation.
    def enterExplicitConstructorInvocation(self, ctx:Java9Parser.ExplicitConstructorInvocationContext):
        pass

    # Exit a parse tree produced by Java9Parser#explicitConstructorInvocation.
    def exitExplicitConstructorInvocation(self, ctx:Java9Parser.ExplicitConstructorInvocationContext):
        pass


    # Enter a parse tree produced by Java9Parser#enumDeclaration.
    def enterEnumDeclaration(self, ctx:Java9Parser.EnumDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#enumDeclaration.
    def exitEnumDeclaration(self, ctx:Java9Parser.EnumDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#enumBody.
    def enterEnumBody(self, ctx:Java9Parser.EnumBodyContext):
        pass

    # Exit a parse tree produced by Java9Parser#enumBody.
    def exitEnumBody(self, ctx:Java9Parser.EnumBodyContext):
        pass


    # Enter a parse tree produced by Java9Parser#enumConstantList.
    def enterEnumConstantList(self, ctx:Java9Parser.EnumConstantListContext):
        pass

    # Exit a parse tree produced by Java9Parser#enumConstantList.
    def exitEnumConstantList(self, ctx:Java9Parser.EnumConstantListContext):
        pass


    # Enter a parse tree produced by Java9Parser#enumConstant.
    def enterEnumConstant(self, ctx:Java9Parser.EnumConstantContext):
        pass

    # Exit a parse tree produced by Java9Parser#enumConstant.
    def exitEnumConstant(self, ctx:Java9Parser.EnumConstantContext):
        pass


    # Enter a parse tree produced by Java9Parser#enumConstantModifier.
    def enterEnumConstantModifier(self, ctx:Java9Parser.EnumConstantModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#enumConstantModifier.
    def exitEnumConstantModifier(self, ctx:Java9Parser.EnumConstantModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#enumBodyDeclarations.
    def enterEnumBodyDeclarations(self, ctx:Java9Parser.EnumBodyDeclarationsContext):
        pass

    # Exit a parse tree produced by Java9Parser#enumBodyDeclarations.
    def exitEnumBodyDeclarations(self, ctx:Java9Parser.EnumBodyDeclarationsContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceDeclaration.
    def enterInterfaceDeclaration(self, ctx:Java9Parser.InterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceDeclaration.
    def exitInterfaceDeclaration(self, ctx:Java9Parser.InterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#normalInterfaceDeclaration.
    def enterNormalInterfaceDeclaration(self, ctx:Java9Parser.NormalInterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#normalInterfaceDeclaration.
    def exitNormalInterfaceDeclaration(self, ctx:Java9Parser.NormalInterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceModifier.
    def enterInterfaceModifier(self, ctx:Java9Parser.InterfaceModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceModifier.
    def exitInterfaceModifier(self, ctx:Java9Parser.InterfaceModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#extendsInterfaces.
    def enterExtendsInterfaces(self, ctx:Java9Parser.ExtendsInterfacesContext):
        pass

    # Exit a parse tree produced by Java9Parser#extendsInterfaces.
    def exitExtendsInterfaces(self, ctx:Java9Parser.ExtendsInterfacesContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceBody.
    def enterInterfaceBody(self, ctx:Java9Parser.InterfaceBodyContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceBody.
    def exitInterfaceBody(self, ctx:Java9Parser.InterfaceBodyContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceMemberDeclaration.
    def enterInterfaceMemberDeclaration(self, ctx:Java9Parser.InterfaceMemberDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceMemberDeclaration.
    def exitInterfaceMemberDeclaration(self, ctx:Java9Parser.InterfaceMemberDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#constantDeclaration.
    def enterConstantDeclaration(self, ctx:Java9Parser.ConstantDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#constantDeclaration.
    def exitConstantDeclaration(self, ctx:Java9Parser.ConstantDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#constantModifier.
    def enterConstantModifier(self, ctx:Java9Parser.ConstantModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#constantModifier.
    def exitConstantModifier(self, ctx:Java9Parser.ConstantModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceMethodDeclaration.
    def enterInterfaceMethodDeclaration(self, ctx:Java9Parser.InterfaceMethodDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceMethodDeclaration.
    def exitInterfaceMethodDeclaration(self, ctx:Java9Parser.InterfaceMethodDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#interfaceMethodModifier.
    def enterInterfaceMethodModifier(self, ctx:Java9Parser.InterfaceMethodModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#interfaceMethodModifier.
    def exitInterfaceMethodModifier(self, ctx:Java9Parser.InterfaceMethodModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#annotationTypeDeclaration.
    def enterAnnotationTypeDeclaration(self, ctx:Java9Parser.AnnotationTypeDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#annotationTypeDeclaration.
    def exitAnnotationTypeDeclaration(self, ctx:Java9Parser.AnnotationTypeDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#annotationTypeBody.
    def enterAnnotationTypeBody(self, ctx:Java9Parser.AnnotationTypeBodyContext):
        pass

    # Exit a parse tree produced by Java9Parser#annotationTypeBody.
    def exitAnnotationTypeBody(self, ctx:Java9Parser.AnnotationTypeBodyContext):
        pass


    # Enter a parse tree produced by Java9Parser#annotationTypeMemberDeclaration.
    def enterAnnotationTypeMemberDeclaration(self, ctx:Java9Parser.AnnotationTypeMemberDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#annotationTypeMemberDeclaration.
    def exitAnnotationTypeMemberDeclaration(self, ctx:Java9Parser.AnnotationTypeMemberDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#annotationTypeElementDeclaration.
    def enterAnnotationTypeElementDeclaration(self, ctx:Java9Parser.AnnotationTypeElementDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#annotationTypeElementDeclaration.
    def exitAnnotationTypeElementDeclaration(self, ctx:Java9Parser.AnnotationTypeElementDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#annotationTypeElementModifier.
    def enterAnnotationTypeElementModifier(self, ctx:Java9Parser.AnnotationTypeElementModifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#annotationTypeElementModifier.
    def exitAnnotationTypeElementModifier(self, ctx:Java9Parser.AnnotationTypeElementModifierContext):
        pass


    # Enter a parse tree produced by Java9Parser#defaultValue.
    def enterDefaultValue(self, ctx:Java9Parser.DefaultValueContext):
        pass

    # Exit a parse tree produced by Java9Parser#defaultValue.
    def exitDefaultValue(self, ctx:Java9Parser.DefaultValueContext):
        pass


    # Enter a parse tree produced by Java9Parser#annotation.
    def enterAnnotation(self, ctx:Java9Parser.AnnotationContext):
        pass

    # Exit a parse tree produced by Java9Parser#annotation.
    def exitAnnotation(self, ctx:Java9Parser.AnnotationContext):
        pass


    # Enter a parse tree produced by Java9Parser#normalAnnotation.
    def enterNormalAnnotation(self, ctx:Java9Parser.NormalAnnotationContext):
        pass

    # Exit a parse tree produced by Java9Parser#normalAnnotation.
    def exitNormalAnnotation(self, ctx:Java9Parser.NormalAnnotationContext):
        pass


    # Enter a parse tree produced by Java9Parser#elementValuePairList.
    def enterElementValuePairList(self, ctx:Java9Parser.ElementValuePairListContext):
        pass

    # Exit a parse tree produced by Java9Parser#elementValuePairList.
    def exitElementValuePairList(self, ctx:Java9Parser.ElementValuePairListContext):
        pass


    # Enter a parse tree produced by Java9Parser#elementValuePair.
    def enterElementValuePair(self, ctx:Java9Parser.ElementValuePairContext):
        pass

    # Exit a parse tree produced by Java9Parser#elementValuePair.
    def exitElementValuePair(self, ctx:Java9Parser.ElementValuePairContext):
        pass


    # Enter a parse tree produced by Java9Parser#elementValue.
    def enterElementValue(self, ctx:Java9Parser.ElementValueContext):
        pass

    # Exit a parse tree produced by Java9Parser#elementValue.
    def exitElementValue(self, ctx:Java9Parser.ElementValueContext):
        pass


    # Enter a parse tree produced by Java9Parser#elementValueArrayInitializer.
    def enterElementValueArrayInitializer(self, ctx:Java9Parser.ElementValueArrayInitializerContext):
        pass

    # Exit a parse tree produced by Java9Parser#elementValueArrayInitializer.
    def exitElementValueArrayInitializer(self, ctx:Java9Parser.ElementValueArrayInitializerContext):
        pass


    # Enter a parse tree produced by Java9Parser#elementValueList.
    def enterElementValueList(self, ctx:Java9Parser.ElementValueListContext):
        pass

    # Exit a parse tree produced by Java9Parser#elementValueList.
    def exitElementValueList(self, ctx:Java9Parser.ElementValueListContext):
        pass


    # Enter a parse tree produced by Java9Parser#markerAnnotation.
    def enterMarkerAnnotation(self, ctx:Java9Parser.MarkerAnnotationContext):
        pass

    # Exit a parse tree produced by Java9Parser#markerAnnotation.
    def exitMarkerAnnotation(self, ctx:Java9Parser.MarkerAnnotationContext):
        pass


    # Enter a parse tree produced by Java9Parser#singleElementAnnotation.
    def enterSingleElementAnnotation(self, ctx:Java9Parser.SingleElementAnnotationContext):
        pass

    # Exit a parse tree produced by Java9Parser#singleElementAnnotation.
    def exitSingleElementAnnotation(self, ctx:Java9Parser.SingleElementAnnotationContext):
        pass


    # Enter a parse tree produced by Java9Parser#arrayInitializer.
    def enterArrayInitializer(self, ctx:Java9Parser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by Java9Parser#arrayInitializer.
    def exitArrayInitializer(self, ctx:Java9Parser.ArrayInitializerContext):
        pass


    # Enter a parse tree produced by Java9Parser#variableInitializerList.
    def enterVariableInitializerList(self, ctx:Java9Parser.VariableInitializerListContext):
        pass

    # Exit a parse tree produced by Java9Parser#variableInitializerList.
    def exitVariableInitializerList(self, ctx:Java9Parser.VariableInitializerListContext):
        pass


    # Enter a parse tree produced by Java9Parser#block.
    def enterBlock(self, ctx:Java9Parser.BlockContext):
        pass

    # Exit a parse tree produced by Java9Parser#block.
    def exitBlock(self, ctx:Java9Parser.BlockContext):
        pass


    # Enter a parse tree produced by Java9Parser#blockStatements.
    def enterBlockStatements(self, ctx:Java9Parser.BlockStatementsContext):
        pass

    # Exit a parse tree produced by Java9Parser#blockStatements.
    def exitBlockStatements(self, ctx:Java9Parser.BlockStatementsContext):
        pass


    # Enter a parse tree produced by Java9Parser#blockStatement.
    def enterBlockStatement(self, ctx:Java9Parser.BlockStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#blockStatement.
    def exitBlockStatement(self, ctx:Java9Parser.BlockStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#localVariableDeclarationStatement.
    def enterLocalVariableDeclarationStatement(self, ctx:Java9Parser.LocalVariableDeclarationStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#localVariableDeclarationStatement.
    def exitLocalVariableDeclarationStatement(self, ctx:Java9Parser.LocalVariableDeclarationStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#localVariableDeclaration.
    def enterLocalVariableDeclaration(self, ctx:Java9Parser.LocalVariableDeclarationContext):
        pass

    # Exit a parse tree produced by Java9Parser#localVariableDeclaration.
    def exitLocalVariableDeclaration(self, ctx:Java9Parser.LocalVariableDeclarationContext):
        pass


    # Enter a parse tree produced by Java9Parser#statement.
    def enterStatement(self, ctx:Java9Parser.StatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#statement.
    def exitStatement(self, ctx:Java9Parser.StatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#statementNoShortIf.
    def enterStatementNoShortIf(self, ctx:Java9Parser.StatementNoShortIfContext):
        pass

    # Exit a parse tree produced by Java9Parser#statementNoShortIf.
    def exitStatementNoShortIf(self, ctx:Java9Parser.StatementNoShortIfContext):
        pass


    # Enter a parse tree produced by Java9Parser#statementWithoutTrailingSubstatement.
    def enterStatementWithoutTrailingSubstatement(self, ctx:Java9Parser.StatementWithoutTrailingSubstatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#statementWithoutTrailingSubstatement.
    def exitStatementWithoutTrailingSubstatement(self, ctx:Java9Parser.StatementWithoutTrailingSubstatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#emptyStatement.
    def enterEmptyStatement(self, ctx:Java9Parser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#emptyStatement.
    def exitEmptyStatement(self, ctx:Java9Parser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#labeledStatement.
    def enterLabeledStatement(self, ctx:Java9Parser.LabeledStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#labeledStatement.
    def exitLabeledStatement(self, ctx:Java9Parser.LabeledStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#labeledStatementNoShortIf.
    def enterLabeledStatementNoShortIf(self, ctx:Java9Parser.LabeledStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by Java9Parser#labeledStatementNoShortIf.
    def exitLabeledStatementNoShortIf(self, ctx:Java9Parser.LabeledStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by Java9Parser#expressionStatement.
    def enterExpressionStatement(self, ctx:Java9Parser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#expressionStatement.
    def exitExpressionStatement(self, ctx:Java9Parser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#statementExpression.
    def enterStatementExpression(self, ctx:Java9Parser.StatementExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#statementExpression.
    def exitStatementExpression(self, ctx:Java9Parser.StatementExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#ifThenStatement.
    def enterIfThenStatement(self, ctx:Java9Parser.IfThenStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#ifThenStatement.
    def exitIfThenStatement(self, ctx:Java9Parser.IfThenStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#ifThenElseStatement.
    def enterIfThenElseStatement(self, ctx:Java9Parser.IfThenElseStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#ifThenElseStatement.
    def exitIfThenElseStatement(self, ctx:Java9Parser.IfThenElseStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#ifThenElseStatementNoShortIf.
    def enterIfThenElseStatementNoShortIf(self, ctx:Java9Parser.IfThenElseStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by Java9Parser#ifThenElseStatementNoShortIf.
    def exitIfThenElseStatementNoShortIf(self, ctx:Java9Parser.IfThenElseStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by Java9Parser#assertStatement.
    def enterAssertStatement(self, ctx:Java9Parser.AssertStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#assertStatement.
    def exitAssertStatement(self, ctx:Java9Parser.AssertStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#switchStatement.
    def enterSwitchStatement(self, ctx:Java9Parser.SwitchStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#switchStatement.
    def exitSwitchStatement(self, ctx:Java9Parser.SwitchStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#switchBlock.
    def enterSwitchBlock(self, ctx:Java9Parser.SwitchBlockContext):
        pass

    # Exit a parse tree produced by Java9Parser#switchBlock.
    def exitSwitchBlock(self, ctx:Java9Parser.SwitchBlockContext):
        pass


    # Enter a parse tree produced by Java9Parser#switchBlockStatementGroup.
    def enterSwitchBlockStatementGroup(self, ctx:Java9Parser.SwitchBlockStatementGroupContext):
        pass

    # Exit a parse tree produced by Java9Parser#switchBlockStatementGroup.
    def exitSwitchBlockStatementGroup(self, ctx:Java9Parser.SwitchBlockStatementGroupContext):
        pass


    # Enter a parse tree produced by Java9Parser#switchLabels.
    def enterSwitchLabels(self, ctx:Java9Parser.SwitchLabelsContext):
        pass

    # Exit a parse tree produced by Java9Parser#switchLabels.
    def exitSwitchLabels(self, ctx:Java9Parser.SwitchLabelsContext):
        pass


    # Enter a parse tree produced by Java9Parser#switchLabel.
    def enterSwitchLabel(self, ctx:Java9Parser.SwitchLabelContext):
        pass

    # Exit a parse tree produced by Java9Parser#switchLabel.
    def exitSwitchLabel(self, ctx:Java9Parser.SwitchLabelContext):
        pass


    # Enter a parse tree produced by Java9Parser#enumConstantName.
    def enterEnumConstantName(self, ctx:Java9Parser.EnumConstantNameContext):
        pass

    # Exit a parse tree produced by Java9Parser#enumConstantName.
    def exitEnumConstantName(self, ctx:Java9Parser.EnumConstantNameContext):
        pass


    # Enter a parse tree produced by Java9Parser#whileStatement.
    def enterWhileStatement(self, ctx:Java9Parser.WhileStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#whileStatement.
    def exitWhileStatement(self, ctx:Java9Parser.WhileStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#whileStatementNoShortIf.
    def enterWhileStatementNoShortIf(self, ctx:Java9Parser.WhileStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by Java9Parser#whileStatementNoShortIf.
    def exitWhileStatementNoShortIf(self, ctx:Java9Parser.WhileStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by Java9Parser#doStatement.
    def enterDoStatement(self, ctx:Java9Parser.DoStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#doStatement.
    def exitDoStatement(self, ctx:Java9Parser.DoStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#forStatement.
    def enterForStatement(self, ctx:Java9Parser.ForStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#forStatement.
    def exitForStatement(self, ctx:Java9Parser.ForStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#forStatementNoShortIf.
    def enterForStatementNoShortIf(self, ctx:Java9Parser.ForStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by Java9Parser#forStatementNoShortIf.
    def exitForStatementNoShortIf(self, ctx:Java9Parser.ForStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by Java9Parser#basicForStatement.
    def enterBasicForStatement(self, ctx:Java9Parser.BasicForStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#basicForStatement.
    def exitBasicForStatement(self, ctx:Java9Parser.BasicForStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#basicForStatementNoShortIf.
    def enterBasicForStatementNoShortIf(self, ctx:Java9Parser.BasicForStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by Java9Parser#basicForStatementNoShortIf.
    def exitBasicForStatementNoShortIf(self, ctx:Java9Parser.BasicForStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by Java9Parser#forInit.
    def enterForInit(self, ctx:Java9Parser.ForInitContext):
        pass

    # Exit a parse tree produced by Java9Parser#forInit.
    def exitForInit(self, ctx:Java9Parser.ForInitContext):
        pass


    # Enter a parse tree produced by Java9Parser#forUpdate.
    def enterForUpdate(self, ctx:Java9Parser.ForUpdateContext):
        pass

    # Exit a parse tree produced by Java9Parser#forUpdate.
    def exitForUpdate(self, ctx:Java9Parser.ForUpdateContext):
        pass


    # Enter a parse tree produced by Java9Parser#statementExpressionList.
    def enterStatementExpressionList(self, ctx:Java9Parser.StatementExpressionListContext):
        pass

    # Exit a parse tree produced by Java9Parser#statementExpressionList.
    def exitStatementExpressionList(self, ctx:Java9Parser.StatementExpressionListContext):
        pass


    # Enter a parse tree produced by Java9Parser#enhancedForStatement.
    def enterEnhancedForStatement(self, ctx:Java9Parser.EnhancedForStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#enhancedForStatement.
    def exitEnhancedForStatement(self, ctx:Java9Parser.EnhancedForStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#enhancedForStatementNoShortIf.
    def enterEnhancedForStatementNoShortIf(self, ctx:Java9Parser.EnhancedForStatementNoShortIfContext):
        pass

    # Exit a parse tree produced by Java9Parser#enhancedForStatementNoShortIf.
    def exitEnhancedForStatementNoShortIf(self, ctx:Java9Parser.EnhancedForStatementNoShortIfContext):
        pass


    # Enter a parse tree produced by Java9Parser#breakStatement.
    def enterBreakStatement(self, ctx:Java9Parser.BreakStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#breakStatement.
    def exitBreakStatement(self, ctx:Java9Parser.BreakStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#continueStatement.
    def enterContinueStatement(self, ctx:Java9Parser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#continueStatement.
    def exitContinueStatement(self, ctx:Java9Parser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#returnStatement.
    def enterReturnStatement(self, ctx:Java9Parser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#returnStatement.
    def exitReturnStatement(self, ctx:Java9Parser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#throwStatement.
    def enterThrowStatement(self, ctx:Java9Parser.ThrowStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#throwStatement.
    def exitThrowStatement(self, ctx:Java9Parser.ThrowStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#synchronizedStatement.
    def enterSynchronizedStatement(self, ctx:Java9Parser.SynchronizedStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#synchronizedStatement.
    def exitSynchronizedStatement(self, ctx:Java9Parser.SynchronizedStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#tryStatement.
    def enterTryStatement(self, ctx:Java9Parser.TryStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#tryStatement.
    def exitTryStatement(self, ctx:Java9Parser.TryStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#catches.
    def enterCatches(self, ctx:Java9Parser.CatchesContext):
        pass

    # Exit a parse tree produced by Java9Parser#catches.
    def exitCatches(self, ctx:Java9Parser.CatchesContext):
        pass


    # Enter a parse tree produced by Java9Parser#catchClause.
    def enterCatchClause(self, ctx:Java9Parser.CatchClauseContext):
        pass

    # Exit a parse tree produced by Java9Parser#catchClause.
    def exitCatchClause(self, ctx:Java9Parser.CatchClauseContext):
        pass


    # Enter a parse tree produced by Java9Parser#catchFormalParameter.
    def enterCatchFormalParameter(self, ctx:Java9Parser.CatchFormalParameterContext):
        pass

    # Exit a parse tree produced by Java9Parser#catchFormalParameter.
    def exitCatchFormalParameter(self, ctx:Java9Parser.CatchFormalParameterContext):
        pass


    # Enter a parse tree produced by Java9Parser#catchType.
    def enterCatchType(self, ctx:Java9Parser.CatchTypeContext):
        pass

    # Exit a parse tree produced by Java9Parser#catchType.
    def exitCatchType(self, ctx:Java9Parser.CatchTypeContext):
        pass


    # Enter a parse tree produced by Java9Parser#finally_.
    def enterFinally_(self, ctx:Java9Parser.Finally_Context):
        pass

    # Exit a parse tree produced by Java9Parser#finally_.
    def exitFinally_(self, ctx:Java9Parser.Finally_Context):
        pass


    # Enter a parse tree produced by Java9Parser#tryWithResourcesStatement.
    def enterTryWithResourcesStatement(self, ctx:Java9Parser.TryWithResourcesStatementContext):
        pass

    # Exit a parse tree produced by Java9Parser#tryWithResourcesStatement.
    def exitTryWithResourcesStatement(self, ctx:Java9Parser.TryWithResourcesStatementContext):
        pass


    # Enter a parse tree produced by Java9Parser#resourceSpecification.
    def enterResourceSpecification(self, ctx:Java9Parser.ResourceSpecificationContext):
        pass

    # Exit a parse tree produced by Java9Parser#resourceSpecification.
    def exitResourceSpecification(self, ctx:Java9Parser.ResourceSpecificationContext):
        pass


    # Enter a parse tree produced by Java9Parser#resourceList.
    def enterResourceList(self, ctx:Java9Parser.ResourceListContext):
        pass

    # Exit a parse tree produced by Java9Parser#resourceList.
    def exitResourceList(self, ctx:Java9Parser.ResourceListContext):
        pass


    # Enter a parse tree produced by Java9Parser#resource.
    def enterResource(self, ctx:Java9Parser.ResourceContext):
        pass

    # Exit a parse tree produced by Java9Parser#resource.
    def exitResource(self, ctx:Java9Parser.ResourceContext):
        pass


    # Enter a parse tree produced by Java9Parser#variableAccess.
    def enterVariableAccess(self, ctx:Java9Parser.VariableAccessContext):
        pass

    # Exit a parse tree produced by Java9Parser#variableAccess.
    def exitVariableAccess(self, ctx:Java9Parser.VariableAccessContext):
        pass


    # Enter a parse tree produced by Java9Parser#primary.
    def enterPrimary(self, ctx:Java9Parser.PrimaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#primary.
    def exitPrimary(self, ctx:Java9Parser.PrimaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray.
    def enterPrimaryNoNewArray(self, ctx:Java9Parser.PrimaryNoNewArrayContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray.
    def exitPrimaryNoNewArray(self, ctx:Java9Parser.PrimaryNoNewArrayContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray_lf_arrayAccess.
    def enterPrimaryNoNewArray_lf_arrayAccess(self, ctx:Java9Parser.PrimaryNoNewArray_lf_arrayAccessContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray_lf_arrayAccess.
    def exitPrimaryNoNewArray_lf_arrayAccess(self, ctx:Java9Parser.PrimaryNoNewArray_lf_arrayAccessContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray_lfno_arrayAccess.
    def enterPrimaryNoNewArray_lfno_arrayAccess(self, ctx:Java9Parser.PrimaryNoNewArray_lfno_arrayAccessContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray_lfno_arrayAccess.
    def exitPrimaryNoNewArray_lfno_arrayAccess(self, ctx:Java9Parser.PrimaryNoNewArray_lfno_arrayAccessContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray_lf_primary.
    def enterPrimaryNoNewArray_lf_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lf_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray_lf_primary.
    def exitPrimaryNoNewArray_lf_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lf_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary.
    def enterPrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary.
    def exitPrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary.
    def enterPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary.
    def exitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray_lfno_primary.
    def enterPrimaryNoNewArray_lfno_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lfno_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray_lfno_primary.
    def exitPrimaryNoNewArray_lfno_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lfno_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary.
    def enterPrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary.
    def exitPrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary.
    def enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary.
    def exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary(self, ctx:Java9Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#classLiteral.
    def enterClassLiteral(self, ctx:Java9Parser.ClassLiteralContext):
        pass

    # Exit a parse tree produced by Java9Parser#classLiteral.
    def exitClassLiteral(self, ctx:Java9Parser.ClassLiteralContext):
        pass


    # Enter a parse tree produced by Java9Parser#classInstanceCreationExpression.
    def enterClassInstanceCreationExpression(self, ctx:Java9Parser.ClassInstanceCreationExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#classInstanceCreationExpression.
    def exitClassInstanceCreationExpression(self, ctx:Java9Parser.ClassInstanceCreationExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#classInstanceCreationExpression_lf_primary.
    def enterClassInstanceCreationExpression_lf_primary(self, ctx:Java9Parser.ClassInstanceCreationExpression_lf_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#classInstanceCreationExpression_lf_primary.
    def exitClassInstanceCreationExpression_lf_primary(self, ctx:Java9Parser.ClassInstanceCreationExpression_lf_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#classInstanceCreationExpression_lfno_primary.
    def enterClassInstanceCreationExpression_lfno_primary(self, ctx:Java9Parser.ClassInstanceCreationExpression_lfno_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#classInstanceCreationExpression_lfno_primary.
    def exitClassInstanceCreationExpression_lfno_primary(self, ctx:Java9Parser.ClassInstanceCreationExpression_lfno_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#typeArgumentsOrDiamond.
    def enterTypeArgumentsOrDiamond(self, ctx:Java9Parser.TypeArgumentsOrDiamondContext):
        pass

    # Exit a parse tree produced by Java9Parser#typeArgumentsOrDiamond.
    def exitTypeArgumentsOrDiamond(self, ctx:Java9Parser.TypeArgumentsOrDiamondContext):
        pass


    # Enter a parse tree produced by Java9Parser#fieldAccess.
    def enterFieldAccess(self, ctx:Java9Parser.FieldAccessContext):
        pass

    # Exit a parse tree produced by Java9Parser#fieldAccess.
    def exitFieldAccess(self, ctx:Java9Parser.FieldAccessContext):
        pass


    # Enter a parse tree produced by Java9Parser#fieldAccess_lf_primary.
    def enterFieldAccess_lf_primary(self, ctx:Java9Parser.FieldAccess_lf_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#fieldAccess_lf_primary.
    def exitFieldAccess_lf_primary(self, ctx:Java9Parser.FieldAccess_lf_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#fieldAccess_lfno_primary.
    def enterFieldAccess_lfno_primary(self, ctx:Java9Parser.FieldAccess_lfno_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#fieldAccess_lfno_primary.
    def exitFieldAccess_lfno_primary(self, ctx:Java9Parser.FieldAccess_lfno_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#arrayAccess.
    def enterArrayAccess(self, ctx:Java9Parser.ArrayAccessContext):
        pass

    # Exit a parse tree produced by Java9Parser#arrayAccess.
    def exitArrayAccess(self, ctx:Java9Parser.ArrayAccessContext):
        pass


    # Enter a parse tree produced by Java9Parser#arrayAccess_lf_primary.
    def enterArrayAccess_lf_primary(self, ctx:Java9Parser.ArrayAccess_lf_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#arrayAccess_lf_primary.
    def exitArrayAccess_lf_primary(self, ctx:Java9Parser.ArrayAccess_lf_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#arrayAccess_lfno_primary.
    def enterArrayAccess_lfno_primary(self, ctx:Java9Parser.ArrayAccess_lfno_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#arrayAccess_lfno_primary.
    def exitArrayAccess_lfno_primary(self, ctx:Java9Parser.ArrayAccess_lfno_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodInvocation.
    def enterMethodInvocation(self, ctx:Java9Parser.MethodInvocationContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodInvocation.
    def exitMethodInvocation(self, ctx:Java9Parser.MethodInvocationContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodInvocation_lf_primary.
    def enterMethodInvocation_lf_primary(self, ctx:Java9Parser.MethodInvocation_lf_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodInvocation_lf_primary.
    def exitMethodInvocation_lf_primary(self, ctx:Java9Parser.MethodInvocation_lf_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodInvocation_lfno_primary.
    def enterMethodInvocation_lfno_primary(self, ctx:Java9Parser.MethodInvocation_lfno_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodInvocation_lfno_primary.
    def exitMethodInvocation_lfno_primary(self, ctx:Java9Parser.MethodInvocation_lfno_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#argumentList.
    def enterArgumentList(self, ctx:Java9Parser.ArgumentListContext):
        pass

    # Exit a parse tree produced by Java9Parser#argumentList.
    def exitArgumentList(self, ctx:Java9Parser.ArgumentListContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodReference.
    def enterMethodReference(self, ctx:Java9Parser.MethodReferenceContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodReference.
    def exitMethodReference(self, ctx:Java9Parser.MethodReferenceContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodReference_lf_primary.
    def enterMethodReference_lf_primary(self, ctx:Java9Parser.MethodReference_lf_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodReference_lf_primary.
    def exitMethodReference_lf_primary(self, ctx:Java9Parser.MethodReference_lf_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#methodReference_lfno_primary.
    def enterMethodReference_lfno_primary(self, ctx:Java9Parser.MethodReference_lfno_primaryContext):
        pass

    # Exit a parse tree produced by Java9Parser#methodReference_lfno_primary.
    def exitMethodReference_lfno_primary(self, ctx:Java9Parser.MethodReference_lfno_primaryContext):
        pass


    # Enter a parse tree produced by Java9Parser#arrayCreationExpression.
    def enterArrayCreationExpression(self, ctx:Java9Parser.ArrayCreationExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#arrayCreationExpression.
    def exitArrayCreationExpression(self, ctx:Java9Parser.ArrayCreationExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#dimExprs.
    def enterDimExprs(self, ctx:Java9Parser.DimExprsContext):
        pass

    # Exit a parse tree produced by Java9Parser#dimExprs.
    def exitDimExprs(self, ctx:Java9Parser.DimExprsContext):
        pass


    # Enter a parse tree produced by Java9Parser#dimExpr.
    def enterDimExpr(self, ctx:Java9Parser.DimExprContext):
        pass

    # Exit a parse tree produced by Java9Parser#dimExpr.
    def exitDimExpr(self, ctx:Java9Parser.DimExprContext):
        pass


    # Enter a parse tree produced by Java9Parser#constantExpression.
    def enterConstantExpression(self, ctx:Java9Parser.ConstantExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#constantExpression.
    def exitConstantExpression(self, ctx:Java9Parser.ConstantExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#expression.
    def enterExpression(self, ctx:Java9Parser.ExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#expression.
    def exitExpression(self, ctx:Java9Parser.ExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#lambdaExpression.
    def enterLambdaExpression(self, ctx:Java9Parser.LambdaExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#lambdaExpression.
    def exitLambdaExpression(self, ctx:Java9Parser.LambdaExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#lambdaParameters.
    def enterLambdaParameters(self, ctx:Java9Parser.LambdaParametersContext):
        pass

    # Exit a parse tree produced by Java9Parser#lambdaParameters.
    def exitLambdaParameters(self, ctx:Java9Parser.LambdaParametersContext):
        pass


    # Enter a parse tree produced by Java9Parser#inferredFormalParameterList.
    def enterInferredFormalParameterList(self, ctx:Java9Parser.InferredFormalParameterListContext):
        pass

    # Exit a parse tree produced by Java9Parser#inferredFormalParameterList.
    def exitInferredFormalParameterList(self, ctx:Java9Parser.InferredFormalParameterListContext):
        pass


    # Enter a parse tree produced by Java9Parser#lambdaBody.
    def enterLambdaBody(self, ctx:Java9Parser.LambdaBodyContext):
        pass

    # Exit a parse tree produced by Java9Parser#lambdaBody.
    def exitLambdaBody(self, ctx:Java9Parser.LambdaBodyContext):
        pass


    # Enter a parse tree produced by Java9Parser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:Java9Parser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:Java9Parser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#assignment.
    def enterAssignment(self, ctx:Java9Parser.AssignmentContext):
        pass

    # Exit a parse tree produced by Java9Parser#assignment.
    def exitAssignment(self, ctx:Java9Parser.AssignmentContext):
        pass


    # Enter a parse tree produced by Java9Parser#leftHandSide.
    def enterLeftHandSide(self, ctx:Java9Parser.LeftHandSideContext):
        pass

    # Exit a parse tree produced by Java9Parser#leftHandSide.
    def exitLeftHandSide(self, ctx:Java9Parser.LeftHandSideContext):
        pass


    # Enter a parse tree produced by Java9Parser#assignmentOperator.
    def enterAssignmentOperator(self, ctx:Java9Parser.AssignmentOperatorContext):
        pass

    # Exit a parse tree produced by Java9Parser#assignmentOperator.
    def exitAssignmentOperator(self, ctx:Java9Parser.AssignmentOperatorContext):
        pass


    # Enter a parse tree produced by Java9Parser#conditionalExpression.
    def enterConditionalExpression(self, ctx:Java9Parser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#conditionalExpression.
    def exitConditionalExpression(self, ctx:Java9Parser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#conditionalOrExpression.
    def enterConditionalOrExpression(self, ctx:Java9Parser.ConditionalOrExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#conditionalOrExpression.
    def exitConditionalOrExpression(self, ctx:Java9Parser.ConditionalOrExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#conditionalAndExpression.
    def enterConditionalAndExpression(self, ctx:Java9Parser.ConditionalAndExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#conditionalAndExpression.
    def exitConditionalAndExpression(self, ctx:Java9Parser.ConditionalAndExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#inclusiveOrExpression.
    def enterInclusiveOrExpression(self, ctx:Java9Parser.InclusiveOrExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#inclusiveOrExpression.
    def exitInclusiveOrExpression(self, ctx:Java9Parser.InclusiveOrExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#exclusiveOrExpression.
    def enterExclusiveOrExpression(self, ctx:Java9Parser.ExclusiveOrExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#exclusiveOrExpression.
    def exitExclusiveOrExpression(self, ctx:Java9Parser.ExclusiveOrExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#andExpression.
    def enterAndExpression(self, ctx:Java9Parser.AndExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#andExpression.
    def exitAndExpression(self, ctx:Java9Parser.AndExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#equalityExpression.
    def enterEqualityExpression(self, ctx:Java9Parser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#equalityExpression.
    def exitEqualityExpression(self, ctx:Java9Parser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#relationalExpression.
    def enterRelationalExpression(self, ctx:Java9Parser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#relationalExpression.
    def exitRelationalExpression(self, ctx:Java9Parser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#shiftExpression.
    def enterShiftExpression(self, ctx:Java9Parser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#shiftExpression.
    def exitShiftExpression(self, ctx:Java9Parser.ShiftExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#additiveExpression.
    def enterAdditiveExpression(self, ctx:Java9Parser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#additiveExpression.
    def exitAdditiveExpression(self, ctx:Java9Parser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:Java9Parser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:Java9Parser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#unaryExpression.
    def enterUnaryExpression(self, ctx:Java9Parser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#unaryExpression.
    def exitUnaryExpression(self, ctx:Java9Parser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#preIncrementExpression.
    def enterPreIncrementExpression(self, ctx:Java9Parser.PreIncrementExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#preIncrementExpression.
    def exitPreIncrementExpression(self, ctx:Java9Parser.PreIncrementExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#preDecrementExpression.
    def enterPreDecrementExpression(self, ctx:Java9Parser.PreDecrementExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#preDecrementExpression.
    def exitPreDecrementExpression(self, ctx:Java9Parser.PreDecrementExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#unaryExpressionNotPlusMinus.
    def enterUnaryExpressionNotPlusMinus(self, ctx:Java9Parser.UnaryExpressionNotPlusMinusContext):
        pass

    # Exit a parse tree produced by Java9Parser#unaryExpressionNotPlusMinus.
    def exitUnaryExpressionNotPlusMinus(self, ctx:Java9Parser.UnaryExpressionNotPlusMinusContext):
        pass


    # Enter a parse tree produced by Java9Parser#postfixExpression.
    def enterPostfixExpression(self, ctx:Java9Parser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#postfixExpression.
    def exitPostfixExpression(self, ctx:Java9Parser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#postIncrementExpression.
    def enterPostIncrementExpression(self, ctx:Java9Parser.PostIncrementExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#postIncrementExpression.
    def exitPostIncrementExpression(self, ctx:Java9Parser.PostIncrementExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#postIncrementExpression_lf_postfixExpression.
    def enterPostIncrementExpression_lf_postfixExpression(self, ctx:Java9Parser.PostIncrementExpression_lf_postfixExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#postIncrementExpression_lf_postfixExpression.
    def exitPostIncrementExpression_lf_postfixExpression(self, ctx:Java9Parser.PostIncrementExpression_lf_postfixExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#postDecrementExpression.
    def enterPostDecrementExpression(self, ctx:Java9Parser.PostDecrementExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#postDecrementExpression.
    def exitPostDecrementExpression(self, ctx:Java9Parser.PostDecrementExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#postDecrementExpression_lf_postfixExpression.
    def enterPostDecrementExpression_lf_postfixExpression(self, ctx:Java9Parser.PostDecrementExpression_lf_postfixExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#postDecrementExpression_lf_postfixExpression.
    def exitPostDecrementExpression_lf_postfixExpression(self, ctx:Java9Parser.PostDecrementExpression_lf_postfixExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#castExpression.
    def enterCastExpression(self, ctx:Java9Parser.CastExpressionContext):
        pass

    # Exit a parse tree produced by Java9Parser#castExpression.
    def exitCastExpression(self, ctx:Java9Parser.CastExpressionContext):
        pass


    # Enter a parse tree produced by Java9Parser#identifier.
    def enterIdentifier(self, ctx:Java9Parser.IdentifierContext):
        pass

    # Exit a parse tree produced by Java9Parser#identifier.
    def exitIdentifier(self, ctx:Java9Parser.IdentifierContext):
        pass



del Java9Parser