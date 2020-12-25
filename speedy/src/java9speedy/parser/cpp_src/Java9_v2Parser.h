
// Generated from D:/AnacondaProjects/CodART/grammars\Java9_v2.g4 by ANTLR 4.9

#pragma once


#include "antlr4-runtime.h"




class  Java9_v2Parser : public antlr4::Parser {
public:
  enum {
    T__0 = 1, T__1 = 2, T__2 = 3, T__3 = 4, T__4 = 5, T__5 = 6, T__6 = 7, 
    T__7 = 8, T__8 = 9, T__9 = 10, ABSTRACT = 11, ASSERT = 12, BOOLEAN = 13, 
    BREAK = 14, BYTE = 15, CASE = 16, CATCH = 17, CHAR = 18, CLASS = 19, 
    CONST = 20, CONTINUE = 21, DEFAULT = 22, DO = 23, DOUBLE = 24, ELSE = 25, 
    ENUM = 26, EXTENDS = 27, FINAL = 28, FINALLY = 29, FLOAT = 30, FOR = 31, 
    IF = 32, GOTO = 33, IMPLEMENTS = 34, IMPORT = 35, INSTANCEOF = 36, INT = 37, 
    INTERFACE = 38, LONG = 39, NATIVE = 40, NEW = 41, PACKAGE = 42, PRIVATE = 43, 
    PROTECTED = 44, PUBLIC = 45, RETURN = 46, SHORT = 47, STATIC = 48, STRICTFP = 49, 
    SUPER = 50, SWITCH = 51, SYNCHRONIZED = 52, THIS = 53, THROW = 54, THROWS = 55, 
    TRANSIENT = 56, TRY = 57, VOID = 58, VOLATILE = 59, WHILE = 60, UNDER_SCORE = 61, 
    IntegerLiteral = 62, FloatingPointLiteral = 63, BooleanLiteral = 64, 
    CharacterLiteral = 65, StringLiteral = 66, NullLiteral = 67, LPAREN = 68, 
    RPAREN = 69, LBRACE = 70, RBRACE = 71, LBRACK = 72, RBRACK = 73, SEMI = 74, 
    COMMA = 75, DOT = 76, ELLIPSIS = 77, AT = 78, COLONCOLON = 79, ASSIGN = 80, 
    GT = 81, LT = 82, BANG = 83, TILDE = 84, QUESTION = 85, COLON = 86, 
    ARROW = 87, EQUAL = 88, LE = 89, GE = 90, NOTEQUAL = 91, AND = 92, OR = 93, 
    INC = 94, DEC = 95, ADD = 96, SUB = 97, MUL = 98, DIV = 99, BITAND = 100, 
    BITOR = 101, CARET = 102, MOD = 103, ADD_ASSIGN = 104, SUB_ASSIGN = 105, 
    MUL_ASSIGN = 106, DIV_ASSIGN = 107, AND_ASSIGN = 108, OR_ASSIGN = 109, 
    XOR_ASSIGN = 110, MOD_ASSIGN = 111, LSHIFT_ASSIGN = 112, RSHIFT_ASSIGN = 113, 
    URSHIFT_ASSIGN = 114, Identifier = 115, WS = 116, COMMENT = 117, LINE_COMMENT = 118
  };

  enum {
    RuleLiteral = 0, RulePrimitiveType = 1, RuleNumericType = 2, RuleIntegralType = 3, 
    RuleFloatingPointType = 4, RuleReferenceType = 5, RuleClassOrInterfaceType = 6, 
    RuleClassType = 7, RuleClassType_lf_classOrInterfaceType = 8, RuleClassType_lfno_classOrInterfaceType = 9, 
    RuleInterfaceType = 10, RuleInterfaceType_lf_classOrInterfaceType = 11, 
    RuleInterfaceType_lfno_classOrInterfaceType = 12, RuleTypeVariable = 13, 
    RuleArrayType = 14, RuleDims = 15, RuleTypeParameter = 16, RuleTypeParameterModifier = 17, 
    RuleTypeBound = 18, RuleAdditionalBound = 19, RuleTypeArguments = 20, 
    RuleTypeArgumentList = 21, RuleTypeArgument = 22, RuleWildcard = 23, 
    RuleWildcardBounds = 24, RuleModuleName = 25, RulePackageName = 26, 
    RuleTypeName = 27, RulePackageOrTypeName = 28, RuleExpressionName = 29, 
    RuleMethodName = 30, RuleAmbiguousName = 31, RuleCompilationUnit = 32, 
    RuleOrdinaryCompilation = 33, RuleModularCompilation = 34, RulePackageDeclaration = 35, 
    RulePackageModifier = 36, RuleImportDeclaration = 37, RuleSingleTypeImportDeclaration = 38, 
    RuleTypeImportOnDemandDeclaration = 39, RuleSingleStaticImportDeclaration = 40, 
    RuleStaticImportOnDemandDeclaration = 41, RuleTypeDeclaration = 42, 
    RuleModuleDeclaration = 43, RuleModuleDirective = 44, RuleRequiresModifier = 45, 
    RuleClassDeclaration = 46, RuleNormalClassDeclaration = 47, RuleClassModifier = 48, 
    RuleTypeParameters = 49, RuleTypeParameterList = 50, RuleSuperclass = 51, 
    RuleSuperinterfaces = 52, RuleInterfaceTypeList = 53, RuleClassBody = 54, 
    RuleClassBodyDeclaration = 55, RuleClassMemberDeclaration = 56, RuleFieldDeclaration = 57, 
    RuleFieldModifier = 58, RuleVariableDeclaratorList = 59, RuleVariableDeclarator = 60, 
    RuleVariableDeclaratorId = 61, RuleVariableInitializer = 62, RuleUnannType = 63, 
    RuleUnannPrimitiveType = 64, RuleUnannReferenceType = 65, RuleUnannClassOrInterfaceType = 66, 
    RuleUnannClassType = 67, RuleUnannClassType_lf_unannClassOrInterfaceType = 68, 
    RuleUnannClassType_lfno_unannClassOrInterfaceType = 69, RuleUnannInterfaceType = 70, 
    RuleUnannInterfaceType_lf_unannClassOrInterfaceType = 71, RuleUnannInterfaceType_lfno_unannClassOrInterfaceType = 72, 
    RuleUnannTypeVariable = 73, RuleUnannArrayType = 74, RuleMethodDeclaration = 75, 
    RuleMethodModifier = 76, RuleMethodHeader = 77, RuleResult = 78, RuleMethodDeclarator = 79, 
    RuleFormalParameterList = 80, RuleFormalParameters = 81, RuleFormalParameter = 82, 
    RuleVariableModifier = 83, RuleLastFormalParameter = 84, RuleReceiverParameter = 85, 
    RuleThrows_ = 86, RuleExceptionTypeList = 87, RuleExceptionType = 88, 
    RuleMethodBody = 89, RuleInstanceInitializer = 90, RuleStaticInitializer = 91, 
    RuleConstructorDeclaration = 92, RuleConstructorModifier = 93, RuleConstructorDeclarator = 94, 
    RuleSimpleTypeName = 95, RuleConstructorBody = 96, RuleExplicitConstructorInvocation = 97, 
    RuleEnumDeclaration = 98, RuleEnumBody = 99, RuleEnumConstantList = 100, 
    RuleEnumConstant = 101, RuleEnumConstantModifier = 102, RuleEnumBodyDeclarations = 103, 
    RuleInterfaceDeclaration = 104, RuleNormalInterfaceDeclaration = 105, 
    RuleInterfaceModifier = 106, RuleExtendsInterfaces = 107, RuleInterfaceBody = 108, 
    RuleInterfaceMemberDeclaration = 109, RuleConstantDeclaration = 110, 
    RuleConstantModifier = 111, RuleInterfaceMethodDeclaration = 112, RuleInterfaceMethodModifier = 113, 
    RuleAnnotationTypeDeclaration = 114, RuleAnnotationTypeBody = 115, RuleAnnotationTypeMemberDeclaration = 116, 
    RuleAnnotationTypeElementDeclaration = 117, RuleAnnotationTypeElementModifier = 118, 
    RuleDefaultValue = 119, RuleAnnotation = 120, RuleNormalAnnotation = 121, 
    RuleElementValuePairList = 122, RuleElementValuePair = 123, RuleElementValue = 124, 
    RuleElementValueArrayInitializer = 125, RuleElementValueList = 126, 
    RuleMarkerAnnotation = 127, RuleSingleElementAnnotation = 128, RuleArrayInitializer = 129, 
    RuleVariableInitializerList = 130, RuleBlock = 131, RuleBlockStatements = 132, 
    RuleBlockStatement = 133, RuleLocalVariableDeclarationStatement = 134, 
    RuleLocalVariableDeclaration = 135, RuleStatement = 136, RuleStatementNoShortIf = 137, 
    RuleStatementWithoutTrailingSubstatement = 138, RuleEmptyStatement = 139, 
    RuleLabeledStatement = 140, RuleLabeledStatementNoShortIf = 141, RuleExpressionStatement = 142, 
    RuleStatementExpression = 143, RuleIfThenStatement = 144, RuleIfThenElseStatement = 145, 
    RuleIfThenElseStatementNoShortIf = 146, RuleAssertStatement = 147, RuleSwitchStatement = 148, 
    RuleSwitchBlock = 149, RuleSwitchBlockStatementGroup = 150, RuleSwitchLabels = 151, 
    RuleSwitchLabel = 152, RuleEnumConstantName = 153, RuleWhileStatement = 154, 
    RuleWhileStatementNoShortIf = 155, RuleDoStatement = 156, RuleForStatement = 157, 
    RuleForStatementNoShortIf = 158, RuleBasicForStatement = 159, RuleBasicForStatementNoShortIf = 160, 
    RuleForInit = 161, RuleForUpdate = 162, RuleStatementExpressionList = 163, 
    RuleEnhancedForStatement = 164, RuleEnhancedForStatementNoShortIf = 165, 
    RuleBreakStatement = 166, RuleContinueStatement = 167, RuleReturnStatement = 168, 
    RuleThrowStatement = 169, RuleSynchronizedStatement = 170, RuleTryStatement = 171, 
    RuleCatches = 172, RuleCatchClause = 173, RuleCatchFormalParameter = 174, 
    RuleCatchType = 175, RuleFinally_ = 176, RuleTryWithResourcesStatement = 177, 
    RuleResourceSpecification = 178, RuleResourceList = 179, RuleResource = 180, 
    RuleVariableAccess = 181, RulePrimary = 182, RulePrimaryNoNewArray = 183, 
    RulePrimaryNoNewArray_lf_arrayAccess = 184, RulePrimaryNoNewArray_lfno_arrayAccess = 185, 
    RulePrimaryNoNewArray_lf_primary = 186, RulePrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary = 187, 
    RulePrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary = 188, 
    RulePrimaryNoNewArray_lfno_primary = 189, RulePrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary = 190, 
    RulePrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary = 191, 
    RuleClassLiteral = 192, RuleClassInstanceCreationExpression = 193, RuleClassInstanceCreationExpression_lf_primary = 194, 
    RuleClassInstanceCreationExpression_lfno_primary = 195, RuleTypeArgumentsOrDiamond = 196, 
    RuleFieldAccess = 197, RuleFieldAccess_lf_primary = 198, RuleFieldAccess_lfno_primary = 199, 
    RuleArrayAccess = 200, RuleArrayAccess_lf_primary = 201, RuleArrayAccess_lfno_primary = 202, 
    RuleMethodInvocation = 203, RuleMethodInvocation_lf_primary = 204, RuleMethodInvocation_lfno_primary = 205, 
    RuleArgumentList = 206, RuleMethodReference = 207, RuleMethodReference_lf_primary = 208, 
    RuleMethodReference_lfno_primary = 209, RuleArrayCreationExpression = 210, 
    RuleDimExprs = 211, RuleDimExpr = 212, RuleConstantExpression = 213, 
    RuleExpression = 214, RuleLambdaExpression = 215, RuleLambdaParameters = 216, 
    RuleInferredFormalParameterList = 217, RuleLambdaBody = 218, RuleAssignmentExpression = 219, 
    RuleAssignment = 220, RuleLeftHandSide = 221, RuleAssignmentOperator = 222, 
    RuleConditionalExpression = 223, RuleConditionalOrExpression = 224, 
    RuleConditionalAndExpression = 225, RuleInclusiveOrExpression = 226, 
    RuleExclusiveOrExpression = 227, RuleAndExpression = 228, RuleEqualityExpression = 229, 
    RuleRelationalExpression = 230, RuleShiftExpression = 231, RuleAdditiveExpression = 232, 
    RuleMultiplicativeExpression = 233, RuleUnaryExpression = 234, RulePreIncrementExpression = 235, 
    RulePreDecrementExpression = 236, RuleUnaryExpressionNotPlusMinus = 237, 
    RulePostfixExpression = 238, RulePostIncrementExpression = 239, RulePostIncrementExpression_lf_postfixExpression = 240, 
    RulePostDecrementExpression = 241, RulePostDecrementExpression_lf_postfixExpression = 242, 
    RuleCastExpression = 243, RuleIdentifier = 244
  };

  explicit Java9_v2Parser(antlr4::TokenStream *input);
  ~Java9_v2Parser();

  virtual std::string getGrammarFileName() const override;
  virtual const antlr4::atn::ATN& getATN() const override { return _atn; };
  virtual const std::vector<std::string>& getTokenNames() const override { return _tokenNames; }; // deprecated: use vocabulary instead.
  virtual const std::vector<std::string>& getRuleNames() const override;
  virtual antlr4::dfa::Vocabulary& getVocabulary() const override;


  class LiteralContext;
  class PrimitiveTypeContext;
  class NumericTypeContext;
  class IntegralTypeContext;
  class FloatingPointTypeContext;
  class ReferenceTypeContext;
  class ClassOrInterfaceTypeContext;
  class ClassTypeContext;
  class ClassType_lf_classOrInterfaceTypeContext;
  class ClassType_lfno_classOrInterfaceTypeContext;
  class InterfaceTypeContext;
  class InterfaceType_lf_classOrInterfaceTypeContext;
  class InterfaceType_lfno_classOrInterfaceTypeContext;
  class TypeVariableContext;
  class ArrayTypeContext;
  class DimsContext;
  class TypeParameterContext;
  class TypeParameterModifierContext;
  class TypeBoundContext;
  class AdditionalBoundContext;
  class TypeArgumentsContext;
  class TypeArgumentListContext;
  class TypeArgumentContext;
  class WildcardContext;
  class WildcardBoundsContext;
  class ModuleNameContext;
  class PackageNameContext;
  class TypeNameContext;
  class PackageOrTypeNameContext;
  class ExpressionNameContext;
  class MethodNameContext;
  class AmbiguousNameContext;
  class CompilationUnitContext;
  class OrdinaryCompilationContext;
  class ModularCompilationContext;
  class PackageDeclarationContext;
  class PackageModifierContext;
  class ImportDeclarationContext;
  class SingleTypeImportDeclarationContext;
  class TypeImportOnDemandDeclarationContext;
  class SingleStaticImportDeclarationContext;
  class StaticImportOnDemandDeclarationContext;
  class TypeDeclarationContext;
  class ModuleDeclarationContext;
  class ModuleDirectiveContext;
  class RequiresModifierContext;
  class ClassDeclarationContext;
  class NormalClassDeclarationContext;
  class ClassModifierContext;
  class TypeParametersContext;
  class TypeParameterListContext;
  class SuperclassContext;
  class SuperinterfacesContext;
  class InterfaceTypeListContext;
  class ClassBodyContext;
  class ClassBodyDeclarationContext;
  class ClassMemberDeclarationContext;
  class FieldDeclarationContext;
  class FieldModifierContext;
  class VariableDeclaratorListContext;
  class VariableDeclaratorContext;
  class VariableDeclaratorIdContext;
  class VariableInitializerContext;
  class UnannTypeContext;
  class UnannPrimitiveTypeContext;
  class UnannReferenceTypeContext;
  class UnannClassOrInterfaceTypeContext;
  class UnannClassTypeContext;
  class UnannClassType_lf_unannClassOrInterfaceTypeContext;
  class UnannClassType_lfno_unannClassOrInterfaceTypeContext;
  class UnannInterfaceTypeContext;
  class UnannInterfaceType_lf_unannClassOrInterfaceTypeContext;
  class UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext;
  class UnannTypeVariableContext;
  class UnannArrayTypeContext;
  class MethodDeclarationContext;
  class MethodModifierContext;
  class MethodHeaderContext;
  class ResultContext;
  class MethodDeclaratorContext;
  class FormalParameterListContext;
  class FormalParametersContext;
  class FormalParameterContext;
  class VariableModifierContext;
  class LastFormalParameterContext;
  class ReceiverParameterContext;
  class Throws_Context;
  class ExceptionTypeListContext;
  class ExceptionTypeContext;
  class MethodBodyContext;
  class InstanceInitializerContext;
  class StaticInitializerContext;
  class ConstructorDeclarationContext;
  class ConstructorModifierContext;
  class ConstructorDeclaratorContext;
  class SimpleTypeNameContext;
  class ConstructorBodyContext;
  class ExplicitConstructorInvocationContext;
  class EnumDeclarationContext;
  class EnumBodyContext;
  class EnumConstantListContext;
  class EnumConstantContext;
  class EnumConstantModifierContext;
  class EnumBodyDeclarationsContext;
  class InterfaceDeclarationContext;
  class NormalInterfaceDeclarationContext;
  class InterfaceModifierContext;
  class ExtendsInterfacesContext;
  class InterfaceBodyContext;
  class InterfaceMemberDeclarationContext;
  class ConstantDeclarationContext;
  class ConstantModifierContext;
  class InterfaceMethodDeclarationContext;
  class InterfaceMethodModifierContext;
  class AnnotationTypeDeclarationContext;
  class AnnotationTypeBodyContext;
  class AnnotationTypeMemberDeclarationContext;
  class AnnotationTypeElementDeclarationContext;
  class AnnotationTypeElementModifierContext;
  class DefaultValueContext;
  class AnnotationContext;
  class NormalAnnotationContext;
  class ElementValuePairListContext;
  class ElementValuePairContext;
  class ElementValueContext;
  class ElementValueArrayInitializerContext;
  class ElementValueListContext;
  class MarkerAnnotationContext;
  class SingleElementAnnotationContext;
  class ArrayInitializerContext;
  class VariableInitializerListContext;
  class BlockContext;
  class BlockStatementsContext;
  class BlockStatementContext;
  class LocalVariableDeclarationStatementContext;
  class LocalVariableDeclarationContext;
  class StatementContext;
  class StatementNoShortIfContext;
  class StatementWithoutTrailingSubstatementContext;
  class EmptyStatementContext;
  class LabeledStatementContext;
  class LabeledStatementNoShortIfContext;
  class ExpressionStatementContext;
  class StatementExpressionContext;
  class IfThenStatementContext;
  class IfThenElseStatementContext;
  class IfThenElseStatementNoShortIfContext;
  class AssertStatementContext;
  class SwitchStatementContext;
  class SwitchBlockContext;
  class SwitchBlockStatementGroupContext;
  class SwitchLabelsContext;
  class SwitchLabelContext;
  class EnumConstantNameContext;
  class WhileStatementContext;
  class WhileStatementNoShortIfContext;
  class DoStatementContext;
  class ForStatementContext;
  class ForStatementNoShortIfContext;
  class BasicForStatementContext;
  class BasicForStatementNoShortIfContext;
  class ForInitContext;
  class ForUpdateContext;
  class StatementExpressionListContext;
  class EnhancedForStatementContext;
  class EnhancedForStatementNoShortIfContext;
  class BreakStatementContext;
  class ContinueStatementContext;
  class ReturnStatementContext;
  class ThrowStatementContext;
  class SynchronizedStatementContext;
  class TryStatementContext;
  class CatchesContext;
  class CatchClauseContext;
  class CatchFormalParameterContext;
  class CatchTypeContext;
  class Finally_Context;
  class TryWithResourcesStatementContext;
  class ResourceSpecificationContext;
  class ResourceListContext;
  class ResourceContext;
  class VariableAccessContext;
  class PrimaryContext;
  class PrimaryNoNewArrayContext;
  class PrimaryNoNewArray_lf_arrayAccessContext;
  class PrimaryNoNewArray_lfno_arrayAccessContext;
  class PrimaryNoNewArray_lf_primaryContext;
  class PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext;
  class PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext;
  class PrimaryNoNewArray_lfno_primaryContext;
  class PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext;
  class PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext;
  class ClassLiteralContext;
  class ClassInstanceCreationExpressionContext;
  class ClassInstanceCreationExpression_lf_primaryContext;
  class ClassInstanceCreationExpression_lfno_primaryContext;
  class TypeArgumentsOrDiamondContext;
  class FieldAccessContext;
  class FieldAccess_lf_primaryContext;
  class FieldAccess_lfno_primaryContext;
  class ArrayAccessContext;
  class ArrayAccess_lf_primaryContext;
  class ArrayAccess_lfno_primaryContext;
  class MethodInvocationContext;
  class MethodInvocation_lf_primaryContext;
  class MethodInvocation_lfno_primaryContext;
  class ArgumentListContext;
  class MethodReferenceContext;
  class MethodReference_lf_primaryContext;
  class MethodReference_lfno_primaryContext;
  class ArrayCreationExpressionContext;
  class DimExprsContext;
  class DimExprContext;
  class ConstantExpressionContext;
  class ExpressionContext;
  class LambdaExpressionContext;
  class LambdaParametersContext;
  class InferredFormalParameterListContext;
  class LambdaBodyContext;
  class AssignmentExpressionContext;
  class AssignmentContext;
  class LeftHandSideContext;
  class AssignmentOperatorContext;
  class ConditionalExpressionContext;
  class ConditionalOrExpressionContext;
  class ConditionalAndExpressionContext;
  class InclusiveOrExpressionContext;
  class ExclusiveOrExpressionContext;
  class AndExpressionContext;
  class EqualityExpressionContext;
  class RelationalExpressionContext;
  class ShiftExpressionContext;
  class AdditiveExpressionContext;
  class MultiplicativeExpressionContext;
  class UnaryExpressionContext;
  class PreIncrementExpressionContext;
  class PreDecrementExpressionContext;
  class UnaryExpressionNotPlusMinusContext;
  class PostfixExpressionContext;
  class PostIncrementExpressionContext;
  class PostIncrementExpression_lf_postfixExpressionContext;
  class PostDecrementExpressionContext;
  class PostDecrementExpression_lf_postfixExpressionContext;
  class CastExpressionContext;
  class IdentifierContext; 

