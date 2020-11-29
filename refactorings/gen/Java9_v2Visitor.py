# Generated from D:/AnacondaProjects/iust_compilers_teaching/grammars\Java9_v2.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Java9_v2Parser import Java9_v2Parser
else:
    from Java9_v2Parser import Java9_v2Parser

# This class defines a complete generic visitor for a parse tree produced by Java9_v2Parser.

class Java9_v2Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by Java9_v2Parser#literal.
    def visitLiteral(self, ctx:Java9_v2Parser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primitiveType1.
    def visitPrimitiveType1(self, ctx:Java9_v2Parser.PrimitiveType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primitiveType2.
    def visitPrimitiveType2(self, ctx:Java9_v2Parser.PrimitiveType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#numericType1.
    def visitNumericType1(self, ctx:Java9_v2Parser.NumericType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#numericType2.
    def visitNumericType2(self, ctx:Java9_v2Parser.NumericType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#integralType.
    def visitIntegralType(self, ctx:Java9_v2Parser.IntegralTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#floatingPointType.
    def visitFloatingPointType(self, ctx:Java9_v2Parser.FloatingPointTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#referenceType1.
    def visitReferenceType1(self, ctx:Java9_v2Parser.ReferenceType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#referenceType2.
    def visitReferenceType2(self, ctx:Java9_v2Parser.ReferenceType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#referenceType3.
    def visitReferenceType3(self, ctx:Java9_v2Parser.ReferenceType3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classOrInterfaceType.
    def visitClassOrInterfaceType(self, ctx:Java9_v2Parser.ClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classType1.
    def visitClassType1(self, ctx:Java9_v2Parser.ClassType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classType2.
    def visitClassType2(self, ctx:Java9_v2Parser.ClassType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classType_lf_classOrInterfaceType.
    def visitClassType_lf_classOrInterfaceType(self, ctx:Java9_v2Parser.ClassType_lf_classOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classType_lfno_classOrInterfaceType.
    def visitClassType_lfno_classOrInterfaceType(self, ctx:Java9_v2Parser.ClassType_lfno_classOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceType.
    def visitInterfaceType(self, ctx:Java9_v2Parser.InterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceType_lf_classOrInterfaceType.
    def visitInterfaceType_lf_classOrInterfaceType(self, ctx:Java9_v2Parser.InterfaceType_lf_classOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceType_lfno_classOrInterfaceType.
    def visitInterfaceType_lfno_classOrInterfaceType(self, ctx:Java9_v2Parser.InterfaceType_lfno_classOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeVariable.
    def visitTypeVariable(self, ctx:Java9_v2Parser.TypeVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayType1.
    def visitArrayType1(self, ctx:Java9_v2Parser.ArrayType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayType2.
    def visitArrayType2(self, ctx:Java9_v2Parser.ArrayType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayTyp3.
    def visitArrayTyp3(self, ctx:Java9_v2Parser.ArrayTyp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#dims.
    def visitDims(self, ctx:Java9_v2Parser.DimsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeParameter.
    def visitTypeParameter(self, ctx:Java9_v2Parser.TypeParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeParameterModifier.
    def visitTypeParameterModifier(self, ctx:Java9_v2Parser.TypeParameterModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeBound1.
    def visitTypeBound1(self, ctx:Java9_v2Parser.TypeBound1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeBound2.
    def visitTypeBound2(self, ctx:Java9_v2Parser.TypeBound2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#additionalBound.
    def visitAdditionalBound(self, ctx:Java9_v2Parser.AdditionalBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeArguments.
    def visitTypeArguments(self, ctx:Java9_v2Parser.TypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeArgumentList.
    def visitTypeArgumentList(self, ctx:Java9_v2Parser.TypeArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeArgument1.
    def visitTypeArgument1(self, ctx:Java9_v2Parser.TypeArgument1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeArgument2.
    def visitTypeArgument2(self, ctx:Java9_v2Parser.TypeArgument2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#wildcard.
    def visitWildcard(self, ctx:Java9_v2Parser.WildcardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#wildcardBounds1.
    def visitWildcardBounds1(self, ctx:Java9_v2Parser.WildcardBounds1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#wildcardBound2.
    def visitWildcardBound2(self, ctx:Java9_v2Parser.WildcardBound2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#moduleName1.
    def visitModuleName1(self, ctx:Java9_v2Parser.ModuleName1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#moduleName2.
    def visitModuleName2(self, ctx:Java9_v2Parser.ModuleName2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#packageName2.
    def visitPackageName2(self, ctx:Java9_v2Parser.PackageName2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#packageName1.
    def visitPackageName1(self, ctx:Java9_v2Parser.PackageName1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeName1.
    def visitTypeName1(self, ctx:Java9_v2Parser.TypeName1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeName2.
    def visitTypeName2(self, ctx:Java9_v2Parser.TypeName2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#packageOrTypeName1.
    def visitPackageOrTypeName1(self, ctx:Java9_v2Parser.PackageOrTypeName1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#packageOrTypeName2.
    def visitPackageOrTypeName2(self, ctx:Java9_v2Parser.PackageOrTypeName2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#expressionName1.
    def visitExpressionName1(self, ctx:Java9_v2Parser.ExpressionName1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#expressionName2.
    def visitExpressionName2(self, ctx:Java9_v2Parser.ExpressionName2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodName.
    def visitMethodName(self, ctx:Java9_v2Parser.MethodNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#ambiguousName1.
    def visitAmbiguousName1(self, ctx:Java9_v2Parser.AmbiguousName1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#ambiguousName2.
    def visitAmbiguousName2(self, ctx:Java9_v2Parser.AmbiguousName2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#compilationUnit1.
    def visitCompilationUnit1(self, ctx:Java9_v2Parser.CompilationUnit1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#compilationUnit2.
    def visitCompilationUnit2(self, ctx:Java9_v2Parser.CompilationUnit2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#ordinaryCompilation.
    def visitOrdinaryCompilation(self, ctx:Java9_v2Parser.OrdinaryCompilationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#modularCompilation.
    def visitModularCompilation(self, ctx:Java9_v2Parser.ModularCompilationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#packageDeclaration.
    def visitPackageDeclaration(self, ctx:Java9_v2Parser.PackageDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#packageModifier.
    def visitPackageModifier(self, ctx:Java9_v2Parser.PackageModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#importDeclaration1.
    def visitImportDeclaration1(self, ctx:Java9_v2Parser.ImportDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#importDeclaration2.
    def visitImportDeclaration2(self, ctx:Java9_v2Parser.ImportDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#importDeclaration3.
    def visitImportDeclaration3(self, ctx:Java9_v2Parser.ImportDeclaration3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#importDeclaration4.
    def visitImportDeclaration4(self, ctx:Java9_v2Parser.ImportDeclaration4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#singleTypeImportDeclaration.
    def visitSingleTypeImportDeclaration(self, ctx:Java9_v2Parser.SingleTypeImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeImportOnDemandDeclaration.
    def visitTypeImportOnDemandDeclaration(self, ctx:Java9_v2Parser.TypeImportOnDemandDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#singleStaticImportDeclaration.
    def visitSingleStaticImportDeclaration(self, ctx:Java9_v2Parser.SingleStaticImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#staticImportOnDemandDeclaration.
    def visitStaticImportOnDemandDeclaration(self, ctx:Java9_v2Parser.StaticImportOnDemandDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeDeclaration1.
    def visitTypeDeclaration1(self, ctx:Java9_v2Parser.TypeDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeDeclaration2.
    def visitTypeDeclaration2(self, ctx:Java9_v2Parser.TypeDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeDeclaration3.
    def visitTypeDeclaration3(self, ctx:Java9_v2Parser.TypeDeclaration3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#moduleDeclaration.
    def visitModuleDeclaration(self, ctx:Java9_v2Parser.ModuleDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#moduleDirective1.
    def visitModuleDirective1(self, ctx:Java9_v2Parser.ModuleDirective1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#moduleDirective2.
    def visitModuleDirective2(self, ctx:Java9_v2Parser.ModuleDirective2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#moduleDirectiv3.
    def visitModuleDirectiv3(self, ctx:Java9_v2Parser.ModuleDirectiv3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#moduleDirective4.
    def visitModuleDirective4(self, ctx:Java9_v2Parser.ModuleDirective4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#moduleDirective5.
    def visitModuleDirective5(self, ctx:Java9_v2Parser.ModuleDirective5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#requiresModifier.
    def visitRequiresModifier(self, ctx:Java9_v2Parser.RequiresModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classDeclaration1.
    def visitClassDeclaration1(self, ctx:Java9_v2Parser.ClassDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classDeclaration2.
    def visitClassDeclaration2(self, ctx:Java9_v2Parser.ClassDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#normalClassDeclaration.
    def visitNormalClassDeclaration(self, ctx:Java9_v2Parser.NormalClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classModifier.
    def visitClassModifier(self, ctx:Java9_v2Parser.ClassModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeParameters.
    def visitTypeParameters(self, ctx:Java9_v2Parser.TypeParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeParameterList.
    def visitTypeParameterList(self, ctx:Java9_v2Parser.TypeParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#superclass.
    def visitSuperclass(self, ctx:Java9_v2Parser.SuperclassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#superinterfaces.
    def visitSuperinterfaces(self, ctx:Java9_v2Parser.SuperinterfacesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceTypeList.
    def visitInterfaceTypeList(self, ctx:Java9_v2Parser.InterfaceTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classBody.
    def visitClassBody(self, ctx:Java9_v2Parser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classBodyDeclaration1.
    def visitClassBodyDeclaration1(self, ctx:Java9_v2Parser.ClassBodyDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classBodyDeclaration2.
    def visitClassBodyDeclaration2(self, ctx:Java9_v2Parser.ClassBodyDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classBodyDeclaration3.
    def visitClassBodyDeclaration3(self, ctx:Java9_v2Parser.ClassBodyDeclaration3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classBodyDeclaration4.
    def visitClassBodyDeclaration4(self, ctx:Java9_v2Parser.ClassBodyDeclaration4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classMemberDeclaration1.
    def visitClassMemberDeclaration1(self, ctx:Java9_v2Parser.ClassMemberDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classMemberDeclaration2.
    def visitClassMemberDeclaration2(self, ctx:Java9_v2Parser.ClassMemberDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classMemberDeclaration3.
    def visitClassMemberDeclaration3(self, ctx:Java9_v2Parser.ClassMemberDeclaration3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classMemberDeclaration4.
    def visitClassMemberDeclaration4(self, ctx:Java9_v2Parser.ClassMemberDeclaration4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classMemberDeclaration5.
    def visitClassMemberDeclaration5(self, ctx:Java9_v2Parser.ClassMemberDeclaration5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx:Java9_v2Parser.FieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#fieldModifier.
    def visitFieldModifier(self, ctx:Java9_v2Parser.FieldModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableDeclaratorList.
    def visitVariableDeclaratorList(self, ctx:Java9_v2Parser.VariableDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableDeclarator.
    def visitVariableDeclarator(self, ctx:Java9_v2Parser.VariableDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableDeclaratorId.
    def visitVariableDeclaratorId(self, ctx:Java9_v2Parser.VariableDeclaratorIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableInitializer1.
    def visitVariableInitializer1(self, ctx:Java9_v2Parser.VariableInitializer1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableInitializer2.
    def visitVariableInitializer2(self, ctx:Java9_v2Parser.VariableInitializer2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannType1.
    def visitUnannType1(self, ctx:Java9_v2Parser.UnannType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannType2.
    def visitUnannType2(self, ctx:Java9_v2Parser.UnannType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannPrimitiveType1.
    def visitUnannPrimitiveType1(self, ctx:Java9_v2Parser.UnannPrimitiveType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannPrimitiveType2.
    def visitUnannPrimitiveType2(self, ctx:Java9_v2Parser.UnannPrimitiveType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannReferenceType1.
    def visitUnannReferenceType1(self, ctx:Java9_v2Parser.UnannReferenceType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannReferenceType2.
    def visitUnannReferenceType2(self, ctx:Java9_v2Parser.UnannReferenceType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannReferenceType3.
    def visitUnannReferenceType3(self, ctx:Java9_v2Parser.UnannReferenceType3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannClassOrInterfaceType.
    def visitUnannClassOrInterfaceType(self, ctx:Java9_v2Parser.UnannClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannClassType1.
    def visitUnannClassType1(self, ctx:Java9_v2Parser.UnannClassType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannClassType2.
    def visitUnannClassType2(self, ctx:Java9_v2Parser.UnannClassType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannClassType_lf_unannClassOrInterfaceType.
    def visitUnannClassType_lf_unannClassOrInterfaceType(self, ctx:Java9_v2Parser.UnannClassType_lf_unannClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannClassType_lfno_unannClassOrInterfaceType.
    def visitUnannClassType_lfno_unannClassOrInterfaceType(self, ctx:Java9_v2Parser.UnannClassType_lfno_unannClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannInterfaceType.
    def visitUnannInterfaceType(self, ctx:Java9_v2Parser.UnannInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannInterfaceType_lf_unannClassOrInterfaceType.
    def visitUnannInterfaceType_lf_unannClassOrInterfaceType(self, ctx:Java9_v2Parser.UnannInterfaceType_lf_unannClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannInterfaceType_lfno_unannClassOrInterfaceType.
    def visitUnannInterfaceType_lfno_unannClassOrInterfaceType(self, ctx:Java9_v2Parser.UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannTypeVariable.
    def visitUnannTypeVariable(self, ctx:Java9_v2Parser.UnannTypeVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannArrayType1.
    def visitUnannArrayType1(self, ctx:Java9_v2Parser.UnannArrayType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannArrayType2.
    def visitUnannArrayType2(self, ctx:Java9_v2Parser.UnannArrayType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unannArrayTyp3.
    def visitUnannArrayTyp3(self, ctx:Java9_v2Parser.UnannArrayTyp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:Java9_v2Parser.MethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodModifier.
    def visitMethodModifier(self, ctx:Java9_v2Parser.MethodModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodHeader.
    def visitMethodHeader(self, ctx:Java9_v2Parser.MethodHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#result.
    def visitResult(self, ctx:Java9_v2Parser.ResultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodDeclarator.
    def visitMethodDeclarator(self, ctx:Java9_v2Parser.MethodDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#formalParameterList1.
    def visitFormalParameterList1(self, ctx:Java9_v2Parser.FormalParameterList1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#formalParameterList2.
    def visitFormalParameterList2(self, ctx:Java9_v2Parser.FormalParameterList2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#formalParameterList3.
    def visitFormalParameterList3(self, ctx:Java9_v2Parser.FormalParameterList3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#formalParameters1.
    def visitFormalParameters1(self, ctx:Java9_v2Parser.FormalParameters1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#formalParameters2.
    def visitFormalParameters2(self, ctx:Java9_v2Parser.FormalParameters2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#formalParameter.
    def visitFormalParameter(self, ctx:Java9_v2Parser.FormalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableModifier.
    def visitVariableModifier(self, ctx:Java9_v2Parser.VariableModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#lastFormalParameter1.
    def visitLastFormalParameter1(self, ctx:Java9_v2Parser.LastFormalParameter1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#lastFormalParameter2.
    def visitLastFormalParameter2(self, ctx:Java9_v2Parser.LastFormalParameter2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#receiverParameter.
    def visitReceiverParameter(self, ctx:Java9_v2Parser.ReceiverParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#throws_.
    def visitThrows_(self, ctx:Java9_v2Parser.Throws_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#exceptionTypeList.
    def visitExceptionTypeList(self, ctx:Java9_v2Parser.ExceptionTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#exceptionType1.
    def visitExceptionType1(self, ctx:Java9_v2Parser.ExceptionType1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#exceptionType2.
    def visitExceptionType2(self, ctx:Java9_v2Parser.ExceptionType2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodBody.
    def visitMethodBody(self, ctx:Java9_v2Parser.MethodBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#instanceInitializer.
    def visitInstanceInitializer(self, ctx:Java9_v2Parser.InstanceInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#staticInitializer.
    def visitStaticInitializer(self, ctx:Java9_v2Parser.StaticInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx:Java9_v2Parser.ConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#constructorModifier.
    def visitConstructorModifier(self, ctx:Java9_v2Parser.ConstructorModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#constructorDeclarator.
    def visitConstructorDeclarator(self, ctx:Java9_v2Parser.ConstructorDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#simpleTypeName.
    def visitSimpleTypeName(self, ctx:Java9_v2Parser.SimpleTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#constructorBody.
    def visitConstructorBody(self, ctx:Java9_v2Parser.ConstructorBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#explicitConstructorInvocation1.
    def visitExplicitConstructorInvocation1(self, ctx:Java9_v2Parser.ExplicitConstructorInvocation1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#explicitConstructorInvocation2.
    def visitExplicitConstructorInvocation2(self, ctx:Java9_v2Parser.ExplicitConstructorInvocation2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#explicitConstructorInvocation3.
    def visitExplicitConstructorInvocation3(self, ctx:Java9_v2Parser.ExplicitConstructorInvocation3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#explicitConstructorInvocation4.
    def visitExplicitConstructorInvocation4(self, ctx:Java9_v2Parser.ExplicitConstructorInvocation4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:Java9_v2Parser.EnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enumBody.
    def visitEnumBody(self, ctx:Java9_v2Parser.EnumBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enumConstantList.
    def visitEnumConstantList(self, ctx:Java9_v2Parser.EnumConstantListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enumConstant.
    def visitEnumConstant(self, ctx:Java9_v2Parser.EnumConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enumConstantModifier.
    def visitEnumConstantModifier(self, ctx:Java9_v2Parser.EnumConstantModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enumBodyDeclarations.
    def visitEnumBodyDeclarations(self, ctx:Java9_v2Parser.EnumBodyDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceDeclaration1.
    def visitInterfaceDeclaration1(self, ctx:Java9_v2Parser.InterfaceDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceDeclaration2.
    def visitInterfaceDeclaration2(self, ctx:Java9_v2Parser.InterfaceDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#normalInterfaceDeclaration.
    def visitNormalInterfaceDeclaration(self, ctx:Java9_v2Parser.NormalInterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceModifier.
    def visitInterfaceModifier(self, ctx:Java9_v2Parser.InterfaceModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#extendsInterfaces.
    def visitExtendsInterfaces(self, ctx:Java9_v2Parser.ExtendsInterfacesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceBody.
    def visitInterfaceBody(self, ctx:Java9_v2Parser.InterfaceBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceMemberDeclaration1.
    def visitInterfaceMemberDeclaration1(self, ctx:Java9_v2Parser.InterfaceMemberDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceMemberDeclaration2.
    def visitInterfaceMemberDeclaration2(self, ctx:Java9_v2Parser.InterfaceMemberDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceMemberDeclaration3.
    def visitInterfaceMemberDeclaration3(self, ctx:Java9_v2Parser.InterfaceMemberDeclaration3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceMemberDeclaration4.
    def visitInterfaceMemberDeclaration4(self, ctx:Java9_v2Parser.InterfaceMemberDeclaration4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceMemberDeclaration5.
    def visitInterfaceMemberDeclaration5(self, ctx:Java9_v2Parser.InterfaceMemberDeclaration5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#constantDeclaration.
    def visitConstantDeclaration(self, ctx:Java9_v2Parser.ConstantDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#constantModifier.
    def visitConstantModifier(self, ctx:Java9_v2Parser.ConstantModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceMethodDeclaration.
    def visitInterfaceMethodDeclaration(self, ctx:Java9_v2Parser.InterfaceMethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#interfaceMethodModifier.
    def visitInterfaceMethodModifier(self, ctx:Java9_v2Parser.InterfaceMethodModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeDeclaration.
    def visitAnnotationTypeDeclaration(self, ctx:Java9_v2Parser.AnnotationTypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeBody.
    def visitAnnotationTypeBody(self, ctx:Java9_v2Parser.AnnotationTypeBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeMemberDeclaration1.
    def visitAnnotationTypeMemberDeclaration1(self, ctx:Java9_v2Parser.AnnotationTypeMemberDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeMemberDeclaration2.
    def visitAnnotationTypeMemberDeclaration2(self, ctx:Java9_v2Parser.AnnotationTypeMemberDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeMemberDeclaration3.
    def visitAnnotationTypeMemberDeclaration3(self, ctx:Java9_v2Parser.AnnotationTypeMemberDeclaration3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeMemberDeclaration4.
    def visitAnnotationTypeMemberDeclaration4(self, ctx:Java9_v2Parser.AnnotationTypeMemberDeclaration4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeMemberDeclaration5.
    def visitAnnotationTypeMemberDeclaration5(self, ctx:Java9_v2Parser.AnnotationTypeMemberDeclaration5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeElementDeclaration.
    def visitAnnotationTypeElementDeclaration(self, ctx:Java9_v2Parser.AnnotationTypeElementDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotationTypeElementModifier.
    def visitAnnotationTypeElementModifier(self, ctx:Java9_v2Parser.AnnotationTypeElementModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#defaultValue.
    def visitDefaultValue(self, ctx:Java9_v2Parser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotation1.
    def visitAnnotation1(self, ctx:Java9_v2Parser.Annotation1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotation2.
    def visitAnnotation2(self, ctx:Java9_v2Parser.Annotation2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#annotation3.
    def visitAnnotation3(self, ctx:Java9_v2Parser.Annotation3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#normalAnnotation.
    def visitNormalAnnotation(self, ctx:Java9_v2Parser.NormalAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#elementValuePairList.
    def visitElementValuePairList(self, ctx:Java9_v2Parser.ElementValuePairListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#elementValuePair.
    def visitElementValuePair(self, ctx:Java9_v2Parser.ElementValuePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#elementValue1.
    def visitElementValue1(self, ctx:Java9_v2Parser.ElementValue1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#elementValue2.
    def visitElementValue2(self, ctx:Java9_v2Parser.ElementValue2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#elementValu3.
    def visitElementValu3(self, ctx:Java9_v2Parser.ElementValu3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#elementValueArrayInitializer.
    def visitElementValueArrayInitializer(self, ctx:Java9_v2Parser.ElementValueArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#elementValueList.
    def visitElementValueList(self, ctx:Java9_v2Parser.ElementValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#markerAnnotation.
    def visitMarkerAnnotation(self, ctx:Java9_v2Parser.MarkerAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#singleElementAnnotation.
    def visitSingleElementAnnotation(self, ctx:Java9_v2Parser.SingleElementAnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayInitializer.
    def visitArrayInitializer(self, ctx:Java9_v2Parser.ArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableInitializerList.
    def visitVariableInitializerList(self, ctx:Java9_v2Parser.VariableInitializerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#block.
    def visitBlock(self, ctx:Java9_v2Parser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#blockStatements.
    def visitBlockStatements(self, ctx:Java9_v2Parser.BlockStatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#blockStatement1.
    def visitBlockStatement1(self, ctx:Java9_v2Parser.BlockStatement1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#blockStatement2.
    def visitBlockStatement2(self, ctx:Java9_v2Parser.BlockStatement2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#blockStatement3.
    def visitBlockStatement3(self, ctx:Java9_v2Parser.BlockStatement3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#localVariableDeclarationStatement.
    def visitLocalVariableDeclarationStatement(self, ctx:Java9_v2Parser.LocalVariableDeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx:Java9_v2Parser.LocalVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statement1.
    def visitStatement1(self, ctx:Java9_v2Parser.Statement1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statement2.
    def visitStatement2(self, ctx:Java9_v2Parser.Statement2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statement3.
    def visitStatement3(self, ctx:Java9_v2Parser.Statement3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statement4.
    def visitStatement4(self, ctx:Java9_v2Parser.Statement4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statement5.
    def visitStatement5(self, ctx:Java9_v2Parser.Statement5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statement6.
    def visitStatement6(self, ctx:Java9_v2Parser.Statement6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementNoShortIf1.
    def visitStatementNoShortIf1(self, ctx:Java9_v2Parser.StatementNoShortIf1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementNoShortIf2.
    def visitStatementNoShortIf2(self, ctx:Java9_v2Parser.StatementNoShortIf2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementNoShortIf3.
    def visitStatementNoShortIf3(self, ctx:Java9_v2Parser.StatementNoShortIf3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementNoShortIf4.
    def visitStatementNoShortIf4(self, ctx:Java9_v2Parser.StatementNoShortIf4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementNoShortIf5.
    def visitStatementNoShortIf5(self, ctx:Java9_v2Parser.StatementNoShortIf5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement1.
    def visitStatementWithoutTrailingSubstatement1(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement2.
    def visitStatementWithoutTrailingSubstatement2(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement3.
    def visitStatementWithoutTrailingSubstatement3(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement4.
    def visitStatementWithoutTrailingSubstatement4(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement5.
    def visitStatementWithoutTrailingSubstatement5(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement6.
    def visitStatementWithoutTrailingSubstatement6(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement7.
    def visitStatementWithoutTrailingSubstatement7(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement8.
    def visitStatementWithoutTrailingSubstatement8(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement8Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement9.
    def visitStatementWithoutTrailingSubstatement9(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement9Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement10.
    def visitStatementWithoutTrailingSubstatement10(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement10Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement11.
    def visitStatementWithoutTrailingSubstatement11(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement11Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementWithoutTrailingSubstatement12.
    def visitStatementWithoutTrailingSubstatement12(self, ctx:Java9_v2Parser.StatementWithoutTrailingSubstatement12Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#emptyStatement.
    def visitEmptyStatement(self, ctx:Java9_v2Parser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#labeledStatement.
    def visitLabeledStatement(self, ctx:Java9_v2Parser.LabeledStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#labeledStatementNoShortIf.
    def visitLabeledStatementNoShortIf(self, ctx:Java9_v2Parser.LabeledStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#expressionStatement.
    def visitExpressionStatement(self, ctx:Java9_v2Parser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementExpression1.
    def visitStatementExpression1(self, ctx:Java9_v2Parser.StatementExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementExpression2.
    def visitStatementExpression2(self, ctx:Java9_v2Parser.StatementExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementExpression3.
    def visitStatementExpression3(self, ctx:Java9_v2Parser.StatementExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementExpression4.
    def visitStatementExpression4(self, ctx:Java9_v2Parser.StatementExpression4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementExpression5.
    def visitStatementExpression5(self, ctx:Java9_v2Parser.StatementExpression5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementExpression6.
    def visitStatementExpression6(self, ctx:Java9_v2Parser.StatementExpression6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementExpression7.
    def visitStatementExpression7(self, ctx:Java9_v2Parser.StatementExpression7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#ifThenStatement.
    def visitIfThenStatement(self, ctx:Java9_v2Parser.IfThenStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#ifThenElseStatement.
    def visitIfThenElseStatement(self, ctx:Java9_v2Parser.IfThenElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#ifThenElseStatementNoShortIf.
    def visitIfThenElseStatementNoShortIf(self, ctx:Java9_v2Parser.IfThenElseStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#assertStatement1.
    def visitAssertStatement1(self, ctx:Java9_v2Parser.AssertStatement1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#assertStatement2.
    def visitAssertStatement2(self, ctx:Java9_v2Parser.AssertStatement2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#switchStatement.
    def visitSwitchStatement(self, ctx:Java9_v2Parser.SwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#switchBlock.
    def visitSwitchBlock(self, ctx:Java9_v2Parser.SwitchBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#switchBlockStatementGroup.
    def visitSwitchBlockStatementGroup(self, ctx:Java9_v2Parser.SwitchBlockStatementGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#switchLabels.
    def visitSwitchLabels(self, ctx:Java9_v2Parser.SwitchLabelsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#switchLabel1.
    def visitSwitchLabel1(self, ctx:Java9_v2Parser.SwitchLabel1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#switchLabel2.
    def visitSwitchLabel2(self, ctx:Java9_v2Parser.SwitchLabel2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#switchLabel3.
    def visitSwitchLabel3(self, ctx:Java9_v2Parser.SwitchLabel3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enumConstantName.
    def visitEnumConstantName(self, ctx:Java9_v2Parser.EnumConstantNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#whileStatement.
    def visitWhileStatement(self, ctx:Java9_v2Parser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#whileStatementNoShortIf.
    def visitWhileStatementNoShortIf(self, ctx:Java9_v2Parser.WhileStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#doStatement.
    def visitDoStatement(self, ctx:Java9_v2Parser.DoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#forStatement1.
    def visitForStatement1(self, ctx:Java9_v2Parser.ForStatement1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#forStatement2.
    def visitForStatement2(self, ctx:Java9_v2Parser.ForStatement2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#forStatementNoShortIf3.
    def visitForStatementNoShortIf3(self, ctx:Java9_v2Parser.ForStatementNoShortIf3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#forStatementNoShortIf4.
    def visitForStatementNoShortIf4(self, ctx:Java9_v2Parser.ForStatementNoShortIf4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#basicForStatement.
    def visitBasicForStatement(self, ctx:Java9_v2Parser.BasicForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#basicForStatementNoShortIf.
    def visitBasicForStatementNoShortIf(self, ctx:Java9_v2Parser.BasicForStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#forInit1.
    def visitForInit1(self, ctx:Java9_v2Parser.ForInit1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#forInit2.
    def visitForInit2(self, ctx:Java9_v2Parser.ForInit2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#forUpdate.
    def visitForUpdate(self, ctx:Java9_v2Parser.ForUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#statementExpressionList.
    def visitStatementExpressionList(self, ctx:Java9_v2Parser.StatementExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enhancedForStatement.
    def visitEnhancedForStatement(self, ctx:Java9_v2Parser.EnhancedForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#enhancedForStatementNoShortIf.
    def visitEnhancedForStatementNoShortIf(self, ctx:Java9_v2Parser.EnhancedForStatementNoShortIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#breakStatement.
    def visitBreakStatement(self, ctx:Java9_v2Parser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#continueStatement.
    def visitContinueStatement(self, ctx:Java9_v2Parser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#returnStatement.
    def visitReturnStatement(self, ctx:Java9_v2Parser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#throwStatement.
    def visitThrowStatement(self, ctx:Java9_v2Parser.ThrowStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#synchronizedStatement.
    def visitSynchronizedStatement(self, ctx:Java9_v2Parser.SynchronizedStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#tryStatement1.
    def visitTryStatement1(self, ctx:Java9_v2Parser.TryStatement1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#tryStatement2.
    def visitTryStatement2(self, ctx:Java9_v2Parser.TryStatement2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#tryStatement3.
    def visitTryStatement3(self, ctx:Java9_v2Parser.TryStatement3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#catches.
    def visitCatches(self, ctx:Java9_v2Parser.CatchesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#catchClause.
    def visitCatchClause(self, ctx:Java9_v2Parser.CatchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#catchFormalParameter.
    def visitCatchFormalParameter(self, ctx:Java9_v2Parser.CatchFormalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#catchType.
    def visitCatchType(self, ctx:Java9_v2Parser.CatchTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#finally_.
    def visitFinally_(self, ctx:Java9_v2Parser.Finally_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#tryWithResourcesStatement.
    def visitTryWithResourcesStatement(self, ctx:Java9_v2Parser.TryWithResourcesStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#resourceSpecification.
    def visitResourceSpecification(self, ctx:Java9_v2Parser.ResourceSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#resourceList.
    def visitResourceList(self, ctx:Java9_v2Parser.ResourceListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#resource1.
    def visitResource1(self, ctx:Java9_v2Parser.Resource1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#resource2.
    def visitResource2(self, ctx:Java9_v2Parser.Resource2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableAccess1.
    def visitVariableAccess1(self, ctx:Java9_v2Parser.VariableAccess1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#variableAccess2.
    def visitVariableAccess2(self, ctx:Java9_v2Parser.VariableAccess2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primary.
    def visitPrimary(self, ctx:Java9_v2Parser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray1.
    def visitPrimaryNoNewArray1(self, ctx:Java9_v2Parser.PrimaryNoNewArray1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray2.
    def visitPrimaryNoNewArray2(self, ctx:Java9_v2Parser.PrimaryNoNewArray2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray3.
    def visitPrimaryNoNewArray3(self, ctx:Java9_v2Parser.PrimaryNoNewArray3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray4.
    def visitPrimaryNoNewArray4(self, ctx:Java9_v2Parser.PrimaryNoNewArray4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray5.
    def visitPrimaryNoNewArray5(self, ctx:Java9_v2Parser.PrimaryNoNewArray5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray6.
    def visitPrimaryNoNewArray6(self, ctx:Java9_v2Parser.PrimaryNoNewArray6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray7.
    def visitPrimaryNoNewArray7(self, ctx:Java9_v2Parser.PrimaryNoNewArray7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray8.
    def visitPrimaryNoNewArray8(self, ctx:Java9_v2Parser.PrimaryNoNewArray8Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray9.
    def visitPrimaryNoNewArray9(self, ctx:Java9_v2Parser.PrimaryNoNewArray9Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray10.
    def visitPrimaryNoNewArray10(self, ctx:Java9_v2Parser.PrimaryNoNewArray10Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_arrayAccess.
    def visitPrimaryNoNewArray_lf_arrayAccess(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_arrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess1.
    def visitPrimaryNoNewArray_lfno_arrayAccess1(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess2.
    def visitPrimaryNoNewArray_lfno_arrayAccess2(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess3.
    def visitPrimaryNoNewArray_lfno_arrayAccess3(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess4.
    def visitPrimaryNoNewArray_lfno_arrayAccess4(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess5.
    def visitPrimaryNoNewArray_lfno_arrayAccess5(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess6.
    def visitPrimaryNoNewArray_lfno_arrayAccess6(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess7.
    def visitPrimaryNoNewArray_lfno_arrayAccess7(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess8.
    def visitPrimaryNoNewArray_lfno_arrayAccess8(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess8Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess9.
    def visitPrimaryNoNewArray_lfno_arrayAccess9(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess9Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_arrayAccess10.
    def visitPrimaryNoNewArray_lfno_arrayAccess10(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_arrayAccess10Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary1.
    def visitPrimaryNoNewArray_lf_primary1(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary2.
    def visitPrimaryNoNewArray_lf_primary2(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary3.
    def visitPrimaryNoNewArray_lf_primary3(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary4.
    def visitPrimaryNoNewArray_lf_primary4(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary5.
    def visitPrimaryNoNewArray_lf_primary5(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary.
    def visitPrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1.
    def visitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2.
    def visitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3.
    def visitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4.
    def visitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary1.
    def visitPrimaryNoNewArray_lfno_primary1(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary2.
    def visitPrimaryNoNewArray_lfno_primary2(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary3.
    def visitPrimaryNoNewArray_lfno_primary3(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary4.
    def visitPrimaryNoNewArray_lfno_primary4(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary5.
    def visitPrimaryNoNewArray_lfno_primary5(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary6.
    def visitPrimaryNoNewArray_lfno_primary6(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary7.
    def visitPrimaryNoNewArray_lfno_primary7(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary8.
    def visitPrimaryNoNewArray_lfno_primary8(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary8Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary9.
    def visitPrimaryNoNewArray_lfno_primary9(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary9Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary10.
    def visitPrimaryNoNewArray_lfno_primary10(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary10Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary11.
    def visitPrimaryNoNewArray_lfno_primary11(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary11Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary12.
    def visitPrimaryNoNewArray_lfno_primary12(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary12Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary.
    def visitPrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11.
    def visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11(self, ctx:Java9_v2Parser.PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classLiteral1.
    def visitClassLiteral1(self, ctx:Java9_v2Parser.ClassLiteral1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classLiteral2.
    def visitClassLiteral2(self, ctx:Java9_v2Parser.ClassLiteral2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classInstanceCreationExpression1.
    def visitClassInstanceCreationExpression1(self, ctx:Java9_v2Parser.ClassInstanceCreationExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classInstanceCreationExpression2.
    def visitClassInstanceCreationExpression2(self, ctx:Java9_v2Parser.ClassInstanceCreationExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classInstanceCreationExpression3.
    def visitClassInstanceCreationExpression3(self, ctx:Java9_v2Parser.ClassInstanceCreationExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classInstanceCreationExpression_lf_primary.
    def visitClassInstanceCreationExpression_lf_primary(self, ctx:Java9_v2Parser.ClassInstanceCreationExpression_lf_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classInstanceCreationExpression_lfno_primary1.
    def visitClassInstanceCreationExpression_lfno_primary1(self, ctx:Java9_v2Parser.ClassInstanceCreationExpression_lfno_primary1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#classInstanceCreationExpression_lfno_primary2.
    def visitClassInstanceCreationExpression_lfno_primary2(self, ctx:Java9_v2Parser.ClassInstanceCreationExpression_lfno_primary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeArgumentsOrDiamond1.
    def visitTypeArgumentsOrDiamond1(self, ctx:Java9_v2Parser.TypeArgumentsOrDiamond1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#typeArgumentsOrDiamond2.
    def visitTypeArgumentsOrDiamond2(self, ctx:Java9_v2Parser.TypeArgumentsOrDiamond2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#fieldAccess1.
    def visitFieldAccess1(self, ctx:Java9_v2Parser.FieldAccess1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#fieldAccess2.
    def visitFieldAccess2(self, ctx:Java9_v2Parser.FieldAccess2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#fieldAccess3.
    def visitFieldAccess3(self, ctx:Java9_v2Parser.FieldAccess3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#fieldAccess_lf_primary.
    def visitFieldAccess_lf_primary(self, ctx:Java9_v2Parser.FieldAccess_lf_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#fieldAccess_lfno_primary1.
    def visitFieldAccess_lfno_primary1(self, ctx:Java9_v2Parser.FieldAccess_lfno_primary1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#fieldAccess_lfno_primary2.
    def visitFieldAccess_lfno_primary2(self, ctx:Java9_v2Parser.FieldAccess_lfno_primary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayAccess.
    def visitArrayAccess(self, ctx:Java9_v2Parser.ArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayAccess_lf_primary.
    def visitArrayAccess_lf_primary(self, ctx:Java9_v2Parser.ArrayAccess_lf_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayAccess_lfno_primary.
    def visitArrayAccess_lfno_primary(self, ctx:Java9_v2Parser.ArrayAccess_lfno_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation1.
    def visitMethodInvocation1(self, ctx:Java9_v2Parser.MethodInvocation1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation2.
    def visitMethodInvocation2(self, ctx:Java9_v2Parser.MethodInvocation2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation3.
    def visitMethodInvocation3(self, ctx:Java9_v2Parser.MethodInvocation3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation4.
    def visitMethodInvocation4(self, ctx:Java9_v2Parser.MethodInvocation4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation5.
    def visitMethodInvocation5(self, ctx:Java9_v2Parser.MethodInvocation5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation6.
    def visitMethodInvocation6(self, ctx:Java9_v2Parser.MethodInvocation6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation_lf_primary.
    def visitMethodInvocation_lf_primary(self, ctx:Java9_v2Parser.MethodInvocation_lf_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation_lfno_primary1.
    def visitMethodInvocation_lfno_primary1(self, ctx:Java9_v2Parser.MethodInvocation_lfno_primary1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation_lfno_primary2.
    def visitMethodInvocation_lfno_primary2(self, ctx:Java9_v2Parser.MethodInvocation_lfno_primary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation_lfno_primary3.
    def visitMethodInvocation_lfno_primary3(self, ctx:Java9_v2Parser.MethodInvocation_lfno_primary3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation_lfno_primary4.
    def visitMethodInvocation_lfno_primary4(self, ctx:Java9_v2Parser.MethodInvocation_lfno_primary4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodInvocation_lfno_primary5.
    def visitMethodInvocation_lfno_primary5(self, ctx:Java9_v2Parser.MethodInvocation_lfno_primary5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#argumentList.
    def visitArgumentList(self, ctx:Java9_v2Parser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference1.
    def visitMethodReference1(self, ctx:Java9_v2Parser.MethodReference1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference2.
    def visitMethodReference2(self, ctx:Java9_v2Parser.MethodReference2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference3.
    def visitMethodReference3(self, ctx:Java9_v2Parser.MethodReference3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference4.
    def visitMethodReference4(self, ctx:Java9_v2Parser.MethodReference4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference5.
    def visitMethodReference5(self, ctx:Java9_v2Parser.MethodReference5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference6.
    def visitMethodReference6(self, ctx:Java9_v2Parser.MethodReference6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference7.
    def visitMethodReference7(self, ctx:Java9_v2Parser.MethodReference7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference_lf_primary.
    def visitMethodReference_lf_primary(self, ctx:Java9_v2Parser.MethodReference_lf_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference_lfno_primary1.
    def visitMethodReference_lfno_primary1(self, ctx:Java9_v2Parser.MethodReference_lfno_primary1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference_lfno_primary2.
    def visitMethodReference_lfno_primary2(self, ctx:Java9_v2Parser.MethodReference_lfno_primary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference_lfno_primary3.
    def visitMethodReference_lfno_primary3(self, ctx:Java9_v2Parser.MethodReference_lfno_primary3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference_lfno_primary4.
    def visitMethodReference_lfno_primary4(self, ctx:Java9_v2Parser.MethodReference_lfno_primary4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference_lfno_primary5.
    def visitMethodReference_lfno_primary5(self, ctx:Java9_v2Parser.MethodReference_lfno_primary5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#methodReference_lfno_primary6.
    def visitMethodReference_lfno_primary6(self, ctx:Java9_v2Parser.MethodReference_lfno_primary6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayCreationExpression1.
    def visitArrayCreationExpression1(self, ctx:Java9_v2Parser.ArrayCreationExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayCreationExpression2.
    def visitArrayCreationExpression2(self, ctx:Java9_v2Parser.ArrayCreationExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayCreationExpression3.
    def visitArrayCreationExpression3(self, ctx:Java9_v2Parser.ArrayCreationExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#arrayCreationExpression4.
    def visitArrayCreationExpression4(self, ctx:Java9_v2Parser.ArrayCreationExpression4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#dimExprs.
    def visitDimExprs(self, ctx:Java9_v2Parser.DimExprsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#dimExpr.
    def visitDimExpr(self, ctx:Java9_v2Parser.DimExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#constantExpression.
    def visitConstantExpression(self, ctx:Java9_v2Parser.ConstantExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#expression1.
    def visitExpression1(self, ctx:Java9_v2Parser.Expression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#expression2.
    def visitExpression2(self, ctx:Java9_v2Parser.Expression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#lambdaExpression.
    def visitLambdaExpression(self, ctx:Java9_v2Parser.LambdaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#lambdaParameters1.
    def visitLambdaParameters1(self, ctx:Java9_v2Parser.LambdaParameters1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#lambdaParameters2.
    def visitLambdaParameters2(self, ctx:Java9_v2Parser.LambdaParameters2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#lambdaParameters3.
    def visitLambdaParameters3(self, ctx:Java9_v2Parser.LambdaParameters3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#inferredFormalParameterList.
    def visitInferredFormalParameterList(self, ctx:Java9_v2Parser.InferredFormalParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#lambdaBody1.
    def visitLambdaBody1(self, ctx:Java9_v2Parser.LambdaBody1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#lambdaBody2.
    def visitLambdaBody2(self, ctx:Java9_v2Parser.LambdaBody2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#assignmentExpression1.
    def visitAssignmentExpression1(self, ctx:Java9_v2Parser.AssignmentExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#assignmentExpression2.
    def visitAssignmentExpression2(self, ctx:Java9_v2Parser.AssignmentExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#assignment.
    def visitAssignment(self, ctx:Java9_v2Parser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#leftHandSide3.
    def visitLeftHandSide3(self, ctx:Java9_v2Parser.LeftHandSide3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#leftHandSide4.
    def visitLeftHandSide4(self, ctx:Java9_v2Parser.LeftHandSide4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#leftHandSide5.
    def visitLeftHandSide5(self, ctx:Java9_v2Parser.LeftHandSide5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:Java9_v2Parser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#conditionalExpression1.
    def visitConditionalExpression1(self, ctx:Java9_v2Parser.ConditionalExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#conditionalExpression2.
    def visitConditionalExpression2(self, ctx:Java9_v2Parser.ConditionalExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#conditionalOrExpression1.
    def visitConditionalOrExpression1(self, ctx:Java9_v2Parser.ConditionalOrExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#conditionalOrExpression2.
    def visitConditionalOrExpression2(self, ctx:Java9_v2Parser.ConditionalOrExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#conditionalAndExpression2.
    def visitConditionalAndExpression2(self, ctx:Java9_v2Parser.ConditionalAndExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#conditionalAndExpression1.
    def visitConditionalAndExpression1(self, ctx:Java9_v2Parser.ConditionalAndExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#inclusiveOrExpression2.
    def visitInclusiveOrExpression2(self, ctx:Java9_v2Parser.InclusiveOrExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#inclusiveOrExpression1.
    def visitInclusiveOrExpression1(self, ctx:Java9_v2Parser.InclusiveOrExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#exclusiveOrExpression1.
    def visitExclusiveOrExpression1(self, ctx:Java9_v2Parser.ExclusiveOrExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#exclusiveOrExpression2.
    def visitExclusiveOrExpression2(self, ctx:Java9_v2Parser.ExclusiveOrExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#andExpression2.
    def visitAndExpression2(self, ctx:Java9_v2Parser.AndExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#andExpression1.
    def visitAndExpression1(self, ctx:Java9_v2Parser.AndExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#equalityExpression3.
    def visitEqualityExpression3(self, ctx:Java9_v2Parser.EqualityExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#equalityExpression2.
    def visitEqualityExpression2(self, ctx:Java9_v2Parser.EqualityExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#equalityExpression1.
    def visitEqualityExpression1(self, ctx:Java9_v2Parser.EqualityExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#relationalExpression1.
    def visitRelationalExpression1(self, ctx:Java9_v2Parser.RelationalExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#relationalExpression2.
    def visitRelationalExpression2(self, ctx:Java9_v2Parser.RelationalExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#relationalExpression5.
    def visitRelationalExpression5(self, ctx:Java9_v2Parser.RelationalExpression5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#relationalExpression6.
    def visitRelationalExpression6(self, ctx:Java9_v2Parser.RelationalExpression6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#relationalExpression3.
    def visitRelationalExpression3(self, ctx:Java9_v2Parser.RelationalExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#relationalExpression4.
    def visitRelationalExpression4(self, ctx:Java9_v2Parser.RelationalExpression4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#shiftExpression1.
    def visitShiftExpression1(self, ctx:Java9_v2Parser.ShiftExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#shiftExpression3.
    def visitShiftExpression3(self, ctx:Java9_v2Parser.ShiftExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#shiftExpression2.
    def visitShiftExpression2(self, ctx:Java9_v2Parser.ShiftExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#shiftExpression4.
    def visitShiftExpression4(self, ctx:Java9_v2Parser.ShiftExpression4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#additiveExpression1.
    def visitAdditiveExpression1(self, ctx:Java9_v2Parser.AdditiveExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#additiveExpression3.
    def visitAdditiveExpression3(self, ctx:Java9_v2Parser.AdditiveExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#additiveExpressio2.
    def visitAdditiveExpressio2(self, ctx:Java9_v2Parser.AdditiveExpressio2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#multiplicativeExpression1.
    def visitMultiplicativeExpression1(self, ctx:Java9_v2Parser.MultiplicativeExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#multiplicativeExpression4.
    def visitMultiplicativeExpression4(self, ctx:Java9_v2Parser.MultiplicativeExpression4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#multiplicativeExpression3.
    def visitMultiplicativeExpression3(self, ctx:Java9_v2Parser.MultiplicativeExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#multiplicativeExpression2.
    def visitMultiplicativeExpression2(self, ctx:Java9_v2Parser.MultiplicativeExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpression1.
    def visitUnaryExpression1(self, ctx:Java9_v2Parser.UnaryExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpression2.
    def visitUnaryExpression2(self, ctx:Java9_v2Parser.UnaryExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpression3.
    def visitUnaryExpression3(self, ctx:Java9_v2Parser.UnaryExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpression4.
    def visitUnaryExpression4(self, ctx:Java9_v2Parser.UnaryExpression4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpression5.
    def visitUnaryExpression5(self, ctx:Java9_v2Parser.UnaryExpression5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#preIncrementExpression.
    def visitPreIncrementExpression(self, ctx:Java9_v2Parser.PreIncrementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#preDecrementExpression.
    def visitPreDecrementExpression(self, ctx:Java9_v2Parser.PreDecrementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpressionNotPlusMinus1.
    def visitUnaryExpressionNotPlusMinus1(self, ctx:Java9_v2Parser.UnaryExpressionNotPlusMinus1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpressionNotPlusMinus2.
    def visitUnaryExpressionNotPlusMinus2(self, ctx:Java9_v2Parser.UnaryExpressionNotPlusMinus2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpressionNotPlusMinus3.
    def visitUnaryExpressionNotPlusMinus3(self, ctx:Java9_v2Parser.UnaryExpressionNotPlusMinus3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#unaryExpressionNotPlusMinus4.
    def visitUnaryExpressionNotPlusMinus4(self, ctx:Java9_v2Parser.UnaryExpressionNotPlusMinus4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#postfixExpression.
    def visitPostfixExpression(self, ctx:Java9_v2Parser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#postIncrementExpression.
    def visitPostIncrementExpression(self, ctx:Java9_v2Parser.PostIncrementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#postIncrementExpression_lf_postfixExpression.
    def visitPostIncrementExpression_lf_postfixExpression(self, ctx:Java9_v2Parser.PostIncrementExpression_lf_postfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#postDecrementExpression.
    def visitPostDecrementExpression(self, ctx:Java9_v2Parser.PostDecrementExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#postDecrementExpression_lf_postfixExpression.
    def visitPostDecrementExpression_lf_postfixExpression(self, ctx:Java9_v2Parser.PostDecrementExpression_lf_postfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#castExpression1.
    def visitCastExpression1(self, ctx:Java9_v2Parser.CastExpression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#castExpression2.
    def visitCastExpression2(self, ctx:Java9_v2Parser.CastExpression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#castExpression3.
    def visitCastExpression3(self, ctx:Java9_v2Parser.CastExpression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java9_v2Parser#identifier.
    def visitIdentifier(self, ctx:Java9_v2Parser.IdentifierContext):
        return self.visitChildren(ctx)



del Java9_v2Parser