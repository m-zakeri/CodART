
// Generated from JavaLabeledParser.g4 by ANTLR 4.9.1

#pragma once


#include "antlr4-runtime.h"




class  JavaLabeledParser : public antlr4::Parser {
public:
  enum {
    ABSTRACT = 1, ASSERT = 2, BOOLEAN = 3, BREAK = 4, BYTE = 5, CASE = 6, 
    CATCH = 7, CHAR = 8, CLASS = 9, CONST = 10, CONTINUE = 11, DEFAULT = 12, 
    DO = 13, DOUBLE = 14, ELSE = 15, ENUM = 16, EXTENDS = 17, FINAL = 18, 
    FINALLY = 19, FLOAT = 20, FOR = 21, IF = 22, GOTO = 23, IMPLEMENTS = 24, 
    IMPORT = 25, INSTANCEOF = 26, INT = 27, INTERFACE = 28, LONG = 29, NATIVE = 30, 
    NEW = 31, PACKAGE = 32, PRIVATE = 33, PROTECTED = 34, PUBLIC = 35, RETURN = 36, 
    SHORT = 37, STATIC = 38, STRICTFP = 39, SUPER = 40, SWITCH = 41, SYNCHRONIZED = 42, 
    THIS = 43, THROW = 44, THROWS = 45, TRANSIENT = 46, TRY = 47, VOID = 48, 
    VOLATILE = 49, WHILE = 50, DECIMAL_LITERAL = 51, HEX_LITERAL = 52, OCT_LITERAL = 53, 
    BINARY_LITERAL = 54, FLOAT_LITERAL = 55, HEX_FLOAT_LITERAL = 56, BOOL_LITERAL = 57, 
    CHAR_LITERAL = 58, STRING_LITERAL = 59, NULL_LITERAL = 60, LPAREN = 61, 
    RPAREN = 62, LBRACE = 63, RBRACE = 64, LBRACK = 65, RBRACK = 66, SEMI = 67, 
    COMMA = 68, DOT = 69, ASSIGN = 70, GT = 71, LT = 72, BANG = 73, TILDE = 74, 
    QUESTION = 75, COLON = 76, EQUAL = 77, LE = 78, GE = 79, NOTEQUAL = 80, 
    AND = 81, OR = 82, INC = 83, DEC = 84, ADD = 85, SUB = 86, MUL = 87, 
    DIV = 88, BITAND = 89, BITOR = 90, CARET = 91, MOD = 92, ADD_ASSIGN = 93, 
    SUB_ASSIGN = 94, MUL_ASSIGN = 95, DIV_ASSIGN = 96, AND_ASSIGN = 97, 
    OR_ASSIGN = 98, XOR_ASSIGN = 99, MOD_ASSIGN = 100, LSHIFT_ASSIGN = 101, 
    RSHIFT_ASSIGN = 102, URSHIFT_ASSIGN = 103, ARROW = 104, COLONCOLON = 105, 
    AT = 106, ELLIPSIS = 107, WS = 108, COMMENT = 109, LINE_COMMENT = 110, 
    IDENTIFIER = 111
  };

  enum {
    RuleCompilationUnit = 0, RulePackageDeclaration = 1, RuleImportDeclaration = 2, 
    RuleTypeDeclaration = 3, RuleModifier = 4, RuleClassOrInterfaceModifier = 5, 
    RuleVariableModifier = 6, RuleClassDeclaration = 7, RuleTypeParameters = 8, 
    RuleTypeParameter = 9, RuleTypeBound = 10, RuleEnumDeclaration = 11, 
    RuleEnumConstants = 12, RuleEnumConstant = 13, RuleEnumBodyDeclarations = 14, 
    RuleInterfaceDeclaration = 15, RuleClassBody = 16, RuleInterfaceBody = 17, 
    RuleClassBodyDeclaration = 18, RuleMemberDeclaration = 19, RuleMethodDeclaration = 20, 
    RuleMethodBody = 21, RuleTypeTypeOrVoid = 22, RuleGenericMethodDeclaration = 23, 
    RuleGenericConstructorDeclaration = 24, RuleConstructorDeclaration = 25, 
    RuleFieldDeclaration = 26, RuleInterfaceBodyDeclaration = 27, RuleInterfaceMemberDeclaration = 28, 
    RuleConstDeclaration = 29, RuleConstantDeclarator = 30, RuleInterfaceMethodDeclaration = 31, 
    RuleInterfaceMethodModifier = 32, RuleGenericInterfaceMethodDeclaration = 33, 
    RuleVariableDeclarators = 34, RuleVariableDeclarator = 35, RuleVariableDeclaratorId = 36, 
    RuleVariableInitializer = 37, RuleArrayInitializer = 38, RuleClassOrInterfaceType = 39, 
    RuleTypeArgument = 40, RuleQualifiedNameList = 41, RuleFormalParameters = 42, 
    RuleFormalParameterList = 43, RuleFormalParameter = 44, RuleLastFormalParameter = 45, 
    RuleQualifiedName = 46, RuleLiteral = 47, RuleIntegerLiteral = 48, RuleFloatLiteral = 49, 
    RuleAltAnnotationQualifiedName = 50, RuleAnnotation = 51, RuleElementValuePairs = 52, 
    RuleElementValuePair = 53, RuleElementValue = 54, RuleElementValueArrayInitializer = 55, 
    RuleAnnotationTypeDeclaration = 56, RuleAnnotationTypeBody = 57, RuleAnnotationTypeElementDeclaration = 58, 
    RuleAnnotationTypeElementRest = 59, RuleAnnotationMethodOrConstantRest = 60, 
    RuleAnnotationMethodRest = 61, RuleAnnotationConstantRest = 62, RuleDefaultValue = 63, 
    RuleBlock = 64, RuleBlockStatement = 65, RuleLocalVariableDeclaration = 66, 
    RuleLocalTypeDeclaration = 67, RuleStatement = 68, RuleCatchClause = 69, 
    RuleCatchType = 70, RuleFinallyBlock = 71, RuleResourceSpecification = 72, 
    RuleResources = 73, RuleResource = 74, RuleSwitchBlockStatementGroup = 75, 
    RuleSwitchLabel = 76, RuleForControl = 77, RuleForInit = 78, RuleEnhancedForControl = 79, 
    RuleParExpression = 80, RuleExpressionList = 81, RuleMethodCall = 82, 
    RuleExpression = 83, RuleLambdaExpression = 84, RuleLambdaParameters = 85, 
    RuleLambdaBody = 86, RulePrimary = 87, RuleClassType = 88, RuleCreator = 89, 
    RuleCreatedName = 90, RuleInnerCreator = 91, RuleArrayCreatorRest = 92, 
    RuleClassCreatorRest = 93, RuleExplicitGenericInvocation = 94, RuleTypeArgumentsOrDiamond = 95, 
    RuleNonWildcardTypeArgumentsOrDiamond = 96, RuleNonWildcardTypeArguments = 97, 
    RuleTypeList = 98, RuleTypeType = 99, RulePrimitiveType = 100, RuleTypeArguments = 101, 
    RuleSuperSuffix = 102, RuleExplicitGenericInvocationSuffix = 103, RuleArguments = 104
  };

  explicit JavaLabeledParser(antlr4::TokenStream *input);
  ~JavaLabeledParser();

  virtual std::string getGrammarFileName() const override;
  virtual const antlr4::atn::ATN& getATN() const override { return _atn; };
  virtual const std::vector<std::string>& getTokenNames() const override { return _tokenNames; }; // deprecated: use vocabulary instead.
  virtual const std::vector<std::string>& getRuleNames() const override;
  virtual antlr4::dfa::Vocabulary& getVocabulary() const override;


