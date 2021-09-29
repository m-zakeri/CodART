
// Generated from D:/AnacondaProjects/CodART/grammars\JavaParserLabeled.g4 by ANTLR 4.9.1

#pragma once


#include "antlr4-runtime.h"
#include "JavaParserLabeled.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by JavaParserLabeled.
 */
class  JavaParserLabeledVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by JavaParserLabeled.
   */
    virtual antlrcpp::Any visitCompilationUnit(JavaParserLabeled::CompilationUnitContext *context) = 0;

    virtual antlrcpp::Any visitPackageDeclaration(JavaParserLabeled::PackageDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitImportDeclaration(JavaParserLabeled::ImportDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitTypeDeclaration(JavaParserLabeled::TypeDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitModifier(JavaParserLabeled::ModifierContext *context) = 0;

    virtual antlrcpp::Any visitClassOrInterfaceModifier(JavaParserLabeled::ClassOrInterfaceModifierContext *context) = 0;

    virtual antlrcpp::Any visitVariableModifier(JavaParserLabeled::VariableModifierContext *context) = 0;

    virtual antlrcpp::Any visitClassDeclaration(JavaParserLabeled::ClassDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitTypeParameters(JavaParserLabeled::TypeParametersContext *context) = 0;

    virtual antlrcpp::Any visitTypeParameter(JavaParserLabeled::TypeParameterContext *context) = 0;

    virtual antlrcpp::Any visitTypeBound(JavaParserLabeled::TypeBoundContext *context) = 0;

    virtual antlrcpp::Any visitEnumDeclaration(JavaParserLabeled::EnumDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitEnumConstants(JavaParserLabeled::EnumConstantsContext *context) = 0;

    virtual antlrcpp::Any visitEnumConstant(JavaParserLabeled::EnumConstantContext *context) = 0;

    virtual antlrcpp::Any visitEnumBodyDeclarations(JavaParserLabeled::EnumBodyDeclarationsContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceDeclaration(JavaParserLabeled::InterfaceDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitClassBody(JavaParserLabeled::ClassBodyContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceBody(JavaParserLabeled::InterfaceBodyContext *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration0(JavaParserLabeled::ClassBodyDeclaration0Context *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration1(JavaParserLabeled::ClassBodyDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitClassBodyDeclaration2(JavaParserLabeled::ClassBodyDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration0(JavaParserLabeled::MemberDeclaration0Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration1(JavaParserLabeled::MemberDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration2(JavaParserLabeled::MemberDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration3(JavaParserLabeled::MemberDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration4(JavaParserLabeled::MemberDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration5(JavaParserLabeled::MemberDeclaration5Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration6(JavaParserLabeled::MemberDeclaration6Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration7(JavaParserLabeled::MemberDeclaration7Context *context) = 0;

    virtual antlrcpp::Any visitMemberDeclaration8(JavaParserLabeled::MemberDeclaration8Context *context) = 0;

    virtual antlrcpp::Any visitMethodDeclaration(JavaParserLabeled::MethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitMethodBody(JavaParserLabeled::MethodBodyContext *context) = 0;

    virtual antlrcpp::Any visitTypeTypeOrVoid(JavaParserLabeled::TypeTypeOrVoidContext *context) = 0;

    virtual antlrcpp::Any visitGenericMethodDeclaration(JavaParserLabeled::GenericMethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitGenericConstructorDeclaration(JavaParserLabeled::GenericConstructorDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitConstructorDeclaration(JavaParserLabeled::ConstructorDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitFieldDeclaration(JavaParserLabeled::FieldDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceBodyDeclaration(JavaParserLabeled::InterfaceBodyDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration0(JavaParserLabeled::InterfaceMemberDeclaration0Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration1(JavaParserLabeled::InterfaceMemberDeclaration1Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration2(JavaParserLabeled::InterfaceMemberDeclaration2Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration3(JavaParserLabeled::InterfaceMemberDeclaration3Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration4(JavaParserLabeled::InterfaceMemberDeclaration4Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration5(JavaParserLabeled::InterfaceMemberDeclaration5Context *context) = 0;

    virtual antlrcpp::Any visitInterfaceMemberDeclaration6(JavaParserLabeled::InterfaceMemberDeclaration6Context *context) = 0;

    virtual antlrcpp::Any visitConstDeclaration(JavaParserLabeled::ConstDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitConstantDeclarator(JavaParserLabeled::ConstantDeclaratorContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMethodDeclaration(JavaParserLabeled::InterfaceMethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitInterfaceMethodModifier(JavaParserLabeled::InterfaceMethodModifierContext *context) = 0;

    virtual antlrcpp::Any visitGenericInterfaceMethodDeclaration(JavaParserLabeled::GenericInterfaceMethodDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclarators(JavaParserLabeled::VariableDeclaratorsContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclarator(JavaParserLabeled::VariableDeclaratorContext *context) = 0;

    virtual antlrcpp::Any visitVariableDeclaratorId(JavaParserLabeled::VariableDeclaratorIdContext *context) = 0;

    virtual antlrcpp::Any visitVariableInitializer0(JavaParserLabeled::VariableInitializer0Context *context) = 0;

    virtual antlrcpp::Any visitVariableInitializer1(JavaParserLabeled::VariableInitializer1Context *context) = 0;

    virtual antlrcpp::Any visitArrayInitializer(JavaParserLabeled::ArrayInitializerContext *context) = 0;

    virtual antlrcpp::Any visitClassOrInterfaceType(JavaParserLabeled::ClassOrInterfaceTypeContext *context) = 0;

    virtual antlrcpp::Any visitTypeArgument0(JavaParserLabeled::TypeArgument0Context *context) = 0;

    virtual antlrcpp::Any visitQualifiedNameList(JavaParserLabeled::QualifiedNameListContext *context) = 0;

    virtual antlrcpp::Any visitFormalParameters(JavaParserLabeled::FormalParametersContext *context) = 0;

    virtual antlrcpp::Any visitFormalParameterList0(JavaParserLabeled::FormalParameterList0Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameterList1(JavaParserLabeled::FormalParameterList1Context *context) = 0;

    virtual antlrcpp::Any visitFormalParameter(JavaParserLabeled::FormalParameterContext *context) = 0;

    virtual antlrcpp::Any visitLastFormalParameter(JavaParserLabeled::LastFormalParameterContext *context) = 0;

    virtual antlrcpp::Any visitQualifiedName(JavaParserLabeled::QualifiedNameContext *context) = 0;

    virtual antlrcpp::Any visitLiteral0(JavaParserLabeled::Literal0Context *context) = 0;

    virtual antlrcpp::Any visitLiteral1(JavaParserLabeled::Literal1Context *context) = 0;

    virtual antlrcpp::Any visitLiteral2(JavaParserLabeled::Literal2Context *context) = 0;

    virtual antlrcpp::Any visitLiteral3(JavaParserLabeled::Literal3Context *context) = 0;

    virtual antlrcpp::Any visitLiteral4(JavaParserLabeled::Literal4Context *context) = 0;

    virtual antlrcpp::Any visitLiteral5(JavaParserLabeled::Literal5Context *context) = 0;

    virtual antlrcpp::Any visitIntegerLiteral(JavaParserLabeled::IntegerLiteralContext *context) = 0;

    virtual antlrcpp::Any visitFloatLiteral(JavaParserLabeled::FloatLiteralContext *context) = 0;

    virtual antlrcpp::Any visitAltAnnotationQualifiedName(JavaParserLabeled::AltAnnotationQualifiedNameContext *context) = 0;

    virtual antlrcpp::Any visitAnnotation(JavaParserLabeled::AnnotationContext *context) = 0;

    virtual antlrcpp::Any visitElementValuePairs(JavaParserLabeled::ElementValuePairsContext *context) = 0;

    virtual antlrcpp::Any visitElementValuePair(JavaParserLabeled::ElementValuePairContext *context) = 0;

    virtual antlrcpp::Any visitElementValue0(JavaParserLabeled::ElementValue0Context *context) = 0;

    virtual antlrcpp::Any visitElementValue1(JavaParserLabeled::ElementValue1Context *context) = 0;

    virtual antlrcpp::Any visitElementValue2(JavaParserLabeled::ElementValue2Context *context) = 0;

    virtual antlrcpp::Any visitElementValueArrayInitializer(JavaParserLabeled::ElementValueArrayInitializerContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeDeclaration(JavaParserLabeled::AnnotationTypeDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeBody(JavaParserLabeled::AnnotationTypeBodyContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementDeclaration(JavaParserLabeled::AnnotationTypeElementDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest0(JavaParserLabeled::AnnotationTypeElementRest0Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest1(JavaParserLabeled::AnnotationTypeElementRest1Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest2(JavaParserLabeled::AnnotationTypeElementRest2Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest3(JavaParserLabeled::AnnotationTypeElementRest3Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationTypeElementRest4(JavaParserLabeled::AnnotationTypeElementRest4Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationMethodOrConstantRest0(JavaParserLabeled::AnnotationMethodOrConstantRest0Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationMethodOrConstantRest1(JavaParserLabeled::AnnotationMethodOrConstantRest1Context *context) = 0;

    virtual antlrcpp::Any visitAnnotationMethodRest(JavaParserLabeled::AnnotationMethodRestContext *context) = 0;

    virtual antlrcpp::Any visitAnnotationConstantRest(JavaParserLabeled::AnnotationConstantRestContext *context) = 0;

    virtual antlrcpp::Any visitDefaultValue(JavaParserLabeled::DefaultValueContext *context) = 0;

    virtual antlrcpp::Any visitBlock(JavaParserLabeled::BlockContext *context) = 0;

    virtual antlrcpp::Any visitBlockStatement0(JavaParserLabeled::BlockStatement0Context *context) = 0;

    virtual antlrcpp::Any visitBlockStatement1(JavaParserLabeled::BlockStatement1Context *context) = 0;

    virtual antlrcpp::Any visitBlockStatement2(JavaParserLabeled::BlockStatement2Context *context) = 0;

    virtual antlrcpp::Any visitLocalVariableDeclaration(JavaParserLabeled::LocalVariableDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitLocalTypeDeclaration(JavaParserLabeled::LocalTypeDeclarationContext *context) = 0;

    virtual antlrcpp::Any visitStatement0(JavaParserLabeled::Statement0Context *context) = 0;

    virtual antlrcpp::Any visitStatement1(JavaParserLabeled::Statement1Context *context) = 0;

    virtual antlrcpp::Any visitStatement2(JavaParserLabeled::Statement2Context *context) = 0;

    virtual antlrcpp::Any visitStatement3(JavaParserLabeled::Statement3Context *context) = 0;

    virtual antlrcpp::Any visitStatement4(JavaParserLabeled::Statement4Context *context) = 0;

    virtual antlrcpp::Any visitStatement5(JavaParserLabeled::Statement5Context *context) = 0;

    virtual antlrcpp::Any visitStatement6(JavaParserLabeled::Statement6Context *context) = 0;

    virtual antlrcpp::Any visitStatement7(JavaParserLabeled::Statement7Context *context) = 0;

    virtual antlrcpp::Any visitStatement8(JavaParserLabeled::Statement8Context *context) = 0;

    virtual antlrcpp::Any visitStatement9(JavaParserLabeled::Statement9Context *context) = 0;

    virtual antlrcpp::Any visitStatement10(JavaParserLabeled::Statement10Context *context) = 0;

    virtual antlrcpp::Any visitStatement11(JavaParserLabeled::Statement11Context *context) = 0;

    virtual antlrcpp::Any visitStatement12(JavaParserLabeled::Statement12Context *context) = 0;

    virtual antlrcpp::Any visitStatement13(JavaParserLabeled::Statement13Context *context) = 0;

    virtual antlrcpp::Any visitStatement14(JavaParserLabeled::Statement14Context *context) = 0;

    virtual antlrcpp::Any visitStatement15(JavaParserLabeled::Statement15Context *context) = 0;

    virtual antlrcpp::Any visitStatement16(JavaParserLabeled::Statement16Context *context) = 0;

    virtual antlrcpp::Any visitCatchClause(JavaParserLabeled::CatchClauseContext *context) = 0;

    virtual antlrcpp::Any visitCatchType(JavaParserLabeled::CatchTypeContext *context) = 0;

    virtual antlrcpp::Any visitFinallyBlock(JavaParserLabeled::FinallyBlockContext *context) = 0;

    virtual antlrcpp::Any visitResourceSpecification(JavaParserLabeled::ResourceSpecificationContext *context) = 0;

    virtual antlrcpp::Any visitResources(JavaParserLabeled::ResourcesContext *context) = 0;

    virtual antlrcpp::Any visitResource(JavaParserLabeled::ResourceContext *context) = 0;

    virtual antlrcpp::Any visitSwitchBlockStatementGroup(JavaParserLabeled::SwitchBlockStatementGroupContext *context) = 0;

    virtual antlrcpp::Any visitSwitchLabel(JavaParserLabeled::SwitchLabelContext *context) = 0;

    virtual antlrcpp::Any visitForControl0(JavaParserLabeled::ForControl0Context *context) = 0;

    virtual antlrcpp::Any visitForControl1(JavaParserLabeled::ForControl1Context *context) = 0;

    virtual antlrcpp::Any visitForInit0(JavaParserLabeled::ForInit0Context *context) = 0;

    virtual antlrcpp::Any visitForInit1(JavaParserLabeled::ForInit1Context *context) = 0;

    virtual antlrcpp::Any visitEnhancedForControl(JavaParserLabeled::EnhancedForControlContext *context) = 0;

    virtual antlrcpp::Any visitParExpression(JavaParserLabeled::ParExpressionContext *context) = 0;

    virtual antlrcpp::Any visitExpressionList(JavaParserLabeled::ExpressionListContext *context) = 0;

    virtual antlrcpp::Any visitMethodCall0(JavaParserLabeled::MethodCall0Context *context) = 0;

    virtual antlrcpp::Any visitMethodCall1(JavaParserLabeled::MethodCall1Context *context) = 0;

    virtual antlrcpp::Any visitMethodCall2(JavaParserLabeled::MethodCall2Context *context) = 0;

    virtual antlrcpp::Any visitExpression8(JavaParserLabeled::Expression8Context *context) = 0;

    virtual antlrcpp::Any visitExpression10(JavaParserLabeled::Expression10Context *context) = 0;

    virtual antlrcpp::Any visitExpression9(JavaParserLabeled::Expression9Context *context) = 0;

    virtual antlrcpp::Any visitExpression12(JavaParserLabeled::Expression12Context *context) = 0;

    virtual antlrcpp::Any visitExpression11(JavaParserLabeled::Expression11Context *context) = 0;

    virtual antlrcpp::Any visitExpression14(JavaParserLabeled::Expression14Context *context) = 0;

    virtual antlrcpp::Any visitExpression13(JavaParserLabeled::Expression13Context *context) = 0;

    virtual antlrcpp::Any visitExpression16(JavaParserLabeled::Expression16Context *context) = 0;

    virtual antlrcpp::Any visitExpression15(JavaParserLabeled::Expression15Context *context) = 0;

    virtual antlrcpp::Any visitExpression18(JavaParserLabeled::Expression18Context *context) = 0;

    virtual antlrcpp::Any visitExpression17(JavaParserLabeled::Expression17Context *context) = 0;

    virtual antlrcpp::Any visitExpression19(JavaParserLabeled::Expression19Context *context) = 0;

    virtual antlrcpp::Any visitExpression6(JavaParserLabeled::Expression6Context *context) = 0;

    virtual antlrcpp::Any visitExpression7(JavaParserLabeled::Expression7Context *context) = 0;

    virtual antlrcpp::Any visitExpression4(JavaParserLabeled::Expression4Context *context) = 0;

    virtual antlrcpp::Any visitExpression5(JavaParserLabeled::Expression5Context *context) = 0;

    virtual antlrcpp::Any visitExpression2(JavaParserLabeled::Expression2Context *context) = 0;

    virtual antlrcpp::Any visitExpression3(JavaParserLabeled::Expression3Context *context) = 0;

    virtual antlrcpp::Any visitExpression0(JavaParserLabeled::Expression0Context *context) = 0;

    virtual antlrcpp::Any visitExpression1(JavaParserLabeled::Expression1Context *context) = 0;

    virtual antlrcpp::Any visitExpression21(JavaParserLabeled::Expression21Context *context) = 0;

    virtual antlrcpp::Any visitExpression20(JavaParserLabeled::Expression20Context *context) = 0;

    virtual antlrcpp::Any visitExpression23(JavaParserLabeled::Expression23Context *context) = 0;

    virtual antlrcpp::Any visitExpression22(JavaParserLabeled::Expression22Context *context) = 0;

    virtual antlrcpp::Any visitExpression25(JavaParserLabeled::Expression25Context *context) = 0;

    virtual antlrcpp::Any visitExpression24(JavaParserLabeled::Expression24Context *context) = 0;

    virtual antlrcpp::Any visitLambdaExpression(JavaParserLabeled::LambdaExpressionContext *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters0(JavaParserLabeled::LambdaParameters0Context *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters1(JavaParserLabeled::LambdaParameters1Context *context) = 0;

    virtual antlrcpp::Any visitLambdaParameters2(JavaParserLabeled::LambdaParameters2Context *context) = 0;

    virtual antlrcpp::Any visitLambdaBody0(JavaParserLabeled::LambdaBody0Context *context) = 0;

    virtual antlrcpp::Any visitLambdaBody1(JavaParserLabeled::LambdaBody1Context *context) = 0;

    virtual antlrcpp::Any visitPrimary0(JavaParserLabeled::Primary0Context *context) = 0;

    virtual antlrcpp::Any visitPrimary1(JavaParserLabeled::Primary1Context *context) = 0;

    virtual antlrcpp::Any visitPrimary2(JavaParserLabeled::Primary2Context *context) = 0;

    virtual antlrcpp::Any visitPrimary3(JavaParserLabeled::Primary3Context *context) = 0;

    virtual antlrcpp::Any visitPrimary4(JavaParserLabeled::Primary4Context *context) = 0;

    virtual antlrcpp::Any visitPrimary5(JavaParserLabeled::Primary5Context *context) = 0;

    virtual antlrcpp::Any visitPrimary6(JavaParserLabeled::Primary6Context *context) = 0;

    virtual antlrcpp::Any visitClassType(JavaParserLabeled::ClassTypeContext *context) = 0;

    virtual antlrcpp::Any visitCreator0(JavaParserLabeled::Creator0Context *context) = 0;

    virtual antlrcpp::Any visitCreator1(JavaParserLabeled::Creator1Context *context) = 0;

    virtual antlrcpp::Any visitCreatedName0(JavaParserLabeled::CreatedName0Context *context) = 0;

    virtual antlrcpp::Any visitCreatedName1(JavaParserLabeled::CreatedName1Context *context) = 0;

    virtual antlrcpp::Any visitInnerCreator(JavaParserLabeled::InnerCreatorContext *context) = 0;

    virtual antlrcpp::Any visitArrayCreatorRest(JavaParserLabeled::ArrayCreatorRestContext *context) = 0;

    virtual antlrcpp::Any visitClassCreatorRest(JavaParserLabeled::ClassCreatorRestContext *context) = 0;

    virtual antlrcpp::Any visitExplicitGenericInvocation(JavaParserLabeled::ExplicitGenericInvocationContext *context) = 0;

    virtual antlrcpp::Any visitTypeArgumentsOrDiamond(JavaParserLabeled::TypeArgumentsOrDiamondContext *context) = 0;

    virtual antlrcpp::Any visitNonWildcardTypeArgumentsOrDiamond(JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext *context) = 0;

    virtual antlrcpp::Any visitNonWildcardTypeArguments(JavaParserLabeled::NonWildcardTypeArgumentsContext *context) = 0;

    virtual antlrcpp::Any visitTypeList(JavaParserLabeled::TypeListContext *context) = 0;

    virtual antlrcpp::Any visitTypeType(JavaParserLabeled::TypeTypeContext *context) = 0;

    virtual antlrcpp::Any visitPrimitiveType(JavaParserLabeled::PrimitiveTypeContext *context) = 0;

    virtual antlrcpp::Any visitTypeArguments(JavaParserLabeled::TypeArgumentsContext *context) = 0;

    virtual antlrcpp::Any visitSuperSuffix0(JavaParserLabeled::SuperSuffix0Context *context) = 0;

    virtual antlrcpp::Any visitSuperSuffix1(JavaParserLabeled::SuperSuffix1Context *context) = 0;

    virtual antlrcpp::Any visitExplicitGenericInvocationSuffix0(JavaParserLabeled::ExplicitGenericInvocationSuffix0Context *context) = 0;

    virtual antlrcpp::Any visitExplicitGenericInvocationSuffix1(JavaParserLabeled::ExplicitGenericInvocationSuffix1Context *context) = 0;

    virtual antlrcpp::Any visitArguments(JavaParserLabeled::ArgumentsContext *context) = 0;


};