  class  LiteralContext : public antlr4::ParserRuleContext {
  public:
    LiteralContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IntegerLiteral();
    antlr4::tree::TerminalNode *FloatingPointLiteral();
    antlr4::tree::TerminalNode *BooleanLiteral();
    antlr4::tree::TerminalNode *CharacterLiteral();
    antlr4::tree::TerminalNode *StringLiteral();
    antlr4::tree::TerminalNode *NullLiteral();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LiteralContext* literal();

  class  PrimitiveTypeContext : public antlr4::ParserRuleContext {
  public:
    PrimitiveTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PrimitiveTypeContext() = default;
    void copyFrom(PrimitiveTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PrimitiveType1Context : public PrimitiveTypeContext {
  public:
    PrimitiveType1Context(PrimitiveTypeContext *ctx);

    NumericTypeContext *numericType();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimitiveType2Context : public PrimitiveTypeContext {
  public:
    PrimitiveType2Context(PrimitiveTypeContext *ctx);

    antlr4::tree::TerminalNode *BOOLEAN();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PrimitiveTypeContext* primitiveType();

  class  NumericTypeContext : public antlr4::ParserRuleContext {
  public:
    NumericTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    NumericTypeContext() = default;
    void copyFrom(NumericTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  NumericType1Context : public NumericTypeContext {
  public:
    NumericType1Context(NumericTypeContext *ctx);

    IntegralTypeContext *integralType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  NumericType2Context : public NumericTypeContext {
  public:
    NumericType2Context(NumericTypeContext *ctx);

    FloatingPointTypeContext *floatingPointType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  NumericTypeContext* numericType();

  class  IntegralTypeContext : public antlr4::ParserRuleContext {
  public:
    IntegralTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *BYTE();
    antlr4::tree::TerminalNode *SHORT();
    antlr4::tree::TerminalNode *INT();
    antlr4::tree::TerminalNode *LONG();
    antlr4::tree::TerminalNode *CHAR();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IntegralTypeContext* integralType();

  class  FloatingPointTypeContext : public antlr4::ParserRuleContext {
  public:
    FloatingPointTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FLOAT();
    antlr4::tree::TerminalNode *DOUBLE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FloatingPointTypeContext* floatingPointType();

  class  ReferenceTypeContext : public antlr4::ParserRuleContext {
  public:
    ReferenceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ReferenceTypeContext() = default;
    void copyFrom(ReferenceTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ReferenceType3Context : public ReferenceTypeContext {
  public:
    ReferenceType3Context(ReferenceTypeContext *ctx);

    ArrayTypeContext *arrayType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ReferenceType2Context : public ReferenceTypeContext {
  public:
    ReferenceType2Context(ReferenceTypeContext *ctx);

    TypeVariableContext *typeVariable();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ReferenceType1Context : public ReferenceTypeContext {
  public:
    ReferenceType1Context(ReferenceTypeContext *ctx);

    ClassOrInterfaceTypeContext *classOrInterfaceType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ReferenceTypeContext* referenceType();

  class  ClassOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    ClassOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassType_lfno_classOrInterfaceTypeContext *classType_lfno_classOrInterfaceType();
    InterfaceType_lfno_classOrInterfaceTypeContext *interfaceType_lfno_classOrInterfaceType();
    std::vector<ClassType_lf_classOrInterfaceTypeContext *> classType_lf_classOrInterfaceType();
    ClassType_lf_classOrInterfaceTypeContext* classType_lf_classOrInterfaceType(size_t i);
    std::vector<InterfaceType_lf_classOrInterfaceTypeContext *> interfaceType_lf_classOrInterfaceType();
    InterfaceType_lf_classOrInterfaceTypeContext* interfaceType_lf_classOrInterfaceType(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassOrInterfaceTypeContext* classOrInterfaceType();

  class  ClassTypeContext : public antlr4::ParserRuleContext {
  public:
    ClassTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ClassTypeContext() = default;
    void copyFrom(ClassTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ClassType1Context : public ClassTypeContext {
  public:
    ClassType1Context(ClassTypeContext *ctx);

    IdentifierContext *identifier();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassType2Context : public ClassTypeContext {
  public:
    ClassType2Context(ClassTypeContext *ctx);

    ClassOrInterfaceTypeContext *classOrInterfaceType();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ClassTypeContext* classType();

  class  ClassType_lf_classOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    ClassType_lf_classOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsContext *typeArguments();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassType_lf_classOrInterfaceTypeContext* classType_lf_classOrInterfaceType();

  class  ClassType_lfno_classOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    ClassType_lfno_classOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsContext *typeArguments();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassType_lfno_classOrInterfaceTypeContext* classType_lfno_classOrInterfaceType();

  class  InterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    InterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassTypeContext *classType();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceTypeContext* interfaceType();

  class  InterfaceType_lf_classOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    InterfaceType_lf_classOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassType_lf_classOrInterfaceTypeContext *classType_lf_classOrInterfaceType();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceType_lf_classOrInterfaceTypeContext* interfaceType_lf_classOrInterfaceType();

  class  InterfaceType_lfno_classOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    InterfaceType_lfno_classOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassType_lfno_classOrInterfaceTypeContext *classType_lfno_classOrInterfaceType();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceType_lfno_classOrInterfaceTypeContext* interfaceType_lfno_classOrInterfaceType();

  class  TypeVariableContext : public antlr4::ParserRuleContext {
  public:
    TypeVariableContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeVariableContext* typeVariable();

  class  ArrayTypeContext : public antlr4::ParserRuleContext {
  public:
    ArrayTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ArrayTypeContext() = default;
    void copyFrom(ArrayTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ArrayTyp3Context : public ArrayTypeContext {
  public:
    ArrayTyp3Context(ArrayTypeContext *ctx);

    TypeVariableContext *typeVariable();
    DimsContext *dims();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ArrayType1Context : public ArrayTypeContext {
  public:
    ArrayType1Context(ArrayTypeContext *ctx);

    PrimitiveTypeContext *primitiveType();
    DimsContext *dims();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ArrayType2Context : public ArrayTypeContext {
  public:
    ArrayType2Context(ArrayTypeContext *ctx);

    ClassOrInterfaceTypeContext *classOrInterfaceType();
    DimsContext *dims();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ArrayTypeContext* arrayType();

  class  DimsContext : public antlr4::ParserRuleContext {
  public:
    DimsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DimsContext* dims();

  class  TypeParameterContext : public antlr4::ParserRuleContext {
  public:
    TypeParameterContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    std::vector<TypeParameterModifierContext *> typeParameterModifier();
    TypeParameterModifierContext* typeParameterModifier(size_t i);
    TypeBoundContext *typeBound();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeParameterContext* typeParameter();

  class  TypeParameterModifierContext : public antlr4::ParserRuleContext {
  public:
    TypeParameterModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeParameterModifierContext* typeParameterModifier();

  class  TypeBoundContext : public antlr4::ParserRuleContext {
  public:
    TypeBoundContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    TypeBoundContext() = default;
    void copyFrom(TypeBoundContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  TypeBound2Context : public TypeBoundContext {
  public:
    TypeBound2Context(TypeBoundContext *ctx);

    antlr4::tree::TerminalNode *EXTENDS();
    ClassOrInterfaceTypeContext *classOrInterfaceType();
    std::vector<AdditionalBoundContext *> additionalBound();
    AdditionalBoundContext* additionalBound(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  TypeBound1Context : public TypeBoundContext {
  public:
    TypeBound1Context(TypeBoundContext *ctx);

    antlr4::tree::TerminalNode *EXTENDS();
    TypeVariableContext *typeVariable();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  TypeBoundContext* typeBound();

  class  AdditionalBoundContext : public antlr4::ParserRuleContext {
  public:
    AdditionalBoundContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *BITAND();
    InterfaceTypeContext *interfaceType();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AdditionalBoundContext* additionalBound();

  class  TypeArgumentsContext : public antlr4::ParserRuleContext {
  public:
    TypeArgumentsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LT();
    TypeArgumentListContext *typeArgumentList();
    antlr4::tree::TerminalNode *GT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeArgumentsContext* typeArguments();

  class  TypeArgumentListContext : public antlr4::ParserRuleContext {
  public:
    TypeArgumentListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<TypeArgumentContext *> typeArgument();
    TypeArgumentContext* typeArgument(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeArgumentListContext* typeArgumentList();

  class  TypeArgumentContext : public antlr4::ParserRuleContext {
  public:
    TypeArgumentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    TypeArgumentContext() = default;
    void copyFrom(TypeArgumentContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  TypeArgument1Context : public TypeArgumentContext {
  public:
    TypeArgument1Context(TypeArgumentContext *ctx);

    ReferenceTypeContext *referenceType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  TypeArgument2Context : public TypeArgumentContext {
  public:
    TypeArgument2Context(TypeArgumentContext *ctx);

    WildcardContext *wildcard();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  TypeArgumentContext* typeArgument();

  class  WildcardContext : public antlr4::ParserRuleContext {
  public:
    WildcardContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *QUESTION();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    WildcardBoundsContext *wildcardBounds();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  WildcardContext* wildcard();

  class  WildcardBoundsContext : public antlr4::ParserRuleContext {
  public:
    WildcardBoundsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    WildcardBoundsContext() = default;
    void copyFrom(WildcardBoundsContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  WildcardBound2Context : public WildcardBoundsContext {
  public:
    WildcardBound2Context(WildcardBoundsContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    ReferenceTypeContext *referenceType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  WildcardBounds1Context : public WildcardBoundsContext {
  public:
    WildcardBounds1Context(WildcardBoundsContext *ctx);

    antlr4::tree::TerminalNode *EXTENDS();
    ReferenceTypeContext *referenceType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  WildcardBoundsContext* wildcardBounds();

  class  ModuleNameContext : public antlr4::ParserRuleContext {
  public:
    ModuleNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ModuleNameContext() = default;
    void copyFrom(ModuleNameContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ModuleName1Context : public ModuleNameContext {
  public:
    ModuleName1Context(ModuleNameContext *ctx);

    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ModuleName2Context : public ModuleNameContext {
  public:
    ModuleName2Context(ModuleNameContext *ctx);

    ModuleNameContext *moduleName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ModuleNameContext* moduleName();
  ModuleNameContext* moduleName(int precedence);
  class  PackageNameContext : public antlr4::ParserRuleContext {
  public:
    PackageNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PackageNameContext() = default;
    void copyFrom(PackageNameContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PackageName2Context : public PackageNameContext {
  public:
    PackageName2Context(PackageNameContext *ctx);

    PackageNameContext *packageName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PackageName1Context : public PackageNameContext {
  public:
    PackageName1Context(PackageNameContext *ctx);

    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PackageNameContext* packageName();
  PackageNameContext* packageName(int precedence);
  class  TypeNameContext : public antlr4::ParserRuleContext {
  public:
    TypeNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    TypeNameContext() = default;
    void copyFrom(TypeNameContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  TypeName1Context : public TypeNameContext {
  public:
    TypeName1Context(TypeNameContext *ctx);

    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  TypeName2Context : public TypeNameContext {
  public:
    TypeName2Context(TypeNameContext *ctx);

    PackageOrTypeNameContext *packageOrTypeName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  TypeNameContext* typeName();

  class  PackageOrTypeNameContext : public antlr4::ParserRuleContext {
  public:
    PackageOrTypeNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PackageOrTypeNameContext() = default;
    void copyFrom(PackageOrTypeNameContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PackageOrTypeName1Context : public PackageOrTypeNameContext {
  public:
    PackageOrTypeName1Context(PackageOrTypeNameContext *ctx);

    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PackageOrTypeName2Context : public PackageOrTypeNameContext {
  public:
    PackageOrTypeName2Context(PackageOrTypeNameContext *ctx);

    PackageOrTypeNameContext *packageOrTypeName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PackageOrTypeNameContext* packageOrTypeName();
  PackageOrTypeNameContext* packageOrTypeName(int precedence);
  class  ExpressionNameContext : public antlr4::ParserRuleContext {
  public:
    ExpressionNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ExpressionNameContext() = default;
    void copyFrom(ExpressionNameContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ExpressionName2Context : public ExpressionNameContext {
  public:
    ExpressionName2Context(ExpressionNameContext *ctx);

    AmbiguousNameContext *ambiguousName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ExpressionName1Context : public ExpressionNameContext {
  public:
    ExpressionName1Context(ExpressionNameContext *ctx);

    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ExpressionNameContext* expressionName();

  class  MethodNameContext : public antlr4::ParserRuleContext {
  public:
    MethodNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodNameContext* methodName();

  class  AmbiguousNameContext : public antlr4::ParserRuleContext {
  public:
    AmbiguousNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AmbiguousNameContext() = default;
    void copyFrom(AmbiguousNameContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  AmbiguousName1Context : public AmbiguousNameContext {
  public:
    AmbiguousName1Context(AmbiguousNameContext *ctx);

    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AmbiguousName2Context : public AmbiguousNameContext {
  public:
    AmbiguousName2Context(AmbiguousNameContext *ctx);

    AmbiguousNameContext *ambiguousName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AmbiguousNameContext* ambiguousName();
  AmbiguousNameContext* ambiguousName(int precedence);
  class  CompilationUnitContext : public antlr4::ParserRuleContext {
  public:
    CompilationUnitContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    CompilationUnitContext() = default;
    void copyFrom(CompilationUnitContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  CompilationUnit2Context : public CompilationUnitContext {
  public:
    CompilationUnit2Context(CompilationUnitContext *ctx);

    ModularCompilationContext *modularCompilation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  CompilationUnit1Context : public CompilationUnitContext {
  public:
    CompilationUnit1Context(CompilationUnitContext *ctx);

    OrdinaryCompilationContext *ordinaryCompilation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  CompilationUnitContext* compilationUnit();

  class  OrdinaryCompilationContext : public antlr4::ParserRuleContext {
  public:
    OrdinaryCompilationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EOF();
    PackageDeclarationContext *packageDeclaration();
    std::vector<ImportDeclarationContext *> importDeclaration();
    ImportDeclarationContext* importDeclaration(size_t i);
    std::vector<TypeDeclarationContext *> typeDeclaration();
    TypeDeclarationContext* typeDeclaration(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  OrdinaryCompilationContext* ordinaryCompilation();

  class  ModularCompilationContext : public antlr4::ParserRuleContext {
  public:
    ModularCompilationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ModuleDeclarationContext *moduleDeclaration();
    std::vector<ImportDeclarationContext *> importDeclaration();
    ImportDeclarationContext* importDeclaration(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ModularCompilationContext* modularCompilation();

  class  PackageDeclarationContext : public antlr4::ParserRuleContext {
  public:
    PackageDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *PACKAGE();
    PackageNameContext *packageName();
    antlr4::tree::TerminalNode *SEMI();
    std::vector<PackageModifierContext *> packageModifier();
    PackageModifierContext* packageModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PackageDeclarationContext* packageDeclaration();

  class  PackageModifierContext : public antlr4::ParserRuleContext {
  public:
    PackageModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PackageModifierContext* packageModifier();

  class  ImportDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ImportDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ImportDeclarationContext() = default;
    void copyFrom(ImportDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ImportDeclaration3Context : public ImportDeclarationContext {
  public:
    ImportDeclaration3Context(ImportDeclarationContext *ctx);

    SingleStaticImportDeclarationContext *singleStaticImportDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ImportDeclaration4Context : public ImportDeclarationContext {
  public:
    ImportDeclaration4Context(ImportDeclarationContext *ctx);

    StaticImportOnDemandDeclarationContext *staticImportOnDemandDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ImportDeclaration1Context : public ImportDeclarationContext {
  public:
    ImportDeclaration1Context(ImportDeclarationContext *ctx);

    SingleTypeImportDeclarationContext *singleTypeImportDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ImportDeclaration2Context : public ImportDeclarationContext {
  public:
    ImportDeclaration2Context(ImportDeclarationContext *ctx);

    TypeImportOnDemandDeclarationContext *typeImportOnDemandDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ImportDeclarationContext* importDeclaration();

  class  SingleTypeImportDeclarationContext : public antlr4::ParserRuleContext {
  public:
    SingleTypeImportDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IMPORT();
    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SingleTypeImportDeclarationContext* singleTypeImportDeclaration();

  class  TypeImportOnDemandDeclarationContext : public antlr4::ParserRuleContext {
  public:
    TypeImportOnDemandDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IMPORT();
    PackageOrTypeNameContext *packageOrTypeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *MUL();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeImportOnDemandDeclarationContext* typeImportOnDemandDeclaration();

  class  SingleStaticImportDeclarationContext : public antlr4::ParserRuleContext {
  public:
    SingleStaticImportDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IMPORT();
    antlr4::tree::TerminalNode *STATIC();
    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SingleStaticImportDeclarationContext* singleStaticImportDeclaration();

  class  StaticImportOnDemandDeclarationContext : public antlr4::ParserRuleContext {
  public:
    StaticImportOnDemandDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IMPORT();
    antlr4::tree::TerminalNode *STATIC();
    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *MUL();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StaticImportOnDemandDeclarationContext* staticImportOnDemandDeclaration();

  class  TypeDeclarationContext : public antlr4::ParserRuleContext {
  public:
    TypeDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    TypeDeclarationContext() = default;
    void copyFrom(TypeDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  TypeDeclaration2Context : public TypeDeclarationContext {
  public:
    TypeDeclaration2Context(TypeDeclarationContext *ctx);

    InterfaceDeclarationContext *interfaceDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  TypeDeclaration3Context : public TypeDeclarationContext {
  public:
    TypeDeclaration3Context(TypeDeclarationContext *ctx);

    antlr4::tree::TerminalNode *SEMI();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  TypeDeclaration1Context : public TypeDeclarationContext {
  public:
    TypeDeclaration1Context(TypeDeclarationContext *ctx);

    ClassDeclarationContext *classDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  TypeDeclarationContext* typeDeclaration();

  class  ModuleDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ModuleDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ModuleNameContext *moduleName();
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    std::vector<ModuleDirectiveContext *> moduleDirective();
    ModuleDirectiveContext* moduleDirective(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ModuleDeclarationContext* moduleDeclaration();

  class  ModuleDirectiveContext : public antlr4::ParserRuleContext {
  public:
    ModuleDirectiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ModuleDirectiveContext() = default;
    void copyFrom(ModuleDirectiveContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ModuleDirective5Context : public ModuleDirectiveContext {
  public:
    ModuleDirective5Context(ModuleDirectiveContext *ctx);

    std::vector<TypeNameContext *> typeName();
    TypeNameContext* typeName(size_t i);
    antlr4::tree::TerminalNode *SEMI();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ModuleDirective4Context : public ModuleDirectiveContext {
  public:
    ModuleDirective4Context(ModuleDirectiveContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *SEMI();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ModuleDirective1Context : public ModuleDirectiveContext {
  public:
    ModuleDirective1Context(ModuleDirectiveContext *ctx);

    ModuleNameContext *moduleName();
    antlr4::tree::TerminalNode *SEMI();
    std::vector<RequiresModifierContext *> requiresModifier();
    RequiresModifierContext* requiresModifier(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ModuleDirective2Context : public ModuleDirectiveContext {
  public:
    ModuleDirective2Context(ModuleDirectiveContext *ctx);

    PackageNameContext *packageName();
    antlr4::tree::TerminalNode *SEMI();
    std::vector<ModuleNameContext *> moduleName();
    ModuleNameContext* moduleName(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ModuleDirectiv3Context : public ModuleDirectiveContext {
  public:
    ModuleDirectiv3Context(ModuleDirectiveContext *ctx);

    PackageNameContext *packageName();
    antlr4::tree::TerminalNode *SEMI();
    std::vector<ModuleNameContext *> moduleName();
    ModuleNameContext* moduleName(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ModuleDirectiveContext* moduleDirective();

  class  RequiresModifierContext : public antlr4::ParserRuleContext {
  public:
    RequiresModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STATIC();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  RequiresModifierContext* requiresModifier();

  class  ClassDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ClassDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ClassDeclarationContext() = default;
    void copyFrom(ClassDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ClassDeclaration1Context : public ClassDeclarationContext {
  public:
    ClassDeclaration1Context(ClassDeclarationContext *ctx);

    NormalClassDeclarationContext *normalClassDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassDeclaration2Context : public ClassDeclarationContext {
  public:
    ClassDeclaration2Context(ClassDeclarationContext *ctx);

    EnumDeclarationContext *enumDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ClassDeclarationContext* classDeclaration();

  class  NormalClassDeclarationContext : public antlr4::ParserRuleContext {
  public:
    NormalClassDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CLASS();
    IdentifierContext *identifier();
    ClassBodyContext *classBody();
    std::vector<ClassModifierContext *> classModifier();
    ClassModifierContext* classModifier(size_t i);
    TypeParametersContext *typeParameters();
    SuperclassContext *superclass();
    SuperinterfacesContext *superinterfaces();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  NormalClassDeclarationContext* normalClassDeclaration();

  class  ClassModifierContext : public antlr4::ParserRuleContext {
  public:
    ClassModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *PROTECTED();
    antlr4::tree::TerminalNode *PRIVATE();
    antlr4::tree::TerminalNode *ABSTRACT();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *FINAL();
    antlr4::tree::TerminalNode *STRICTFP();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassModifierContext* classModifier();

  class  TypeParametersContext : public antlr4::ParserRuleContext {
  public:
    TypeParametersContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LT();
    TypeParameterListContext *typeParameterList();
    antlr4::tree::TerminalNode *GT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeParametersContext* typeParameters();

  class  TypeParameterListContext : public antlr4::ParserRuleContext {
  public:
    TypeParameterListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<TypeParameterContext *> typeParameter();
    TypeParameterContext* typeParameter(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeParameterListContext* typeParameterList();

  class  SuperclassContext : public antlr4::ParserRuleContext {
  public:
    SuperclassContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EXTENDS();
    ClassTypeContext *classType();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SuperclassContext* superclass();

  class  SuperinterfacesContext : public antlr4::ParserRuleContext {
  public:
    SuperinterfacesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IMPLEMENTS();
    InterfaceTypeListContext *interfaceTypeList();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SuperinterfacesContext* superinterfaces();

  class  InterfaceTypeListContext : public antlr4::ParserRuleContext {
  public:
    InterfaceTypeListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<InterfaceTypeContext *> interfaceType();
    InterfaceTypeContext* interfaceType(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceTypeListContext* interfaceTypeList();

  class  ClassBodyContext : public antlr4::ParserRuleContext {
  public:
    ClassBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<ClassBodyDeclarationContext *> classBodyDeclaration();
    ClassBodyDeclarationContext* classBodyDeclaration(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassBodyContext* classBody();

  class  ClassBodyDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ClassBodyDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ClassBodyDeclarationContext() = default;
    void copyFrom(ClassBodyDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ClassBodyDeclaration4Context : public ClassBodyDeclarationContext {
  public:
    ClassBodyDeclaration4Context(ClassBodyDeclarationContext *ctx);

    ConstructorDeclarationContext *constructorDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassBodyDeclaration1Context : public ClassBodyDeclarationContext {
  public:
    ClassBodyDeclaration1Context(ClassBodyDeclarationContext *ctx);

    ClassMemberDeclarationContext *classMemberDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassBodyDeclaration3Context : public ClassBodyDeclarationContext {
  public:
    ClassBodyDeclaration3Context(ClassBodyDeclarationContext *ctx);

    StaticInitializerContext *staticInitializer();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassBodyDeclaration2Context : public ClassBodyDeclarationContext {
  public:
    ClassBodyDeclaration2Context(ClassBodyDeclarationContext *ctx);

    InstanceInitializerContext *instanceInitializer();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ClassBodyDeclarationContext* classBodyDeclaration();

  class  ClassMemberDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ClassMemberDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ClassMemberDeclarationContext() = default;
    void copyFrom(ClassMemberDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ClassMemberDeclaration4Context : public ClassMemberDeclarationContext {
  public:
    ClassMemberDeclaration4Context(ClassMemberDeclarationContext *ctx);

    InterfaceDeclarationContext *interfaceDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassMemberDeclaration5Context : public ClassMemberDeclarationContext {
  public:
    ClassMemberDeclaration5Context(ClassMemberDeclarationContext *ctx);

    antlr4::tree::TerminalNode *SEMI();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassMemberDeclaration2Context : public ClassMemberDeclarationContext {
  public:
    ClassMemberDeclaration2Context(ClassMemberDeclarationContext *ctx);

    MethodDeclarationContext *methodDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassMemberDeclaration3Context : public ClassMemberDeclarationContext {
  public:
    ClassMemberDeclaration3Context(ClassMemberDeclarationContext *ctx);

    ClassDeclarationContext *classDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassMemberDeclaration1Context : public ClassMemberDeclarationContext {
  public:
    ClassMemberDeclaration1Context(ClassMemberDeclarationContext *ctx);

    FieldDeclarationContext *fieldDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ClassMemberDeclarationContext* classMemberDeclaration();

  class  FieldDeclarationContext : public antlr4::ParserRuleContext {
  public:
    FieldDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannTypeContext *unannType();
    VariableDeclaratorListContext *variableDeclaratorList();
    antlr4::tree::TerminalNode *SEMI();
    std::vector<FieldModifierContext *> fieldModifier();
    FieldModifierContext* fieldModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FieldDeclarationContext* fieldDeclaration();

  class  FieldModifierContext : public antlr4::ParserRuleContext {
  public:
    FieldModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *PROTECTED();
    antlr4::tree::TerminalNode *PRIVATE();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *FINAL();
    antlr4::tree::TerminalNode *TRANSIENT();
    antlr4::tree::TerminalNode *VOLATILE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FieldModifierContext* fieldModifier();

  class  VariableDeclaratorListContext : public antlr4::ParserRuleContext {
  public:
    VariableDeclaratorListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<VariableDeclaratorContext *> variableDeclarator();
    VariableDeclaratorContext* variableDeclarator(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VariableDeclaratorListContext* variableDeclaratorList();

  class  VariableDeclaratorContext : public antlr4::ParserRuleContext {
  public:
    VariableDeclaratorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    VariableDeclaratorIdContext *variableDeclaratorId();
    antlr4::tree::TerminalNode *ASSIGN();
    VariableInitializerContext *variableInitializer();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VariableDeclaratorContext* variableDeclarator();

  class  VariableDeclaratorIdContext : public antlr4::ParserRuleContext {
  public:
    VariableDeclaratorIdContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    DimsContext *dims();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VariableDeclaratorIdContext* variableDeclaratorId();

  class  VariableInitializerContext : public antlr4::ParserRuleContext {
  public:
    VariableInitializerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    VariableInitializerContext() = default;
    void copyFrom(VariableInitializerContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  VariableInitializer1Context : public VariableInitializerContext {
  public:
    VariableInitializer1Context(VariableInitializerContext *ctx);

    ExpressionContext *expression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  VariableInitializer2Context : public VariableInitializerContext {
  public:
    VariableInitializer2Context(VariableInitializerContext *ctx);

    ArrayInitializerContext *arrayInitializer();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  VariableInitializerContext* variableInitializer();

  class  UnannTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    UnannTypeContext() = default;
    void copyFrom(UnannTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnannType2Context : public UnannTypeContext {
  public:
    UnannType2Context(UnannTypeContext *ctx);

    UnannReferenceTypeContext *unannReferenceType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnannType1Context : public UnannTypeContext {
  public:
    UnannType1Context(UnannTypeContext *ctx);

    UnannPrimitiveTypeContext *unannPrimitiveType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  UnannTypeContext* unannType();

  class  UnannPrimitiveTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannPrimitiveTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    UnannPrimitiveTypeContext() = default;
    void copyFrom(UnannPrimitiveTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnannPrimitiveType2Context : public UnannPrimitiveTypeContext {
  public:
    UnannPrimitiveType2Context(UnannPrimitiveTypeContext *ctx);

    antlr4::tree::TerminalNode *BOOLEAN();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnannPrimitiveType1Context : public UnannPrimitiveTypeContext {
  public:
    UnannPrimitiveType1Context(UnannPrimitiveTypeContext *ctx);

    NumericTypeContext *numericType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  UnannPrimitiveTypeContext* unannPrimitiveType();

  class  UnannReferenceTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannReferenceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    UnannReferenceTypeContext() = default;
    void copyFrom(UnannReferenceTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnannReferenceType3Context : public UnannReferenceTypeContext {
  public:
    UnannReferenceType3Context(UnannReferenceTypeContext *ctx);

    UnannArrayTypeContext *unannArrayType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnannReferenceType1Context : public UnannReferenceTypeContext {
  public:
    UnannReferenceType1Context(UnannReferenceTypeContext *ctx);

    UnannClassOrInterfaceTypeContext *unannClassOrInterfaceType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnannReferenceType2Context : public UnannReferenceTypeContext {
  public:
    UnannReferenceType2Context(UnannReferenceTypeContext *ctx);

    UnannTypeVariableContext *unannTypeVariable();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  UnannReferenceTypeContext* unannReferenceType();

  class  UnannClassOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannClassOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannClassType_lfno_unannClassOrInterfaceTypeContext *unannClassType_lfno_unannClassOrInterfaceType();
    UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext *unannInterfaceType_lfno_unannClassOrInterfaceType();
    std::vector<UnannClassType_lf_unannClassOrInterfaceTypeContext *> unannClassType_lf_unannClassOrInterfaceType();
    UnannClassType_lf_unannClassOrInterfaceTypeContext* unannClassType_lf_unannClassOrInterfaceType(size_t i);
    std::vector<UnannInterfaceType_lf_unannClassOrInterfaceTypeContext *> unannInterfaceType_lf_unannClassOrInterfaceType();
    UnannInterfaceType_lf_unannClassOrInterfaceTypeContext* unannInterfaceType_lf_unannClassOrInterfaceType(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UnannClassOrInterfaceTypeContext* unannClassOrInterfaceType();

  class  UnannClassTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannClassTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    UnannClassTypeContext() = default;
    void copyFrom(UnannClassTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnannClassType2Context : public UnannClassTypeContext {
  public:
    UnannClassType2Context(UnannClassTypeContext *ctx);

    UnannClassOrInterfaceTypeContext *unannClassOrInterfaceType();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnannClassType1Context : public UnannClassTypeContext {
  public:
    UnannClassType1Context(UnannClassTypeContext *ctx);

    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  UnannClassTypeContext* unannClassType();

  class  UnannClassType_lf_unannClassOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannClassType_lf_unannClassOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsContext *typeArguments();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UnannClassType_lf_unannClassOrInterfaceTypeContext* unannClassType_lf_unannClassOrInterfaceType();

  class  UnannClassType_lfno_unannClassOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannClassType_lfno_unannClassOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UnannClassType_lfno_unannClassOrInterfaceTypeContext* unannClassType_lfno_unannClassOrInterfaceType();

  class  UnannInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannClassTypeContext *unannClassType();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UnannInterfaceTypeContext* unannInterfaceType();

  class  UnannInterfaceType_lf_unannClassOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannInterfaceType_lf_unannClassOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannClassType_lf_unannClassOrInterfaceTypeContext *unannClassType_lf_unannClassOrInterfaceType();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UnannInterfaceType_lf_unannClassOrInterfaceTypeContext* unannInterfaceType_lf_unannClassOrInterfaceType();

  class  UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannClassType_lfno_unannClassOrInterfaceTypeContext *unannClassType_lfno_unannClassOrInterfaceType();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UnannInterfaceType_lfno_unannClassOrInterfaceTypeContext* unannInterfaceType_lfno_unannClassOrInterfaceType();

  class  UnannTypeVariableContext : public antlr4::ParserRuleContext {
  public:
    UnannTypeVariableContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UnannTypeVariableContext* unannTypeVariable();

  class  UnannArrayTypeContext : public antlr4::ParserRuleContext {
  public:
    UnannArrayTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    UnannArrayTypeContext() = default;
    void copyFrom(UnannArrayTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnannArrayType2Context : public UnannArrayTypeContext {
  public:
    UnannArrayType2Context(UnannArrayTypeContext *ctx);

    UnannClassOrInterfaceTypeContext *unannClassOrInterfaceType();
    DimsContext *dims();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnannArrayType1Context : public UnannArrayTypeContext {
  public:
    UnannArrayType1Context(UnannArrayTypeContext *ctx);

    UnannPrimitiveTypeContext *unannPrimitiveType();
    DimsContext *dims();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnannArrayTyp3Context : public UnannArrayTypeContext {
  public:
    UnannArrayTyp3Context(UnannArrayTypeContext *ctx);

    UnannTypeVariableContext *unannTypeVariable();
    DimsContext *dims();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  UnannArrayTypeContext* unannArrayType();

  class  MethodDeclarationContext : public antlr4::ParserRuleContext {
  public:
    MethodDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    MethodHeaderContext *methodHeader();
    MethodBodyContext *methodBody();
    std::vector<MethodModifierContext *> methodModifier();
    MethodModifierContext* methodModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodDeclarationContext* methodDeclaration();

  class  MethodModifierContext : public antlr4::ParserRuleContext {
  public:
    MethodModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *PROTECTED();
    antlr4::tree::TerminalNode *PRIVATE();
    antlr4::tree::TerminalNode *ABSTRACT();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *FINAL();
    antlr4::tree::TerminalNode *SYNCHRONIZED();
    antlr4::tree::TerminalNode *NATIVE();
    antlr4::tree::TerminalNode *STRICTFP();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodModifierContext* methodModifier();

  class  MethodHeaderContext : public antlr4::ParserRuleContext {
  public:
    MethodHeaderContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ResultContext *result();
    MethodDeclaratorContext *methodDeclarator();
    Throws_Context *throws_();
    TypeParametersContext *typeParameters();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodHeaderContext* methodHeader();

  class  ResultContext : public antlr4::ParserRuleContext {
  public:
    ResultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannTypeContext *unannType();
    antlr4::tree::TerminalNode *VOID();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ResultContext* result();

  class  MethodDeclaratorContext : public antlr4::ParserRuleContext {
  public:
    MethodDeclaratorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    FormalParameterListContext *formalParameterList();
    DimsContext *dims();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodDeclaratorContext* methodDeclarator();

  class  FormalParameterListContext : public antlr4::ParserRuleContext {
  public:
    FormalParameterListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    FormalParameterListContext() = default;
    void copyFrom(FormalParameterListContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  FormalParameterList3Context : public FormalParameterListContext {
  public:
    FormalParameterList3Context(FormalParameterListContext *ctx);

    ReceiverParameterContext *receiverParameter();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  FormalParameterList2Context : public FormalParameterListContext {
  public:
    FormalParameterList2Context(FormalParameterListContext *ctx);

    LastFormalParameterContext *lastFormalParameter();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  FormalParameterList1Context : public FormalParameterListContext {
  public:
    FormalParameterList1Context(FormalParameterListContext *ctx);

    FormalParametersContext *formalParameters();
    antlr4::tree::TerminalNode *COMMA();
    LastFormalParameterContext *lastFormalParameter();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  FormalParameterListContext* formalParameterList();

  class  FormalParametersContext : public antlr4::ParserRuleContext {
  public:
    FormalParametersContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    FormalParametersContext() = default;
    void copyFrom(FormalParametersContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  FormalParameters2Context : public FormalParametersContext {
  public:
    FormalParameters2Context(FormalParametersContext *ctx);

    ReceiverParameterContext *receiverParameter();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    std::vector<FormalParameterContext *> formalParameter();
    FormalParameterContext* formalParameter(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  FormalParameters1Context : public FormalParametersContext {
  public:
    FormalParameters1Context(FormalParametersContext *ctx);

    std::vector<FormalParameterContext *> formalParameter();
    FormalParameterContext* formalParameter(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  FormalParametersContext* formalParameters();

  class  FormalParameterContext : public antlr4::ParserRuleContext {
  public:
    FormalParameterContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannTypeContext *unannType();
    VariableDeclaratorIdContext *variableDeclaratorId();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FormalParameterContext* formalParameter();

  class  VariableModifierContext : public antlr4::ParserRuleContext {
  public:
    VariableModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *FINAL();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VariableModifierContext* variableModifier();

  class  LastFormalParameterContext : public antlr4::ParserRuleContext {
  public:
    LastFormalParameterContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    LastFormalParameterContext() = default;
    void copyFrom(LastFormalParameterContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  LastFormalParameter2Context : public LastFormalParameterContext {
  public:
    LastFormalParameter2Context(LastFormalParameterContext *ctx);

    FormalParameterContext *formalParameter();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LastFormalParameter1Context : public LastFormalParameterContext {
  public:
    LastFormalParameter1Context(LastFormalParameterContext *ctx);

    UnannTypeContext *unannType();
    antlr4::tree::TerminalNode *ELLIPSIS();
    VariableDeclaratorIdContext *variableDeclaratorId();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  LastFormalParameterContext* lastFormalParameter();

  class  ReceiverParameterContext : public antlr4::ParserRuleContext {
  public:
    ReceiverParameterContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannTypeContext *unannType();
    antlr4::tree::TerminalNode *THIS();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *DOT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ReceiverParameterContext* receiverParameter();

  class  Throws_Context : public antlr4::ParserRuleContext {
  public:
    Throws_Context(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *THROWS();
    ExceptionTypeListContext *exceptionTypeList();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Throws_Context* throws_();

  class  ExceptionTypeListContext : public antlr4::ParserRuleContext {
  public:
    ExceptionTypeListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExceptionTypeContext *> exceptionType();
    ExceptionTypeContext* exceptionType(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExceptionTypeListContext* exceptionTypeList();

  class  ExceptionTypeContext : public antlr4::ParserRuleContext {
  public:
    ExceptionTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ExceptionTypeContext() = default;
    void copyFrom(ExceptionTypeContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ExceptionType2Context : public ExceptionTypeContext {
  public:
    ExceptionType2Context(ExceptionTypeContext *ctx);

    TypeVariableContext *typeVariable();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ExceptionType1Context : public ExceptionTypeContext {
  public:
    ExceptionType1Context(ExceptionTypeContext *ctx);

    ClassTypeContext *classType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ExceptionTypeContext* exceptionType();

  class  MethodBodyContext : public antlr4::ParserRuleContext {
  public:
    MethodBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    BlockContext *block();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodBodyContext* methodBody();

  class  InstanceInitializerContext : public antlr4::ParserRuleContext {
  public:
    InstanceInitializerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    BlockContext *block();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InstanceInitializerContext* instanceInitializer();

  class  StaticInitializerContext : public antlr4::ParserRuleContext {
  public:
    StaticInitializerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STATIC();
    BlockContext *block();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StaticInitializerContext* staticInitializer();

  class  ConstructorDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ConstructorDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ConstructorDeclaratorContext *constructorDeclarator();
    ConstructorBodyContext *constructorBody();
    std::vector<ConstructorModifierContext *> constructorModifier();
    ConstructorModifierContext* constructorModifier(size_t i);
    Throws_Context *throws_();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstructorDeclarationContext* constructorDeclaration();

  class  ConstructorModifierContext : public antlr4::ParserRuleContext {
  public:
    ConstructorModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *PROTECTED();
    antlr4::tree::TerminalNode *PRIVATE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstructorModifierContext* constructorModifier();

  class  ConstructorDeclaratorContext : public antlr4::ParserRuleContext {
  public:
    ConstructorDeclaratorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SimpleTypeNameContext *simpleTypeName();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeParametersContext *typeParameters();
    FormalParameterListContext *formalParameterList();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstructorDeclaratorContext* constructorDeclarator();

  class  SimpleTypeNameContext : public antlr4::ParserRuleContext {
  public:
    SimpleTypeNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SimpleTypeNameContext* simpleTypeName();

  class  ConstructorBodyContext : public antlr4::ParserRuleContext {
  public:
    ConstructorBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    ExplicitConstructorInvocationContext *explicitConstructorInvocation();
    BlockStatementsContext *blockStatements();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstructorBodyContext* constructorBody();

  class  ExplicitConstructorInvocationContext : public antlr4::ParserRuleContext {
  public:
    ExplicitConstructorInvocationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ExplicitConstructorInvocationContext() = default;
    void copyFrom(ExplicitConstructorInvocationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ExplicitConstructorInvocation1Context : public ExplicitConstructorInvocationContext {
  public:
    ExplicitConstructorInvocation1Context(ExplicitConstructorInvocationContext *ctx);

    antlr4::tree::TerminalNode *THIS();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    antlr4::tree::TerminalNode *SEMI();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ExplicitConstructorInvocation4Context : public ExplicitConstructorInvocationContext {
  public:
    ExplicitConstructorInvocation4Context(ExplicitConstructorInvocationContext *ctx);

    PrimaryContext *primary();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    antlr4::tree::TerminalNode *SEMI();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ExplicitConstructorInvocation2Context : public ExplicitConstructorInvocationContext {
  public:
    ExplicitConstructorInvocation2Context(ExplicitConstructorInvocationContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    antlr4::tree::TerminalNode *SEMI();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ExplicitConstructorInvocation3Context : public ExplicitConstructorInvocationContext {
  public:
    ExplicitConstructorInvocation3Context(ExplicitConstructorInvocationContext *ctx);

    ExpressionNameContext *expressionName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    antlr4::tree::TerminalNode *SEMI();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ExplicitConstructorInvocationContext* explicitConstructorInvocation();

  class  EnumDeclarationContext : public antlr4::ParserRuleContext {
  public:
    EnumDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ENUM();
    IdentifierContext *identifier();
    EnumBodyContext *enumBody();
    std::vector<ClassModifierContext *> classModifier();
    ClassModifierContext* classModifier(size_t i);
    SuperinterfacesContext *superinterfaces();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumDeclarationContext* enumDeclaration();

  class  EnumBodyContext : public antlr4::ParserRuleContext {
  public:
    EnumBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    EnumConstantListContext *enumConstantList();
    antlr4::tree::TerminalNode *COMMA();
    EnumBodyDeclarationsContext *enumBodyDeclarations();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumBodyContext* enumBody();

  class  EnumConstantListContext : public antlr4::ParserRuleContext {
  public:
    EnumConstantListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<EnumConstantContext *> enumConstant();
    EnumConstantContext* enumConstant(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumConstantListContext* enumConstantList();

  class  EnumConstantContext : public antlr4::ParserRuleContext {
  public:
    EnumConstantContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    std::vector<EnumConstantModifierContext *> enumConstantModifier();
    EnumConstantModifierContext* enumConstantModifier(size_t i);
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ClassBodyContext *classBody();
    ArgumentListContext *argumentList();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumConstantContext* enumConstant();

  class  EnumConstantModifierContext : public antlr4::ParserRuleContext {
  public:
    EnumConstantModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumConstantModifierContext* enumConstantModifier();

  class  EnumBodyDeclarationsContext : public antlr4::ParserRuleContext {
  public:
    EnumBodyDeclarationsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *SEMI();
    std::vector<ClassBodyDeclarationContext *> classBodyDeclaration();
    ClassBodyDeclarationContext* classBodyDeclaration(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumBodyDeclarationsContext* enumBodyDeclarations();

  class  InterfaceDeclarationContext : public antlr4::ParserRuleContext {
  public:
    InterfaceDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    InterfaceDeclarationContext() = default;
    void copyFrom(InterfaceDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  InterfaceDeclaration1Context : public InterfaceDeclarationContext {
  public:
    InterfaceDeclaration1Context(InterfaceDeclarationContext *ctx);

    NormalInterfaceDeclarationContext *normalInterfaceDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceDeclaration2Context : public InterfaceDeclarationContext {
  public:
    InterfaceDeclaration2Context(InterfaceDeclarationContext *ctx);

    AnnotationTypeDeclarationContext *annotationTypeDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  InterfaceDeclarationContext* interfaceDeclaration();

  class  NormalInterfaceDeclarationContext : public antlr4::ParserRuleContext {
  public:
    NormalInterfaceDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *INTERFACE();
    IdentifierContext *identifier();
    InterfaceBodyContext *interfaceBody();
    std::vector<InterfaceModifierContext *> interfaceModifier();
    InterfaceModifierContext* interfaceModifier(size_t i);
    TypeParametersContext *typeParameters();
    ExtendsInterfacesContext *extendsInterfaces();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  NormalInterfaceDeclarationContext* normalInterfaceDeclaration();

  class  InterfaceModifierContext : public antlr4::ParserRuleContext {
  public:
    InterfaceModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *PROTECTED();
    antlr4::tree::TerminalNode *PRIVATE();
    antlr4::tree::TerminalNode *ABSTRACT();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *STRICTFP();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceModifierContext* interfaceModifier();

  class  ExtendsInterfacesContext : public antlr4::ParserRuleContext {
  public:
    ExtendsInterfacesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EXTENDS();
    InterfaceTypeListContext *interfaceTypeList();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExtendsInterfacesContext* extendsInterfaces();

  class  InterfaceBodyContext : public antlr4::ParserRuleContext {
  public:
    InterfaceBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<InterfaceMemberDeclarationContext *> interfaceMemberDeclaration();
    InterfaceMemberDeclarationContext* interfaceMemberDeclaration(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceBodyContext* interfaceBody();

  class  InterfaceMemberDeclarationContext : public antlr4::ParserRuleContext {
  public:
    InterfaceMemberDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    InterfaceMemberDeclarationContext() = default;
    void copyFrom(InterfaceMemberDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  InterfaceMemberDeclaration5Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration5Context(InterfaceMemberDeclarationContext *ctx);

    antlr4::tree::TerminalNode *SEMI();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration4Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration4Context(InterfaceMemberDeclarationContext *ctx);

    InterfaceDeclarationContext *interfaceDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration3Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration3Context(InterfaceMemberDeclarationContext *ctx);

    ClassDeclarationContext *classDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration2Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration2Context(InterfaceMemberDeclarationContext *ctx);

    InterfaceMethodDeclarationContext *interfaceMethodDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration1Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration1Context(InterfaceMemberDeclarationContext *ctx);

    ConstantDeclarationContext *constantDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  InterfaceMemberDeclarationContext* interfaceMemberDeclaration();

  class  ConstantDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ConstantDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannTypeContext *unannType();
    VariableDeclaratorListContext *variableDeclaratorList();
    antlr4::tree::TerminalNode *SEMI();
    std::vector<ConstantModifierContext *> constantModifier();
    ConstantModifierContext* constantModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstantDeclarationContext* constantDeclaration();

  class  ConstantModifierContext : public antlr4::ParserRuleContext {
  public:
    ConstantModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *FINAL();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstantModifierContext* constantModifier();

  class  InterfaceMethodDeclarationContext : public antlr4::ParserRuleContext {
  public:
    InterfaceMethodDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    MethodHeaderContext *methodHeader();
    MethodBodyContext *methodBody();
    std::vector<InterfaceMethodModifierContext *> interfaceMethodModifier();
    InterfaceMethodModifierContext* interfaceMethodModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceMethodDeclarationContext* interfaceMethodDeclaration();

  class  InterfaceMethodModifierContext : public antlr4::ParserRuleContext {
  public:
    InterfaceMethodModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *PRIVATE();
    antlr4::tree::TerminalNode *ABSTRACT();
    antlr4::tree::TerminalNode *DEFAULT();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *STRICTFP();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceMethodModifierContext* interfaceMethodModifier();

  class  AnnotationTypeDeclarationContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AT();
    antlr4::tree::TerminalNode *INTERFACE();
    IdentifierContext *identifier();
    AnnotationTypeBodyContext *annotationTypeBody();
    std::vector<InterfaceModifierContext *> interfaceModifier();
    InterfaceModifierContext* interfaceModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationTypeDeclarationContext* annotationTypeDeclaration();

  class  AnnotationTypeBodyContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<AnnotationTypeMemberDeclarationContext *> annotationTypeMemberDeclaration();
    AnnotationTypeMemberDeclarationContext* annotationTypeMemberDeclaration(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationTypeBodyContext* annotationTypeBody();

  class  AnnotationTypeMemberDeclarationContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeMemberDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AnnotationTypeMemberDeclarationContext() = default;
    void copyFrom(AnnotationTypeMemberDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  AnnotationTypeMemberDeclaration1Context : public AnnotationTypeMemberDeclarationContext {
  public:
    AnnotationTypeMemberDeclaration1Context(AnnotationTypeMemberDeclarationContext *ctx);

    AnnotationTypeElementDeclarationContext *annotationTypeElementDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationTypeMemberDeclaration2Context : public AnnotationTypeMemberDeclarationContext {
  public:
    AnnotationTypeMemberDeclaration2Context(AnnotationTypeMemberDeclarationContext *ctx);

    ConstantDeclarationContext *constantDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationTypeMemberDeclaration3Context : public AnnotationTypeMemberDeclarationContext {
  public:
    AnnotationTypeMemberDeclaration3Context(AnnotationTypeMemberDeclarationContext *ctx);

    ClassDeclarationContext *classDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationTypeMemberDeclaration4Context : public AnnotationTypeMemberDeclarationContext {
  public:
    AnnotationTypeMemberDeclaration4Context(AnnotationTypeMemberDeclarationContext *ctx);

    InterfaceDeclarationContext *interfaceDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationTypeMemberDeclaration5Context : public AnnotationTypeMemberDeclarationContext {
  public:
    AnnotationTypeMemberDeclaration5Context(AnnotationTypeMemberDeclarationContext *ctx);

    antlr4::tree::TerminalNode *SEMI();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AnnotationTypeMemberDeclarationContext* annotationTypeMemberDeclaration();

  class  AnnotationTypeElementDeclarationContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeElementDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannTypeContext *unannType();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    antlr4::tree::TerminalNode *SEMI();
    std::vector<AnnotationTypeElementModifierContext *> annotationTypeElementModifier();
    AnnotationTypeElementModifierContext* annotationTypeElementModifier(size_t i);
    DimsContext *dims();
    DefaultValueContext *defaultValue();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationTypeElementDeclarationContext* annotationTypeElementDeclaration();

  class  AnnotationTypeElementModifierContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeElementModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *ABSTRACT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationTypeElementModifierContext* annotationTypeElementModifier();

  class  DefaultValueContext : public antlr4::ParserRuleContext {
  public:
    DefaultValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DEFAULT();
    ElementValueContext *elementValue();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DefaultValueContext* defaultValue();

  class  AnnotationContext : public antlr4::ParserRuleContext {
  public:
    AnnotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AnnotationContext() = default;
    void copyFrom(AnnotationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Annotation3Context : public AnnotationContext {
  public:
    Annotation3Context(AnnotationContext *ctx);

    SingleElementAnnotationContext *singleElementAnnotation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Annotation2Context : public AnnotationContext {
  public:
    Annotation2Context(AnnotationContext *ctx);

    MarkerAnnotationContext *markerAnnotation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Annotation1Context : public AnnotationContext {
  public:
    Annotation1Context(AnnotationContext *ctx);

    NormalAnnotationContext *normalAnnotation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AnnotationContext* annotation();

  class  NormalAnnotationContext : public antlr4::ParserRuleContext {
  public:
    NormalAnnotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AT();
    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ElementValuePairListContext *elementValuePairList();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  NormalAnnotationContext* normalAnnotation();

  class  ElementValuePairListContext : public antlr4::ParserRuleContext {
  public:
    ElementValuePairListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ElementValuePairContext *> elementValuePair();
    ElementValuePairContext* elementValuePair(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ElementValuePairListContext* elementValuePairList();

  class  ElementValuePairContext : public antlr4::ParserRuleContext {
  public:
    ElementValuePairContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *ASSIGN();
    ElementValueContext *elementValue();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ElementValuePairContext* elementValuePair();

  class  ElementValueContext : public antlr4::ParserRuleContext {
  public:
    ElementValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ElementValueContext() = default;
    void copyFrom(ElementValueContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ElementValue2Context : public ElementValueContext {
  public:
    ElementValue2Context(ElementValueContext *ctx);

    ElementValueArrayInitializerContext *elementValueArrayInitializer();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ElementValue1Context : public ElementValueContext {
  public:
    ElementValue1Context(ElementValueContext *ctx);

    ConditionalExpressionContext *conditionalExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ElementValu3Context : public ElementValueContext {
  public:
    ElementValu3Context(ElementValueContext *ctx);

    AnnotationContext *annotation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ElementValueContext* elementValue();

  class  ElementValueArrayInitializerContext : public antlr4::ParserRuleContext {
  public:
    ElementValueArrayInitializerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    ElementValueListContext *elementValueList();
    antlr4::tree::TerminalNode *COMMA();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ElementValueArrayInitializerContext* elementValueArrayInitializer();

  class  ElementValueListContext : public antlr4::ParserRuleContext {
  public:
    ElementValueListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ElementValueContext *> elementValue();
    ElementValueContext* elementValue(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ElementValueListContext* elementValueList();

  class  MarkerAnnotationContext : public antlr4::ParserRuleContext {
  public:
    MarkerAnnotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AT();
    TypeNameContext *typeName();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MarkerAnnotationContext* markerAnnotation();

  class  SingleElementAnnotationContext : public antlr4::ParserRuleContext {
  public:
    SingleElementAnnotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AT();
    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *LPAREN();
    ElementValueContext *elementValue();
    antlr4::tree::TerminalNode *RPAREN();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SingleElementAnnotationContext* singleElementAnnotation();

  class  ArrayInitializerContext : public antlr4::ParserRuleContext {
  public:
    ArrayInitializerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    VariableInitializerListContext *variableInitializerList();
    antlr4::tree::TerminalNode *COMMA();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArrayInitializerContext* arrayInitializer();

  class  VariableInitializerListContext : public antlr4::ParserRuleContext {
  public:
    VariableInitializerListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<VariableInitializerContext *> variableInitializer();
    VariableInitializerContext* variableInitializer(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VariableInitializerListContext* variableInitializerList();

  class  BlockContext : public antlr4::ParserRuleContext {
  public:
    BlockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    BlockStatementsContext *blockStatements();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  BlockContext* block();

  class  BlockStatementsContext : public antlr4::ParserRuleContext {
  public:
    BlockStatementsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<BlockStatementContext *> blockStatement();
    BlockStatementContext* blockStatement(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  BlockStatementsContext* blockStatements();

  class  BlockStatementContext : public antlr4::ParserRuleContext {
  public:
    BlockStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    BlockStatementContext() = default;
    void copyFrom(BlockStatementContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  BlockStatement1Context : public BlockStatementContext {
  public:
    BlockStatement1Context(BlockStatementContext *ctx);

    LocalVariableDeclarationStatementContext *localVariableDeclarationStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  BlockStatement3Context : public BlockStatementContext {
  public:
    BlockStatement3Context(BlockStatementContext *ctx);

    StatementContext *statement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  BlockStatement2Context : public BlockStatementContext {
  public:
    BlockStatement2Context(BlockStatementContext *ctx);

    ClassDeclarationContext *classDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  BlockStatementContext* blockStatement();

  class  LocalVariableDeclarationStatementContext : public antlr4::ParserRuleContext {
  public:
    LocalVariableDeclarationStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    LocalVariableDeclarationContext *localVariableDeclaration();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LocalVariableDeclarationStatementContext* localVariableDeclarationStatement();

  class  LocalVariableDeclarationContext : public antlr4::ParserRuleContext {
  public:
    LocalVariableDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannTypeContext *unannType();
    VariableDeclaratorListContext *variableDeclaratorList();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LocalVariableDeclarationContext* localVariableDeclaration();

  class  StatementContext : public antlr4::ParserRuleContext {
  public:
    StatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    StatementContext() = default;
    void copyFrom(StatementContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Statement5Context : public StatementContext {
  public:
    Statement5Context(StatementContext *ctx);

    WhileStatementContext *whileStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement6Context : public StatementContext {
  public:
    Statement6Context(StatementContext *ctx);

    ForStatementContext *forStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement3Context : public StatementContext {
  public:
    Statement3Context(StatementContext *ctx);

    IfThenStatementContext *ifThenStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement4Context : public StatementContext {
  public:
    Statement4Context(StatementContext *ctx);

    IfThenElseStatementContext *ifThenElseStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement1Context : public StatementContext {
  public:
    Statement1Context(StatementContext *ctx);

    StatementWithoutTrailingSubstatementContext *statementWithoutTrailingSubstatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement2Context : public StatementContext {
  public:
    Statement2Context(StatementContext *ctx);

    LabeledStatementContext *labeledStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  StatementContext* statement();

  class  StatementNoShortIfContext : public antlr4::ParserRuleContext {
  public:
    StatementNoShortIfContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    StatementNoShortIfContext() = default;
    void copyFrom(StatementNoShortIfContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  StatementNoShortIf5Context : public StatementNoShortIfContext {
  public:
    StatementNoShortIf5Context(StatementNoShortIfContext *ctx);

    ForStatementNoShortIfContext *forStatementNoShortIf();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementNoShortIf2Context : public StatementNoShortIfContext {
  public:
    StatementNoShortIf2Context(StatementNoShortIfContext *ctx);

    LabeledStatementNoShortIfContext *labeledStatementNoShortIf();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementNoShortIf1Context : public StatementNoShortIfContext {
  public:
    StatementNoShortIf1Context(StatementNoShortIfContext *ctx);

    StatementWithoutTrailingSubstatementContext *statementWithoutTrailingSubstatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementNoShortIf4Context : public StatementNoShortIfContext {
  public:
    StatementNoShortIf4Context(StatementNoShortIfContext *ctx);

    WhileStatementNoShortIfContext *whileStatementNoShortIf();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementNoShortIf3Context : public StatementNoShortIfContext {
  public:
    StatementNoShortIf3Context(StatementNoShortIfContext *ctx);

    IfThenElseStatementNoShortIfContext *ifThenElseStatementNoShortIf();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  StatementNoShortIfContext* statementNoShortIf();

  class  StatementWithoutTrailingSubstatementContext : public antlr4::ParserRuleContext {
  public:
    StatementWithoutTrailingSubstatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    StatementWithoutTrailingSubstatementContext() = default;
    void copyFrom(StatementWithoutTrailingSubstatementContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  StatementWithoutTrailingSubstatement8Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement8Context(StatementWithoutTrailingSubstatementContext *ctx);

    ContinueStatementContext *continueStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement9Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement9Context(StatementWithoutTrailingSubstatementContext *ctx);

    ReturnStatementContext *returnStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement4Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement4Context(StatementWithoutTrailingSubstatementContext *ctx);

    AssertStatementContext *assertStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement5Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement5Context(StatementWithoutTrailingSubstatementContext *ctx);

    SwitchStatementContext *switchStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement6Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement6Context(StatementWithoutTrailingSubstatementContext *ctx);

    DoStatementContext *doStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement7Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement7Context(StatementWithoutTrailingSubstatementContext *ctx);

    BreakStatementContext *breakStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement1Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement1Context(StatementWithoutTrailingSubstatementContext *ctx);

    BlockContext *block();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement10Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement10Context(StatementWithoutTrailingSubstatementContext *ctx);

    SynchronizedStatementContext *synchronizedStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement2Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement2Context(StatementWithoutTrailingSubstatementContext *ctx);

    EmptyStatementContext *emptyStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement3Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement3Context(StatementWithoutTrailingSubstatementContext *ctx);

    ExpressionStatementContext *expressionStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement11Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement11Context(StatementWithoutTrailingSubstatementContext *ctx);

    ThrowStatementContext *throwStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementWithoutTrailingSubstatement12Context : public StatementWithoutTrailingSubstatementContext {
  public:
    StatementWithoutTrailingSubstatement12Context(StatementWithoutTrailingSubstatementContext *ctx);

    TryStatementContext *tryStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  StatementWithoutTrailingSubstatementContext* statementWithoutTrailingSubstatement();

  class  EmptyStatementContext : public antlr4::ParserRuleContext {
  public:
    EmptyStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EmptyStatementContext* emptyStatement();

  class  LabeledStatementContext : public antlr4::ParserRuleContext {
  public:
    LabeledStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *COLON();
    StatementContext *statement();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LabeledStatementContext* labeledStatement();

  class  LabeledStatementNoShortIfContext : public antlr4::ParserRuleContext {
  public:
    LabeledStatementNoShortIfContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *COLON();
    StatementNoShortIfContext *statementNoShortIf();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LabeledStatementNoShortIfContext* labeledStatementNoShortIf();

  class  ExpressionStatementContext : public antlr4::ParserRuleContext {
  public:
    ExpressionStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    StatementExpressionContext *statementExpression();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExpressionStatementContext* expressionStatement();

  class  StatementExpressionContext : public antlr4::ParserRuleContext {
  public:
    StatementExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    StatementExpressionContext() = default;
    void copyFrom(StatementExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  StatementExpression3Context : public StatementExpressionContext {
  public:
    StatementExpression3Context(StatementExpressionContext *ctx);

    PreDecrementExpressionContext *preDecrementExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementExpression4Context : public StatementExpressionContext {
  public:
    StatementExpression4Context(StatementExpressionContext *ctx);

    PostIncrementExpressionContext *postIncrementExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementExpression5Context : public StatementExpressionContext {
  public:
    StatementExpression5Context(StatementExpressionContext *ctx);

    PostDecrementExpressionContext *postDecrementExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementExpression6Context : public StatementExpressionContext {
  public:
    StatementExpression6Context(StatementExpressionContext *ctx);

    MethodInvocationContext *methodInvocation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementExpression1Context : public StatementExpressionContext {
  public:
    StatementExpression1Context(StatementExpressionContext *ctx);

    AssignmentContext *assignment();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementExpression2Context : public StatementExpressionContext {
  public:
    StatementExpression2Context(StatementExpressionContext *ctx);

    PreIncrementExpressionContext *preIncrementExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  StatementExpression7Context : public StatementExpressionContext {
  public:
    StatementExpression7Context(StatementExpressionContext *ctx);

    ClassInstanceCreationExpressionContext *classInstanceCreationExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  StatementExpressionContext* statementExpression();

  class  IfThenStatementContext : public antlr4::ParserRuleContext {
  public:
    IfThenStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IF();
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    StatementContext *statement();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IfThenStatementContext* ifThenStatement();

  class  IfThenElseStatementContext : public antlr4::ParserRuleContext {
  public:
    IfThenElseStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IF();
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    StatementNoShortIfContext *statementNoShortIf();
    antlr4::tree::TerminalNode *ELSE();
    StatementContext *statement();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IfThenElseStatementContext* ifThenElseStatement();

  class  IfThenElseStatementNoShortIfContext : public antlr4::ParserRuleContext {
  public:
    IfThenElseStatementNoShortIfContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IF();
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    std::vector<StatementNoShortIfContext *> statementNoShortIf();
    StatementNoShortIfContext* statementNoShortIf(size_t i);
    antlr4::tree::TerminalNode *ELSE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IfThenElseStatementNoShortIfContext* ifThenElseStatementNoShortIf();

  class  AssertStatementContext : public antlr4::ParserRuleContext {
  public:
    AssertStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AssertStatementContext() = default;
    void copyFrom(AssertStatementContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  AssertStatement2Context : public AssertStatementContext {
  public:
    AssertStatement2Context(AssertStatementContext *ctx);

    antlr4::tree::TerminalNode *ASSERT();
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *COLON();
    antlr4::tree::TerminalNode *SEMI();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AssertStatement1Context : public AssertStatementContext {
  public:
    AssertStatement1Context(AssertStatementContext *ctx);

    antlr4::tree::TerminalNode *ASSERT();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *SEMI();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AssertStatementContext* assertStatement();

  class  SwitchStatementContext : public antlr4::ParserRuleContext {
  public:
    SwitchStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *SWITCH();
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    SwitchBlockContext *switchBlock();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SwitchStatementContext* switchStatement();

  class  SwitchBlockContext : public antlr4::ParserRuleContext {
  public:
    SwitchBlockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<SwitchBlockStatementGroupContext *> switchBlockStatementGroup();
    SwitchBlockStatementGroupContext* switchBlockStatementGroup(size_t i);
    std::vector<SwitchLabelContext *> switchLabel();
    SwitchLabelContext* switchLabel(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SwitchBlockContext* switchBlock();

  class  SwitchBlockStatementGroupContext : public antlr4::ParserRuleContext {
  public:
    SwitchBlockStatementGroupContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SwitchLabelsContext *switchLabels();
    BlockStatementsContext *blockStatements();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SwitchBlockStatementGroupContext* switchBlockStatementGroup();

  class  SwitchLabelsContext : public antlr4::ParserRuleContext {
  public:
    SwitchLabelsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<SwitchLabelContext *> switchLabel();
    SwitchLabelContext* switchLabel(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SwitchLabelsContext* switchLabels();

  class  SwitchLabelContext : public antlr4::ParserRuleContext {
  public:
    SwitchLabelContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    SwitchLabelContext() = default;
    void copyFrom(SwitchLabelContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  SwitchLabel3Context : public SwitchLabelContext {
  public:
    SwitchLabel3Context(SwitchLabelContext *ctx);

    antlr4::tree::TerminalNode *DEFAULT();
    antlr4::tree::TerminalNode *COLON();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  SwitchLabel2Context : public SwitchLabelContext {
  public:
    SwitchLabel2Context(SwitchLabelContext *ctx);

    antlr4::tree::TerminalNode *CASE();
    EnumConstantNameContext *enumConstantName();
    antlr4::tree::TerminalNode *COLON();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  SwitchLabel1Context : public SwitchLabelContext {
  public:
    SwitchLabel1Context(SwitchLabelContext *ctx);

    antlr4::tree::TerminalNode *CASE();
    ConstantExpressionContext *constantExpression();
    antlr4::tree::TerminalNode *COLON();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  SwitchLabelContext* switchLabel();

  class  EnumConstantNameContext : public antlr4::ParserRuleContext {
  public:
    EnumConstantNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumConstantNameContext* enumConstantName();

  class  WhileStatementContext : public antlr4::ParserRuleContext {
  public:
    WhileStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *WHILE();
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    StatementContext *statement();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  WhileStatementContext* whileStatement();

  class  WhileStatementNoShortIfContext : public antlr4::ParserRuleContext {
  public:
    WhileStatementNoShortIfContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *WHILE();
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    StatementNoShortIfContext *statementNoShortIf();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  WhileStatementNoShortIfContext* whileStatementNoShortIf();

  class  DoStatementContext : public antlr4::ParserRuleContext {
  public:
    DoStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DO();
    StatementContext *statement();
    antlr4::tree::TerminalNode *WHILE();
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DoStatementContext* doStatement();

  class  ForStatementContext : public antlr4::ParserRuleContext {
  public:
    ForStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ForStatementContext() = default;
    void copyFrom(ForStatementContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ForStatement1Context : public ForStatementContext {
  public:
    ForStatement1Context(ForStatementContext *ctx);

    BasicForStatementContext *basicForStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ForStatement2Context : public ForStatementContext {
  public:
    ForStatement2Context(ForStatementContext *ctx);

    EnhancedForStatementContext *enhancedForStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ForStatementContext* forStatement();

  class  ForStatementNoShortIfContext : public antlr4::ParserRuleContext {
  public:
    ForStatementNoShortIfContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ForStatementNoShortIfContext() = default;
    void copyFrom(ForStatementNoShortIfContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ForStatementNoShortIf3Context : public ForStatementNoShortIfContext {
  public:
    ForStatementNoShortIf3Context(ForStatementNoShortIfContext *ctx);

    BasicForStatementNoShortIfContext *basicForStatementNoShortIf();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ForStatementNoShortIf4Context : public ForStatementNoShortIfContext {
  public:
    ForStatementNoShortIf4Context(ForStatementNoShortIfContext *ctx);

    EnhancedForStatementNoShortIfContext *enhancedForStatementNoShortIf();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ForStatementNoShortIfContext* forStatementNoShortIf();

  class  BasicForStatementContext : public antlr4::ParserRuleContext {
  public:
    BasicForStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FOR();
    antlr4::tree::TerminalNode *LPAREN();
    std::vector<antlr4::tree::TerminalNode *> SEMI();
    antlr4::tree::TerminalNode* SEMI(size_t i);
    antlr4::tree::TerminalNode *RPAREN();
    StatementContext *statement();
    ForInitContext *forInit();
    ExpressionContext *expression();
    ForUpdateContext *forUpdate();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  BasicForStatementContext* basicForStatement();

  class  BasicForStatementNoShortIfContext : public antlr4::ParserRuleContext {
  public:
    BasicForStatementNoShortIfContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FOR();
    antlr4::tree::TerminalNode *LPAREN();
    std::vector<antlr4::tree::TerminalNode *> SEMI();
    antlr4::tree::TerminalNode* SEMI(size_t i);
    antlr4::tree::TerminalNode *RPAREN();
    StatementNoShortIfContext *statementNoShortIf();
    ForInitContext *forInit();
    ExpressionContext *expression();
    ForUpdateContext *forUpdate();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  BasicForStatementNoShortIfContext* basicForStatementNoShortIf();

  class  ForInitContext : public antlr4::ParserRuleContext {
  public:
    ForInitContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ForInitContext() = default;
    void copyFrom(ForInitContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ForInit1Context : public ForInitContext {
  public:
    ForInit1Context(ForInitContext *ctx);

    StatementExpressionListContext *statementExpressionList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ForInit2Context : public ForInitContext {
  public:
    ForInit2Context(ForInitContext *ctx);

    LocalVariableDeclarationContext *localVariableDeclaration();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ForInitContext* forInit();

  class  ForUpdateContext : public antlr4::ParserRuleContext {
  public:
    ForUpdateContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    StatementExpressionListContext *statementExpressionList();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ForUpdateContext* forUpdate();

  class  StatementExpressionListContext : public antlr4::ParserRuleContext {
  public:
    StatementExpressionListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<StatementExpressionContext *> statementExpression();
    StatementExpressionContext* statementExpression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StatementExpressionListContext* statementExpressionList();

  class  EnhancedForStatementContext : public antlr4::ParserRuleContext {
  public:
    EnhancedForStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FOR();
    antlr4::tree::TerminalNode *LPAREN();
    UnannTypeContext *unannType();
    VariableDeclaratorIdContext *variableDeclaratorId();
    antlr4::tree::TerminalNode *COLON();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    StatementContext *statement();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnhancedForStatementContext* enhancedForStatement();

  class  EnhancedForStatementNoShortIfContext : public antlr4::ParserRuleContext {
  public:
    EnhancedForStatementNoShortIfContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FOR();
    antlr4::tree::TerminalNode *LPAREN();
    UnannTypeContext *unannType();
    VariableDeclaratorIdContext *variableDeclaratorId();
    antlr4::tree::TerminalNode *COLON();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    StatementNoShortIfContext *statementNoShortIf();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnhancedForStatementNoShortIfContext* enhancedForStatementNoShortIf();

  class  BreakStatementContext : public antlr4::ParserRuleContext {
  public:
    BreakStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *BREAK();
    antlr4::tree::TerminalNode *SEMI();
    IdentifierContext *identifier();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  BreakStatementContext* breakStatement();

  class  ContinueStatementContext : public antlr4::ParserRuleContext {
  public:
    ContinueStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CONTINUE();
    antlr4::tree::TerminalNode *SEMI();
    IdentifierContext *identifier();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ContinueStatementContext* continueStatement();

  class  ReturnStatementContext : public antlr4::ParserRuleContext {
  public:
    ReturnStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *RETURN();
    antlr4::tree::TerminalNode *SEMI();
    ExpressionContext *expression();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ReturnStatementContext* returnStatement();

  class  ThrowStatementContext : public antlr4::ParserRuleContext {
  public:
    ThrowStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *THROW();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ThrowStatementContext* throwStatement();

  class  SynchronizedStatementContext : public antlr4::ParserRuleContext {
  public:
    SynchronizedStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *SYNCHRONIZED();
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    BlockContext *block();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SynchronizedStatementContext* synchronizedStatement();

  class  TryStatementContext : public antlr4::ParserRuleContext {
  public:
    TryStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    TryStatementContext() = default;
    void copyFrom(TryStatementContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  TryStatement2Context : public TryStatementContext {
  public:
    TryStatement2Context(TryStatementContext *ctx);

    antlr4::tree::TerminalNode *TRY();
    BlockContext *block();
    Finally_Context *finally_();
    CatchesContext *catches();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  TryStatement3Context : public TryStatementContext {
  public:
    TryStatement3Context(TryStatementContext *ctx);

    TryWithResourcesStatementContext *tryWithResourcesStatement();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  TryStatement1Context : public TryStatementContext {
  public:
    TryStatement1Context(TryStatementContext *ctx);

    antlr4::tree::TerminalNode *TRY();
    BlockContext *block();
    CatchesContext *catches();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  TryStatementContext* tryStatement();

  class  CatchesContext : public antlr4::ParserRuleContext {
  public:
    CatchesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<CatchClauseContext *> catchClause();
    CatchClauseContext* catchClause(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  CatchesContext* catches();

  class  CatchClauseContext : public antlr4::ParserRuleContext {
  public:
    CatchClauseContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CATCH();
    antlr4::tree::TerminalNode *LPAREN();
    CatchFormalParameterContext *catchFormalParameter();
    antlr4::tree::TerminalNode *RPAREN();
    BlockContext *block();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  CatchClauseContext* catchClause();

  class  CatchFormalParameterContext : public antlr4::ParserRuleContext {
  public:
    CatchFormalParameterContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    CatchTypeContext *catchType();
    VariableDeclaratorIdContext *variableDeclaratorId();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  CatchFormalParameterContext* catchFormalParameter();

  class  CatchTypeContext : public antlr4::ParserRuleContext {
  public:
    CatchTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnannClassTypeContext *unannClassType();
    std::vector<antlr4::tree::TerminalNode *> BITOR();
    antlr4::tree::TerminalNode* BITOR(size_t i);
    std::vector<ClassTypeContext *> classType();
    ClassTypeContext* classType(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  CatchTypeContext* catchType();

  class  Finally_Context : public antlr4::ParserRuleContext {
  public:
    Finally_Context(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FINALLY();
    BlockContext *block();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Finally_Context* finally_();

  class  TryWithResourcesStatementContext : public antlr4::ParserRuleContext {
  public:
    TryWithResourcesStatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *TRY();
    ResourceSpecificationContext *resourceSpecification();
    BlockContext *block();
    CatchesContext *catches();
    Finally_Context *finally_();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TryWithResourcesStatementContext* tryWithResourcesStatement();

  class  ResourceSpecificationContext : public antlr4::ParserRuleContext {
  public:
    ResourceSpecificationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LPAREN();
    ResourceListContext *resourceList();
    antlr4::tree::TerminalNode *RPAREN();
    antlr4::tree::TerminalNode *SEMI();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ResourceSpecificationContext* resourceSpecification();

  class  ResourceListContext : public antlr4::ParserRuleContext {
  public:
    ResourceListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ResourceContext *> resource();
    ResourceContext* resource(size_t i);
    std::vector<antlr4::tree::TerminalNode *> SEMI();
    antlr4::tree::TerminalNode* SEMI(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ResourceListContext* resourceList();

  class  ResourceContext : public antlr4::ParserRuleContext {
  public:
    ResourceContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ResourceContext() = default;
    void copyFrom(ResourceContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Resource2Context : public ResourceContext {
  public:
    Resource2Context(ResourceContext *ctx);

    VariableAccessContext *variableAccess();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Resource1Context : public ResourceContext {
  public:
    Resource1Context(ResourceContext *ctx);

    UnannTypeContext *unannType();
    VariableDeclaratorIdContext *variableDeclaratorId();
    antlr4::tree::TerminalNode *ASSIGN();
    ExpressionContext *expression();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ResourceContext* resource();

  class  VariableAccessContext : public antlr4::ParserRuleContext {
  public:
    VariableAccessContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    VariableAccessContext() = default;
    void copyFrom(VariableAccessContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  VariableAccess1Context : public VariableAccessContext {
  public:
    VariableAccess1Context(VariableAccessContext *ctx);

    ExpressionNameContext *expressionName();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  VariableAccess2Context : public VariableAccessContext {
  public:
    VariableAccess2Context(VariableAccessContext *ctx);

    FieldAccessContext *fieldAccess();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  VariableAccessContext* variableAccess();

  class  PrimaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    PrimaryNoNewArray_lfno_primaryContext *primaryNoNewArray_lfno_primary();
    ArrayCreationExpressionContext *arrayCreationExpression();
    std::vector<PrimaryNoNewArray_lf_primaryContext *> primaryNoNewArray_lf_primary();
    PrimaryNoNewArray_lf_primaryContext* primaryNoNewArray_lf_primary(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PrimaryContext* primary();

  class  PrimaryNoNewArrayContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArrayContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PrimaryNoNewArrayContext() = default;
    void copyFrom(PrimaryNoNewArrayContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PrimaryNoNewArray1Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray1Context(PrimaryNoNewArrayContext *ctx);

    LiteralContext *literal();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray2Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray2Context(PrimaryNoNewArrayContext *ctx);

    ClassLiteralContext *classLiteral();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray3Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray3Context(PrimaryNoNewArrayContext *ctx);

    antlr4::tree::TerminalNode *THIS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray8Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray8Context(PrimaryNoNewArrayContext *ctx);

    ArrayAccessContext *arrayAccess();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray9Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray9Context(PrimaryNoNewArrayContext *ctx);

    MethodInvocationContext *methodInvocation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray4Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray4Context(PrimaryNoNewArrayContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *THIS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray5Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray5Context(PrimaryNoNewArrayContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray6Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray6Context(PrimaryNoNewArrayContext *ctx);

    ClassInstanceCreationExpressionContext *classInstanceCreationExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray10Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray10Context(PrimaryNoNewArrayContext *ctx);

    MethodReferenceContext *methodReference();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray7Context : public PrimaryNoNewArrayContext {
  public:
    PrimaryNoNewArray7Context(PrimaryNoNewArrayContext *ctx);

    FieldAccessContext *fieldAccess();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PrimaryNoNewArrayContext* primaryNoNewArray();

  class  PrimaryNoNewArray_lf_arrayAccessContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArray_lf_arrayAccessContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PrimaryNoNewArray_lf_arrayAccessContext* primaryNoNewArray_lf_arrayAccess();

  class  PrimaryNoNewArray_lfno_arrayAccessContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccessContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PrimaryNoNewArray_lfno_arrayAccessContext() = default;
    void copyFrom(PrimaryNoNewArray_lfno_arrayAccessContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PrimaryNoNewArray_lfno_arrayAccess6Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess6Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess10Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess10Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    MethodReferenceContext *methodReference();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess7Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess7Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    ClassInstanceCreationExpressionContext *classInstanceCreationExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess4Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess4Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    antlr4::tree::TerminalNode *THIS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess5Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess5Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *THIS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess8Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess8Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    FieldAccessContext *fieldAccess();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess9Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess9Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    MethodInvocationContext *methodInvocation();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess2Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess2Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess3Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess3Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    antlr4::tree::TerminalNode *VOID();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_arrayAccess1Context : public PrimaryNoNewArray_lfno_arrayAccessContext {
  public:
    PrimaryNoNewArray_lfno_arrayAccess1Context(PrimaryNoNewArray_lfno_arrayAccessContext *ctx);

    LiteralContext *literal();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PrimaryNoNewArray_lfno_arrayAccessContext* primaryNoNewArray_lfno_arrayAccess();

  class  PrimaryNoNewArray_lf_primaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArray_lf_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PrimaryNoNewArray_lf_primaryContext() = default;
    void copyFrom(PrimaryNoNewArray_lf_primaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PrimaryNoNewArray_lf_primary2Context : public PrimaryNoNewArray_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary2Context(PrimaryNoNewArray_lf_primaryContext *ctx);

    FieldAccess_lf_primaryContext *fieldAccess_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lf_primary3Context : public PrimaryNoNewArray_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary3Context(PrimaryNoNewArray_lf_primaryContext *ctx);

    ArrayAccess_lf_primaryContext *arrayAccess_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lf_primary1Context : public PrimaryNoNewArray_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary1Context(PrimaryNoNewArray_lf_primaryContext *ctx);

    ClassInstanceCreationExpression_lf_primaryContext *classInstanceCreationExpression_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lf_primary4Context : public PrimaryNoNewArray_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary4Context(PrimaryNoNewArray_lf_primaryContext *ctx);

    MethodInvocation_lf_primaryContext *methodInvocation_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lf_primary5Context : public PrimaryNoNewArray_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary5Context(PrimaryNoNewArray_lf_primaryContext *ctx);

    MethodReference_lf_primaryContext *methodReference_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PrimaryNoNewArray_lf_primaryContext* primaryNoNewArray_lf_primary();

  class  PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext* primaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary();

  class  PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext() = default;
    void copyFrom(PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1Context : public PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1Context(PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext *ctx);

    ClassInstanceCreationExpression_lf_primaryContext *classInstanceCreationExpression_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3Context : public PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3Context(PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext *ctx);

    MethodInvocation_lf_primaryContext *methodInvocation_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2Context : public PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2Context(PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext *ctx);

    FieldAccess_lf_primaryContext *fieldAccess_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4Context : public PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext {
  public:
    PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4Context(PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext *ctx);

    MethodReference_lf_primaryContext *methodReference_lf_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext* primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary();

  class  PrimaryNoNewArray_lfno_primaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArray_lfno_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PrimaryNoNewArray_lfno_primaryContext() = default;
    void copyFrom(PrimaryNoNewArray_lfno_primaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PrimaryNoNewArray_lfno_primary9Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary9Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    FieldAccess_lfno_primaryContext *fieldAccess_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary5Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary5Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *THIS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary6Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary6Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *THIS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary7Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary7Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary8Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary8Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    ClassInstanceCreationExpression_lfno_primaryContext *classInstanceCreationExpression_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary1Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary1Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    LiteralContext *literal();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary2Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary2Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary12Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary12Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    MethodReference_lfno_primaryContext *methodReference_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary3Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary3Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    UnannPrimitiveTypeContext *unannPrimitiveType();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary11Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary11Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    MethodInvocation_lfno_primaryContext *methodInvocation_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary4Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary4Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *VOID();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary10Context : public PrimaryNoNewArray_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary10Context(PrimaryNoNewArray_lfno_primaryContext *ctx);

    ArrayAccess_lfno_primaryContext *arrayAccess_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PrimaryNoNewArray_lfno_primaryContext* primaryNoNewArray_lfno_primary();

  class  PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext* primaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary();

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext() = default;
    void copyFrom(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    UnannPrimitiveTypeContext *unannPrimitiveType();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    MethodReference_lfno_primaryContext *methodReference_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *THIS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *VOID();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    MethodInvocation_lfno_primaryContext *methodInvocation_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    LiteralContext *literal();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *THIS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    FieldAccess_lfno_primaryContext *fieldAccess_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8Context : public PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext {
  public:
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8Context(PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *ctx);

    ClassInstanceCreationExpression_lfno_primaryContext *classInstanceCreationExpression_lfno_primary();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext* primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary();

  class  ClassLiteralContext : public antlr4::ParserRuleContext {
  public:
    ClassLiteralContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ClassLiteralContext() = default;
    void copyFrom(ClassLiteralContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ClassLiteral2Context : public ClassLiteralContext {
  public:
    ClassLiteral2Context(ClassLiteralContext *ctx);

    antlr4::tree::TerminalNode *VOID();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassLiteral1Context : public ClassLiteralContext {
  public:
    ClassLiteral1Context(ClassLiteralContext *ctx);

    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();
    TypeNameContext *typeName();
    NumericTypeContext *numericType();
    antlr4::tree::TerminalNode *BOOLEAN();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ClassLiteralContext* classLiteral();

  class  ClassInstanceCreationExpressionContext : public antlr4::ParserRuleContext {
  public:
    ClassInstanceCreationExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ClassInstanceCreationExpressionContext() = default;
    void copyFrom(ClassInstanceCreationExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ClassInstanceCreationExpression1Context : public ClassInstanceCreationExpressionContext {
  public:
    ClassInstanceCreationExpression1Context(ClassInstanceCreationExpressionContext *ctx);

    antlr4::tree::TerminalNode *NEW();
    std::vector<IdentifierContext *> identifier();
    IdentifierContext* identifier(size_t i);
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);
    TypeArgumentsOrDiamondContext *typeArgumentsOrDiamond();
    ArgumentListContext *argumentList();
    ClassBodyContext *classBody();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassInstanceCreationExpression3Context : public ClassInstanceCreationExpressionContext {
  public:
    ClassInstanceCreationExpression3Context(ClassInstanceCreationExpressionContext *ctx);

    PrimaryContext *primary();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *NEW();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsOrDiamondContext *typeArgumentsOrDiamond();
    ArgumentListContext *argumentList();
    ClassBodyContext *classBody();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassInstanceCreationExpression2Context : public ClassInstanceCreationExpressionContext {
  public:
    ClassInstanceCreationExpression2Context(ClassInstanceCreationExpressionContext *ctx);

    ExpressionNameContext *expressionName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *NEW();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsOrDiamondContext *typeArgumentsOrDiamond();
    ArgumentListContext *argumentList();
    ClassBodyContext *classBody();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ClassInstanceCreationExpressionContext* classInstanceCreationExpression();

  class  ClassInstanceCreationExpression_lf_primaryContext : public antlr4::ParserRuleContext {
  public:
    ClassInstanceCreationExpression_lf_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *NEW();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsOrDiamondContext *typeArgumentsOrDiamond();
    ArgumentListContext *argumentList();
    ClassBodyContext *classBody();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassInstanceCreationExpression_lf_primaryContext* classInstanceCreationExpression_lf_primary();

  class  ClassInstanceCreationExpression_lfno_primaryContext : public antlr4::ParserRuleContext {
  public:
    ClassInstanceCreationExpression_lfno_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ClassInstanceCreationExpression_lfno_primaryContext() = default;
    void copyFrom(ClassInstanceCreationExpression_lfno_primaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ClassInstanceCreationExpression_lfno_primary1Context : public ClassInstanceCreationExpression_lfno_primaryContext {
  public:
    ClassInstanceCreationExpression_lfno_primary1Context(ClassInstanceCreationExpression_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *NEW();
    std::vector<IdentifierContext *> identifier();
    IdentifierContext* identifier(size_t i);
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);
    TypeArgumentsOrDiamondContext *typeArgumentsOrDiamond();
    ArgumentListContext *argumentList();
    ClassBodyContext *classBody();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassInstanceCreationExpression_lfno_primary2Context : public ClassInstanceCreationExpression_lfno_primaryContext {
  public:
    ClassInstanceCreationExpression_lfno_primary2Context(ClassInstanceCreationExpression_lfno_primaryContext *ctx);

    ExpressionNameContext *expressionName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *NEW();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsOrDiamondContext *typeArgumentsOrDiamond();
    ArgumentListContext *argumentList();
    ClassBodyContext *classBody();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ClassInstanceCreationExpression_lfno_primaryContext* classInstanceCreationExpression_lfno_primary();

  class  TypeArgumentsOrDiamondContext : public antlr4::ParserRuleContext {
  public:
    TypeArgumentsOrDiamondContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    TypeArgumentsOrDiamondContext() = default;
    void copyFrom(TypeArgumentsOrDiamondContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  TypeArgumentsOrDiamond1Context : public TypeArgumentsOrDiamondContext {
  public:
    TypeArgumentsOrDiamond1Context(TypeArgumentsOrDiamondContext *ctx);

    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  TypeArgumentsOrDiamond2Context : public TypeArgumentsOrDiamondContext {
  public:
    TypeArgumentsOrDiamond2Context(TypeArgumentsOrDiamondContext *ctx);

    antlr4::tree::TerminalNode *LT();
    antlr4::tree::TerminalNode *GT();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  TypeArgumentsOrDiamondContext* typeArgumentsOrDiamond();

  class  FieldAccessContext : public antlr4::ParserRuleContext {
  public:
    FieldAccessContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    FieldAccessContext() = default;
    void copyFrom(FieldAccessContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  FieldAccess1Context : public FieldAccessContext {
  public:
    FieldAccess1Context(FieldAccessContext *ctx);

    PrimaryContext *primary();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  FieldAccess2Context : public FieldAccessContext {
  public:
    FieldAccess2Context(FieldAccessContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  FieldAccess3Context : public FieldAccessContext {
  public:
    FieldAccess3Context(FieldAccessContext *ctx);

    TypeNameContext *typeName();
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);
    antlr4::tree::TerminalNode *SUPER();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  FieldAccessContext* fieldAccess();

  class  FieldAccess_lf_primaryContext : public antlr4::ParserRuleContext {
  public:
    FieldAccess_lf_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FieldAccess_lf_primaryContext* fieldAccess_lf_primary();

  class  FieldAccess_lfno_primaryContext : public antlr4::ParserRuleContext {
  public:
    FieldAccess_lfno_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    FieldAccess_lfno_primaryContext() = default;
    void copyFrom(FieldAccess_lfno_primaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  FieldAccess_lfno_primary2Context : public FieldAccess_lfno_primaryContext {
  public:
    FieldAccess_lfno_primary2Context(FieldAccess_lfno_primaryContext *ctx);

    TypeNameContext *typeName();
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);
    antlr4::tree::TerminalNode *SUPER();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  FieldAccess_lfno_primary1Context : public FieldAccess_lfno_primaryContext {
  public:
    FieldAccess_lfno_primary1Context(FieldAccess_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  FieldAccess_lfno_primaryContext* fieldAccess_lfno_primary();

  class  ArrayAccessContext : public antlr4::ParserRuleContext {
  public:
    ArrayAccessContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExpressionNameContext *expressionName();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    PrimaryNoNewArray_lfno_arrayAccessContext *primaryNoNewArray_lfno_arrayAccess();
    std::vector<PrimaryNoNewArray_lf_arrayAccessContext *> primaryNoNewArray_lf_arrayAccess();
    PrimaryNoNewArray_lf_arrayAccessContext* primaryNoNewArray_lf_arrayAccess(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArrayAccessContext* arrayAccess();

  class  ArrayAccess_lf_primaryContext : public antlr4::ParserRuleContext {
  public:
    ArrayAccess_lf_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    PrimaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primaryContext *primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    std::vector<PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext *> primaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary();
    PrimaryNoNewArray_lf_primary_lf_arrayAccess_lf_primaryContext* primaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArrayAccess_lf_primaryContext* arrayAccess_lf_primary();

  class  ArrayAccess_lfno_primaryContext : public antlr4::ParserRuleContext {
  public:
    ArrayAccess_lfno_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExpressionNameContext *expressionName();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    PrimaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primaryContext *primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary();
    std::vector<PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext *> primaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary();
    PrimaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primaryContext* primaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArrayAccess_lfno_primaryContext* arrayAccess_lfno_primary();

  class  MethodInvocationContext : public antlr4::ParserRuleContext {
  public:
    MethodInvocationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    MethodInvocationContext() = default;
    void copyFrom(MethodInvocationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  MethodInvocation1Context : public MethodInvocationContext {
  public:
    MethodInvocation1Context(MethodInvocationContext *ctx);

    MethodNameContext *methodName();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation2Context : public MethodInvocationContext {
  public:
    MethodInvocation2Context(MethodInvocationContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation3Context : public MethodInvocationContext {
  public:
    MethodInvocation3Context(MethodInvocationContext *ctx);

    ExpressionNameContext *expressionName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation4Context : public MethodInvocationContext {
  public:
    MethodInvocation4Context(MethodInvocationContext *ctx);

    PrimaryContext *primary();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation5Context : public MethodInvocationContext {
  public:
    MethodInvocation5Context(MethodInvocationContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation6Context : public MethodInvocationContext {
  public:
    MethodInvocation6Context(MethodInvocationContext *ctx);

    TypeNameContext *typeName();
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);
    antlr4::tree::TerminalNode *SUPER();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  MethodInvocationContext* methodInvocation();

  class  MethodInvocation_lf_primaryContext : public antlr4::ParserRuleContext {
  public:
    MethodInvocation_lf_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodInvocation_lf_primaryContext* methodInvocation_lf_primary();

  class  MethodInvocation_lfno_primaryContext : public antlr4::ParserRuleContext {
  public:
    MethodInvocation_lfno_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    MethodInvocation_lfno_primaryContext() = default;
    void copyFrom(MethodInvocation_lfno_primaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  MethodInvocation_lfno_primary3Context : public MethodInvocation_lfno_primaryContext {
  public:
    MethodInvocation_lfno_primary3Context(MethodInvocation_lfno_primaryContext *ctx);

    ExpressionNameContext *expressionName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation_lfno_primary2Context : public MethodInvocation_lfno_primaryContext {
  public:
    MethodInvocation_lfno_primary2Context(MethodInvocation_lfno_primaryContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation_lfno_primary1Context : public MethodInvocation_lfno_primaryContext {
  public:
    MethodInvocation_lfno_primary1Context(MethodInvocation_lfno_primaryContext *ctx);

    MethodNameContext *methodName();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation_lfno_primary5Context : public MethodInvocation_lfno_primaryContext {
  public:
    MethodInvocation_lfno_primary5Context(MethodInvocation_lfno_primaryContext *ctx);

    TypeNameContext *typeName();
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);
    antlr4::tree::TerminalNode *SUPER();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodInvocation_lfno_primary4Context : public MethodInvocation_lfno_primaryContext {
  public:
    MethodInvocation_lfno_primary4Context(MethodInvocation_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    TypeArgumentsContext *typeArguments();
    ArgumentListContext *argumentList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  MethodInvocation_lfno_primaryContext* methodInvocation_lfno_primary();

  class  ArgumentListContext : public antlr4::ParserRuleContext {
  public:
    ArgumentListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArgumentListContext* argumentList();

  class  MethodReferenceContext : public antlr4::ParserRuleContext {
  public:
    MethodReferenceContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    MethodReferenceContext() = default;
    void copyFrom(MethodReferenceContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  MethodReference1Context : public MethodReferenceContext {
  public:
    MethodReference1Context(MethodReferenceContext *ctx);

    ExpressionNameContext *expressionName();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference3Context : public MethodReferenceContext {
  public:
    MethodReference3Context(MethodReferenceContext *ctx);

    PrimaryContext *primary();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference2Context : public MethodReferenceContext {
  public:
    MethodReference2Context(MethodReferenceContext *ctx);

    ReferenceTypeContext *referenceType();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference5Context : public MethodReferenceContext {
  public:
    MethodReference5Context(MethodReferenceContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference4Context : public MethodReferenceContext {
  public:
    MethodReference4Context(MethodReferenceContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference7Context : public MethodReferenceContext {
  public:
    MethodReference7Context(MethodReferenceContext *ctx);

    ArrayTypeContext *arrayType();
    antlr4::tree::TerminalNode *COLONCOLON();
    antlr4::tree::TerminalNode *NEW();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference6Context : public MethodReferenceContext {
  public:
    MethodReference6Context(MethodReferenceContext *ctx);

    ClassTypeContext *classType();
    antlr4::tree::TerminalNode *COLONCOLON();
    antlr4::tree::TerminalNode *NEW();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  MethodReferenceContext* methodReference();

  class  MethodReference_lf_primaryContext : public antlr4::ParserRuleContext {
  public:
    MethodReference_lf_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodReference_lf_primaryContext* methodReference_lf_primary();

  class  MethodReference_lfno_primaryContext : public antlr4::ParserRuleContext {
  public:
    MethodReference_lfno_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    MethodReference_lfno_primaryContext() = default;
    void copyFrom(MethodReference_lfno_primaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  MethodReference_lfno_primary6Context : public MethodReference_lfno_primaryContext {
  public:
    MethodReference_lfno_primary6Context(MethodReference_lfno_primaryContext *ctx);

    ArrayTypeContext *arrayType();
    antlr4::tree::TerminalNode *COLONCOLON();
    antlr4::tree::TerminalNode *NEW();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference_lfno_primary5Context : public MethodReference_lfno_primaryContext {
  public:
    MethodReference_lfno_primary5Context(MethodReference_lfno_primaryContext *ctx);

    ClassTypeContext *classType();
    antlr4::tree::TerminalNode *COLONCOLON();
    antlr4::tree::TerminalNode *NEW();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference_lfno_primary4Context : public MethodReference_lfno_primaryContext {
  public:
    MethodReference_lfno_primary4Context(MethodReference_lfno_primaryContext *ctx);

    TypeNameContext *typeName();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference_lfno_primary3Context : public MethodReference_lfno_primaryContext {
  public:
    MethodReference_lfno_primary3Context(MethodReference_lfno_primaryContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference_lfno_primary2Context : public MethodReference_lfno_primaryContext {
  public:
    MethodReference_lfno_primary2Context(MethodReference_lfno_primaryContext *ctx);

    ReferenceTypeContext *referenceType();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodReference_lfno_primary1Context : public MethodReference_lfno_primaryContext {
  public:
    MethodReference_lfno_primary1Context(MethodReference_lfno_primaryContext *ctx);

    ExpressionNameContext *expressionName();
    antlr4::tree::TerminalNode *COLONCOLON();
    IdentifierContext *identifier();
    TypeArgumentsContext *typeArguments();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  MethodReference_lfno_primaryContext* methodReference_lfno_primary();

  class  ArrayCreationExpressionContext : public antlr4::ParserRuleContext {
  public:
    ArrayCreationExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ArrayCreationExpressionContext() = default;
    void copyFrom(ArrayCreationExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ArrayCreationExpression4Context : public ArrayCreationExpressionContext {
  public:
    ArrayCreationExpression4Context(ArrayCreationExpressionContext *ctx);

    antlr4::tree::TerminalNode *NEW();
    ClassOrInterfaceTypeContext *classOrInterfaceType();
    DimsContext *dims();
    ArrayInitializerContext *arrayInitializer();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ArrayCreationExpression2Context : public ArrayCreationExpressionContext {
  public:
    ArrayCreationExpression2Context(ArrayCreationExpressionContext *ctx);

    antlr4::tree::TerminalNode *NEW();
    ClassOrInterfaceTypeContext *classOrInterfaceType();
    DimExprsContext *dimExprs();
    DimsContext *dims();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ArrayCreationExpression3Context : public ArrayCreationExpressionContext {
  public:
    ArrayCreationExpression3Context(ArrayCreationExpressionContext *ctx);

    antlr4::tree::TerminalNode *NEW();
    PrimitiveTypeContext *primitiveType();
    DimsContext *dims();
    ArrayInitializerContext *arrayInitializer();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ArrayCreationExpression1Context : public ArrayCreationExpressionContext {
  public:
    ArrayCreationExpression1Context(ArrayCreationExpressionContext *ctx);

    antlr4::tree::TerminalNode *NEW();
    PrimitiveTypeContext *primitiveType();
    DimExprsContext *dimExprs();
    DimsContext *dims();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ArrayCreationExpressionContext* arrayCreationExpression();

  class  DimExprsContext : public antlr4::ParserRuleContext {
  public:
    DimExprsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<DimExprContext *> dimExpr();
    DimExprContext* dimExpr(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DimExprsContext* dimExprs();

  class  DimExprContext : public antlr4::ParserRuleContext {
  public:
    DimExprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACK();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RBRACK();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DimExprContext* dimExpr();

  class  ConstantExpressionContext : public antlr4::ParserRuleContext {
  public:
    ConstantExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExpressionContext *expression();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstantExpressionContext* constantExpression();

  class  ExpressionContext : public antlr4::ParserRuleContext {
  public:
    ExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ExpressionContext() = default;
    void copyFrom(ExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Expression2Context : public ExpressionContext {
  public:
    Expression2Context(ExpressionContext *ctx);

    AssignmentExpressionContext *assignmentExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression1Context : public ExpressionContext {
  public:
    Expression1Context(ExpressionContext *ctx);

    LambdaExpressionContext *lambdaExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ExpressionContext* expression();

  class  LambdaExpressionContext : public antlr4::ParserRuleContext {
  public:
    LambdaExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    LambdaParametersContext *lambdaParameters();
    antlr4::tree::TerminalNode *ARROW();
    LambdaBodyContext *lambdaBody();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LambdaExpressionContext* lambdaExpression();

  class  LambdaParametersContext : public antlr4::ParserRuleContext {
  public:
    LambdaParametersContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    LambdaParametersContext() = default;
    void copyFrom(LambdaParametersContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  LambdaParameters3Context : public LambdaParametersContext {
  public:
    LambdaParameters3Context(LambdaParametersContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    InferredFormalParameterListContext *inferredFormalParameterList();
    antlr4::tree::TerminalNode *RPAREN();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LambdaParameters1Context : public LambdaParametersContext {
  public:
    LambdaParameters1Context(LambdaParametersContext *ctx);

    IdentifierContext *identifier();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LambdaParameters2Context : public LambdaParametersContext {
  public:
    LambdaParameters2Context(LambdaParametersContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    FormalParameterListContext *formalParameterList();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  LambdaParametersContext* lambdaParameters();

  class  InferredFormalParameterListContext : public antlr4::ParserRuleContext {
  public:
    InferredFormalParameterListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<IdentifierContext *> identifier();
    IdentifierContext* identifier(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InferredFormalParameterListContext* inferredFormalParameterList();

  class  LambdaBodyContext : public antlr4::ParserRuleContext {
  public:
    LambdaBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    LambdaBodyContext() = default;
    void copyFrom(LambdaBodyContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  LambdaBody1Context : public LambdaBodyContext {
  public:
    LambdaBody1Context(LambdaBodyContext *ctx);

    ExpressionContext *expression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LambdaBody2Context : public LambdaBodyContext {
  public:
    LambdaBody2Context(LambdaBodyContext *ctx);

    BlockContext *block();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  LambdaBodyContext* lambdaBody();

  class  AssignmentExpressionContext : public antlr4::ParserRuleContext {
  public:
    AssignmentExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AssignmentExpressionContext() = default;
    void copyFrom(AssignmentExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  AssignmentExpression1Context : public AssignmentExpressionContext {
  public:
    AssignmentExpression1Context(AssignmentExpressionContext *ctx);

    ConditionalExpressionContext *conditionalExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AssignmentExpression2Context : public AssignmentExpressionContext {
  public:
    AssignmentExpression2Context(AssignmentExpressionContext *ctx);

    AssignmentContext *assignment();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AssignmentExpressionContext* assignmentExpression();

  class  AssignmentContext : public antlr4::ParserRuleContext {
  public:
    AssignmentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    LeftHandSideContext *leftHandSide();
    AssignmentOperatorContext *assignmentOperator();
    ExpressionContext *expression();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AssignmentContext* assignment();

  class  LeftHandSideContext : public antlr4::ParserRuleContext {
  public:
    LeftHandSideContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    LeftHandSideContext() = default;
    void copyFrom(LeftHandSideContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  LeftHandSide5Context : public LeftHandSideContext {
  public:
    LeftHandSide5Context(LeftHandSideContext *ctx);

    ArrayAccessContext *arrayAccess();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LeftHandSide4Context : public LeftHandSideContext {
  public:
    LeftHandSide4Context(LeftHandSideContext *ctx);

    FieldAccessContext *fieldAccess();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LeftHandSide3Context : public LeftHandSideContext {
  public:
    LeftHandSide3Context(LeftHandSideContext *ctx);

    ExpressionNameContext *expressionName();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  LeftHandSideContext* leftHandSide();

  class  AssignmentOperatorContext : public antlr4::ParserRuleContext {
  public:
    AssignmentOperatorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ASSIGN();
    antlr4::tree::TerminalNode *MUL_ASSIGN();
    antlr4::tree::TerminalNode *DIV_ASSIGN();
    antlr4::tree::TerminalNode *MOD_ASSIGN();
    antlr4::tree::TerminalNode *ADD_ASSIGN();
    antlr4::tree::TerminalNode *SUB_ASSIGN();
    antlr4::tree::TerminalNode *LSHIFT_ASSIGN();
    antlr4::tree::TerminalNode *RSHIFT_ASSIGN();
    antlr4::tree::TerminalNode *URSHIFT_ASSIGN();
    antlr4::tree::TerminalNode *AND_ASSIGN();
    antlr4::tree::TerminalNode *XOR_ASSIGN();
    antlr4::tree::TerminalNode *OR_ASSIGN();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AssignmentOperatorContext* assignmentOperator();

  class  ConditionalExpressionContext : public antlr4::ParserRuleContext {
  public:
    ConditionalExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ConditionalExpressionContext() = default;
    void copyFrom(ConditionalExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ConditionalExpression1Context : public ConditionalExpressionContext {
  public:
    ConditionalExpression1Context(ConditionalExpressionContext *ctx);

    ConditionalOrExpressionContext *conditionalOrExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ConditionalExpression2Context : public ConditionalExpressionContext {
  public:
    ConditionalExpression2Context(ConditionalExpressionContext *ctx);

    ConditionalOrExpressionContext *conditionalOrExpression();
    antlr4::tree::TerminalNode *QUESTION();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *COLON();
    ConditionalExpressionContext *conditionalExpression();
    LambdaExpressionContext *lambdaExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ConditionalExpressionContext* conditionalExpression();

  class  ConditionalOrExpressionContext : public antlr4::ParserRuleContext {
  public:
    ConditionalOrExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ConditionalOrExpressionContext() = default;
    void copyFrom(ConditionalOrExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ConditionalOrExpression1Context : public ConditionalOrExpressionContext {
  public:
    ConditionalOrExpression1Context(ConditionalOrExpressionContext *ctx);

    ConditionalAndExpressionContext *conditionalAndExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ConditionalOrExpression2Context : public ConditionalOrExpressionContext {
  public:
    ConditionalOrExpression2Context(ConditionalOrExpressionContext *ctx);

    ConditionalOrExpressionContext *conditionalOrExpression();
    antlr4::tree::TerminalNode *OR();
    ConditionalAndExpressionContext *conditionalAndExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ConditionalOrExpressionContext* conditionalOrExpression();
  ConditionalOrExpressionContext* conditionalOrExpression(int precedence);
  class  ConditionalAndExpressionContext : public antlr4::ParserRuleContext {
  public:
    ConditionalAndExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ConditionalAndExpressionContext() = default;
    void copyFrom(ConditionalAndExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ConditionalAndExpression2Context : public ConditionalAndExpressionContext {
  public:
    ConditionalAndExpression2Context(ConditionalAndExpressionContext *ctx);

    ConditionalAndExpressionContext *conditionalAndExpression();
    antlr4::tree::TerminalNode *AND();
    InclusiveOrExpressionContext *inclusiveOrExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ConditionalAndExpression1Context : public ConditionalAndExpressionContext {
  public:
    ConditionalAndExpression1Context(ConditionalAndExpressionContext *ctx);

    InclusiveOrExpressionContext *inclusiveOrExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ConditionalAndExpressionContext* conditionalAndExpression();
  ConditionalAndExpressionContext* conditionalAndExpression(int precedence);
  class  InclusiveOrExpressionContext : public antlr4::ParserRuleContext {
  public:
    InclusiveOrExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    InclusiveOrExpressionContext() = default;
    void copyFrom(InclusiveOrExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  InclusiveOrExpression2Context : public InclusiveOrExpressionContext {
  public:
    InclusiveOrExpression2Context(InclusiveOrExpressionContext *ctx);

    InclusiveOrExpressionContext *inclusiveOrExpression();
    antlr4::tree::TerminalNode *BITOR();
    ExclusiveOrExpressionContext *exclusiveOrExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InclusiveOrExpression1Context : public InclusiveOrExpressionContext {
  public:
    InclusiveOrExpression1Context(InclusiveOrExpressionContext *ctx);

    ExclusiveOrExpressionContext *exclusiveOrExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  InclusiveOrExpressionContext* inclusiveOrExpression();
  InclusiveOrExpressionContext* inclusiveOrExpression(int precedence);
  class  ExclusiveOrExpressionContext : public antlr4::ParserRuleContext {
  public:
    ExclusiveOrExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ExclusiveOrExpressionContext() = default;
    void copyFrom(ExclusiveOrExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ExclusiveOrExpression1Context : public ExclusiveOrExpressionContext {
  public:
    ExclusiveOrExpression1Context(ExclusiveOrExpressionContext *ctx);

    AndExpressionContext *andExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ExclusiveOrExpression2Context : public ExclusiveOrExpressionContext {
  public:
    ExclusiveOrExpression2Context(ExclusiveOrExpressionContext *ctx);

    ExclusiveOrExpressionContext *exclusiveOrExpression();
    antlr4::tree::TerminalNode *CARET();
    AndExpressionContext *andExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ExclusiveOrExpressionContext* exclusiveOrExpression();
  ExclusiveOrExpressionContext* exclusiveOrExpression(int precedence);
  class  AndExpressionContext : public antlr4::ParserRuleContext {
  public:
    AndExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AndExpressionContext() = default;
    void copyFrom(AndExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  AndExpression2Context : public AndExpressionContext {
  public:
    AndExpression2Context(AndExpressionContext *ctx);

    AndExpressionContext *andExpression();
    antlr4::tree::TerminalNode *BITAND();
    EqualityExpressionContext *equalityExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AndExpression1Context : public AndExpressionContext {
  public:
    AndExpression1Context(AndExpressionContext *ctx);

    EqualityExpressionContext *equalityExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AndExpressionContext* andExpression();
  AndExpressionContext* andExpression(int precedence);
  class  EqualityExpressionContext : public antlr4::ParserRuleContext {
  public:
    EqualityExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    EqualityExpressionContext() = default;
    void copyFrom(EqualityExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  EqualityExpression3Context : public EqualityExpressionContext {
  public:
    EqualityExpression3Context(EqualityExpressionContext *ctx);

    EqualityExpressionContext *equalityExpression();
    antlr4::tree::TerminalNode *NOTEQUAL();
    RelationalExpressionContext *relationalExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  EqualityExpression2Context : public EqualityExpressionContext {
  public:
    EqualityExpression2Context(EqualityExpressionContext *ctx);

    EqualityExpressionContext *equalityExpression();
    antlr4::tree::TerminalNode *EQUAL();
    RelationalExpressionContext *relationalExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  EqualityExpression1Context : public EqualityExpressionContext {
  public:
    EqualityExpression1Context(EqualityExpressionContext *ctx);

    RelationalExpressionContext *relationalExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  EqualityExpressionContext* equalityExpression();
  EqualityExpressionContext* equalityExpression(int precedence);
  class  RelationalExpressionContext : public antlr4::ParserRuleContext {
  public:
    RelationalExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    RelationalExpressionContext() = default;
    void copyFrom(RelationalExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  RelationalExpression1Context : public RelationalExpressionContext {
  public:
    RelationalExpression1Context(RelationalExpressionContext *ctx);

    ShiftExpressionContext *shiftExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  RelationalExpression2Context : public RelationalExpressionContext {
  public:
    RelationalExpression2Context(RelationalExpressionContext *ctx);

    RelationalExpressionContext *relationalExpression();
    antlr4::tree::TerminalNode *LT();
    ShiftExpressionContext *shiftExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  RelationalExpression5Context : public RelationalExpressionContext {
  public:
    RelationalExpression5Context(RelationalExpressionContext *ctx);

    RelationalExpressionContext *relationalExpression();
    antlr4::tree::TerminalNode *GE();
    ShiftExpressionContext *shiftExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  RelationalExpression6Context : public RelationalExpressionContext {
  public:
    RelationalExpression6Context(RelationalExpressionContext *ctx);

    RelationalExpressionContext *relationalExpression();
    antlr4::tree::TerminalNode *INSTANCEOF();
    ReferenceTypeContext *referenceType();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  RelationalExpression3Context : public RelationalExpressionContext {
  public:
    RelationalExpression3Context(RelationalExpressionContext *ctx);

    RelationalExpressionContext *relationalExpression();
    antlr4::tree::TerminalNode *GT();
    ShiftExpressionContext *shiftExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  RelationalExpression4Context : public RelationalExpressionContext {
  public:
    RelationalExpression4Context(RelationalExpressionContext *ctx);

    RelationalExpressionContext *relationalExpression();
    antlr4::tree::TerminalNode *LE();
    ShiftExpressionContext *shiftExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  RelationalExpressionContext* relationalExpression();
  RelationalExpressionContext* relationalExpression(int precedence);
  class  ShiftExpressionContext : public antlr4::ParserRuleContext {
  public:
    ShiftExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ShiftExpressionContext() = default;
    void copyFrom(ShiftExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ShiftExpression1Context : public ShiftExpressionContext {
  public:
    ShiftExpression1Context(ShiftExpressionContext *ctx);

    AdditiveExpressionContext *additiveExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ShiftExpression3Context : public ShiftExpressionContext {
  public:
    ShiftExpression3Context(ShiftExpressionContext *ctx);

    ShiftExpressionContext *shiftExpression();
    std::vector<antlr4::tree::TerminalNode *> GT();
    antlr4::tree::TerminalNode* GT(size_t i);
    AdditiveExpressionContext *additiveExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ShiftExpression2Context : public ShiftExpressionContext {
  public:
    ShiftExpression2Context(ShiftExpressionContext *ctx);

    ShiftExpressionContext *shiftExpression();
    std::vector<antlr4::tree::TerminalNode *> LT();
    antlr4::tree::TerminalNode* LT(size_t i);
    AdditiveExpressionContext *additiveExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ShiftExpression4Context : public ShiftExpressionContext {
  public:
    ShiftExpression4Context(ShiftExpressionContext *ctx);

    ShiftExpressionContext *shiftExpression();
    std::vector<antlr4::tree::TerminalNode *> GT();
    antlr4::tree::TerminalNode* GT(size_t i);
    AdditiveExpressionContext *additiveExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ShiftExpressionContext* shiftExpression();
  ShiftExpressionContext* shiftExpression(int precedence);
  class  AdditiveExpressionContext : public antlr4::ParserRuleContext {
  public:
    AdditiveExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AdditiveExpressionContext() = default;
    void copyFrom(AdditiveExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  AdditiveExpression1Context : public AdditiveExpressionContext {
  public:
    AdditiveExpression1Context(AdditiveExpressionContext *ctx);

    MultiplicativeExpressionContext *multiplicativeExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AdditiveExpression3Context : public AdditiveExpressionContext {
  public:
    AdditiveExpression3Context(AdditiveExpressionContext *ctx);

    AdditiveExpressionContext *additiveExpression();
    antlr4::tree::TerminalNode *SUB();
    MultiplicativeExpressionContext *multiplicativeExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AdditiveExpressio2Context : public AdditiveExpressionContext {
  public:
    AdditiveExpressio2Context(AdditiveExpressionContext *ctx);

    AdditiveExpressionContext *additiveExpression();
    antlr4::tree::TerminalNode *ADD();
    MultiplicativeExpressionContext *multiplicativeExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AdditiveExpressionContext* additiveExpression();
  AdditiveExpressionContext* additiveExpression(int precedence);
  class  MultiplicativeExpressionContext : public antlr4::ParserRuleContext {
  public:
    MultiplicativeExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    MultiplicativeExpressionContext() = default;
    void copyFrom(MultiplicativeExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  MultiplicativeExpression1Context : public MultiplicativeExpressionContext {
  public:
    MultiplicativeExpression1Context(MultiplicativeExpressionContext *ctx);

    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MultiplicativeExpression4Context : public MultiplicativeExpressionContext {
  public:
    MultiplicativeExpression4Context(MultiplicativeExpressionContext *ctx);

    MultiplicativeExpressionContext *multiplicativeExpression();
    antlr4::tree::TerminalNode *MOD();
    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MultiplicativeExpression3Context : public MultiplicativeExpressionContext {
  public:
    MultiplicativeExpression3Context(MultiplicativeExpressionContext *ctx);

    MultiplicativeExpressionContext *multiplicativeExpression();
    antlr4::tree::TerminalNode *DIV();
    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MultiplicativeExpression2Context : public MultiplicativeExpressionContext {
  public:
    MultiplicativeExpression2Context(MultiplicativeExpressionContext *ctx);

    MultiplicativeExpressionContext *multiplicativeExpression();
    antlr4::tree::TerminalNode *MUL();
    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  MultiplicativeExpressionContext* multiplicativeExpression();
  MultiplicativeExpressionContext* multiplicativeExpression(int precedence);
  class  UnaryExpressionContext : public antlr4::ParserRuleContext {
  public:
    UnaryExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    UnaryExpressionContext() = default;
    void copyFrom(UnaryExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnaryExpression2Context : public UnaryExpressionContext {
  public:
    UnaryExpression2Context(UnaryExpressionContext *ctx);

    PreDecrementExpressionContext *preDecrementExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnaryExpression1Context : public UnaryExpressionContext {
  public:
    UnaryExpression1Context(UnaryExpressionContext *ctx);

    PreIncrementExpressionContext *preIncrementExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnaryExpression5Context : public UnaryExpressionContext {
  public:
    UnaryExpression5Context(UnaryExpressionContext *ctx);

    UnaryExpressionNotPlusMinusContext *unaryExpressionNotPlusMinus();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnaryExpression4Context : public UnaryExpressionContext {
  public:
    UnaryExpression4Context(UnaryExpressionContext *ctx);

    antlr4::tree::TerminalNode *SUB();
    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnaryExpression3Context : public UnaryExpressionContext {
  public:
    UnaryExpression3Context(UnaryExpressionContext *ctx);

    antlr4::tree::TerminalNode *ADD();
    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  UnaryExpressionContext* unaryExpression();

  class  PreIncrementExpressionContext : public antlr4::ParserRuleContext {
  public:
    PreIncrementExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *INC();
    UnaryExpressionContext *unaryExpression();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PreIncrementExpressionContext* preIncrementExpression();

  class  PreDecrementExpressionContext : public antlr4::ParserRuleContext {
  public:
    PreDecrementExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DEC();
    UnaryExpressionContext *unaryExpression();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PreDecrementExpressionContext* preDecrementExpression();

  class  UnaryExpressionNotPlusMinusContext : public antlr4::ParserRuleContext {
  public:
    UnaryExpressionNotPlusMinusContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    UnaryExpressionNotPlusMinusContext() = default;
    void copyFrom(UnaryExpressionNotPlusMinusContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnaryExpressionNotPlusMinus4Context : public UnaryExpressionNotPlusMinusContext {
  public:
    UnaryExpressionNotPlusMinus4Context(UnaryExpressionNotPlusMinusContext *ctx);

    CastExpressionContext *castExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnaryExpressionNotPlusMinus3Context : public UnaryExpressionNotPlusMinusContext {
  public:
    UnaryExpressionNotPlusMinus3Context(UnaryExpressionNotPlusMinusContext *ctx);

    antlr4::tree::TerminalNode *BANG();
    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnaryExpressionNotPlusMinus2Context : public UnaryExpressionNotPlusMinusContext {
  public:
    UnaryExpressionNotPlusMinus2Context(UnaryExpressionNotPlusMinusContext *ctx);

    antlr4::tree::TerminalNode *TILDE();
    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnaryExpressionNotPlusMinus1Context : public UnaryExpressionNotPlusMinusContext {
  public:
    UnaryExpressionNotPlusMinus1Context(UnaryExpressionNotPlusMinusContext *ctx);

    PostfixExpressionContext *postfixExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  UnaryExpressionNotPlusMinusContext* unaryExpressionNotPlusMinus();

  class  PostfixExpressionContext : public antlr4::ParserRuleContext {
  public:
    PostfixExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    PrimaryContext *primary();
    ExpressionNameContext *expressionName();
    std::vector<PostIncrementExpression_lf_postfixExpressionContext *> postIncrementExpression_lf_postfixExpression();
    PostIncrementExpression_lf_postfixExpressionContext* postIncrementExpression_lf_postfixExpression(size_t i);
    std::vector<PostDecrementExpression_lf_postfixExpressionContext *> postDecrementExpression_lf_postfixExpression();
    PostDecrementExpression_lf_postfixExpressionContext* postDecrementExpression_lf_postfixExpression(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PostfixExpressionContext* postfixExpression();

  class  PostIncrementExpressionContext : public antlr4::ParserRuleContext {
  public:
    PostIncrementExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    PostfixExpressionContext *postfixExpression();
    antlr4::tree::TerminalNode *INC();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PostIncrementExpressionContext* postIncrementExpression();

  class  PostIncrementExpression_lf_postfixExpressionContext : public antlr4::ParserRuleContext {
  public:
    PostIncrementExpression_lf_postfixExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *INC();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PostIncrementExpression_lf_postfixExpressionContext* postIncrementExpression_lf_postfixExpression();

  class  PostDecrementExpressionContext : public antlr4::ParserRuleContext {
  public:
    PostDecrementExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    PostfixExpressionContext *postfixExpression();
    antlr4::tree::TerminalNode *DEC();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PostDecrementExpressionContext* postDecrementExpression();

  class  PostDecrementExpression_lf_postfixExpressionContext : public antlr4::ParserRuleContext {
  public:
    PostDecrementExpression_lf_postfixExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DEC();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PostDecrementExpression_lf_postfixExpressionContext* postDecrementExpression_lf_postfixExpression();

  class  CastExpressionContext : public antlr4::ParserRuleContext {
  public:
    CastExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    CastExpressionContext() = default;
    void copyFrom(CastExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  CastExpression3Context : public CastExpressionContext {
  public:
    CastExpression3Context(CastExpressionContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    ReferenceTypeContext *referenceType();
    antlr4::tree::TerminalNode *RPAREN();
    LambdaExpressionContext *lambdaExpression();
    std::vector<AdditionalBoundContext *> additionalBound();
    AdditionalBoundContext* additionalBound(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  CastExpression1Context : public CastExpressionContext {
  public:
    CastExpression1Context(CastExpressionContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    PrimitiveTypeContext *primitiveType();
    antlr4::tree::TerminalNode *RPAREN();
    UnaryExpressionContext *unaryExpression();
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  CastExpression2Context : public CastExpressionContext {
  public:
    CastExpression2Context(CastExpressionContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    ReferenceTypeContext *referenceType();
    antlr4::tree::TerminalNode *RPAREN();
    UnaryExpressionNotPlusMinusContext *unaryExpressionNotPlusMinus();
    std::vector<AdditionalBoundContext *> additionalBound();
    AdditionalBoundContext* additionalBound(size_t i);
    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  CastExpressionContext* castExpression();

  class  IdentifierContext : public antlr4::ParserRuleContext {
  public:
    IdentifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *Identifier();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IdentifierContext* identifier();


  virtual bool sempred(antlr4::RuleContext *_localctx, size_t ruleIndex, size_t predicateIndex) override;
  bool moduleNameSempred(ModuleNameContext *_localctx, size_t predicateIndex);
  bool packageNameSempred(PackageNameContext *_localctx, size_t predicateIndex);
  bool packageOrTypeNameSempred(PackageOrTypeNameContext *_localctx, size_t predicateIndex);
  bool ambiguousNameSempred(AmbiguousNameContext *_localctx, size_t predicateIndex);
  bool conditionalOrExpressionSempred(ConditionalOrExpressionContext *_localctx, size_t predicateIndex);
  bool conditionalAndExpressionSempred(ConditionalAndExpressionContext *_localctx, size_t predicateIndex);
  bool inclusiveOrExpressionSempred(InclusiveOrExpressionContext *_localctx, size_t predicateIndex);
  bool exclusiveOrExpressionSempred(ExclusiveOrExpressionContext *_localctx, size_t predicateIndex);
  bool andExpressionSempred(AndExpressionContext *_localctx, size_t predicateIndex);
  bool equalityExpressionSempred(EqualityExpressionContext *_localctx, size_t predicateIndex);
  bool relationalExpressionSempred(RelationalExpressionContext *_localctx, size_t predicateIndex);
  bool shiftExpressionSempred(ShiftExpressionContext *_localctx, size_t predicateIndex);
  bool additiveExpressionSempred(AdditiveExpressionContext *_localctx, size_t predicateIndex);
  bool multiplicativeExpressionSempred(MultiplicativeExpressionContext *_localctx, size_t predicateIndex);

private:
  static std::vector<antlr4::dfa::DFA> _decisionToDFA;
  static antlr4::atn::PredictionContextCache _sharedContextCache;
  static std::vector<std::string> _ruleNames;
  static std::vector<std::string> _tokenNames;

  static std::vector<std::string> _literalNames;
  static std::vector<std::string> _symbolicNames;
  static antlr4::dfa::Vocabulary _vocabulary;
  static antlr4::atn::ATN _atn;
  static std::vector<uint16_t> _serializedATN;


  struct Initializer {
    Initializer();
  };
  static Initializer _init;
};