  class CompilationUnitContext;
  class PackageDeclarationContext;
  class ImportDeclarationContext;
  class TypeDeclarationContext;
  class ModifierContext;
  class ClassOrInterfaceModifierContext;
  class VariableModifierContext;
  class ClassDeclarationContext;
  class TypeParametersContext;
  class TypeParameterContext;
  class TypeBoundContext;
  class EnumDeclarationContext;
  class EnumConstantsContext;
  class EnumConstantContext;
  class EnumBodyDeclarationsContext;
  class InterfaceDeclarationContext;
  class ClassBodyContext;
  class InterfaceBodyContext;
  class ClassBodyDeclarationContext;
  class MemberDeclarationContext;
  class MethodDeclarationContext;
  class MethodBodyContext;
  class TypeTypeOrVoidContext;
  class GenericMethodDeclarationContext;
  class GenericConstructorDeclarationContext;
  class ConstructorDeclarationContext;
  class FieldDeclarationContext;
  class InterfaceBodyDeclarationContext;
  class InterfaceMemberDeclarationContext;
  class ConstDeclarationContext;
  class ConstantDeclaratorContext;
  class InterfaceMethodDeclarationContext;
  class InterfaceMethodModifierContext;
  class GenericInterfaceMethodDeclarationContext;
  class VariableDeclaratorsContext;
  class VariableDeclaratorContext;
  class VariableDeclaratorIdContext;
  class VariableInitializerContext;
  class ArrayInitializerContext;
  class ClassOrInterfaceTypeContext;
  class TypeArgumentContext;
  class QualifiedNameListContext;
  class FormalParametersContext;
  class FormalParameterListContext;
  class FormalParameterContext;
  class LastFormalParameterContext;
  class QualifiedNameContext;
  class LiteralContext;
  class IntegerLiteralContext;
  class FloatLiteralContext;
  class AltAnnotationQualifiedNameContext;
  class AnnotationContext;
  class ElementValuePairsContext;
  class ElementValuePairContext;
  class ElementValueContext;
  class ElementValueArrayInitializerContext;
  class AnnotationTypeDeclarationContext;
  class AnnotationTypeBodyContext;
  class AnnotationTypeElementDeclarationContext;
  class AnnotationTypeElementRestContext;
  class AnnotationMethodOrConstantRestContext;
  class AnnotationMethodRestContext;
  class AnnotationConstantRestContext;
  class DefaultValueContext;
  class BlockContext;
  class BlockStatementContext;
  class LocalVariableDeclarationContext;
  class LocalTypeDeclarationContext;
  class StatementContext;
  class CatchClauseContext;
  class CatchTypeContext;
  class FinallyBlockContext;
  class ResourceSpecificationContext;
  class ResourcesContext;
  class ResourceContext;
  class SwitchBlockStatementGroupContext;
  class SwitchLabelContext;
  class ForControlContext;
  class ForInitContext;
  class EnhancedForControlContext;
  class ParExpressionContext;
  class ExpressionListContext;
  class MethodCallContext;
  class ExpressionContext;
  class LambdaExpressionContext;
  class LambdaParametersContext;
  class LambdaBodyContext;
  class PrimaryContext;
  class ClassTypeContext;
  class CreatorContext;
  class CreatedNameContext;
  class InnerCreatorContext;
  class ArrayCreatorRestContext;
  class ClassCreatorRestContext;
  class ExplicitGenericInvocationContext;
  class TypeArgumentsOrDiamondContext;
  class NonWildcardTypeArgumentsOrDiamondContext;
  class NonWildcardTypeArgumentsContext;
  class TypeListContext;
  class TypeTypeContext;
  class PrimitiveTypeContext;
  class TypeArgumentsContext;
  class SuperSuffixContext;
  class ExplicitGenericInvocationSuffixContext;
  class ArgumentsContext; 

