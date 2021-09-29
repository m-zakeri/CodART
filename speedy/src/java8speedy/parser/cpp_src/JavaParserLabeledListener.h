
// Generated from D:/AnacondaProjects/CodART/grammars\JavaParserLabeled.g4 by ANTLR 4.9.1

#pragma once


#include "antlr4-runtime.h"
#include "JavaParserLabeled.h"


/**
 * This interface defines an abstract listener for a parse tree produced by JavaParserLabeled.
 */
class  JavaParserLabeledListener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterCompilationUnit(JavaParserLabeled::CompilationUnitContext *ctx) = 0;
  virtual void exitCompilationUnit(JavaParserLabeled::CompilationUnitContext *ctx) = 0;

  virtual void enterPackageDeclaration(JavaParserLabeled::PackageDeclarationContext *ctx) = 0;
  virtual void exitPackageDeclaration(JavaParserLabeled::PackageDeclarationContext *ctx) = 0;

  virtual void enterImportDeclaration(JavaParserLabeled::ImportDeclarationContext *ctx) = 0;
  virtual void exitImportDeclaration(JavaParserLabeled::ImportDeclarationContext *ctx) = 0;

  virtual void enterTypeDeclaration(JavaParserLabeled::TypeDeclarationContext *ctx) = 0;
  virtual void exitTypeDeclaration(JavaParserLabeled::TypeDeclarationContext *ctx) = 0;

  virtual void enterModifier(JavaParserLabeled::ModifierContext *ctx) = 0;
  virtual void exitModifier(JavaParserLabeled::ModifierContext *ctx) = 0;

  virtual void enterClassOrInterfaceModifier(JavaParserLabeled::ClassOrInterfaceModifierContext *ctx) = 0;
  virtual void exitClassOrInterfaceModifier(JavaParserLabeled::ClassOrInterfaceModifierContext *ctx) = 0;

  virtual void enterVariableModifier(JavaParserLabeled::VariableModifierContext *ctx) = 0;
  virtual void exitVariableModifier(JavaParserLabeled::VariableModifierContext *ctx) = 0;

  virtual void enterClassDeclaration(JavaParserLabeled::ClassDeclarationContext *ctx) = 0;
  virtual void exitClassDeclaration(JavaParserLabeled::ClassDeclarationContext *ctx) = 0;

  virtual void enterTypeParameters(JavaParserLabeled::TypeParametersContext *ctx) = 0;
  virtual void exitTypeParameters(JavaParserLabeled::TypeParametersContext *ctx) = 0;

  virtual void enterTypeParameter(JavaParserLabeled::TypeParameterContext *ctx) = 0;
  virtual void exitTypeParameter(JavaParserLabeled::TypeParameterContext *ctx) = 0;

  virtual void enterTypeBound(JavaParserLabeled::TypeBoundContext *ctx) = 0;
  virtual void exitTypeBound(JavaParserLabeled::TypeBoundContext *ctx) = 0;

  virtual void enterEnumDeclaration(JavaParserLabeled::EnumDeclarationContext *ctx) = 0;
  virtual void exitEnumDeclaration(JavaParserLabeled::EnumDeclarationContext *ctx) = 0;

  virtual void enterEnumConstants(JavaParserLabeled::EnumConstantsContext *ctx) = 0;
  virtual void exitEnumConstants(JavaParserLabeled::EnumConstantsContext *ctx) = 0;

  virtual void enterEnumConstant(JavaParserLabeled::EnumConstantContext *ctx) = 0;
  virtual void exitEnumConstant(JavaParserLabeled::EnumConstantContext *ctx) = 0;

  virtual void enterEnumBodyDeclarations(JavaParserLabeled::EnumBodyDeclarationsContext *ctx) = 0;
  virtual void exitEnumBodyDeclarations(JavaParserLabeled::EnumBodyDeclarationsContext *ctx) = 0;

  virtual void enterInterfaceDeclaration(JavaParserLabeled::InterfaceDeclarationContext *ctx) = 0;
  virtual void exitInterfaceDeclaration(JavaParserLabeled::InterfaceDeclarationContext *ctx) = 0;

  virtual void enterClassBody(JavaParserLabeled::ClassBodyContext *ctx) = 0;
  virtual void exitClassBody(JavaParserLabeled::ClassBodyContext *ctx) = 0;

  virtual void enterInterfaceBody(JavaParserLabeled::InterfaceBodyContext *ctx) = 0;
  virtual void exitInterfaceBody(JavaParserLabeled::InterfaceBodyContext *ctx) = 0;

  virtual void enterClassBodyDeclaration0(JavaParserLabeled::ClassBodyDeclaration0Context *ctx) = 0;
  virtual void exitClassBodyDeclaration0(JavaParserLabeled::ClassBodyDeclaration0Context *ctx) = 0;

  virtual void enterClassBodyDeclaration1(JavaParserLabeled::ClassBodyDeclaration1Context *ctx) = 0;
  virtual void exitClassBodyDeclaration1(JavaParserLabeled::ClassBodyDeclaration1Context *ctx) = 0;

  virtual void enterClassBodyDeclaration2(JavaParserLabeled::ClassBodyDeclaration2Context *ctx) = 0;
  virtual void exitClassBodyDeclaration2(JavaParserLabeled::ClassBodyDeclaration2Context *ctx) = 0;

  virtual void enterMemberDeclaration0(JavaParserLabeled::MemberDeclaration0Context *ctx) = 0;
  virtual void exitMemberDeclaration0(JavaParserLabeled::MemberDeclaration0Context *ctx) = 0;

  virtual void enterMemberDeclaration1(JavaParserLabeled::MemberDeclaration1Context *ctx) = 0;
  virtual void exitMemberDeclaration1(JavaParserLabeled::MemberDeclaration1Context *ctx) = 0;

  virtual void enterMemberDeclaration2(JavaParserLabeled::MemberDeclaration2Context *ctx) = 0;
  virtual void exitMemberDeclaration2(JavaParserLabeled::MemberDeclaration2Context *ctx) = 0;

  virtual void enterMemberDeclaration3(JavaParserLabeled::MemberDeclaration3Context *ctx) = 0;
  virtual void exitMemberDeclaration3(JavaParserLabeled::MemberDeclaration3Context *ctx) = 0;

  virtual void enterMemberDeclaration4(JavaParserLabeled::MemberDeclaration4Context *ctx) = 0;
  virtual void exitMemberDeclaration4(JavaParserLabeled::MemberDeclaration4Context *ctx) = 0;

  virtual void enterMemberDeclaration5(JavaParserLabeled::MemberDeclaration5Context *ctx) = 0;
  virtual void exitMemberDeclaration5(JavaParserLabeled::MemberDeclaration5Context *ctx) = 0;

  virtual void enterMemberDeclaration6(JavaParserLabeled::MemberDeclaration6Context *ctx) = 0;
  virtual void exitMemberDeclaration6(JavaParserLabeled::MemberDeclaration6Context *ctx) = 0;

  virtual void enterMemberDeclaration7(JavaParserLabeled::MemberDeclaration7Context *ctx) = 0;
  virtual void exitMemberDeclaration7(JavaParserLabeled::MemberDeclaration7Context *ctx) = 0;

  virtual void enterMemberDeclaration8(JavaParserLabeled::MemberDeclaration8Context *ctx) = 0;
  virtual void exitMemberDeclaration8(JavaParserLabeled::MemberDeclaration8Context *ctx) = 0;

  virtual void enterMethodDeclaration(JavaParserLabeled::MethodDeclarationContext *ctx) = 0;
  virtual void exitMethodDeclaration(JavaParserLabeled::MethodDeclarationContext *ctx) = 0;

  virtual void enterMethodBody(JavaParserLabeled::MethodBodyContext *ctx) = 0;
  virtual void exitMethodBody(JavaParserLabeled::MethodBodyContext *ctx) = 0;

  virtual void enterTypeTypeOrVoid(JavaParserLabeled::TypeTypeOrVoidContext *ctx) = 0;
  virtual void exitTypeTypeOrVoid(JavaParserLabeled::TypeTypeOrVoidContext *ctx) = 0;

  virtual void enterGenericMethodDeclaration(JavaParserLabeled::GenericMethodDeclarationContext *ctx) = 0;
  virtual void exitGenericMethodDeclaration(JavaParserLabeled::GenericMethodDeclarationContext *ctx) = 0;

  virtual void enterGenericConstructorDeclaration(JavaParserLabeled::GenericConstructorDeclarationContext *ctx) = 0;
  virtual void exitGenericConstructorDeclaration(JavaParserLabeled::GenericConstructorDeclarationContext *ctx) = 0;

  virtual void enterConstructorDeclaration(JavaParserLabeled::ConstructorDeclarationContext *ctx) = 0;
  virtual void exitConstructorDeclaration(JavaParserLabeled::ConstructorDeclarationContext *ctx) = 0;

  virtual void enterFieldDeclaration(JavaParserLabeled::FieldDeclarationContext *ctx) = 0;
  virtual void exitFieldDeclaration(JavaParserLabeled::FieldDeclarationContext *ctx) = 0;

  virtual void enterInterfaceBodyDeclaration(JavaParserLabeled::InterfaceBodyDeclarationContext *ctx) = 0;
  virtual void exitInterfaceBodyDeclaration(JavaParserLabeled::InterfaceBodyDeclarationContext *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration0(JavaParserLabeled::InterfaceMemberDeclaration0Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration0(JavaParserLabeled::InterfaceMemberDeclaration0Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration1(JavaParserLabeled::InterfaceMemberDeclaration1Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration1(JavaParserLabeled::InterfaceMemberDeclaration1Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration2(JavaParserLabeled::InterfaceMemberDeclaration2Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration2(JavaParserLabeled::InterfaceMemberDeclaration2Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration3(JavaParserLabeled::InterfaceMemberDeclaration3Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration3(JavaParserLabeled::InterfaceMemberDeclaration3Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration4(JavaParserLabeled::InterfaceMemberDeclaration4Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration4(JavaParserLabeled::InterfaceMemberDeclaration4Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration5(JavaParserLabeled::InterfaceMemberDeclaration5Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration5(JavaParserLabeled::InterfaceMemberDeclaration5Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration6(JavaParserLabeled::InterfaceMemberDeclaration6Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration6(JavaParserLabeled::InterfaceMemberDeclaration6Context *ctx) = 0;

  virtual void enterConstDeclaration(JavaParserLabeled::ConstDeclarationContext *ctx) = 0;
  virtual void exitConstDeclaration(JavaParserLabeled::ConstDeclarationContext *ctx) = 0;

  virtual void enterConstantDeclarator(JavaParserLabeled::ConstantDeclaratorContext *ctx) = 0;
  virtual void exitConstantDeclarator(JavaParserLabeled::ConstantDeclaratorContext *ctx) = 0;

  virtual void enterInterfaceMethodDeclaration(JavaParserLabeled::InterfaceMethodDeclarationContext *ctx) = 0;
  virtual void exitInterfaceMethodDeclaration(JavaParserLabeled::InterfaceMethodDeclarationContext *ctx) = 0;

  virtual void enterInterfaceMethodModifier(JavaParserLabeled::InterfaceMethodModifierContext *ctx) = 0;
  virtual void exitInterfaceMethodModifier(JavaParserLabeled::InterfaceMethodModifierContext *ctx) = 0;

  virtual void enterGenericInterfaceMethodDeclaration(JavaParserLabeled::GenericInterfaceMethodDeclarationContext *ctx) = 0;
  virtual void exitGenericInterfaceMethodDeclaration(JavaParserLabeled::GenericInterfaceMethodDeclarationContext *ctx) = 0;

  virtual void enterVariableDeclarators(JavaParserLabeled::VariableDeclaratorsContext *ctx) = 0;
  virtual void exitVariableDeclarators(JavaParserLabeled::VariableDeclaratorsContext *ctx) = 0;

  virtual void enterVariableDeclarator(JavaParserLabeled::VariableDeclaratorContext *ctx) = 0;
  virtual void exitVariableDeclarator(JavaParserLabeled::VariableDeclaratorContext *ctx) = 0;

  virtual void enterVariableDeclaratorId(JavaParserLabeled::VariableDeclaratorIdContext *ctx) = 0;
  virtual void exitVariableDeclaratorId(JavaParserLabeled::VariableDeclaratorIdContext *ctx) = 0;

  virtual void enterVariableInitializer0(JavaParserLabeled::VariableInitializer0Context *ctx) = 0;
  virtual void exitVariableInitializer0(JavaParserLabeled::VariableInitializer0Context *ctx) = 0;

  virtual void enterVariableInitializer1(JavaParserLabeled::VariableInitializer1Context *ctx) = 0;
  virtual void exitVariableInitializer1(JavaParserLabeled::VariableInitializer1Context *ctx) = 0;

  virtual void enterArrayInitializer(JavaParserLabeled::ArrayInitializerContext *ctx) = 0;
  virtual void exitArrayInitializer(JavaParserLabeled::ArrayInitializerContext *ctx) = 0;

  virtual void enterClassOrInterfaceType(JavaParserLabeled::ClassOrInterfaceTypeContext *ctx) = 0;
  virtual void exitClassOrInterfaceType(JavaParserLabeled::ClassOrInterfaceTypeContext *ctx) = 0;

  virtual void enterTypeArgument0(JavaParserLabeled::TypeArgument0Context *ctx) = 0;
  virtual void exitTypeArgument0(JavaParserLabeled::TypeArgument0Context *ctx) = 0;

  virtual void enterQualifiedNameList(JavaParserLabeled::QualifiedNameListContext *ctx) = 0;
  virtual void exitQualifiedNameList(JavaParserLabeled::QualifiedNameListContext *ctx) = 0;

  virtual void enterFormalParameters(JavaParserLabeled::FormalParametersContext *ctx) = 0;
  virtual void exitFormalParameters(JavaParserLabeled::FormalParametersContext *ctx) = 0;

  virtual void enterFormalParameterList0(JavaParserLabeled::FormalParameterList0Context *ctx) = 0;
  virtual void exitFormalParameterList0(JavaParserLabeled::FormalParameterList0Context *ctx) = 0;

  virtual void enterFormalParameterList1(JavaParserLabeled::FormalParameterList1Context *ctx) = 0;
  virtual void exitFormalParameterList1(JavaParserLabeled::FormalParameterList1Context *ctx) = 0;

  virtual void enterFormalParameter(JavaParserLabeled::FormalParameterContext *ctx) = 0;
  virtual void exitFormalParameter(JavaParserLabeled::FormalParameterContext *ctx) = 0;

  virtual void enterLastFormalParameter(JavaParserLabeled::LastFormalParameterContext *ctx) = 0;
  virtual void exitLastFormalParameter(JavaParserLabeled::LastFormalParameterContext *ctx) = 0;

  virtual void enterQualifiedName(JavaParserLabeled::QualifiedNameContext *ctx) = 0;
  virtual void exitQualifiedName(JavaParserLabeled::QualifiedNameContext *ctx) = 0;

  virtual void enterLiteral0(JavaParserLabeled::Literal0Context *ctx) = 0;
  virtual void exitLiteral0(JavaParserLabeled::Literal0Context *ctx) = 0;

  virtual void enterLiteral1(JavaParserLabeled::Literal1Context *ctx) = 0;
  virtual void exitLiteral1(JavaParserLabeled::Literal1Context *ctx) = 0;

  virtual void enterLiteral2(JavaParserLabeled::Literal2Context *ctx) = 0;
  virtual void exitLiteral2(JavaParserLabeled::Literal2Context *ctx) = 0;

  virtual void enterLiteral3(JavaParserLabeled::Literal3Context *ctx) = 0;
  virtual void exitLiteral3(JavaParserLabeled::Literal3Context *ctx) = 0;

  virtual void enterLiteral4(JavaParserLabeled::Literal4Context *ctx) = 0;
  virtual void exitLiteral4(JavaParserLabeled::Literal4Context *ctx) = 0;

  virtual void enterLiteral5(JavaParserLabeled::Literal5Context *ctx) = 0;
  virtual void exitLiteral5(JavaParserLabeled::Literal5Context *ctx) = 0;

  virtual void enterIntegerLiteral(JavaParserLabeled::IntegerLiteralContext *ctx) = 0;
  virtual void exitIntegerLiteral(JavaParserLabeled::IntegerLiteralContext *ctx) = 0;

  virtual void enterFloatLiteral(JavaParserLabeled::FloatLiteralContext *ctx) = 0;
  virtual void exitFloatLiteral(JavaParserLabeled::FloatLiteralContext *ctx) = 0;

  virtual void enterAltAnnotationQualifiedName(JavaParserLabeled::AltAnnotationQualifiedNameContext *ctx) = 0;
  virtual void exitAltAnnotationQualifiedName(JavaParserLabeled::AltAnnotationQualifiedNameContext *ctx) = 0;

  virtual void enterAnnotation(JavaParserLabeled::AnnotationContext *ctx) = 0;
  virtual void exitAnnotation(JavaParserLabeled::AnnotationContext *ctx) = 0;

  virtual void enterElementValuePairs(JavaParserLabeled::ElementValuePairsContext *ctx) = 0;
  virtual void exitElementValuePairs(JavaParserLabeled::ElementValuePairsContext *ctx) = 0;

  virtual void enterElementValuePair(JavaParserLabeled::ElementValuePairContext *ctx) = 0;
  virtual void exitElementValuePair(JavaParserLabeled::ElementValuePairContext *ctx) = 0;

  virtual void enterElementValue0(JavaParserLabeled::ElementValue0Context *ctx) = 0;
  virtual void exitElementValue0(JavaParserLabeled::ElementValue0Context *ctx) = 0;

  virtual void enterElementValue1(JavaParserLabeled::ElementValue1Context *ctx) = 0;
  virtual void exitElementValue1(JavaParserLabeled::ElementValue1Context *ctx) = 0;

  virtual void enterElementValue2(JavaParserLabeled::ElementValue2Context *ctx) = 0;
  virtual void exitElementValue2(JavaParserLabeled::ElementValue2Context *ctx) = 0;

  virtual void enterElementValueArrayInitializer(JavaParserLabeled::ElementValueArrayInitializerContext *ctx) = 0;
  virtual void exitElementValueArrayInitializer(JavaParserLabeled::ElementValueArrayInitializerContext *ctx) = 0;

  virtual void enterAnnotationTypeDeclaration(JavaParserLabeled::AnnotationTypeDeclarationContext *ctx) = 0;
  virtual void exitAnnotationTypeDeclaration(JavaParserLabeled::AnnotationTypeDeclarationContext *ctx) = 0;

  virtual void enterAnnotationTypeBody(JavaParserLabeled::AnnotationTypeBodyContext *ctx) = 0;
  virtual void exitAnnotationTypeBody(JavaParserLabeled::AnnotationTypeBodyContext *ctx) = 0;

  virtual void enterAnnotationTypeElementDeclaration(JavaParserLabeled::AnnotationTypeElementDeclarationContext *ctx) = 0;
  virtual void exitAnnotationTypeElementDeclaration(JavaParserLabeled::AnnotationTypeElementDeclarationContext *ctx) = 0;

  virtual void enterAnnotationTypeElementRest0(JavaParserLabeled::AnnotationTypeElementRest0Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest0(JavaParserLabeled::AnnotationTypeElementRest0Context *ctx) = 0;

  virtual void enterAnnotationTypeElementRest1(JavaParserLabeled::AnnotationTypeElementRest1Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest1(JavaParserLabeled::AnnotationTypeElementRest1Context *ctx) = 0;

  virtual void enterAnnotationTypeElementRest2(JavaParserLabeled::AnnotationTypeElementRest2Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest2(JavaParserLabeled::AnnotationTypeElementRest2Context *ctx) = 0;

  virtual void enterAnnotationTypeElementRest3(JavaParserLabeled::AnnotationTypeElementRest3Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest3(JavaParserLabeled::AnnotationTypeElementRest3Context *ctx) = 0;

  virtual void enterAnnotationTypeElementRest4(JavaParserLabeled::AnnotationTypeElementRest4Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest4(JavaParserLabeled::AnnotationTypeElementRest4Context *ctx) = 0;

  virtual void enterAnnotationMethodOrConstantRest0(JavaParserLabeled::AnnotationMethodOrConstantRest0Context *ctx) = 0;
  virtual void exitAnnotationMethodOrConstantRest0(JavaParserLabeled::AnnotationMethodOrConstantRest0Context *ctx) = 0;

  virtual void enterAnnotationMethodOrConstantRest1(JavaParserLabeled::AnnotationMethodOrConstantRest1Context *ctx) = 0;
  virtual void exitAnnotationMethodOrConstantRest1(JavaParserLabeled::AnnotationMethodOrConstantRest1Context *ctx) = 0;

  virtual void enterAnnotationMethodRest(JavaParserLabeled::AnnotationMethodRestContext *ctx) = 0;
  virtual void exitAnnotationMethodRest(JavaParserLabeled::AnnotationMethodRestContext *ctx) = 0;

  virtual void enterAnnotationConstantRest(JavaParserLabeled::AnnotationConstantRestContext *ctx) = 0;
  virtual void exitAnnotationConstantRest(JavaParserLabeled::AnnotationConstantRestContext *ctx) = 0;

  virtual void enterDefaultValue(JavaParserLabeled::DefaultValueContext *ctx) = 0;
  virtual void exitDefaultValue(JavaParserLabeled::DefaultValueContext *ctx) = 0;

  virtual void enterBlock(JavaParserLabeled::BlockContext *ctx) = 0;
  virtual void exitBlock(JavaParserLabeled::BlockContext *ctx) = 0;

  virtual void enterBlockStatement0(JavaParserLabeled::BlockStatement0Context *ctx) = 0;
  virtual void exitBlockStatement0(JavaParserLabeled::BlockStatement0Context *ctx) = 0;

  virtual void enterBlockStatement1(JavaParserLabeled::BlockStatement1Context *ctx) = 0;
  virtual void exitBlockStatement1(JavaParserLabeled::BlockStatement1Context *ctx) = 0;

  virtual void enterBlockStatement2(JavaParserLabeled::BlockStatement2Context *ctx) = 0;
  virtual void exitBlockStatement2(JavaParserLabeled::BlockStatement2Context *ctx) = 0;

  virtual void enterLocalVariableDeclaration(JavaParserLabeled::LocalVariableDeclarationContext *ctx) = 0;
  virtual void exitLocalVariableDeclaration(JavaParserLabeled::LocalVariableDeclarationContext *ctx) = 0;

  virtual void enterLocalTypeDeclaration(JavaParserLabeled::LocalTypeDeclarationContext *ctx) = 0;
  virtual void exitLocalTypeDeclaration(JavaParserLabeled::LocalTypeDeclarationContext *ctx) = 0;

  virtual void enterStatement0(JavaParserLabeled::Statement0Context *ctx) = 0;
  virtual void exitStatement0(JavaParserLabeled::Statement0Context *ctx) = 0;

  virtual void enterStatement1(JavaParserLabeled::Statement1Context *ctx) = 0;
  virtual void exitStatement1(JavaParserLabeled::Statement1Context *ctx) = 0;

  virtual void enterStatement2(JavaParserLabeled::Statement2Context *ctx) = 0;
  virtual void exitStatement2(JavaParserLabeled::Statement2Context *ctx) = 0;

  virtual void enterStatement3(JavaParserLabeled::Statement3Context *ctx) = 0;
  virtual void exitStatement3(JavaParserLabeled::Statement3Context *ctx) = 0;

  virtual void enterStatement4(JavaParserLabeled::Statement4Context *ctx) = 0;
  virtual void exitStatement4(JavaParserLabeled::Statement4Context *ctx) = 0;

  virtual void enterStatement5(JavaParserLabeled::Statement5Context *ctx) = 0;
  virtual void exitStatement5(JavaParserLabeled::Statement5Context *ctx) = 0;

  virtual void enterStatement6(JavaParserLabeled::Statement6Context *ctx) = 0;
  virtual void exitStatement6(JavaParserLabeled::Statement6Context *ctx) = 0;

  virtual void enterStatement7(JavaParserLabeled::Statement7Context *ctx) = 0;
  virtual void exitStatement7(JavaParserLabeled::Statement7Context *ctx) = 0;

  virtual void enterStatement8(JavaParserLabeled::Statement8Context *ctx) = 0;
  virtual void exitStatement8(JavaParserLabeled::Statement8Context *ctx) = 0;

  virtual void enterStatement9(JavaParserLabeled::Statement9Context *ctx) = 0;
  virtual void exitStatement9(JavaParserLabeled::Statement9Context *ctx) = 0;

  virtual void enterStatement10(JavaParserLabeled::Statement10Context *ctx) = 0;
  virtual void exitStatement10(JavaParserLabeled::Statement10Context *ctx) = 0;

  virtual void enterStatement11(JavaParserLabeled::Statement11Context *ctx) = 0;
  virtual void exitStatement11(JavaParserLabeled::Statement11Context *ctx) = 0;

  virtual void enterStatement12(JavaParserLabeled::Statement12Context *ctx) = 0;
  virtual void exitStatement12(JavaParserLabeled::Statement12Context *ctx) = 0;

  virtual void enterStatement13(JavaParserLabeled::Statement13Context *ctx) = 0;
  virtual void exitStatement13(JavaParserLabeled::Statement13Context *ctx) = 0;

  virtual void enterStatement14(JavaParserLabeled::Statement14Context *ctx) = 0;
  virtual void exitStatement14(JavaParserLabeled::Statement14Context *ctx) = 0;

  virtual void enterStatement15(JavaParserLabeled::Statement15Context *ctx) = 0;
  virtual void exitStatement15(JavaParserLabeled::Statement15Context *ctx) = 0;

  virtual void enterStatement16(JavaParserLabeled::Statement16Context *ctx) = 0;
  virtual void exitStatement16(JavaParserLabeled::Statement16Context *ctx) = 0;

  virtual void enterCatchClause(JavaParserLabeled::CatchClauseContext *ctx) = 0;
  virtual void exitCatchClause(JavaParserLabeled::CatchClauseContext *ctx) = 0;

  virtual void enterCatchType(JavaParserLabeled::CatchTypeContext *ctx) = 0;
  virtual void exitCatchType(JavaParserLabeled::CatchTypeContext *ctx) = 0;

  virtual void enterFinallyBlock(JavaParserLabeled::FinallyBlockContext *ctx) = 0;
  virtual void exitFinallyBlock(JavaParserLabeled::FinallyBlockContext *ctx) = 0;

  virtual void enterResourceSpecification(JavaParserLabeled::ResourceSpecificationContext *ctx) = 0;
  virtual void exitResourceSpecification(JavaParserLabeled::ResourceSpecificationContext *ctx) = 0;

  virtual void enterResources(JavaParserLabeled::ResourcesContext *ctx) = 0;
  virtual void exitResources(JavaParserLabeled::ResourcesContext *ctx) = 0;

  virtual void enterResource(JavaParserLabeled::ResourceContext *ctx) = 0;
  virtual void exitResource(JavaParserLabeled::ResourceContext *ctx) = 0;

  virtual void enterSwitchBlockStatementGroup(JavaParserLabeled::SwitchBlockStatementGroupContext *ctx) = 0;
  virtual void exitSwitchBlockStatementGroup(JavaParserLabeled::SwitchBlockStatementGroupContext *ctx) = 0;

  virtual void enterSwitchLabel(JavaParserLabeled::SwitchLabelContext *ctx) = 0;
  virtual void exitSwitchLabel(JavaParserLabeled::SwitchLabelContext *ctx) = 0;

  virtual void enterForControl0(JavaParserLabeled::ForControl0Context *ctx) = 0;
  virtual void exitForControl0(JavaParserLabeled::ForControl0Context *ctx) = 0;

  virtual void enterForControl1(JavaParserLabeled::ForControl1Context *ctx) = 0;
  virtual void exitForControl1(JavaParserLabeled::ForControl1Context *ctx) = 0;

  virtual void enterForInit0(JavaParserLabeled::ForInit0Context *ctx) = 0;
  virtual void exitForInit0(JavaParserLabeled::ForInit0Context *ctx) = 0;

  virtual void enterForInit1(JavaParserLabeled::ForInit1Context *ctx) = 0;
  virtual void exitForInit1(JavaParserLabeled::ForInit1Context *ctx) = 0;

  virtual void enterEnhancedForControl(JavaParserLabeled::EnhancedForControlContext *ctx) = 0;
  virtual void exitEnhancedForControl(JavaParserLabeled::EnhancedForControlContext *ctx) = 0;

  virtual void enterParExpression(JavaParserLabeled::ParExpressionContext *ctx) = 0;
  virtual void exitParExpression(JavaParserLabeled::ParExpressionContext *ctx) = 0;

  virtual void enterExpressionList(JavaParserLabeled::ExpressionListContext *ctx) = 0;
  virtual void exitExpressionList(JavaParserLabeled::ExpressionListContext *ctx) = 0;

  virtual void enterMethodCall0(JavaParserLabeled::MethodCall0Context *ctx) = 0;
  virtual void exitMethodCall0(JavaParserLabeled::MethodCall0Context *ctx) = 0;

  virtual void enterMethodCall1(JavaParserLabeled::MethodCall1Context *ctx) = 0;
  virtual void exitMethodCall1(JavaParserLabeled::MethodCall1Context *ctx) = 0;

  virtual void enterMethodCall2(JavaParserLabeled::MethodCall2Context *ctx) = 0;
  virtual void exitMethodCall2(JavaParserLabeled::MethodCall2Context *ctx) = 0;

  virtual void enterExpression8(JavaParserLabeled::Expression8Context *ctx) = 0;
  virtual void exitExpression8(JavaParserLabeled::Expression8Context *ctx) = 0;

  virtual void enterExpression10(JavaParserLabeled::Expression10Context *ctx) = 0;
  virtual void exitExpression10(JavaParserLabeled::Expression10Context *ctx) = 0;

  virtual void enterExpression9(JavaParserLabeled::Expression9Context *ctx) = 0;
  virtual void exitExpression9(JavaParserLabeled::Expression9Context *ctx) = 0;

  virtual void enterExpression12(JavaParserLabeled::Expression12Context *ctx) = 0;
  virtual void exitExpression12(JavaParserLabeled::Expression12Context *ctx) = 0;

  virtual void enterExpression11(JavaParserLabeled::Expression11Context *ctx) = 0;
  virtual void exitExpression11(JavaParserLabeled::Expression11Context *ctx) = 0;

  virtual void enterExpression14(JavaParserLabeled::Expression14Context *ctx) = 0;
  virtual void exitExpression14(JavaParserLabeled::Expression14Context *ctx) = 0;

  virtual void enterExpression13(JavaParserLabeled::Expression13Context *ctx) = 0;
  virtual void exitExpression13(JavaParserLabeled::Expression13Context *ctx) = 0;

  virtual void enterExpression16(JavaParserLabeled::Expression16Context *ctx) = 0;
  virtual void exitExpression16(JavaParserLabeled::Expression16Context *ctx) = 0;

  virtual void enterExpression15(JavaParserLabeled::Expression15Context *ctx) = 0;
  virtual void exitExpression15(JavaParserLabeled::Expression15Context *ctx) = 0;

  virtual void enterExpression18(JavaParserLabeled::Expression18Context *ctx) = 0;
  virtual void exitExpression18(JavaParserLabeled::Expression18Context *ctx) = 0;

  virtual void enterExpression17(JavaParserLabeled::Expression17Context *ctx) = 0;
  virtual void exitExpression17(JavaParserLabeled::Expression17Context *ctx) = 0;

  virtual void enterExpression19(JavaParserLabeled::Expression19Context *ctx) = 0;
  virtual void exitExpression19(JavaParserLabeled::Expression19Context *ctx) = 0;

  virtual void enterExpression6(JavaParserLabeled::Expression6Context *ctx) = 0;
  virtual void exitExpression6(JavaParserLabeled::Expression6Context *ctx) = 0;

  virtual void enterExpression7(JavaParserLabeled::Expression7Context *ctx) = 0;
  virtual void exitExpression7(JavaParserLabeled::Expression7Context *ctx) = 0;

  virtual void enterExpression4(JavaParserLabeled::Expression4Context *ctx) = 0;
  virtual void exitExpression4(JavaParserLabeled::Expression4Context *ctx) = 0;

  virtual void enterExpression5(JavaParserLabeled::Expression5Context *ctx) = 0;
  virtual void exitExpression5(JavaParserLabeled::Expression5Context *ctx) = 0;

  virtual void enterExpression2(JavaParserLabeled::Expression2Context *ctx) = 0;
  virtual void exitExpression2(JavaParserLabeled::Expression2Context *ctx) = 0;

  virtual void enterExpression3(JavaParserLabeled::Expression3Context *ctx) = 0;
  virtual void exitExpression3(JavaParserLabeled::Expression3Context *ctx) = 0;

  virtual void enterExpression0(JavaParserLabeled::Expression0Context *ctx) = 0;
  virtual void exitExpression0(JavaParserLabeled::Expression0Context *ctx) = 0;

  virtual void enterExpression1(JavaParserLabeled::Expression1Context *ctx) = 0;
  virtual void exitExpression1(JavaParserLabeled::Expression1Context *ctx) = 0;

  virtual void enterExpression21(JavaParserLabeled::Expression21Context *ctx) = 0;
  virtual void exitExpression21(JavaParserLabeled::Expression21Context *ctx) = 0;

  virtual void enterExpression20(JavaParserLabeled::Expression20Context *ctx) = 0;
  virtual void exitExpression20(JavaParserLabeled::Expression20Context *ctx) = 0;

  virtual void enterExpression23(JavaParserLabeled::Expression23Context *ctx) = 0;
  virtual void exitExpression23(JavaParserLabeled::Expression23Context *ctx) = 0;

  virtual void enterExpression22(JavaParserLabeled::Expression22Context *ctx) = 0;
  virtual void exitExpression22(JavaParserLabeled::Expression22Context *ctx) = 0;

  virtual void enterExpression25(JavaParserLabeled::Expression25Context *ctx) = 0;
  virtual void exitExpression25(JavaParserLabeled::Expression25Context *ctx) = 0;

  virtual void enterExpression24(JavaParserLabeled::Expression24Context *ctx) = 0;
  virtual void exitExpression24(JavaParserLabeled::Expression24Context *ctx) = 0;

  virtual void enterLambdaExpression(JavaParserLabeled::LambdaExpressionContext *ctx) = 0;
  virtual void exitLambdaExpression(JavaParserLabeled::LambdaExpressionContext *ctx) = 0;

  virtual void enterLambdaParameters0(JavaParserLabeled::LambdaParameters0Context *ctx) = 0;
  virtual void exitLambdaParameters0(JavaParserLabeled::LambdaParameters0Context *ctx) = 0;

  virtual void enterLambdaParameters1(JavaParserLabeled::LambdaParameters1Context *ctx) = 0;
  virtual void exitLambdaParameters1(JavaParserLabeled::LambdaParameters1Context *ctx) = 0;

  virtual void enterLambdaParameters2(JavaParserLabeled::LambdaParameters2Context *ctx) = 0;
  virtual void exitLambdaParameters2(JavaParserLabeled::LambdaParameters2Context *ctx) = 0;

  virtual void enterLambdaBody0(JavaParserLabeled::LambdaBody0Context *ctx) = 0;
  virtual void exitLambdaBody0(JavaParserLabeled::LambdaBody0Context *ctx) = 0;

  virtual void enterLambdaBody1(JavaParserLabeled::LambdaBody1Context *ctx) = 0;
  virtual void exitLambdaBody1(JavaParserLabeled::LambdaBody1Context *ctx) = 0;

  virtual void enterPrimary0(JavaParserLabeled::Primary0Context *ctx) = 0;
  virtual void exitPrimary0(JavaParserLabeled::Primary0Context *ctx) = 0;

  virtual void enterPrimary1(JavaParserLabeled::Primary1Context *ctx) = 0;
  virtual void exitPrimary1(JavaParserLabeled::Primary1Context *ctx) = 0;

  virtual void enterPrimary2(JavaParserLabeled::Primary2Context *ctx) = 0;
  virtual void exitPrimary2(JavaParserLabeled::Primary2Context *ctx) = 0;

  virtual void enterPrimary3(JavaParserLabeled::Primary3Context *ctx) = 0;
  virtual void exitPrimary3(JavaParserLabeled::Primary3Context *ctx) = 0;

  virtual void enterPrimary4(JavaParserLabeled::Primary4Context *ctx) = 0;
  virtual void exitPrimary4(JavaParserLabeled::Primary4Context *ctx) = 0;

  virtual void enterPrimary5(JavaParserLabeled::Primary5Context *ctx) = 0;
  virtual void exitPrimary5(JavaParserLabeled::Primary5Context *ctx) = 0;

  virtual void enterPrimary6(JavaParserLabeled::Primary6Context *ctx) = 0;
  virtual void exitPrimary6(JavaParserLabeled::Primary6Context *ctx) = 0;

  virtual void enterClassType(JavaParserLabeled::ClassTypeContext *ctx) = 0;
  virtual void exitClassType(JavaParserLabeled::ClassTypeContext *ctx) = 0;

  virtual void enterCreator0(JavaParserLabeled::Creator0Context *ctx) = 0;
  virtual void exitCreator0(JavaParserLabeled::Creator0Context *ctx) = 0;

  virtual void enterCreator1(JavaParserLabeled::Creator1Context *ctx) = 0;
  virtual void exitCreator1(JavaParserLabeled::Creator1Context *ctx) = 0;

  virtual void enterCreatedName0(JavaParserLabeled::CreatedName0Context *ctx) = 0;
  virtual void exitCreatedName0(JavaParserLabeled::CreatedName0Context *ctx) = 0;

  virtual void enterCreatedName1(JavaParserLabeled::CreatedName1Context *ctx) = 0;
  virtual void exitCreatedName1(JavaParserLabeled::CreatedName1Context *ctx) = 0;

  virtual void enterInnerCreator(JavaParserLabeled::InnerCreatorContext *ctx) = 0;
  virtual void exitInnerCreator(JavaParserLabeled::InnerCreatorContext *ctx) = 0;

  virtual void enterArrayCreatorRest(JavaParserLabeled::ArrayCreatorRestContext *ctx) = 0;
  virtual void exitArrayCreatorRest(JavaParserLabeled::ArrayCreatorRestContext *ctx) = 0;

  virtual void enterClassCreatorRest(JavaParserLabeled::ClassCreatorRestContext *ctx) = 0;
  virtual void exitClassCreatorRest(JavaParserLabeled::ClassCreatorRestContext *ctx) = 0;

  virtual void enterExplicitGenericInvocation(JavaParserLabeled::ExplicitGenericInvocationContext *ctx) = 0;
  virtual void exitExplicitGenericInvocation(JavaParserLabeled::ExplicitGenericInvocationContext *ctx) = 0;

  virtual void enterTypeArgumentsOrDiamond(JavaParserLabeled::TypeArgumentsOrDiamondContext *ctx) = 0;
  virtual void exitTypeArgumentsOrDiamond(JavaParserLabeled::TypeArgumentsOrDiamondContext *ctx) = 0;

  virtual void enterNonWildcardTypeArgumentsOrDiamond(JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext *ctx) = 0;
  virtual void exitNonWildcardTypeArgumentsOrDiamond(JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext *ctx) = 0;

  virtual void enterNonWildcardTypeArguments(JavaParserLabeled::NonWildcardTypeArgumentsContext *ctx) = 0;
  virtual void exitNonWildcardTypeArguments(JavaParserLabeled::NonWildcardTypeArgumentsContext *ctx) = 0;

  virtual void enterTypeList(JavaParserLabeled::TypeListContext *ctx) = 0;
  virtual void exitTypeList(JavaParserLabeled::TypeListContext *ctx) = 0;

  virtual void enterTypeType(JavaParserLabeled::TypeTypeContext *ctx) = 0;
  virtual void exitTypeType(JavaParserLabeled::TypeTypeContext *ctx) = 0;

  virtual void enterPrimitiveType(JavaParserLabeled::PrimitiveTypeContext *ctx) = 0;
  virtual void exitPrimitiveType(JavaParserLabeled::PrimitiveTypeContext *ctx) = 0;

  virtual void enterTypeArguments(JavaParserLabeled::TypeArgumentsContext *ctx) = 0;
  virtual void exitTypeArguments(JavaParserLabeled::TypeArgumentsContext *ctx) = 0;

  virtual void enterSuperSuffix0(JavaParserLabeled::SuperSuffix0Context *ctx) = 0;
  virtual void exitSuperSuffix0(JavaParserLabeled::SuperSuffix0Context *ctx) = 0;

  virtual void enterSuperSuffix1(JavaParserLabeled::SuperSuffix1Context *ctx) = 0;
  virtual void exitSuperSuffix1(JavaParserLabeled::SuperSuffix1Context *ctx) = 0;

  virtual void enterExplicitGenericInvocationSuffix0(JavaParserLabeled::ExplicitGenericInvocationSuffix0Context *ctx) = 0;
  virtual void exitExplicitGenericInvocationSuffix0(JavaParserLabeled::ExplicitGenericInvocationSuffix0Context *ctx) = 0;

  virtual void enterExplicitGenericInvocationSuffix1(JavaParserLabeled::ExplicitGenericInvocationSuffix1Context *ctx) = 0;
  virtual void exitExplicitGenericInvocationSuffix1(JavaParserLabeled::ExplicitGenericInvocationSuffix1Context *ctx) = 0;

  virtual void enterArguments(JavaParserLabeled::ArgumentsContext *ctx) = 0;
  virtual void exitArguments(JavaParserLabeled::ArgumentsContext *ctx) = 0;


};

