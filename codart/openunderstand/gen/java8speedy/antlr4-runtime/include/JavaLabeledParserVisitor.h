
// Generated from JavaLabeledParser.g4 by ANTLR 4.9.1

#pragma once


#include "antlr4-runtime.h"
#include "JavaLabeledParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by JavaLabeledParser.
 */
class  JavaLabeledParserVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by JavaLabeledParser.
   */
    virtual antlrcpp::Any visitCompilationUnit(JavaLabeledParser::CompilationUnitContext *context) = 0;

    virtual antlrcpp::Any visitPackageDeclaration(JavaLabeledParser::PackageDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitImportDeclaration(JavaLabeledParser::ImportDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitTypeDeclaration(JavaLabeledParser::TypeDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitModifier(JavaLabeledParser::ModifierContext *context) = 0;

    virtual antlrcpp::Any visitClassOrInterfaceModifier(JavaLabeledParser::ClassOrInterfaceModifierContext *context) = 0;

    virtual antlrcpp::Any visitVariableModifier(JavaLabeledParser::VariableModifierContext *context) = 0;

    virtual antlrcpp::Any visitClassDeclaration(JavaLabeledParser::ClassDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitTypeParameters(JavaLabeledParser::TypeParametersContext *context) = 0;

    virtual antlrcpp::Any visitTypeParameter(JavaLabeledParser::TypeParameterContext *context) = 0;

    virtual antlrcpp::Any visitTypeBound(JavaLabeledParser::TypeBoundContext *context) = 0;

    virtual antlrcpp::Any visitEnumDeclaration(JavaLabeledParser::EnumDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitEnumConstants(JavaLabeledParser::EnumConstantsContext *context) = 0;

    virtual antlrcpp::Any visitEnumConstant(JavaLabeledParser::EnumConstantContext *context) = 0;

    virtual antlrcpp::Any visitEnumBodyDeclarations(JavaLabeledParser::EnumBodyDeclarationsContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceDeclaration(JavaLabeledParser::InterfaceDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitClassBody(JavaLabeledParser::ClassBodyContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceBody(JavaLabeledParser::InterfaceBodyContext *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration0(JavaLabeledParser::ClassBodyDeclaration0Context *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration1(JavaLabeledParser::ClassBodyDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration2(JavaLabeledParser::ClassBodyDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration0(JavaLabeledParser::MemberDeclaration0Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration1(JavaLabeledParser::MemberDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration2(JavaLabeledParser::MemberDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration3(JavaLabeledParser::MemberDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration4(JavaLabeledParser::MemberDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration5(JavaLabeledParser::MemberDeclaration5Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration6(JavaLabeledParser::MemberDeclaration6Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration7(JavaLabeledParser::MemberDeclaration7Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration8(JavaLabeledParser::MemberDeclaration8Context *context) = 0;

    virtual antlrcpp::Any visitMethodDeclaration(JavaLabeledParser::MethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitMethodBody(JavaLabeledParser::MethodBodyContext *context) = 0;

    virtual antlrcpp::Any visitTypeTypeOrVoid(JavaLabeledParser::TypeTypeOrVoidContext *context) = 0;

    virtual antlrcpp::Any visitGenericMethodDeclaration(JavaLabeledParser::GenericMethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitGenericConstructorDeclaration(JavaLabeledParser::GenericConstructorDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitConstructorDeclaration(JavaLabeledParser::ConstructorDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitFieldDeclaration(JavaLabeledParser::FieldDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceBodyDeclaration(JavaLabeledParser::InterfaceBodyDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration0(JavaLabeledParser::InterfaceMemberDeclaration0Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration1(JavaLabeledParser::InterfaceMemberDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration2(JavaLabeledParser::InterfaceMemberDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration3(JavaLabeledParser::InterfaceMemberDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration4(JavaLabeledParser::InterfaceMemberDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration5(JavaLabeledParser::InterfaceMemberDeclaration5Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration6(JavaLabeledParser::InterfaceMemberDeclaration6Context *context) = 0;

    virtual antlrcpp::Any visitConstDeclaration(JavaLabeledParser::ConstDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitConstantDeclarator(JavaLabeledParser::ConstantDeclaratorContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMethodDeclaration(JavaLabeledParser::InterfaceMethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMethodModifier(JavaLabeledParser::InterfaceMethodModifierContext *context) = 0;

    virtual antlrcpp::Any visitGenericInterfaceMethodDeclaration(JavaLabeledParser::GenericInterfaceMethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclarators(JavaLabeledParser::VariableDeclaratorsContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclarator(JavaLabeledParser::VariableDeclaratorContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclaratorId(JavaLabeledParser::VariableDeclaratorIdContext *context) = 0;

    virtual antlrcpp::Any visitVariableInitializer0(JavaLabeledParser::VariableInitializer0Context *context) = 0;

    virtual antlrcpp::Any visitVariableInitializer1(JavaLabeledParser::VariableInitializer1Context *context) = 0;

    virtual antlrcpp::Any visitArrayInitializer(JavaLabeledParser::ArrayInitializerContext *context) = 0;

    virtual antlrcpp::Any visitClassOrInterfaceType(JavaLabeledParser::ClassOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitTypeArgument0(JavaLabeledParser::TypeArgument0Context *context) = 0;

    virtual antlrcpp::Any visitQualifiedNameList(JavaLabeledParser::QualifiedNameListContext *context) = 0;

    virtual antlrcpp::Any visitFormalParameters(JavaLabeledParser::FormalParametersContext *context) = 0;

    virtual antlrcpp::Any visitFormalParameterList0(JavaLabeledParser::FormalParameterList0Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameterList1(JavaLabeledParser::FormalParameterList1Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameter(JavaLabeledParser::FormalParameterContext *context) = 0;

    virtual antlrcpp::Any visitLastFormalParameter(JavaLabeledParser::LastFormalParameterContext *context) = 0;

    virtual antlrcpp::Any visitQualifiedName(JavaLabeledParser::QualifiedNameContext *context) = 0;

    virtual antlrcpp::Any visitLiteral0(JavaLabeledParser::Literal0Context *context) = 0;

    virtual antlrcpp::Any visitLiteral1(JavaLabeledParser::Literal1Context *context) = 0;

    virtual antlrcpp::Any visitLiteral2(JavaLabeledParser::Literal2Context *context) = 0;

    virtual antlrcpp::Any visitLiteral3(JavaLabeledParser::Literal3Context *context) = 0;

    virtual antlrcpp::Any visitLiteral4(JavaLabeledParser::Literal4Context *context) = 0;

    virtual antlrcpp::Any visitLiteral5(JavaLabeledParser::Literal5Context *context) = 0;

    virtual antlrcpp::Any visitIntegerLiteral(JavaLabeledParser::IntegerLiteralContext *context) = 0;

    virtual antlrcpp::Any visitFloatLiteral(JavaLabeledParser::FloatLiteralContext *context) = 0;

    virtual antlrcpp::Any visitAltAnnotationQualifiedName(JavaLabeledParser::AltAnnotationQualifiedNameContext *context) = 0;

    virtual antlrcpp::Any visitAnnotation(JavaLabeledParser::AnnotationContext *context) = 0;

    virtual antlrcpp::Any visitElementValuePairs(JavaLabeledParser::ElementValuePairsContext *context) = 0;

    virtual antlrcpp::Any visitElementValuePair(JavaLabeledParser::ElementValuePairContext *context) = 0;

    virtual antlrcpp::Any visitElementValue0(JavaLabeledParser::ElementValue0Context *context) = 0;

    virtual antlrcpp::Any visitElementValue1(JavaLabeledParser::ElementValue1Context *context) = 0;

    virtual antlrcpp::Any visitElementValue2(JavaLabeledParser::ElementValue2Context *context) = 0;

    virtual antlrcpp::Any visitElementValueArrayInitializer(JavaLabeledParser::ElementValueArrayInitializerContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeDeclaration(JavaLabeledParser::AnnotationTypeDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeBody(JavaLabeledParser::AnnotationTypeBodyContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementDeclaration(JavaLabeledParser::AnnotationTypeElementDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest0(JavaLabeledParser::AnnotationTypeElementRest0Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest1(JavaLabeledParser::AnnotationTypeElementRest1Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest2(JavaLabeledParser::AnnotationTypeElementRest2Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest3(JavaLabeledParser::AnnotationTypeElementRest3Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest4(JavaLabeledParser::AnnotationTypeElementRest4Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationMethodOrConstantRest0(JavaLabeledParser::AnnotationMethodOrConstantRest0Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationMethodOrConstantRest1(JavaLabeledParser::AnnotationMethodOrConstantRest1Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationMethodRest(JavaLabeledParser::AnnotationMethodRestContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationConstantRest(JavaLabeledParser::AnnotationConstantRestContext *context) = 0;

    virtual antlrcpp::Any visitDefaultValue(JavaLabeledParser::DefaultValueContext *context) = 0;

    virtual antlrcpp::Any visitBlock(JavaLabeledParser::BlockContext *context) = 0;

    virtual antlrcpp::Any visitBlockStatement0(JavaLabeledParser::BlockStatement0Context *context) = 0;

    virtual antlrcpp::Any visitBlockStatement1(JavaLabeledParser::BlockStatement1Context *context) = 0;

    virtual antlrcpp::Any visitBlockStatement2(JavaLabeledParser::BlockStatement2Context *context) = 0;

    virtual antlrcpp::Any visitLocalVariableDeclaration(JavaLabeledParser::LocalVariableDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitLocalTypeDeclaration(JavaLabeledParser::LocalTypeDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitStatement0(JavaLabeledParser::Statement0Context *context) = 0;

    virtual antlrcpp::Any visitStatement1(JavaLabeledParser::Statement1Context *context) = 0;

    virtual antlrcpp::Any visitStatement2(JavaLabeledParser::Statement2Context *context) = 0;

    virtual antlrcpp::Any visitStatement3(JavaLabeledParser::Statement3Context *context) = 0;

    virtual antlrcpp::Any visitStatement4(JavaLabeledParser::Statement4Context *context) = 0;

    virtual antlrcpp::Any visitStatement5(JavaLabeledParser::Statement5Context *context) = 0;

    virtual antlrcpp::Any visitStatement6(JavaLabeledParser::Statement6Context *context) = 0;

    virtual antlrcpp::Any visitStatement7(JavaLabeledParser::Statement7Context *context) = 0;

    virtual antlrcpp::Any visitStatement8(JavaLabeledParser::Statement8Context *context) = 0;

    virtual antlrcpp::Any visitStatement9(JavaLabeledParser::Statement9Context *context) = 0;

    virtual antlrcpp::Any visitStatement10(JavaLabeledParser::Statement10Context *context) = 0;

    virtual antlrcpp::Any visitStatement11(JavaLabeledParser::Statement11Context *context) = 0;

    virtual antlrcpp::Any visitStatement12(JavaLabeledParser::Statement12Context *context) = 0;

    virtual antlrcpp::Any visitStatement13(JavaLabeledParser::Statement13Context *context) = 0;

    virtual antlrcpp::Any visitStatement14(JavaLabeledParser::Statement14Context *context) = 0;

    virtual antlrcpp::Any visitStatement15(JavaLabeledParser::Statement15Context *context) = 0;

    virtual antlrcpp::Any visitStatement16(JavaLabeledParser::Statement16Context *context) = 0;

    virtual antlrcpp::Any visitCatchClause(JavaLabeledParser::CatchClauseContext *context) = 0;

    virtual antlrcpp::Any visitCatchType(JavaLabeledParser::CatchTypeContext *context) = 0;

    virtual antlrcpp::Any visitFinallyBlock(JavaLabeledParser::FinallyBlockContext *context) = 0;

    virtual antlrcpp::Any visitResourceSpecification(JavaLabeledParser::ResourceSpecificationContext *context) = 0;

    virtual antlrcpp::Any visitResources(JavaLabeledParser::ResourcesContext *context) = 0;

    virtual antlrcpp::Any visitResource(JavaLabeledParser::ResourceContext *context) = 0;

    virtual antlrcpp::Any visitSwitchBlockStatementGroup(JavaLabeledParser::SwitchBlockStatementGroupContext *context) = 0;

    virtual antlrcpp::Any visitSwitchLabel(JavaLabeledParser::SwitchLabelContext *context) = 0;

    virtual antlrcpp::Any visitForControl0(JavaLabeledParser::ForControl0Context *context) = 0;

    virtual antlrcpp::Any visitForControl1(JavaLabeledParser::ForControl1Context *context) = 0;

    virtual antlrcpp::Any visitForInit0(JavaLabeledParser::ForInit0Context *context) = 0;

    virtual antlrcpp::Any visitForInit1(JavaLabeledParser::ForInit1Context *context) = 0;

    virtual antlrcpp::Any visitEnhancedForControl(JavaLabeledParser::EnhancedForControlContext *context) = 0;

    virtual antlrcpp::Any visitParExpression(JavaLabeledParser::ParExpressionContext *context) = 0;

    virtual antlrcpp::Any visitExpressionList(JavaLabeledParser::ExpressionListContext *context) = 0;

    virtual antlrcpp::Any visitMethodCall0(JavaLabeledParser::MethodCall0Context *context) = 0;

    virtual antlrcpp::Any visitMethodCall1(JavaLabeledParser::MethodCall1Context *context) = 0;

    virtual antlrcpp::Any visitMethodCall2(JavaLabeledParser::MethodCall2Context *context) = 0;

    virtual antlrcpp::Any visitExpression8(JavaLabeledParser::Expression8Context *context) = 0;

    virtual antlrcpp::Any visitExpression10(JavaLabeledParser::Expression10Context *context) = 0;

    virtual antlrcpp::Any visitExpression9(JavaLabeledParser::Expression9Context *context) = 0;

    virtual antlrcpp::Any visitExpression12(JavaLabeledParser::Expression12Context *context) = 0;

    virtual antlrcpp::Any visitExpression11(JavaLabeledParser::Expression11Context *context) = 0;

    virtual antlrcpp::Any visitExpression14(JavaLabeledParser::Expression14Context *context) = 0;

    virtual antlrcpp::Any visitExpression13(JavaLabeledParser::Expression13Context *context) = 0;

    virtual antlrcpp::Any visitExpression16(JavaLabeledParser::Expression16Context *context) = 0;

    virtual antlrcpp::Any visitExpression15(JavaLabeledParser::Expression15Context *context) = 0;

    virtual antlrcpp::Any visitExpression18(JavaLabeledParser::Expression18Context *context) = 0;

    virtual antlrcpp::Any visitExpression17(JavaLabeledParser::Expression17Context *context) = 0;

    virtual antlrcpp::Any visitExpression19(JavaLabeledParser::Expression19Context *context) = 0;

    virtual antlrcpp::Any visitExpression6(JavaLabeledParser::Expression6Context *context) = 0;

    virtual antlrcpp::Any visitExpression7(JavaLabeledParser::Expression7Context *context) = 0;

    virtual antlrcpp::Any visitExpression4(JavaLabeledParser::Expression4Context *context) = 0;

    virtual antlrcpp::Any visitExpression5(JavaLabeledParser::Expression5Context *context) = 0;

    virtual antlrcpp::Any visitExpression2(JavaLabeledParser::Expression2Context *context) = 0;

    virtual antlrcpp::Any visitExpression3(JavaLabeledParser::Expression3Context *context) = 0;

    virtual antlrcpp::Any visitExpression0(JavaLabeledParser::Expression0Context *context) = 0;

    virtual antlrcpp::Any visitExpression1(JavaLabeledParser::Expression1Context *context) = 0;

    virtual antlrcpp::Any visitExpression21(JavaLabeledParser::Expression21Context *context) = 0;

    virtual antlrcpp::Any visitExpression20(JavaLabeledParser::Expression20Context *context) = 0;

    virtual antlrcpp::Any visitExpression23(JavaLabeledParser::Expression23Context *context) = 0;

    virtual antlrcpp::Any visitExpression22(JavaLabeledParser::Expression22Context *context) = 0;

    virtual antlrcpp::Any visitExpression25(JavaLabeledParser::Expression25Context *context) = 0;

    virtual antlrcpp::Any visitExpression24(JavaLabeledParser::Expression24Context *context) = 0;

    virtual antlrcpp::Any visitLambdaExpression(JavaLabeledParser::LambdaExpressionContext *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters0(JavaLabeledParser::LambdaParameters0Context *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters1(JavaLabeledParser::LambdaParameters1Context *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters2(JavaLabeledParser::LambdaParameters2Context *context) = 0;

    virtual antlrcpp::Any visitLambdaBody0(JavaLabeledParser::LambdaBody0Context *context) = 0;

    virtual antlrcpp::Any visitLambdaBody1(JavaLabeledParser::LambdaBody1Context *context) = 0;

    virtual antlrcpp::Any visitPrimary0(JavaLabeledParser::Primary0Context *context) = 0;

    virtual antlrcpp::Any visitPrimary1(JavaLabeledParser::Primary1Context *context) = 0;

    virtual antlrcpp::Any visitPrimary2(JavaLabeledParser::Primary2Context *context) = 0;

    virtual antlrcpp::Any visitPrimary3(JavaLabeledParser::Primary3Context *context) = 0;

    virtual antlrcpp::Any visitPrimary4(JavaLabeledParser::Primary4Context *context) = 0;

    virtual antlrcpp::Any visitPrimary5(JavaLabeledParser::Primary5Context *context) = 0;

    virtual antlrcpp::Any visitPrimary6(JavaLabeledParser::Primary6Context *context) = 0;

    virtual antlrcpp::Any visitClassType(JavaLabeledParser::ClassTypeContext *context) = 0;

    virtual antlrcpp::Any visitCreator0(JavaLabeledParser::Creator0Context *context) = 0;

    virtual antlrcpp::Any visitCreator1(JavaLabeledParser::Creator1Context *context) = 0;

    virtual antlrcpp::Any visitCreatedName0(JavaLabeledParser::CreatedName0Context *context) = 0;

    virtual antlrcpp::Any visitCreatedName1(JavaLabeledParser::CreatedName1Context *context) = 0;

    virtual antlrcpp::Any visitInnerCreator(JavaLabeledParser::InnerCreatorContext *context) = 0;

    virtual antlrcpp::Any visitArrayCreatorRest(JavaLabeledParser::ArrayCreatorRestContext *context) = 0;

    virtual antlrcpp::Any visitClassCreatorRest(JavaLabeledParser::ClassCreatorRestContext *context) = 0;

    virtual antlrcpp::Any visitExplicitGenericInvocation(JavaLabeledParser::ExplicitGenericInvocationContext *context) = 0;

    virtual antlrcpp::Any visitTypeArgumentsOrDiamond(JavaLabeledParser::TypeArgumentsOrDiamondContext *context) = 0;

    virtual antlrcpp::Any visitNonWildcardTypeArgumentsOrDiamond(JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext *context) = 0;

    virtual antlrcpp::Any visitNonWildcardTypeArguments(JavaLabeledParser::NonWildcardTypeArgumentsContext *context) = 0;

    virtual antlrcpp::Any visitTypeList(JavaLabeledParser::TypeListContext *context) = 0;

    virtual antlrcpp::Any visitTypeType(JavaLabeledParser::TypeTypeContext *context) = 0;

    virtual antlrcpp::Any visitPrimitiveType(JavaLabeledParser::PrimitiveTypeContext *context) = 0;

    virtual antlrcpp::Any visitTypeArguments(JavaLabeledParser::TypeArgumentsContext *context) = 0;

    virtual antlrcpp::Any visitSuperSuffix0(JavaLabeledParser::SuperSuffix0Context *context) = 0;

    virtual antlrcpp::Any visitSuperSuffix1(JavaLabeledParser::SuperSuffix1Context *context) = 0;

    virtual antlrcpp::Any visitExplicitGenericInvocationSuffix0(JavaLabeledParser::ExplicitGenericInvocationSuffix0Context *context) = 0;

    virtual antlrcpp::Any visitExplicitGenericInvocationSuffix1(JavaLabeledParser::ExplicitGenericInvocationSuffix1Context *context) = 0;

    virtual antlrcpp::Any visitArguments(JavaLabeledParser::ArgumentsContext *context) = 0;


};

