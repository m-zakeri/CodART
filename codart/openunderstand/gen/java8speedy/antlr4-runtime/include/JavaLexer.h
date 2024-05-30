
// Generated from JavaLexer.g4 by ANTLR 4.9.1

#pragma once


#include "antlr4-runtime.h"




class  JavaLexer : public antlr4::Lexer {
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

  explicit JavaLexer(antlr4::CharStream *input);
  ~JavaLexer();

  virtual std::string getGrammarFileName() const override;
  virtual const std::vector<std::string>& getRuleNames() const override;

  virtual const std::vector<std::string>& getChannelNames() const override;
  virtual const std::vector<std::string>& getModeNames() const override;
  virtual const std::vector<std::string>& getTokenNames() const override; // deprecated, use vocabulary instead
  virtual antlr4::dfa::Vocabulary& getVocabulary() const override;

  virtual const std::vector<uint16_t> getSerializedATN() const override;
  virtual const antlr4::atn::ATN& getATN() const override;

private:
  static std::vector<antlr4::dfa::DFA> _decisionToDFA;
  static antlr4::atn::PredictionContextCache _sharedContextCache;
  static std::vector<std::string> _ruleNames;
  static std::vector<std::string> _tokenNames;
  static std::vector<std::string> _channelNames;
  static std::vector<std::string> _modeNames;

  static std::vector<std::string> _literalNames;
  static std::vector<std::string> _symbolicNames;
  static antlr4::dfa::Vocabulary _vocabulary;
  static antlr4::atn::ATN _atn;
  static std::vector<uint16_t> _serializedATN;


  // Individual action functions triggered by action() above.

  // Individual semantic predicate functions triggered by sempred() above.

  struct Initializer {
    Initializer();
  };
  static Initializer _init;
};

