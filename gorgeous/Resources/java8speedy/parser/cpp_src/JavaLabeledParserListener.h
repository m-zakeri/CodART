
// Generated from JavaLabeledParser.g4 by ANTLR 4.9.3

#pragma once


#include "antlr4-runtime.h"
#include "JavaLabeledParser.h"


/**
 * This interface defines an abstract listener for a parse tree produced by JavaLabeledParser.
 */
class  JavaLabeledParserListener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterCompilationUnit(JavaLabeledParser::CompilationUnitContext *ctx) = 0;
  virtual void exitCompilationUnit(JavaLabeledParser::CompilationUnitContext *ctx) = 0;

  virtual void enterPackageDeclaration(JavaLabeledParser::PackageDeclarationContext *ctx) = 0;
  virtual void exitPackageDeclaration(JavaLabeledParser::PackageDeclarationContext *ctx) = 0;

  virtual void enterImportDeclaration(JavaLabeledParser::ImportDeclarationContext *ctx) = 0;
  virtual void exitImportDeclaration(JavaLabeledParser::ImportDeclarationContext *ctx) = 0;

  virtual void enterTypeDeclaration(JavaLabeledParser::TypeDeclarationContext *ctx) = 0;
  virtual void exitTypeDeclaration(JavaLabeledParser::TypeDeclarationContext *ctx) = 0;

  virtual void enterModifier(JavaLabeledParser::ModifierContext *ctx) = 0;
  virtual void exitModifier(JavaLabeledParser::ModifierContext *ctx) = 0;

  virtual void enterClassOrInterfaceModifier(JavaLabeledParser::ClassOrInterfaceModifierContext *ctx) = 0;
  virtual void exitClassOrInterfaceModifier(JavaLabeledParser::ClassOrInterfaceModifierContext *ctx) = 0;

  virtual void enterVariableModifier(JavaLabeledParser::VariableModifierContext *ctx) = 0;
  virtual void exitVariableModifier(JavaLabeledParser::VariableModifierContext *ctx) = 0;

  virtual void enterClassDeclaration(JavaLabeledParser::ClassDeclarationContext *ctx) = 0;
  virtual void exitClassDeclaration(JavaLabeledParser::ClassDeclarationContext *ctx) = 0;

  virtual void enterTypeParameters(JavaLabeledParser::TypeParametersContext *ctx) = 0;
  virtual void exitTypeParameters(JavaLabeledParser::TypeParametersContext *ctx) = 0;

  virtual void enterTypeParameter(JavaLabeledParser::TypeParameterContext *ctx) = 0;
  virtual void exitTypeParameter(JavaLabeledParser::TypeParameterContext *ctx) = 0;

  virtual void enterTypeBound(JavaLabeledParser::TypeBoundContext *ctx) = 0;
  virtual void exitTypeBound(JavaLabeledParser::TypeBoundContext *ctx) = 0;

  virtual void enterEnumDeclaration(JavaLabeledParser::EnumDeclarationContext *ctx) = 0;
  virtual void exitEnumDeclaration(JavaLabeledParser::EnumDeclarationContext *ctx) = 0;

  virtual void enterEnumConstants(JavaLabeledParser::EnumConstantsContext *ctx) = 0;
  virtual void exitEnumConstants(JavaLabeledParser::EnumConstantsContext *ctx) = 0;

  virtual void enterEnumConstant(JavaLabeledParser::EnumConstantContext *ctx) = 0;
  virtual void exitEnumConstant(JavaLabeledParser::EnumConstantContext *ctx) = 0;

  virtual void enterEnumBodyDeclarations(JavaLabeledParser::EnumBodyDeclarationsContext *ctx) = 0;
  virtual void exitEnumBodyDeclarations(JavaLabeledParser::EnumBodyDeclarationsContext *ctx) = 0;

  virtual void enterInterfaceDeclaration(JavaLabeledParser::InterfaceDeclarationContext *ctx) = 0;
  virtual void exitInterfaceDeclaration(JavaLabeledParser::InterfaceDeclarationContext *ctx) = 0;

  virtual void enterClassBody(JavaLabeledParser::ClassBodyContext *ctx) = 0;
  virtual void exitClassBody(JavaLabeledParser::ClassBodyContext *ctx) = 0;

  virtual void enterInterfaceBody(JavaLabeledParser::InterfaceBodyContext *ctx) = 0;
  virtual void exitInterfaceBody(JavaLabeledParser::InterfaceBodyContext *ctx) = 0;

  virtual void enterClassBodyDeclaration0(JavaLabeledParser::ClassBodyDeclaration0Context *ctx) = 0;
  virtual void exitClassBodyDeclaration0(JavaLabeledParser::ClassBodyDeclaration0Context *ctx) = 0;

  virtual void enterClassBodyDeclaration1(JavaLabeledParser::ClassBodyDeclaration1Context *ctx) = 0;
  virtual void exitClassBodyDeclaration1(JavaLabeledParser::ClassBodyDeclaration1Context *ctx) = 0;

  virtual void enterClassBodyDeclaration2(JavaLabeledParser::ClassBodyDeclaration2Context *ctx) = 0;
  virtual void exitClassBodyDeclaration2(JavaLabeledParser::ClassBodyDeclaration2Context *ctx) = 0;

  virtual void enterMemberDeclaration0(JavaLabeledParser::MemberDeclaration0Context *ctx) = 0;
  virtual void exitMemberDeclaration0(JavaLabeledParser::MemberDeclaration0Context *ctx) = 0;

  virtual void enterMemberDeclaration1(JavaLabeledParser::MemberDeclaration1Context *ctx) = 0;
  virtual void exitMemberDeclaration1(JavaLabeledParser::MemberDeclaration1Context *ctx) = 0;

  virtual void enterMemberDeclaration2(JavaLabeledParser::MemberDeclaration2Context *ctx) = 0;
  virtual void exitMemberDeclaration2(JavaLabeledParser::MemberDeclaration2Context *ctx) = 0;

  virtual void enterMemberDeclaration3(JavaLabeledParser::MemberDeclaration3Context *ctx) = 0;
  virtual void exitMemberDeclaration3(JavaLabeledParser::MemberDeclaration3Context *ctx) = 0;

  virtual void enterMemberDeclaration4(JavaLabeledParser::MemberDeclaration4Context *ctx) = 0;
  virtual void exitMemberDeclaration4(JavaLabeledParser::MemberDeclaration4Context *ctx) = 0;

  virtual void enterMemberDeclaration5(JavaLabeledParser::MemberDeclaration5Context *ctx) = 0;
  virtual void exitMemberDeclaration5(JavaLabeledParser::MemberDeclaration5Context *ctx) = 0;

  virtual void enterMemberDeclaration6(JavaLabeledParser::MemberDeclaration6Context *ctx) = 0;
  virtual void exitMemberDeclaration6(JavaLabeledParser::MemberDeclaration6Context *ctx) = 0;

  virtual void enterMemberDeclaration7(JavaLabeledParser::MemberDeclaration7Context *ctx) = 0;
  virtual void exitMemberDeclaration7(JavaLabeledParser::MemberDeclaration7Context *ctx) = 0;

  virtual void enterMemberDeclaration8(JavaLabeledParser::MemberDeclaration8Context *ctx) = 0;
  virtual void exitMemberDeclaration8(JavaLabeledParser::MemberDeclaration8Context *ctx) = 0;

  virtual void enterMethodDeclaration(JavaLabeledParser::MethodDeclarationContext *ctx) = 0;
  virtual void exitMethodDeclaration(JavaLabeledParser::MethodDeclarationContext *ctx) = 0;

  virtual void enterMethodBody(JavaLabeledParser::MethodBodyContext *ctx) = 0;
  virtual void exitMethodBody(JavaLabeledParser::MethodBodyContext *ctx) = 0;

  virtual void enterTypeTypeOrVoid(JavaLabeledParser::TypeTypeOrVoidContext *ctx) = 0;
  virtual void exitTypeTypeOrVoid(JavaLabeledParser::TypeTypeOrVoidContext *ctx) = 0;

  virtual void enterGenericMethodDeclaration(JavaLabeledParser::GenericMethodDeclarationContext *ctx) = 0;
  virtual void exitGenericMethodDeclaration(JavaLabeledParser::GenericMethodDeclarationContext *ctx) = 0;

  virtual void enterGenericConstructorDeclaration(JavaLabeledParser::GenericConstructorDeclarationContext *ctx) = 0;
  virtual void exitGenericConstructorDeclaration(JavaLabeledParser::GenericConstructorDeclarationContext *ctx) = 0;

  virtual void enterConstructorDeclaration(JavaLabeledParser::ConstructorDeclarationContext *ctx) = 0;
  virtual void exitConstructorDeclaration(JavaLabeledParser::ConstructorDeclarationContext *ctx) = 0;

  virtual void enterFieldDeclaration(JavaLabeledParser::FieldDeclarationContext *ctx) = 0;
  virtual void exitFieldDeclaration(JavaLabeledParser::FieldDeclarationContext *ctx) = 0;

  virtual void enterInterfaceBodyDeclaration(JavaLabeledParser::InterfaceBodyDeclarationContext *ctx) = 0;
  virtual void exitInterfaceBodyDeclaration(JavaLabeledParser::InterfaceBodyDeclarationContext *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration0(JavaLabeledParser::InterfaceMemberDeclaration0Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration0(JavaLabeledParser::InterfaceMemberDeclaration0Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration1(JavaLabeledParser::InterfaceMemberDeclaration1Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration1(JavaLabeledParser::InterfaceMemberDeclaration1Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration2(JavaLabeledParser::InterfaceMemberDeclaration2Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration2(JavaLabeledParser::InterfaceMemberDeclaration2Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration3(JavaLabeledParser::InterfaceMemberDeclaration3Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration3(JavaLabeledParser::InterfaceMemberDeclaration3Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration4(JavaLabeledParser::InterfaceMemberDeclaration4Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration4(JavaLabeledParser::InterfaceMemberDeclaration4Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration5(JavaLabeledParser::InterfaceMemberDeclaration5Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration5(JavaLabeledParser::InterfaceMemberDeclaration5Context *ctx) = 0;

  virtual void enterInterfaceMemberDeclaration6(JavaLabeledParser::InterfaceMemberDeclaration6Context *ctx) = 0;
  virtual void exitInterfaceMemberDeclaration6(JavaLabeledParser::InterfaceMemberDeclaration6Context *ctx) = 0;

  virtual void enterConstDeclaration(JavaLabeledParser::ConstDeclarationContext *ctx) = 0;
  virtual void exitConstDeclaration(JavaLabeledParser::ConstDeclarationContext *ctx) = 0;

  virtual void enterConstantDeclarator(JavaLabeledParser::ConstantDeclaratorContext *ctx) = 0;
  virtual void exitConstantDeclarator(JavaLabeledParser::ConstantDeclaratorContext *ctx) = 0;

  virtual void enterInterfaceMethodDeclaration(JavaLabeledParser::InterfaceMethodDeclarationContext *ctx) = 0;
  virtual void exitInterfaceMethodDeclaration(JavaLabeledParser::InterfaceMethodDeclarationContext *ctx) = 0;

  virtual void enterInterfaceMethodModifier(JavaLabeledParser::InterfaceMethodModifierContext *ctx) = 0;
  virtual void exitInterfaceMethodModifier(JavaLabeledParser::InterfaceMethodModifierContext *ctx) = 0;

  virtual void enterGenericInterfaceMethodDeclaration(JavaLabeledParser::GenericInterfaceMethodDeclarationContext *ctx) = 0;
  virtual void exitGenericInterfaceMethodDeclaration(JavaLabeledParser::GenericInterfaceMethodDeclarationContext *ctx) = 0;

  virtual void enterVariableDeclarators(JavaLabeledParser::VariableDeclaratorsContext *ctx) = 0;
  virtual void exitVariableDeclarators(JavaLabeledParser::VariableDeclaratorsContext *ctx) = 0;

  virtual void enterVariableDeclarator(JavaLabeledParser::VariableDeclaratorContext *ctx) = 0;
  virtual void exitVariableDeclarator(JavaLabeledParser::VariableDeclaratorContext *ctx) = 0;

  virtual void enterVariableDeclaratorId(JavaLabeledParser::VariableDeclaratorIdContext *ctx) = 0;
  virtual void exitVariableDeclaratorId(JavaLabeledParser::VariableDeclaratorIdContext *ctx) = 0;

  virtual void enterVariableInitializer0(JavaLabeledParser::VariableInitializer0Context *ctx) = 0;
  virtual void exitVariableInitializer0(JavaLabeledParser::VariableInitializer0Context *ctx) = 0;

  virtual void enterVariableInitializer1(JavaLabeledParser::VariableInitializer1Context *ctx) = 0;
  virtual void exitVariableInitializer1(JavaLabeledParser::VariableInitializer1Context *ctx) = 0;

  virtual void enterArrayInitializer(JavaLabeledParser::ArrayInitializerContext *ctx) = 0;
  virtual void exitArrayInitializer(JavaLabeledParser::ArrayInitializerContext *ctx) = 0;

  virtual void enterClassOrInterfaceType(JavaLabeledParser::ClassOrInterfaceTypeContext *ctx) = 0;
  virtual void exitClassOrInterfaceType(JavaLabeledParser::ClassOrInterfaceTypeContext *ctx) = 0;

  virtual void enterTypeArgument0(JavaLabeledParser::TypeArgument0Context *ctx) = 0;
  virtual void exitTypeArgument0(JavaLabeledParser::TypeArgument0Context *ctx) = 0;

  virtual void enterQualifiedNameList(JavaLabeledParser::QualifiedNameListContext *ctx) = 0;
  virtual void exitQualifiedNameList(JavaLabeledParser::QualifiedNameListContext *ctx) = 0;

  virtual void enterFormalParameters(JavaLabeledParser::FormalParametersContext *ctx) = 0;
  virtual void exitFormalParameters(JavaLabeledParser::FormalParametersContext *ctx) = 0;

  virtual void enterFormalParameterList0(JavaLabeledParser::FormalParameterList0Context *ctx) = 0;
  virtual void exitFormalParameterList0(JavaLabeledParser::FormalParameterList0Context *ctx) = 0;

  virtual void enterFormalParameterList1(JavaLabeledParser::FormalParameterList1Context *ctx) = 0;
  virtual void exitFormalParameterList1(JavaLabeledParser::FormalParameterList1Context *ctx) = 0;

  virtual void enterFormalParameter(JavaLabeledParser::FormalParameterContext *ctx) = 0;
  virtual void exitFormalParameter(JavaLabeledParser::FormalParameterContext *ctx) = 0;

  virtual void enterLastFormalParameter(JavaLabeledParser::LastFormalParameterContext *ctx) = 0;
  virtual void exitLastFormalParameter(JavaLabeledParser::LastFormalParameterContext *ctx) = 0;

  virtual void enterQualifiedName(JavaLabeledParser::QualifiedNameContext *ctx) = 0;
  virtual void exitQualifiedName(JavaLabeledParser::QualifiedNameContext *ctx) = 0;

  virtual void enterLiteral0(JavaLabeledParser::Literal0Context *ctx) = 0;
  virtual void exitLiteral0(JavaLabeledParser::Literal0Context *ctx) = 0;

  virtual void enterLiteral1(JavaLabeledParser::Literal1Context *ctx) = 0;
  virtual void exitLiteral1(JavaLabeledParser::Literal1Context *ctx) = 0;

  virtual void enterLiteral2(JavaLabeledParser::Literal2Context *ctx) = 0;
  virtual void exitLiteral2(JavaLabeledParser::Literal2Context *ctx) = 0;

  virtual void enterLiteral3(JavaLabeledParser::Literal3Context *ctx) = 0;
  virtual void exitLiteral3(JavaLabeledParser::Literal3Context *ctx) = 0;

  virtual void enterLiteral4(JavaLabeledParser::Literal4Context *ctx) = 0;
  virtual void exitLiteral4(JavaLabeledParser::Literal4Context *ctx) = 0;

  virtual void enterLiteral5(JavaLabeledParser::Literal5Context *ctx) = 0;
  virtual void exitLiteral5(JavaLabeledParser::Literal5Context *ctx) = 0;

  virtual void enterIntegerLiteral(JavaLabeledParser::IntegerLiteralContext *ctx) = 0;
  virtual void exitIntegerLiteral(JavaLabeledParser::IntegerLiteralContext *ctx) = 0;

  virtual void enterFloatLiteral(JavaLabeledParser::FloatLiteralContext *ctx) = 0;
  virtual void exitFloatLiteral(JavaLabeledParser::FloatLiteralContext *ctx) = 0;

  virtual void enterAltAnnotationQualifiedName(JavaLabeledParser::AltAnnotationQualifiedNameContext *ctx) = 0;
  virtual void exitAltAnnotationQualifiedName(JavaLabeledParser::AltAnnotationQualifiedNameContext *ctx) = 0;

  virtual void enterAnnotation(JavaLabeledParser::AnnotationContext *ctx) = 0;
  virtual void exitAnnotation(JavaLabeledParser::AnnotationContext *ctx) = 0;

  virtual void enterElementValuePairs(JavaLabeledParser::ElementValuePairsContext *ctx) = 0;
  virtual void exitElementValuePairs(JavaLabeledParser::ElementValuePairsContext *ctx) = 0;

  virtual void enterElementValuePair(JavaLabeledParser::ElementValuePairContext *ctx) = 0;
  virtual void exitElementValuePair(JavaLabeledParser::ElementValuePairContext *ctx) = 0;

  virtual void enterElementValue0(JavaLabeledParser::ElementValue0Context *ctx) = 0;
  virtual void exitElementValue0(JavaLabeledParser::ElementValue0Context *ctx) = 0;

  virtual void enterElementValue1(JavaLabeledParser::ElementValue1Context *ctx) = 0;
  virtual void exitElementValue1(JavaLabeledParser::ElementValue1Context *ctx) = 0;

  virtual void enterElementValue2(JavaLabeledParser::ElementValue2Context *ctx) = 0;
  virtual void exitElementValue2(JavaLabeledParser::ElementValue2Context *ctx) = 0;

  virtual void enterElementValueArrayInitializer(JavaLabeledParser::ElementValueArrayInitializerContext *ctx) = 0;
  virtual void exitElementValueArrayInitializer(JavaLabeledParser::ElementValueArrayInitializerContext *ctx) = 0;

  virtual void enterAnnotationTypeDeclaration(JavaLabeledParser::AnnotationTypeDeclarationContext *ctx) = 0;
  virtual void exitAnnotationTypeDeclaration(JavaLabeledParser::AnnotationTypeDeclarationContext *ctx) = 0;

  virtual void enterAnnotationTypeBody(JavaLabeledParser::AnnotationTypeBodyContext *ctx) = 0;
  virtual void exitAnnotationTypeBody(JavaLabeledParser::AnnotationTypeBodyContext *ctx) = 0;

  virtual void enterAnnotationTypeElementDeclaration(JavaLabeledParser::AnnotationTypeElementDeclarationContext *ctx) = 0;
  virtual void exitAnnotationTypeElementDeclaration(JavaLabeledParser::AnnotationTypeElementDeclarationContext *ctx) = 0;

  virtual void enterAnnotationTypeElementRest0(JavaLabeledParser::AnnotationTypeElementRest0Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest0(JavaLabeledParser::AnnotationTypeElementRest0Context *ctx) = 0;

  virtual void enterAnnotationTypeElementRest1(JavaLabeledParser::AnnotationTypeElementRest1Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest1(JavaLabeledParser::AnnotationTypeElementRest1Context *ctx) = 0;

  virtual void enterAnnotationTypeElementRest2(JavaLabeledParser::AnnotationTypeElementRest2Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest2(JavaLabeledParser::AnnotationTypeElementRest2Context *ctx) = 0;

  virtual void enterAnnotationTypeElementRest3(JavaLabeledParser::AnnotationTypeElementRest3Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest3(JavaLabeledParser::AnnotationTypeElementRest3Context *ctx) = 0;

  virtual void enterAnnotationTypeElementRest4(JavaLabeledParser::AnnotationTypeElementRest4Context *ctx) = 0;
  virtual void exitAnnotationTypeElementRest4(JavaLabeledParser::AnnotationTypeElementRest4Context *ctx) = 0;

  virtual void enterAnnotationMethodOrConstantRest0(JavaLabeledParser::AnnotationMethodOrConstantRest0Context *ctx) = 0;
  virtual void exitAnnotationMethodOrConstantRest0(JavaLabeledParser::AnnotationMethodOrConstantRest0Context *ctx) = 0;

  virtual void enterAnnotationMethodOrConstantRest1(JavaLabeledParser::AnnotationMethodOrConstantRest1Context *ctx) = 0;
  virtual void exitAnnotationMethodOrConstantRest1(JavaLabeledParser::AnnotationMethodOrConstantRest1Context *ctx) = 0;

  virtual void enterAnnotationMethodRest(JavaLabeledParser::AnnotationMethodRestContext *ctx) = 0;
  virtual void exitAnnotationMethodRest(JavaLabeledParser::AnnotationMethodRestContext *ctx) = 0;

  virtual void enterAnnotationConstantRest(JavaLabeledParser::AnnotationConstantRestContext *ctx) = 0;
  virtual void exitAnnotationConstantRest(JavaLabeledParser::AnnotationConstantRestContext *ctx) = 0;

  virtual void enterDefaultValue(JavaLabeledParser::DefaultValueContext *ctx) = 0;
  virtual void exitDefaultValue(JavaLabeledParser::DefaultValueContext *ctx) = 0;

  virtual void enterBlock(JavaLabeledParser::BlockContext *ctx) = 0;
  virtual void exitBlock(JavaLabeledParser::BlockContext *ctx) = 0;

  virtual void enterBlockStatement0(JavaLabeledParser::BlockStatement0Context *ctx) = 0;
  virtual void exitBlockStatement0(JavaLabeledParser::BlockStatement0Context *ctx) = 0;

  virtual void enterBlockStatement1(JavaLabeledParser::BlockStatement1Context *ctx) = 0;
  virtual void exitBlockStatement1(JavaLabeledParser::BlockStatement1Context *ctx) = 0;

  virtual void enterBlockStatement2(JavaLabeledParser::BlockStatement2Context *ctx) = 0;
  virtual void exitBlockStatement2(JavaLabeledParser::BlockStatement2Context *ctx) = 0;

  virtual void enterLocalVariableDeclaration(JavaLabeledParser::LocalVariableDeclarationContext *ctx) = 0;
  virtual void exitLocalVariableDeclaration(JavaLabeledParser::LocalVariableDeclarationContext *ctx) = 0;

  virtual void enterLocalTypeDeclaration(JavaLabeledParser::LocalTypeDeclarationContext *ctx) = 0;
  virtual void exitLocalTypeDeclaration(JavaLabeledParser::LocalTypeDeclarationContext *ctx) = 0;

  virtual void enterStatement0(JavaLabeledParser::Statement0Context *ctx) = 0;
  virtual void exitStatement0(JavaLabeledParser::Statement0Context *ctx) = 0;

  virtual void enterStatement1(JavaLabeledParser::Statement1Context *ctx) = 0;
  virtual void exitStatement1(JavaLabeledParser::Statement1Context *ctx) = 0;

  virtual void enterStatement2(JavaLabeledParser::Statement2Context *ctx) = 0;
  virtual void exitStatement2(JavaLabeledParser::Statement2Context *ctx) = 0;

  virtual void enterStatement3(JavaLabeledParser::Statement3Context *ctx) = 0;
  virtual void exitStatement3(JavaLabeledParser::Statement3Context *ctx) = 0;

  virtual void enterStatement4(JavaLabeledParser::Statement4Context *ctx) = 0;
  virtual void exitStatement4(JavaLabeledParser::Statement4Context *ctx) = 0;

  virtual void enterStatement5(JavaLabeledParser::Statement5Context *ctx) = 0;
  virtual void exitStatement5(JavaLabeledParser::Statement5Context *ctx) = 0;

  virtual void enterStatement6(JavaLabeledParser::Statement6Context *ctx) = 0;
  virtual void exitStatement6(JavaLabeledParser::Statement6Context *ctx) = 0;

  virtual void enterStatement7(JavaLabeledParser::Statement7Context *ctx) = 0;
  virtual void exitStatement7(JavaLabeledParser::Statement7Context *ctx) = 0;

  virtual void enterStatement8(JavaLabeledParser::Statement8Context *ctx) = 0;
  virtual void exitStatement8(JavaLabeledParser::Statement8Context *ctx) = 0;

  virtual void enterStatement9(JavaLabeledParser::Statement9Context *ctx) = 0;
  virtual void exitStatement9(JavaLabeledParser::Statement9Context *ctx) = 0;

  virtual void enterStatement10(JavaLabeledParser::Statement10Context *ctx) = 0;
  virtual void exitStatement10(JavaLabeledParser::Statement10Context *ctx) = 0;

  virtual void enterStatement11(JavaLabeledParser::Statement11Context *ctx) = 0;
  virtual void exitStatement11(JavaLabeledParser::Statement11Context *ctx) = 0;

  virtual void enterStatement12(JavaLabeledParser::Statement12Context *ctx) = 0;
  virtual void exitStatement12(JavaLabeledParser::Statement12Context *ctx) = 0;

  virtual void enterStatement13(JavaLabeledParser::Statement13Context *ctx) = 0;
  virtual void exitStatement13(JavaLabeledParser::Statement13Context *ctx) = 0;

  virtual void enterStatement14(JavaLabeledParser::Statement14Context *ctx) = 0;
  virtual void exitStatement14(JavaLabeledParser::Statement14Context *ctx) = 0;

  virtual void enterStatement15(JavaLabeledParser::Statement15Context *ctx) = 0;
  virtual void exitStatement15(JavaLabeledParser::Statement15Context *ctx) = 0;

  virtual void enterStatement16(JavaLabeledParser::Statement16Context *ctx) = 0;
  virtual void exitStatement16(JavaLabeledParser::Statement16Context *ctx) = 0;

  virtual void enterCatchClause(JavaLabeledParser::CatchClauseContext *ctx) = 0;
  virtual void exitCatchClause(JavaLabeledParser::CatchClauseContext *ctx) = 0;

  virtual void enterCatchType(JavaLabeledParser::CatchTypeContext *ctx) = 0;
  virtual void exitCatchType(JavaLabeledParser::CatchTypeContext *ctx) = 0;

  virtual void enterFinallyBlock(JavaLabeledParser::FinallyBlockContext *ctx) = 0;
  virtual void exitFinallyBlock(JavaLabeledParser::FinallyBlockContext *ctx) = 0;

  virtual void enterResourceSpecification(JavaLabeledParser::ResourceSpecificationContext *ctx) = 0;
  virtual void exitResourceSpecification(JavaLabeledParser::ResourceSpecificationContext *ctx) = 0;

  virtual void enterResources(JavaLabeledParser::ResourcesContext *ctx) = 0;
  virtual void exitResources(JavaLabeledParser::ResourcesContext *ctx) = 0;

  virtual void enterResource(JavaLabeledParser::ResourceContext *ctx) = 0;
  virtual void exitResource(JavaLabeledParser::ResourceContext *ctx) = 0;

  virtual void enterSwitchBlockStatementGroup(JavaLabeledParser::SwitchBlockStatementGroupContext *ctx) = 0;
  virtual void exitSwitchBlockStatementGroup(JavaLabeledParser::SwitchBlockStatementGroupContext *ctx) = 0;

  virtual void enterSwitchLabel(JavaLabeledParser::SwitchLabelContext *ctx) = 0;
  virtual void exitSwitchLabel(JavaLabeledParser::SwitchLabelContext *ctx) = 0;

  virtual void enterForControl0(JavaLabeledParser::ForControl0Context *ctx) = 0;
  virtual void exitForControl0(JavaLabeledParser::ForControl0Context *ctx) = 0;

  virtual void enterForControl1(JavaLabeledParser::ForControl1Context *ctx) = 0;
  virtual void exitForControl1(JavaLabeledParser::ForControl1Context *ctx) = 0;

  virtual void enterForInit0(JavaLabeledParser::ForInit0Context *ctx) = 0;
  virtual void exitForInit0(JavaLabeledParser::ForInit0Context *ctx) = 0;

  virtual void enterForInit1(JavaLabeledParser::ForInit1Context *ctx) = 0;
  virtual void exitForInit1(JavaLabeledParser::ForInit1Context *ctx) = 0;

  virtual void enterEnhancedForControl(JavaLabeledParser::EnhancedForControlContext *ctx) = 0;
  virtual void exitEnhancedForControl(JavaLabeledParser::EnhancedForControlContext *ctx) = 0;

  virtual void enterParExpression(JavaLabeledParser::ParExpressionContext *ctx) = 0;
  virtual void exitParExpression(JavaLabeledParser::ParExpressionContext *ctx) = 0;

  virtual void enterExpressionList(JavaLabeledParser::ExpressionListContext *ctx) = 0;
  virtual void exitExpressionList(JavaLabeledParser::ExpressionListContext *ctx) = 0;

  virtual void enterMethodCall0(JavaLabeledParser::MethodCall0Context *ctx) = 0;
  virtual void exitMethodCall0(JavaLabeledParser::MethodCall0Context *ctx) = 0;

  virtual void enterMethodCall1(JavaLabeledParser::MethodCall1Context *ctx) = 0;
  virtual void exitMethodCall1(JavaLabeledParser::MethodCall1Context *ctx) = 0;

  virtual void enterMethodCall2(JavaLabeledParser::MethodCall2Context *ctx) = 0;
  virtual void exitMethodCall2(JavaLabeledParser::MethodCall2Context *ctx) = 0;

  virtual void enterExpression8(JavaLabeledParser::Expression8Context *ctx) = 0;
  virtual void exitExpression8(JavaLabeledParser::Expression8Context *ctx) = 0;

  virtual void enterExpression10(JavaLabeledParser::Expression10Context *ctx) = 0;
  virtual void exitExpression10(JavaLabeledParser::Expression10Context *ctx) = 0;

  virtual void enterExpression9(JavaLabeledParser::Expression9Context *ctx) = 0;
  virtual void exitExpression9(JavaLabeledParser::Expression9Context *ctx) = 0;

  virtual void enterExpression12(JavaLabeledParser::Expression12Context *ctx) = 0;
  virtual void exitExpression12(JavaLabeledParser::Expression12Context *ctx) = 0;

  virtual void enterExpression11(JavaLabeledParser::Expression11Context *ctx) = 0;
  virtual void exitExpression11(JavaLabeledParser::Expression11Context *ctx) = 0;

  virtual void enterExpression14(JavaLabeledParser::Expression14Context *ctx) = 0;
  virtual void exitExpression14(JavaLabeledParser::Expression14Context *ctx) = 0;

  virtual void enterExpression13(JavaLabeledParser::Expression13Context *ctx) = 0;
  virtual void exitExpression13(JavaLabeledParser::Expression13Context *ctx) = 0;

  virtual void enterExpression16(JavaLabeledParser::Expression16Context *ctx) = 0;
  virtual void exitExpression16(JavaLabeledParser::Expression16Context *ctx) = 0;

  virtual void enterExpression15(JavaLabeledParser::Expression15Context *ctx) = 0;
  virtual void exitExpression15(JavaLabeledParser::Expression15Context *ctx) = 0;

  virtual void enterExpression18(JavaLabeledParser::Expression18Context *ctx) = 0;
  virtual void exitExpression18(JavaLabeledParser::Expression18Context *ctx) = 0;

  virtual void enterExpression17(JavaLabeledParser::Expression17Context *ctx) = 0;
  virtual void exitExpression17(JavaLabeledParser::Expression17Context *ctx) = 0;

  virtual void enterExpression19(JavaLabeledParser::Expression19Context *ctx) = 0;
  virtual void exitExpression19(JavaLabeledParser::Expression19Context *ctx) = 0;

  virtual void enterExpression6(JavaLabeledParser::Expression6Context *ctx) = 0;
  virtual void exitExpression6(JavaLabeledParser::Expression6Context *ctx) = 0;

  virtual void enterExpression7(JavaLabeledParser::Expression7Context *ctx) = 0;
  virtual void exitExpression7(JavaLabeledParser::Expression7Context *ctx) = 0;

  virtual void enterExpression4(JavaLabeledParser::Expression4Context *ctx) = 0;
  virtual void exitExpression4(JavaLabeledParser::Expression4Context *ctx) = 0;

  virtual void enterExpression5(JavaLabeledParser::Expression5Context *ctx) = 0;
  virtual void exitExpression5(JavaLabeledParser::Expression5Context *ctx) = 0;

  virtual void enterExpression2(JavaLabeledParser::Expression2Context *ctx) = 0;
  virtual void exitExpression2(JavaLabeledParser::Expression2Context *ctx) = 0;

  virtual void enterExpression3(JavaLabeledParser::Expression3Context *ctx) = 0;
  virtual void exitExpression3(JavaLabeledParser::Expression3Context *ctx) = 0;

  virtual void enterExpression0(JavaLabeledParser::Expression0Context *ctx) = 0;
  virtual void exitExpression0(JavaLabeledParser::Expression0Context *ctx) = 0;

  virtual void enterExpression1(JavaLabeledParser::Expression1Context *ctx) = 0;
  virtual void exitExpression1(JavaLabeledParser::Expression1Context *ctx) = 0;

  virtual void enterExpression21(JavaLabeledParser::Expression21Context *ctx) = 0;
  virtual void exitExpression21(JavaLabeledParser::Expression21Context *ctx) = 0;

  virtual void enterExpression20(JavaLabeledParser::Expression20Context *ctx) = 0;
  virtual void exitExpression20(JavaLabeledParser::Expression20Context *ctx) = 0;

  virtual void enterExpression23(JavaLabeledParser::Expression23Context *ctx) = 0;
  virtual void exitExpression23(JavaLabeledParser::Expression23Context *ctx) = 0;

  virtual void enterExpression22(JavaLabeledParser::Expression22Context *ctx) = 0;
  virtual void exitExpression22(JavaLabeledParser::Expression22Context *ctx) = 0;

  virtual void enterExpression25(JavaLabeledParser::Expression25Context *ctx) = 0;
  virtual void exitExpression25(JavaLabeledParser::Expression25Context *ctx) = 0;

  virtual void enterExpression24(JavaLabeledParser::Expression24Context *ctx) = 0;
  virtual void exitExpression24(JavaLabeledParser::Expression24Context *ctx) = 0;

  virtual void enterLambdaExpression(JavaLabeledParser::LambdaExpressionContext *ctx) = 0;
  virtual void exitLambdaExpression(JavaLabeledParser::LambdaExpressionContext *ctx) = 0;

  virtual void enterLambdaParameters0(JavaLabeledParser::LambdaParameters0Context *ctx) = 0;
  virtual void exitLambdaParameters0(JavaLabeledParser::LambdaParameters0Context *ctx) = 0;

  virtual void enterLambdaParameters1(JavaLabeledParser::LambdaParameters1Context *ctx) = 0;
  virtual void exitLambdaParameters1(JavaLabeledParser::LambdaParameters1Context *ctx) = 0;

  virtual void enterLambdaParameters2(JavaLabeledParser::LambdaParameters2Context *ctx) = 0;
  virtual void exitLambdaParameters2(JavaLabeledParser::LambdaParameters2Context *ctx) = 0;

  virtual void enterLambdaBody0(JavaLabeledParser::LambdaBody0Context *ctx) = 0;
  virtual void exitLambdaBody0(JavaLabeledParser::LambdaBody0Context *ctx) = 0;

  virtual void enterLambdaBody1(JavaLabeledParser::LambdaBody1Context *ctx) = 0;
  virtual void exitLambdaBody1(JavaLabeledParser::LambdaBody1Context *ctx) = 0;

  virtual void enterPrimary0(JavaLabeledParser::Primary0Context *ctx) = 0;
  virtual void exitPrimary0(JavaLabeledParser::Primary0Context *ctx) = 0;

  virtual void enterPrimary1(JavaLabeledParser::Primary1Context *ctx) = 0;
  virtual void exitPrimary1(JavaLabeledParser::Primary1Context *ctx) = 0;

  virtual void enterPrimary2(JavaLabeledParser::Primary2Context *ctx) = 0;
  virtual void exitPrimary2(JavaLabeledParser::Primary2Context *ctx) = 0;

  virtual void enterPrimary3(JavaLabeledParser::Primary3Context *ctx) = 0;
  virtual void exitPrimary3(JavaLabeledParser::Primary3Context *ctx) = 0;

  virtual void enterPrimary4(JavaLabeledParser::Primary4Context *ctx) = 0;
  virtual void exitPrimary4(JavaLabeledParser::Primary4Context *ctx) = 0;

  virtual void enterPrimary5(JavaLabeledParser::Primary5Context *ctx) = 0;
  virtual void exitPrimary5(JavaLabeledParser::Primary5Context *ctx) = 0;

  virtual void enterPrimary6(JavaLabeledParser::Primary6Context *ctx) = 0;
  virtual void exitPrimary6(JavaLabeledParser::Primary6Context *ctx) = 0;

  virtual void enterClassType(JavaLabeledParser::ClassTypeContext *ctx) = 0;
  virtual void exitClassType(JavaLabeledParser::ClassTypeContext *ctx) = 0;

  virtual void enterCreator0(JavaLabeledParser::Creator0Context *ctx) = 0;
  virtual void exitCreator0(JavaLabeledParser::Creator0Context *ctx) = 0;

  virtual void enterCreator1(JavaLabeledParser::Creator1Context *ctx) = 0;
  virtual void exitCreator1(JavaLabeledParser::Creator1Context *ctx) = 0;

  virtual void enterCreatedName0(JavaLabeledParser::CreatedName0Context *ctx) = 0;
  virtual void exitCreatedName0(JavaLabeledParser::CreatedName0Context *ctx) = 0;

  virtual void enterCreatedName1(JavaLabeledParser::CreatedName1Context *ctx) = 0;
  virtual void exitCreatedName1(JavaLabeledParser::CreatedName1Context *ctx) = 0;

  virtual void enterInnerCreator(JavaLabeledParser::InnerCreatorContext *ctx) = 0;
  virtual void exitInnerCreator(JavaLabeledParser::InnerCreatorContext *ctx) = 0;

  virtual void enterArrayCreatorRest(JavaLabeledParser::ArrayCreatorRestContext *ctx) = 0;
  virtual void exitArrayCreatorRest(JavaLabeledParser::ArrayCreatorRestContext *ctx) = 0;

  virtual void enterClassCreatorRest(JavaLabeledParser::ClassCreatorRestContext *ctx) = 0;
  virtual void exitClassCreatorRest(JavaLabeledParser::ClassCreatorRestContext *ctx) = 0;

  virtual void enterExplicitGenericInvocation(JavaLabeledParser::ExplicitGenericInvocationContext *ctx) = 0;
  virtual void exitExplicitGenericInvocation(JavaLabeledParser::ExplicitGenericInvocationContext *ctx) = 0;

  virtual void enterTypeArgumentsOrDiamond(JavaLabeledParser::TypeArgumentsOrDiamondContext *ctx) = 0;
  virtual void exitTypeArgumentsOrDiamond(JavaLabeledParser::TypeArgumentsOrDiamondContext *ctx) = 0;

  virtual void enterNonWildcardTypeArgumentsOrDiamond(JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext *ctx) = 0;
  virtual void exitNonWildcardTypeArgumentsOrDiamond(JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext *ctx) = 0;

  virtual void enterNonWildcardTypeArguments(JavaLabeledParser::NonWildcardTypeArgumentsContext *ctx) = 0;
  virtual void exitNonWildcardTypeArguments(JavaLabeledParser::NonWildcardTypeArgumentsContext *ctx) = 0;

  virtual void enterTypeList(JavaLabeledParser::TypeListContext *ctx) = 0;
  virtual void exitTypeList(JavaLabeledParser::TypeListContext *ctx) = 0;

  virtual void enterTypeType(JavaLabeledParser::TypeTypeContext *ctx) = 0;
  virtual void exitTypeType(JavaLabeledParser::TypeTypeContext *ctx) = 0;

  virtual void enterPrimitiveType(JavaLabeledParser::PrimitiveTypeContext *ctx) = 0;
  virtual void exitPrimitiveType(JavaLabeledParser::PrimitiveTypeContext *ctx) = 0;

  virtual void enterTypeArguments(JavaLabeledParser::TypeArgumentsContext *ctx) = 0;
  virtual void exitTypeArguments(JavaLabeledParser::TypeArgumentsContext *ctx) = 0;

  virtual void enterSuperSuffix0(JavaLabeledParser::SuperSuffix0Context *ctx) = 0;
  virtual void exitSuperSuffix0(JavaLabeledParser::SuperSuffix0Context *ctx) = 0;

  virtual void enterSuperSuffix1(JavaLabeledParser::SuperSuffix1Context *ctx) = 0;
  virtual void exitSuperSuffix1(JavaLabeledParser::SuperSuffix1Context *ctx) = 0;

  virtual void enterExplicitGenericInvocationSuffix0(JavaLabeledParser::ExplicitGenericInvocationSuffix0Context *ctx) = 0;
  virtual void exitExplicitGenericInvocationSuffix0(JavaLabeledParser::ExplicitGenericInvocationSuffix0Context *ctx) = 0;

  virtual void enterExplicitGenericInvocationSuffix1(JavaLabeledParser::ExplicitGenericInvocationSuffix1Context *ctx) = 0;
  virtual void exitExplicitGenericInvocationSuffix1(JavaLabeledParser::ExplicitGenericInvocationSuffix1Context *ctx) = 0;

  virtual void enterArguments(JavaLabeledParser::ArgumentsContext *ctx) = 0;
  virtual void exitArguments(JavaLabeledParser::ArgumentsContext *ctx) = 0;


};

