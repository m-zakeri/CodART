
// Generated from D:/AnacondaProjects/CodART/grammars\Java9_v2.g4 by ANTLR 4.9

#pragma once


#include "antlr4-runtime.h"
#include "Java9_v2Parser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by Java9_v2Parser.
 */
class  Java9_v2Visitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by Java9_v2Parser.
   */
    virtual antlrcpp::Any visitLiteral(Java9_v2Parser::LiteralContext *context) = 0;

    virtual antlrcpp::Any visitPrimitiveType1(Java9_v2Parser::PrimitiveType1Context *context) = 0;

    virtual antlrcpp::Any visitPrimitiveType2(Java9_v2Parser::PrimitiveType2Context *context) = 0;

    virtual antlrcpp::Any visitNumericType1(Java9_v2Parser::NumericType1Context *context) = 0;

    virtual antlrcpp::Any visitNumericType2(Java9_v2Parser::NumericType2Context *context) = 0;

    virtual antlrcpp::Any visitIntegralType(Java9_v2Parser::IntegralTypeContext *context) = 0;

    virtual antlrcpp::Any visitFloatingPointType(Java9_v2Parser::FloatingPointTypeContext *context) = 0;

    virtual antlrcpp::Any visitReferenceType1(Java9_v2Parser::ReferenceType1Context *context) = 0;

    virtual antlrcpp::Any visitReferenceType2(Java9_v2Parser::ReferenceType2Context *context) = 0;

    virtual antlrcpp::Any visitReferenceType3(Java9_v2Parser::ReferenceType3Context *context) = 0;

    virtual antlrcpp::Any visitClassOrInterfaceType(Java9_v2Parser::ClassOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitClassType1(Java9_v2Parser::ClassType1Context *context) = 0;

    virtual antlrcpp::Any visitClassType2(Java9_v2Parser::ClassType2Context *context) = 0;

    virtual antlrcpp::Any visitClassType_lf_classOrInterfaceType(Java9_v2Parser::ClassType_lf_classOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitClassType_lfno_classOrInterfaceType(Java9_v2Parser::ClassType_lfno_classOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceType(Java9_v2Parser::InterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceType_lf_classOrInterfaceType(Java9_v2Parser::InterfaceType_lf_classOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceType_lfno_classOrInterfaceType(Java9_v2Parser::InterfaceType_lfno_classOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitTypeVariable(Java9_v2Parser::TypeVariableContext *context) = 0;

    virtual antlrcpp::Any visitArrayType1(Java9_v2Parser::ArrayType1Context *context) = 0;

    virtual antlrcpp::Any visitArrayType2(Java9_v2Parser::ArrayType2Context *context) = 0;

    virtual antlrcpp::Any visitArrayTyp3(Java9_v2Parser::ArrayTyp3Context *context) = 0;

    virtual antlrcpp::Any visitDims(Java9_v2Parser::DimsContext *context) = 0;

    virtual antlrcpp::Any visitTypeParameter(Java9_v2Parser::TypeParameterContext *context) = 0;

    virtual antlrcpp::Any visitTypeParameterModifier(Java9_v2Parser::TypeParameterModifierContext *context) = 0;

    virtual antlrcpp::Any visitTypeBound1(Java9_v2Parser::TypeBound1Context *context) = 0;

    virtual antlrcpp::Any visitTypeBound2(Java9_v2Parser::TypeBound2Context *context) = 0;

    virtual antlrcpp::Any visitAdditionalBound(Java9_v2Parser::AdditionalBoundContext *context) = 0;

    virtual antlrcpp::Any visitTypeArguments(Java9_v2Parser::TypeArgumentsContext *context) = 0;

    virtual antlrcpp::Any visitTypeArgumentList(Java9_v2Parser::TypeArgumentListContext *context) = 0;

    virtual antlrcpp::Any visitTypeArgument1(Java9_v2Parser::TypeArgument1Context *context) = 0;

    virtual antlrcpp::Any visitTypeArgument2(Java9_v2Parser::TypeArgument2Context *context) = 0;

    virtual antlrcpp::Any visitWildcard(Java9_v2Parser::WildcardContext *context) = 0;

    virtual antlrcpp::Any visitWildcardBounds1(Java9_v2Parser::WildcardBounds1Context *context) = 0;

    virtual antlrcpp::Any visitWildcardBound2(Java9_v2Parser::WildcardBound2Context *context) = 0;

    virtual antlrcpp::Any visitModuleName1(Java9_v2Parser::ModuleName1Context *context) = 0;

    virtual antlrcpp::Any visitModuleName2(Java9_v2Parser::ModuleName2Context *context) = 0;

    virtual antlrcpp::Any visitPackageName2(Java9_v2Parser::PackageName2Context *context) = 0;

    virtual antlrcpp::Any visitPackageName1(Java9_v2Parser::PackageName1Context *context) = 0;

    virtual antlrcpp::Any visitTypeName1(Java9_v2Parser::TypeName1Context *context) = 0;

    virtual antlrcpp::Any visitTypeName2(Java9_v2Parser::TypeName2Context *context) = 0;

    virtual antlrcpp::Any visitPackageOrTypeName1(Java9_v2Parser::PackageOrTypeName1Context *context) = 0;

    virtual antlrcpp::Any visitPackageOrTypeName2(Java9_v2Parser::PackageOrTypeName2Context *context) = 0;

    virtual antlrcpp::Any visitExpressionName1(Java9_v2Parser::ExpressionName1Context *context) = 0;

    virtual antlrcpp::Any visitExpressionName2(Java9_v2Parser::ExpressionName2Context *context) = 0;

    virtual antlrcpp::Any visitMethodName(Java9_v2Parser::MethodNameContext *context) = 0;

    virtual antlrcpp::Any visitAmbiguousName1(Java9_v2Parser::AmbiguousName1Context *context) = 0;

    virtual antlrcpp::Any visitAmbiguousName2(Java9_v2Parser::AmbiguousName2Context *context) = 0;

    virtual antlrcpp::Any visitCompilationUnit1(Java9_v2Parser::CompilationUnit1Context *context) = 0;

    virtual antlrcpp::Any visitCompilationUnit2(Java9_v2Parser::CompilationUnit2Context *context) = 0;

    virtual antlrcpp::Any visitOrdinaryCompilation(Java9_v2Parser::OrdinaryCompilationContext *context) = 0;

    virtual antlrcpp::Any visitModularCompilation(Java9_v2Parser::ModularCompilationContext *context) = 0;

    virtual antlrcpp::Any visitPackageDeclaration(Java9_v2Parser::PackageDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitPackageModifier(Java9_v2Parser::PackageModifierContext *context) = 0;

    virtual antlrcpp::Any visitImportDeclaration1(Java9_v2Parser::ImportDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitImportDeclaration2(Java9_v2Parser::ImportDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitImportDeclaration3(Java9_v2Parser::ImportDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitImportDeclaration4(Java9_v2Parser::ImportDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitSingleTypeImportDeclaration(Java9_v2Parser::SingleTypeImportDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitTypeImportOnDemandDeclaration(Java9_v2Parser::TypeImportOnDemandDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitSingleStaticImportDeclaration(Java9_v2Parser::SingleStaticImportDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitStaticImportOnDemandDeclaration(Java9_v2Parser::StaticImportOnDemandDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitTypeDeclaration1(Java9_v2Parser::TypeDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitTypeDeclaration2(Java9_v2Parser::TypeDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitTypeDeclaration3(Java9_v2Parser::TypeDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitModuleDeclaration(Java9_v2Parser::ModuleDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitModuleDirective1(Java9_v2Parser::ModuleDirective1Context *context) = 0;

    virtual antlrcpp::Any visitModuleDirective2(Java9_v2Parser::ModuleDirective2Context *context) = 0;

    virtual antlrcpp::Any visitModuleDirectiv3(Java9_v2Parser::ModuleDirectiv3Context *context) = 0;

    virtual antlrcpp::Any visitModuleDirective4(Java9_v2Parser::ModuleDirective4Context *context) = 0;

    virtual antlrcpp::Any visitModuleDirective5(Java9_v2Parser::ModuleDirective5Context *context) = 0;

    virtual antlrcpp::Any visitRequiresModifier(Java9_v2Parser::RequiresModifierContext *context) = 0;

    virtual antlrcpp::Any visitClassDeclaration1(Java9_v2Parser::ClassDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitClassDeclaration2(Java9_v2Parser::ClassDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitNormalClassDeclaration(Java9_v2Parser::NormalClassDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitClassModifier(Java9_v2Parser::ClassModifierContext *context) = 0;

    virtual antlrcpp::Any visitTypeParameters(Java9_v2Parser::TypeParametersContext *context) = 0;

    virtual antlrcpp::Any visitTypeParameterList(Java9_v2Parser::TypeParameterListContext *context) = 0;

    virtual antlrcpp::Any visitSuperclass(Java9_v2Parser::SuperclassContext *context) = 0;

    virtual antlrcpp::Any visitSuperinterfaces(Java9_v2Parser::SuperinterfacesContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceTypeList(Java9_v2Parser::InterfaceTypeListContext *context) = 0;

    virtual antlrcpp::Any visitClassBody(Java9_v2Parser::ClassBodyContext *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration1(Java9_v2Parser::ClassBodyDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration2(Java9_v2Parser::ClassBodyDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration3(Java9_v2Parser::ClassBodyDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration4(Java9_v2Parser::ClassBodyDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitClassMemberDeclaration1(Java9_v2Parser::ClassMemberDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitClassMemberDeclaration2(Java9_v2Parser::ClassMemberDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitClassMemberDeclaration3(Java9_v2Parser::ClassMemberDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitClassMemberDeclaration4(Java9_v2Parser::ClassMemberDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitClassMemberDeclaration5(Java9_v2Parser::ClassMemberDeclaration5Context *context) = 0;

    virtual antlrcpp::Any visitFieldDeclaration(Java9_v2Parser::FieldDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitFieldModifier(Java9_v2Parser::FieldModifierContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclaratorList(Java9_v2Parser::VariableDeclaratorListContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclarator(Java9_v2Parser::VariableDeclaratorContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclaratorId(Java9_v2Parser::VariableDeclaratorIdContext *context) = 0;

    virtual antlrcpp::Any visitVariableInitializer1(Java9_v2Parser::VariableInitializer1Context *context) = 0;

    virtual antlrcpp::Any visitVariableInitializer2(Java9_v2Parser::VariableInitializer2Context *context) = 0;

    virtual antlrcpp::Any visitUnannType1(Java9_v2Parser::UnannType1Context *context) = 0;

    virtual antlrcpp::Any visitUnannType2(Java9_v2Parser::UnannType2Context *context) = 0;

    virtual antlrcpp::Any visitUnannPrimitiveType1(Java9_v2Parser::UnannPrimitiveType1Context *context) = 0;

    virtual antlrcpp::Any visitUnannPrimitiveType2(Java9_v2Parser::UnannPrimitiveType2Context *context) = 0;

    virtual antlrcpp::Any visitUnannReferenceType1(Java9_v2Parser::UnannReferenceType1Context *context) = 0;

    virtual antlrcpp::Any visitUnannReferenceType2(Java9_v2Parser::UnannReferenceType2Context *context) = 0;

    virtual antlrcpp::Any visitUnannReferenceType3(Java9_v2Parser::UnannReferenceType3Context *context) = 0;

    virtual antlrcpp::Any visitUnannClassOrInterfaceType(Java9_v2Parser::UnannClassOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitUnannClassType1(Java9_v2Parser::UnannClassType1Context *context) = 0;

    virtual antlrcpp::Any visitUnannClassType2(Java9_v2Parser::UnannClassType2Context *context) = 0;

    virtual antlrcpp::Any visitUnannClassType_lf_unannClassOrInterfaceType(Java9_v2Parser::UnannClassType_lf_unannClassOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitUnannClassType_lfno_unannClassOrInterfaceType(Java9_v2Parser::UnannClassType_lfno_unannClassOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitUnannInterfaceType(Java9_v2Parser::UnannInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitUnannInterfaceType_lf_unannClassOrInterfaceType(Java9_v2Parser::UnannInterfaceType_lf_unannClassOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitUnannInterfaceType_lfno_unannClassOrInterfaceType(Java9_v2Parser::UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitUnannTypeVariable(Java9_v2Parser::UnannTypeVariableContext *context) = 0;

    virtual antlrcpp::Any visitUnannArrayType1(Java9_v2Parser::UnannArrayType1Context *context) = 0;

    virtual antlrcpp::Any visitUnannArrayType2(Java9_v2Parser::UnannArrayType2Context *context) = 0;

    virtual antlrcpp::Any visitUnannArrayTyp3(Java9_v2Parser::UnannArrayTyp3Context *context) = 0;

    virtual antlrcpp::Any visitMethodDeclaration(Java9_v2Parser::MethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitMethodModifier(Java9_v2Parser::MethodModifierContext *context) = 0;

    virtual antlrcpp::Any visitMethodHeader(Java9_v2Parser::MethodHeaderContext *context) = 0;

    virtual antlrcpp::Any visitResult(Java9_v2Parser::ResultContext *context) = 0;

    virtual antlrcpp::Any visitMethodDeclarator(Java9_v2Parser::MethodDeclaratorContext *context) = 0;

    virtual antlrcpp::Any visitFormalParameterList1(Java9_v2Parser::FormalParameterList1Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameterList2(Java9_v2Parser::FormalParameterList2Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameterList3(Java9_v2Parser::FormalParameterList3Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameters1(Java9_v2Parser::FormalParameters1Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameters2(Java9_v2Parser::FormalParameters2Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameter(Java9_v2Parser::FormalParameterContext *context) = 0;

    virtual antlrcpp::Any visitVariableModifier(Java9_v2Parser::VariableModifierContext *context) = 0;

    virtual antlrcpp::Any visitLastFormalParameter1(Java9_v2Parser::LastFormalParameter1Context *context) = 0;

    virtual antlrcpp::Any visitLastFormalParameter2(Java9_v2Parser::LastFormalParameter2Context *context) = 0;

    virtual antlrcpp::Any visitReceiverParameter(Java9_v2Parser::ReceiverParameterContext *context) = 0;

    virtual antlrcpp::Any visitThrows_(Java9_v2Parser::Throws_Context *context) = 0;

    virtual antlrcpp::Any visitExceptionTypeList(Java9_v2Parser::ExceptionTypeListContext *context) = 0;

    virtual antlrcpp::Any visitExceptionType1(Java9_v2Parser::ExceptionType1Context *context) = 0;

    virtual antlrcpp::Any visitExceptionType2(Java9_v2Parser::ExceptionType2Context *context) = 0;

    virtual antlrcpp::Any visitMethodBody(Java9_v2Parser::MethodBodyContext *context) = 0;

    virtual antlrcpp::Any visitInstanceInitializer(Java9_v2Parser::InstanceInitializerContext *context) = 0;

    virtual antlrcpp::Any visitStaticInitializer(Java9_v2Parser::StaticInitializerContext *context) = 0;

    virtual antlrcpp::Any visitConstructorDeclaration(Java9_v2Parser::ConstructorDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitConstructorModifier(Java9_v2Parser::ConstructorModifierContext *context) = 0;

    virtual antlrcpp::Any visitConstructorDeclarator(Java9_v2Parser::ConstructorDeclaratorContext *context) = 0;

    virtual antlrcpp::Any visitSimpleTypeName(Java9_v2Parser::SimpleTypeNameContext *context) = 0;

    virtual antlrcpp::Any visitConstructorBody(Java9_v2Parser::ConstructorBodyContext *context) = 0;

    virtual antlrcpp::Any visitExplicitConstructorInvocation1(Java9_v2Parser::ExplicitConstructorInvocation1Context *context) = 0;

    virtual antlrcpp::Any visitExplicitConstructorInvocation2(Java9_v2Parser::ExplicitConstructorInvocation2Context *context) = 0;

    virtual antlrcpp::Any visitExplicitConstructorInvocation3(Java9_v2Parser::ExplicitConstructorInvocation3Context *context) = 0;

    virtual antlrcpp::Any visitExplicitConstructorInvocation4(Java9_v2Parser::ExplicitConstructorInvocation4Context *context) = 0;

    virtual antlrcpp::Any visitEnumDeclaration(Java9_v2Parser::EnumDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitEnumBody(Java9_v2Parser::EnumBodyContext *context) = 0;

    virtual antlrcpp::Any visitEnumConstantList(Java9_v2Parser::EnumConstantListContext *context) = 0;

    virtual antlrcpp::Any visitEnumConstant(Java9_v2Parser::EnumConstantContext *context) = 0;

    virtual antlrcpp::Any visitEnumConstantModifier(Java9_v2Parser::EnumConstantModifierContext *context) = 0;

    virtual antlrcpp::Any visitEnumBodyDeclarations(Java9_v2Parser::EnumBodyDeclarationsContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceDeclaration1(Java9_v2Parser::InterfaceDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceDeclaration2(Java9_v2Parser::InterfaceDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitNormalInterfaceDeclaration(Java9_v2Parser::NormalInterfaceDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceModifier(Java9_v2Parser::InterfaceModifierContext *context) = 0;

    virtual antlrcpp::Any visitExtendsInterfaces(Java9_v2Parser::ExtendsInterfacesContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceBody(Java9_v2Parser::InterfaceBodyContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration1(Java9_v2Parser::InterfaceMemberDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration2(Java9_v2Parser::InterfaceMemberDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration3(Java9_v2Parser::InterfaceMemberDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration4(Java9_v2Parser::InterfaceMemberDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration5(Java9_v2Parser::InterfaceMemberDeclaration5Context *context) = 0;

    virtual antlrcpp::Any visitConstantDeclaration(Java9_v2Parser::ConstantDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitConstantModifier(Java9_v2Parser::ConstantModifierContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMethodDeclaration(Java9_v2Parser::InterfaceMethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMethodModifier(Java9_v2Parser::InterfaceMethodModifierContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeDeclaration(Java9_v2Parser::AnnotationTypeDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeBody(Java9_v2Parser::AnnotationTypeBodyContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeMemberDeclaration1(Java9_v2Parser::AnnotationTypeMemberDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeMemberDeclaration2(Java9_v2Parser::AnnotationTypeMemberDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeMemberDeclaration3(Java9_v2Parser::AnnotationTypeMemberDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeMemberDeclaration4(Java9_v2Parser::AnnotationTypeMemberDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeMemberDeclaration5(Java9_v2Parser::AnnotationTypeMemberDeclaration5Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementDeclaration(Java9_v2Parser::AnnotationTypeElementDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementModifier(Java9_v2Parser::AnnotationTypeElementModifierContext *context) = 0;

    virtual antlrcpp::Any visitDefaultValue(Java9_v2Parser::DefaultValueContext *context) = 0;

    virtual antlrcpp::Any visitAnnotation1(Java9_v2Parser::Annotation1Context *context) = 0;

    virtual antlrcpp::Any visitAnnotation2(Java9_v2Parser::Annotation2Context *context) = 0;

    virtual antlrcpp::Any visitAnnotation3(Java9_v2Parser::Annotation3Context *context) = 0;

    virtual antlrcpp::Any visitNormalAnnotation(Java9_v2Parser::NormalAnnotationContext *context) = 0;

    virtual antlrcpp::Any visitElementValuePairList(Java9_v2Parser::ElementValuePairListContext *context) = 0;

    virtual antlrcpp::Any visitElementValuePair(Java9_v2Parser::ElementValuePairContext *context) = 0;

    virtual antlrcpp::Any visitElementValue1(Java9_v2Parser::ElementValue1Context *context) = 0;

    virtual antlrcpp::Any visitElementValue2(Java9_v2Parser::ElementValue2Context *context) = 0;

    virtual antlrcpp::Any visitElementValu3(Java9_v2Parser::ElementValu3Context *context) = 0;

    virtual antlrcpp::Any visitElementValueArrayInitializer(Java9_v2Parser::ElementValueArrayInitializerContext *context) = 0;

    virtual antlrcpp::Any visitElementValueList(Java9_v2Parser::ElementValueListContext *context) = 0;

    virtual antlrcpp::Any visitMarkerAnnotation(Java9_v2Parser::MarkerAnnotationContext *context) = 0;

    virtual antlrcpp::Any visitSingleElementAnnotation(Java9_v2Parser::SingleElementAnnotationContext *context) = 0;

    virtual antlrcpp::Any visitArrayInitializer(Java9_v2Parser::ArrayInitializerContext *context) = 0;

    virtual antlrcpp::Any visitVariableInitializerList(Java9_v2Parser::VariableInitializerListContext *context) = 0;

    virtual antlrcpp::Any visitBlock(Java9_v2Parser::BlockContext *context) = 0;

    virtual antlrcpp::Any visitBlockStatements(Java9_v2Parser::BlockStatementsContext *context) = 0;

    virtual antlrcpp::Any visitBlockStatement1(Java9_v2Parser::BlockStatement1Context *context) = 0;

    virtual antlrcpp::Any visitBlockStatement2(Java9_v2Parser::BlockStatement2Context *context) = 0;

    virtual antlrcpp::Any visitBlockStatement3(Java9_v2Parser::BlockStatement3Context *context) = 0;

    virtual antlrcpp::Any visitLocalVariableDeclarationStatement(Java9_v2Parser::LocalVariableDeclarationStatementContext *context) = 0;

    virtual antlrcpp::Any visitLocalVariableDeclaration(Java9_v2Parser::LocalVariableDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitStatement1(Java9_v2Parser::Statement1Context *context) = 0;

    virtual antlrcpp::Any visitStatement2(Java9_v2Parser::Statement2Context *context) = 0;

    virtual antlrcpp::Any visitStatement3(Java9_v2Parser::Statement3Context *context) = 0;

    virtual antlrcpp::Any visitStatement4(Java9_v2Parser::Statement4Context *context) = 0;

    virtual antlrcpp::Any visitStatement5(Java9_v2Parser::Statement5Context *context) = 0;

    virtual antlrcpp::Any visitStatement6(Java9_v2Parser::Statement6Context *context) = 0;

    virtual antlrcpp::Any visitStatementNoShortIf1(Java9_v2Parser::StatementNoShortIf1Context *context) = 0;

    virtual antlrcpp::Any visitStatementNoShortIf2(Java9_v2Parser::StatementNoShortIf2Context *context) = 0;

    virtual antlrcpp::Any visitStatementNoShortIf3(Java9_v2Parser::StatementNoShortIf3Context *context) = 0;

    virtual antlrcpp::Any visitStatementNoShortIf4(Java9_v2Parser::StatementNoShortIf4Context *context) = 0;

    virtual antlrcpp::Any visitStatementNoShortIf5(Java9_v2Parser::StatementNoShortIf5Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement1(Java9_v2Parser::StatementWithoutTrailingSubstatement1Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement2(Java9_v2Parser::StatementWithoutTrailingSubstatement2Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement3(Java9_v2Parser::StatementWithoutTrailingSubstatement3Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement4(Java9_v2Parser::StatementWithoutTrailingSubstatement4Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement5(Java9_v2Parser::StatementWithoutTrailingSubstatement5Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement6(Java9_v2Parser::StatementWithoutTrailingSubstatement6Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement7(Java9_v2Parser::StatementWithoutTrailingSubstatement7Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement8(Java9_v2Parser::StatementWithoutTrailingSubstatement8Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement9(Java9_v2Parser::StatementWithoutTrailingSubstatement9Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement10(Java9_v2Parser::StatementWithoutTrailingSubstatement10Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement11(Java9_v2Parser::StatementWithoutTrailingSubstatement11Context *context) = 0;

    virtual antlrcpp::Any visitStatementWithoutTrailingSubstatement12(Java9_v2Parser::StatementWithoutTrailingSubstatement12Context *context) = 0;

    virtual antlrcpp::Any visitEmptyStatement(Java9_v2Parser::EmptyStatementContext *context) = 0;

    virtual antlrcpp::Any visitLabeledStatement(Java9_v2Parser::LabeledStatementContext *context) = 0;

    virtual antlrcpp::Any visitLabeledStatementNoShortIf(Java9_v2Parser::LabeledStatementNoShortIfContext *context) = 0;

    virtual antlrcpp::Any visitExpressionStatement(Java9_v2Parser::ExpressionStatementContext *context) = 0;

    virtual antlrcpp::Any visitStatementExpression1(Java9_v2Parser::StatementExpression1Context *context) = 0;

    virtual antlrcpp::Any visitStatementExpression2(Java9_v2Parser::StatementExpression2Context *context) = 0;

    virtual antlrcpp::Any visitStatementExpression3(Java9_v2Parser::StatementExpression3Context *context) = 0;

    virtual antlrcpp::Any visitStatementExpression4(Java9_v2Parser::StatementExpression4Context *context) = 0;

    virtual antlrcpp::Any visitStatementExpression5(Java9_v2Parser::StatementExpression5Context *context) = 0;

    virtual antlrcpp::Any visitStatementExpression6(Java9_v2Parser::StatementExpression6Context *context) = 0;

    virtual antlrcpp::Any visitStatementExpression7(Java9_v2Parser::StatementExpression7Context *context) = 0;

    virtual antlrcpp::Any visitIfThenStatement(Java9_v2Parser::IfThenStatementContext *context) = 0;

    virtual antlrcpp::Any visitIfThenElseStatement(Java9_v2Parser::IfThenElseStatementContext *context) = 0;

    virtual antlrcpp::Any visitIfThenElseStatementNoShortIf(Java9_v2Parser::IfThenElseStatementNoShortIfContext *context) = 0;

    virtual antlrcpp::Any visitAssertStatement1(Java9_v2Parser::AssertStatement1Context *context) = 0;

    virtual antlrcpp::Any visitAssertStatement2(Java9_v2Parser::AssertStatement2Context *context) = 0;

    virtual antlrcpp::Any visitSwitchStatement(Java9_v2Parser::SwitchStatementContext *context) = 0;

    virtual antlrcpp::Any visitSwitchBlock(Java9_v2Parser::SwitchBlockContext *context) = 0;

    virtual antlrcpp::Any visitSwitchBlockStatementGroup(Java9_v2Parser::SwitchBlockStatementGroupContext *context) = 0;

    virtual antlrcpp::Any visitSwitchLabels(Java9_v2Parser::SwitchLabelsContext *context) = 0;

    virtual antlrcpp::Any visitSwitchLabel1(Java9_v2Parser::SwitchLabel1Context *context) = 0;

    virtual antlrcpp::Any visitSwitchLabel2(Java9_v2Parser::SwitchLabel2Context *context) = 0;

    virtual antlrcpp::Any visitSwitchLabel3(Java9_v2Parser::SwitchLabel3Context *context) = 0;

    virtual antlrcpp::Any visitEnumConstantName(Java9_v2Parser::EnumConstantNameContext *context) = 0;

    virtual antlrcpp::Any visitWhileStatement(Java9_v2Parser::WhileStatementContext *context) = 0;

    virtual antlrcpp::Any visitWhileStatementNoShortIf(Java9_v2Parser::WhileStatementNoShortIfContext *context) = 0;

    virtual antlrcpp::Any visitDoStatement(Java9_v2Parser::DoStatementContext *context) = 0;

    virtual antlrcpp::Any visitForStatement1(Java9_v2Parser::ForStatement1Context *context) = 0;

    virtual antlrcpp::Any visitForStatement2(Java9_v2Parser::ForStatement2Context *context) = 0;

    virtual antlrcpp::Any visitForStatementNoShortIf3(Java9_v2Parser::ForStatementNoShortIf3Context *context) = 0;

    virtual antlrcpp::Any visitForStatementNoShortIf4(Java9_v2Parser::ForStatementNoShortIf4Context *context) = 0;

    virtual antlrcpp::Any visitBasicForStatement(Java9_v2Parser::BasicForStatementContext *context) = 0;

    virtual antlrcpp::Any visitBasicForStatementNoShortIf(Java9_v2Parser::BasicForStatementNoShortIfContext *context) = 0;

    virtual antlrcpp::Any visitForInit1(Java9_v2Parser::ForInit1Context *context) = 0;

    virtual antlrcpp::Any visitForInit2(Java9_v2Parser::ForInit2Context *context) = 0;

    virtual antlrcpp::Any visitForUpdate(Java9_v2Parser::ForUpdateContext *context) = 0;

    virtual antlrcpp::Any visitStatementExpressionList(Java9_v2Parser::StatementExpressionListContext *context) = 0;

    virtual antlrcpp::Any visitEnhancedForStatement(Java9_v2Parser::EnhancedForStatementContext *context) = 0;

    virtual antlrcpp::Any visitEnhancedForStatementNoShortIf(Java9_v2Parser::EnhancedForStatementNoShortIfContext *context) = 0;

    virtual antlrcpp::Any visitBreakStatement(Java9_v2Parser::BreakStatementContext *context) = 0;

    virtual antlrcpp::Any visitContinueStatement(Java9_v2Parser::ContinueStatementContext *context) = 0;

    virtual antlrcpp::Any visitReturnStatement(Java9_v2Parser::ReturnStatementContext *context) = 0;

    virtual antlrcpp::Any visitThrowStatement(Java9_v2Parser::ThrowStatementContext *context) = 0;

    virtual antlrcpp::Any visitSynchronizedStatement(Java9_v2Parser::SynchronizedStatementContext *context) = 0;

    virtual antlrcpp::Any visitTryStatement1(Java9_v2Parser::TryStatement1Context *context) = 0;

    virtual antlrcpp::Any visitTryStatement2(Java9_v2Parser::TryStatement2Context *context) = 0;

    virtual antlrcpp::Any visitTryStatement3(Java9_v2Parser::TryStatement3Context *context) = 0;

    virtual antlrcpp::Any visitCatches(Java9_v2Parser::CatchesContext *context) = 0;

    virtual antlrcpp::Any visitCatchClause(Java9_v2Parser::CatchClauseContext *context) = 0;

    virtual antlrcpp::Any visitCatchFormalParameter(Java9_v2Parser::CatchFormalParameterContext *context) = 0;

    virtual antlrcpp::Any visitCatchType(Java9_v2Parser::CatchTypeContext *context) = 0;

    virtual antlrcpp::Any visitFinally_(Java9_v2Parser::Finally_Context *context) = 0;

    virtual antlrcpp::Any visitTryWithResourcesStatement(Java9_v2Parser::TryWithResourcesStatementContext *context) = 0;

    virtual antlrcpp::Any visitResourceSpecification(Java9_v2Parser::ResourceSpecificationContext *context) = 0;

    virtual antlrcpp::Any visitResourceList(Java9_v2Parser::ResourceListContext *context) = 0;

    virtual antlrcpp::Any visitResource1(Java9_v2Parser::Resource1Context *context) = 0;

    virtual antlrcpp::Any visitResource2(Java9_v2Parser::Resource2Context *context) = 0;

    virtual antlrcpp::Any visitVariableAccess1(Java9_v2Parser::VariableAccess1Context *context) = 0;

    virtual antlrcpp::Any visitVariableAccess2(Java9_v2Parser::VariableAccess2Context *context) = 0;

    virtual antlrcpp::Any visitPrimary(Java9_v2Parser::PrimaryContext *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray1(Java9_v2Parser::PrimaryNoNewArray1Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray2(Java9_v2Parser::PrimaryNoNewArray2Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray3(Java9_v2Parser::PrimaryNoNewArray3Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray4(Java9_v2Parser::PrimaryNoNewArray4Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray5(Java9_v2Parser::PrimaryNoNewArray5Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray6(Java9_v2Parser::PrimaryNoNewArray6Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray7(Java9_v2Parser::PrimaryNoNewArray7Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray8(Java9_v2Parser::PrimaryNoNewArray8Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray9(Java9_v2Parser::PrimaryNoNewArray9Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray10(Java9_v2Parser::PrimaryNoNewArray10Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_arrayAccess(Java9_v2Parser::PrimaryNoNewArray_lf_arrayAccessContext *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess1(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess1Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess2(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess2Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess3(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess3Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess4(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess4Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess5(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess5Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess6(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess6Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess7(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess7Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess8(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess8Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess9(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess9Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_arrayAccess10(Java9_v2Parser::PrimaryNoNewArray_lfno_arrayAccess10Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary1(Java9_v2Parser::PrimaryNoNewArray_lf_primary1Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary2(Java9_v2Parser::PrimaryNoNewArray_lf_primary2Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary3(Java9_v2Parser::PrimaryNoNewArray_lf_primary3Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary4(Java9_v2Parser::PrimaryNoNewArray_lf_primary4Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary5(Java9_v2Parser::PrimaryNoNewArray_lf_primary5Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4(Java9_v2Parser::PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary1(Java9_v2Parser::PrimaryNoNewArray_lfno_primary1Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary2(Java9_v2Parser::PrimaryNoNewArray_lfno_primary2Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary3(Java9_v2Parser::PrimaryNoNewArray_lfno_primary3Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary4(Java9_v2Parser::PrimaryNoNewArray_lfno_primary4Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary5(Java9_v2Parser::PrimaryNoNewArray_lfno_primary5Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary6(Java9_v2Parser::PrimaryNoNewArray_lfno_primary6Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary7(Java9_v2Parser::PrimaryNoNewArray_lfno_primary7Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary8(Java9_v2Parser::PrimaryNoNewArray_lfno_primary8Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary9(Java9_v2Parser::PrimaryNoNewArray_lfno_primary9Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary10(Java9_v2Parser::PrimaryNoNewArray_lfno_primary10Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary11(Java9_v2Parser::PrimaryNoNewArray_lfno_primary11Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary12(Java9_v2Parser::PrimaryNoNewArray_lfno_primary12Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10Context *context) = 0;

    virtual antlrcpp::Any visitPrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11(Java9_v2Parser::PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11Context *context) = 0;

    virtual antlrcpp::Any visitClassLiteral1(Java9_v2Parser::ClassLiteral1Context *context) = 0;

    virtual antlrcpp::Any visitClassLiteral2(Java9_v2Parser::ClassLiteral2Context *context) = 0;

    virtual antlrcpp::Any visitClassInstanceCreationExpression1(Java9_v2Parser::ClassInstanceCreationExpression1Context *context) = 0;

    virtual antlrcpp::Any visitClassInstanceCreationExpression2(Java9_v2Parser::ClassInstanceCreationExpression2Context *context) = 0;

    virtual antlrcpp::Any visitClassInstanceCreationExpression3(Java9_v2Parser::ClassInstanceCreationExpression3Context *context) = 0;

    virtual antlrcpp::Any visitClassInstanceCreationExpression_lf_primary(Java9_v2Parser::ClassInstanceCreationExpression_lf_primaryContext *context) = 0;

    virtual antlrcpp::Any visitClassInstanceCreationExpression_lfno_primary1(Java9_v2Parser::ClassInstanceCreationExpression_lfno_primary1Context *context) = 0;

    virtual antlrcpp::Any visitClassInstanceCreationExpression_lfno_primary2(Java9_v2Parser::ClassInstanceCreationExpression_lfno_primary2Context *context) = 0;

    virtual antlrcpp::Any visitTypeArgumentsOrDiamond1(Java9_v2Parser::TypeArgumentsOrDiamond1Context *context) = 0;

    virtual antlrcpp::Any visitTypeArgumentsOrDiamond2(Java9_v2Parser::TypeArgumentsOrDiamond2Context *context) = 0;

    virtual antlrcpp::Any visitFieldAccess1(Java9_v2Parser::FieldAccess1Context *context) = 0;

    virtual antlrcpp::Any visitFieldAccess2(Java9_v2Parser::FieldAccess2Context *context) = 0;

    virtual antlrcpp::Any visitFieldAccess3(Java9_v2Parser::FieldAccess3Context *context) = 0;

    virtual antlrcpp::Any visitFieldAccess_lf_primary(Java9_v2Parser::FieldAccess_lf_primaryContext *context) = 0;

    virtual antlrcpp::Any visitFieldAccess_lfno_primary1(Java9_v2Parser::FieldAccess_lfno_primary1Context *context) = 0;

    virtual antlrcpp::Any visitFieldAccess_lfno_primary2(Java9_v2Parser::FieldAccess_lfno_primary2Context *context) = 0;

    virtual antlrcpp::Any visitArrayAccess(Java9_v2Parser::ArrayAccessContext *context) = 0;

    virtual antlrcpp::Any visitArrayAccess_lf_primary(Java9_v2Parser::ArrayAccess_lf_primaryContext *context) = 0;

    virtual antlrcpp::Any visitArrayAccess_lfno_primary(Java9_v2Parser::ArrayAccess_lfno_primaryContext *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation1(Java9_v2Parser::MethodInvocation1Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation2(Java9_v2Parser::MethodInvocation2Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation3(Java9_v2Parser::MethodInvocation3Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation4(Java9_v2Parser::MethodInvocation4Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation5(Java9_v2Parser::MethodInvocation5Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation6(Java9_v2Parser::MethodInvocation6Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation_lf_primary(Java9_v2Parser::MethodInvocation_lf_primaryContext *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation_lfno_primary1(Java9_v2Parser::MethodInvocation_lfno_primary1Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation_lfno_primary2(Java9_v2Parser::MethodInvocation_lfno_primary2Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation_lfno_primary3(Java9_v2Parser::MethodInvocation_lfno_primary3Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation_lfno_primary4(Java9_v2Parser::MethodInvocation_lfno_primary4Context *context) = 0;

    virtual antlrcpp::Any visitMethodInvocation_lfno_primary5(Java9_v2Parser::MethodInvocation_lfno_primary5Context *context) = 0;

    virtual antlrcpp::Any visitArgumentList(Java9_v2Parser::ArgumentListContext *context) = 0;

    virtual antlrcpp::Any visitMethodReference1(Java9_v2Parser::MethodReference1Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference2(Java9_v2Parser::MethodReference2Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference3(Java9_v2Parser::MethodReference3Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference4(Java9_v2Parser::MethodReference4Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference5(Java9_v2Parser::MethodReference5Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference6(Java9_v2Parser::MethodReference6Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference7(Java9_v2Parser::MethodReference7Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference_lf_primary(Java9_v2Parser::MethodReference_lf_primaryContext *context) = 0;

    virtual antlrcpp::Any visitMethodReference_lfno_primary1(Java9_v2Parser::MethodReference_lfno_primary1Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference_lfno_primary2(Java9_v2Parser::MethodReference_lfno_primary2Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference_lfno_primary3(Java9_v2Parser::MethodReference_lfno_primary3Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference_lfno_primary4(Java9_v2Parser::MethodReference_lfno_primary4Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference_lfno_primary5(Java9_v2Parser::MethodReference_lfno_primary5Context *context) = 0;

    virtual antlrcpp::Any visitMethodReference_lfno_primary6(Java9_v2Parser::MethodReference_lfno_primary6Context *context) = 0;

    virtual antlrcpp::Any visitArrayCreationExpression1(Java9_v2Parser::ArrayCreationExpression1Context *context) = 0;

    virtual antlrcpp::Any visitArrayCreationExpression2(Java9_v2Parser::ArrayCreationExpression2Context *context) = 0;

    virtual antlrcpp::Any visitArrayCreationExpression3(Java9_v2Parser::ArrayCreationExpression3Context *context) = 0;

    virtual antlrcpp::Any visitArrayCreationExpression4(Java9_v2Parser::ArrayCreationExpression4Context *context) = 0;

    virtual antlrcpp::Any visitDimExprs(Java9_v2Parser::DimExprsContext *context) = 0;

    virtual antlrcpp::Any visitDimExpr(Java9_v2Parser::DimExprContext *context) = 0;

    virtual antlrcpp::Any visitConstantExpression(Java9_v2Parser::ConstantExpressionContext *context) = 0;

    virtual antlrcpp::Any visitExpression1(Java9_v2Parser::Expression1Context *context) = 0;

    virtual antlrcpp::Any visitExpression2(Java9_v2Parser::Expression2Context *context) = 0;

    virtual antlrcpp::Any visitLambdaExpression(Java9_v2Parser::LambdaExpressionContext *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters1(Java9_v2Parser::LambdaParameters1Context *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters2(Java9_v2Parser::LambdaParameters2Context *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters3(Java9_v2Parser::LambdaParameters3Context *context) = 0;

    virtual antlrcpp::Any visitInferredFormalParameterList(Java9_v2Parser::InferredFormalParameterListContext *context) = 0;

    virtual antlrcpp::Any visitLambdaBody1(Java9_v2Parser::LambdaBody1Context *context) = 0;

    virtual antlrcpp::Any visitLambdaBody2(Java9_v2Parser::LambdaBody2Context *context) = 0;

    virtual antlrcpp::Any visitAssignmentExpression1(Java9_v2Parser::AssignmentExpression1Context *context) = 0;

    virtual antlrcpp::Any visitAssignmentExpression2(Java9_v2Parser::AssignmentExpression2Context *context) = 0;

    virtual antlrcpp::Any visitAssignment(Java9_v2Parser::AssignmentContext *context) = 0;

    virtual antlrcpp::Any visitLeftHandSide3(Java9_v2Parser::LeftHandSide3Context *context) = 0;

    virtual antlrcpp::Any visitLeftHandSide4(Java9_v2Parser::LeftHandSide4Context *context) = 0;

    virtual antlrcpp::Any visitLeftHandSide5(Java9_v2Parser::LeftHandSide5Context *context) = 0;

    virtual antlrcpp::Any visitAssignmentOperator(Java9_v2Parser::AssignmentOperatorContext *context) = 0;

    virtual antlrcpp::Any visitConditionalExpression1(Java9_v2Parser::ConditionalExpression1Context *context) = 0;

    virtual antlrcpp::Any visitConditionalExpression2(Java9_v2Parser::ConditionalExpression2Context *context) = 0;

    virtual antlrcpp::Any visitConditionalOrExpression1(Java9_v2Parser::ConditionalOrExpression1Context *context) = 0;

    virtual antlrcpp::Any visitConditionalOrExpression2(Java9_v2Parser::ConditionalOrExpression2Context *context) = 0;

    virtual antlrcpp::Any visitConditionalAndExpression2(Java9_v2Parser::ConditionalAndExpression2Context *context) = 0;

    virtual antlrcpp::Any visitConditionalAndExpression1(Java9_v2Parser::ConditionalAndExpression1Context *context) = 0;

    virtual antlrcpp::Any visitInclusiveOrExpression2(Java9_v2Parser::InclusiveOrExpression2Context *context) = 0;

    virtual antlrcpp::Any visitInclusiveOrExpression1(Java9_v2Parser::InclusiveOrExpression1Context *context) = 0;

    virtual antlrcpp::Any visitExclusiveOrExpression1(Java9_v2Parser::ExclusiveOrExpression1Context *context) = 0;

    virtual antlrcpp::Any visitExclusiveOrExpression2(Java9_v2Parser::ExclusiveOrExpression2Context *context) = 0;

    virtual antlrcpp::Any visitAndExpression2(Java9_v2Parser::AndExpression2Context *context) = 0;

    virtual antlrcpp::Any visitAndExpression1(Java9_v2Parser::AndExpression1Context *context) = 0;

    virtual antlrcpp::Any visitEqualityExpression3(Java9_v2Parser::EqualityExpression3Context *context) = 0;

    virtual antlrcpp::Any visitEqualityExpression2(Java9_v2Parser::EqualityExpression2Context *context) = 0;

    virtual antlrcpp::Any visitEqualityExpression1(Java9_v2Parser::EqualityExpression1Context *context) = 0;

    virtual antlrcpp::Any visitRelationalExpression1(Java9_v2Parser::RelationalExpression1Context *context) = 0;

    virtual antlrcpp::Any visitRelationalExpression2(Java9_v2Parser::RelationalExpression2Context *context) = 0;

    virtual antlrcpp::Any visitRelationalExpression5(Java9_v2Parser::RelationalExpression5Context *context) = 0;

    virtual antlrcpp::Any visitRelationalExpression6(Java9_v2Parser::RelationalExpression6Context *context) = 0;

    virtual antlrcpp::Any visitRelationalExpression3(Java9_v2Parser::RelationalExpression3Context *context) = 0;

    virtual antlrcpp::Any visitRelationalExpression4(Java9_v2Parser::RelationalExpression4Context *context) = 0;

    virtual antlrcpp::Any visitShiftExpression1(Java9_v2Parser::ShiftExpression1Context *context) = 0;

    virtual antlrcpp::Any visitShiftExpression3(Java9_v2Parser::ShiftExpression3Context *context) = 0;

    virtual antlrcpp::Any visitShiftExpression2(Java9_v2Parser::ShiftExpression2Context *context) = 0;

    virtual antlrcpp::Any visitShiftExpression4(Java9_v2Parser::ShiftExpression4Context *context) = 0;

    virtual antlrcpp::Any visitAdditiveExpression1(Java9_v2Parser::AdditiveExpression1Context *context) = 0;

    virtual antlrcpp::Any visitAdditiveExpression3(Java9_v2Parser::AdditiveExpression3Context *context) = 0;

    virtual antlrcpp::Any visitAdditiveExpressio2(Java9_v2Parser::AdditiveExpressio2Context *context) = 0;

    virtual antlrcpp::Any visitMultiplicativeExpression1(Java9_v2Parser::MultiplicativeExpression1Context *context) = 0;

    virtual antlrcpp::Any visitMultiplicativeExpression4(Java9_v2Parser::MultiplicativeExpression4Context *context) = 0;

    virtual antlrcpp::Any visitMultiplicativeExpression3(Java9_v2Parser::MultiplicativeExpression3Context *context) = 0;

    virtual antlrcpp::Any visitMultiplicativeExpression2(Java9_v2Parser::MultiplicativeExpression2Context *context) = 0;

    virtual antlrcpp::Any visitUnaryExpression1(Java9_v2Parser::UnaryExpression1Context *context) = 0;

    virtual antlrcpp::Any visitUnaryExpression2(Java9_v2Parser::UnaryExpression2Context *context) = 0;

    virtual antlrcpp::Any visitUnaryExpression3(Java9_v2Parser::UnaryExpression3Context *context) = 0;

    virtual antlrcpp::Any visitUnaryExpression4(Java9_v2Parser::UnaryExpression4Context *context) = 0;

    virtual antlrcpp::Any visitUnaryExpression5(Java9_v2Parser::UnaryExpression5Context *context) = 0;

    virtual antlrcpp::Any visitPreIncrementExpression(Java9_v2Parser::PreIncrementExpressionContext *context) = 0;

    virtual antlrcpp::Any visitPreDecrementExpression(Java9_v2Parser::PreDecrementExpressionContext *context) = 0;

    virtual antlrcpp::Any visitUnaryExpressionNotPlusMinus1(Java9_v2Parser::UnaryExpressionNotPlusMinus1Context *context) = 0;

    virtual antlrcpp::Any visitUnaryExpressionNotPlusMinus2(Java9_v2Parser::UnaryExpressionNotPlusMinus2Context *context) = 0;

    virtual antlrcpp::Any visitUnaryExpressionNotPlusMinus3(Java9_v2Parser::UnaryExpressionNotPlusMinus3Context *context) = 0;

    virtual antlrcpp::Any visitUnaryExpressionNotPlusMinus4(Java9_v2Parser::UnaryExpressionNotPlusMinus4Context *context) = 0;

    virtual antlrcpp::Any visitPostfixExpression(Java9_v2Parser::PostfixExpressionContext *context) = 0;

    virtual antlrcpp::Any visitPostIncrementExpression(Java9_v2Parser::PostIncrementExpressionContext *context) = 0;

    virtual antlrcpp::Any visitPostIncrementExpression_lf_postfixExpression(Java9_v2Parser::PostIncrementExpression_lf_postfixExpressionContext *context) = 0;

    virtual antlrcpp::Any visitPostDecrementExpression(Java9_v2Parser::PostDecrementExpressionContext *context) = 0;

    virtual antlrcpp::Any visitPostDecrementExpression_lf_postfixExpression(Java9_v2Parser::PostDecrementExpression_lf_postfixExpressionContext *context) = 0;

    virtual antlrcpp::Any visitCastExpression1(Java9_v2Parser::CastExpression1Context *context) = 0;

    virtual antlrcpp::Any visitCastExpression2(Java9_v2Parser::CastExpression2Context *context) = 0;

    virtual antlrcpp::Any visitCastExpression3(Java9_v2Parser::CastExpression3Context *context) = 0;

    virtual antlrcpp::Any visitIdentifier(Java9_v2Parser::IdentifierContext *context) = 0;


};

