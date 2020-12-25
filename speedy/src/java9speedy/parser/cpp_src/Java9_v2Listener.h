
// Generated from D:/AnacondaProjects/CodART/grammars\Java9_v2.g4 by ANTLR 4.9

#pragma once


#include "antlr4-runtime.h"
#include "Java9_v2Parser.h"


/**
 * This interface defines an abstract listener for a parse tree produced by Java9_v2Parser.
 */
class  Java9_v2Listener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterLiteral(Java9_v2Parser::LiteralContext *ctx) = 0;
  virtual void exitLiteral(Java9_v2Parser::LiteralContext *ctx) = 0;

  virtual void enterPrimitiveType1(Java9_v2Parser::PrimitiveType1Context *ctx) = 0;
  virtual void exitPrimitiveType1(Java9_v2Parser::PrimitiveType1Context *ctx) = 0;

  virtual void enterPrimitiveType2(Java9_v2Parser::PrimitiveType2Context *ctx) = 0;
  virtual void exitPrimitiveType2(Java9_v2Parser::PrimitiveType2Context *ctx) = 0;

  virtual void enterNumericType1(Java9_v2Parser::NumericType1Context *ctx) = 0;
  virtual void exitNumericType1(Java9_v2Parser::NumericType1Context *ctx) = 0;

  virtual void enterNumericType2(Java9_v2Parser::NumericType2Context *ctx) = 0;
  virtual void exitNumericType2(Java9_v2Parser::NumericType2Context *ctx) = 0;

  virtual void enterIntegralType(Java9_v2Parser::IntegralTypeContext *ctx) = 0;
  virtual void exitIntegralType(Java9_v2Parser::IntegralTypeContext *ctx) = 0;

  virtual void enterFloatingPointType(Java9_v2Parser::FloatingPointTypeContext *ctx) = 0;
  virtual void exitFloatingPointType(Java9_v2Parser::FloatingPointTypeContext *ctx) = 0;

  virtual void enterReferenceType1(Java9_v2Parser::ReferenceType1Context *ctx) = 0;
  virtual void exitReferenceType1(Java9_v2Parser::ReferenceType1Context *ctx) = 0;

  virtual void enterReferenceType2(Java9_v2Parser::ReferenceType2Context *ctx) = 0;
  virtual void exitReferenceType2(Java9_v2Parser::ReferenceType2Context *ctx) = 0;

  virtual void enterReferenceType3(Java9_v2Parser::ReferenceType3Context *ctx) = 0;
  virtual void exitReferenceType3(Java9_v2Parser::ReferenceType3Context *ctx) = 0;

  virtual void enterClassOrInterfaceType(Java9_v2Parser::ClassOrInterfaceTypeContext *ctx) = 0;
  virtual void exitClassOrInterfaceType(Java9_v2Parser::ClassOrInterfaceTypeContext *ctx) = 0;

  virtual void enterClassType1(Java9_v2Parser::ClassType1Context *ctx) = 0;
  virtual void exitClassType1(Java9_v2Parser::ClassType1Context *ctx) = 0;

  virtual void enterClassType2(Java9_v2Parser::ClassType2Context *ctx) = 0;
  virtual void exitClassType2(Java9_v2Parser::ClassType2Context *ctx) = 0;

  virtual void enterClassType_lf_classOrInterfaceType(Java9_v2Parser::ClassType_lf_classOrInterfaceTypeContext *ctx) = 0;
  virtual void exitClassType_lf_classOrInterfaceType(Java9_v2Parser::ClassType_lf_classOrInterfaceTypeContext *ctx) = 0;

  virtual void enterClassType_lfno_classOrInterfaceType(Java9_v2Parser::ClassType_lfno_classOrInterfaceTypeContext *ctx) = 0;
  virtual void exitClassType_lfno_classOrInterfaceType(Java9_v2Parser::ClassType_lfno_classOrInterfaceTypeContext *ctx) = 0;

  virtual void enterInterfaceType(Java9_v2Parser::InterfaceTypeContext *ctx) = 0;
  virtual void exitInterfaceType(Java9_v2Parser::InterfaceTypeContext *ctx) = 0;

  virtual void enterInterfaceType_lf_classOrInterfaceType(Java9_v2Parser::InterfaceType_lf_classOrInterfaceTypeContext *ctx) = 0;
  virtual void exitInterfaceType_lf_classOrInterfaceType(Java9_v2Parser::InterfaceType_lf_classOrInterfaceTypeContext *ctx) = 0;

  virtual void enterInterfaceType_lfno_classOrInterfaceType(Java9_v2Parser::InterfaceType_lfno_classOrInterfaceTypeContext *ctx) = 0;
  virtual void exitInterfaceType_lfno_classOrInterfaceType(Java9_v2Parser::InterfaceType_lfno_classOrInterfaceTypeContext *ctx) = 0;

  virtual void enterTypeVariable(Java9_v2Parser::TypeVariableContext *ctx) = 0;
  virtual void exitTypeVariable(Java9_v2Parser::TypeVariableContext *ctx) = 0;

  virtual void enterArrayType1(Java9_v2Parser::ArrayType1Context *ctx) = 0;
  virtual void exitArrayType1(Java9_v2Parser::ArrayType1Context *ctx) = 0;

  virtual void enterArrayType2(Java9_v2Parser::ArrayType2Context *ctx) = 0;
  virtual void exitArrayType2(Java9_v2Parser::ArrayType2Context *ctx) = 0;

  virtual void enterArrayTyp3(Java9_v2Parser::ArrayTyp3Context *ctx) = 0;
  virtual void exitArrayTyp3(Java9_v2Parser::ArrayTyp3Context *ctx) = 0;

  virtual void enterDims(Java9_v2Parser::DimsContext *ctx) = 0;
  virtual void exitDims(Java9_v2Parser::DimsContext *ctx) = 0;

  virtual void enterTypeParameter(Java9_v2Parser::TypeParameterContext *ctx) = 0;
  virtual void exitTypeParameter(Java9_v2Parser::TypeParameterContext *ctx) = 0;

  virtual void enterTypeParameterModifier(Java9_v2Parser::TypeParameterModifierContext *ctx) = 0;
  virtual void exitTypeParameterModifier(Java9_v2Parser::TypeParameterModifierContext *ctx) = 0;

  virtual void enterTypeBound1(Java9_v2Parser::TypeBound1Context *ctx) = 0;
  virtual void exitTypeBound1(Java9_v2Parser::TypeBound1Context *ctx) = 0;

  virtual void enterTypeBound2(Java9_v2Parser::TypeBound2Context *ctx) = 0;
  virtual void exitTypeBound2(Java9_v2Parser::TypeBound2Context *ctx) = 0;

  virtual void enterAdditionalBound(Java9_v2Parser::AdditionalBoundContext *ctx) = 0;
  virtual void exitAdditionalBound(Java9_v2Parser::AdditionalBoundContext *ctx) = 0;

  virtual void enterTypeArguments(Java9_v2Parser::TypeArgumentsContext *ctx) = 0;
  virtual void exitTypeArguments(Java9_v2Parser::TypeArgumentsContext *ctx) = 0;

  virtual void enterTypeArgumentList(Java9_v2Parser::TypeArgumentListContext *ctx) = 0;
  virtual void exitTypeArgumentList(Java9_v2Parser::TypeArgumentListContext *ctx) = 0;

  virtual void enterTypeArgument1(Java9_v2Parser::TypeArgument1Context *ctx) = 0;
  virtual void exitTypeArgument1(Java9_v2Parser::TypeArgument1Context *ctx) = 0;

  virtual void enterTypeArgument2(Java9_v2Parser::TypeArgument2Context *ctx) = 0;
  virtual void exitTypeArgument2(Java9_v2Parser::TypeArgument2Context *ctx) = 0;

  virtual void enterWildcard(Java9_v2Parser::WildcardContext *ctx) = 0;
  virtual void exitWildcard(Java9_v2Parser::WildcardContext *ctx) = 0;

  virtual void enterWildcardBounds1(Java9_v2Parser::WildcardBounds1Context *ctx) = 0;
  virtual void exitWildcardBounds1(Java9_v2Parser::WildcardBounds1Context *ctx) = 0;

  virtual void enterWildcardBound2(Java9_v2Parser::WildcardBound2Context *ctx) = 0;
  virtual void exitWildcardBound2(Java9_v2Parser::WildcardBound2Context *ctx) = 0;

  virtual void enterModuleName1(Java9_v2Parser::ModuleName1Context *ctx) = 0;
  virtual void exitModuleName1(Java9_v2Parser::ModuleName1Context *ctx) = 0;

  virtual void enterModuleName2(Java9_v2Parser::ModuleName2Context *ctx) = 0;
  virtual void exitModuleName2(Java9_v2Parser::ModuleName2Context *ctx) = 0;

  virtual void enterPackageName2(Java9_v2Parser::PackageName2Context *ctx) = 0;
  virtual void exitPackageName2(Java9_v2Parser::PackageName2Context *ctx) = 0;

  virtual void enterPackageName1(Java9_v2Parser::PackageName1Context *ctx) = 0;
  virtual void exitPackageName1(Java9_v2Parser::PackageName1Context *ctx) = 0;

  virtual void enterTypeName1(Java9_v2Parser::TypeName1Context *ctx) = 0;
  virtual void exitTypeName1(Java9_v2Parser::TypeName1Context *ctx) = 0;

  virtual void enterTypeName2(Java9_v2Parser::TypeName2Context *ctx) = 0;
  virtual void exitTypeName2(Java9_v2Parser::TypeName2Context *ctx) = 0;

  virtual void enterPackageOrTypeName1(Java9_v2Parser::PackageOrTypeName1Context *ctx) = 0;
  virtual void exitPackageOrTypeName1(Java9_v2Parser::PackageOrTypeName1Context *ctx) = 0;

  virtual void enterPackageOrTypeName2(Java9_v2Parser::PackageOrTypeName2Context *ctx) = 0;
  virtual void exitPackageOrTypeName2(Java9_v2Parser::PackageOrTypeName2Context *ctx) = 0;

  virtual void enterExpressionName1(Java9_v2Parser::ExpressionName1Context *ctx) = 0;
  virtual void exitExpressionName1(Java9_v2Parser::ExpressionName1Context *ctx) = 0;

  virtual void enterExpressionName2(Java9_v2Parser::ExpressionName2Context *ctx) = 0;
  virtual void exitExpressionName2(Java9_v2Parser::ExpressionName2Context *ctx) = 0;

  virtual void enterMethodName(Java9_v2Parser::MethodNameContext *ctx) = 0;
  virtual void exitMethodName(Java9_v2Parser::MethodNameContext *ctx) = 0;

  virtual void enterAmbiguousName1(Java9_v2Parser::AmbiguousName1Context *ctx) = 0;
  virtual void exitAmbiguousName1(Java9_v2Parser::AmbiguousName1Context *ctx) = 0;

  virtual void enterAmbiguousName2(Java9_v2Parser::AmbiguousName2Context *ctx) = 0;
  virtual void exitAmbiguousName2(Java9_v2Parser::AmbiguousName2Context *ctx) = 0;

  virtual void enterCompilationUnit1(Java9_v2Parser::CompilationUnit1Context *ctx) = 0;
  virtual void exitCompilationUnit1(Java9_v2Parser::CompilationUnit1Context *ctx) = 0;

  virtual void enterCompilationUnit2(Java9_v2Parser::CompilationUnit2Context *ctx) = 0;
  virtual void exitCompilationUnit2(Java9_v2Parser::CompilationUnit2Context *ctx) = 0;

  virtual void enterOrdinaryCompilation(Java9_v2Parser::OrdinaryCompilationContext *ctx) = 0;
  virtual void exitOrdinaryCompilation(Java9_v2Parser::OrdinaryCompilationContext *ctx) = 0;

  virtual void enterModularCompilation(Java9_v2Parser::ModularCompilationContext *ctx) = 0;
  virtual void exitModularCompilation(Java9_v2Parser::ModularCompilationContext *ctx) = 0;

  virtual void enterPackageDeclaration(Java9_v2Parser::PackageDeclarationContext *ctx) = 0;
  virtual void exitPackageDeclaration(Java9_v2Parser::PackageDeclarationContext *ctx) = 0;

  virtual void enterPackageModifier(Java9_v2Parser::PackageModifierContext *ctx) = 0;
  virtual void exitPackageModifier(Java9_v2Parser::PackageModifierContext *ctx) = 0;

  virtual void enterImportDeclaration1(Java9_v2Parser::ImportDeclaration1Context *ctx) = 0;
  virtual void exitImportDeclaration1(Java9_v2Parser::ImportDeclaration1Context *ctx) = 0;

  virtual void enterImportDeclaration2(Java9_v2Parser::ImportDeclaration2Context *ctx) = 0;
  virtual void exitImportDeclaration2(Java9_v2Parser::ImportDeclaration2Context *ctx) = 0;

  virtual void enterImportDeclaration3(Java9_v2Parser::ImportDeclaration3Context *ctx) = 0;
  virtual void exitImportDeclaration3(Java9_v2Parser::ImportDeclaration3Context *ctx) = 0;

  virtual void enterImportDeclaration4(Java9_v2Parser::ImportDeclaration4Context *ctx) = 0;
  virtual void exitImportDeclaration4(Java9_v2Parser::ImportDeclaration4Context *ctx) = 0;

  virtual void enterSingleTypeImportDeclaration(Java9_v2Parser::SingleTypeImportDeclarationContext *ctx) = 0;
  virtual void exitSingleTypeImportDeclaration(Java9_v2Parser::SingleTypeImportDeclarationContext *ctx) = 0;

  virtual void enterTypeImportOnDemandDeclaration(Java9_v2Parser::TypeImportOnDemandDeclarationContext *ctx) = 0;
  virtual void exitTypeImportOnDemandDeclaration(Java9_v2Parser::TypeImportOnDemandDeclarationContext *ctx) = 0;

  virtual void enterSingleStaticImportDeclaration(Java9_v2Parser::SingleStaticImportDeclarationContext *ctx) = 0;
  virtual void exitSingleStaticImportDeclaration(Java9_v2Parser::SingleStaticImportDeclarationContext *ctx) = 0;

  virtual void enterStaticImportOnDemandDeclaration(Java9_v2Parser::StaticImportOnDemandDeclarationContext *ctx) = 0;
  virtual void exitStaticImportOnDemandDeclaration(Java9_v2Parser::StaticImportOnDemandDeclarationContext *ctx) = 0;

  virtual void enterTypeDeclaration1(Java9_v2Parser::TypeDeclaration1Context *ctx) = 0;
  virtual void exitTypeDeclaration1(Java9_v2Parser::TypeDeclaration1Context *ctx) = 0;

  virtual void enterTypeDeclaration2(Java9_v2Parser::TypeDeclaration2Context *ctx) = 0;
  virtual void exitTypeDeclaration2(Java9_v2Parser::TypeDeclaration2Context *ctx) = 0;

  virtual void enterTypeDeclaration3(Java9_v2Parser::TypeDeclaration3Context *ctx) = 0;
  virtual void exitTypeDeclaration3(Java9_v2Parser::TypeDeclaration3Context *ctx) = 0;

  virtual void enterModuleDeclaration(Java9_v2Parser::ModuleDeclarationContext *ctx) = 0;
  virtual void exitModuleDeclaration(Java9_v2Parser::ModuleDeclarationContext *ctx) = 0;

  virtual void enterModuleDirective1(Java9_v2Parser::ModuleDirective1Context *ctx) = 0;
  virtual void exitModuleDirective1(Java9_v2Parser::ModuleDirective1Context *ctx) = 0;

  virtual void enterModuleDirective2(Java9_v2Parser::ModuleDirective2Context *ctx) = 0;
  virtual void exitModuleDirective2(Java9_v2Parser::ModuleDirective2Context *ctx) = 0;

  virtual void enterModuleDirectiv3(Java9_v2Parser::ModuleDirectiv3Context *ctx) = 0;
  virtual void exitModuleDirectiv3(Java9_v2Parser::ModuleDirectiv3Context *ctx) = 0;

  virtual void enterModuleDirective4(Java9_v2Parser::ModuleDirective4Context *ctx) = 0;
  virtual void exitModuleDirective4(Java9_v2Parser::ModuleDirective4Context *ctx) = 0;

  virtual void enterModuleDirective5(Java9_v2Parser::ModuleDirective5Context *ctx) = 0;
  virtual void exitModuleDirective5(Java9_v2Parser::ModuleDirective5Context *ctx) = 0;

  virtual void enterRequiresModifier(Java9_v2Parser::RequiresModifierContext *ctx) = 0;
  virtual void exitRequiresModifier(Java9_v2Parser::RequiresModifierContext *ctx) = 0;

  virtual void enterClassDeclaration1(Java9_v2Parser::ClassDeclaration1Context *ctx) = 0;
  virtual void exitClassDeclaration1(Java9_v2Parser::ClassDeclaration1Context *ctx) = 0;

  virtual void enterClassDeclaration2(Java9_v2Parser::ClassDeclaration2Context *ctx) = 0;
  virtual void exitClassDeclaration2(Java9_v2Parser::ClassDeclaration2Context *ctx) = 0;

  virtual void enterNormalClassDeclaration(Java9_v2Parser::NormalClassDeclarationContext *ctx) = 0;
  virtual void exitNormalClassDeclaration(Java9_v2Parser::NormalClassDeclarationContext *ctx) = 0;

  virtual void enterClassModifier(Java9_v2Parser::ClassModifierContext *ctx) = 0;
  virtual void exitClassModifier(Java9_v2Parser::ClassModifierContext *ctx) = 0;

  virtual void enterTypeParameters(Java9_v2Parser::TypeParametersContext *ctx) = 0;
  virtual void exitTypeParameters(Java9_v2Parser::TypeParametersContext *ctx) = 0;

  virtual void enterTypeParameterList(Java9_v2Parser::TypeParameterListContext *ctx) = 0;
  virtual void exitTypeParameterList(Java9_v2Parser::TypeParameterListContext *ctx) = 0;

  virtual void enterSuperclass(Java9_v2Parser::SuperclassContext *ctx) = 0;
  virtual void exitSuperclass(Java9_v2Parser::SuperclassContext *ctx) = 0;

  virtual void enterSuperinterfaces(Java9_v2Parser::SuperinterfacesContext *ctx) = 0;
  virtual void exitSuperinterfaces(Java9_v2Parser::SuperinterfacesContext *ctx) = 0;

  virtual void enterInterfaceTypeList(Java9_v2Parser::InterfaceTypeListContext *ctx) = 0;
  virtual void exitInterfaceTypeList(Java9_v2Parser::InterfaceTypeListContext *ctx) = 0;

  virtual void enterClassBody(Java9_v2Parser::ClassBodyContext *ctx) = 0;
  virtual void exitClassBody(Java9_v2Parser::ClassBodyContext *ctx) = 0;

  virtual void enterClassBodyDeclaration1(Java9_v2Parser::ClassBodyDeclaration1Context *ctx) = 0;
  virtual void exitClassBodyDeclaration1(Java9_v2Parser::ClassBodyDeclaration1Context *ctx) = 0;

  virtual void enterClassBodyDeclaration2(Java9_v2Parser::ClassBodyDeclaration2Context *ctx) = 0;
  virtual void exitClassBodyDeclaration2(Java9_v2Parser::ClassBodyDeclaration2Context *ctx) = 0;

  virtual void enterClassBodyDeclaration3(Java9_v2Parser::ClassBodyDeclaration3Context *ctx) = 0;
  virtual void exitClassBodyDeclaration3(Java9_v2Parser::ClassBodyDeclaration3Context *ctx) = 0;

  virtual void enterClassBodyDeclaration4(Java9_v2Parser::ClassBodyDeclaration4Context *ctx) = 0;
  virtual void exitClassBodyDeclaration4(Java9_v2Parser::ClassBodyDeclaration4Context *ctx) = 0;

  virtual void enterClassMemberDeclaration1(Java9_v2Parser::ClassMemberDeclaration1Context *ctx) = 0;
  virtual void exitClassMemberDeclaration1(Java9_v2Parser::ClassMemberDeclaration1Context *ctx) = 0;

  virtual void enterClassMemberDeclaration2(Java9_v2Parser::ClassMemberDeclaration2Context *ctx) = 0;
  virtual void exitClassMemberDeclaration2(Java9_v2Parser::ClassMemberDeclaration2Context *ctx) = 0;

  virtual void enterClassMemberDeclaration3(Java9_v2Parser::ClassMemberDeclaration3Context *ctx) = 0;
  virtual void exitClassMemberDeclaration3(Java9_v2Parser::ClassMemberDeclaration3Context *ctx) = 0;

  virtual void enterClassMemberDeclaration4(Java9_v2Parser::ClassMemberDeclaration4Context *ctx) = 0;
  virtual void exitClassMemberDeclaration4(Java9_v2Parser::ClassMemberDeclaration4Context *ctx) = 0;

  virtual void enterClassMemberDeclaration5(Java9_v2Parser::ClassMemberDeclaration5Context *ctx) = 0;
  virtual void exitClassMemberDeclaration5(Java9_v2Parser::ClassMemberDeclaration5Context *ctx) = 0;

  virtual void enterFieldDeclaration(Java9_v2Parser::FieldDeclarationContext *ctx) = 0;
  virtual void exitFieldDeclaration(Java9_v2Parser::FieldDeclarationContext *ctx) = 0;

  virtual void enterFieldModifier(Java9_v2Parser::FieldModifierContext *ctx) = 0;
  virtual void exitFieldModifier(Java9_v2Parser::FieldModifierContext *ctx) = 0;

  virtual void enterVariableDeclaratorList(Java9_v2Parser::VariableDeclaratorListContext *ctx) = 0;
  virtual void exitVariableDeclaratorList(Java9_v2Parser::VariableDeclaratorListContext *ctx) = 0;

  virtual void enterVariableDeclarator(Java9_v2Parser::VariableDeclaratorContext *ctx) = 0;
  virtual void exitVariableDeclarator(Java9_v2Parser::VariableDeclaratorContext *ctx) = 0;

  virtual void enterVariableDeclaratorId(Java9_v2Parser::VariableDeclaratorIdContext *ctx) = 0;
  virtual void exitVariableDeclaratorId(Java9_v2Parser::VariableDeclaratorIdContext *ctx) = 0;

  virtual void enterVariableInitializer1(Java9_v2Parser::VariableInitializer1Context *ctx) = 0;
  virtual void exitVariableInitializer1(Java9_v2Parser::VariableInitializer1Context *ctx) = 0;

  virtual void enterVariableInitializer2(Java9_v2Parser::VariableInitializer2Context *ctx) = 0;
  virtual void exitVariableInitializer2(Java9_v2Parser::VariableInitializer2Context *ctx) = 0;

  virtual void enterUnannType1(Java9_v2Parser::UnannType1Context *ctx) = 0;
  virtual void exitUnannType1(Java9_v2Parser::UnannType1Context *ctx) = 0;

  virtual void enterUnannType2(Java9_v2Parser::UnannType2Context *ctx) = 0;
  virtual void exitUnannType2(Java9_v2Parser::UnannType2Context *ctx) = 0;

  virtual void enterUnannPrimitiveType1(Java9_v2Parser::UnannPrimitiveType1Context *ctx) = 0;
  virtual void exitUnannPrimitiveType1(Java9_v2Parser::UnannPrimitiveType1Context *ctx) = 0;

  virtual void enterUnannPrimitiveType2(Java9_v2Parser::UnannPrimitiveType2Context *ctx) = 0;
  virtual void exitUnannPrimitiveType2(Java9_v2Parser::UnannPrimitiveType2Context *ctx) = 0;

  virtual void enterUnannReferenceType1(Java9_v2Parser::UnannReferenceType1Context *ctx) = 0;
  virtual void exitUnannReferenceType1(Java9_v2Parser::UnannReferenceType1Context *ctx) = 0;

  virtual void enterUnannReferenceType2(Java9_v2Parser::UnannReferenceType2Context *ctx) = 0;
  virtual void exitUnannReferenceType2(Java9_v2Parser::UnannReferenceType2Context *ctx) = 0;

  virtual void enterUnannReferenceType3(Java9_v2Parser::UnannReferenceType3Context *ctx) = 0;
  virtual void exitUnannReferenceType3(Java9_v2Parser::UnannReferenceType3Context *ctx) = 0;

  virtual void enterUnannClassOrInterfaceType(Java9_v2Parser::UnannClassOrInterfaceTypeContext *ctx) = 0;
  virtual void exitUnannClassOrInterfaceType(Java9_v2Parser::UnannClassOrInterfaceTypeContext *ctx) = 0;

  virtual void enterUnannClassType1(Java9_v2Parser::UnannClassType1Context *ctx) = 0;
  virtual void exitUnannClassType1(Java9_v2Parser::UnannClassType1Context *ctx) = 0;

  virtual void enterUnannClassType2(Java9_v2Parser::UnannClassType2Context *ctx) = 0;
  virtual void exitUnannClassType2(Java9_v2Parser::UnannClassType2Context *ctx) = 0;

  virtual void enterUnannClassType_lf_unannClassOrInterfaceType(Java9_v2Parser::UnannClassType_lf_unannClassOrInterfaceTypeContext *ctx) = 0;
  virtual void exitUnannClassType_lf_unannClassOrInterfaceType(Java9_v2Parser::UnannClassType_lf_unannClassOrInterfaceTypeContext *ctx) = 0;

  virtual void enterUnannClassType_lfno_unannClassOrInterfaceType(Java9_v2Parser::UnannClassType_lfno_unannClassOrInterfaceTypeContext *ctx) = 0;
  virtual void exitUnannClassType_lfno_unannClassOrInterfaceType(Java9_v2Parser::UnannClassType_lfno_unannClassOrInterfaceTypeContext *ctx) = 0;

  virtual void enterUnannInterfaceType(Java9_v2Parser::UnannInterfaceTypeContext *ctx) = 0;
  virtual void exitUnannInterfaceType(Java9_v2Parser::UnannInterfaceTypeContext *ctx) = 0;

  virtual void enterUnannInterfaceType_lf_unannClassOrInterfaceType(Java9_v2Parser::UnannInterfaceType_lf_unannClassOrInterfaceTypeContext *ctx) = 0;
  virtual void exitUnannInterfaceType_lf_unannClassOrInterfaceType(Java9_v2Parser::UnannInterfaceType_lf_unannClassOrInterfaceTypeContext *ctx) = 0;

  virtual void enterUnannInterfaceType_lfno_unannClassOrInterfaceType(Java9_v2Parser::UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext *ctx) = 0;
  virtual void exitUnannInterfaceType_lfno_unannClassOrInterfaceType(Java9_v2Parser::UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext *ctx) = 0;

  virtual void enterUnannTypeVariable(Java9_v2Parser::UnannTypeVariableContext *ctx) = 0;
  virtual void exitUnannTypeVariable(Java9_v2Parser::UnannTypeVariableContext *ctx) = 0;

  virtual void enterUnannArrayType1(Java9_v2Parser::UnannArrayType1Context *ctx) = 0;
  virtual void exitUnannArrayType1(Java9_v2Parser::UnannArrayType1Context *ctx) = 0;

  virtual void enterUnannArrayType2(Java9_v2Parser::UnannArrayType2Context *ctx) = 0;
  virtual void exitUnannArrayType2(Java9_v2Parser::UnannArrayType2Context *ctx) = 0;

  virtual void enterUnannArrayTyp3(Java9_v2Parser::UnannArrayTyp3Context *ctx) = 0;
  virtual void exitUnannArrayTyp3(Java9_v2Parser::UnannArrayTyp3Context *ctx) = 0;

  virtual void enterMethodDeclaration(Java9_v2Parser::MethodDeclarationContext *ctx) = 0;
  virtual void exitMethodDeclaration(Java9_v2Parser::MethodDeclarationContext *ctx) = 0;

  virtual void enterMethodModifier(Java9_v2Parser::MethodModifierContext *ctx) = 0;
  virtual void exitMethodModifier(Java9_v2Parser::MethodModifierContext *ctx) = 0;

  virtual void enterMethodHeader(Java9_v2Parser::MethodHeaderContext *ctx) = 0;
  virtual void exitMethodHeader(Java9_v2Parser::MethodHeaderContext *ctx) = 0;

  virtual void enterResult(Java9_v2Parser::ResultContext *ctx) = 0;
  virtual void exitResult(Java9_v2Parser::ResultContext *ctx) = 0;

  virtual void enterMethodDeclarator(Java9_v2Parser::MethodDeclaratorContext *ctx) = 0;
  virtual void exitMethodDeclarator(Java9_v2Parser::MethodDeclaratorContext *ctx) = 0;

  virtual void enterFormalParameterList1(Java9_v2Parser::FormalParameterList1Context *ctx) = 0;
  virtual void exitFormalParameterList1(Java9_v2Parser::FormalParameterList1Context *ctx) = 0;

  virtual void enterFormalParameterList2(Java9_v2Parser::FormalParameterList2Context *ctx) = 0;
  virtual void exitFormalParameterList2(Java9_v2Parser::FormalParameterList2Context *ctx) = 0;

  virtual void enterFormalParameterList3(Java9_v2Parser::FormalParameterList3Context *ctx) = 0;
  virtual void exitFormalParameterList3(Java9_v2Parser::FormalParameterList3Context *ctx) = 0;

  virtual void enterFormalParameters1(Java9_v2Parser::FormalParameters1Context *ctx) = 0;
  virtual void exitFormalParameters1(Java9_v2Parser::FormalParameters1Context *ctx) = 0;

  virtual void enterFormalParameters2(Java9_v2Parser::FormalParameters2Context *ctx) = 0;
  virtual void exitFormalParameters2(Java9_v2Parser::FormalParameters2Context *ctx) = 0;

  virtual void enterFormalParameter(Java9_v2Parser::FormalParameterContext *ctx) = 0;
  virtual void exitFormalParameter(Java9_v2Parser::FormalParameterContext *ctx) = 0;

  virtual void enterVariableModifier(Java9_v2Parser::VariableModifierContext *ctx) = 0;
  virtual void exitVariableModifier(Java9_v2Parser::VariableModifierContext *ctx) = 0;

  virtual void enterLastFormalParameter1(Java9_v2Parser::LastFormalParameter1Context *ctx) = 0;
  virtual void exitLastFormalParameter1(Java9_v2Parser::LastFormalParameter1Context *ctx) = 0;

  virtual void enterLastFormalParameter2(Java9_v2Parser::LastFormalParameter2Context *ctx) = 0;
  virtual void exitLastFormalParameter2(Java9_v2Parser::LastFormalParameter2Context *ctx) = 0;

  virtual void enterReceiverParameter(Java9_v2Parser::ReceiverParameterContext *ctx) = 0;
  virtual void exitReceiverParameter(Java9_v2Parser::ReceiverParameterContext *ctx) = 0;

  virtual void enterThrows_(Java9_v2Parser::Throws_Context *ctx) = 0;
  virtual void exitThrows_(Java9_v2Parser::Throws_Context *ctx) = 0;

  virtual void enterExceptionTypeList(Java9_v2Parser::ExceptionTypeListContext *ctx) = 0;
  virtual void exitExceptionTypeList(Java9_v2Parser::ExceptionTypeListContext *ctx) = 0;

  virtual void enterExceptionType1(Java9_v2Parser::ExceptionType1Context *ctx) = 0;
  virtual void exitExceptionType1(Java9_v2Parser::ExceptionType1Context *ctx) = 0;

  virtual void enterExceptionType2(Java9_v2Parser::ExceptionType2Context *ctx) = 0;
  virtual void exitExceptionType2(Java9_v2Parser::ExceptionType2Context *ctx) = 0;

  virtual void enterMethodBody(Java9_v2Parser::MethodBodyContext *ctx) = 0;
  virtual void exitMethodBody(Java9_v2Parser::MethodBodyContext *ctx) = 0;

  virtual void enterInstanceInitializer(Java9_v2Parser::InstanceInitializerContext *ctx) = 0;
  virtual void exitInstanceInitializer(Java9_v2Parser::InstanceInitializerContext *ctx) = 0;

  virtual void enterStaticInitializer(Java9_v2Parser::StaticInitializerContext *ctx) = 0;
  virtual void exitStaticInitializer(Java9_v2Parser::StaticInitializerContext *ctx) = 0;

  virtual void enterConstructorDeclaration(Java9_v2Parser::ConstructorDeclarationContext *ctx) = 0;
  virtual void exitConstructorDeclaration(Java9_v2Parser::ConstructorDeclarationContext *ctx) = 0;

  virtual void enterConstructorModifier(Java9_v2Parser::ConstructorModifierContext *ctx) = 0;
  virtual void exitConstructorModifier(Java9_v2Parser::ConstructorModifierContext *ctx) = 0;

  virtual void enterConstructorDeclarator(Java9_v2Parser::ConstructorDeclaratorContext *ctx) = 0;
  virtual void exitConstructorDeclarator(Java9_v2Parser::ConstructorDeclaratorContext *ctx) = 0;

  virtual void enterSimpleTypeName(Java9_v2Parser::SimpleTypeNameContext *ctx) = 0;
  virtual void exitSimpleTypeName(Java9_v2Parser::SimpleTypeNameContext *ctx) = 0;

  virtual void enterConstructorBody(Java9_v2Parser::ConstructorBodyContext *ctx) = 0;
  virtual void exitConstructorBody(Java9_v2Parser::ConstructorBodyContext *ctx) = 0;

  virtual void enterExplicitConstructorInvocation1(Java9_v2Parser::ExplicitConstructorInvocation1Context *ctx) = 0;
  virtual void exitExplicitConstructorInvocation1(Java9_v2Parser::ExplicitConstructorInvocation1Context *ctx) = 0;

  virtual void enterExplicitConstructorInvocation2(Java9_v2Parser::ExplicitConstructorInvocation2Context *ctx) = 0;
  virtual void exitExplicitConstructorInvocation2(Java9_v2Parser::ExplicitConstructorInvocation2Context *ctx) = 0;

  virtual void enterExplicitConstructorInvocation3(Java9_v2Parser::ExplicitConstructorInvocation3Context *ctx) = 0;
  virtual void exitExplicitConstructorInvocation3(Java9_v2Parser::ExplicitConstructorInvocation3Context *ctx) = 0;

  virtual void enterExplicitConstructorInvocation4(Java9_v2Parser::ExplicitConstructorInvocation4Context *ctx) = 0;
  virtual void exitExplicitConstructorInvocation4(Java9_v2Parser::ExplicitConstructorInvocation4Context *ctx) = 0;

  virtual void enterEnumDeclaration(Java9_v2Parser::EnumDeclarationContext *ctx) = 0;
  virtual void exitEnumDeclaration(Java9_v2Parser::EnumDeclarationContext *ctx) = 0;

  virtual void enterEnumBody(Java9_v2Parser::EnumBodyContext *ctx) = 0;
  virtual void exitEnumBody(Java9_v2Parser::EnumBodyContext *ctx) = 0;

  virtual void enterEnumConstantList(Java9_v2Parser::EnumConstantListContext *ctx) = 0;
  virtual void exitEnumConstantList(Java9_v2Parser::EnumConstantListContext *ctx) = 0;

  virtual void enterEnumConstant(Java9_v2Parser::EnumConstantContext *ctx) = 0;
  virtual void exitEnumConstant(Java9_v2Parser::EnumConstantContext *ctx) = 0;

  virtual void enterEnumConstantModifier(Java9_v2Parser::EnumConstantModifierContext *ctx) = 0;
  virtual void exitEnumConstantModifier(Java9_v2Parser::EnumConstantModifierContext *ctx) = 0;

  virtual void enterEnumBodyDeclarations(Java9_v2Parser::EnumBodyDeclarationsContext *ctx) = 0;
  virtual void exitEnumBodyDeclarations(Java9_v2Parser::EnumBodyDeclarationsContext *ctx) = 0;

  virtual void enterInterfaceDeclaration1(Java9_v2Parser::InterfaceDeclaration1Context *ctx) = 0;
  virtual void exitInterfaceDeclaration1(Java9_v2Parser::InterfaceDeclaration1Context *ctx) = 0;

  virtual void enterInterfaceDeclaration2(Java9_v2Parser::InterfaceDeclaration2Context *ctx) = 0;
  virtual void exitInterfaceDeclaration2(Java9_v2Parser::InterfaceDeclaration2Context *ctx) = 0;

  virtual void enterNormalInterfaceDeclaration(Java9_v2Parser::NormalInterfaceDeclarationContext *ctx) = 0;
  virtual void exitNormalInterfaceDeclaration(Java9_v2Parser::NormalInterfaceDeclarationContext *ctx) = 0;

  virtual void enterInterfaceModifier(Java9_v2Parser::InterfaceModifierContext *ctx) = 0;
  virtual void exitInterfaceModifier(Java9_v2Parser::InterfaceModifierContext *ctx) = 0;

  virtual void enterExtendsInterfaces(Java9_v2Parser::ExtendsInterfacesContext *ctx) = 0;
  virtual void exitExtendsInterfaces(Java9_v2Parser::ExtendsInterfacesContext *ctx) = 0;

  virtual void enterInterfaceBody(Java9_v2Parser::InterfaceBodyContext *ctx) = 0;
  virtual void exitInterfaceBody(Java9_v2Parser::InterfaceBodyContext *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration1(Java9_v2Parser::InterfaceMemberDeclaration1Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration1(Java9_v2Parser::InterfaceMemberDeclaration1Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration2(Java9_v2Parser::InterfaceMemberDeclaration2Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration2(Java9_v2Parser::InterfaceMemberDeclaration2Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration3(Java9_v2Parser::InterfaceMemberDeclaration3Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration3(Java9_v2Parser::InterfaceMemberDeclaration3Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration4(Java9_v2Parser::InterfaceMemberDeclaration4Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration4(Java9_v2Parser::InterfaceMemberDeclaration4Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration5(Java9_v2Parser::InterfaceMemberDeclaration5Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration5(Java9_v2Parser::InterfaceMemberDeclaration5Context *ctx) = 0;

  virtual void enterConstantDeclaration(Java9_v2Parser::ConstantDeclarationContext *ctx) = 0;
  virtual void exitConstantDeclaration(Java9_v2Parser::ConstantDeclarationContext *ctx) = 0;

  virtual void enterConstantModifier(Java9_v2Parser::ConstantModifierContext *ctx) = 0;
  virtual void exitConstantModifier(Java9_v2Parser::ConstantModifierContext *ctx) = 0;

  virtual void enterInterfaceMethodDeclaration(Java9_v2Parser::InterfaceMethodDeclarationContext *ctx) = 0;
  virtual void exitInterfaceMethodDeclaration(Java9_v2Parser::InterfaceMethodDeclarationContext *ctx) = 0;

  virtual void enterInterfaceMethodModifier(Java9_v2Parser::InterfaceMethodModifierContext *ctx) = 0;
  virtual void exitInterfaceMethodModifier(Java9_v2Parser::InterfaceMethodModifierContext *ctx) = 0;

  virtual void enterAnnotationTypeDeclaration(Java9_v2Parser::AnnotationTypeDeclarationContext *ctx) = 0;
  virtual void exitAnnotationTypeDeclaration(Java9_v2Parser::AnnotationTypeDeclarationContext *ctx) = 0;

  virtual void enterAnnotationTypeBody(Java9_v2Parser::AnnotationTypeBodyContext *ctx) = 0;
  virtual void exitAnnotationTypeBody(Java9_v2Parser::AnnotationTypeBodyContext *ctx) = 0;

  virtual void enterAnnotationTypeMemberDeclaration1(Java9_v2Parser::AnnotationTypeMemberDeclaration1Context *ctx) = 0;
  virtual void exitAnnotationTypeMemberDeclaration1(Java9_v2Parser::AnnotationTypeMemberDeclaration1Context *ctx) = 0;

  virtual void enterAnnotationTypeMemberDeclaration2(Java9_v2Parser::AnnotationTypeMemberDeclaration2Context *ctx) = 0;
  virtual void exitAnnotationTypeMemberDeclaration2(Java9_v2Parser::AnnotationTypeMemberDeclaration2Context *ctx) = 0;

  virtual void enterAnnotationTypeMemberDeclaration3(Java9_v2Parser::AnnotationTypeMemberDeclaration3Context *ctx) = 0;
  virtual void exitAnnotationTypeMemberDeclaration3(Java9_v2Parser::AnnotationTypeMemberDeclaration3Context *ctx) = 0;

  virtual void enterAnnotationTypeMemberDeclaration4(Java9_v2Parser::AnnotationTypeMemberDeclaration4Context *ctx) = 0;
  virtual void exitAnnotationTypeMemberDeclaration4(Java9_v2Parser::AnnotationTypeMemberDeclaration4Context *ctx) = 0;

  virtual void enterAnnotationTypeMemberDeclaration5(Java9_v2Parser::AnnotationTypeMemberDeclaration5Context *ctx) = 0;
  virtual void exitAnnotationTypeMemberDeclaration5(Java9_v2Parser::AnnotationTypeMemberDeclaration5Context *ctx) = 0;

  virtual void enterAnnotationTypeElementDeclaration(Java9_v2Parser::AnnotationTypeElementDeclarationContext *ctx) = 0;
  virtual void exitAnnotationTypeElementDeclaration(Java9_v2Parser::AnnotationTypeElementDeclarationContext *ctx) = 0;

  virtual void enterAnnotationTypeElementModifier(Java9_v2Parser::AnnotationTypeElementModifierContext *ctx) = 0;
  virtual void exitAnnotationTypeElementModifier(Java9_v2Parser::AnnotationTypeElementModifierContext *ctx) = 0;

  virtual void enterDefaultValue(Java9_v2Parser::DefaultValueContext *ctx) = 0;
  virtual void exitDefaultValue(Java9_v2Parser::DefaultValueContext *ctx) = 0;

  virtual void enterAnnotation1(Java9_v2Parser::Annotation1Context *ctx) = 0;
  virtual void exitAnnotation1(Java9_v2Parser::Annotation1Context *ctx) = 0;

  virtual void enterAnnotation2(Java9_v2Parser::Annotation2Context *ctx) = 0;
  virtual void exitAnnotation2(Java9_v2Parser::Annotation2Context *ctx) = 0;

  virtual void enterAnnotation3(Java9_v2Parser::Annotation3Context *ctx) = 0;
  virtual void exitAnnotation3(Java9_v2Parser::Annotation3Context *ctx) = 0;

  virtual void enterNormalAnnotation(Java9_v2Parser::NormalAnnotationContext *ctx) = 0;
  virtual void exitNormalAnnotation(Java9_v2Parser::NormalAnnotationContext *ctx) = 0;

  virtual void enterElementValuePairList(Java9_v2Parser::ElementValuePairListContext *ctx) = 0;
  virtual void exitElementValuePairList(Java9_v2Parser::ElementValuePairListContext *ctx) = 0;

  virtual void enterElementValuePair(Java9_v2Parser::ElementValuePairContext *ctx) = 0;
  virtual void exitElementValuePair(Java9_v2Parser::ElementValuePairContext *ctx) = 0;

  virtual void enterElementValue1(Java9_v2Parser::ElementValue1Context *ctx) = 0;
  virtual void exitElementValue1(Java9_v2Parser::ElementValue1Context *ctx) = 0;

  virtual void enterElementValue2(Java9_v2Parser::ElementValue2Context *ctx) = 0;
  virtual void exitElementValue2(Java9_v2Parser::ElementValue2Context *ctx) = 0;

  virtual void enterElementValu3(Java9_v2Parser::ElementValu3Context *ctx) = 0;
  virtual void exitElementValu3(Java9_v2Parser::ElementValu3Context *ctx) = 0;

  virtual void enterElementValueArrayInitializer(Java9_v2Parser::ElementValueArrayInitializerContext *ctx) = 0;
  virtual void exitElementValueArrayInitializer(Java9_v2Parser::ElementValueArrayInitializerContext *ctx) = 0;

  virtual void enterElementValueList(Java9_v2Parser::ElementValueListContext *ctx) = 0;
  virtual void exitElementValueList(Java9_v2Parser::ElementValueListContext *ctx) = 0;

  virtual void enterMarkerAnnotation(Java9_v2Parser::MarkerAnnotationContext *ctx) = 0;
  virtual void exitMarkerAnnotation(Java9_v2Parser::MarkerAnnotationContext *ctx) = 0;

  virtual void enterSingleElementAnnotation(Java9_v2Parser::SingleElementAnnotationContext *ctx) = 0;
  virtual void exitSingleElementAnnotation(Java9_v2Parser::SingleElementAnnotationContext *ctx) = 0;

  virtual void enterArrayInitializer(Java9_v2Parser::ArrayInitializerContext *ctx) = 0;
  virtual void exitArrayInitializer(Java9_v2Parser::ArrayInitializerContext *ctx) = 0;

  virtual void enterVariableInitializerList(Java9_v2Parser::VariableInitializerListContext *ctx) = 0;
  virtual void exitVariableInitializerList(Java9_v2Parser::VariableInitializerListContext *ctx) = 0;

  virtual void enterBlock(Java9_v2Parser::BlockContext *ctx) = 0;
  virtual void exitBlock(Java9_v2Parser::BlockContext *ctx) = 0;

  virtual void enterBlockStatements(Java9_v2Parser::BlockStatementsContext *ctx) = 0;
  virtual void exitBlockStatements(Java9_v2Parser::BlockStatementsContext *ctx) = 0;

  virtual void enterBlockStatement1(Java9_v2Parser::BlockStatement1Context *ctx) = 0;
  virtual void exitBlockStatement1(Java9_v2Parser::BlockStatement1Context *ctx) = 0;

  virtual void enterBlockStatement2(Java9_v2Parser::BlockStatement2Context *ctx) = 0;
  virtual void exitBlockStatement2(Java9_v2Parser::BlockStatement2Context *ctx) = 0;

  virtual void enterBlockStatement3(Java9_v2Parser::BlockStatement3Context *ctx) = 0;
  virtual void exitBlockStatement3(Java9_v2Parser::BlockStatement3Context *ctx) = 0;

  virtual void enterLocalVariableDeclarationStatement(Java9_v2Parser::LocalVariableDeclarationStatementContext *ctx) = 0;
  virtual void exitLocalVariableDeclarationStatement(Java9_v2Parser::LocalVariableDeclarationStatementContext *ctx) = 0;

  virtual void enterLocalVariableDeclaration(Java9_v2Parser::LocalVariableDeclarationContext *ctx) = 0;
  virtual void exitLocalVariableDeclaration(Java9_v2Parser::LocalVariableDeclarationContext *ctx) = 0;

  virtual void enterStatement1(Java9_v2Parser::Statement1Context *ctx) = 0;
  virtual void exitStatement1(Java9_v2Parser::Statement1Context *ctx) = 0;

  virtual void enterStatement2(Java9_v2Parser::Statement2Context *ctx) = 0;
  virtual void exitStatement2(Java9_v2Parser::Statement2Context *ctx) = 0;

  virtual void enterStatement3(Java9_v2Parser::Statement3Context *ctx) = 0;
  virtual void exitStatement3(Java9_v2Parser::Statement3Context *ctx) = 0;

  virtual void enterStatement4(Java9_v2Parser::Statement4Context *ctx) = 0;
  virtual void exitStatement4(Java9_v2Parser::Statement4Context *ctx) = 0;

  virtual void enterStatement5(Java9_v2Parser::Statement5Context *ctx) = 0;
  virtual void exitStatement5(Java9_v2Parser::Statement5Context *ctx) = 0;

  virtual void enterStatement6(Java9_v2Parser::Statement6Context *ctx) = 0;
  virtual void exitStatement6(Java9_v2Parser::Statement6Context *ctx) = 0;

  virtual void enterStatementNoShortIf1(Java9_v2Parser::StatementNoShortIf1Context *ctx) = 0;
  virtual void exitStatementNoShortIf1(Java9_v2Parser::StatementNoShortIf1Context *ctx) = 0;

  virtual void enterStatementNoShortIf2(Java9_v2Parser::StatementNoShortIf2Context *ctx) = 0;
  virtual void exitStatementNoShortIf2(Java9_v2Parser::StatementNoShortIf2Context *ctx) = 0;

  virtual void enterStatementNoShortIf3(Java9_v2Parser::StatementNoShortIf3Context *ctx) = 0;
  virtual void exitStatementNoShortIf3(Java9_v2Parser::StatementNoShortIf3Context *ctx) = 0;

  virtual void enterStatementNoShortIf4(Java9_v2Parser::StatementNoShortIf4Context *ctx) = 0;
  virtual void exitStatementNoShortIf4(Java9_v2Parser::StatementNoShortIf4Context *ctx) = 0;

  virtual void enterStatementNoShortIf5(Java9_v2Parser::StatementNoShortIf5Context *ctx) = 0;
  virtual void exitStatementNoShortIf5(Java9_v2Parser::StatementNoShortIf5Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement1(Java9_v2Parser::StatementWithoutTrailingSubstatement1Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement1(Java9_v2Parser::StatementWithoutTrailingSubstatement1Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement2(Java9_v2Parser::StatementWithoutTrailingSubstatement2Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement2(Java9_v2Parser::StatementWithoutTrailingSubstatement2Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement3(Java9_v2Parser::StatementWithoutTrailingSubstatement3Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement3(Java9_v2Parser::StatementWithoutTrailingSubstatement3Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement4(Java9_v2Parser::StatementWithoutTrailingSubstatement4Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement4(Java9_v2Parser::StatementWithoutTrailingSubstatement4Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement5(Java9_v2Parser::StatementWithoutTrailingSubstatement5Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement5(Java9_v2Parser::StatementWithoutTrailingSubstatement5Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement6(Java9_v2Parser::StatementWithoutTrailingSubstatement6Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement6(Java9_v2Parser::StatementWithoutTrailingSubstatement6Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement7(Java9_v2Parser::StatementWithoutTrailingSubstatement7Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement7(Java9_v2Parser::StatementWithoutTrailingSubstatement7Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement8(Java9_v2Parser::StatementWithoutTrailingSubstatement8Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement8(Java9_v2Parser::StatementWithoutTrailingSubstatement8Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement9(Java9_v2Parser::StatementWithoutTrailingSubstatement9Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement9(Java9_v2Parser::StatementWithoutTrailingSubstatement9Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement10(Java9_v2Parser::StatementWithoutTrailingSubstatement10Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement10(Java9_v2Parser::StatementWithoutTrailingSubstatement10Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement11(Java9_v2Parser::StatementWithoutTrailingSubstatement11Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement11(Java9_v2Parser::StatementWithoutTrailingSubstatement11Context *ctx) = 0;

  virtual void enterStatementWithoutTrailingSubstatement12(Java9_v2Parser::StatementWithoutTrailingSubstatement12Context *ctx) = 0;
  virtual void exitStatementWithoutTrailingSubstatement12(Java9_v2Parser::StatementWithoutTrailingSubstatement12Context *ctx) = 0;

  virtual void enterEmptyStatement(Java9_v2Parser::EmptyStatementContext *ctx) = 0;
  virtual void exitEmptyStatement(Java9_v2Parser::EmptyStatementContext *ctx) = 0;

  virtual void enterLabeledStatement(Java9_v2Parser::LabeledStatementContext *ctx) = 0;
  virtual void exitLabeledStatement(Java9_v2Parser::LabeledStatementContext *ctx) = 0;

  virtual void enterLabeledStatementNoShortIf(Java9_v2Parser::LabeledStatementNoShortIfContext *ctx) = 0;
  virtual void exitLabeledStatementNoShortIf(Java9_v2Parser::LabeledStatementNoShortIfContext *ctx) = 0;

  virtual void enterExpressionStatement(Java9_v2Parser::ExpressionStatementContext *ctx) = 0;
  virtual void exitExpressionStatement(Java9_v2Parser::ExpressionStatementContext *ctx) = 0;

  virtual void enterStatementExpression1(Java9_v2Parser::StatementExpression1Context *ctx) = 0;
  virtual void exitStatementExpression1(Java9_v2Parser::StatementExpression1Context *ctx) = 0;

  virtual void enterStatementExpression2(Java9_v2Parser::StatementExpression2Context *ctx) = 0;
  virtual void exitStatementExpression2(Java9_v2Parser::StatementExpression2Context *ctx) = 0;

  virtual void enterStatementExpression3(Java9_v2Parser::StatementExpression3Context *ctx) = 0;
  virtual void exitStatementExpression3(Java9_v2Parser::StatementExpression3Context *ctx) = 0;

  virtual void enterStatementExpression4(Java9_v2Parser::StatementExpression4Context *ctx) = 0;
  virtual void exitStatementExpression4(Java9_v2Parser::StatementExpression4Context *ctx) = 0;

  virtual void enterStatementExpression5(Java9_v2Parser::StatementExpression5Context *ctx) = 0;
  virtual void exitStatementExpression5(Java9_v2Parser::StatementExpression5Context *ctx) = 0;

  virtual void enterStatementExpression6(Java9_v2Parser::StatementExpression6Context *ctx) = 0;
  virtual void exitStatementExpression6(Java9_v2Parser::StatementExpression6Context *ctx) = 0;

  virtual void enterStatementExpression7(Java9_v2Parser::StatementExpression7Context *ctx) = 0;
  virtual void exitStatementExpression7(Java9_v2Parser::StatementExpression7Context *ctx) = 0;

  virtual void enterIfThenStatement(Java9_v2Parser::IfThenStatementContext *ctx) = 0;
  virtual void exitIfThenStatement(Java9_v2Parser::IfThenStatementContext *ctx) = 0;

  virtual void enterIfThenElseStatement(Java9_v2Parser::IfThenElseStatementContext *ctx) = 0;
  virtual void exitIfThenElseStatement(Java9_v2Parser::IfThenElseStatementContext *ctx) = 0;

  virtual void enterIfThenElseStatementNoShortIf(Java9_v2Parser::IfThenElseStatementNoShortIfContext *ctx) = 0;
  virtual void exitIfThenElseStatementNoShortIf(Java9_v2Parser::IfThenElseStatementNoShortIfContext *ctx) = 0;

  virtual void enterAssertStatement1(Java9_v2Parser::AssertStatement1Context *ctx) = 0;
  virtual void exitAssertStatement1(Java9_v2Parser::AssertStatement1Context *ctx) = 0;

  virtual void enterAssertStatement2(Java9_v2Parser::AssertStatement2Context *ctx) = 0;
  virtual void exitAssertStatement2(Java9_v2Parser::AssertStatement2Context *ctx) = 0;

  virtual void enterSwitchStatement(Java9_v2Parser::SwitchStatementContext *ctx) = 0;
  virtual void exitSwitchStatement(Java9_v2Parser::SwitchStatementContext *ctx) = 0;

  virtual void enterSwitchBlock(Java9_v2Parser::SwitchBlockContext *ctx) = 0;
  virtual void exitSwitchBlock(Java9_v2Parser::SwitchBlockContext *ctx) = 0;

  virtual void enterSwitchBlockStatementGroup(Java9_v2Parser::SwitchBlockStatementGroupContext *ctx) = 0;
  virtual void exitSwitchBlockStatementGroup(Java9_v2Parser::SwitchBlockStatementGroupContext *ctx) = 0;

  virtual void enterSwitchLabels(Java9_v2Parser::SwitchLabelsContext *ctx) = 0;
  virtual void exitSwitchLabels(Java9_v2Parser::SwitchLabelsContext *ctx) = 0;

  virtual void enterSwitchLabel1(Java9_v2Parser::SwitchLabel1Context *ctx) = 0;
  virtual void exitSwitchLabel1(Java9_v2Parser::SwitchLabel1Context *ctx) = 0;

  virtual void enterSwitchLabel2(Java9_v2Parser::SwitchLabel2Context *ctx) = 0;
  virtual void exitSwitchLabel2(Java9_v2Parser::SwitchLabel2Context *ctx) = 0;

  virtual void enterSwitchLabel3(Java9_v2Parser::SwitchLabel3Context *ctx) = 0;
  virtual void exitSwitchLabel3(Java9_v2Parser::SwitchLabel3Context *ctx) = 0;

  virtual void enterEnumConstantName(Java9_v2Parser::EnumConstantNameContext *ctx) = 0;
  virtual void exitEnumConstantName(Java9_v2Parser::EnumConstantNameContext *ctx) = 0;

  virtual void enterWhileStatement(Java9_v2Parser::WhileStatementContext *ctx) = 0;
  virtual void exitWhileStatement(Java9_v2Parser::WhileStatementContext *ctx) = 0;

  virtual void enterWhileStatementNoShortIf(Java9_v2Parser::WhileStatementNoShortIfContext *ctx) = 0;
  virtual void exitWhileStatementNoShortIf(Java9_v2Parser::WhileStatementNoShortIfContext *ctx) = 0;

  virtual void enterDoStatement(Java9_v2Parser::DoStatementContext *ctx) = 0;
  virtual void exitDoStatement(Java9_v2Parser::DoStatementContext *ctx) = 0;

  virtual void enterForStatement1(Java9_v2Parser::ForStatement1Context *ctx) = 0;
  virtual void exitForStatement1(Java9_v2Parser::ForStatement1Context *ctx) = 0;

  virtual void enterForStatement2(Java9_v2Parser::ForStatement2Context *ctx) = 0;
  virtual void exitForStatement2(Java9_v2Parser::ForStatement2Context *ctx) = 0;

  virtual void enterForStatementNoShortIf3(Java9_v2Parser::ForStatementNoShortIf3Context *ctx) = 0;
  virtual void exitForStatementNoShortIf3(Java9_v2Parser::ForStatementNoShortIf3Context *ctx) = 0;

  virtual void enterForStatementNoShortIf4(Java9_v2Parser::ForStatementNoShortIf4Context *ctx) = 0;
  virtual void exitForStatementNoShortIf4(Java9_v2Parser::ForStatementNoShortIf4Context *ctx) = 0;

  virtual void enterBasicForStatement(Java9_v2Parser::BasicForStatementContext *ctx) = 0;
  virtual void exitBasicForStatement(Java9_v2Parser::BasicForStatementContext *ctx) = 0;

  virtual void enterBasicForStatementNoShortIf(Java9_v2Parser::BasicForStatementNoShortIfContext *ctx) = 0;
  virtual void exitBasicForStatementNoShortIf(Java9_v2Parser::BasicForStatementNoShortIfContext *ctx) = 0;

  virtual void enterForInit1(Java9_v2Parser::ForInit1Context *ctx) = 0;
  virtual void exitForInit1(Java9_v2Parser::ForInit1Context *ctx) = 0;

  virtual void enterForInit2(Java9_v2Parser::ForInit2Context *ctx) = 0;
  virtual void exitForInit2(Java9_v2Parser::ForInit2Context *ctx) = 0;

  virtual void enterForUpdate(Java9_v2Parser::ForUpdateContext *ctx) = 0;
  virtual void exitForUpdate(Java9_v2Parser::ForUpdateContext *ctx) = 0;

  virtual void enterStatementExpressionList(Java9_v2Parser::StatementExpressionListContext *ctx) = 0;
  virtual void exitStatementExpressionList(Java9_v2Parser::StatementExpressionListContext *ctx) = 0;

  virtual void enterEnhancedForStatement(Java9_v2Parser::EnhancedForStatementContext *ctx) = 0;
  virtual void exitEnhancedForStatement(Java9_v2Parser::EnhancedForStatementContext *ctx) = 0;

  virtual void enterEnhancedForStatementNoShortIf(Java9_v2Parser::EnhancedForStatementNoShortIfContext *ctx) = 0;
  virtual void exitEnhancedForStatementNoShortIf(Java9_v2Parser::EnhancedForStatementNoShortIfContext *ctx) = 0;

  virtual void enterBreakStatement(Java9_v2Parser::BreakStatementContext *ctx) = 0;
  virtual void exitBreakStatement(Java9_v2Parser::BreakStatementContext *ctx) = 0;

  virtual void enterContinueStatement(Java9_v2Parser::ContinueStatementContext *ctx) = 0;
  virtual void exitContinueStatement(Java9_v2Parser::ContinueStatementContext *ctx) = 0;

  virtual void enterReturnStatement(Java9_v2Parser::ReturnStatementContext *ctx) = 0;
  virtual void exitReturnStatement(Java9_v2Parser::ReturnStatementContext *ctx) = 0;

  virtual void enterThrowStatement(Java9_v2Parser::ThrowStatementContext *ctx) = 0;
  virtual void exitThrowStatement(Java9_v2Parser::ThrowStatementContext *ctx) = 0;

  virtual void enterSynchronizedStatement(Java9_v2Parser::SynchronizedStatementContext *ctx) = 0;
  virtual void exitSynchronizedStatement(Java9_v2Parser::SynchronizedStatementContext *ctx) = 0;

  virtual void enterTryStatement1(Java9_v2Parser::TryStatement1Context *ctx) = 0;
  virtual void exitTryStatement1(Java9_v2Parser::TryStatement1Context *ctx) = 0;

  virtual void enterTryStatement2(Java9_v2Parser::TryStatement2Context *ctx) = 0;
  virtual void exitTryStatement2(Java9_v2Parser::TryStatement2Context *ctx) = 0;

  virtual void enterTryStatement3(Java9_v2Parser::TryStatement3Context *ctx) = 0;
  virtual void exitTryStatement3(Java9_v2Parser::TryStatement3Context *ctx) = 0;

  virtual void enterCatches(Java9_v2Parser::CatchesContext *ctx) = 0;
  virtual void exitCatches(Java9_v2Parser::CatchesContext *ctx) = 0;

  virtual void enterCatchClause(Java9_v2Parser::CatchClauseContext *ctx) = 0;
  virtual void exitCatchClause(Java9_v2Parser::CatchClauseContext *ctx) = 0;

  virtual void enterCatchFormalParameter(Java9_v2Parser::CatchFormalParameterContext *ctx) = 0;
  virtual void exitCatchFormalParameter(Java9_v2Parser::CatchFormalParameterContext *ctx) = 0;

  virtual void enterCatchType(Java9_v2Parser::CatchTypeContext *ctx) = 0;
  virtual void exitCatchType(Java9_v2Parser::CatchTypeContext *ctx) = 0;

  virtual void enterFinally_(Java9_v2Parser::Finally_Context *ctx) = 0;
  virtual void exitFinally_(Java9_v2Parser::Finally_Context *ctx) = 0;

  virtual void enterTryWithResourcesStatement(Java9_v2Parser::TryWithResourcesStatementContext *ctx) = 0;
  virtual void exitTryWithResourcesStatement(Java9_v2Parser::TryWithResourcesStatementContext *ctx) = 0;

  virtual void enterResourceSpecification(Java9_v2Parser::ResourceSpecificationContext *ctx) = 0;
  virtual void exitResourceSpecification(Java9_v2Parser::ResourceSpecificationContext *ctx) = 0;

  virtual void enterResourceList(Java9_v2Parser::ResourceListContext *ctx) = 0;
  virtual void exitResourceList(Java9_v2Parser::ResourceListContext *ctx) = 0;

  virtual void enterResource1(Java9_v2Parser::Resource1Context *ctx) = 0;
  virtual void exitResource1(Java9_v2Parser::Resource1Context *ctx) = 0;

  virtual void enterResource2(Java9_v2Parser::Resource2Context *ctx) = 0;
  virtual void exitResource2(Java9_v2Parser::Resource2Context *ctx) = 0;

  virtual void enterVariableAccess1(Java9_v2Parser::VariableAccess1Context *ctx) = 0;
  virtual void exitVariableAccess1(Java9_v2Parser::VariableAccess1Context *ctx) = 0;

  virtual void enterVariableAccess2(Java9_v2Parser::VariableAccess2Context *ctx) = 0;
  virtual void exitVariableAccess2(Java9_v2Parser::VariableAccess2Context *ctx) = 0;

  virtual void enterPrimary(Java9_v2Parser::PrimaryContext *ctx) = 0;
  virtual void exitPrimary(Java9_v2Parser::PrimaryContext *ctx) = 0;

  virtual void enterPrimaryNoNewArray1(Java9_v2Parser::PrimaryNoNewArray1Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray1(Java9_v2Parser::PrimaryNoNewArray1Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray2(Java9_v2Parser::PrimaryNoNewArray2Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray2(Java9_v2Parser::PrimaryNoNewArray2Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray3(Java9_v2Parser::PrimaryNoNewArray3Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray3(Java9_v2Parser::PrimaryNoNewArray3Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray4(Java9_v2Parser::PrimaryNoNewArray4Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray4(Java9_v2Parser::PrimaryNoNewArray4Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray5(Java9_v2Parser::PrimaryNoNewArray5Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray5(Java9_v2Parser::PrimaryNoNewArray5Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray6(Java9_v2Parser::PrimaryNoNewArray6Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray6(Java9_v2Parser::PrimaryNoNewArray6Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray7(Java9_v2Parser::PrimaryNoNewArray7Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray7(Java9_v2Parser::PrimaryNoNewArray7Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray8(Java9_v2Parser::PrimaryNoNewArray8Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray8(Java9_v2Parser::PrimaryNoNewArray8Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray9(Java9_v2Parser::PrimaryNoNewArray9Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray9(Java9_v2Parser::PrimaryNoNewArray9Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray10(Java9_v2Parser::PrimaryNoNewArray10Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray10(Java9_v2Parser::PrimaryNoNewArray10Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_arrayAccess(Java9_v2Parser::PrimaryNoNewArray_lf_arrayAccessContext *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_arrayAccess(Java9_v2Parser::PrimaryNoNewArray_lf_arrayAccessContext *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess1(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess1Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess1(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess1Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess2(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess2Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess2(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess2Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess3(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess3Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess3(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess3Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess4(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess4Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess4(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess4Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess5(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess5Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess5(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess5Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess6(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess6Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess6(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess6Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess7(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess7Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess7(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess7Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess8(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess8Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess8(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess8Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess9(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess9Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess9(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess9Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_arrayAccess10(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess10Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_arrayAccess10(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess10Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary1(Java9_v2Parser::PrimaryNoNewArray_lf_primary1Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary1(Java9_v2Parser::PrimaryNoNewArray_lf_primary1Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary2(Java9_v2Parser::PrimaryNoNewArray_lf_primary2Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary2(Java9_v2Parser::PrimaryNoNewArray_lf_primary2Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary3(Java9_v2Parser::PrimaryNoNewArray_lf_primary3Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary3(Java9_v2Parser::PrimaryNoNewArray_lf_primary3Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary4(Java9_v2Parser::PrimaryNoNewArray_lf_primary4Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary4(Java9_v2Parser::PrimaryNoNewArray_lf_primary4Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary5(Java9_v2Parser::PrimaryNoNewArray_lf_primary5Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary5(Java9_v2Parser::PrimaryNoNewArray_lf_primary5Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary1(Java9_v2Parser::PrimaryNoNewArray_lfno_primary1Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary1(Java9_v2Parser::PrimaryNoNewArray_lfno_primary1Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary2(Java9_v2Parser::PrimaryNoNewArray_lfno_primary2Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary2(Java9_v2Parser::PrimaryNoNewArray_lfno_primary2Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary3(Java9_v2Parser::PrimaryNoNewArray_lfno_primary3Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary3(Java9_v2Parser::PrimaryNoNewArray_lfno_primary3Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary4(Java9_v2Parser::PrimaryNoNewArray_lfno_primary4Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary4(Java9_v2Parser::PrimaryNoNewArray_lfno_primary4Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary5(Java9_v2Parser::PrimaryNoNewArray_lfno_primary5Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary5(Java9_v2Parser::PrimaryNoNewArray_lfno_primary5Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary6(Java9_v2Parser::PrimaryNoNewArray_lfno_primary6Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary6(Java9_v2Parser::PrimaryNoNewArray_lfno_primary6Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary7(Java9_v2Parser::PrimaryNoNewArray_lfno_primary7Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary7(Java9_v2Parser::PrimaryNoNewArray_lfno_primary7Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary8(Java9_v2Parser::PrimaryNoNewArray_lfno_primary8Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary8(Java9_v2Parser::PrimaryNoNewArray_lfno_primary8Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary9(Java9_v2Parser::PrimaryNoNewArray_lfno_primary9Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary9(Java9_v2Parser::PrimaryNoNewArray_lfno_primary9Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary10(Java9_v2Parser::PrimaryNoNewArray_lfno_primary10Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary10(Java9_v2Parser::PrimaryNoNewArray_lfno_primary10Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary11(Java9_v2Parser::PrimaryNoNewArray_lfno_primary11Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary11(Java9_v2Parser::PrimaryNoNewArray_lfno_primary11Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary12(Java9_v2Parser::PrimaryNoNewArray_lfno_primary12Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary12(Java9_v2Parser::PrimaryNoNewArray_lfno_primary12Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10Context *ctx) = 0;

  virtual void enterPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11Context *ctx) = 0;
  virtual void exitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11Context *ctx) = 0;

  virtual void enterClassLiteral1(Java9_v2Parser::ClassLiteral1Context *ctx) = 0;
  virtual void exitClassLiteral1(Java9_v2Parser::ClassLiteral1Context *ctx) = 0;

  virtual void enterClassLiteral2(Java9_v2Parser::ClassLiteral2Context *ctx) = 0;
  virtual void exitClassLiteral2(Java9_v2Parser::ClassLiteral2Context *ctx) = 0;

  virtual void enterClassInstanceCreationExpression1(Java9_v2Parser::ClassInstanceCreationExpression1Context *ctx) = 0;
  virtual void exitClassInstanceCreationExpression1(Java9_v2Parser::ClassInstanceCreationExpression1Context *ctx) = 0;

  virtual void enterClassInstanceCreationExpression2(Java9_v2Parser::ClassInstanceCreationExpression2Context *ctx) = 0;
  virtual void exitClassInstanceCreationExpression2(Java9_v2Parser::ClassInstanceCreationExpression2Context *ctx) = 0;

  virtual void enterClassInstanceCreationExpression3(Java9_v2Parser::ClassInstanceCreationExpression3Context *ctx) = 0;
  virtual void exitClassInstanceCreationExpression3(Java9_v2Parser::ClassInstanceCreationExpression3Context *ctx) = 0;

  virtual void enterClassInstanceCreationExpression_lf_primary(Java9_v2Parser::ClassInstanceCreationExpression_lf_primaryContext *ctx) = 0;
  virtual void exitClassInstanceCreationExpression_lf_primary(Java9_v2Parser::ClassInstanceCreationExpression_lf_primaryContext *ctx) = 0;

  virtual void enterClassInstanceCreationExpression_lfno_primary1(Java9_v2Parser::ClassInstanceCreationExpression_lfno_primary1Context *ctx) = 0;
  virtual void exitClassInstanceCreationExpression_lfno_primary1(Java9_v2Parser::ClassInstanceCreationExpression_lfno_primary1Context *ctx) = 0;

  virtual void enterClassInstanceCreationExpression_lfno_primary2(Java9_v2Parser::ClassInstanceCreationExpression_lfno_primary2Context *ctx) = 0;
  virtual void exitClassInstanceCreationExpression_lfno_primary2(Java9_v2Parser::ClassInstanceCreationExpression_lfno_primary2Context *ctx) = 0;

  virtual void enterTypeArgumentsOrDiamond1(Java9_v2Parser::TypeArgumentsOrDiamond1Context *ctx) = 0;
  virtual void exitTypeArgumentsOrDiamond1(Java9_v2Parser::TypeArgumentsOrDiamond1Context *ctx) = 0;

  virtual void enterTypeArgumentsOrDiamond2(Java9_v2Parser::TypeArgumentsOrDiamond2Context *ctx) = 0;
  virtual void exitTypeArgumentsOrDiamond2(Java9_v2Parser::TypeArgumentsOrDiamond2Context *ctx) = 0;

  virtual void enterFieldAccess1(Java9_v2Parser::FieldAccess1Context *ctx) = 0;
  virtual void exitFieldAccess1(Java9_v2Parser::FieldAccess1Context *ctx) = 0;

  virtual void enterFieldAccess2(Java9_v2Parser::FieldAccess2Context *ctx) = 0;
  virtual void exitFieldAccess2(Java9_v2Parser::FieldAccess2Context *ctx) = 0;

  virtual void enterFieldAccess3(Java9_v2Parser::FieldAccess3Context *ctx) = 0;
  virtual void exitFieldAccess3(Java9_v2Parser::FieldAccess3Context *ctx) = 0;

  virtual void enterFieldAccess_lf_primary(Java9_v2Parser::FieldAccess_lf_primaryContext *ctx) = 0;
  virtual void exitFieldAccess_lf_primary(Java9_v2Parser::FieldAccess_lf_primaryContext *ctx) = 0;

  virtual void enterFieldAccess_lfno_primary1(Java9_v2Parser::FieldAccess_lfno_primary1Context *ctx) = 0;
  virtual void exitFieldAccess_lfno_primary1(Java9_v2Parser::FieldAccess_lfno_primary1Context *ctx) = 0;

  virtual void enterFieldAccess_lfno_primary2(Java9_v2Parser::FieldAccess_lfno_primary2Context *ctx) = 0;
  virtual void exitFieldAccess_lfno_primary2(Java9_v2Parser::FieldAccess_lfno_primary2Context *ctx) = 0;

  virtual void enterArrayAccess(Java9_v2Parser::ArrayAccessContext *ctx) = 0;
  virtual void exitArrayAccess(Java9_v2Parser::ArrayAccessContext *ctx) = 0;

  virtual void enterArrayAccess_lf_primary(Java9_v2Parser::ArrayAccess_lf_primaryContext *ctx) = 0;
  virtual void exitArrayAccess_lf_primary(Java9_v2Parser::ArrayAccess_lf_primaryContext *ctx) = 0;

  virtual void enterArrayAccess_lfno_primary(Java9_v2Parser::ArrayAccess_lfno_primaryContext *ctx) = 0;
  virtual void exitArrayAccess_lfno_primary(Java9_v2Parser::ArrayAccess_lfno_primaryContext *ctx) = 0;

  virtual void enterMethodInvocation1(Java9_v2Parser::MethodInvocation1Context *ctx) = 0;
  virtual void exitMethodInvocation1(Java9_v2Parser::MethodInvocation1Context *ctx) = 0;

  virtual void enterMethodInvocation2(Java9_v2Parser::MethodInvocation2Context *ctx) = 0;
  virtual void exitMethodInvocation2(Java9_v2Parser::MethodInvocation2Context *ctx) = 0;

  virtual void enterMethodInvocation3(Java9_v2Parser::MethodInvocation3Context *ctx) = 0;
  virtual void exitMethodInvocation3(Java9_v2Parser::MethodInvocation3Context *ctx) = 0;

  virtual void enterMethodInvocation4(Java9_v2Parser::MethodInvocation4Context *ctx) = 0;
  virtual void exitMethodInvocation4(Java9_v2Parser::MethodInvocation4Context *ctx) = 0;

  virtual void enterMethodInvocation5(Java9_v2Parser::MethodInvocation5Context *ctx) = 0;
  virtual void exitMethodInvocation5(Java9_v2Parser::MethodInvocation5Context *ctx) = 0;

  virtual void enterMethodInvocation6(Java9_v2Parser::MethodInvocation6Context *ctx) = 0;
  virtual void exitMethodInvocation6(Java9_v2Parser::MethodInvocation6Context *ctx) = 0;

  virtual void enterMethodInvocation_lf_primary(Java9_v2Parser::MethodInvocation_lf_primaryContext *ctx) = 0;
  virtual void exitMethodInvocation_lf_primary(Java9_v2Parser::MethodInvocation_lf_primaryContext *ctx) = 0;

  virtual void enterMethodInvocation_lfno_primary1(Java9_v2Parser::MethodInvocation_lfno_primary1Context *ctx) = 0;
  virtual void exitMethodInvocation_lfno_primary1(Java9_v2Parser::MethodInvocation_lfno_primary1Context *ctx) = 0;

  virtual void enterMethodInvocation_lfno_primary2(Java9_v2Parser::MethodInvocation_lfno_primary2Context *ctx) = 0;
  virtual void exitMethodInvocation_lfno_primary2(Java9_v2Parser::MethodInvocation_lfno_primary2Context *ctx) = 0;

  virtual void enterMethodInvocation_lfno_primary3(Java9_v2Parser::MethodInvocation_lfno_primary3Context *ctx) = 0;
  virtual void exitMethodInvocation_lfno_primary3(Java9_v2Parser::MethodInvocation_lfno_primary3Context *ctx) = 0;

  virtual void enterMethodInvocation_lfno_primary4(Java9_v2Parser::MethodInvocation_lfno_primary4Context *ctx) = 0;
  virtual void exitMethodInvocation_lfno_primary4(Java9_v2Parser::MethodInvocation_lfno_primary4Context *ctx) = 0;

  virtual void enterMethodInvocation_lfno_primary5(Java9_v2Parser::MethodInvocation_lfno_primary5Context *ctx) = 0;
  virtual void exitMethodInvocation_lfno_primary5(Java9_v2Parser::MethodInvocation_lfno_primary5Context *ctx) = 0;

  virtual void enterArgumentList(Java9_v2Parser::ArgumentListContext *ctx) = 0;
  virtual void exitArgumentList(Java9_v2Parser::ArgumentListContext *ctx) = 0;

  virtual void enterMethodReference1(Java9_v2Parser::MethodReference1Context *ctx) = 0;
  virtual void exitMethodReference1(Java9_v2Parser::MethodReference1Context *ctx) = 0;

  virtual void enterMethodReference2(Java9_v2Parser::MethodReference2Context *ctx) = 0;
  virtual void exitMethodReference2(Java9_v2Parser::MethodReference2Context *ctx) = 0;

  virtual void enterMethodReference3(Java9_v2Parser::MethodReference3Context *ctx) = 0;
  virtual void exitMethodReference3(Java9_v2Parser::MethodReference3Context *ctx) = 0;

  virtual void enterMethodReference4(Java9_v2Parser::MethodReference4Context *ctx) = 0;
  virtual void exitMethodReference4(Java9_v2Parser::MethodReference4Context *ctx) = 0;

  virtual void enterMethodReference5(Java9_v2Parser::MethodReference5Context *ctx) = 0;
  virtual void exitMethodReference5(Java9_v2Parser::MethodReference5Context *ctx) = 0;

  virtual void enterMethodReference6(Java9_v2Parser::MethodReference6Context *ctx) = 0;
  virtual void exitMethodReference6(Java9_v2Parser::MethodReference6Context *ctx) = 0;

  virtual void enterMethodReference7(Java9_v2Parser::MethodReference7Context *ctx) = 0;
  virtual void exitMethodReference7(Java9_v2Parser::MethodReference7Context *ctx) = 0;

  virtual void enterMethodReference_lf_primary(Java9_v2Parser::MethodReference_lf_primaryContext *ctx) = 0;
  virtual void exitMethodReference_lf_primary(Java9_v2Parser::MethodReference_lf_primaryContext *ctx) = 0;

  virtual void enterMethodReference_lfno_primary1(Java9_v2Parser::MethodReference_lfno_primary1Context *ctx) = 0;
  virtual void exitMethodReference_lfno_primary1(Java9_v2Parser::MethodReference_lfno_primary1Context *ctx) = 0;

  virtual void enterMethodReference_lfno_primary2(Java9_v2Parser::MethodReference_lfno_primary2Context *ctx) = 0;
  virtual void exitMethodReference_lfno_primary2(Java9_v2Parser::MethodReference_lfno_primary2Context *ctx) = 0;

  virtual void enterMethodReference_lfno_primary3(Java9_v2Parser::MethodReference_lfno_primary3Context *ctx) = 0;
  virtual void exitMethodReference_lfno_primary3(Java9_v2Parser::MethodReference_lfno_primary3Context *ctx) = 0;

  virtual void enterMethodReference_lfno_primary4(Java9_v2Parser::MethodReference_lfno_primary4Context *ctx) = 0;
  virtual void exitMethodReference_lfno_primary4(Java9_v2Parser::MethodReference_lfno_primary4Context *ctx) = 0;

  virtual void enterMethodReference_lfno_primary5(Java9_v2Parser::MethodReference_lfno_primary5Context *ctx) = 0;
  virtual void exitMethodReference_lfno_primary5(Java9_v2Parser::MethodReference_lfno_primary5Context *ctx) = 0;

  virtual void enterMethodReference_lfno_primary6(Java9_v2Parser::MethodReference_lfno_primary6Context *ctx) = 0;
  virtual void exitMethodReference_lfno_primary6(Java9_v2Parser::MethodReference_lfno_primary6Context *ctx) = 0;

  virtual void enterArrayCreationExpression1(Java9_v2Parser::ArrayCreationExpression1Context *ctx) = 0;
  virtual void exitArrayCreationExpression1(Java9_v2Parser::ArrayCreationExpression1Context *ctx) = 0;

  virtual void enterArrayCreationExpression2(Java9_v2Parser::ArrayCreationExpression2Context *ctx) = 0;
  virtual void exitArrayCreationExpression2(Java9_v2Parser::ArrayCreationExpression2Context *ctx) = 0;

  virtual void enterArrayCreationExpression3(Java9_v2Parser::ArrayCreationExpression3Context *ctx) = 0;
  virtual void exitArrayCreationExpression3(Java9_v2Parser::ArrayCreationExpression3Context *ctx) = 0;

  virtual void enterArrayCreationExpression4(Java9_v2Parser::ArrayCreationExpression4Context *ctx) = 0;
  virtual void exitArrayCreationExpression4(Java9_v2Parser::ArrayCreationExpression4Context *ctx) = 0;

  virtual void enterDimExprs(Java9_v2Parser::DimExprsContext *ctx) = 0;
  virtual void exitDimExprs(Java9_v2Parser::DimExprsContext *ctx) = 0;

  virtual void enterDimExpr(Java9_v2Parser::DimExprContext *ctx) = 0;
  virtual void exitDimExpr(Java9_v2Parser::DimExprContext *ctx) = 0;

  virtual void enterConstantExpression(Java9_v2Parser::ConstantExpressionContext *ctx) = 0;
  virtual void exitConstantExpression(Java9_v2Parser::ConstantExpressionContext *ctx) = 0;

  virtual void enterExpression1(Java9_v2Parser::Expression1Context *ctx) = 0;
  virtual void exitExpression1(Java9_v2Parser::Expression1Context *ctx) = 0;

  virtual void enterExpression2(Java9_v2Parser::Expression2Context *ctx) = 0;
  virtual void exitExpression2(Java9_v2Parser::Expression2Context *ctx) = 0;

  virtual void enterLambdaExpression(Java9_v2Parser::LambdaExpressionContext *ctx) = 0;
  virtual void exitLambdaExpression(Java9_v2Parser::LambdaExpressionContext *ctx) = 0;

  virtual void enterLambdaParameters1(Java9_v2Parser::LambdaParameters1Context *ctx) = 0;
  virtual void exitLambdaParameters1(Java9_v2Parser::LambdaParameters1Context *ctx) = 0;

  virtual void enterLambdaParameters2(Java9_v2Parser::LambdaParameters2Context *ctx) = 0;
  virtual void exitLambdaParameters2(Java9_v2Parser::LambdaParameters2Context *ctx) = 0;

  virtual void enterLambdaParameters3(Java9_v2Parser::LambdaParameters3Context *ctx) = 0;
  virtual void exitLambdaParameters3(Java9_v2Parser::LambdaParameters3Context *ctx) = 0;

  virtual void enterInferredFormalParameterList(Java9_v2Parser::InferredFormalParameterListContext *ctx) = 0;
  virtual void exitInferredFormalParameterList(Java9_v2Parser::InferredFormalParameterListContext *ctx) = 0;

  virtual void enterLambdaBody1(Java9_v2Parser::LambdaBody1Context *ctx) = 0;
  virtual void exitLambdaBody1(Java9_v2Parser::LambdaBody1Context *ctx) = 0;

  virtual void enterLambdaBody2(Java9_v2Parser::LambdaBody2Context *ctx) = 0;
  virtual void exitLambdaBody2(Java9_v2Parser::LambdaBody2Context *ctx) = 0;

  virtual void enterAssignmentExpression1(Java9_v2Parser::AssignmentExpression1Context *ctx) = 0;
  virtual void exitAssignmentExpression1(Java9_v2Parser::AssignmentExpression1Context *ctx) = 0;

  virtual void enterAssignmentExpression2(Java9_v2Parser::AssignmentExpression2Context *ctx) = 0;
  virtual void exitAssignmentExpression2(Java9_v2Parser::AssignmentExpression2Context *ctx) = 0;

  virtual void enterAssignment(Java9_v2Parser::AssignmentContext *ctx) = 0;
  virtual void exitAssignment(Java9_v2Parser::AssignmentContext *ctx) = 0;

  virtual void enterLeftHandSide3(Java9_v2Parser::LeftHandSide3Context *ctx) = 0;
  virtual void exitLeftHandSide3(Java9_v2Parser::LeftHandSide3Context *ctx) = 0;

  virtual void enterLeftHandSide4(Java9_v2Parser::LeftHandSide4Context *ctx) = 0;
  virtual void exitLeftHandSide4(Java9_v2Parser::LeftHandSide4Context *ctx) = 0;

  virtual void enterLeftHandSide5(Java9_v2Parser::LeftHandSide5Context *ctx) = 0;
  virtual void exitLeftHandSide5(Java9_v2Parser::LeftHandSide5Context *ctx) = 0;

  virtual void enterAssignmentOperator(Java9_v2Parser::AssignmentOperatorContext *ctx) = 0;
  virtual void exitAssignmentOperator(Java9_v2Parser::AssignmentOperatorContext *ctx) = 0;

  virtual void enterConditionalExpression1(Java9_v2Parser::ConditionalExpression1Context *ctx) = 0;
  virtual void exitConditionalExpression1(Java9_v2Parser::ConditionalExpression1Context *ctx) = 0;

  virtual void enterConditionalExpression2(Java9_v2Parser::ConditionalExpression2Context *ctx) = 0;
  virtual void exitConditionalExpression2(Java9_v2Parser::ConditionalExpression2Context *ctx) = 0;

  virtual void enterConditionalOrExpression1(Java9_v2Parser::ConditionalOrExpression1Context *ctx) = 0;
  virtual void exitConditionalOrExpression1(Java9_v2Parser::ConditionalOrExpression1Context *ctx) = 0;

  virtual void enterConditionalOrExpression2(Java9_v2Parser::ConditionalOrExpression2Context *ctx) = 0;
  virtual void exitConditionalOrExpression2(Java9_v2Parser::ConditionalOrExpression2Context *ctx) = 0;

  virtual void enterConditionalAndExpression2(Java9_v2Parser::ConditionalAndExpression2Context *ctx) = 0;
  virtual void exitConditionalAndExpression2(Java9_v2Parser::ConditionalAndExpression2Context *ctx) = 0;

  virtual void enterConditionalAndExpression1(Java9_v2Parser::ConditionalAndExpression1Context *ctx) = 0;
  virtual void exitConditionalAndExpression1(Java9_v2Parser::ConditionalAndExpression1Context *ctx) = 0;

  virtual void enterInclusiveOrExpression2(Java9_v2Parser::InclusiveOrExpression2Context *ctx) = 0;
  virtual void exitInclusiveOrExpression2(Java9_v2Parser::InclusiveOrExpression2Context *ctx) = 0;

  virtual void enterInclusiveOrExpression1(Java9_v2Parser::InclusiveOrExpression1Context *ctx) = 0;
  virtual void exitInclusiveOrExpression1(Java9_v2Parser::InclusiveOrExpression1Context *ctx) = 0;

  virtual void enterExclusiveOrExpression1(Java9_v2Parser::ExclusiveOrExpression1Context *ctx) = 0;
  virtual void exitExclusiveOrExpression1(Java9_v2Parser::ExclusiveOrExpression1Context *ctx) = 0;

  virtual void enterExclusiveOrExpression2(Java9_v2Parser::ExclusiveOrExpression2Context *ctx) = 0;
  virtual void exitExclusiveOrExpression2(Java9_v2Parser::ExclusiveOrExpression2Context *ctx) = 0;

  virtual void enterAndExpression2(Java9_v2Parser::AndExpression2Context *ctx) = 0;
  virtual void exitAndExpression2(Java9_v2Parser::AndExpression2Context *ctx) = 0;

  virtual void enterAndExpression1(Java9_v2Parser::AndExpression1Context *ctx) = 0;
  virtual void exitAndExpression1(Java9_v2Parser::AndExpression1Context *ctx) = 0;

  virtual void enterEqualityExpression3(Java9_v2Parser::EqualityExpression3Context *ctx) = 0;
  virtual void exitEqualityExpression3(Java9_v2Parser::EqualityExpression3Context *ctx) = 0;

  virtual void enterEqualityExpression2(Java9_v2Parser::EqualityExpression2Context *ctx) = 0;
  virtual void exitEqualityExpression2(Java9_v2Parser::EqualityExpression2Context *ctx) = 0;

  virtual void enterEqualityExpression1(Java9_v2Parser::EqualityExpression1Context *ctx) = 0;
  virtual void exitEqualityExpression1(Java9_v2Parser::EqualityExpression1Context *ctx) = 0;

  virtual void enterRelationalExpression1(Java9_v2Parser::RelationalExpression1Context *ctx) = 0;
  virtual void exitRelationalExpression1(Java9_v2Parser::RelationalExpression1Context *ctx) = 0;

  virtual void enterRelationalExpression2(Java9_v2Parser::RelationalExpression2Context *ctx) = 0;
  virtual void exitRelationalExpression2(Java9_v2Parser::RelationalExpression2Context *ctx) = 0;

  virtual void enterRelationalExpression5(Java9_v2Parser::RelationalExpression5Context *ctx) = 0;
  virtual void exitRelationalExpression5(Java9_v2Parser::RelationalExpression5Context *ctx) = 0;

  virtual void enterRelationalExpression6(Java9_v2Parser::RelationalExpression6Context *ctx) = 0;
  virtual void exitRelationalExpression6(Java9_v2Parser::RelationalExpression6Context *ctx) = 0;

  virtual void enterRelationalExpression3(Java9_v2Parser::RelationalExpression3Context *ctx) = 0;
  virtual void exitRelationalExpression3(Java9_v2Parser::RelationalExpression3Context *ctx) = 0;

  virtual void enterRelationalExpression4(Java9_v2Parser::RelationalExpression4Context *ctx) = 0;
  virtual void exitRelationalExpression4(Java9_v2Parser::RelationalExpression4Context *ctx) = 0;

  virtual void enterShiftExpression1(Java9_v2Parser::ShiftExpression1Context *ctx) = 0;
  virtual void exitShiftExpression1(Java9_v2Parser::ShiftExpression1Context *ctx) = 0;

  virtual void enterShiftExpression3(Java9_v2Parser::ShiftExpression3Context *ctx) = 0;
  virtual void exitShiftExpression3(Java9_v2Parser::ShiftExpression3Context *ctx) = 0;

  virtual void enterShiftExpression2(Java9_v2Parser::ShiftExpression2Context *ctx) = 0;
  virtual void exitShiftExpression2(Java9_v2Parser::ShiftExpression2Context *ctx) = 0;

  virtual void enterShiftExpression4(Java9_v2Parser::ShiftExpression4Context *ctx) = 0;
  virtual void exitShiftExpression4(Java9_v2Parser::ShiftExpression4Context *ctx) = 0;

  virtual void enterAdditiveExpression1(Java9_v2Parser::AdditiveExpression1Context *ctx) = 0;
  virtual void exitAdditiveExpression1(Java9_v2Parser::AdditiveExpression1Context *ctx) = 0;

  virtual void enterAdditiveExpression3(Java9_v2Parser::AdditiveExpression3Context *ctx) = 0;
  virtual void exitAdditiveExpression3(Java9_v2Parser::AdditiveExpression3Context *ctx) = 0;

  virtual void enterAdditiveExpressio2(Java9_v2Parser::AdditiveExpressio2Context *ctx) = 0;
  virtual void exitAdditiveExpressio2(Java9_v2Parser::AdditiveExpressio2Context *ctx) = 0;

  virtual void enterMultiplicativeExpression1(Java9_v2Parser::MultiplicativeExpression1Context *ctx) = 0;
  virtual void exitMultiplicativeExpression1(Java9_v2Parser::MultiplicativeExpression1Context *ctx) = 0;

  virtual void enterMultiplicativeExpression4(Java9_v2Parser::MultiplicativeExpression4Context *ctx) = 0;
  virtual void exitMultiplicativeExpression4(Java9_v2Parser::MultiplicativeExpression4Context *ctx) = 0;

  virtual void enterMultiplicativeExpression3(Java9_v2Parser::MultiplicativeExpression3Context *ctx) = 0;
  virtual void exitMultiplicativeExpression3(Java9_v2Parser::MultiplicativeExpression3Context *ctx) = 0;

  virtual void enterMultiplicativeExpression2(Java9_v2Parser::MultiplicativeExpression2Context *ctx) = 0;
  virtual void exitMultiplicativeExpression2(Java9_v2Parser::MultiplicativeExpression2Context *ctx) = 0;

  virtual void enterUnaryExpression1(Java9_v2Parser::UnaryExpression1Context *ctx) = 0;
  virtual void exitUnaryExpression1(Java9_v2Parser::UnaryExpression1Context *ctx) = 0;

  virtual void enterUnaryExpression2(Java9_v2Parser::UnaryExpression2Context *ctx) = 0;
  virtual void exitUnaryExpression2(Java9_v2Parser::UnaryExpression2Context *ctx) = 0;

  virtual void enterUnaryExpression3(Java9_v2Parser::UnaryExpression3Context *ctx) = 0;
  virtual void exitUnaryExpression3(Java9_v2Parser::UnaryExpression3Context *ctx) = 0;

  virtual void enterUnaryExpression4(Java9_v2Parser::UnaryExpression4Context *ctx) = 0;
  virtual void exitUnaryExpression4(Java9_v2Parser::UnaryExpression4Context *ctx) = 0;

  virtual void enterUnaryExpression5(Java9_v2Parser::UnaryExpression5Context *ctx) = 0;
  virtual void exitUnaryExpression5(Java9_v2Parser::UnaryExpression5Context *ctx) = 0;

  virtual void enterPreIncrementExpression(Java9_v2Parser::PreIncrementExpressionContext *ctx) = 0;
  virtual void exitPreIncrementExpression(Java9_v2Parser::PreIncrementExpressionContext *ctx) = 0;

  virtual void enterPreDecrementExpression(Java9_v2Parser::PreDecrementExpressionContext *ctx) = 0;
  virtual void exitPreDecrementExpression(Java9_v2Parser::PreDecrementExpressionContext *ctx) = 0;

  virtual void enterUnaryExpressionNotPlusMinus1(Java9_v2Parser::UnaryExpressionNotPlusMinus1Context *ctx) = 0;
  virtual void exitUnaryExpressionNotPlusMinus1(Java9_v2Parser::UnaryExpressionNotPlusMinus1Context *ctx) = 0;

  virtual void enterUnaryExpressionNotPlusMinus2(Java9_v2Parser::UnaryExpressionNotPlusMinus2Context *ctx) = 0;
  virtual void exitUnaryExpressionNotPlusMinus2(Java9_v2Parser::UnaryExpressionNotPlusMinus2Context *ctx) = 0;

  virtual void enterUnaryExpressionNotPlusMinus3(Java9_v2Parser::UnaryExpressionNotPlusMinus3Context *ctx) = 0;
  virtual void exitUnaryExpressionNotPlusMinus3(Java9_v2Parser::UnaryExpressionNotPlusMinus3Context *ctx) = 0;

  virtual void enterUnaryExpressionNotPlusMinus4(Java9_v2Parser::UnaryExpressionNotPlusMinus4Context *ctx) = 0;
  virtual void exitUnaryExpressionNotPlusMinus4(Java9_v2Parser::UnaryExpressionNotPlusMinus4Context *ctx) = 0;

  virtual void enterPostfixExpression(Java9_v2Parser::PostfixExpressionContext *ctx) = 0;
  virtual void exitPostfixExpression(Java9_v2Parser::PostfixExpressionContext *ctx) = 0;

  virtual void enterPostIncrementExpression(Java9_v2Parser::PostIncrementExpressionContext *ctx) = 0;
  virtual void exitPostIncrementExpression(Java9_v2Parser::PostIncrementExpressionContext *ctx) = 0;

  virtual void enterPostIncrementExpression_lf_postfixExpression(Java9_v2Parser::PostIncrementExpression_lf_postfixExpressionContext *ctx) = 0;
  virtual void exitPostIncrementExpression_lf_postfixExpression(Java9_v2Parser::PostIncrementExpression_lf_postfixExpressionContext *ctx) = 0;

  virtual void enterPostDecrementExpression(Java9_v2Parser::PostDecrementExpressionContext *ctx) = 0;
  virtual void exitPostDecrementExpression(Java9_v2Parser::PostDecrementExpressionContext *ctx) = 0;

  virtual void enterPostDecrementExpression_lf_postfixExpression(Java9_v2Parser::PostDecrementExpression_lf_postfixExpressionContext *ctx) = 0;
  virtual void exitPostDecrementExpression_lf_postfixExpression(Java9_v2Parser::PostDecrementExpression_lf_postfixExpressionContext *ctx) = 0;

  virtual void enterCastExpression1(Java9_v2Parser::CastExpression1Context *ctx) = 0;
  virtual void exitCastExpression1(Java9_v2Parser::CastExpression1Context *ctx) = 0;

  virtual void enterCastExpression2(Java9_v2Parser::CastExpression2Context *ctx) = 0;
  virtual void exitCastExpression2(Java9_v2Parser::CastExpression2Context *ctx) = 0;

  virtual void enterCastExpression3(Java9_v2Parser::CastExpression3Context *ctx) = 0;
  virtual void exitCastExpression3(Java9_v2Parser::CastExpression3Context *ctx) = 0;

  virtual void enterIdentifier(Java9_v2Parser::IdentifierContext *ctx) = 0;
  virtual void exitIdentifier(Java9_v2Parser::IdentifierContext *ctx) = 0;


};