  class  CompilationUnitContext : public antlr4::ParserRuleContext {
  public:
    CompilationUnitContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EOF();
    PackageDeclarationContext *packageDeclaration();
    std::vector<ImportDeclarationContext *> importDeclaration();
    ImportDeclarationContext* importDeclaration(size_t i);
    std::vector<TypeDeclarationContext *> typeDeclaration();
    TypeDeclarationContext* typeDeclaration(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  CompilationUnitContext* compilationUnit();

  class  PackageDeclarationContext : public antlr4::ParserRuleContext {
  public:
    PackageDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *PACKAGE();
    QualifiedNameContext *qualifiedName();
    antlr4::tree::TerminalNode *SEMI();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PackageDeclarationContext* packageDeclaration();

  class  ImportDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ImportDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IMPORT();
    QualifiedNameContext *qualifiedName();
    antlr4::tree::TerminalNode *SEMI();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *MUL();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ImportDeclarationContext* importDeclaration();

  class  TypeDeclarationContext : public antlr4::ParserRuleContext {
  public:
    TypeDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassDeclarationContext *classDeclaration();
    EnumDeclarationContext *enumDeclaration();
    InterfaceDeclarationContext *interfaceDeclaration();
    AnnotationTypeDeclarationContext *annotationTypeDeclaration();
    std::vector<ClassOrInterfaceModifierContext *> classOrInterfaceModifier();
    ClassOrInterfaceModifierContext* classOrInterfaceModifier(size_t i);
    antlr4::tree::TerminalNode *SEMI();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeDeclarationContext* typeDeclaration();

  class  ModifierContext : public antlr4::ParserRuleContext {
  public:
    ModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassOrInterfaceModifierContext *classOrInterfaceModifier();
    antlr4::tree::TerminalNode *NATIVE();
    antlr4::tree::TerminalNode *SYNCHRONIZED();
    antlr4::tree::TerminalNode *TRANSIENT();
    antlr4::tree::TerminalNode *VOLATILE();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ModifierContext* modifier();

  class  ClassOrInterfaceModifierContext : public antlr4::ParserRuleContext {
  public:
    ClassOrInterfaceModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *PROTECTED();
    antlr4::tree::TerminalNode *PRIVATE();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *ABSTRACT();
    antlr4::tree::TerminalNode *FINAL();
    antlr4::tree::TerminalNode *STRICTFP();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassOrInterfaceModifierContext* classOrInterfaceModifier();

  class  VariableModifierContext : public antlr4::ParserRuleContext {
  public:
    VariableModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FINAL();
    AnnotationContext *annotation();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VariableModifierContext* variableModifier();

  class  ClassDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ClassDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CLASS();
    antlr4::tree::TerminalNode *IDENTIFIER();
    ClassBodyContext *classBody();
    TypeParametersContext *typeParameters();
    antlr4::tree::TerminalNode *EXTENDS();
    TypeTypeContext *typeType();
    antlr4::tree::TerminalNode *IMPLEMENTS();
    TypeListContext *typeList();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassDeclarationContext* classDeclaration();

  class  TypeParametersContext : public antlr4::ParserRuleContext {
  public:
    TypeParametersContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LT();
    std::vector<TypeParameterContext *> typeParameter();
    TypeParameterContext* typeParameter(size_t i);
    antlr4::tree::TerminalNode *GT();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeParametersContext* typeParameters();

  class  TypeParameterContext : public antlr4::ParserRuleContext {
  public:
    TypeParameterContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    antlr4::tree::TerminalNode *EXTENDS();
    TypeBoundContext *typeBound();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeParameterContext* typeParameter();

  class  TypeBoundContext : public antlr4::ParserRuleContext {
  public:
    TypeBoundContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<TypeTypeContext *> typeType();
    TypeTypeContext* typeType(size_t i);
    std::vector<antlr4::tree::TerminalNode *> BITAND();
    antlr4::tree::TerminalNode* BITAND(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeBoundContext* typeBound();

  class  EnumDeclarationContext : public antlr4::ParserRuleContext {
  public:
    EnumDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ENUM();
    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    antlr4::tree::TerminalNode *IMPLEMENTS();
    TypeListContext *typeList();
    EnumConstantsContext *enumConstants();
    antlr4::tree::TerminalNode *COMMA();
    EnumBodyDeclarationsContext *enumBodyDeclarations();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumDeclarationContext* enumDeclaration();

  class  EnumConstantsContext : public antlr4::ParserRuleContext {
  public:
    EnumConstantsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<EnumConstantContext *> enumConstant();
    EnumConstantContext* enumConstant(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumConstantsContext* enumConstants();

  class  EnumConstantContext : public antlr4::ParserRuleContext {
  public:
    EnumConstantContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    ArgumentsContext *arguments();
    ClassBodyContext *classBody();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumConstantContext* enumConstant();

  class  EnumBodyDeclarationsContext : public antlr4::ParserRuleContext {
  public:
    EnumBodyDeclarationsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *SEMI();
    std::vector<ClassBodyDeclarationContext *> classBodyDeclaration();
    ClassBodyDeclarationContext* classBodyDeclaration(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumBodyDeclarationsContext* enumBodyDeclarations();

  class  InterfaceDeclarationContext : public antlr4::ParserRuleContext {
  public:
    InterfaceDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *INTERFACE();
    antlr4::tree::TerminalNode *IDENTIFIER();
    InterfaceBodyContext *interfaceBody();
    TypeParametersContext *typeParameters();
    antlr4::tree::TerminalNode *EXTENDS();
    TypeListContext *typeList();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceDeclarationContext* interfaceDeclaration();

  class  ClassBodyContext : public antlr4::ParserRuleContext {
  public:
    ClassBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<ClassBodyDeclarationContext *> classBodyDeclaration();
    ClassBodyDeclarationContext* classBodyDeclaration(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassBodyContext* classBody();

  class  InterfaceBodyContext : public antlr4::ParserRuleContext {
  public:
    InterfaceBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<InterfaceBodyDeclarationContext *> interfaceBodyDeclaration();
    InterfaceBodyDeclarationContext* interfaceBodyDeclaration(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceBodyContext* interfaceBody();

  class  ClassBodyDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ClassBodyDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ClassBodyDeclarationContext() = default;
    void copyFrom(ClassBodyDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ClassBodyDeclaration1Context : public ClassBodyDeclarationContext {
  public:
    ClassBodyDeclaration1Context(ClassBodyDeclarationContext *ctx);

    BlockContext *block();
    antlr4::tree::TerminalNode *STATIC();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassBodyDeclaration0Context : public ClassBodyDeclarationContext {
  public:
    ClassBodyDeclaration0Context(ClassBodyDeclarationContext *ctx);

    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ClassBodyDeclaration2Context : public ClassBodyDeclarationContext {
  public:
    ClassBodyDeclaration2Context(ClassBodyDeclarationContext *ctx);

    MemberDeclarationContext *memberDeclaration();
    std::vector<ModifierContext *> modifier();
    ModifierContext* modifier(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ClassBodyDeclarationContext* classBodyDeclaration();

  class  MemberDeclarationContext : public antlr4::ParserRuleContext {
  public:
    MemberDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    MemberDeclarationContext() = default;
    void copyFrom(MemberDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  MemberDeclaration8Context : public MemberDeclarationContext {
  public:
    MemberDeclaration8Context(MemberDeclarationContext *ctx);

    EnumDeclarationContext *enumDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MemberDeclaration0Context : public MemberDeclarationContext {
  public:
    MemberDeclaration0Context(MemberDeclarationContext *ctx);

    MethodDeclarationContext *methodDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MemberDeclaration1Context : public MemberDeclarationContext {
  public:
    MemberDeclaration1Context(MemberDeclarationContext *ctx);

    GenericMethodDeclarationContext *genericMethodDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MemberDeclaration2Context : public MemberDeclarationContext {
  public:
    MemberDeclaration2Context(MemberDeclarationContext *ctx);

    FieldDeclarationContext *fieldDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MemberDeclaration3Context : public MemberDeclarationContext {
  public:
    MemberDeclaration3Context(MemberDeclarationContext *ctx);

    ConstructorDeclarationContext *constructorDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MemberDeclaration4Context : public MemberDeclarationContext {
  public:
    MemberDeclaration4Context(MemberDeclarationContext *ctx);

    GenericConstructorDeclarationContext *genericConstructorDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MemberDeclaration5Context : public MemberDeclarationContext {
  public:
    MemberDeclaration5Context(MemberDeclarationContext *ctx);

    InterfaceDeclarationContext *interfaceDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MemberDeclaration6Context : public MemberDeclarationContext {
  public:
    MemberDeclaration6Context(MemberDeclarationContext *ctx);

    AnnotationTypeDeclarationContext *annotationTypeDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MemberDeclaration7Context : public MemberDeclarationContext {
  public:
    MemberDeclaration7Context(MemberDeclarationContext *ctx);

    ClassDeclarationContext *classDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  MemberDeclarationContext* memberDeclaration();

  class  MethodDeclarationContext : public antlr4::ParserRuleContext {
  public:
    MethodDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeTypeOrVoidContext *typeTypeOrVoid();
    antlr4::tree::TerminalNode *IDENTIFIER();
    FormalParametersContext *formalParameters();
    MethodBodyContext *methodBody();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    antlr4::tree::TerminalNode *THROWS();
    QualifiedNameListContext *qualifiedNameList();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodDeclarationContext* methodDeclaration();

  class  MethodBodyContext : public antlr4::ParserRuleContext {
  public:
    MethodBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    BlockContext *block();
    antlr4::tree::TerminalNode *SEMI();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MethodBodyContext* methodBody();

  class  TypeTypeOrVoidContext : public antlr4::ParserRuleContext {
  public:
    TypeTypeOrVoidContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeTypeContext *typeType();
    antlr4::tree::TerminalNode *VOID();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeTypeOrVoidContext* typeTypeOrVoid();

  class  GenericMethodDeclarationContext : public antlr4::ParserRuleContext {
  public:
    GenericMethodDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeParametersContext *typeParameters();
    MethodDeclarationContext *methodDeclaration();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  GenericMethodDeclarationContext* genericMethodDeclaration();

  class  GenericConstructorDeclarationContext : public antlr4::ParserRuleContext {
  public:
    GenericConstructorDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeParametersContext *typeParameters();
    ConstructorDeclarationContext *constructorDeclaration();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  GenericConstructorDeclarationContext* genericConstructorDeclaration();

  class  ConstructorDeclarationContext : public antlr4::ParserRuleContext {
  public:
    JavaLabeledParser::BlockContext *constructorBody = nullptr;
    ConstructorDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    FormalParametersContext *formalParameters();
    BlockContext *block();
    antlr4::tree::TerminalNode *THROWS();
    QualifiedNameListContext *qualifiedNameList();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstructorDeclarationContext* constructorDeclaration();

  class  FieldDeclarationContext : public antlr4::ParserRuleContext {
  public:
    FieldDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeTypeContext *typeType();
    VariableDeclaratorsContext *variableDeclarators();
    antlr4::tree::TerminalNode *SEMI();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FieldDeclarationContext* fieldDeclaration();

  class  InterfaceBodyDeclarationContext : public antlr4::ParserRuleContext {
  public:
    InterfaceBodyDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    InterfaceMemberDeclarationContext *interfaceMemberDeclaration();
    std::vector<ModifierContext *> modifier();
    ModifierContext* modifier(size_t i);
    antlr4::tree::TerminalNode *SEMI();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceBodyDeclarationContext* interfaceBodyDeclaration();

  class  InterfaceMemberDeclarationContext : public antlr4::ParserRuleContext {
  public:
    InterfaceMemberDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    InterfaceMemberDeclarationContext() = default;
    void copyFrom(InterfaceMemberDeclarationContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  InterfaceMemberDeclaration6Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration6Context(InterfaceMemberDeclarationContext *ctx);

    EnumDeclarationContext *enumDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration5Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration5Context(InterfaceMemberDeclarationContext *ctx);

    ClassDeclarationContext *classDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration4Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration4Context(InterfaceMemberDeclarationContext *ctx);

    AnnotationTypeDeclarationContext *annotationTypeDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration3Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration3Context(InterfaceMemberDeclarationContext *ctx);

    InterfaceDeclarationContext *interfaceDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration2Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration2Context(InterfaceMemberDeclarationContext *ctx);

    GenericInterfaceMethodDeclarationContext *genericInterfaceMethodDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration1Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration1Context(InterfaceMemberDeclarationContext *ctx);

    InterfaceMethodDeclarationContext *interfaceMethodDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  InterfaceMemberDeclaration0Context : public InterfaceMemberDeclarationContext {
  public:
    InterfaceMemberDeclaration0Context(InterfaceMemberDeclarationContext *ctx);

    ConstDeclarationContext *constDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  InterfaceMemberDeclarationContext* interfaceMemberDeclaration();

  class  ConstDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ConstDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeTypeContext *typeType();
    std::vector<ConstantDeclaratorContext *> constantDeclarator();
    ConstantDeclaratorContext* constantDeclarator(size_t i);
    antlr4::tree::TerminalNode *SEMI();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstDeclarationContext* constDeclaration();

  class  ConstantDeclaratorContext : public antlr4::ParserRuleContext {
  public:
    ConstantDeclaratorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *ASSIGN();
    VariableInitializerContext *variableInitializer();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstantDeclaratorContext* constantDeclarator();

  class  InterfaceMethodDeclarationContext : public antlr4::ParserRuleContext {
  public:
    InterfaceMethodDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    FormalParametersContext *formalParameters();
    MethodBodyContext *methodBody();
    TypeTypeOrVoidContext *typeTypeOrVoid();
    TypeParametersContext *typeParameters();
    std::vector<InterfaceMethodModifierContext *> interfaceMethodModifier();
    InterfaceMethodModifierContext* interfaceMethodModifier(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    antlr4::tree::TerminalNode *THROWS();
    QualifiedNameListContext *qualifiedNameList();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceMethodDeclarationContext* interfaceMethodDeclaration();

  class  InterfaceMethodModifierContext : public antlr4::ParserRuleContext {
  public:
    InterfaceMethodModifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationContext *annotation();
    antlr4::tree::TerminalNode *PUBLIC();
    antlr4::tree::TerminalNode *ABSTRACT();
    antlr4::tree::TerminalNode *DEFAULT();
    antlr4::tree::TerminalNode *STATIC();
    antlr4::tree::TerminalNode *STRICTFP();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InterfaceMethodModifierContext* interfaceMethodModifier();

  class  GenericInterfaceMethodDeclarationContext : public antlr4::ParserRuleContext {
  public:
    GenericInterfaceMethodDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeParametersContext *typeParameters();
    InterfaceMethodDeclarationContext *interfaceMethodDeclaration();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  GenericInterfaceMethodDeclarationContext* genericInterfaceMethodDeclaration();

  class  VariableDeclaratorsContext : public antlr4::ParserRuleContext {
  public:
    VariableDeclaratorsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<VariableDeclaratorContext *> variableDeclarator();
    VariableDeclaratorContext* variableDeclarator(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VariableDeclaratorsContext* variableDeclarators();

  class  VariableDeclaratorContext : public antlr4::ParserRuleContext {
  public:
    VariableDeclaratorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    VariableDeclaratorIdContext *variableDeclaratorId();
    antlr4::tree::TerminalNode *ASSIGN();
    VariableInitializerContext *variableInitializer();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VariableDeclaratorContext* variableDeclarator();

  class  VariableDeclaratorIdContext : public antlr4::ParserRuleContext {
  public:
    VariableDeclaratorIdContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);


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

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  VariableInitializer0Context : public VariableInitializerContext {
  public:
    VariableInitializer0Context(VariableInitializerContext *ctx);

    ArrayInitializerContext *arrayInitializer();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  VariableInitializerContext* variableInitializer();

  class  ArrayInitializerContext : public antlr4::ParserRuleContext {
  public:
    ArrayInitializerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<VariableInitializerContext *> variableInitializer();
    VariableInitializerContext* variableInitializer(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArrayInitializerContext* arrayInitializer();

  class  ClassOrInterfaceTypeContext : public antlr4::ParserRuleContext {
  public:
    ClassOrInterfaceTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> IDENTIFIER();
    antlr4::tree::TerminalNode* IDENTIFIER(size_t i);
    std::vector<TypeArgumentsContext *> typeArguments();
    TypeArgumentsContext* typeArguments(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassOrInterfaceTypeContext* classOrInterfaceType();

  class  TypeArgumentContext : public antlr4::ParserRuleContext {
  public:
    TypeArgumentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    TypeArgumentContext() = default;
    void copyFrom(TypeArgumentContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  TypeArgument0Context : public TypeArgumentContext {
  public:
    TypeArgument0Context(TypeArgumentContext *ctx);

    TypeTypeContext *typeType();
    antlr4::tree::TerminalNode *QUESTION();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    antlr4::tree::TerminalNode *EXTENDS();
    antlr4::tree::TerminalNode *SUPER();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  TypeArgumentContext* typeArgument();

  class  QualifiedNameListContext : public antlr4::ParserRuleContext {
  public:
    QualifiedNameListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<QualifiedNameContext *> qualifiedName();
    QualifiedNameContext* qualifiedName(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  QualifiedNameListContext* qualifiedNameList();

  class  FormalParametersContext : public antlr4::ParserRuleContext {
  public:
    FormalParametersContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    FormalParameterListContext *formalParameterList();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FormalParametersContext* formalParameters();

  class  FormalParameterListContext : public antlr4::ParserRuleContext {
  public:
    FormalParameterListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    FormalParameterListContext() = default;
    void copyFrom(FormalParameterListContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  FormalParameterList1Context : public FormalParameterListContext {
  public:
    FormalParameterList1Context(FormalParameterListContext *ctx);

    LastFormalParameterContext *lastFormalParameter();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  FormalParameterList0Context : public FormalParameterListContext {
  public:
    FormalParameterList0Context(FormalParameterListContext *ctx);

    std::vector<FormalParameterContext *> formalParameter();
    FormalParameterContext* formalParameter(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    LastFormalParameterContext *lastFormalParameter();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  FormalParameterListContext* formalParameterList();

  class  FormalParameterContext : public antlr4::ParserRuleContext {
  public:
    FormalParameterContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeTypeContext *typeType();
    VariableDeclaratorIdContext *variableDeclaratorId();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FormalParameterContext* formalParameter();

  class  LastFormalParameterContext : public antlr4::ParserRuleContext {
  public:
    LastFormalParameterContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeTypeContext *typeType();
    antlr4::tree::TerminalNode *ELLIPSIS();
    VariableDeclaratorIdContext *variableDeclaratorId();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LastFormalParameterContext* lastFormalParameter();

  class  QualifiedNameContext : public antlr4::ParserRuleContext {
  public:
    QualifiedNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> IDENTIFIER();
    antlr4::tree::TerminalNode* IDENTIFIER(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  QualifiedNameContext* qualifiedName();

  class  LiteralContext : public antlr4::ParserRuleContext {
  public:
    LiteralContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    LiteralContext() = default;
    void copyFrom(LiteralContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Literal2Context : public LiteralContext {
  public:
    Literal2Context(LiteralContext *ctx);

    antlr4::tree::TerminalNode *CHAR_LITERAL();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Literal1Context : public LiteralContext {
  public:
    Literal1Context(LiteralContext *ctx);

    FloatLiteralContext *floatLiteral();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Literal0Context : public LiteralContext {
  public:
    Literal0Context(LiteralContext *ctx);

    IntegerLiteralContext *integerLiteral();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Literal5Context : public LiteralContext {
  public:
    Literal5Context(LiteralContext *ctx);

    antlr4::tree::TerminalNode *NULL_LITERAL();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Literal4Context : public LiteralContext {
  public:
    Literal4Context(LiteralContext *ctx);

    antlr4::tree::TerminalNode *BOOL_LITERAL();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Literal3Context : public LiteralContext {
  public:
    Literal3Context(LiteralContext *ctx);

    antlr4::tree::TerminalNode *STRING_LITERAL();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  LiteralContext* literal();

  class  IntegerLiteralContext : public antlr4::ParserRuleContext {
  public:
    IntegerLiteralContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DECIMAL_LITERAL();
    antlr4::tree::TerminalNode *HEX_LITERAL();
    antlr4::tree::TerminalNode *OCT_LITERAL();
    antlr4::tree::TerminalNode *BINARY_LITERAL();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IntegerLiteralContext* integerLiteral();

  class  FloatLiteralContext : public antlr4::ParserRuleContext {
  public:
    FloatLiteralContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FLOAT_LITERAL();
    antlr4::tree::TerminalNode *HEX_FLOAT_LITERAL();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FloatLiteralContext* floatLiteral();

  class  AltAnnotationQualifiedNameContext : public antlr4::ParserRuleContext {
  public:
    AltAnnotationQualifiedNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AT();
    std::vector<antlr4::tree::TerminalNode *> IDENTIFIER();
    antlr4::tree::TerminalNode* IDENTIFIER(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AltAnnotationQualifiedNameContext* altAnnotationQualifiedName();

  class  AnnotationContext : public antlr4::ParserRuleContext {
  public:
    AnnotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AT();
    QualifiedNameContext *qualifiedName();
    AltAnnotationQualifiedNameContext *altAnnotationQualifiedName();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ElementValuePairsContext *elementValuePairs();
    ElementValueContext *elementValue();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationContext* annotation();

  class  ElementValuePairsContext : public antlr4::ParserRuleContext {
  public:
    ElementValuePairsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ElementValuePairContext *> elementValuePair();
    ElementValuePairContext* elementValuePair(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ElementValuePairsContext* elementValuePairs();

  class  ElementValuePairContext : public antlr4::ParserRuleContext {
  public:
    ElementValuePairContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *ASSIGN();
    ElementValueContext *elementValue();


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

  class  ElementValue0Context : public ElementValueContext {
  public:
    ElementValue0Context(ElementValueContext *ctx);

    ExpressionContext *expression();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ElementValue2Context : public ElementValueContext {
  public:
    ElementValue2Context(ElementValueContext *ctx);

    ElementValueArrayInitializerContext *elementValueArrayInitializer();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ElementValue1Context : public ElementValueContext {
  public:
    ElementValue1Context(ElementValueContext *ctx);

    AnnotationContext *annotation();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ElementValueContext* elementValue();

  class  ElementValueArrayInitializerContext : public antlr4::ParserRuleContext {
  public:
    ElementValueArrayInitializerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<ElementValueContext *> elementValue();
    ElementValueContext* elementValue(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ElementValueArrayInitializerContext* elementValueArrayInitializer();

  class  AnnotationTypeDeclarationContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AT();
    antlr4::tree::TerminalNode *INTERFACE();
    antlr4::tree::TerminalNode *IDENTIFIER();
    AnnotationTypeBodyContext *annotationTypeBody();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationTypeDeclarationContext* annotationTypeDeclaration();

  class  AnnotationTypeBodyContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<AnnotationTypeElementDeclarationContext *> annotationTypeElementDeclaration();
    AnnotationTypeElementDeclarationContext* annotationTypeElementDeclaration(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationTypeBodyContext* annotationTypeBody();

  class  AnnotationTypeElementDeclarationContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeElementDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AnnotationTypeElementRestContext *annotationTypeElementRest();
    std::vector<ModifierContext *> modifier();
    ModifierContext* modifier(size_t i);
    antlr4::tree::TerminalNode *SEMI();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationTypeElementDeclarationContext* annotationTypeElementDeclaration();

  class  AnnotationTypeElementRestContext : public antlr4::ParserRuleContext {
  public:
    AnnotationTypeElementRestContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AnnotationTypeElementRestContext() = default;
    void copyFrom(AnnotationTypeElementRestContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  AnnotationTypeElementRest0Context : public AnnotationTypeElementRestContext {
  public:
    AnnotationTypeElementRest0Context(AnnotationTypeElementRestContext *ctx);

    TypeTypeContext *typeType();
    AnnotationMethodOrConstantRestContext *annotationMethodOrConstantRest();
    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationTypeElementRest1Context : public AnnotationTypeElementRestContext {
  public:
    AnnotationTypeElementRest1Context(AnnotationTypeElementRestContext *ctx);

    ClassDeclarationContext *classDeclaration();
    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationTypeElementRest2Context : public AnnotationTypeElementRestContext {
  public:
    AnnotationTypeElementRest2Context(AnnotationTypeElementRestContext *ctx);

    InterfaceDeclarationContext *interfaceDeclaration();
    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationTypeElementRest3Context : public AnnotationTypeElementRestContext {
  public:
    AnnotationTypeElementRest3Context(AnnotationTypeElementRestContext *ctx);

    EnumDeclarationContext *enumDeclaration();
    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationTypeElementRest4Context : public AnnotationTypeElementRestContext {
  public:
    AnnotationTypeElementRest4Context(AnnotationTypeElementRestContext *ctx);

    AnnotationTypeDeclarationContext *annotationTypeDeclaration();
    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AnnotationTypeElementRestContext* annotationTypeElementRest();

  class  AnnotationMethodOrConstantRestContext : public antlr4::ParserRuleContext {
  public:
    AnnotationMethodOrConstantRestContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AnnotationMethodOrConstantRestContext() = default;
    void copyFrom(AnnotationMethodOrConstantRestContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  AnnotationMethodOrConstantRest0Context : public AnnotationMethodOrConstantRestContext {
  public:
    AnnotationMethodOrConstantRest0Context(AnnotationMethodOrConstantRestContext *ctx);

    AnnotationMethodRestContext *annotationMethodRest();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AnnotationMethodOrConstantRest1Context : public AnnotationMethodOrConstantRestContext {
  public:
    AnnotationMethodOrConstantRest1Context(AnnotationMethodOrConstantRestContext *ctx);

    AnnotationConstantRestContext *annotationConstantRest();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AnnotationMethodOrConstantRestContext* annotationMethodOrConstantRest();

  class  AnnotationMethodRestContext : public antlr4::ParserRuleContext {
  public:
    AnnotationMethodRestContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    DefaultValueContext *defaultValue();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationMethodRestContext* annotationMethodRest();

  class  AnnotationConstantRestContext : public antlr4::ParserRuleContext {
  public:
    AnnotationConstantRestContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    VariableDeclaratorsContext *variableDeclarators();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationConstantRestContext* annotationConstantRest();

  class  DefaultValueContext : public antlr4::ParserRuleContext {
  public:
    DefaultValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DEFAULT();
    ElementValueContext *elementValue();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DefaultValueContext* defaultValue();

  class  BlockContext : public antlr4::ParserRuleContext {
  public:
    BlockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<BlockStatementContext *> blockStatement();
    BlockStatementContext* blockStatement(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  BlockContext* block();

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

    StatementContext *statement();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  BlockStatement0Context : public BlockStatementContext {
  public:
    BlockStatement0Context(BlockStatementContext *ctx);

    LocalVariableDeclarationContext *localVariableDeclaration();
    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  BlockStatement2Context : public BlockStatementContext {
  public:
    BlockStatement2Context(BlockStatementContext *ctx);

    LocalTypeDeclarationContext *localTypeDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  BlockStatementContext* blockStatement();

  class  LocalVariableDeclarationContext : public antlr4::ParserRuleContext {
  public:
    LocalVariableDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeTypeContext *typeType();
    VariableDeclaratorsContext *variableDeclarators();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LocalVariableDeclarationContext* localVariableDeclaration();

  class  LocalTypeDeclarationContext : public antlr4::ParserRuleContext {
  public:
    LocalTypeDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassDeclarationContext *classDeclaration();
    InterfaceDeclarationContext *interfaceDeclaration();
    std::vector<ClassOrInterfaceModifierContext *> classOrInterfaceModifier();
    ClassOrInterfaceModifierContext* classOrInterfaceModifier(size_t i);
    antlr4::tree::TerminalNode *SEMI();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LocalTypeDeclarationContext* localTypeDeclaration();

  class  StatementContext : public antlr4::ParserRuleContext {
  public:
    StatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    StatementContext() = default;
    void copyFrom(StatementContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Statement14Context : public StatementContext {
  public:
    Statement14Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement15Context : public StatementContext {
  public:
    Statement15Context(StatementContext *ctx);

    JavaLabeledParser::ExpressionContext *statementExpression = nullptr;
    antlr4::tree::TerminalNode *SEMI();
    ExpressionContext *expression();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement12Context : public StatementContext {
  public:
    Statement12Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *BREAK();
    antlr4::tree::TerminalNode *SEMI();
    antlr4::tree::TerminalNode *IDENTIFIER();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement13Context : public StatementContext {
  public:
    Statement13Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *CONTINUE();
    antlr4::tree::TerminalNode *SEMI();
    antlr4::tree::TerminalNode *IDENTIFIER();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement9Context : public StatementContext {
  public:
    Statement9Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *SYNCHRONIZED();
    ParExpressionContext *parExpression();
    BlockContext *block();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement7Context : public StatementContext {
  public:
    Statement7Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *TRY();
    ResourceSpecificationContext *resourceSpecification();
    BlockContext *block();
    std::vector<CatchClauseContext *> catchClause();
    CatchClauseContext* catchClause(size_t i);
    FinallyBlockContext *finallyBlock();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement16Context : public StatementContext {
  public:
    Statement16Context(StatementContext *ctx);

    antlr4::Token *identifierLabel = nullptr;
    antlr4::tree::TerminalNode *COLON();
    StatementContext *statement();
    antlr4::tree::TerminalNode *IDENTIFIER();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement8Context : public StatementContext {
  public:
    Statement8Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *SWITCH();
    ParExpressionContext *parExpression();
    antlr4::tree::TerminalNode *LBRACE();
    antlr4::tree::TerminalNode *RBRACE();
    std::vector<SwitchBlockStatementGroupContext *> switchBlockStatementGroup();
    SwitchBlockStatementGroupContext* switchBlockStatementGroup(size_t i);
    std::vector<SwitchLabelContext *> switchLabel();
    SwitchLabelContext* switchLabel(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement5Context : public StatementContext {
  public:
    Statement5Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *DO();
    StatementContext *statement();
    antlr4::tree::TerminalNode *WHILE();
    ParExpressionContext *parExpression();
    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement6Context : public StatementContext {
  public:
    Statement6Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *TRY();
    BlockContext *block();
    FinallyBlockContext *finallyBlock();
    std::vector<CatchClauseContext *> catchClause();
    CatchClauseContext* catchClause(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement3Context : public StatementContext {
  public:
    Statement3Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *FOR();
    antlr4::tree::TerminalNode *LPAREN();
    ForControlContext *forControl();
    antlr4::tree::TerminalNode *RPAREN();
    StatementContext *statement();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement4Context : public StatementContext {
  public:
    Statement4Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *WHILE();
    ParExpressionContext *parExpression();
    StatementContext *statement();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement1Context : public StatementContext {
  public:
    Statement1Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *ASSERT();
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *SEMI();
    antlr4::tree::TerminalNode *COLON();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement2Context : public StatementContext {
  public:
    Statement2Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *IF();
    ParExpressionContext *parExpression();
    std::vector<StatementContext *> statement();
    StatementContext* statement(size_t i);
    antlr4::tree::TerminalNode *ELSE();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement0Context : public StatementContext {
  public:
    Statement0Context(StatementContext *ctx);

    JavaLabeledParser::BlockContext *blockLabel = nullptr;
    BlockContext *block();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement10Context : public StatementContext {
  public:
    Statement10Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *RETURN();
    antlr4::tree::TerminalNode *SEMI();
    ExpressionContext *expression();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Statement11Context : public StatementContext {
  public:
    Statement11Context(StatementContext *ctx);

    antlr4::tree::TerminalNode *THROW();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *SEMI();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  StatementContext* statement();

  class  CatchClauseContext : public antlr4::ParserRuleContext {
  public:
    CatchClauseContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CATCH();
    antlr4::tree::TerminalNode *LPAREN();
    CatchTypeContext *catchType();
    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *RPAREN();
    BlockContext *block();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  CatchClauseContext* catchClause();

  class  CatchTypeContext : public antlr4::ParserRuleContext {
  public:
    CatchTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<QualifiedNameContext *> qualifiedName();
    QualifiedNameContext* qualifiedName(size_t i);
    std::vector<antlr4::tree::TerminalNode *> BITOR();
    antlr4::tree::TerminalNode* BITOR(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  CatchTypeContext* catchType();

  class  FinallyBlockContext : public antlr4::ParserRuleContext {
  public:
    FinallyBlockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FINALLY();
    BlockContext *block();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FinallyBlockContext* finallyBlock();

  class  ResourceSpecificationContext : public antlr4::ParserRuleContext {
  public:
    ResourceSpecificationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LPAREN();
    ResourcesContext *resources();
    antlr4::tree::TerminalNode *RPAREN();
    antlr4::tree::TerminalNode *SEMI();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ResourceSpecificationContext* resourceSpecification();

  class  ResourcesContext : public antlr4::ParserRuleContext {
  public:
    ResourcesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ResourceContext *> resource();
    ResourceContext* resource(size_t i);
    std::vector<antlr4::tree::TerminalNode *> SEMI();
    antlr4::tree::TerminalNode* SEMI(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ResourcesContext* resources();

  class  ResourceContext : public antlr4::ParserRuleContext {
  public:
    ResourceContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassOrInterfaceTypeContext *classOrInterfaceType();
    VariableDeclaratorIdContext *variableDeclaratorId();
    antlr4::tree::TerminalNode *ASSIGN();
    ExpressionContext *expression();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ResourceContext* resource();

  class  SwitchBlockStatementGroupContext : public antlr4::ParserRuleContext {
  public:
    SwitchBlockStatementGroupContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<SwitchLabelContext *> switchLabel();
    SwitchLabelContext* switchLabel(size_t i);
    std::vector<BlockStatementContext *> blockStatement();
    BlockStatementContext* blockStatement(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SwitchBlockStatementGroupContext* switchBlockStatementGroup();

  class  SwitchLabelContext : public antlr4::ParserRuleContext {
  public:
    JavaLabeledParser::ExpressionContext *constantExpression = nullptr;
    antlr4::Token *enumConstantName = nullptr;
    SwitchLabelContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CASE();
    antlr4::tree::TerminalNode *COLON();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *DEFAULT();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SwitchLabelContext* switchLabel();

  class  ForControlContext : public antlr4::ParserRuleContext {
  public:
    ForControlContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ForControlContext() = default;
    void copyFrom(ForControlContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ForControl0Context : public ForControlContext {
  public:
    ForControl0Context(ForControlContext *ctx);

    EnhancedForControlContext *enhancedForControl();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ForControl1Context : public ForControlContext {
  public:
    ForControl1Context(ForControlContext *ctx);

    JavaLabeledParser::ExpressionListContext *forUpdate = nullptr;
    std::vector<antlr4::tree::TerminalNode *> SEMI();
    antlr4::tree::TerminalNode* SEMI(size_t i);
    ForInitContext *forInit();
    ExpressionContext *expression();
    ExpressionListContext *expressionList();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ForControlContext* forControl();

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

    ExpressionListContext *expressionList();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ForInit0Context : public ForInitContext {
  public:
    ForInit0Context(ForInitContext *ctx);

    LocalVariableDeclarationContext *localVariableDeclaration();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ForInitContext* forInit();

  class  EnhancedForControlContext : public antlr4::ParserRuleContext {
  public:
    EnhancedForControlContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TypeTypeContext *typeType();
    VariableDeclaratorIdContext *variableDeclaratorId();
    antlr4::tree::TerminalNode *COLON();
    ExpressionContext *expression();
    std::vector<VariableModifierContext *> variableModifier();
    VariableModifierContext* variableModifier(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnhancedForControlContext* enhancedForControl();

  class  ParExpressionContext : public antlr4::ParserRuleContext {
  public:
    ParExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ParExpressionContext* parExpression();

  class  ExpressionListContext : public antlr4::ParserRuleContext {
  public:
    ExpressionListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExpressionListContext* expressionList();

  class  MethodCallContext : public antlr4::ParserRuleContext {
  public:
    MethodCallContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    MethodCallContext() = default;
    void copyFrom(MethodCallContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  MethodCall0Context : public MethodCallContext {
  public:
    MethodCall0Context(MethodCallContext *ctx);

    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ExpressionListContext *expressionList();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodCall1Context : public MethodCallContext {
  public:
    MethodCall1Context(MethodCallContext *ctx);

    antlr4::tree::TerminalNode *THIS();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ExpressionListContext *expressionList();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MethodCall2Context : public MethodCallContext {
  public:
    MethodCall2Context(MethodCallContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ExpressionListContext *expressionList();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  MethodCallContext* methodCall();

  class  ExpressionContext : public antlr4::ParserRuleContext {
  public:
    ExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ExpressionContext() = default;
    void copyFrom(ExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Expression8Context : public ExpressionContext {
  public:
    Expression8Context(ExpressionContext *ctx);

    antlr4::Token *prefix = nullptr;
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *TILDE();
    antlr4::tree::TerminalNode *BANG();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression10Context : public ExpressionContext {
  public:
    Expression10Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *ADD();
    antlr4::tree::TerminalNode *SUB();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression9Context : public ExpressionContext {
  public:
    Expression9Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *MUL();
    antlr4::tree::TerminalNode *DIV();
    antlr4::tree::TerminalNode *MOD();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression12Context : public ExpressionContext {
  public:
    Expression12Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *LE();
    antlr4::tree::TerminalNode *GE();
    antlr4::tree::TerminalNode *GT();
    antlr4::tree::TerminalNode *LT();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression11Context : public ExpressionContext {
  public:
    Expression11Context(ExpressionContext *ctx);

    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LT();
    antlr4::tree::TerminalNode* LT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> GT();
    antlr4::tree::TerminalNode* GT(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression14Context : public ExpressionContext {
  public:
    Expression14Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *EQUAL();
    antlr4::tree::TerminalNode *NOTEQUAL();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression13Context : public ExpressionContext {
  public:
    Expression13Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    ExpressionContext *expression();
    TypeTypeContext *typeType();
    antlr4::tree::TerminalNode *INSTANCEOF();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression16Context : public ExpressionContext {
  public:
    Expression16Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *CARET();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression15Context : public ExpressionContext {
  public:
    Expression15Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *BITAND();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression18Context : public ExpressionContext {
  public:
    Expression18Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *AND();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression17Context : public ExpressionContext {
  public:
    Expression17Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *BITOR();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression19Context : public ExpressionContext {
  public:
    Expression19Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *OR();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression6Context : public ExpressionContext {
  public:
    Expression6Context(ExpressionContext *ctx);

    antlr4::Token *postfix = nullptr;
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *INC();
    antlr4::tree::TerminalNode *DEC();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression7Context : public ExpressionContext {
  public:
    Expression7Context(ExpressionContext *ctx);

    antlr4::Token *prefix = nullptr;
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *ADD();
    antlr4::tree::TerminalNode *SUB();
    antlr4::tree::TerminalNode *INC();
    antlr4::tree::TerminalNode *DEC();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression4Context : public ExpressionContext {
  public:
    Expression4Context(ExpressionContext *ctx);

    antlr4::tree::TerminalNode *NEW();
    CreatorContext *creator();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression5Context : public ExpressionContext {
  public:
    Expression5Context(ExpressionContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    TypeTypeContext *typeType();
    antlr4::tree::TerminalNode *RPAREN();
    ExpressionContext *expression();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression2Context : public ExpressionContext {
  public:
    Expression2Context(ExpressionContext *ctx);

    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *LBRACK();
    antlr4::tree::TerminalNode *RBRACK();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression3Context : public ExpressionContext {
  public:
    Expression3Context(ExpressionContext *ctx);

    MethodCallContext *methodCall();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression0Context : public ExpressionContext {
  public:
    Expression0Context(ExpressionContext *ctx);

    PrimaryContext *primary();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression1Context : public ExpressionContext {
  public:
    Expression1Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *IDENTIFIER();
    MethodCallContext *methodCall();
    antlr4::tree::TerminalNode *THIS();
    antlr4::tree::TerminalNode *NEW();
    InnerCreatorContext *innerCreator();
    antlr4::tree::TerminalNode *SUPER();
    SuperSuffixContext *superSuffix();
    ExplicitGenericInvocationContext *explicitGenericInvocation();
    NonWildcardTypeArgumentsContext *nonWildcardTypeArguments();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression21Context : public ExpressionContext {
  public:
    Expression21Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *ASSIGN();
    antlr4::tree::TerminalNode *ADD_ASSIGN();
    antlr4::tree::TerminalNode *SUB_ASSIGN();
    antlr4::tree::TerminalNode *MUL_ASSIGN();
    antlr4::tree::TerminalNode *DIV_ASSIGN();
    antlr4::tree::TerminalNode *AND_ASSIGN();
    antlr4::tree::TerminalNode *OR_ASSIGN();
    antlr4::tree::TerminalNode *XOR_ASSIGN();
    antlr4::tree::TerminalNode *RSHIFT_ASSIGN();
    antlr4::tree::TerminalNode *URSHIFT_ASSIGN();
    antlr4::tree::TerminalNode *LSHIFT_ASSIGN();
    antlr4::tree::TerminalNode *MOD_ASSIGN();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression20Context : public ExpressionContext {
  public:
    Expression20Context(ExpressionContext *ctx);

    antlr4::Token *bop = nullptr;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *COLON();
    antlr4::tree::TerminalNode *QUESTION();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression23Context : public ExpressionContext {
  public:
    Expression23Context(ExpressionContext *ctx);

    ExpressionContext *expression();
    antlr4::tree::TerminalNode *COLONCOLON();
    antlr4::tree::TerminalNode *IDENTIFIER();
    TypeArgumentsContext *typeArguments();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression22Context : public ExpressionContext {
  public:
    Expression22Context(ExpressionContext *ctx);

    LambdaExpressionContext *lambdaExpression();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression25Context : public ExpressionContext {
  public:
    Expression25Context(ExpressionContext *ctx);

    ClassTypeContext *classType();
    antlr4::tree::TerminalNode *COLONCOLON();
    antlr4::tree::TerminalNode *NEW();
    TypeArgumentsContext *typeArguments();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Expression24Context : public ExpressionContext {
  public:
    Expression24Context(ExpressionContext *ctx);

    TypeTypeContext *typeType();
    antlr4::tree::TerminalNode *COLONCOLON();
    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *NEW();
    TypeArgumentsContext *typeArguments();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ExpressionContext* expression();
  ExpressionContext* expression(int precedence);
  class  LambdaExpressionContext : public antlr4::ParserRuleContext {
  public:
    LambdaExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    LambdaParametersContext *lambdaParameters();
    antlr4::tree::TerminalNode *ARROW();
    LambdaBodyContext *lambdaBody();


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

  class  LambdaParameters0Context : public LambdaParametersContext {
  public:
    LambdaParameters0Context(LambdaParametersContext *ctx);

    antlr4::tree::TerminalNode *IDENTIFIER();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LambdaParameters1Context : public LambdaParametersContext {
  public:
    LambdaParameters1Context(LambdaParametersContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    FormalParameterListContext *formalParameterList();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LambdaParameters2Context : public LambdaParametersContext {
  public:
    LambdaParameters2Context(LambdaParametersContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    std::vector<antlr4::tree::TerminalNode *> IDENTIFIER();
    antlr4::tree::TerminalNode* IDENTIFIER(size_t i);
    antlr4::tree::TerminalNode *RPAREN();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  LambdaParametersContext* lambdaParameters();

  class  LambdaBodyContext : public antlr4::ParserRuleContext {
  public:
    LambdaBodyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    LambdaBodyContext() = default;
    void copyFrom(LambdaBodyContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  LambdaBody0Context : public LambdaBodyContext {
  public:
    LambdaBody0Context(LambdaBodyContext *ctx);

    ExpressionContext *expression();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  LambdaBody1Context : public LambdaBodyContext {
  public:
    LambdaBody1Context(LambdaBodyContext *ctx);

    BlockContext *block();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  LambdaBodyContext* lambdaBody();

  class  PrimaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    PrimaryContext() = default;
    void copyFrom(PrimaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Primary6Context : public PrimaryContext {
  public:
    Primary6Context(PrimaryContext *ctx);

    NonWildcardTypeArgumentsContext *nonWildcardTypeArguments();
    ExplicitGenericInvocationSuffixContext *explicitGenericInvocationSuffix();
    antlr4::tree::TerminalNode *THIS();
    ArgumentsContext *arguments();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Primary2Context : public PrimaryContext {
  public:
    Primary2Context(PrimaryContext *ctx);

    antlr4::tree::TerminalNode *SUPER();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Primary3Context : public PrimaryContext {
  public:
    Primary3Context(PrimaryContext *ctx);

    LiteralContext *literal();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Primary4Context : public PrimaryContext {
  public:
    Primary4Context(PrimaryContext *ctx);

    antlr4::tree::TerminalNode *IDENTIFIER();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Primary5Context : public PrimaryContext {
  public:
    Primary5Context(PrimaryContext *ctx);

    TypeTypeOrVoidContext *typeTypeOrVoid();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *CLASS();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Primary0Context : public PrimaryContext {
  public:
    Primary0Context(PrimaryContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *RPAREN();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Primary1Context : public PrimaryContext {
  public:
    Primary1Context(PrimaryContext *ctx);

    antlr4::tree::TerminalNode *THIS();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  PrimaryContext* primary();

  class  ClassTypeContext : public antlr4::ParserRuleContext {
  public:
    ClassTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    ClassOrInterfaceTypeContext *classOrInterfaceType();
    antlr4::tree::TerminalNode *DOT();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    TypeArgumentsContext *typeArguments();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassTypeContext* classType();

  class  CreatorContext : public antlr4::ParserRuleContext {
  public:
    CreatorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    CreatorContext() = default;
    void copyFrom(CreatorContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  Creator1Context : public CreatorContext {
  public:
    Creator1Context(CreatorContext *ctx);

    CreatedNameContext *createdName();
    ArrayCreatorRestContext *arrayCreatorRest();
    ClassCreatorRestContext *classCreatorRest();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  Creator0Context : public CreatorContext {
  public:
    Creator0Context(CreatorContext *ctx);

    NonWildcardTypeArgumentsContext *nonWildcardTypeArguments();
    CreatedNameContext *createdName();
    ClassCreatorRestContext *classCreatorRest();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  CreatorContext* creator();

  class  CreatedNameContext : public antlr4::ParserRuleContext {
  public:
    CreatedNameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    CreatedNameContext() = default;
    void copyFrom(CreatedNameContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  CreatedName0Context : public CreatedNameContext {
  public:
    CreatedName0Context(CreatedNameContext *ctx);

    std::vector<antlr4::tree::TerminalNode *> IDENTIFIER();
    antlr4::tree::TerminalNode* IDENTIFIER(size_t i);
    std::vector<TypeArgumentsOrDiamondContext *> typeArgumentsOrDiamond();
    TypeArgumentsOrDiamondContext* typeArgumentsOrDiamond(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  CreatedName1Context : public CreatedNameContext {
  public:
    CreatedName1Context(CreatedNameContext *ctx);

    PrimitiveTypeContext *primitiveType();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  CreatedNameContext* createdName();

  class  InnerCreatorContext : public antlr4::ParserRuleContext {
  public:
    InnerCreatorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IDENTIFIER();
    ClassCreatorRestContext *classCreatorRest();
    NonWildcardTypeArgumentsOrDiamondContext *nonWildcardTypeArgumentsOrDiamond();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InnerCreatorContext* innerCreator();

  class  ArrayCreatorRestContext : public antlr4::ParserRuleContext {
  public:
    ArrayCreatorRestContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);
    ArrayInitializerContext *arrayInitializer();
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArrayCreatorRestContext* arrayCreatorRest();

  class  ClassCreatorRestContext : public antlr4::ParserRuleContext {
  public:
    ClassCreatorRestContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ArgumentsContext *arguments();
    ClassBodyContext *classBody();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ClassCreatorRestContext* classCreatorRest();

  class  ExplicitGenericInvocationContext : public antlr4::ParserRuleContext {
  public:
    ExplicitGenericInvocationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    NonWildcardTypeArgumentsContext *nonWildcardTypeArguments();
    ExplicitGenericInvocationSuffixContext *explicitGenericInvocationSuffix();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExplicitGenericInvocationContext* explicitGenericInvocation();

  class  TypeArgumentsOrDiamondContext : public antlr4::ParserRuleContext {
  public:
    TypeArgumentsOrDiamondContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LT();
    antlr4::tree::TerminalNode *GT();
    TypeArgumentsContext *typeArguments();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeArgumentsOrDiamondContext* typeArgumentsOrDiamond();

  class  NonWildcardTypeArgumentsOrDiamondContext : public antlr4::ParserRuleContext {
  public:
    NonWildcardTypeArgumentsOrDiamondContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LT();
    antlr4::tree::TerminalNode *GT();
    NonWildcardTypeArgumentsContext *nonWildcardTypeArguments();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  NonWildcardTypeArgumentsOrDiamondContext* nonWildcardTypeArgumentsOrDiamond();

  class  NonWildcardTypeArgumentsContext : public antlr4::ParserRuleContext {
  public:
    NonWildcardTypeArgumentsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LT();
    TypeListContext *typeList();
    antlr4::tree::TerminalNode *GT();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  NonWildcardTypeArgumentsContext* nonWildcardTypeArguments();

  class  TypeListContext : public antlr4::ParserRuleContext {
  public:
    TypeListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<TypeTypeContext *> typeType();
    TypeTypeContext* typeType(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeListContext* typeList();

  class  TypeTypeContext : public antlr4::ParserRuleContext {
  public:
    TypeTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ClassOrInterfaceTypeContext *classOrInterfaceType();
    PrimitiveTypeContext *primitiveType();
    std::vector<AnnotationContext *> annotation();
    AnnotationContext* annotation(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LBRACK();
    antlr4::tree::TerminalNode* LBRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RBRACK();
    antlr4::tree::TerminalNode* RBRACK(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeTypeContext* typeType();

  class  PrimitiveTypeContext : public antlr4::ParserRuleContext {
  public:
    PrimitiveTypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *BOOLEAN();
    antlr4::tree::TerminalNode *CHAR();
    antlr4::tree::TerminalNode *BYTE();
    antlr4::tree::TerminalNode *SHORT();
    antlr4::tree::TerminalNode *INT();
    antlr4::tree::TerminalNode *LONG();
    antlr4::tree::TerminalNode *FLOAT();
    antlr4::tree::TerminalNode *DOUBLE();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PrimitiveTypeContext* primitiveType();

  class  TypeArgumentsContext : public antlr4::ParserRuleContext {
  public:
    TypeArgumentsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LT();
    std::vector<TypeArgumentContext *> typeArgument();
    TypeArgumentContext* typeArgument(size_t i);
    antlr4::tree::TerminalNode *GT();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TypeArgumentsContext* typeArguments();

  class  SuperSuffixContext : public antlr4::ParserRuleContext {
  public:
    SuperSuffixContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    SuperSuffixContext() = default;
    void copyFrom(SuperSuffixContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  SuperSuffix1Context : public SuperSuffixContext {
  public:
    SuperSuffix1Context(SuperSuffixContext *ctx);

    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *IDENTIFIER();
    ArgumentsContext *arguments();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  SuperSuffix0Context : public SuperSuffixContext {
  public:
    SuperSuffix0Context(SuperSuffixContext *ctx);

    ArgumentsContext *arguments();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  SuperSuffixContext* superSuffix();

  class  ExplicitGenericInvocationSuffixContext : public antlr4::ParserRuleContext {
  public:
    ExplicitGenericInvocationSuffixContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ExplicitGenericInvocationSuffixContext() = default;
    void copyFrom(ExplicitGenericInvocationSuffixContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  ExplicitGenericInvocationSuffix0Context : public ExplicitGenericInvocationSuffixContext {
  public:
    ExplicitGenericInvocationSuffix0Context(ExplicitGenericInvocationSuffixContext *ctx);

    antlr4::tree::TerminalNode *SUPER();
    SuperSuffixContext *superSuffix();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ExplicitGenericInvocationSuffix1Context : public ExplicitGenericInvocationSuffixContext {
  public:
    ExplicitGenericInvocationSuffix1Context(ExplicitGenericInvocationSuffixContext *ctx);

    antlr4::tree::TerminalNode *IDENTIFIER();
    ArgumentsContext *arguments();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ExplicitGenericInvocationSuffixContext* explicitGenericInvocationSuffix();

  class  ArgumentsContext : public antlr4::ParserRuleContext {
  public:
    ArgumentsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ExpressionListContext *expressionList();


    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArgumentsContext* arguments();


  virtual bool sempred(antlr4::RuleContext *_localctx, size_t ruleIndex, size_t predicateIndex) override;
  bool expressionSempred(ExpressionContext *_localctx, size_t predicateIndex);

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

