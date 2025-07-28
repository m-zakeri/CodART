
// Generated from JavaLabeledParser.g4 by ANTLR 4.9.3


#include "JavaLabeledParserListener.h"
#include "JavaLabeledParserVisitor.h"

#include "JavaLabeledParser.h"


using namespace antlrcpp;
using namespace antlr4;

JavaLabeledParser::JavaLabeledParser(TokenStream *input) : Parser(input) {
  _interpreter = new atn::ParserATNSimulator(this, _atn, _decisionToDFA, _sharedContextCache);
}

JavaLabeledParser::~JavaLabeledParser() {
  delete _interpreter;
}

std::string JavaLabeledParser::getGrammarFileName() const {
  return "JavaLabeledParser.g4";
}

const std::vector<std::string>& JavaLabeledParser::getRuleNames() const {
  return _ruleNames;
}

dfa::Vocabulary& JavaLabeledParser::getVocabulary() const {
  return _vocabulary;
}


//----------------- CompilationUnitContext ------------------------------------------------------------------

JavaLabeledParser::CompilationUnitContext::CompilationUnitContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::CompilationUnitContext::EOF() {
  return getToken(JavaLabeledParser::EOF, 0);
}

JavaLabeledParser::PackageDeclarationContext* JavaLabeledParser::CompilationUnitContext::packageDeclaration() {
  return getRuleContext<JavaLabeledParser::PackageDeclarationContext>(0);
}

std::vector<JavaLabeledParser::ImportDeclarationContext *> JavaLabeledParser::CompilationUnitContext::importDeclaration() {
  return getRuleContexts<JavaLabeledParser::ImportDeclarationContext>();
}

JavaLabeledParser::ImportDeclarationContext* JavaLabeledParser::CompilationUnitContext::importDeclaration(size_t i) {
  return getRuleContext<JavaLabeledParser::ImportDeclarationContext>(i);
}

std::vector<JavaLabeledParser::TypeDeclarationContext *> JavaLabeledParser::CompilationUnitContext::typeDeclaration() {
  return getRuleContexts<JavaLabeledParser::TypeDeclarationContext>();
}

JavaLabeledParser::TypeDeclarationContext* JavaLabeledParser::CompilationUnitContext::typeDeclaration(size_t i) {
  return getRuleContext<JavaLabeledParser::TypeDeclarationContext>(i);
}


size_t JavaLabeledParser::CompilationUnitContext::getRuleIndex() const {
  return JavaLabeledParser::RuleCompilationUnit;
}

void JavaLabeledParser::CompilationUnitContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCompilationUnit(this);
}

void JavaLabeledParser::CompilationUnitContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCompilationUnit(this);
}


antlrcpp::Any JavaLabeledParser::CompilationUnitContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitCompilationUnit(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::CompilationUnitContext* JavaLabeledParser::compilationUnit() {
  CompilationUnitContext *_localctx = _tracker.createInstance<CompilationUnitContext>(_ctx, getState());
  enterRule(_localctx, 0, JavaLabeledParser::RuleCompilationUnit);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(211);
    _errHandler->sync(this);

    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 0, _ctx)) {
    case 1: {
      setState(210);
      packageDeclaration();
      break;
    }

    default:
      break;
    }
    setState(216);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::IMPORT) {
      setState(213);
      importDeclaration();
      setState(218);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(222);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::ABSTRACT)
      | (1ULL << JavaLabeledParser::CLASS)
      | (1ULL << JavaLabeledParser::ENUM)
      | (1ULL << JavaLabeledParser::FINAL)
      | (1ULL << JavaLabeledParser::INTERFACE)
      | (1ULL << JavaLabeledParser::PRIVATE)
      | (1ULL << JavaLabeledParser::PROTECTED)
      | (1ULL << JavaLabeledParser::PUBLIC)
      | (1ULL << JavaLabeledParser::STATIC)
      | (1ULL << JavaLabeledParser::STRICTFP))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaLabeledParser::SEMI - 67))
      | (1ULL << (JavaLabeledParser::AT - 67))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 67)))) != 0)) {
      setState(219);
      typeDeclaration();
      setState(224);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(225);
    match(JavaLabeledParser::EOF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PackageDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::PackageDeclarationContext::PackageDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::PackageDeclarationContext::PACKAGE() {
  return getToken(JavaLabeledParser::PACKAGE, 0);
}

JavaLabeledParser::QualifiedNameContext* JavaLabeledParser::PackageDeclarationContext::qualifiedName() {
  return getRuleContext<JavaLabeledParser::QualifiedNameContext>(0);
}

tree::TerminalNode* JavaLabeledParser::PackageDeclarationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::PackageDeclarationContext::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::PackageDeclarationContext::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}


size_t JavaLabeledParser::PackageDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RulePackageDeclaration;
}

void JavaLabeledParser::PackageDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPackageDeclaration(this);
}

void JavaLabeledParser::PackageDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPackageDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::PackageDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPackageDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::PackageDeclarationContext* JavaLabeledParser::packageDeclaration() {
  PackageDeclarationContext *_localctx = _tracker.createInstance<PackageDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 2, JavaLabeledParser::RulePackageDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(230);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::AT

    || _la == JavaLabeledParser::IDENTIFIER) {
      setState(227);
      annotation();
      setState(232);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(233);
    match(JavaLabeledParser::PACKAGE);
    setState(234);
    qualifiedName();
    setState(235);
    match(JavaLabeledParser::SEMI);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ImportDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::ImportDeclarationContext::ImportDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ImportDeclarationContext::IMPORT() {
  return getToken(JavaLabeledParser::IMPORT, 0);
}

JavaLabeledParser::QualifiedNameContext* JavaLabeledParser::ImportDeclarationContext::qualifiedName() {
  return getRuleContext<JavaLabeledParser::QualifiedNameContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ImportDeclarationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

tree::TerminalNode* JavaLabeledParser::ImportDeclarationContext::STATIC() {
  return getToken(JavaLabeledParser::STATIC, 0);
}

tree::TerminalNode* JavaLabeledParser::ImportDeclarationContext::DOT() {
  return getToken(JavaLabeledParser::DOT, 0);
}

tree::TerminalNode* JavaLabeledParser::ImportDeclarationContext::MUL() {
  return getToken(JavaLabeledParser::MUL, 0);
}


size_t JavaLabeledParser::ImportDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleImportDeclaration;
}

void JavaLabeledParser::ImportDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterImportDeclaration(this);
}

void JavaLabeledParser::ImportDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitImportDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::ImportDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitImportDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ImportDeclarationContext* JavaLabeledParser::importDeclaration() {
  ImportDeclarationContext *_localctx = _tracker.createInstance<ImportDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 4, JavaLabeledParser::RuleImportDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(237);
    match(JavaLabeledParser::IMPORT);
    setState(239);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::STATIC) {
      setState(238);
      match(JavaLabeledParser::STATIC);
    }
    setState(241);
    qualifiedName();
    setState(244);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::DOT) {
      setState(242);
      match(JavaLabeledParser::DOT);
      setState(243);
      match(JavaLabeledParser::MUL);
    }
    setState(246);
    match(JavaLabeledParser::SEMI);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::TypeDeclarationContext::TypeDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::ClassDeclarationContext* JavaLabeledParser::TypeDeclarationContext::classDeclaration() {
  return getRuleContext<JavaLabeledParser::ClassDeclarationContext>(0);
}

JavaLabeledParser::EnumDeclarationContext* JavaLabeledParser::TypeDeclarationContext::enumDeclaration() {
  return getRuleContext<JavaLabeledParser::EnumDeclarationContext>(0);
}

JavaLabeledParser::InterfaceDeclarationContext* JavaLabeledParser::TypeDeclarationContext::interfaceDeclaration() {
  return getRuleContext<JavaLabeledParser::InterfaceDeclarationContext>(0);
}

JavaLabeledParser::AnnotationTypeDeclarationContext* JavaLabeledParser::TypeDeclarationContext::annotationTypeDeclaration() {
  return getRuleContext<JavaLabeledParser::AnnotationTypeDeclarationContext>(0);
}

std::vector<JavaLabeledParser::ClassOrInterfaceModifierContext *> JavaLabeledParser::TypeDeclarationContext::classOrInterfaceModifier() {
  return getRuleContexts<JavaLabeledParser::ClassOrInterfaceModifierContext>();
}

JavaLabeledParser::ClassOrInterfaceModifierContext* JavaLabeledParser::TypeDeclarationContext::classOrInterfaceModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::ClassOrInterfaceModifierContext>(i);
}

tree::TerminalNode* JavaLabeledParser::TypeDeclarationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}


size_t JavaLabeledParser::TypeDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeDeclaration;
}

void JavaLabeledParser::TypeDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeDeclaration(this);
}

void JavaLabeledParser::TypeDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::TypeDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeDeclarationContext* JavaLabeledParser::typeDeclaration() {
  TypeDeclarationContext *_localctx = _tracker.createInstance<TypeDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 6, JavaLabeledParser::RuleTypeDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    setState(261);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::ABSTRACT:
      case JavaLabeledParser::CLASS:
      case JavaLabeledParser::ENUM:
      case JavaLabeledParser::FINAL:
      case JavaLabeledParser::INTERFACE:
      case JavaLabeledParser::PRIVATE:
      case JavaLabeledParser::PROTECTED:
      case JavaLabeledParser::PUBLIC:
      case JavaLabeledParser::STATIC:
      case JavaLabeledParser::STRICTFP:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(251);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 6, _ctx);
        while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
          if (alt == 1) {
            setState(248);
            classOrInterfaceModifier(); 
          }
          setState(253);
          _errHandler->sync(this);
          alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 6, _ctx);
        }
        setState(258);
        _errHandler->sync(this);
        switch (_input->LA(1)) {
          case JavaLabeledParser::CLASS: {
            setState(254);
            classDeclaration();
            break;
          }

          case JavaLabeledParser::ENUM: {
            setState(255);
            enumDeclaration();
            break;
          }

          case JavaLabeledParser::INTERFACE: {
            setState(256);
            interfaceDeclaration();
            break;
          }

          case JavaLabeledParser::AT: {
            setState(257);
            annotationTypeDeclaration();
            break;
          }

        default:
          throw NoViableAltException(this);
        }
        break;
      }

      case JavaLabeledParser::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(260);
        match(JavaLabeledParser::SEMI);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ModifierContext ------------------------------------------------------------------

JavaLabeledParser::ModifierContext::ModifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::ClassOrInterfaceModifierContext* JavaLabeledParser::ModifierContext::classOrInterfaceModifier() {
  return getRuleContext<JavaLabeledParser::ClassOrInterfaceModifierContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ModifierContext::NATIVE() {
  return getToken(JavaLabeledParser::NATIVE, 0);
}

tree::TerminalNode* JavaLabeledParser::ModifierContext::SYNCHRONIZED() {
  return getToken(JavaLabeledParser::SYNCHRONIZED, 0);
}

tree::TerminalNode* JavaLabeledParser::ModifierContext::TRANSIENT() {
  return getToken(JavaLabeledParser::TRANSIENT, 0);
}

tree::TerminalNode* JavaLabeledParser::ModifierContext::VOLATILE() {
  return getToken(JavaLabeledParser::VOLATILE, 0);
}


size_t JavaLabeledParser::ModifierContext::getRuleIndex() const {
  return JavaLabeledParser::RuleModifier;
}

void JavaLabeledParser::ModifierContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterModifier(this);
}

void JavaLabeledParser::ModifierContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitModifier(this);
}


antlrcpp::Any JavaLabeledParser::ModifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitModifier(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ModifierContext* JavaLabeledParser::modifier() {
  ModifierContext *_localctx = _tracker.createInstance<ModifierContext>(_ctx, getState());
  enterRule(_localctx, 8, JavaLabeledParser::RuleModifier);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(268);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::ABSTRACT:
      case JavaLabeledParser::FINAL:
      case JavaLabeledParser::PRIVATE:
      case JavaLabeledParser::PROTECTED:
      case JavaLabeledParser::PUBLIC:
      case JavaLabeledParser::STATIC:
      case JavaLabeledParser::STRICTFP:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(263);
        classOrInterfaceModifier();
        break;
      }

      case JavaLabeledParser::NATIVE: {
        enterOuterAlt(_localctx, 2);
        setState(264);
        match(JavaLabeledParser::NATIVE);
        break;
      }

      case JavaLabeledParser::SYNCHRONIZED: {
        enterOuterAlt(_localctx, 3);
        setState(265);
        match(JavaLabeledParser::SYNCHRONIZED);
        break;
      }

      case JavaLabeledParser::TRANSIENT: {
        enterOuterAlt(_localctx, 4);
        setState(266);
        match(JavaLabeledParser::TRANSIENT);
        break;
      }

      case JavaLabeledParser::VOLATILE: {
        enterOuterAlt(_localctx, 5);
        setState(267);
        match(JavaLabeledParser::VOLATILE);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassOrInterfaceModifierContext ------------------------------------------------------------------

JavaLabeledParser::ClassOrInterfaceModifierContext::ClassOrInterfaceModifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::ClassOrInterfaceModifierContext::annotation() {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceModifierContext::PUBLIC() {
  return getToken(JavaLabeledParser::PUBLIC, 0);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceModifierContext::PROTECTED() {
  return getToken(JavaLabeledParser::PROTECTED, 0);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceModifierContext::PRIVATE() {
  return getToken(JavaLabeledParser::PRIVATE, 0);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceModifierContext::STATIC() {
  return getToken(JavaLabeledParser::STATIC, 0);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceModifierContext::ABSTRACT() {
  return getToken(JavaLabeledParser::ABSTRACT, 0);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceModifierContext::FINAL() {
  return getToken(JavaLabeledParser::FINAL, 0);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceModifierContext::STRICTFP() {
  return getToken(JavaLabeledParser::STRICTFP, 0);
}


size_t JavaLabeledParser::ClassOrInterfaceModifierContext::getRuleIndex() const {
  return JavaLabeledParser::RuleClassOrInterfaceModifier;
}

void JavaLabeledParser::ClassOrInterfaceModifierContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassOrInterfaceModifier(this);
}

void JavaLabeledParser::ClassOrInterfaceModifierContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassOrInterfaceModifier(this);
}


antlrcpp::Any JavaLabeledParser::ClassOrInterfaceModifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassOrInterfaceModifier(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ClassOrInterfaceModifierContext* JavaLabeledParser::classOrInterfaceModifier() {
  ClassOrInterfaceModifierContext *_localctx = _tracker.createInstance<ClassOrInterfaceModifierContext>(_ctx, getState());
  enterRule(_localctx, 10, JavaLabeledParser::RuleClassOrInterfaceModifier);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(278);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(270);
        annotation();
        break;
      }

      case JavaLabeledParser::PUBLIC: {
        enterOuterAlt(_localctx, 2);
        setState(271);
        match(JavaLabeledParser::PUBLIC);
        break;
      }

      case JavaLabeledParser::PROTECTED: {
        enterOuterAlt(_localctx, 3);
        setState(272);
        match(JavaLabeledParser::PROTECTED);
        break;
      }

      case JavaLabeledParser::PRIVATE: {
        enterOuterAlt(_localctx, 4);
        setState(273);
        match(JavaLabeledParser::PRIVATE);
        break;
      }

      case JavaLabeledParser::STATIC: {
        enterOuterAlt(_localctx, 5);
        setState(274);
        match(JavaLabeledParser::STATIC);
        break;
      }

      case JavaLabeledParser::ABSTRACT: {
        enterOuterAlt(_localctx, 6);
        setState(275);
        match(JavaLabeledParser::ABSTRACT);
        break;
      }

      case JavaLabeledParser::FINAL: {
        enterOuterAlt(_localctx, 7);
        setState(276);
        match(JavaLabeledParser::FINAL);
        break;
      }

      case JavaLabeledParser::STRICTFP: {
        enterOuterAlt(_localctx, 8);
        setState(277);
        match(JavaLabeledParser::STRICTFP);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- VariableModifierContext ------------------------------------------------------------------

JavaLabeledParser::VariableModifierContext::VariableModifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::VariableModifierContext::FINAL() {
  return getToken(JavaLabeledParser::FINAL, 0);
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::VariableModifierContext::annotation() {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(0);
}


size_t JavaLabeledParser::VariableModifierContext::getRuleIndex() const {
  return JavaLabeledParser::RuleVariableModifier;
}

void JavaLabeledParser::VariableModifierContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableModifier(this);
}

void JavaLabeledParser::VariableModifierContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableModifier(this);
}


antlrcpp::Any JavaLabeledParser::VariableModifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitVariableModifier(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::VariableModifierContext* JavaLabeledParser::variableModifier() {
  VariableModifierContext *_localctx = _tracker.createInstance<VariableModifierContext>(_ctx, getState());
  enterRule(_localctx, 12, JavaLabeledParser::RuleVariableModifier);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(282);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::FINAL: {
        enterOuterAlt(_localctx, 1);
        setState(280);
        match(JavaLabeledParser::FINAL);
        break;
      }

      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 2);
        setState(281);
        annotation();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::ClassDeclarationContext::ClassDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ClassDeclarationContext::CLASS() {
  return getToken(JavaLabeledParser::CLASS, 0);
}

tree::TerminalNode* JavaLabeledParser::ClassDeclarationContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::ClassBodyContext* JavaLabeledParser::ClassDeclarationContext::classBody() {
  return getRuleContext<JavaLabeledParser::ClassBodyContext>(0);
}

JavaLabeledParser::TypeParametersContext* JavaLabeledParser::ClassDeclarationContext::typeParameters() {
  return getRuleContext<JavaLabeledParser::TypeParametersContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ClassDeclarationContext::EXTENDS() {
  return getToken(JavaLabeledParser::EXTENDS, 0);
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::ClassDeclarationContext::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ClassDeclarationContext::IMPLEMENTS() {
  return getToken(JavaLabeledParser::IMPLEMENTS, 0);
}

JavaLabeledParser::TypeListContext* JavaLabeledParser::ClassDeclarationContext::typeList() {
  return getRuleContext<JavaLabeledParser::TypeListContext>(0);
}


size_t JavaLabeledParser::ClassDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleClassDeclaration;
}

void JavaLabeledParser::ClassDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassDeclaration(this);
}

void JavaLabeledParser::ClassDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::ClassDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ClassDeclarationContext* JavaLabeledParser::classDeclaration() {
  ClassDeclarationContext *_localctx = _tracker.createInstance<ClassDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 14, JavaLabeledParser::RuleClassDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(284);
    match(JavaLabeledParser::CLASS);
    setState(285);
    match(JavaLabeledParser::IDENTIFIER);
    setState(287);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::LT) {
      setState(286);
      typeParameters();
    }
    setState(291);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::EXTENDS) {
      setState(289);
      match(JavaLabeledParser::EXTENDS);
      setState(290);
      typeType();
    }
    setState(295);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::IMPLEMENTS) {
      setState(293);
      match(JavaLabeledParser::IMPLEMENTS);
      setState(294);
      typeList();
    }
    setState(297);
    classBody();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeParametersContext ------------------------------------------------------------------

JavaLabeledParser::TypeParametersContext::TypeParametersContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::TypeParametersContext::LT() {
  return getToken(JavaLabeledParser::LT, 0);
}

std::vector<JavaLabeledParser::TypeParameterContext *> JavaLabeledParser::TypeParametersContext::typeParameter() {
  return getRuleContexts<JavaLabeledParser::TypeParameterContext>();
}

JavaLabeledParser::TypeParameterContext* JavaLabeledParser::TypeParametersContext::typeParameter(size_t i) {
  return getRuleContext<JavaLabeledParser::TypeParameterContext>(i);
}

tree::TerminalNode* JavaLabeledParser::TypeParametersContext::GT() {
  return getToken(JavaLabeledParser::GT, 0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::TypeParametersContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::TypeParametersContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::TypeParametersContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeParameters;
}

void JavaLabeledParser::TypeParametersContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeParameters(this);
}

void JavaLabeledParser::TypeParametersContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeParameters(this);
}


antlrcpp::Any JavaLabeledParser::TypeParametersContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeParameters(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeParametersContext* JavaLabeledParser::typeParameters() {
  TypeParametersContext *_localctx = _tracker.createInstance<TypeParametersContext>(_ctx, getState());
  enterRule(_localctx, 16, JavaLabeledParser::RuleTypeParameters);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(299);
    match(JavaLabeledParser::LT);
    setState(300);
    typeParameter();
    setState(305);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::COMMA) {
      setState(301);
      match(JavaLabeledParser::COMMA);
      setState(302);
      typeParameter();
      setState(307);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(308);
    match(JavaLabeledParser::GT);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeParameterContext ------------------------------------------------------------------

JavaLabeledParser::TypeParameterContext::TypeParameterContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::TypeParameterContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::TypeParameterContext::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::TypeParameterContext::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}

tree::TerminalNode* JavaLabeledParser::TypeParameterContext::EXTENDS() {
  return getToken(JavaLabeledParser::EXTENDS, 0);
}

JavaLabeledParser::TypeBoundContext* JavaLabeledParser::TypeParameterContext::typeBound() {
  return getRuleContext<JavaLabeledParser::TypeBoundContext>(0);
}


size_t JavaLabeledParser::TypeParameterContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeParameter;
}

void JavaLabeledParser::TypeParameterContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeParameter(this);
}

void JavaLabeledParser::TypeParameterContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeParameter(this);
}


antlrcpp::Any JavaLabeledParser::TypeParameterContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeParameter(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeParameterContext* JavaLabeledParser::typeParameter() {
  TypeParameterContext *_localctx = _tracker.createInstance<TypeParameterContext>(_ctx, getState());
  enterRule(_localctx, 18, JavaLabeledParser::RuleTypeParameter);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(313);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 16, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(310);
        annotation(); 
      }
      setState(315);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 16, _ctx);
    }
    setState(316);
    match(JavaLabeledParser::IDENTIFIER);
    setState(325);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::EXTENDS) {
      setState(317);
      match(JavaLabeledParser::EXTENDS);
      setState(321);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 17, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(318);
          annotation(); 
        }
        setState(323);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 17, _ctx);
      }
      setState(324);
      typeBound();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeBoundContext ------------------------------------------------------------------

JavaLabeledParser::TypeBoundContext::TypeBoundContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::TypeTypeContext *> JavaLabeledParser::TypeBoundContext::typeType() {
  return getRuleContexts<JavaLabeledParser::TypeTypeContext>();
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::TypeBoundContext::typeType(size_t i) {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::TypeBoundContext::BITAND() {
  return getTokens(JavaLabeledParser::BITAND);
}

tree::TerminalNode* JavaLabeledParser::TypeBoundContext::BITAND(size_t i) {
  return getToken(JavaLabeledParser::BITAND, i);
}


size_t JavaLabeledParser::TypeBoundContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeBound;
}

void JavaLabeledParser::TypeBoundContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeBound(this);
}

void JavaLabeledParser::TypeBoundContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeBound(this);
}


antlrcpp::Any JavaLabeledParser::TypeBoundContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeBound(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeBoundContext* JavaLabeledParser::typeBound() {
  TypeBoundContext *_localctx = _tracker.createInstance<TypeBoundContext>(_ctx, getState());
  enterRule(_localctx, 20, JavaLabeledParser::RuleTypeBound);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(327);
    typeType();
    setState(332);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::BITAND) {
      setState(328);
      match(JavaLabeledParser::BITAND);
      setState(329);
      typeType();
      setState(334);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- EnumDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::EnumDeclarationContext::EnumDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::EnumDeclarationContext::ENUM() {
  return getToken(JavaLabeledParser::ENUM, 0);
}

tree::TerminalNode* JavaLabeledParser::EnumDeclarationContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

tree::TerminalNode* JavaLabeledParser::EnumDeclarationContext::LBRACE() {
  return getToken(JavaLabeledParser::LBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::EnumDeclarationContext::RBRACE() {
  return getToken(JavaLabeledParser::RBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::EnumDeclarationContext::IMPLEMENTS() {
  return getToken(JavaLabeledParser::IMPLEMENTS, 0);
}

JavaLabeledParser::TypeListContext* JavaLabeledParser::EnumDeclarationContext::typeList() {
  return getRuleContext<JavaLabeledParser::TypeListContext>(0);
}

JavaLabeledParser::EnumConstantsContext* JavaLabeledParser::EnumDeclarationContext::enumConstants() {
  return getRuleContext<JavaLabeledParser::EnumConstantsContext>(0);
}

tree::TerminalNode* JavaLabeledParser::EnumDeclarationContext::COMMA() {
  return getToken(JavaLabeledParser::COMMA, 0);
}

JavaLabeledParser::EnumBodyDeclarationsContext* JavaLabeledParser::EnumDeclarationContext::enumBodyDeclarations() {
  return getRuleContext<JavaLabeledParser::EnumBodyDeclarationsContext>(0);
}


size_t JavaLabeledParser::EnumDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleEnumDeclaration;
}

void JavaLabeledParser::EnumDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnumDeclaration(this);
}

void JavaLabeledParser::EnumDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnumDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::EnumDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitEnumDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::EnumDeclarationContext* JavaLabeledParser::enumDeclaration() {
  EnumDeclarationContext *_localctx = _tracker.createInstance<EnumDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 22, JavaLabeledParser::RuleEnumDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(335);
    match(JavaLabeledParser::ENUM);
    setState(336);
    match(JavaLabeledParser::IDENTIFIER);
    setState(339);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::IMPLEMENTS) {
      setState(337);
      match(JavaLabeledParser::IMPLEMENTS);
      setState(338);
      typeList();
    }
    setState(341);
    match(JavaLabeledParser::LBRACE);
    setState(343);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::AT

    || _la == JavaLabeledParser::IDENTIFIER) {
      setState(342);
      enumConstants();
    }
    setState(346);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::COMMA) {
      setState(345);
      match(JavaLabeledParser::COMMA);
    }
    setState(349);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::SEMI) {
      setState(348);
      enumBodyDeclarations();
    }
    setState(351);
    match(JavaLabeledParser::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- EnumConstantsContext ------------------------------------------------------------------

JavaLabeledParser::EnumConstantsContext::EnumConstantsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::EnumConstantContext *> JavaLabeledParser::EnumConstantsContext::enumConstant() {
  return getRuleContexts<JavaLabeledParser::EnumConstantContext>();
}

JavaLabeledParser::EnumConstantContext* JavaLabeledParser::EnumConstantsContext::enumConstant(size_t i) {
  return getRuleContext<JavaLabeledParser::EnumConstantContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::EnumConstantsContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::EnumConstantsContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::EnumConstantsContext::getRuleIndex() const {
  return JavaLabeledParser::RuleEnumConstants;
}

void JavaLabeledParser::EnumConstantsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnumConstants(this);
}

void JavaLabeledParser::EnumConstantsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnumConstants(this);
}


antlrcpp::Any JavaLabeledParser::EnumConstantsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitEnumConstants(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::EnumConstantsContext* JavaLabeledParser::enumConstants() {
  EnumConstantsContext *_localctx = _tracker.createInstance<EnumConstantsContext>(_ctx, getState());
  enterRule(_localctx, 24, JavaLabeledParser::RuleEnumConstants);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(353);
    enumConstant();
    setState(358);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 24, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(354);
        match(JavaLabeledParser::COMMA);
        setState(355);
        enumConstant(); 
      }
      setState(360);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 24, _ctx);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- EnumConstantContext ------------------------------------------------------------------

JavaLabeledParser::EnumConstantContext::EnumConstantContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::EnumConstantContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::EnumConstantContext::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::EnumConstantContext::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}

JavaLabeledParser::ArgumentsContext* JavaLabeledParser::EnumConstantContext::arguments() {
  return getRuleContext<JavaLabeledParser::ArgumentsContext>(0);
}

JavaLabeledParser::ClassBodyContext* JavaLabeledParser::EnumConstantContext::classBody() {
  return getRuleContext<JavaLabeledParser::ClassBodyContext>(0);
}


size_t JavaLabeledParser::EnumConstantContext::getRuleIndex() const {
  return JavaLabeledParser::RuleEnumConstant;
}

void JavaLabeledParser::EnumConstantContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnumConstant(this);
}

void JavaLabeledParser::EnumConstantContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnumConstant(this);
}


antlrcpp::Any JavaLabeledParser::EnumConstantContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitEnumConstant(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::EnumConstantContext* JavaLabeledParser::enumConstant() {
  EnumConstantContext *_localctx = _tracker.createInstance<EnumConstantContext>(_ctx, getState());
  enterRule(_localctx, 26, JavaLabeledParser::RuleEnumConstant);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(364);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 25, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(361);
        annotation(); 
      }
      setState(366);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 25, _ctx);
    }
    setState(367);
    match(JavaLabeledParser::IDENTIFIER);
    setState(369);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::LPAREN) {
      setState(368);
      arguments();
    }
    setState(372);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::LBRACE) {
      setState(371);
      classBody();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- EnumBodyDeclarationsContext ------------------------------------------------------------------

JavaLabeledParser::EnumBodyDeclarationsContext::EnumBodyDeclarationsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::EnumBodyDeclarationsContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

std::vector<JavaLabeledParser::ClassBodyDeclarationContext *> JavaLabeledParser::EnumBodyDeclarationsContext::classBodyDeclaration() {
  return getRuleContexts<JavaLabeledParser::ClassBodyDeclarationContext>();
}

JavaLabeledParser::ClassBodyDeclarationContext* JavaLabeledParser::EnumBodyDeclarationsContext::classBodyDeclaration(size_t i) {
  return getRuleContext<JavaLabeledParser::ClassBodyDeclarationContext>(i);
}


size_t JavaLabeledParser::EnumBodyDeclarationsContext::getRuleIndex() const {
  return JavaLabeledParser::RuleEnumBodyDeclarations;
}

void JavaLabeledParser::EnumBodyDeclarationsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnumBodyDeclarations(this);
}

void JavaLabeledParser::EnumBodyDeclarationsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnumBodyDeclarations(this);
}


antlrcpp::Any JavaLabeledParser::EnumBodyDeclarationsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitEnumBodyDeclarations(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::EnumBodyDeclarationsContext* JavaLabeledParser::enumBodyDeclarations() {
  EnumBodyDeclarationsContext *_localctx = _tracker.createInstance<EnumBodyDeclarationsContext>(_ctx, getState());
  enterRule(_localctx, 28, JavaLabeledParser::RuleEnumBodyDeclarations);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(374);
    match(JavaLabeledParser::SEMI);
    setState(378);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::ABSTRACT)
      | (1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::CLASS)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::ENUM)
      | (1ULL << JavaLabeledParser::FINAL)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::INTERFACE)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NATIVE)
      | (1ULL << JavaLabeledParser::PRIVATE)
      | (1ULL << JavaLabeledParser::PROTECTED)
      | (1ULL << JavaLabeledParser::PUBLIC)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::STATIC)
      | (1ULL << JavaLabeledParser::STRICTFP)
      | (1ULL << JavaLabeledParser::SYNCHRONIZED)
      | (1ULL << JavaLabeledParser::TRANSIENT)
      | (1ULL << JavaLabeledParser::VOID)
      | (1ULL << JavaLabeledParser::VOLATILE)
      | (1ULL << JavaLabeledParser::LBRACE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaLabeledParser::SEMI - 67))
      | (1ULL << (JavaLabeledParser::LT - 67))
      | (1ULL << (JavaLabeledParser::AT - 67))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 67)))) != 0)) {
      setState(375);
      classBodyDeclaration();
      setState(380);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InterfaceDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::InterfaceDeclarationContext::InterfaceDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::InterfaceDeclarationContext::INTERFACE() {
  return getToken(JavaLabeledParser::INTERFACE, 0);
}

tree::TerminalNode* JavaLabeledParser::InterfaceDeclarationContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::InterfaceBodyContext* JavaLabeledParser::InterfaceDeclarationContext::interfaceBody() {
  return getRuleContext<JavaLabeledParser::InterfaceBodyContext>(0);
}

JavaLabeledParser::TypeParametersContext* JavaLabeledParser::InterfaceDeclarationContext::typeParameters() {
  return getRuleContext<JavaLabeledParser::TypeParametersContext>(0);
}

tree::TerminalNode* JavaLabeledParser::InterfaceDeclarationContext::EXTENDS() {
  return getToken(JavaLabeledParser::EXTENDS, 0);
}

JavaLabeledParser::TypeListContext* JavaLabeledParser::InterfaceDeclarationContext::typeList() {
  return getRuleContext<JavaLabeledParser::TypeListContext>(0);
}


size_t JavaLabeledParser::InterfaceDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleInterfaceDeclaration;
}

void JavaLabeledParser::InterfaceDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceDeclaration(this);
}

void JavaLabeledParser::InterfaceDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::InterfaceDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::InterfaceDeclarationContext* JavaLabeledParser::interfaceDeclaration() {
  InterfaceDeclarationContext *_localctx = _tracker.createInstance<InterfaceDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 30, JavaLabeledParser::RuleInterfaceDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(381);
    match(JavaLabeledParser::INTERFACE);
    setState(382);
    match(JavaLabeledParser::IDENTIFIER);
    setState(384);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::LT) {
      setState(383);
      typeParameters();
    }
    setState(388);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::EXTENDS) {
      setState(386);
      match(JavaLabeledParser::EXTENDS);
      setState(387);
      typeList();
    }
    setState(390);
    interfaceBody();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassBodyContext ------------------------------------------------------------------

JavaLabeledParser::ClassBodyContext::ClassBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ClassBodyContext::LBRACE() {
  return getToken(JavaLabeledParser::LBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::ClassBodyContext::RBRACE() {
  return getToken(JavaLabeledParser::RBRACE, 0);
}

std::vector<JavaLabeledParser::ClassBodyDeclarationContext *> JavaLabeledParser::ClassBodyContext::classBodyDeclaration() {
  return getRuleContexts<JavaLabeledParser::ClassBodyDeclarationContext>();
}

JavaLabeledParser::ClassBodyDeclarationContext* JavaLabeledParser::ClassBodyContext::classBodyDeclaration(size_t i) {
  return getRuleContext<JavaLabeledParser::ClassBodyDeclarationContext>(i);
}


size_t JavaLabeledParser::ClassBodyContext::getRuleIndex() const {
  return JavaLabeledParser::RuleClassBody;
}

void JavaLabeledParser::ClassBodyContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassBody(this);
}

void JavaLabeledParser::ClassBodyContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassBody(this);
}


antlrcpp::Any JavaLabeledParser::ClassBodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassBody(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ClassBodyContext* JavaLabeledParser::classBody() {
  ClassBodyContext *_localctx = _tracker.createInstance<ClassBodyContext>(_ctx, getState());
  enterRule(_localctx, 32, JavaLabeledParser::RuleClassBody);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(392);
    match(JavaLabeledParser::LBRACE);
    setState(396);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::ABSTRACT)
      | (1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::CLASS)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::ENUM)
      | (1ULL << JavaLabeledParser::FINAL)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::INTERFACE)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NATIVE)
      | (1ULL << JavaLabeledParser::PRIVATE)
      | (1ULL << JavaLabeledParser::PROTECTED)
      | (1ULL << JavaLabeledParser::PUBLIC)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::STATIC)
      | (1ULL << JavaLabeledParser::STRICTFP)
      | (1ULL << JavaLabeledParser::SYNCHRONIZED)
      | (1ULL << JavaLabeledParser::TRANSIENT)
      | (1ULL << JavaLabeledParser::VOID)
      | (1ULL << JavaLabeledParser::VOLATILE)
      | (1ULL << JavaLabeledParser::LBRACE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaLabeledParser::SEMI - 67))
      | (1ULL << (JavaLabeledParser::LT - 67))
      | (1ULL << (JavaLabeledParser::AT - 67))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 67)))) != 0)) {
      setState(393);
      classBodyDeclaration();
      setState(398);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(399);
    match(JavaLabeledParser::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InterfaceBodyContext ------------------------------------------------------------------

JavaLabeledParser::InterfaceBodyContext::InterfaceBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::InterfaceBodyContext::LBRACE() {
  return getToken(JavaLabeledParser::LBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::InterfaceBodyContext::RBRACE() {
  return getToken(JavaLabeledParser::RBRACE, 0);
}

std::vector<JavaLabeledParser::InterfaceBodyDeclarationContext *> JavaLabeledParser::InterfaceBodyContext::interfaceBodyDeclaration() {
  return getRuleContexts<JavaLabeledParser::InterfaceBodyDeclarationContext>();
}

JavaLabeledParser::InterfaceBodyDeclarationContext* JavaLabeledParser::InterfaceBodyContext::interfaceBodyDeclaration(size_t i) {
  return getRuleContext<JavaLabeledParser::InterfaceBodyDeclarationContext>(i);
}


size_t JavaLabeledParser::InterfaceBodyContext::getRuleIndex() const {
  return JavaLabeledParser::RuleInterfaceBody;
}

void JavaLabeledParser::InterfaceBodyContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceBody(this);
}

void JavaLabeledParser::InterfaceBodyContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceBody(this);
}


antlrcpp::Any JavaLabeledParser::InterfaceBodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceBody(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::InterfaceBodyContext* JavaLabeledParser::interfaceBody() {
  InterfaceBodyContext *_localctx = _tracker.createInstance<InterfaceBodyContext>(_ctx, getState());
  enterRule(_localctx, 34, JavaLabeledParser::RuleInterfaceBody);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(401);
    match(JavaLabeledParser::LBRACE);
    setState(405);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::ABSTRACT)
      | (1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::CLASS)
      | (1ULL << JavaLabeledParser::DEFAULT)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::ENUM)
      | (1ULL << JavaLabeledParser::FINAL)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::INTERFACE)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NATIVE)
      | (1ULL << JavaLabeledParser::PRIVATE)
      | (1ULL << JavaLabeledParser::PROTECTED)
      | (1ULL << JavaLabeledParser::PUBLIC)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::STATIC)
      | (1ULL << JavaLabeledParser::STRICTFP)
      | (1ULL << JavaLabeledParser::SYNCHRONIZED)
      | (1ULL << JavaLabeledParser::TRANSIENT)
      | (1ULL << JavaLabeledParser::VOID)
      | (1ULL << JavaLabeledParser::VOLATILE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaLabeledParser::SEMI - 67))
      | (1ULL << (JavaLabeledParser::LT - 67))
      | (1ULL << (JavaLabeledParser::AT - 67))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 67)))) != 0)) {
      setState(402);
      interfaceBodyDeclaration();
      setState(407);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(408);
    match(JavaLabeledParser::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassBodyDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::ClassBodyDeclarationContext::ClassBodyDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::ClassBodyDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleClassBodyDeclaration;
}

void JavaLabeledParser::ClassBodyDeclarationContext::copyFrom(ClassBodyDeclarationContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ClassBodyDeclaration1Context ------------------------------------------------------------------

JavaLabeledParser::BlockContext* JavaLabeledParser::ClassBodyDeclaration1Context::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ClassBodyDeclaration1Context::STATIC() {
  return getToken(JavaLabeledParser::STATIC, 0);
}

JavaLabeledParser::ClassBodyDeclaration1Context::ClassBodyDeclaration1Context(ClassBodyDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ClassBodyDeclaration1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassBodyDeclaration1(this);
}
void JavaLabeledParser::ClassBodyDeclaration1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassBodyDeclaration1(this);
}

antlrcpp::Any JavaLabeledParser::ClassBodyDeclaration1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassBodyDeclaration1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ClassBodyDeclaration0Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::ClassBodyDeclaration0Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::ClassBodyDeclaration0Context::ClassBodyDeclaration0Context(ClassBodyDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ClassBodyDeclaration0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassBodyDeclaration0(this);
}
void JavaLabeledParser::ClassBodyDeclaration0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassBodyDeclaration0(this);
}

antlrcpp::Any JavaLabeledParser::ClassBodyDeclaration0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassBodyDeclaration0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ClassBodyDeclaration2Context ------------------------------------------------------------------

JavaLabeledParser::MemberDeclarationContext* JavaLabeledParser::ClassBodyDeclaration2Context::memberDeclaration() {
  return getRuleContext<JavaLabeledParser::MemberDeclarationContext>(0);
}

std::vector<JavaLabeledParser::ModifierContext *> JavaLabeledParser::ClassBodyDeclaration2Context::modifier() {
  return getRuleContexts<JavaLabeledParser::ModifierContext>();
}

JavaLabeledParser::ModifierContext* JavaLabeledParser::ClassBodyDeclaration2Context::modifier(size_t i) {
  return getRuleContext<JavaLabeledParser::ModifierContext>(i);
}

JavaLabeledParser::ClassBodyDeclaration2Context::ClassBodyDeclaration2Context(ClassBodyDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ClassBodyDeclaration2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassBodyDeclaration2(this);
}
void JavaLabeledParser::ClassBodyDeclaration2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassBodyDeclaration2(this);
}

antlrcpp::Any JavaLabeledParser::ClassBodyDeclaration2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassBodyDeclaration2(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::ClassBodyDeclarationContext* JavaLabeledParser::classBodyDeclaration() {
  ClassBodyDeclarationContext *_localctx = _tracker.createInstance<ClassBodyDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 36, JavaLabeledParser::RuleClassBodyDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    setState(422);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 35, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ClassBodyDeclaration0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(410);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ClassBodyDeclaration1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(412);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::STATIC) {
        setState(411);
        match(JavaLabeledParser::STATIC);
      }
      setState(414);
      block();
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ClassBodyDeclaration2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(418);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 34, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(415);
          modifier(); 
        }
        setState(420);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 34, _ctx);
      }
      setState(421);
      memberDeclaration();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- MemberDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::MemberDeclarationContext::MemberDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::MemberDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleMemberDeclaration;
}

void JavaLabeledParser::MemberDeclarationContext::copyFrom(MemberDeclarationContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- MemberDeclaration8Context ------------------------------------------------------------------

JavaLabeledParser::EnumDeclarationContext* JavaLabeledParser::MemberDeclaration8Context::enumDeclaration() {
  return getRuleContext<JavaLabeledParser::EnumDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration8Context::MemberDeclaration8Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration8Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration8(this);
}
void JavaLabeledParser::MemberDeclaration8Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration8(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration8Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration8(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration0Context ------------------------------------------------------------------

JavaLabeledParser::MethodDeclarationContext* JavaLabeledParser::MemberDeclaration0Context::methodDeclaration() {
  return getRuleContext<JavaLabeledParser::MethodDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration0Context::MemberDeclaration0Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration0(this);
}
void JavaLabeledParser::MemberDeclaration0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration0(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration1Context ------------------------------------------------------------------

JavaLabeledParser::GenericMethodDeclarationContext* JavaLabeledParser::MemberDeclaration1Context::genericMethodDeclaration() {
  return getRuleContext<JavaLabeledParser::GenericMethodDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration1Context::MemberDeclaration1Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration1(this);
}
void JavaLabeledParser::MemberDeclaration1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration1(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration2Context ------------------------------------------------------------------

JavaLabeledParser::FieldDeclarationContext* JavaLabeledParser::MemberDeclaration2Context::fieldDeclaration() {
  return getRuleContext<JavaLabeledParser::FieldDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration2Context::MemberDeclaration2Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration2(this);
}
void JavaLabeledParser::MemberDeclaration2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration2(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration3Context ------------------------------------------------------------------

JavaLabeledParser::ConstructorDeclarationContext* JavaLabeledParser::MemberDeclaration3Context::constructorDeclaration() {
  return getRuleContext<JavaLabeledParser::ConstructorDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration3Context::MemberDeclaration3Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration3(this);
}
void JavaLabeledParser::MemberDeclaration3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration3(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration4Context ------------------------------------------------------------------

JavaLabeledParser::GenericConstructorDeclarationContext* JavaLabeledParser::MemberDeclaration4Context::genericConstructorDeclaration() {
  return getRuleContext<JavaLabeledParser::GenericConstructorDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration4Context::MemberDeclaration4Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration4(this);
}
void JavaLabeledParser::MemberDeclaration4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration4(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration5Context ------------------------------------------------------------------

JavaLabeledParser::InterfaceDeclarationContext* JavaLabeledParser::MemberDeclaration5Context::interfaceDeclaration() {
  return getRuleContext<JavaLabeledParser::InterfaceDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration5Context::MemberDeclaration5Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration5(this);
}
void JavaLabeledParser::MemberDeclaration5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration5(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration6Context ------------------------------------------------------------------

JavaLabeledParser::AnnotationTypeDeclarationContext* JavaLabeledParser::MemberDeclaration6Context::annotationTypeDeclaration() {
  return getRuleContext<JavaLabeledParser::AnnotationTypeDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration6Context::MemberDeclaration6Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration6(this);
}
void JavaLabeledParser::MemberDeclaration6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration6(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration7Context ------------------------------------------------------------------

JavaLabeledParser::ClassDeclarationContext* JavaLabeledParser::MemberDeclaration7Context::classDeclaration() {
  return getRuleContext<JavaLabeledParser::ClassDeclarationContext>(0);
}

JavaLabeledParser::MemberDeclaration7Context::MemberDeclaration7Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MemberDeclaration7Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration7(this);
}
void JavaLabeledParser::MemberDeclaration7Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration7(this);
}

antlrcpp::Any JavaLabeledParser::MemberDeclaration7Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration7(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::MemberDeclarationContext* JavaLabeledParser::memberDeclaration() {
  MemberDeclarationContext *_localctx = _tracker.createInstance<MemberDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 38, JavaLabeledParser::RuleMemberDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(433);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 36, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(424);
      methodDeclaration();
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(425);
      genericMethodDeclaration();
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(426);
      fieldDeclaration();
      break;
    }

    case 4: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration3Context>(_localctx);
      enterOuterAlt(_localctx, 4);
      setState(427);
      constructorDeclaration();
      break;
    }

    case 5: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration4Context>(_localctx);
      enterOuterAlt(_localctx, 5);
      setState(428);
      genericConstructorDeclaration();
      break;
    }

    case 6: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration5Context>(_localctx);
      enterOuterAlt(_localctx, 6);
      setState(429);
      interfaceDeclaration();
      break;
    }

    case 7: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration6Context>(_localctx);
      enterOuterAlt(_localctx, 7);
      setState(430);
      annotationTypeDeclaration();
      break;
    }

    case 8: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration7Context>(_localctx);
      enterOuterAlt(_localctx, 8);
      setState(431);
      classDeclaration();
      break;
    }

    case 9: {
      _localctx = _tracker.createInstance<JavaLabeledParser::MemberDeclaration8Context>(_localctx);
      enterOuterAlt(_localctx, 9);
      setState(432);
      enumDeclaration();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- MethodDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::MethodDeclarationContext::MethodDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeTypeOrVoidContext* JavaLabeledParser::MethodDeclarationContext::typeTypeOrVoid() {
  return getRuleContext<JavaLabeledParser::TypeTypeOrVoidContext>(0);
}

tree::TerminalNode* JavaLabeledParser::MethodDeclarationContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::FormalParametersContext* JavaLabeledParser::MethodDeclarationContext::formalParameters() {
  return getRuleContext<JavaLabeledParser::FormalParametersContext>(0);
}

JavaLabeledParser::MethodBodyContext* JavaLabeledParser::MethodDeclarationContext::methodBody() {
  return getRuleContext<JavaLabeledParser::MethodBodyContext>(0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::MethodDeclarationContext::LBRACK() {
  return getTokens(JavaLabeledParser::LBRACK);
}

tree::TerminalNode* JavaLabeledParser::MethodDeclarationContext::LBRACK(size_t i) {
  return getToken(JavaLabeledParser::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::MethodDeclarationContext::RBRACK() {
  return getTokens(JavaLabeledParser::RBRACK);
}

tree::TerminalNode* JavaLabeledParser::MethodDeclarationContext::RBRACK(size_t i) {
  return getToken(JavaLabeledParser::RBRACK, i);
}

tree::TerminalNode* JavaLabeledParser::MethodDeclarationContext::THROWS() {
  return getToken(JavaLabeledParser::THROWS, 0);
}

JavaLabeledParser::QualifiedNameListContext* JavaLabeledParser::MethodDeclarationContext::qualifiedNameList() {
  return getRuleContext<JavaLabeledParser::QualifiedNameListContext>(0);
}


size_t JavaLabeledParser::MethodDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleMethodDeclaration;
}

void JavaLabeledParser::MethodDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodDeclaration(this);
}

void JavaLabeledParser::MethodDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::MethodDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMethodDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::MethodDeclarationContext* JavaLabeledParser::methodDeclaration() {
  MethodDeclarationContext *_localctx = _tracker.createInstance<MethodDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 40, JavaLabeledParser::RuleMethodDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(435);
    typeTypeOrVoid();
    setState(436);
    match(JavaLabeledParser::IDENTIFIER);
    setState(437);
    formalParameters();
    setState(442);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::LBRACK) {
      setState(438);
      match(JavaLabeledParser::LBRACK);
      setState(439);
      match(JavaLabeledParser::RBRACK);
      setState(444);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(447);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::THROWS) {
      setState(445);
      match(JavaLabeledParser::THROWS);
      setState(446);
      qualifiedNameList();
    }
    setState(449);
    methodBody();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- MethodBodyContext ------------------------------------------------------------------

JavaLabeledParser::MethodBodyContext::MethodBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::BlockContext* JavaLabeledParser::MethodBodyContext::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

tree::TerminalNode* JavaLabeledParser::MethodBodyContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}


size_t JavaLabeledParser::MethodBodyContext::getRuleIndex() const {
  return JavaLabeledParser::RuleMethodBody;
}

void JavaLabeledParser::MethodBodyContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodBody(this);
}

void JavaLabeledParser::MethodBodyContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodBody(this);
}


antlrcpp::Any JavaLabeledParser::MethodBodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMethodBody(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::MethodBodyContext* JavaLabeledParser::methodBody() {
  MethodBodyContext *_localctx = _tracker.createInstance<MethodBodyContext>(_ctx, getState());
  enterRule(_localctx, 42, JavaLabeledParser::RuleMethodBody);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(453);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::LBRACE: {
        enterOuterAlt(_localctx, 1);
        setState(451);
        block();
        break;
      }

      case JavaLabeledParser::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(452);
        match(JavaLabeledParser::SEMI);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeTypeOrVoidContext ------------------------------------------------------------------

JavaLabeledParser::TypeTypeOrVoidContext::TypeTypeOrVoidContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::TypeTypeOrVoidContext::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::TypeTypeOrVoidContext::VOID() {
  return getToken(JavaLabeledParser::VOID, 0);
}


size_t JavaLabeledParser::TypeTypeOrVoidContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeTypeOrVoid;
}

void JavaLabeledParser::TypeTypeOrVoidContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeTypeOrVoid(this);
}

void JavaLabeledParser::TypeTypeOrVoidContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeTypeOrVoid(this);
}


antlrcpp::Any JavaLabeledParser::TypeTypeOrVoidContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeTypeOrVoid(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeTypeOrVoidContext* JavaLabeledParser::typeTypeOrVoid() {
  TypeTypeOrVoidContext *_localctx = _tracker.createInstance<TypeTypeOrVoidContext>(_ctx, getState());
  enterRule(_localctx, 44, JavaLabeledParser::RuleTypeTypeOrVoid);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(457);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::SHORT:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(455);
        typeType();
        break;
      }

      case JavaLabeledParser::VOID: {
        enterOuterAlt(_localctx, 2);
        setState(456);
        match(JavaLabeledParser::VOID);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- GenericMethodDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::GenericMethodDeclarationContext::GenericMethodDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeParametersContext* JavaLabeledParser::GenericMethodDeclarationContext::typeParameters() {
  return getRuleContext<JavaLabeledParser::TypeParametersContext>(0);
}

JavaLabeledParser::MethodDeclarationContext* JavaLabeledParser::GenericMethodDeclarationContext::methodDeclaration() {
  return getRuleContext<JavaLabeledParser::MethodDeclarationContext>(0);
}


size_t JavaLabeledParser::GenericMethodDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleGenericMethodDeclaration;
}

void JavaLabeledParser::GenericMethodDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterGenericMethodDeclaration(this);
}

void JavaLabeledParser::GenericMethodDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitGenericMethodDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::GenericMethodDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitGenericMethodDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::GenericMethodDeclarationContext* JavaLabeledParser::genericMethodDeclaration() {
  GenericMethodDeclarationContext *_localctx = _tracker.createInstance<GenericMethodDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 46, JavaLabeledParser::RuleGenericMethodDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(459);
    typeParameters();
    setState(460);
    methodDeclaration();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- GenericConstructorDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::GenericConstructorDeclarationContext::GenericConstructorDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeParametersContext* JavaLabeledParser::GenericConstructorDeclarationContext::typeParameters() {
  return getRuleContext<JavaLabeledParser::TypeParametersContext>(0);
}

JavaLabeledParser::ConstructorDeclarationContext* JavaLabeledParser::GenericConstructorDeclarationContext::constructorDeclaration() {
  return getRuleContext<JavaLabeledParser::ConstructorDeclarationContext>(0);
}


size_t JavaLabeledParser::GenericConstructorDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleGenericConstructorDeclaration;
}

void JavaLabeledParser::GenericConstructorDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterGenericConstructorDeclaration(this);
}

void JavaLabeledParser::GenericConstructorDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitGenericConstructorDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::GenericConstructorDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitGenericConstructorDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::GenericConstructorDeclarationContext* JavaLabeledParser::genericConstructorDeclaration() {
  GenericConstructorDeclarationContext *_localctx = _tracker.createInstance<GenericConstructorDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 48, JavaLabeledParser::RuleGenericConstructorDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(462);
    typeParameters();
    setState(463);
    constructorDeclaration();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ConstructorDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::ConstructorDeclarationContext::ConstructorDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ConstructorDeclarationContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::FormalParametersContext* JavaLabeledParser::ConstructorDeclarationContext::formalParameters() {
  return getRuleContext<JavaLabeledParser::FormalParametersContext>(0);
}

JavaLabeledParser::BlockContext* JavaLabeledParser::ConstructorDeclarationContext::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ConstructorDeclarationContext::THROWS() {
  return getToken(JavaLabeledParser::THROWS, 0);
}

JavaLabeledParser::QualifiedNameListContext* JavaLabeledParser::ConstructorDeclarationContext::qualifiedNameList() {
  return getRuleContext<JavaLabeledParser::QualifiedNameListContext>(0);
}


size_t JavaLabeledParser::ConstructorDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleConstructorDeclaration;
}

void JavaLabeledParser::ConstructorDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterConstructorDeclaration(this);
}

void JavaLabeledParser::ConstructorDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitConstructorDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::ConstructorDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitConstructorDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ConstructorDeclarationContext* JavaLabeledParser::constructorDeclaration() {
  ConstructorDeclarationContext *_localctx = _tracker.createInstance<ConstructorDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 50, JavaLabeledParser::RuleConstructorDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(465);
    match(JavaLabeledParser::IDENTIFIER);
    setState(466);
    formalParameters();
    setState(469);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::THROWS) {
      setState(467);
      match(JavaLabeledParser::THROWS);
      setState(468);
      qualifiedNameList();
    }
    setState(471);
    antlrcpp::downCast<ConstructorDeclarationContext *>(_localctx)->constructorBody = block();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FieldDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::FieldDeclarationContext::FieldDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::FieldDeclarationContext::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

JavaLabeledParser::VariableDeclaratorsContext* JavaLabeledParser::FieldDeclarationContext::variableDeclarators() {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorsContext>(0);
}

tree::TerminalNode* JavaLabeledParser::FieldDeclarationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}


size_t JavaLabeledParser::FieldDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleFieldDeclaration;
}

void JavaLabeledParser::FieldDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFieldDeclaration(this);
}

void JavaLabeledParser::FieldDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFieldDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::FieldDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitFieldDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::FieldDeclarationContext* JavaLabeledParser::fieldDeclaration() {
  FieldDeclarationContext *_localctx = _tracker.createInstance<FieldDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 52, JavaLabeledParser::RuleFieldDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(473);
    typeType();
    setState(474);
    variableDeclarators();
    setState(475);
    match(JavaLabeledParser::SEMI);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InterfaceBodyDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::InterfaceBodyDeclarationContext::InterfaceBodyDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::InterfaceMemberDeclarationContext* JavaLabeledParser::InterfaceBodyDeclarationContext::interfaceMemberDeclaration() {
  return getRuleContext<JavaLabeledParser::InterfaceMemberDeclarationContext>(0);
}

std::vector<JavaLabeledParser::ModifierContext *> JavaLabeledParser::InterfaceBodyDeclarationContext::modifier() {
  return getRuleContexts<JavaLabeledParser::ModifierContext>();
}

JavaLabeledParser::ModifierContext* JavaLabeledParser::InterfaceBodyDeclarationContext::modifier(size_t i) {
  return getRuleContext<JavaLabeledParser::ModifierContext>(i);
}

tree::TerminalNode* JavaLabeledParser::InterfaceBodyDeclarationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}


size_t JavaLabeledParser::InterfaceBodyDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleInterfaceBodyDeclaration;
}

void JavaLabeledParser::InterfaceBodyDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceBodyDeclaration(this);
}

void JavaLabeledParser::InterfaceBodyDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceBodyDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::InterfaceBodyDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceBodyDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::InterfaceBodyDeclarationContext* JavaLabeledParser::interfaceBodyDeclaration() {
  InterfaceBodyDeclarationContext *_localctx = _tracker.createInstance<InterfaceBodyDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 54, JavaLabeledParser::RuleInterfaceBodyDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    setState(485);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::ABSTRACT:
      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::CLASS:
      case JavaLabeledParser::DEFAULT:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::ENUM:
      case JavaLabeledParser::FINAL:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::INTERFACE:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::NATIVE:
      case JavaLabeledParser::PRIVATE:
      case JavaLabeledParser::PROTECTED:
      case JavaLabeledParser::PUBLIC:
      case JavaLabeledParser::SHORT:
      case JavaLabeledParser::STATIC:
      case JavaLabeledParser::STRICTFP:
      case JavaLabeledParser::SYNCHRONIZED:
      case JavaLabeledParser::TRANSIENT:
      case JavaLabeledParser::VOID:
      case JavaLabeledParser::VOLATILE:
      case JavaLabeledParser::LT:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(480);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 42, _ctx);
        while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
          if (alt == 1) {
            setState(477);
            modifier(); 
          }
          setState(482);
          _errHandler->sync(this);
          alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 42, _ctx);
        }
        setState(483);
        interfaceMemberDeclaration();
        break;
      }

      case JavaLabeledParser::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(484);
        match(JavaLabeledParser::SEMI);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InterfaceMemberDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::InterfaceMemberDeclarationContext::InterfaceMemberDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::InterfaceMemberDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleInterfaceMemberDeclaration;
}

void JavaLabeledParser::InterfaceMemberDeclarationContext::copyFrom(InterfaceMemberDeclarationContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- InterfaceMemberDeclaration6Context ------------------------------------------------------------------

JavaLabeledParser::EnumDeclarationContext* JavaLabeledParser::InterfaceMemberDeclaration6Context::enumDeclaration() {
  return getRuleContext<JavaLabeledParser::EnumDeclarationContext>(0);
}

JavaLabeledParser::InterfaceMemberDeclaration6Context::InterfaceMemberDeclaration6Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::InterfaceMemberDeclaration6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration6(this);
}
void JavaLabeledParser::InterfaceMemberDeclaration6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration6(this);
}

antlrcpp::Any JavaLabeledParser::InterfaceMemberDeclaration6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration5Context ------------------------------------------------------------------

JavaLabeledParser::ClassDeclarationContext* JavaLabeledParser::InterfaceMemberDeclaration5Context::classDeclaration() {
  return getRuleContext<JavaLabeledParser::ClassDeclarationContext>(0);
}

JavaLabeledParser::InterfaceMemberDeclaration5Context::InterfaceMemberDeclaration5Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::InterfaceMemberDeclaration5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration5(this);
}
void JavaLabeledParser::InterfaceMemberDeclaration5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration5(this);
}

antlrcpp::Any JavaLabeledParser::InterfaceMemberDeclaration5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration4Context ------------------------------------------------------------------

JavaLabeledParser::AnnotationTypeDeclarationContext* JavaLabeledParser::InterfaceMemberDeclaration4Context::annotationTypeDeclaration() {
  return getRuleContext<JavaLabeledParser::AnnotationTypeDeclarationContext>(0);
}

JavaLabeledParser::InterfaceMemberDeclaration4Context::InterfaceMemberDeclaration4Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::InterfaceMemberDeclaration4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration4(this);
}
void JavaLabeledParser::InterfaceMemberDeclaration4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration4(this);
}

antlrcpp::Any JavaLabeledParser::InterfaceMemberDeclaration4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration3Context ------------------------------------------------------------------

JavaLabeledParser::InterfaceDeclarationContext* JavaLabeledParser::InterfaceMemberDeclaration3Context::interfaceDeclaration() {
  return getRuleContext<JavaLabeledParser::InterfaceDeclarationContext>(0);
}

JavaLabeledParser::InterfaceMemberDeclaration3Context::InterfaceMemberDeclaration3Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::InterfaceMemberDeclaration3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration3(this);
}
void JavaLabeledParser::InterfaceMemberDeclaration3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration3(this);
}

antlrcpp::Any JavaLabeledParser::InterfaceMemberDeclaration3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration2Context ------------------------------------------------------------------

JavaLabeledParser::GenericInterfaceMethodDeclarationContext* JavaLabeledParser::InterfaceMemberDeclaration2Context::genericInterfaceMethodDeclaration() {
  return getRuleContext<JavaLabeledParser::GenericInterfaceMethodDeclarationContext>(0);
}

JavaLabeledParser::InterfaceMemberDeclaration2Context::InterfaceMemberDeclaration2Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::InterfaceMemberDeclaration2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration2(this);
}
void JavaLabeledParser::InterfaceMemberDeclaration2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration2(this);
}

antlrcpp::Any JavaLabeledParser::InterfaceMemberDeclaration2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration1Context ------------------------------------------------------------------

JavaLabeledParser::InterfaceMethodDeclarationContext* JavaLabeledParser::InterfaceMemberDeclaration1Context::interfaceMethodDeclaration() {
  return getRuleContext<JavaLabeledParser::InterfaceMethodDeclarationContext>(0);
}

JavaLabeledParser::InterfaceMemberDeclaration1Context::InterfaceMemberDeclaration1Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::InterfaceMemberDeclaration1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration1(this);
}
void JavaLabeledParser::InterfaceMemberDeclaration1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration1(this);
}

antlrcpp::Any JavaLabeledParser::InterfaceMemberDeclaration1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration0Context ------------------------------------------------------------------

JavaLabeledParser::ConstDeclarationContext* JavaLabeledParser::InterfaceMemberDeclaration0Context::constDeclaration() {
  return getRuleContext<JavaLabeledParser::ConstDeclarationContext>(0);
}

JavaLabeledParser::InterfaceMemberDeclaration0Context::InterfaceMemberDeclaration0Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::InterfaceMemberDeclaration0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration0(this);
}
void JavaLabeledParser::InterfaceMemberDeclaration0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration0(this);
}

antlrcpp::Any JavaLabeledParser::InterfaceMemberDeclaration0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration0(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::InterfaceMemberDeclarationContext* JavaLabeledParser::interfaceMemberDeclaration() {
  InterfaceMemberDeclarationContext *_localctx = _tracker.createInstance<InterfaceMemberDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 56, JavaLabeledParser::RuleInterfaceMemberDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(494);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 44, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::InterfaceMemberDeclaration0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(487);
      constDeclaration();
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::InterfaceMemberDeclaration1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(488);
      interfaceMethodDeclaration();
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::InterfaceMemberDeclaration2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(489);
      genericInterfaceMethodDeclaration();
      break;
    }

    case 4: {
      _localctx = _tracker.createInstance<JavaLabeledParser::InterfaceMemberDeclaration3Context>(_localctx);
      enterOuterAlt(_localctx, 4);
      setState(490);
      interfaceDeclaration();
      break;
    }

    case 5: {
      _localctx = _tracker.createInstance<JavaLabeledParser::InterfaceMemberDeclaration4Context>(_localctx);
      enterOuterAlt(_localctx, 5);
      setState(491);
      annotationTypeDeclaration();
      break;
    }

    case 6: {
      _localctx = _tracker.createInstance<JavaLabeledParser::InterfaceMemberDeclaration5Context>(_localctx);
      enterOuterAlt(_localctx, 6);
      setState(492);
      classDeclaration();
      break;
    }

    case 7: {
      _localctx = _tracker.createInstance<JavaLabeledParser::InterfaceMemberDeclaration6Context>(_localctx);
      enterOuterAlt(_localctx, 7);
      setState(493);
      enumDeclaration();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ConstDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::ConstDeclarationContext::ConstDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::ConstDeclarationContext::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

std::vector<JavaLabeledParser::ConstantDeclaratorContext *> JavaLabeledParser::ConstDeclarationContext::constantDeclarator() {
  return getRuleContexts<JavaLabeledParser::ConstantDeclaratorContext>();
}

JavaLabeledParser::ConstantDeclaratorContext* JavaLabeledParser::ConstDeclarationContext::constantDeclarator(size_t i) {
  return getRuleContext<JavaLabeledParser::ConstantDeclaratorContext>(i);
}

tree::TerminalNode* JavaLabeledParser::ConstDeclarationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ConstDeclarationContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::ConstDeclarationContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::ConstDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleConstDeclaration;
}

void JavaLabeledParser::ConstDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterConstDeclaration(this);
}

void JavaLabeledParser::ConstDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitConstDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::ConstDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitConstDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ConstDeclarationContext* JavaLabeledParser::constDeclaration() {
  ConstDeclarationContext *_localctx = _tracker.createInstance<ConstDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 58, JavaLabeledParser::RuleConstDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(496);
    typeType();
    setState(497);
    constantDeclarator();
    setState(502);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::COMMA) {
      setState(498);
      match(JavaLabeledParser::COMMA);
      setState(499);
      constantDeclarator();
      setState(504);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(505);
    match(JavaLabeledParser::SEMI);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ConstantDeclaratorContext ------------------------------------------------------------------

JavaLabeledParser::ConstantDeclaratorContext::ConstantDeclaratorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ConstantDeclaratorContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

tree::TerminalNode* JavaLabeledParser::ConstantDeclaratorContext::ASSIGN() {
  return getToken(JavaLabeledParser::ASSIGN, 0);
}

JavaLabeledParser::VariableInitializerContext* JavaLabeledParser::ConstantDeclaratorContext::variableInitializer() {
  return getRuleContext<JavaLabeledParser::VariableInitializerContext>(0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ConstantDeclaratorContext::LBRACK() {
  return getTokens(JavaLabeledParser::LBRACK);
}

tree::TerminalNode* JavaLabeledParser::ConstantDeclaratorContext::LBRACK(size_t i) {
  return getToken(JavaLabeledParser::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ConstantDeclaratorContext::RBRACK() {
  return getTokens(JavaLabeledParser::RBRACK);
}

tree::TerminalNode* JavaLabeledParser::ConstantDeclaratorContext::RBRACK(size_t i) {
  return getToken(JavaLabeledParser::RBRACK, i);
}


size_t JavaLabeledParser::ConstantDeclaratorContext::getRuleIndex() const {
  return JavaLabeledParser::RuleConstantDeclarator;
}

void JavaLabeledParser::ConstantDeclaratorContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterConstantDeclarator(this);
}

void JavaLabeledParser::ConstantDeclaratorContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitConstantDeclarator(this);
}


antlrcpp::Any JavaLabeledParser::ConstantDeclaratorContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitConstantDeclarator(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ConstantDeclaratorContext* JavaLabeledParser::constantDeclarator() {
  ConstantDeclaratorContext *_localctx = _tracker.createInstance<ConstantDeclaratorContext>(_ctx, getState());
  enterRule(_localctx, 60, JavaLabeledParser::RuleConstantDeclarator);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(507);
    match(JavaLabeledParser::IDENTIFIER);
    setState(512);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::LBRACK) {
      setState(508);
      match(JavaLabeledParser::LBRACK);
      setState(509);
      match(JavaLabeledParser::RBRACK);
      setState(514);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(515);
    match(JavaLabeledParser::ASSIGN);
    setState(516);
    variableInitializer();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InterfaceMethodDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::InterfaceMethodDeclarationContext::InterfaceMethodDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodDeclarationContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::FormalParametersContext* JavaLabeledParser::InterfaceMethodDeclarationContext::formalParameters() {
  return getRuleContext<JavaLabeledParser::FormalParametersContext>(0);
}

JavaLabeledParser::MethodBodyContext* JavaLabeledParser::InterfaceMethodDeclarationContext::methodBody() {
  return getRuleContext<JavaLabeledParser::MethodBodyContext>(0);
}

JavaLabeledParser::TypeTypeOrVoidContext* JavaLabeledParser::InterfaceMethodDeclarationContext::typeTypeOrVoid() {
  return getRuleContext<JavaLabeledParser::TypeTypeOrVoidContext>(0);
}

JavaLabeledParser::TypeParametersContext* JavaLabeledParser::InterfaceMethodDeclarationContext::typeParameters() {
  return getRuleContext<JavaLabeledParser::TypeParametersContext>(0);
}

std::vector<JavaLabeledParser::InterfaceMethodModifierContext *> JavaLabeledParser::InterfaceMethodDeclarationContext::interfaceMethodModifier() {
  return getRuleContexts<JavaLabeledParser::InterfaceMethodModifierContext>();
}

JavaLabeledParser::InterfaceMethodModifierContext* JavaLabeledParser::InterfaceMethodDeclarationContext::interfaceMethodModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::InterfaceMethodModifierContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::InterfaceMethodDeclarationContext::LBRACK() {
  return getTokens(JavaLabeledParser::LBRACK);
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodDeclarationContext::LBRACK(size_t i) {
  return getToken(JavaLabeledParser::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::InterfaceMethodDeclarationContext::RBRACK() {
  return getTokens(JavaLabeledParser::RBRACK);
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodDeclarationContext::RBRACK(size_t i) {
  return getToken(JavaLabeledParser::RBRACK, i);
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodDeclarationContext::THROWS() {
  return getToken(JavaLabeledParser::THROWS, 0);
}

JavaLabeledParser::QualifiedNameListContext* JavaLabeledParser::InterfaceMethodDeclarationContext::qualifiedNameList() {
  return getRuleContext<JavaLabeledParser::QualifiedNameListContext>(0);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::InterfaceMethodDeclarationContext::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::InterfaceMethodDeclarationContext::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}


size_t JavaLabeledParser::InterfaceMethodDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleInterfaceMethodDeclaration;
}

void JavaLabeledParser::InterfaceMethodDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMethodDeclaration(this);
}

void JavaLabeledParser::InterfaceMethodDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMethodDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::InterfaceMethodDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMethodDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::InterfaceMethodDeclarationContext* JavaLabeledParser::interfaceMethodDeclaration() {
  InterfaceMethodDeclarationContext *_localctx = _tracker.createInstance<InterfaceMethodDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 62, JavaLabeledParser::RuleInterfaceMethodDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(521);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 47, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(518);
        interfaceMethodModifier(); 
      }
      setState(523);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 47, _ctx);
    }
    setState(534);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::SHORT:
      case JavaLabeledParser::VOID:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        setState(524);
        typeTypeOrVoid();
        break;
      }

      case JavaLabeledParser::LT: {
        setState(525);
        typeParameters();
        setState(529);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 48, _ctx);
        while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
          if (alt == 1) {
            setState(526);
            annotation(); 
          }
          setState(531);
          _errHandler->sync(this);
          alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 48, _ctx);
        }
        setState(532);
        typeTypeOrVoid();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
    setState(536);
    match(JavaLabeledParser::IDENTIFIER);
    setState(537);
    formalParameters();
    setState(542);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::LBRACK) {
      setState(538);
      match(JavaLabeledParser::LBRACK);
      setState(539);
      match(JavaLabeledParser::RBRACK);
      setState(544);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(547);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::THROWS) {
      setState(545);
      match(JavaLabeledParser::THROWS);
      setState(546);
      qualifiedNameList();
    }
    setState(549);
    methodBody();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InterfaceMethodModifierContext ------------------------------------------------------------------

JavaLabeledParser::InterfaceMethodModifierContext::InterfaceMethodModifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::InterfaceMethodModifierContext::annotation() {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(0);
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodModifierContext::PUBLIC() {
  return getToken(JavaLabeledParser::PUBLIC, 0);
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodModifierContext::ABSTRACT() {
  return getToken(JavaLabeledParser::ABSTRACT, 0);
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodModifierContext::DEFAULT() {
  return getToken(JavaLabeledParser::DEFAULT, 0);
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodModifierContext::STATIC() {
  return getToken(JavaLabeledParser::STATIC, 0);
}

tree::TerminalNode* JavaLabeledParser::InterfaceMethodModifierContext::STRICTFP() {
  return getToken(JavaLabeledParser::STRICTFP, 0);
}


size_t JavaLabeledParser::InterfaceMethodModifierContext::getRuleIndex() const {
  return JavaLabeledParser::RuleInterfaceMethodModifier;
}

void JavaLabeledParser::InterfaceMethodModifierContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMethodModifier(this);
}

void JavaLabeledParser::InterfaceMethodModifierContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMethodModifier(this);
}


antlrcpp::Any JavaLabeledParser::InterfaceMethodModifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInterfaceMethodModifier(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::InterfaceMethodModifierContext* JavaLabeledParser::interfaceMethodModifier() {
  InterfaceMethodModifierContext *_localctx = _tracker.createInstance<InterfaceMethodModifierContext>(_ctx, getState());
  enterRule(_localctx, 64, JavaLabeledParser::RuleInterfaceMethodModifier);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(557);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(551);
        annotation();
        break;
      }

      case JavaLabeledParser::PUBLIC: {
        enterOuterAlt(_localctx, 2);
        setState(552);
        match(JavaLabeledParser::PUBLIC);
        break;
      }

      case JavaLabeledParser::ABSTRACT: {
        enterOuterAlt(_localctx, 3);
        setState(553);
        match(JavaLabeledParser::ABSTRACT);
        break;
      }

      case JavaLabeledParser::DEFAULT: {
        enterOuterAlt(_localctx, 4);
        setState(554);
        match(JavaLabeledParser::DEFAULT);
        break;
      }

      case JavaLabeledParser::STATIC: {
        enterOuterAlt(_localctx, 5);
        setState(555);
        match(JavaLabeledParser::STATIC);
        break;
      }

      case JavaLabeledParser::STRICTFP: {
        enterOuterAlt(_localctx, 6);
        setState(556);
        match(JavaLabeledParser::STRICTFP);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- GenericInterfaceMethodDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::GenericInterfaceMethodDeclarationContext::GenericInterfaceMethodDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeParametersContext* JavaLabeledParser::GenericInterfaceMethodDeclarationContext::typeParameters() {
  return getRuleContext<JavaLabeledParser::TypeParametersContext>(0);
}

JavaLabeledParser::InterfaceMethodDeclarationContext* JavaLabeledParser::GenericInterfaceMethodDeclarationContext::interfaceMethodDeclaration() {
  return getRuleContext<JavaLabeledParser::InterfaceMethodDeclarationContext>(0);
}


size_t JavaLabeledParser::GenericInterfaceMethodDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleGenericInterfaceMethodDeclaration;
}

void JavaLabeledParser::GenericInterfaceMethodDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterGenericInterfaceMethodDeclaration(this);
}

void JavaLabeledParser::GenericInterfaceMethodDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitGenericInterfaceMethodDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::GenericInterfaceMethodDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitGenericInterfaceMethodDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::GenericInterfaceMethodDeclarationContext* JavaLabeledParser::genericInterfaceMethodDeclaration() {
  GenericInterfaceMethodDeclarationContext *_localctx = _tracker.createInstance<GenericInterfaceMethodDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 66, JavaLabeledParser::RuleGenericInterfaceMethodDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(559);
    typeParameters();
    setState(560);
    interfaceMethodDeclaration();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- VariableDeclaratorsContext ------------------------------------------------------------------

JavaLabeledParser::VariableDeclaratorsContext::VariableDeclaratorsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::VariableDeclaratorContext *> JavaLabeledParser::VariableDeclaratorsContext::variableDeclarator() {
  return getRuleContexts<JavaLabeledParser::VariableDeclaratorContext>();
}

JavaLabeledParser::VariableDeclaratorContext* JavaLabeledParser::VariableDeclaratorsContext::variableDeclarator(size_t i) {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::VariableDeclaratorsContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::VariableDeclaratorsContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::VariableDeclaratorsContext::getRuleIndex() const {
  return JavaLabeledParser::RuleVariableDeclarators;
}

void JavaLabeledParser::VariableDeclaratorsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableDeclarators(this);
}

void JavaLabeledParser::VariableDeclaratorsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableDeclarators(this);
}


antlrcpp::Any JavaLabeledParser::VariableDeclaratorsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitVariableDeclarators(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::VariableDeclaratorsContext* JavaLabeledParser::variableDeclarators() {
  VariableDeclaratorsContext *_localctx = _tracker.createInstance<VariableDeclaratorsContext>(_ctx, getState());
  enterRule(_localctx, 68, JavaLabeledParser::RuleVariableDeclarators);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(562);
    variableDeclarator();
    setState(567);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::COMMA) {
      setState(563);
      match(JavaLabeledParser::COMMA);
      setState(564);
      variableDeclarator();
      setState(569);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- VariableDeclaratorContext ------------------------------------------------------------------

JavaLabeledParser::VariableDeclaratorContext::VariableDeclaratorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::VariableDeclaratorIdContext* JavaLabeledParser::VariableDeclaratorContext::variableDeclaratorId() {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorIdContext>(0);
}

tree::TerminalNode* JavaLabeledParser::VariableDeclaratorContext::ASSIGN() {
  return getToken(JavaLabeledParser::ASSIGN, 0);
}

JavaLabeledParser::VariableInitializerContext* JavaLabeledParser::VariableDeclaratorContext::variableInitializer() {
  return getRuleContext<JavaLabeledParser::VariableInitializerContext>(0);
}


size_t JavaLabeledParser::VariableDeclaratorContext::getRuleIndex() const {
  return JavaLabeledParser::RuleVariableDeclarator;
}

void JavaLabeledParser::VariableDeclaratorContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableDeclarator(this);
}

void JavaLabeledParser::VariableDeclaratorContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableDeclarator(this);
}


antlrcpp::Any JavaLabeledParser::VariableDeclaratorContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitVariableDeclarator(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::VariableDeclaratorContext* JavaLabeledParser::variableDeclarator() {
  VariableDeclaratorContext *_localctx = _tracker.createInstance<VariableDeclaratorContext>(_ctx, getState());
  enterRule(_localctx, 70, JavaLabeledParser::RuleVariableDeclarator);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(570);
    variableDeclaratorId();
    setState(573);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::ASSIGN) {
      setState(571);
      match(JavaLabeledParser::ASSIGN);
      setState(572);
      variableInitializer();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- VariableDeclaratorIdContext ------------------------------------------------------------------

JavaLabeledParser::VariableDeclaratorIdContext::VariableDeclaratorIdContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::VariableDeclaratorIdContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::VariableDeclaratorIdContext::LBRACK() {
  return getTokens(JavaLabeledParser::LBRACK);
}

tree::TerminalNode* JavaLabeledParser::VariableDeclaratorIdContext::LBRACK(size_t i) {
  return getToken(JavaLabeledParser::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::VariableDeclaratorIdContext::RBRACK() {
  return getTokens(JavaLabeledParser::RBRACK);
}

tree::TerminalNode* JavaLabeledParser::VariableDeclaratorIdContext::RBRACK(size_t i) {
  return getToken(JavaLabeledParser::RBRACK, i);
}


size_t JavaLabeledParser::VariableDeclaratorIdContext::getRuleIndex() const {
  return JavaLabeledParser::RuleVariableDeclaratorId;
}

void JavaLabeledParser::VariableDeclaratorIdContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableDeclaratorId(this);
}

void JavaLabeledParser::VariableDeclaratorIdContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableDeclaratorId(this);
}


antlrcpp::Any JavaLabeledParser::VariableDeclaratorIdContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitVariableDeclaratorId(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::VariableDeclaratorIdContext* JavaLabeledParser::variableDeclaratorId() {
  VariableDeclaratorIdContext *_localctx = _tracker.createInstance<VariableDeclaratorIdContext>(_ctx, getState());
  enterRule(_localctx, 72, JavaLabeledParser::RuleVariableDeclaratorId);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(575);
    match(JavaLabeledParser::IDENTIFIER);
    setState(580);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::LBRACK) {
      setState(576);
      match(JavaLabeledParser::LBRACK);
      setState(577);
      match(JavaLabeledParser::RBRACK);
      setState(582);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- VariableInitializerContext ------------------------------------------------------------------

JavaLabeledParser::VariableInitializerContext::VariableInitializerContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::VariableInitializerContext::getRuleIndex() const {
  return JavaLabeledParser::RuleVariableInitializer;
}

void JavaLabeledParser::VariableInitializerContext::copyFrom(VariableInitializerContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- VariableInitializer1Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::VariableInitializer1Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

JavaLabeledParser::VariableInitializer1Context::VariableInitializer1Context(VariableInitializerContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::VariableInitializer1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableInitializer1(this);
}
void JavaLabeledParser::VariableInitializer1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableInitializer1(this);
}

antlrcpp::Any JavaLabeledParser::VariableInitializer1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitVariableInitializer1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- VariableInitializer0Context ------------------------------------------------------------------

JavaLabeledParser::ArrayInitializerContext* JavaLabeledParser::VariableInitializer0Context::arrayInitializer() {
  return getRuleContext<JavaLabeledParser::ArrayInitializerContext>(0);
}

JavaLabeledParser::VariableInitializer0Context::VariableInitializer0Context(VariableInitializerContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::VariableInitializer0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableInitializer0(this);
}
void JavaLabeledParser::VariableInitializer0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableInitializer0(this);
}

antlrcpp::Any JavaLabeledParser::VariableInitializer0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitVariableInitializer0(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::VariableInitializerContext* JavaLabeledParser::variableInitializer() {
  VariableInitializerContext *_localctx = _tracker.createInstance<VariableInitializerContext>(_ctx, getState());
  enterRule(_localctx, 74, JavaLabeledParser::RuleVariableInitializer);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(585);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::LBRACE: {
        _localctx = _tracker.createInstance<JavaLabeledParser::VariableInitializer0Context>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(583);
        arrayInitializer();
        break;
      }

      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::NEW:
      case JavaLabeledParser::SHORT:
      case JavaLabeledParser::SUPER:
      case JavaLabeledParser::THIS:
      case JavaLabeledParser::VOID:
      case JavaLabeledParser::DECIMAL_LITERAL:
      case JavaLabeledParser::HEX_LITERAL:
      case JavaLabeledParser::OCT_LITERAL:
      case JavaLabeledParser::BINARY_LITERAL:
      case JavaLabeledParser::FLOAT_LITERAL:
      case JavaLabeledParser::HEX_FLOAT_LITERAL:
      case JavaLabeledParser::BOOL_LITERAL:
      case JavaLabeledParser::CHAR_LITERAL:
      case JavaLabeledParser::STRING_LITERAL:
      case JavaLabeledParser::NULL_LITERAL:
      case JavaLabeledParser::LPAREN:
      case JavaLabeledParser::LT:
      case JavaLabeledParser::BANG:
      case JavaLabeledParser::TILDE:
      case JavaLabeledParser::INC:
      case JavaLabeledParser::DEC:
      case JavaLabeledParser::ADD:
      case JavaLabeledParser::SUB:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        _localctx = _tracker.createInstance<JavaLabeledParser::VariableInitializer1Context>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(584);
        expression(0);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ArrayInitializerContext ------------------------------------------------------------------

JavaLabeledParser::ArrayInitializerContext::ArrayInitializerContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ArrayInitializerContext::LBRACE() {
  return getToken(JavaLabeledParser::LBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::ArrayInitializerContext::RBRACE() {
  return getToken(JavaLabeledParser::RBRACE, 0);
}

std::vector<JavaLabeledParser::VariableInitializerContext *> JavaLabeledParser::ArrayInitializerContext::variableInitializer() {
  return getRuleContexts<JavaLabeledParser::VariableInitializerContext>();
}

JavaLabeledParser::VariableInitializerContext* JavaLabeledParser::ArrayInitializerContext::variableInitializer(size_t i) {
  return getRuleContext<JavaLabeledParser::VariableInitializerContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ArrayInitializerContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::ArrayInitializerContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::ArrayInitializerContext::getRuleIndex() const {
  return JavaLabeledParser::RuleArrayInitializer;
}

void JavaLabeledParser::ArrayInitializerContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterArrayInitializer(this);
}

void JavaLabeledParser::ArrayInitializerContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitArrayInitializer(this);
}


antlrcpp::Any JavaLabeledParser::ArrayInitializerContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitArrayInitializer(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ArrayInitializerContext* JavaLabeledParser::arrayInitializer() {
  ArrayInitializerContext *_localctx = _tracker.createInstance<ArrayInitializerContext>(_ctx, getState());
  enterRule(_localctx, 76, JavaLabeledParser::RuleArrayInitializer);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(587);
    match(JavaLabeledParser::LBRACE);
    setState(599);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NEW)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::SUPER)
      | (1ULL << JavaLabeledParser::THIS)
      | (1ULL << JavaLabeledParser::VOID)
      | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_LITERAL)
      | (1ULL << JavaLabeledParser::OCT_LITERAL)
      | (1ULL << JavaLabeledParser::BINARY_LITERAL)
      | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::BOOL_LITERAL)
      | (1ULL << JavaLabeledParser::CHAR_LITERAL)
      | (1ULL << JavaLabeledParser::STRING_LITERAL)
      | (1ULL << JavaLabeledParser::NULL_LITERAL)
      | (1ULL << JavaLabeledParser::LPAREN)
      | (1ULL << JavaLabeledParser::LBRACE))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
      | (1ULL << (JavaLabeledParser::BANG - 72))
      | (1ULL << (JavaLabeledParser::TILDE - 72))
      | (1ULL << (JavaLabeledParser::INC - 72))
      | (1ULL << (JavaLabeledParser::DEC - 72))
      | (1ULL << (JavaLabeledParser::ADD - 72))
      | (1ULL << (JavaLabeledParser::SUB - 72))
      | (1ULL << (JavaLabeledParser::AT - 72))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
      setState(588);
      variableInitializer();
      setState(593);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 57, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(589);
          match(JavaLabeledParser::COMMA);
          setState(590);
          variableInitializer(); 
        }
        setState(595);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 57, _ctx);
      }
      setState(597);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::COMMA) {
        setState(596);
        match(JavaLabeledParser::COMMA);
      }
    }
    setState(601);
    match(JavaLabeledParser::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassOrInterfaceTypeContext ------------------------------------------------------------------

JavaLabeledParser::ClassOrInterfaceTypeContext::ClassOrInterfaceTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ClassOrInterfaceTypeContext::IDENTIFIER() {
  return getTokens(JavaLabeledParser::IDENTIFIER);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceTypeContext::IDENTIFIER(size_t i) {
  return getToken(JavaLabeledParser::IDENTIFIER, i);
}

std::vector<JavaLabeledParser::TypeArgumentsContext *> JavaLabeledParser::ClassOrInterfaceTypeContext::typeArguments() {
  return getRuleContexts<JavaLabeledParser::TypeArgumentsContext>();
}

JavaLabeledParser::TypeArgumentsContext* JavaLabeledParser::ClassOrInterfaceTypeContext::typeArguments(size_t i) {
  return getRuleContext<JavaLabeledParser::TypeArgumentsContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ClassOrInterfaceTypeContext::DOT() {
  return getTokens(JavaLabeledParser::DOT);
}

tree::TerminalNode* JavaLabeledParser::ClassOrInterfaceTypeContext::DOT(size_t i) {
  return getToken(JavaLabeledParser::DOT, i);
}


size_t JavaLabeledParser::ClassOrInterfaceTypeContext::getRuleIndex() const {
  return JavaLabeledParser::RuleClassOrInterfaceType;
}

void JavaLabeledParser::ClassOrInterfaceTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassOrInterfaceType(this);
}

void JavaLabeledParser::ClassOrInterfaceTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassOrInterfaceType(this);
}


antlrcpp::Any JavaLabeledParser::ClassOrInterfaceTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassOrInterfaceType(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ClassOrInterfaceTypeContext* JavaLabeledParser::classOrInterfaceType() {
  ClassOrInterfaceTypeContext *_localctx = _tracker.createInstance<ClassOrInterfaceTypeContext>(_ctx, getState());
  enterRule(_localctx, 78, JavaLabeledParser::RuleClassOrInterfaceType);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(603);
    match(JavaLabeledParser::IDENTIFIER);
    setState(605);
    _errHandler->sync(this);

    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 60, _ctx)) {
    case 1: {
      setState(604);
      typeArguments();
      break;
    }

    default:
      break;
    }
    setState(614);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 62, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(607);
        match(JavaLabeledParser::DOT);
        setState(608);
        match(JavaLabeledParser::IDENTIFIER);
        setState(610);
        _errHandler->sync(this);

        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 61, _ctx)) {
        case 1: {
          setState(609);
          typeArguments();
          break;
        }

        default:
          break;
        } 
      }
      setState(616);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 62, _ctx);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeArgumentContext ------------------------------------------------------------------

JavaLabeledParser::TypeArgumentContext::TypeArgumentContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::TypeArgumentContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeArgument;
}

void JavaLabeledParser::TypeArgumentContext::copyFrom(TypeArgumentContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- TypeArgument0Context ------------------------------------------------------------------

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::TypeArgument0Context::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::TypeArgument0Context::QUESTION() {
  return getToken(JavaLabeledParser::QUESTION, 0);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::TypeArgument0Context::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::TypeArgument0Context::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}

tree::TerminalNode* JavaLabeledParser::TypeArgument0Context::EXTENDS() {
  return getToken(JavaLabeledParser::EXTENDS, 0);
}

tree::TerminalNode* JavaLabeledParser::TypeArgument0Context::SUPER() {
  return getToken(JavaLabeledParser::SUPER, 0);
}

JavaLabeledParser::TypeArgument0Context::TypeArgument0Context(TypeArgumentContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::TypeArgument0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeArgument0(this);
}
void JavaLabeledParser::TypeArgument0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeArgument0(this);
}

antlrcpp::Any JavaLabeledParser::TypeArgument0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeArgument0(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::TypeArgumentContext* JavaLabeledParser::typeArgument() {
  TypeArgumentContext *_localctx = _tracker.createInstance<TypeArgumentContext>(_ctx, getState());
  enterRule(_localctx, 80, JavaLabeledParser::RuleTypeArgument);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(629);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 65, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::TypeArgument0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(617);
      typeType();
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::TypeArgument0Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(621);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == JavaLabeledParser::AT

      || _la == JavaLabeledParser::IDENTIFIER) {
        setState(618);
        annotation();
        setState(623);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(624);
      match(JavaLabeledParser::QUESTION);
      setState(627);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::EXTENDS

      || _la == JavaLabeledParser::SUPER) {
        setState(625);
        _la = _input->LA(1);
        if (!(_la == JavaLabeledParser::EXTENDS

        || _la == JavaLabeledParser::SUPER)) {
        _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        setState(626);
        typeType();
      }
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- QualifiedNameListContext ------------------------------------------------------------------

JavaLabeledParser::QualifiedNameListContext::QualifiedNameListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::QualifiedNameContext *> JavaLabeledParser::QualifiedNameListContext::qualifiedName() {
  return getRuleContexts<JavaLabeledParser::QualifiedNameContext>();
}

JavaLabeledParser::QualifiedNameContext* JavaLabeledParser::QualifiedNameListContext::qualifiedName(size_t i) {
  return getRuleContext<JavaLabeledParser::QualifiedNameContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::QualifiedNameListContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::QualifiedNameListContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::QualifiedNameListContext::getRuleIndex() const {
  return JavaLabeledParser::RuleQualifiedNameList;
}

void JavaLabeledParser::QualifiedNameListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterQualifiedNameList(this);
}

void JavaLabeledParser::QualifiedNameListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitQualifiedNameList(this);
}


antlrcpp::Any JavaLabeledParser::QualifiedNameListContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitQualifiedNameList(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::QualifiedNameListContext* JavaLabeledParser::qualifiedNameList() {
  QualifiedNameListContext *_localctx = _tracker.createInstance<QualifiedNameListContext>(_ctx, getState());
  enterRule(_localctx, 82, JavaLabeledParser::RuleQualifiedNameList);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(631);
    qualifiedName();
    setState(636);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::COMMA) {
      setState(632);
      match(JavaLabeledParser::COMMA);
      setState(633);
      qualifiedName();
      setState(638);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FormalParametersContext ------------------------------------------------------------------

JavaLabeledParser::FormalParametersContext::FormalParametersContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::FormalParametersContext::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::FormalParametersContext::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::FormalParameterListContext* JavaLabeledParser::FormalParametersContext::formalParameterList() {
  return getRuleContext<JavaLabeledParser::FormalParameterListContext>(0);
}


size_t JavaLabeledParser::FormalParametersContext::getRuleIndex() const {
  return JavaLabeledParser::RuleFormalParameters;
}

void JavaLabeledParser::FormalParametersContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormalParameters(this);
}

void JavaLabeledParser::FormalParametersContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormalParameters(this);
}


antlrcpp::Any JavaLabeledParser::FormalParametersContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitFormalParameters(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::FormalParametersContext* JavaLabeledParser::formalParameters() {
  FormalParametersContext *_localctx = _tracker.createInstance<FormalParametersContext>(_ctx, getState());
  enterRule(_localctx, 84, JavaLabeledParser::RuleFormalParameters);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(639);
    match(JavaLabeledParser::LPAREN);
    setState(641);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::FINAL)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::SHORT))) != 0) || _la == JavaLabeledParser::AT

    || _la == JavaLabeledParser::IDENTIFIER) {
      setState(640);
      formalParameterList();
    }
    setState(643);
    match(JavaLabeledParser::RPAREN);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FormalParameterListContext ------------------------------------------------------------------

JavaLabeledParser::FormalParameterListContext::FormalParameterListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::FormalParameterListContext::getRuleIndex() const {
  return JavaLabeledParser::RuleFormalParameterList;
}

void JavaLabeledParser::FormalParameterListContext::copyFrom(FormalParameterListContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- FormalParameterList1Context ------------------------------------------------------------------

JavaLabeledParser::LastFormalParameterContext* JavaLabeledParser::FormalParameterList1Context::lastFormalParameter() {
  return getRuleContext<JavaLabeledParser::LastFormalParameterContext>(0);
}

JavaLabeledParser::FormalParameterList1Context::FormalParameterList1Context(FormalParameterListContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::FormalParameterList1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormalParameterList1(this);
}
void JavaLabeledParser::FormalParameterList1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormalParameterList1(this);
}

antlrcpp::Any JavaLabeledParser::FormalParameterList1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitFormalParameterList1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- FormalParameterList0Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::FormalParameterContext *> JavaLabeledParser::FormalParameterList0Context::formalParameter() {
  return getRuleContexts<JavaLabeledParser::FormalParameterContext>();
}

JavaLabeledParser::FormalParameterContext* JavaLabeledParser::FormalParameterList0Context::formalParameter(size_t i) {
  return getRuleContext<JavaLabeledParser::FormalParameterContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::FormalParameterList0Context::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::FormalParameterList0Context::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}

JavaLabeledParser::LastFormalParameterContext* JavaLabeledParser::FormalParameterList0Context::lastFormalParameter() {
  return getRuleContext<JavaLabeledParser::LastFormalParameterContext>(0);
}

JavaLabeledParser::FormalParameterList0Context::FormalParameterList0Context(FormalParameterListContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::FormalParameterList0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormalParameterList0(this);
}
void JavaLabeledParser::FormalParameterList0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormalParameterList0(this);
}

antlrcpp::Any JavaLabeledParser::FormalParameterList0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitFormalParameterList0(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::FormalParameterListContext* JavaLabeledParser::formalParameterList() {
  FormalParameterListContext *_localctx = _tracker.createInstance<FormalParameterListContext>(_ctx, getState());
  enterRule(_localctx, 86, JavaLabeledParser::RuleFormalParameterList);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    setState(658);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 70, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::FormalParameterList0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(645);
      formalParameter();
      setState(650);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 68, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(646);
          match(JavaLabeledParser::COMMA);
          setState(647);
          formalParameter(); 
        }
        setState(652);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 68, _ctx);
      }
      setState(655);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::COMMA) {
        setState(653);
        match(JavaLabeledParser::COMMA);
        setState(654);
        lastFormalParameter();
      }
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::FormalParameterList1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(657);
      lastFormalParameter();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FormalParameterContext ------------------------------------------------------------------

JavaLabeledParser::FormalParameterContext::FormalParameterContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::FormalParameterContext::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

JavaLabeledParser::VariableDeclaratorIdContext* JavaLabeledParser::FormalParameterContext::variableDeclaratorId() {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorIdContext>(0);
}

std::vector<JavaLabeledParser::VariableModifierContext *> JavaLabeledParser::FormalParameterContext::variableModifier() {
  return getRuleContexts<JavaLabeledParser::VariableModifierContext>();
}

JavaLabeledParser::VariableModifierContext* JavaLabeledParser::FormalParameterContext::variableModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::VariableModifierContext>(i);
}


size_t JavaLabeledParser::FormalParameterContext::getRuleIndex() const {
  return JavaLabeledParser::RuleFormalParameter;
}

void JavaLabeledParser::FormalParameterContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormalParameter(this);
}

void JavaLabeledParser::FormalParameterContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormalParameter(this);
}


antlrcpp::Any JavaLabeledParser::FormalParameterContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitFormalParameter(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::FormalParameterContext* JavaLabeledParser::formalParameter() {
  FormalParameterContext *_localctx = _tracker.createInstance<FormalParameterContext>(_ctx, getState());
  enterRule(_localctx, 88, JavaLabeledParser::RuleFormalParameter);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(663);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 71, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(660);
        variableModifier(); 
      }
      setState(665);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 71, _ctx);
    }
    setState(666);
    typeType();
    setState(667);
    variableDeclaratorId();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LastFormalParameterContext ------------------------------------------------------------------

JavaLabeledParser::LastFormalParameterContext::LastFormalParameterContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::LastFormalParameterContext::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::LastFormalParameterContext::ELLIPSIS() {
  return getToken(JavaLabeledParser::ELLIPSIS, 0);
}

JavaLabeledParser::VariableDeclaratorIdContext* JavaLabeledParser::LastFormalParameterContext::variableDeclaratorId() {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorIdContext>(0);
}

std::vector<JavaLabeledParser::VariableModifierContext *> JavaLabeledParser::LastFormalParameterContext::variableModifier() {
  return getRuleContexts<JavaLabeledParser::VariableModifierContext>();
}

JavaLabeledParser::VariableModifierContext* JavaLabeledParser::LastFormalParameterContext::variableModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::VariableModifierContext>(i);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::LastFormalParameterContext::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::LastFormalParameterContext::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}


size_t JavaLabeledParser::LastFormalParameterContext::getRuleIndex() const {
  return JavaLabeledParser::RuleLastFormalParameter;
}

void JavaLabeledParser::LastFormalParameterContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLastFormalParameter(this);
}

void JavaLabeledParser::LastFormalParameterContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLastFormalParameter(this);
}


antlrcpp::Any JavaLabeledParser::LastFormalParameterContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLastFormalParameter(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::LastFormalParameterContext* JavaLabeledParser::lastFormalParameter() {
  LastFormalParameterContext *_localctx = _tracker.createInstance<LastFormalParameterContext>(_ctx, getState());
  enterRule(_localctx, 90, JavaLabeledParser::RuleLastFormalParameter);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(672);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 72, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(669);
        variableModifier(); 
      }
      setState(674);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 72, _ctx);
    }
    setState(675);
    typeType();
    setState(679);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::AT

    || _la == JavaLabeledParser::IDENTIFIER) {
      setState(676);
      annotation();
      setState(681);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(682);
    match(JavaLabeledParser::ELLIPSIS);
    setState(683);
    variableDeclaratorId();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- QualifiedNameContext ------------------------------------------------------------------

JavaLabeledParser::QualifiedNameContext::QualifiedNameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> JavaLabeledParser::QualifiedNameContext::IDENTIFIER() {
  return getTokens(JavaLabeledParser::IDENTIFIER);
}

tree::TerminalNode* JavaLabeledParser::QualifiedNameContext::IDENTIFIER(size_t i) {
  return getToken(JavaLabeledParser::IDENTIFIER, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::QualifiedNameContext::DOT() {
  return getTokens(JavaLabeledParser::DOT);
}

tree::TerminalNode* JavaLabeledParser::QualifiedNameContext::DOT(size_t i) {
  return getToken(JavaLabeledParser::DOT, i);
}


size_t JavaLabeledParser::QualifiedNameContext::getRuleIndex() const {
  return JavaLabeledParser::RuleQualifiedName;
}

void JavaLabeledParser::QualifiedNameContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterQualifiedName(this);
}

void JavaLabeledParser::QualifiedNameContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitQualifiedName(this);
}


antlrcpp::Any JavaLabeledParser::QualifiedNameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitQualifiedName(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::QualifiedNameContext* JavaLabeledParser::qualifiedName() {
  QualifiedNameContext *_localctx = _tracker.createInstance<QualifiedNameContext>(_ctx, getState());
  enterRule(_localctx, 92, JavaLabeledParser::RuleQualifiedName);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(685);
    match(JavaLabeledParser::IDENTIFIER);
    setState(690);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 74, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(686);
        match(JavaLabeledParser::DOT);
        setState(687);
        match(JavaLabeledParser::IDENTIFIER); 
      }
      setState(692);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 74, _ctx);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LiteralContext ------------------------------------------------------------------

JavaLabeledParser::LiteralContext::LiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::LiteralContext::getRuleIndex() const {
  return JavaLabeledParser::RuleLiteral;
}

void JavaLabeledParser::LiteralContext::copyFrom(LiteralContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Literal2Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Literal2Context::CHAR_LITERAL() {
  return getToken(JavaLabeledParser::CHAR_LITERAL, 0);
}

JavaLabeledParser::Literal2Context::Literal2Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Literal2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral2(this);
}
void JavaLabeledParser::Literal2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral2(this);
}

antlrcpp::Any JavaLabeledParser::Literal2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLiteral2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal1Context ------------------------------------------------------------------

JavaLabeledParser::FloatLiteralContext* JavaLabeledParser::Literal1Context::floatLiteral() {
  return getRuleContext<JavaLabeledParser::FloatLiteralContext>(0);
}

JavaLabeledParser::Literal1Context::Literal1Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Literal1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral1(this);
}
void JavaLabeledParser::Literal1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral1(this);
}

antlrcpp::Any JavaLabeledParser::Literal1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLiteral1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal0Context ------------------------------------------------------------------

JavaLabeledParser::IntegerLiteralContext* JavaLabeledParser::Literal0Context::integerLiteral() {
  return getRuleContext<JavaLabeledParser::IntegerLiteralContext>(0);
}

JavaLabeledParser::Literal0Context::Literal0Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Literal0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral0(this);
}
void JavaLabeledParser::Literal0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral0(this);
}

antlrcpp::Any JavaLabeledParser::Literal0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLiteral0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal5Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Literal5Context::NULL_LITERAL() {
  return getToken(JavaLabeledParser::NULL_LITERAL, 0);
}

JavaLabeledParser::Literal5Context::Literal5Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Literal5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral5(this);
}
void JavaLabeledParser::Literal5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral5(this);
}

antlrcpp::Any JavaLabeledParser::Literal5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLiteral5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal4Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Literal4Context::BOOL_LITERAL() {
  return getToken(JavaLabeledParser::BOOL_LITERAL, 0);
}

JavaLabeledParser::Literal4Context::Literal4Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Literal4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral4(this);
}
void JavaLabeledParser::Literal4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral4(this);
}

antlrcpp::Any JavaLabeledParser::Literal4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLiteral4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal3Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Literal3Context::STRING_LITERAL() {
  return getToken(JavaLabeledParser::STRING_LITERAL, 0);
}

JavaLabeledParser::Literal3Context::Literal3Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Literal3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral3(this);
}
void JavaLabeledParser::Literal3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral3(this);
}

antlrcpp::Any JavaLabeledParser::Literal3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLiteral3(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::LiteralContext* JavaLabeledParser::literal() {
  LiteralContext *_localctx = _tracker.createInstance<LiteralContext>(_ctx, getState());
  enterRule(_localctx, 94, JavaLabeledParser::RuleLiteral);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(699);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::DECIMAL_LITERAL:
      case JavaLabeledParser::HEX_LITERAL:
      case JavaLabeledParser::OCT_LITERAL:
      case JavaLabeledParser::BINARY_LITERAL: {
        _localctx = _tracker.createInstance<JavaLabeledParser::Literal0Context>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(693);
        integerLiteral();
        break;
      }

      case JavaLabeledParser::FLOAT_LITERAL:
      case JavaLabeledParser::HEX_FLOAT_LITERAL: {
        _localctx = _tracker.createInstance<JavaLabeledParser::Literal1Context>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(694);
        floatLiteral();
        break;
      }

      case JavaLabeledParser::CHAR_LITERAL: {
        _localctx = _tracker.createInstance<JavaLabeledParser::Literal2Context>(_localctx);
        enterOuterAlt(_localctx, 3);
        setState(695);
        match(JavaLabeledParser::CHAR_LITERAL);
        break;
      }

      case JavaLabeledParser::STRING_LITERAL: {
        _localctx = _tracker.createInstance<JavaLabeledParser::Literal3Context>(_localctx);
        enterOuterAlt(_localctx, 4);
        setState(696);
        match(JavaLabeledParser::STRING_LITERAL);
        break;
      }

      case JavaLabeledParser::BOOL_LITERAL: {
        _localctx = _tracker.createInstance<JavaLabeledParser::Literal4Context>(_localctx);
        enterOuterAlt(_localctx, 5);
        setState(697);
        match(JavaLabeledParser::BOOL_LITERAL);
        break;
      }

      case JavaLabeledParser::NULL_LITERAL: {
        _localctx = _tracker.createInstance<JavaLabeledParser::Literal5Context>(_localctx);
        enterOuterAlt(_localctx, 6);
        setState(698);
        match(JavaLabeledParser::NULL_LITERAL);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- IntegerLiteralContext ------------------------------------------------------------------

JavaLabeledParser::IntegerLiteralContext::IntegerLiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::IntegerLiteralContext::DECIMAL_LITERAL() {
  return getToken(JavaLabeledParser::DECIMAL_LITERAL, 0);
}

tree::TerminalNode* JavaLabeledParser::IntegerLiteralContext::HEX_LITERAL() {
  return getToken(JavaLabeledParser::HEX_LITERAL, 0);
}

tree::TerminalNode* JavaLabeledParser::IntegerLiteralContext::OCT_LITERAL() {
  return getToken(JavaLabeledParser::OCT_LITERAL, 0);
}

tree::TerminalNode* JavaLabeledParser::IntegerLiteralContext::BINARY_LITERAL() {
  return getToken(JavaLabeledParser::BINARY_LITERAL, 0);
}


size_t JavaLabeledParser::IntegerLiteralContext::getRuleIndex() const {
  return JavaLabeledParser::RuleIntegerLiteral;
}

void JavaLabeledParser::IntegerLiteralContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterIntegerLiteral(this);
}

void JavaLabeledParser::IntegerLiteralContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitIntegerLiteral(this);
}


antlrcpp::Any JavaLabeledParser::IntegerLiteralContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitIntegerLiteral(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::IntegerLiteralContext* JavaLabeledParser::integerLiteral() {
  IntegerLiteralContext *_localctx = _tracker.createInstance<IntegerLiteralContext>(_ctx, getState());
  enterRule(_localctx, 96, JavaLabeledParser::RuleIntegerLiteral);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(701);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::DECIMAL_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_LITERAL)
      | (1ULL << JavaLabeledParser::OCT_LITERAL)
      | (1ULL << JavaLabeledParser::BINARY_LITERAL))) != 0))) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FloatLiteralContext ------------------------------------------------------------------

JavaLabeledParser::FloatLiteralContext::FloatLiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::FloatLiteralContext::FLOAT_LITERAL() {
  return getToken(JavaLabeledParser::FLOAT_LITERAL, 0);
}

tree::TerminalNode* JavaLabeledParser::FloatLiteralContext::HEX_FLOAT_LITERAL() {
  return getToken(JavaLabeledParser::HEX_FLOAT_LITERAL, 0);
}


size_t JavaLabeledParser::FloatLiteralContext::getRuleIndex() const {
  return JavaLabeledParser::RuleFloatLiteral;
}

void JavaLabeledParser::FloatLiteralContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFloatLiteral(this);
}

void JavaLabeledParser::FloatLiteralContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFloatLiteral(this);
}


antlrcpp::Any JavaLabeledParser::FloatLiteralContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitFloatLiteral(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::FloatLiteralContext* JavaLabeledParser::floatLiteral() {
  FloatLiteralContext *_localctx = _tracker.createInstance<FloatLiteralContext>(_ctx, getState());
  enterRule(_localctx, 98, JavaLabeledParser::RuleFloatLiteral);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(703);
    _la = _input->LA(1);
    if (!(_la == JavaLabeledParser::FLOAT_LITERAL

    || _la == JavaLabeledParser::HEX_FLOAT_LITERAL)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AltAnnotationQualifiedNameContext ------------------------------------------------------------------

JavaLabeledParser::AltAnnotationQualifiedNameContext::AltAnnotationQualifiedNameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::AltAnnotationQualifiedNameContext::AT() {
  return getToken(JavaLabeledParser::AT, 0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::AltAnnotationQualifiedNameContext::IDENTIFIER() {
  return getTokens(JavaLabeledParser::IDENTIFIER);
}

tree::TerminalNode* JavaLabeledParser::AltAnnotationQualifiedNameContext::IDENTIFIER(size_t i) {
  return getToken(JavaLabeledParser::IDENTIFIER, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::AltAnnotationQualifiedNameContext::DOT() {
  return getTokens(JavaLabeledParser::DOT);
}

tree::TerminalNode* JavaLabeledParser::AltAnnotationQualifiedNameContext::DOT(size_t i) {
  return getToken(JavaLabeledParser::DOT, i);
}


size_t JavaLabeledParser::AltAnnotationQualifiedNameContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAltAnnotationQualifiedName;
}

void JavaLabeledParser::AltAnnotationQualifiedNameContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAltAnnotationQualifiedName(this);
}

void JavaLabeledParser::AltAnnotationQualifiedNameContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAltAnnotationQualifiedName(this);
}


antlrcpp::Any JavaLabeledParser::AltAnnotationQualifiedNameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAltAnnotationQualifiedName(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::AltAnnotationQualifiedNameContext* JavaLabeledParser::altAnnotationQualifiedName() {
  AltAnnotationQualifiedNameContext *_localctx = _tracker.createInstance<AltAnnotationQualifiedNameContext>(_ctx, getState());
  enterRule(_localctx, 100, JavaLabeledParser::RuleAltAnnotationQualifiedName);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(709);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::IDENTIFIER) {
      setState(705);
      match(JavaLabeledParser::IDENTIFIER);
      setState(706);
      match(JavaLabeledParser::DOT);
      setState(711);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(712);
    match(JavaLabeledParser::AT);
    setState(713);
    match(JavaLabeledParser::IDENTIFIER);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationContext ------------------------------------------------------------------

JavaLabeledParser::AnnotationContext::AnnotationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::AnnotationContext::AT() {
  return getToken(JavaLabeledParser::AT, 0);
}

JavaLabeledParser::QualifiedNameContext* JavaLabeledParser::AnnotationContext::qualifiedName() {
  return getRuleContext<JavaLabeledParser::QualifiedNameContext>(0);
}

JavaLabeledParser::AltAnnotationQualifiedNameContext* JavaLabeledParser::AnnotationContext::altAnnotationQualifiedName() {
  return getRuleContext<JavaLabeledParser::AltAnnotationQualifiedNameContext>(0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationContext::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationContext::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::ElementValuePairsContext* JavaLabeledParser::AnnotationContext::elementValuePairs() {
  return getRuleContext<JavaLabeledParser::ElementValuePairsContext>(0);
}

JavaLabeledParser::ElementValueContext* JavaLabeledParser::AnnotationContext::elementValue() {
  return getRuleContext<JavaLabeledParser::ElementValueContext>(0);
}


size_t JavaLabeledParser::AnnotationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAnnotation;
}

void JavaLabeledParser::AnnotationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotation(this);
}

void JavaLabeledParser::AnnotationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotation(this);
}


antlrcpp::Any JavaLabeledParser::AnnotationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotation(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::annotation() {
  AnnotationContext *_localctx = _tracker.createInstance<AnnotationContext>(_ctx, getState());
  enterRule(_localctx, 102, JavaLabeledParser::RuleAnnotation);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(718);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 77, _ctx)) {
    case 1: {
      setState(715);
      match(JavaLabeledParser::AT);
      setState(716);
      qualifiedName();
      break;
    }

    case 2: {
      setState(717);
      altAnnotationQualifiedName();
      break;
    }

    default:
      break;
    }
    setState(726);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::LPAREN) {
      setState(720);
      match(JavaLabeledParser::LPAREN);
      setState(723);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 78, _ctx)) {
      case 1: {
        setState(721);
        elementValuePairs();
        break;
      }

      case 2: {
        setState(722);
        elementValue();
        break;
      }

      default:
        break;
      }
      setState(725);
      match(JavaLabeledParser::RPAREN);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ElementValuePairsContext ------------------------------------------------------------------

JavaLabeledParser::ElementValuePairsContext::ElementValuePairsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::ElementValuePairContext *> JavaLabeledParser::ElementValuePairsContext::elementValuePair() {
  return getRuleContexts<JavaLabeledParser::ElementValuePairContext>();
}

JavaLabeledParser::ElementValuePairContext* JavaLabeledParser::ElementValuePairsContext::elementValuePair(size_t i) {
  return getRuleContext<JavaLabeledParser::ElementValuePairContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ElementValuePairsContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::ElementValuePairsContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::ElementValuePairsContext::getRuleIndex() const {
  return JavaLabeledParser::RuleElementValuePairs;
}

void JavaLabeledParser::ElementValuePairsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValuePairs(this);
}

void JavaLabeledParser::ElementValuePairsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValuePairs(this);
}


antlrcpp::Any JavaLabeledParser::ElementValuePairsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitElementValuePairs(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ElementValuePairsContext* JavaLabeledParser::elementValuePairs() {
  ElementValuePairsContext *_localctx = _tracker.createInstance<ElementValuePairsContext>(_ctx, getState());
  enterRule(_localctx, 104, JavaLabeledParser::RuleElementValuePairs);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(728);
    elementValuePair();
    setState(733);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::COMMA) {
      setState(729);
      match(JavaLabeledParser::COMMA);
      setState(730);
      elementValuePair();
      setState(735);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ElementValuePairContext ------------------------------------------------------------------

JavaLabeledParser::ElementValuePairContext::ElementValuePairContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ElementValuePairContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

tree::TerminalNode* JavaLabeledParser::ElementValuePairContext::ASSIGN() {
  return getToken(JavaLabeledParser::ASSIGN, 0);
}

JavaLabeledParser::ElementValueContext* JavaLabeledParser::ElementValuePairContext::elementValue() {
  return getRuleContext<JavaLabeledParser::ElementValueContext>(0);
}


size_t JavaLabeledParser::ElementValuePairContext::getRuleIndex() const {
  return JavaLabeledParser::RuleElementValuePair;
}

void JavaLabeledParser::ElementValuePairContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValuePair(this);
}

void JavaLabeledParser::ElementValuePairContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValuePair(this);
}


antlrcpp::Any JavaLabeledParser::ElementValuePairContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitElementValuePair(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ElementValuePairContext* JavaLabeledParser::elementValuePair() {
  ElementValuePairContext *_localctx = _tracker.createInstance<ElementValuePairContext>(_ctx, getState());
  enterRule(_localctx, 106, JavaLabeledParser::RuleElementValuePair);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(736);
    match(JavaLabeledParser::IDENTIFIER);
    setState(737);
    match(JavaLabeledParser::ASSIGN);
    setState(738);
    elementValue();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ElementValueContext ------------------------------------------------------------------

JavaLabeledParser::ElementValueContext::ElementValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::ElementValueContext::getRuleIndex() const {
  return JavaLabeledParser::RuleElementValue;
}

void JavaLabeledParser::ElementValueContext::copyFrom(ElementValueContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ElementValue0Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::ElementValue0Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

JavaLabeledParser::ElementValue0Context::ElementValue0Context(ElementValueContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ElementValue0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValue0(this);
}
void JavaLabeledParser::ElementValue0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValue0(this);
}

antlrcpp::Any JavaLabeledParser::ElementValue0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitElementValue0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ElementValue2Context ------------------------------------------------------------------

JavaLabeledParser::ElementValueArrayInitializerContext* JavaLabeledParser::ElementValue2Context::elementValueArrayInitializer() {
  return getRuleContext<JavaLabeledParser::ElementValueArrayInitializerContext>(0);
}

JavaLabeledParser::ElementValue2Context::ElementValue2Context(ElementValueContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ElementValue2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValue2(this);
}
void JavaLabeledParser::ElementValue2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValue2(this);
}

antlrcpp::Any JavaLabeledParser::ElementValue2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitElementValue2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ElementValue1Context ------------------------------------------------------------------

JavaLabeledParser::AnnotationContext* JavaLabeledParser::ElementValue1Context::annotation() {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(0);
}

JavaLabeledParser::ElementValue1Context::ElementValue1Context(ElementValueContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ElementValue1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValue1(this);
}
void JavaLabeledParser::ElementValue1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValue1(this);
}

antlrcpp::Any JavaLabeledParser::ElementValue1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitElementValue1(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::ElementValueContext* JavaLabeledParser::elementValue() {
  ElementValueContext *_localctx = _tracker.createInstance<ElementValueContext>(_ctx, getState());
  enterRule(_localctx, 108, JavaLabeledParser::RuleElementValue);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(743);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 81, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ElementValue0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(740);
      expression(0);
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ElementValue1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(741);
      annotation();
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ElementValue2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(742);
      elementValueArrayInitializer();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ElementValueArrayInitializerContext ------------------------------------------------------------------

JavaLabeledParser::ElementValueArrayInitializerContext::ElementValueArrayInitializerContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ElementValueArrayInitializerContext::LBRACE() {
  return getToken(JavaLabeledParser::LBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::ElementValueArrayInitializerContext::RBRACE() {
  return getToken(JavaLabeledParser::RBRACE, 0);
}

std::vector<JavaLabeledParser::ElementValueContext *> JavaLabeledParser::ElementValueArrayInitializerContext::elementValue() {
  return getRuleContexts<JavaLabeledParser::ElementValueContext>();
}

JavaLabeledParser::ElementValueContext* JavaLabeledParser::ElementValueArrayInitializerContext::elementValue(size_t i) {
  return getRuleContext<JavaLabeledParser::ElementValueContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ElementValueArrayInitializerContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::ElementValueArrayInitializerContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::ElementValueArrayInitializerContext::getRuleIndex() const {
  return JavaLabeledParser::RuleElementValueArrayInitializer;
}

void JavaLabeledParser::ElementValueArrayInitializerContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValueArrayInitializer(this);
}

void JavaLabeledParser::ElementValueArrayInitializerContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValueArrayInitializer(this);
}


antlrcpp::Any JavaLabeledParser::ElementValueArrayInitializerContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitElementValueArrayInitializer(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ElementValueArrayInitializerContext* JavaLabeledParser::elementValueArrayInitializer() {
  ElementValueArrayInitializerContext *_localctx = _tracker.createInstance<ElementValueArrayInitializerContext>(_ctx, getState());
  enterRule(_localctx, 110, JavaLabeledParser::RuleElementValueArrayInitializer);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(745);
    match(JavaLabeledParser::LBRACE);
    setState(754);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NEW)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::SUPER)
      | (1ULL << JavaLabeledParser::THIS)
      | (1ULL << JavaLabeledParser::VOID)
      | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_LITERAL)
      | (1ULL << JavaLabeledParser::OCT_LITERAL)
      | (1ULL << JavaLabeledParser::BINARY_LITERAL)
      | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::BOOL_LITERAL)
      | (1ULL << JavaLabeledParser::CHAR_LITERAL)
      | (1ULL << JavaLabeledParser::STRING_LITERAL)
      | (1ULL << JavaLabeledParser::NULL_LITERAL)
      | (1ULL << JavaLabeledParser::LPAREN)
      | (1ULL << JavaLabeledParser::LBRACE))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
      | (1ULL << (JavaLabeledParser::BANG - 72))
      | (1ULL << (JavaLabeledParser::TILDE - 72))
      | (1ULL << (JavaLabeledParser::INC - 72))
      | (1ULL << (JavaLabeledParser::DEC - 72))
      | (1ULL << (JavaLabeledParser::ADD - 72))
      | (1ULL << (JavaLabeledParser::SUB - 72))
      | (1ULL << (JavaLabeledParser::AT - 72))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
      setState(746);
      elementValue();
      setState(751);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 82, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(747);
          match(JavaLabeledParser::COMMA);
          setState(748);
          elementValue(); 
        }
        setState(753);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 82, _ctx);
      }
    }
    setState(757);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::COMMA) {
      setState(756);
      match(JavaLabeledParser::COMMA);
    }
    setState(759);
    match(JavaLabeledParser::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationTypeDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::AnnotationTypeDeclarationContext::AnnotationTypeDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeDeclarationContext::AT() {
  return getToken(JavaLabeledParser::AT, 0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeDeclarationContext::INTERFACE() {
  return getToken(JavaLabeledParser::INTERFACE, 0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeDeclarationContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::AnnotationTypeBodyContext* JavaLabeledParser::AnnotationTypeDeclarationContext::annotationTypeBody() {
  return getRuleContext<JavaLabeledParser::AnnotationTypeBodyContext>(0);
}


size_t JavaLabeledParser::AnnotationTypeDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAnnotationTypeDeclaration;
}

void JavaLabeledParser::AnnotationTypeDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeDeclaration(this);
}

void JavaLabeledParser::AnnotationTypeDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::AnnotationTypeDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::AnnotationTypeDeclarationContext* JavaLabeledParser::annotationTypeDeclaration() {
  AnnotationTypeDeclarationContext *_localctx = _tracker.createInstance<AnnotationTypeDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 112, JavaLabeledParser::RuleAnnotationTypeDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(761);
    match(JavaLabeledParser::AT);
    setState(762);
    match(JavaLabeledParser::INTERFACE);
    setState(763);
    match(JavaLabeledParser::IDENTIFIER);
    setState(764);
    annotationTypeBody();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationTypeBodyContext ------------------------------------------------------------------

JavaLabeledParser::AnnotationTypeBodyContext::AnnotationTypeBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeBodyContext::LBRACE() {
  return getToken(JavaLabeledParser::LBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeBodyContext::RBRACE() {
  return getToken(JavaLabeledParser::RBRACE, 0);
}

std::vector<JavaLabeledParser::AnnotationTypeElementDeclarationContext *> JavaLabeledParser::AnnotationTypeBodyContext::annotationTypeElementDeclaration() {
  return getRuleContexts<JavaLabeledParser::AnnotationTypeElementDeclarationContext>();
}

JavaLabeledParser::AnnotationTypeElementDeclarationContext* JavaLabeledParser::AnnotationTypeBodyContext::annotationTypeElementDeclaration(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationTypeElementDeclarationContext>(i);
}


size_t JavaLabeledParser::AnnotationTypeBodyContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAnnotationTypeBody;
}

void JavaLabeledParser::AnnotationTypeBodyContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeBody(this);
}

void JavaLabeledParser::AnnotationTypeBodyContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeBody(this);
}


antlrcpp::Any JavaLabeledParser::AnnotationTypeBodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeBody(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::AnnotationTypeBodyContext* JavaLabeledParser::annotationTypeBody() {
  AnnotationTypeBodyContext *_localctx = _tracker.createInstance<AnnotationTypeBodyContext>(_ctx, getState());
  enterRule(_localctx, 114, JavaLabeledParser::RuleAnnotationTypeBody);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(766);
    match(JavaLabeledParser::LBRACE);
    setState(770);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::ABSTRACT)
      | (1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::CLASS)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::ENUM)
      | (1ULL << JavaLabeledParser::FINAL)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::INTERFACE)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NATIVE)
      | (1ULL << JavaLabeledParser::PRIVATE)
      | (1ULL << JavaLabeledParser::PROTECTED)
      | (1ULL << JavaLabeledParser::PUBLIC)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::STATIC)
      | (1ULL << JavaLabeledParser::STRICTFP)
      | (1ULL << JavaLabeledParser::SYNCHRONIZED)
      | (1ULL << JavaLabeledParser::TRANSIENT)
      | (1ULL << JavaLabeledParser::VOLATILE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaLabeledParser::SEMI - 67))
      | (1ULL << (JavaLabeledParser::AT - 67))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 67)))) != 0)) {
      setState(767);
      annotationTypeElementDeclaration();
      setState(772);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(773);
    match(JavaLabeledParser::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationTypeElementDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::AnnotationTypeElementDeclarationContext::AnnotationTypeElementDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::AnnotationTypeElementRestContext* JavaLabeledParser::AnnotationTypeElementDeclarationContext::annotationTypeElementRest() {
  return getRuleContext<JavaLabeledParser::AnnotationTypeElementRestContext>(0);
}

std::vector<JavaLabeledParser::ModifierContext *> JavaLabeledParser::AnnotationTypeElementDeclarationContext::modifier() {
  return getRuleContexts<JavaLabeledParser::ModifierContext>();
}

JavaLabeledParser::ModifierContext* JavaLabeledParser::AnnotationTypeElementDeclarationContext::modifier(size_t i) {
  return getRuleContext<JavaLabeledParser::ModifierContext>(i);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeElementDeclarationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}


size_t JavaLabeledParser::AnnotationTypeElementDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAnnotationTypeElementDeclaration;
}

void JavaLabeledParser::AnnotationTypeElementDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementDeclaration(this);
}

void JavaLabeledParser::AnnotationTypeElementDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::AnnotationTypeElementDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::AnnotationTypeElementDeclarationContext* JavaLabeledParser::annotationTypeElementDeclaration() {
  AnnotationTypeElementDeclarationContext *_localctx = _tracker.createInstance<AnnotationTypeElementDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 116, JavaLabeledParser::RuleAnnotationTypeElementDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    setState(783);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::ABSTRACT:
      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::CLASS:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::ENUM:
      case JavaLabeledParser::FINAL:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::INTERFACE:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::NATIVE:
      case JavaLabeledParser::PRIVATE:
      case JavaLabeledParser::PROTECTED:
      case JavaLabeledParser::PUBLIC:
      case JavaLabeledParser::SHORT:
      case JavaLabeledParser::STATIC:
      case JavaLabeledParser::STRICTFP:
      case JavaLabeledParser::SYNCHRONIZED:
      case JavaLabeledParser::TRANSIENT:
      case JavaLabeledParser::VOLATILE:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(778);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 86, _ctx);
        while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
          if (alt == 1) {
            setState(775);
            modifier(); 
          }
          setState(780);
          _errHandler->sync(this);
          alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 86, _ctx);
        }
        setState(781);
        annotationTypeElementRest();
        break;
      }

      case JavaLabeledParser::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(782);
        match(JavaLabeledParser::SEMI);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationTypeElementRestContext ------------------------------------------------------------------

JavaLabeledParser::AnnotationTypeElementRestContext::AnnotationTypeElementRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::AnnotationTypeElementRestContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAnnotationTypeElementRest;
}

void JavaLabeledParser::AnnotationTypeElementRestContext::copyFrom(AnnotationTypeElementRestContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- AnnotationTypeElementRest0Context ------------------------------------------------------------------

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::AnnotationTypeElementRest0Context::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

JavaLabeledParser::AnnotationMethodOrConstantRestContext* JavaLabeledParser::AnnotationTypeElementRest0Context::annotationMethodOrConstantRest() {
  return getRuleContext<JavaLabeledParser::AnnotationMethodOrConstantRestContext>(0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeElementRest0Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::AnnotationTypeElementRest0Context::AnnotationTypeElementRest0Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::AnnotationTypeElementRest0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest0(this);
}
void JavaLabeledParser::AnnotationTypeElementRest0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest0(this);
}

antlrcpp::Any JavaLabeledParser::AnnotationTypeElementRest0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationTypeElementRest1Context ------------------------------------------------------------------

JavaLabeledParser::ClassDeclarationContext* JavaLabeledParser::AnnotationTypeElementRest1Context::classDeclaration() {
  return getRuleContext<JavaLabeledParser::ClassDeclarationContext>(0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeElementRest1Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::AnnotationTypeElementRest1Context::AnnotationTypeElementRest1Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::AnnotationTypeElementRest1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest1(this);
}
void JavaLabeledParser::AnnotationTypeElementRest1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest1(this);
}

antlrcpp::Any JavaLabeledParser::AnnotationTypeElementRest1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationTypeElementRest2Context ------------------------------------------------------------------

JavaLabeledParser::InterfaceDeclarationContext* JavaLabeledParser::AnnotationTypeElementRest2Context::interfaceDeclaration() {
  return getRuleContext<JavaLabeledParser::InterfaceDeclarationContext>(0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeElementRest2Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::AnnotationTypeElementRest2Context::AnnotationTypeElementRest2Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::AnnotationTypeElementRest2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest2(this);
}
void JavaLabeledParser::AnnotationTypeElementRest2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest2(this);
}

antlrcpp::Any JavaLabeledParser::AnnotationTypeElementRest2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationTypeElementRest3Context ------------------------------------------------------------------

JavaLabeledParser::EnumDeclarationContext* JavaLabeledParser::AnnotationTypeElementRest3Context::enumDeclaration() {
  return getRuleContext<JavaLabeledParser::EnumDeclarationContext>(0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeElementRest3Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::AnnotationTypeElementRest3Context::AnnotationTypeElementRest3Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::AnnotationTypeElementRest3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest3(this);
}
void JavaLabeledParser::AnnotationTypeElementRest3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest3(this);
}

antlrcpp::Any JavaLabeledParser::AnnotationTypeElementRest3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationTypeElementRest4Context ------------------------------------------------------------------

JavaLabeledParser::AnnotationTypeDeclarationContext* JavaLabeledParser::AnnotationTypeElementRest4Context::annotationTypeDeclaration() {
  return getRuleContext<JavaLabeledParser::AnnotationTypeDeclarationContext>(0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationTypeElementRest4Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::AnnotationTypeElementRest4Context::AnnotationTypeElementRest4Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::AnnotationTypeElementRest4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest4(this);
}
void JavaLabeledParser::AnnotationTypeElementRest4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest4(this);
}

antlrcpp::Any JavaLabeledParser::AnnotationTypeElementRest4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest4(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::AnnotationTypeElementRestContext* JavaLabeledParser::annotationTypeElementRest() {
  AnnotationTypeElementRestContext *_localctx = _tracker.createInstance<AnnotationTypeElementRestContext>(_ctx, getState());
  enterRule(_localctx, 118, JavaLabeledParser::RuleAnnotationTypeElementRest);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(805);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 92, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::AnnotationTypeElementRest0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(785);
      typeType();
      setState(786);
      annotationMethodOrConstantRest();
      setState(787);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::AnnotationTypeElementRest1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(789);
      classDeclaration();
      setState(791);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 88, _ctx)) {
      case 1: {
        setState(790);
        match(JavaLabeledParser::SEMI);
        break;
      }

      default:
        break;
      }
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::AnnotationTypeElementRest2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(793);
      interfaceDeclaration();
      setState(795);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 89, _ctx)) {
      case 1: {
        setState(794);
        match(JavaLabeledParser::SEMI);
        break;
      }

      default:
        break;
      }
      break;
    }

    case 4: {
      _localctx = _tracker.createInstance<JavaLabeledParser::AnnotationTypeElementRest3Context>(_localctx);
      enterOuterAlt(_localctx, 4);
      setState(797);
      enumDeclaration();
      setState(799);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 90, _ctx)) {
      case 1: {
        setState(798);
        match(JavaLabeledParser::SEMI);
        break;
      }

      default:
        break;
      }
      break;
    }

    case 5: {
      _localctx = _tracker.createInstance<JavaLabeledParser::AnnotationTypeElementRest4Context>(_localctx);
      enterOuterAlt(_localctx, 5);
      setState(801);
      annotationTypeDeclaration();
      setState(803);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 91, _ctx)) {
      case 1: {
        setState(802);
        match(JavaLabeledParser::SEMI);
        break;
      }

      default:
        break;
      }
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationMethodOrConstantRestContext ------------------------------------------------------------------

JavaLabeledParser::AnnotationMethodOrConstantRestContext::AnnotationMethodOrConstantRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::AnnotationMethodOrConstantRestContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAnnotationMethodOrConstantRest;
}

void JavaLabeledParser::AnnotationMethodOrConstantRestContext::copyFrom(AnnotationMethodOrConstantRestContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- AnnotationMethodOrConstantRest0Context ------------------------------------------------------------------

JavaLabeledParser::AnnotationMethodRestContext* JavaLabeledParser::AnnotationMethodOrConstantRest0Context::annotationMethodRest() {
  return getRuleContext<JavaLabeledParser::AnnotationMethodRestContext>(0);
}

JavaLabeledParser::AnnotationMethodOrConstantRest0Context::AnnotationMethodOrConstantRest0Context(AnnotationMethodOrConstantRestContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::AnnotationMethodOrConstantRest0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationMethodOrConstantRest0(this);
}
void JavaLabeledParser::AnnotationMethodOrConstantRest0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationMethodOrConstantRest0(this);
}

antlrcpp::Any JavaLabeledParser::AnnotationMethodOrConstantRest0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationMethodOrConstantRest0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationMethodOrConstantRest1Context ------------------------------------------------------------------

JavaLabeledParser::AnnotationConstantRestContext* JavaLabeledParser::AnnotationMethodOrConstantRest1Context::annotationConstantRest() {
  return getRuleContext<JavaLabeledParser::AnnotationConstantRestContext>(0);
}

JavaLabeledParser::AnnotationMethodOrConstantRest1Context::AnnotationMethodOrConstantRest1Context(AnnotationMethodOrConstantRestContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::AnnotationMethodOrConstantRest1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationMethodOrConstantRest1(this);
}
void JavaLabeledParser::AnnotationMethodOrConstantRest1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationMethodOrConstantRest1(this);
}

antlrcpp::Any JavaLabeledParser::AnnotationMethodOrConstantRest1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationMethodOrConstantRest1(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::AnnotationMethodOrConstantRestContext* JavaLabeledParser::annotationMethodOrConstantRest() {
  AnnotationMethodOrConstantRestContext *_localctx = _tracker.createInstance<AnnotationMethodOrConstantRestContext>(_ctx, getState());
  enterRule(_localctx, 120, JavaLabeledParser::RuleAnnotationMethodOrConstantRest);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(809);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 93, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::AnnotationMethodOrConstantRest0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(807);
      annotationMethodRest();
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::AnnotationMethodOrConstantRest1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(808);
      annotationConstantRest();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationMethodRestContext ------------------------------------------------------------------

JavaLabeledParser::AnnotationMethodRestContext::AnnotationMethodRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::AnnotationMethodRestContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationMethodRestContext::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::AnnotationMethodRestContext::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::DefaultValueContext* JavaLabeledParser::AnnotationMethodRestContext::defaultValue() {
  return getRuleContext<JavaLabeledParser::DefaultValueContext>(0);
}


size_t JavaLabeledParser::AnnotationMethodRestContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAnnotationMethodRest;
}

void JavaLabeledParser::AnnotationMethodRestContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationMethodRest(this);
}

void JavaLabeledParser::AnnotationMethodRestContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationMethodRest(this);
}


antlrcpp::Any JavaLabeledParser::AnnotationMethodRestContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationMethodRest(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::AnnotationMethodRestContext* JavaLabeledParser::annotationMethodRest() {
  AnnotationMethodRestContext *_localctx = _tracker.createInstance<AnnotationMethodRestContext>(_ctx, getState());
  enterRule(_localctx, 122, JavaLabeledParser::RuleAnnotationMethodRest);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(811);
    match(JavaLabeledParser::IDENTIFIER);
    setState(812);
    match(JavaLabeledParser::LPAREN);
    setState(813);
    match(JavaLabeledParser::RPAREN);
    setState(815);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::DEFAULT) {
      setState(814);
      defaultValue();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationConstantRestContext ------------------------------------------------------------------

JavaLabeledParser::AnnotationConstantRestContext::AnnotationConstantRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::VariableDeclaratorsContext* JavaLabeledParser::AnnotationConstantRestContext::variableDeclarators() {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorsContext>(0);
}


size_t JavaLabeledParser::AnnotationConstantRestContext::getRuleIndex() const {
  return JavaLabeledParser::RuleAnnotationConstantRest;
}

void JavaLabeledParser::AnnotationConstantRestContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationConstantRest(this);
}

void JavaLabeledParser::AnnotationConstantRestContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationConstantRest(this);
}


antlrcpp::Any JavaLabeledParser::AnnotationConstantRestContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitAnnotationConstantRest(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::AnnotationConstantRestContext* JavaLabeledParser::annotationConstantRest() {
  AnnotationConstantRestContext *_localctx = _tracker.createInstance<AnnotationConstantRestContext>(_ctx, getState());
  enterRule(_localctx, 124, JavaLabeledParser::RuleAnnotationConstantRest);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(817);
    variableDeclarators();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- DefaultValueContext ------------------------------------------------------------------

JavaLabeledParser::DefaultValueContext::DefaultValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::DefaultValueContext::DEFAULT() {
  return getToken(JavaLabeledParser::DEFAULT, 0);
}

JavaLabeledParser::ElementValueContext* JavaLabeledParser::DefaultValueContext::elementValue() {
  return getRuleContext<JavaLabeledParser::ElementValueContext>(0);
}


size_t JavaLabeledParser::DefaultValueContext::getRuleIndex() const {
  return JavaLabeledParser::RuleDefaultValue;
}

void JavaLabeledParser::DefaultValueContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterDefaultValue(this);
}

void JavaLabeledParser::DefaultValueContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitDefaultValue(this);
}


antlrcpp::Any JavaLabeledParser::DefaultValueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitDefaultValue(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::DefaultValueContext* JavaLabeledParser::defaultValue() {
  DefaultValueContext *_localctx = _tracker.createInstance<DefaultValueContext>(_ctx, getState());
  enterRule(_localctx, 126, JavaLabeledParser::RuleDefaultValue);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(819);
    match(JavaLabeledParser::DEFAULT);
    setState(820);
    elementValue();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- BlockContext ------------------------------------------------------------------

JavaLabeledParser::BlockContext::BlockContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::BlockContext::LBRACE() {
  return getToken(JavaLabeledParser::LBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::BlockContext::RBRACE() {
  return getToken(JavaLabeledParser::RBRACE, 0);
}

std::vector<JavaLabeledParser::BlockStatementContext *> JavaLabeledParser::BlockContext::blockStatement() {
  return getRuleContexts<JavaLabeledParser::BlockStatementContext>();
}

JavaLabeledParser::BlockStatementContext* JavaLabeledParser::BlockContext::blockStatement(size_t i) {
  return getRuleContext<JavaLabeledParser::BlockStatementContext>(i);
}


size_t JavaLabeledParser::BlockContext::getRuleIndex() const {
  return JavaLabeledParser::RuleBlock;
}

void JavaLabeledParser::BlockContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlock(this);
}

void JavaLabeledParser::BlockContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlock(this);
}


antlrcpp::Any JavaLabeledParser::BlockContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitBlock(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::BlockContext* JavaLabeledParser::block() {
  BlockContext *_localctx = _tracker.createInstance<BlockContext>(_ctx, getState());
  enterRule(_localctx, 128, JavaLabeledParser::RuleBlock);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(822);
    match(JavaLabeledParser::LBRACE);
    setState(826);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::ABSTRACT)
      | (1ULL << JavaLabeledParser::ASSERT)
      | (1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BREAK)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::CLASS)
      | (1ULL << JavaLabeledParser::CONTINUE)
      | (1ULL << JavaLabeledParser::DO)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::FINAL)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::FOR)
      | (1ULL << JavaLabeledParser::IF)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::INTERFACE)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NEW)
      | (1ULL << JavaLabeledParser::PRIVATE)
      | (1ULL << JavaLabeledParser::PROTECTED)
      | (1ULL << JavaLabeledParser::PUBLIC)
      | (1ULL << JavaLabeledParser::RETURN)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::STATIC)
      | (1ULL << JavaLabeledParser::STRICTFP)
      | (1ULL << JavaLabeledParser::SUPER)
      | (1ULL << JavaLabeledParser::SWITCH)
      | (1ULL << JavaLabeledParser::SYNCHRONIZED)
      | (1ULL << JavaLabeledParser::THIS)
      | (1ULL << JavaLabeledParser::THROW)
      | (1ULL << JavaLabeledParser::TRY)
      | (1ULL << JavaLabeledParser::VOID)
      | (1ULL << JavaLabeledParser::WHILE)
      | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_LITERAL)
      | (1ULL << JavaLabeledParser::OCT_LITERAL)
      | (1ULL << JavaLabeledParser::BINARY_LITERAL)
      | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::BOOL_LITERAL)
      | (1ULL << JavaLabeledParser::CHAR_LITERAL)
      | (1ULL << JavaLabeledParser::STRING_LITERAL)
      | (1ULL << JavaLabeledParser::NULL_LITERAL)
      | (1ULL << JavaLabeledParser::LPAREN)
      | (1ULL << JavaLabeledParser::LBRACE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaLabeledParser::SEMI - 67))
      | (1ULL << (JavaLabeledParser::LT - 67))
      | (1ULL << (JavaLabeledParser::BANG - 67))
      | (1ULL << (JavaLabeledParser::TILDE - 67))
      | (1ULL << (JavaLabeledParser::INC - 67))
      | (1ULL << (JavaLabeledParser::DEC - 67))
      | (1ULL << (JavaLabeledParser::ADD - 67))
      | (1ULL << (JavaLabeledParser::SUB - 67))
      | (1ULL << (JavaLabeledParser::AT - 67))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 67)))) != 0)) {
      setState(823);
      blockStatement();
      setState(828);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(829);
    match(JavaLabeledParser::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- BlockStatementContext ------------------------------------------------------------------

JavaLabeledParser::BlockStatementContext::BlockStatementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::BlockStatementContext::getRuleIndex() const {
  return JavaLabeledParser::RuleBlockStatement;
}

void JavaLabeledParser::BlockStatementContext::copyFrom(BlockStatementContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- BlockStatement1Context ------------------------------------------------------------------

JavaLabeledParser::StatementContext* JavaLabeledParser::BlockStatement1Context::statement() {
  return getRuleContext<JavaLabeledParser::StatementContext>(0);
}

JavaLabeledParser::BlockStatement1Context::BlockStatement1Context(BlockStatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::BlockStatement1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlockStatement1(this);
}
void JavaLabeledParser::BlockStatement1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlockStatement1(this);
}

antlrcpp::Any JavaLabeledParser::BlockStatement1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitBlockStatement1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- BlockStatement0Context ------------------------------------------------------------------

JavaLabeledParser::LocalVariableDeclarationContext* JavaLabeledParser::BlockStatement0Context::localVariableDeclaration() {
  return getRuleContext<JavaLabeledParser::LocalVariableDeclarationContext>(0);
}

tree::TerminalNode* JavaLabeledParser::BlockStatement0Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::BlockStatement0Context::BlockStatement0Context(BlockStatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::BlockStatement0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlockStatement0(this);
}
void JavaLabeledParser::BlockStatement0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlockStatement0(this);
}

antlrcpp::Any JavaLabeledParser::BlockStatement0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitBlockStatement0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- BlockStatement2Context ------------------------------------------------------------------

JavaLabeledParser::LocalTypeDeclarationContext* JavaLabeledParser::BlockStatement2Context::localTypeDeclaration() {
  return getRuleContext<JavaLabeledParser::LocalTypeDeclarationContext>(0);
}

JavaLabeledParser::BlockStatement2Context::BlockStatement2Context(BlockStatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::BlockStatement2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlockStatement2(this);
}
void JavaLabeledParser::BlockStatement2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlockStatement2(this);
}

antlrcpp::Any JavaLabeledParser::BlockStatement2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitBlockStatement2(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::BlockStatementContext* JavaLabeledParser::blockStatement() {
  BlockStatementContext *_localctx = _tracker.createInstance<BlockStatementContext>(_ctx, getState());
  enterRule(_localctx, 130, JavaLabeledParser::RuleBlockStatement);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(836);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 96, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::BlockStatement0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(831);
      localVariableDeclaration();
      setState(832);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::BlockStatement1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(834);
      statement();
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::BlockStatement2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(835);
      localTypeDeclaration();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LocalVariableDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::LocalVariableDeclarationContext::LocalVariableDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::LocalVariableDeclarationContext::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

JavaLabeledParser::VariableDeclaratorsContext* JavaLabeledParser::LocalVariableDeclarationContext::variableDeclarators() {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorsContext>(0);
}

std::vector<JavaLabeledParser::VariableModifierContext *> JavaLabeledParser::LocalVariableDeclarationContext::variableModifier() {
  return getRuleContexts<JavaLabeledParser::VariableModifierContext>();
}

JavaLabeledParser::VariableModifierContext* JavaLabeledParser::LocalVariableDeclarationContext::variableModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::VariableModifierContext>(i);
}


size_t JavaLabeledParser::LocalVariableDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleLocalVariableDeclaration;
}

void JavaLabeledParser::LocalVariableDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLocalVariableDeclaration(this);
}

void JavaLabeledParser::LocalVariableDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLocalVariableDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::LocalVariableDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLocalVariableDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::LocalVariableDeclarationContext* JavaLabeledParser::localVariableDeclaration() {
  LocalVariableDeclarationContext *_localctx = _tracker.createInstance<LocalVariableDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 132, JavaLabeledParser::RuleLocalVariableDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(841);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 97, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(838);
        variableModifier(); 
      }
      setState(843);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 97, _ctx);
    }
    setState(844);
    typeType();
    setState(845);
    variableDeclarators();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LocalTypeDeclarationContext ------------------------------------------------------------------

JavaLabeledParser::LocalTypeDeclarationContext::LocalTypeDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::ClassDeclarationContext* JavaLabeledParser::LocalTypeDeclarationContext::classDeclaration() {
  return getRuleContext<JavaLabeledParser::ClassDeclarationContext>(0);
}

JavaLabeledParser::InterfaceDeclarationContext* JavaLabeledParser::LocalTypeDeclarationContext::interfaceDeclaration() {
  return getRuleContext<JavaLabeledParser::InterfaceDeclarationContext>(0);
}

std::vector<JavaLabeledParser::ClassOrInterfaceModifierContext *> JavaLabeledParser::LocalTypeDeclarationContext::classOrInterfaceModifier() {
  return getRuleContexts<JavaLabeledParser::ClassOrInterfaceModifierContext>();
}

JavaLabeledParser::ClassOrInterfaceModifierContext* JavaLabeledParser::LocalTypeDeclarationContext::classOrInterfaceModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::ClassOrInterfaceModifierContext>(i);
}

tree::TerminalNode* JavaLabeledParser::LocalTypeDeclarationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}


size_t JavaLabeledParser::LocalTypeDeclarationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleLocalTypeDeclaration;
}

void JavaLabeledParser::LocalTypeDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLocalTypeDeclaration(this);
}

void JavaLabeledParser::LocalTypeDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLocalTypeDeclaration(this);
}


antlrcpp::Any JavaLabeledParser::LocalTypeDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLocalTypeDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::LocalTypeDeclarationContext* JavaLabeledParser::localTypeDeclaration() {
  LocalTypeDeclarationContext *_localctx = _tracker.createInstance<LocalTypeDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 134, JavaLabeledParser::RuleLocalTypeDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(858);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::ABSTRACT:
      case JavaLabeledParser::CLASS:
      case JavaLabeledParser::FINAL:
      case JavaLabeledParser::INTERFACE:
      case JavaLabeledParser::PRIVATE:
      case JavaLabeledParser::PROTECTED:
      case JavaLabeledParser::PUBLIC:
      case JavaLabeledParser::STATIC:
      case JavaLabeledParser::STRICTFP:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(850);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << JavaLabeledParser::ABSTRACT)
          | (1ULL << JavaLabeledParser::FINAL)
          | (1ULL << JavaLabeledParser::PRIVATE)
          | (1ULL << JavaLabeledParser::PROTECTED)
          | (1ULL << JavaLabeledParser::PUBLIC)
          | (1ULL << JavaLabeledParser::STATIC)
          | (1ULL << JavaLabeledParser::STRICTFP))) != 0) || _la == JavaLabeledParser::AT

        || _la == JavaLabeledParser::IDENTIFIER) {
          setState(847);
          classOrInterfaceModifier();
          setState(852);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        setState(855);
        _errHandler->sync(this);
        switch (_input->LA(1)) {
          case JavaLabeledParser::CLASS: {
            setState(853);
            classDeclaration();
            break;
          }

          case JavaLabeledParser::INTERFACE: {
            setState(854);
            interfaceDeclaration();
            break;
          }

        default:
          throw NoViableAltException(this);
        }
        break;
      }

      case JavaLabeledParser::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(857);
        match(JavaLabeledParser::SEMI);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- StatementContext ------------------------------------------------------------------

JavaLabeledParser::StatementContext::StatementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::StatementContext::getRuleIndex() const {
  return JavaLabeledParser::RuleStatement;
}

void JavaLabeledParser::StatementContext::copyFrom(StatementContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Statement14Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement14Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::Statement14Context::Statement14Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement14Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement14(this);
}
void JavaLabeledParser::Statement14Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement14(this);
}

antlrcpp::Any JavaLabeledParser::Statement14Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement14(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement15Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement15Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Statement15Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

JavaLabeledParser::Statement15Context::Statement15Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement15Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement15(this);
}
void JavaLabeledParser::Statement15Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement15(this);
}

antlrcpp::Any JavaLabeledParser::Statement15Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement15(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement12Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement12Context::BREAK() {
  return getToken(JavaLabeledParser::BREAK, 0);
}

tree::TerminalNode* JavaLabeledParser::Statement12Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

tree::TerminalNode* JavaLabeledParser::Statement12Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::Statement12Context::Statement12Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement12Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement12(this);
}
void JavaLabeledParser::Statement12Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement12(this);
}

antlrcpp::Any JavaLabeledParser::Statement12Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement12(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement13Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement13Context::CONTINUE() {
  return getToken(JavaLabeledParser::CONTINUE, 0);
}

tree::TerminalNode* JavaLabeledParser::Statement13Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

tree::TerminalNode* JavaLabeledParser::Statement13Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::Statement13Context::Statement13Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement13Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement13(this);
}
void JavaLabeledParser::Statement13Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement13(this);
}

antlrcpp::Any JavaLabeledParser::Statement13Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement13(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement9Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement9Context::SYNCHRONIZED() {
  return getToken(JavaLabeledParser::SYNCHRONIZED, 0);
}

JavaLabeledParser::ParExpressionContext* JavaLabeledParser::Statement9Context::parExpression() {
  return getRuleContext<JavaLabeledParser::ParExpressionContext>(0);
}

JavaLabeledParser::BlockContext* JavaLabeledParser::Statement9Context::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

JavaLabeledParser::Statement9Context::Statement9Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement9Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement9(this);
}
void JavaLabeledParser::Statement9Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement9(this);
}

antlrcpp::Any JavaLabeledParser::Statement9Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement9(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement7Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement7Context::TRY() {
  return getToken(JavaLabeledParser::TRY, 0);
}

JavaLabeledParser::ResourceSpecificationContext* JavaLabeledParser::Statement7Context::resourceSpecification() {
  return getRuleContext<JavaLabeledParser::ResourceSpecificationContext>(0);
}

JavaLabeledParser::BlockContext* JavaLabeledParser::Statement7Context::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

std::vector<JavaLabeledParser::CatchClauseContext *> JavaLabeledParser::Statement7Context::catchClause() {
  return getRuleContexts<JavaLabeledParser::CatchClauseContext>();
}

JavaLabeledParser::CatchClauseContext* JavaLabeledParser::Statement7Context::catchClause(size_t i) {
  return getRuleContext<JavaLabeledParser::CatchClauseContext>(i);
}

JavaLabeledParser::FinallyBlockContext* JavaLabeledParser::Statement7Context::finallyBlock() {
  return getRuleContext<JavaLabeledParser::FinallyBlockContext>(0);
}

JavaLabeledParser::Statement7Context::Statement7Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement7Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement7(this);
}
void JavaLabeledParser::Statement7Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement7(this);
}

antlrcpp::Any JavaLabeledParser::Statement7Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement7(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement16Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement16Context::COLON() {
  return getToken(JavaLabeledParser::COLON, 0);
}

JavaLabeledParser::StatementContext* JavaLabeledParser::Statement16Context::statement() {
  return getRuleContext<JavaLabeledParser::StatementContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Statement16Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::Statement16Context::Statement16Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement16Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement16(this);
}
void JavaLabeledParser::Statement16Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement16(this);
}

antlrcpp::Any JavaLabeledParser::Statement16Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement16(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement8Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement8Context::SWITCH() {
  return getToken(JavaLabeledParser::SWITCH, 0);
}

JavaLabeledParser::ParExpressionContext* JavaLabeledParser::Statement8Context::parExpression() {
  return getRuleContext<JavaLabeledParser::ParExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Statement8Context::LBRACE() {
  return getToken(JavaLabeledParser::LBRACE, 0);
}

tree::TerminalNode* JavaLabeledParser::Statement8Context::RBRACE() {
  return getToken(JavaLabeledParser::RBRACE, 0);
}

std::vector<JavaLabeledParser::SwitchBlockStatementGroupContext *> JavaLabeledParser::Statement8Context::switchBlockStatementGroup() {
  return getRuleContexts<JavaLabeledParser::SwitchBlockStatementGroupContext>();
}

JavaLabeledParser::SwitchBlockStatementGroupContext* JavaLabeledParser::Statement8Context::switchBlockStatementGroup(size_t i) {
  return getRuleContext<JavaLabeledParser::SwitchBlockStatementGroupContext>(i);
}

std::vector<JavaLabeledParser::SwitchLabelContext *> JavaLabeledParser::Statement8Context::switchLabel() {
  return getRuleContexts<JavaLabeledParser::SwitchLabelContext>();
}

JavaLabeledParser::SwitchLabelContext* JavaLabeledParser::Statement8Context::switchLabel(size_t i) {
  return getRuleContext<JavaLabeledParser::SwitchLabelContext>(i);
}

JavaLabeledParser::Statement8Context::Statement8Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement8Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement8(this);
}
void JavaLabeledParser::Statement8Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement8(this);
}

antlrcpp::Any JavaLabeledParser::Statement8Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement8(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement5Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement5Context::DO() {
  return getToken(JavaLabeledParser::DO, 0);
}

JavaLabeledParser::StatementContext* JavaLabeledParser::Statement5Context::statement() {
  return getRuleContext<JavaLabeledParser::StatementContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Statement5Context::WHILE() {
  return getToken(JavaLabeledParser::WHILE, 0);
}

JavaLabeledParser::ParExpressionContext* JavaLabeledParser::Statement5Context::parExpression() {
  return getRuleContext<JavaLabeledParser::ParExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Statement5Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::Statement5Context::Statement5Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement5(this);
}
void JavaLabeledParser::Statement5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement5(this);
}

antlrcpp::Any JavaLabeledParser::Statement5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement6Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement6Context::TRY() {
  return getToken(JavaLabeledParser::TRY, 0);
}

JavaLabeledParser::BlockContext* JavaLabeledParser::Statement6Context::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

JavaLabeledParser::FinallyBlockContext* JavaLabeledParser::Statement6Context::finallyBlock() {
  return getRuleContext<JavaLabeledParser::FinallyBlockContext>(0);
}

std::vector<JavaLabeledParser::CatchClauseContext *> JavaLabeledParser::Statement6Context::catchClause() {
  return getRuleContexts<JavaLabeledParser::CatchClauseContext>();
}

JavaLabeledParser::CatchClauseContext* JavaLabeledParser::Statement6Context::catchClause(size_t i) {
  return getRuleContext<JavaLabeledParser::CatchClauseContext>(i);
}

JavaLabeledParser::Statement6Context::Statement6Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement6(this);
}
void JavaLabeledParser::Statement6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement6(this);
}

antlrcpp::Any JavaLabeledParser::Statement6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement3Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement3Context::FOR() {
  return getToken(JavaLabeledParser::FOR, 0);
}

tree::TerminalNode* JavaLabeledParser::Statement3Context::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

JavaLabeledParser::ForControlContext* JavaLabeledParser::Statement3Context::forControl() {
  return getRuleContext<JavaLabeledParser::ForControlContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Statement3Context::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::StatementContext* JavaLabeledParser::Statement3Context::statement() {
  return getRuleContext<JavaLabeledParser::StatementContext>(0);
}

JavaLabeledParser::Statement3Context::Statement3Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement3(this);
}
void JavaLabeledParser::Statement3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement3(this);
}

antlrcpp::Any JavaLabeledParser::Statement3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement4Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement4Context::WHILE() {
  return getToken(JavaLabeledParser::WHILE, 0);
}

JavaLabeledParser::ParExpressionContext* JavaLabeledParser::Statement4Context::parExpression() {
  return getRuleContext<JavaLabeledParser::ParExpressionContext>(0);
}

JavaLabeledParser::StatementContext* JavaLabeledParser::Statement4Context::statement() {
  return getRuleContext<JavaLabeledParser::StatementContext>(0);
}

JavaLabeledParser::Statement4Context::Statement4Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement4(this);
}
void JavaLabeledParser::Statement4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement4(this);
}

antlrcpp::Any JavaLabeledParser::Statement4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement1Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement1Context::ASSERT() {
  return getToken(JavaLabeledParser::ASSERT, 0);
}

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Statement1Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Statement1Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Statement1Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

tree::TerminalNode* JavaLabeledParser::Statement1Context::COLON() {
  return getToken(JavaLabeledParser::COLON, 0);
}

JavaLabeledParser::Statement1Context::Statement1Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement1(this);
}
void JavaLabeledParser::Statement1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement1(this);
}

antlrcpp::Any JavaLabeledParser::Statement1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement2Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement2Context::IF() {
  return getToken(JavaLabeledParser::IF, 0);
}

JavaLabeledParser::ParExpressionContext* JavaLabeledParser::Statement2Context::parExpression() {
  return getRuleContext<JavaLabeledParser::ParExpressionContext>(0);
}

std::vector<JavaLabeledParser::StatementContext *> JavaLabeledParser::Statement2Context::statement() {
  return getRuleContexts<JavaLabeledParser::StatementContext>();
}

JavaLabeledParser::StatementContext* JavaLabeledParser::Statement2Context::statement(size_t i) {
  return getRuleContext<JavaLabeledParser::StatementContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Statement2Context::ELSE() {
  return getToken(JavaLabeledParser::ELSE, 0);
}

JavaLabeledParser::Statement2Context::Statement2Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement2(this);
}
void JavaLabeledParser::Statement2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement2(this);
}

antlrcpp::Any JavaLabeledParser::Statement2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement0Context ------------------------------------------------------------------

JavaLabeledParser::BlockContext* JavaLabeledParser::Statement0Context::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

JavaLabeledParser::Statement0Context::Statement0Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement0(this);
}
void JavaLabeledParser::Statement0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement0(this);
}

antlrcpp::Any JavaLabeledParser::Statement0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement10Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement10Context::RETURN() {
  return getToken(JavaLabeledParser::RETURN, 0);
}

tree::TerminalNode* JavaLabeledParser::Statement10Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Statement10Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

JavaLabeledParser::Statement10Context::Statement10Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement10Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement10(this);
}
void JavaLabeledParser::Statement10Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement10(this);
}

antlrcpp::Any JavaLabeledParser::Statement10Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement10(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement11Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Statement11Context::THROW() {
  return getToken(JavaLabeledParser::THROW, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Statement11Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Statement11Context::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}

JavaLabeledParser::Statement11Context::Statement11Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Statement11Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement11(this);
}
void JavaLabeledParser::Statement11Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement11(this);
}

antlrcpp::Any JavaLabeledParser::Statement11Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitStatement11(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::StatementContext* JavaLabeledParser::statement() {
  StatementContext *_localctx = _tracker.createInstance<StatementContext>(_ctx, getState());
  enterRule(_localctx, 136, JavaLabeledParser::RuleStatement);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    setState(964);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 113, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(860);
      antlrcpp::downCast<Statement0Context *>(_localctx)->blockLabel = block();
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(861);
      match(JavaLabeledParser::ASSERT);
      setState(862);
      expression(0);
      setState(865);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::COLON) {
        setState(863);
        match(JavaLabeledParser::COLON);
        setState(864);
        expression(0);
      }
      setState(867);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(869);
      match(JavaLabeledParser::IF);
      setState(870);
      parExpression();
      setState(871);
      statement();
      setState(874);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 102, _ctx)) {
      case 1: {
        setState(872);
        match(JavaLabeledParser::ELSE);
        setState(873);
        statement();
        break;
      }

      default:
        break;
      }
      break;
    }

    case 4: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement3Context>(_localctx);
      enterOuterAlt(_localctx, 4);
      setState(876);
      match(JavaLabeledParser::FOR);
      setState(877);
      match(JavaLabeledParser::LPAREN);
      setState(878);
      forControl();
      setState(879);
      match(JavaLabeledParser::RPAREN);
      setState(880);
      statement();
      break;
    }

    case 5: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement4Context>(_localctx);
      enterOuterAlt(_localctx, 5);
      setState(882);
      match(JavaLabeledParser::WHILE);
      setState(883);
      parExpression();
      setState(884);
      statement();
      break;
    }

    case 6: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement5Context>(_localctx);
      enterOuterAlt(_localctx, 6);
      setState(886);
      match(JavaLabeledParser::DO);
      setState(887);
      statement();
      setState(888);
      match(JavaLabeledParser::WHILE);
      setState(889);
      parExpression();
      setState(890);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 7: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement6Context>(_localctx);
      enterOuterAlt(_localctx, 7);
      setState(892);
      match(JavaLabeledParser::TRY);
      setState(893);
      block();
      setState(903);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case JavaLabeledParser::CATCH: {
          setState(895); 
          _errHandler->sync(this);
          _la = _input->LA(1);
          do {
            setState(894);
            catchClause();
            setState(897); 
            _errHandler->sync(this);
            _la = _input->LA(1);
          } while (_la == JavaLabeledParser::CATCH);
          setState(900);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == JavaLabeledParser::FINALLY) {
            setState(899);
            finallyBlock();
          }
          break;
        }

        case JavaLabeledParser::FINALLY: {
          setState(902);
          finallyBlock();
          break;
        }

      default:
        throw NoViableAltException(this);
      }
      break;
    }

    case 8: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement7Context>(_localctx);
      enterOuterAlt(_localctx, 8);
      setState(905);
      match(JavaLabeledParser::TRY);
      setState(906);
      resourceSpecification();
      setState(907);
      block();
      setState(911);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == JavaLabeledParser::CATCH) {
        setState(908);
        catchClause();
        setState(913);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(915);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::FINALLY) {
        setState(914);
        finallyBlock();
      }
      break;
    }

    case 9: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement8Context>(_localctx);
      enterOuterAlt(_localctx, 9);
      setState(917);
      match(JavaLabeledParser::SWITCH);
      setState(918);
      parExpression();
      setState(919);
      match(JavaLabeledParser::LBRACE);
      setState(923);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 108, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(920);
          switchBlockStatementGroup(); 
        }
        setState(925);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 108, _ctx);
      }
      setState(929);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == JavaLabeledParser::CASE

      || _la == JavaLabeledParser::DEFAULT) {
        setState(926);
        switchLabel();
        setState(931);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(932);
      match(JavaLabeledParser::RBRACE);
      break;
    }

    case 10: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement9Context>(_localctx);
      enterOuterAlt(_localctx, 10);
      setState(934);
      match(JavaLabeledParser::SYNCHRONIZED);
      setState(935);
      parExpression();
      setState(936);
      block();
      break;
    }

    case 11: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement10Context>(_localctx);
      enterOuterAlt(_localctx, 11);
      setState(938);
      match(JavaLabeledParser::RETURN);
      setState(940);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
        | (1ULL << JavaLabeledParser::BYTE)
        | (1ULL << JavaLabeledParser::CHAR)
        | (1ULL << JavaLabeledParser::DOUBLE)
        | (1ULL << JavaLabeledParser::FLOAT)
        | (1ULL << JavaLabeledParser::INT)
        | (1ULL << JavaLabeledParser::LONG)
        | (1ULL << JavaLabeledParser::NEW)
        | (1ULL << JavaLabeledParser::SHORT)
        | (1ULL << JavaLabeledParser::SUPER)
        | (1ULL << JavaLabeledParser::THIS)
        | (1ULL << JavaLabeledParser::VOID)
        | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
        | (1ULL << JavaLabeledParser::HEX_LITERAL)
        | (1ULL << JavaLabeledParser::OCT_LITERAL)
        | (1ULL << JavaLabeledParser::BINARY_LITERAL)
        | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
        | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
        | (1ULL << JavaLabeledParser::BOOL_LITERAL)
        | (1ULL << JavaLabeledParser::CHAR_LITERAL)
        | (1ULL << JavaLabeledParser::STRING_LITERAL)
        | (1ULL << JavaLabeledParser::NULL_LITERAL)
        | (1ULL << JavaLabeledParser::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
        | (1ULL << (JavaLabeledParser::BANG - 72))
        | (1ULL << (JavaLabeledParser::TILDE - 72))
        | (1ULL << (JavaLabeledParser::INC - 72))
        | (1ULL << (JavaLabeledParser::DEC - 72))
        | (1ULL << (JavaLabeledParser::ADD - 72))
        | (1ULL << (JavaLabeledParser::SUB - 72))
        | (1ULL << (JavaLabeledParser::AT - 72))
        | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
        setState(939);
        expression(0);
      }
      setState(942);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 12: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement11Context>(_localctx);
      enterOuterAlt(_localctx, 12);
      setState(943);
      match(JavaLabeledParser::THROW);
      setState(944);
      expression(0);
      setState(945);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 13: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement12Context>(_localctx);
      enterOuterAlt(_localctx, 13);
      setState(947);
      match(JavaLabeledParser::BREAK);
      setState(949);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::IDENTIFIER) {
        setState(948);
        match(JavaLabeledParser::IDENTIFIER);
      }
      setState(951);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 14: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement13Context>(_localctx);
      enterOuterAlt(_localctx, 14);
      setState(952);
      match(JavaLabeledParser::CONTINUE);
      setState(954);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::IDENTIFIER) {
        setState(953);
        match(JavaLabeledParser::IDENTIFIER);
      }
      setState(956);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 15: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement14Context>(_localctx);
      enterOuterAlt(_localctx, 15);
      setState(957);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 16: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement15Context>(_localctx);
      enterOuterAlt(_localctx, 16);
      setState(958);
      antlrcpp::downCast<Statement15Context *>(_localctx)->statementExpression = expression(0);
      setState(959);
      match(JavaLabeledParser::SEMI);
      break;
    }

    case 17: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Statement16Context>(_localctx);
      enterOuterAlt(_localctx, 17);
      setState(961);
      antlrcpp::downCast<Statement16Context *>(_localctx)->identifierLabel = match(JavaLabeledParser::IDENTIFIER);
      setState(962);
      match(JavaLabeledParser::COLON);
      setState(963);
      statement();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- CatchClauseContext ------------------------------------------------------------------

JavaLabeledParser::CatchClauseContext::CatchClauseContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::CatchClauseContext::CATCH() {
  return getToken(JavaLabeledParser::CATCH, 0);
}

tree::TerminalNode* JavaLabeledParser::CatchClauseContext::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

JavaLabeledParser::CatchTypeContext* JavaLabeledParser::CatchClauseContext::catchType() {
  return getRuleContext<JavaLabeledParser::CatchTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::CatchClauseContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

tree::TerminalNode* JavaLabeledParser::CatchClauseContext::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::BlockContext* JavaLabeledParser::CatchClauseContext::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

std::vector<JavaLabeledParser::VariableModifierContext *> JavaLabeledParser::CatchClauseContext::variableModifier() {
  return getRuleContexts<JavaLabeledParser::VariableModifierContext>();
}

JavaLabeledParser::VariableModifierContext* JavaLabeledParser::CatchClauseContext::variableModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::VariableModifierContext>(i);
}


size_t JavaLabeledParser::CatchClauseContext::getRuleIndex() const {
  return JavaLabeledParser::RuleCatchClause;
}

void JavaLabeledParser::CatchClauseContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCatchClause(this);
}

void JavaLabeledParser::CatchClauseContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCatchClause(this);
}


antlrcpp::Any JavaLabeledParser::CatchClauseContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitCatchClause(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::CatchClauseContext* JavaLabeledParser::catchClause() {
  CatchClauseContext *_localctx = _tracker.createInstance<CatchClauseContext>(_ctx, getState());
  enterRule(_localctx, 138, JavaLabeledParser::RuleCatchClause);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(966);
    match(JavaLabeledParser::CATCH);
    setState(967);
    match(JavaLabeledParser::LPAREN);
    setState(971);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 114, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(968);
        variableModifier(); 
      }
      setState(973);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 114, _ctx);
    }
    setState(974);
    catchType();
    setState(975);
    match(JavaLabeledParser::IDENTIFIER);
    setState(976);
    match(JavaLabeledParser::RPAREN);
    setState(977);
    block();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- CatchTypeContext ------------------------------------------------------------------

JavaLabeledParser::CatchTypeContext::CatchTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::QualifiedNameContext *> JavaLabeledParser::CatchTypeContext::qualifiedName() {
  return getRuleContexts<JavaLabeledParser::QualifiedNameContext>();
}

JavaLabeledParser::QualifiedNameContext* JavaLabeledParser::CatchTypeContext::qualifiedName(size_t i) {
  return getRuleContext<JavaLabeledParser::QualifiedNameContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::CatchTypeContext::BITOR() {
  return getTokens(JavaLabeledParser::BITOR);
}

tree::TerminalNode* JavaLabeledParser::CatchTypeContext::BITOR(size_t i) {
  return getToken(JavaLabeledParser::BITOR, i);
}


size_t JavaLabeledParser::CatchTypeContext::getRuleIndex() const {
  return JavaLabeledParser::RuleCatchType;
}

void JavaLabeledParser::CatchTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCatchType(this);
}

void JavaLabeledParser::CatchTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCatchType(this);
}


antlrcpp::Any JavaLabeledParser::CatchTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitCatchType(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::CatchTypeContext* JavaLabeledParser::catchType() {
  CatchTypeContext *_localctx = _tracker.createInstance<CatchTypeContext>(_ctx, getState());
  enterRule(_localctx, 140, JavaLabeledParser::RuleCatchType);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(979);
    qualifiedName();
    setState(984);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::BITOR) {
      setState(980);
      match(JavaLabeledParser::BITOR);
      setState(981);
      qualifiedName();
      setState(986);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FinallyBlockContext ------------------------------------------------------------------

JavaLabeledParser::FinallyBlockContext::FinallyBlockContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::FinallyBlockContext::FINALLY() {
  return getToken(JavaLabeledParser::FINALLY, 0);
}

JavaLabeledParser::BlockContext* JavaLabeledParser::FinallyBlockContext::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}


size_t JavaLabeledParser::FinallyBlockContext::getRuleIndex() const {
  return JavaLabeledParser::RuleFinallyBlock;
}

void JavaLabeledParser::FinallyBlockContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFinallyBlock(this);
}

void JavaLabeledParser::FinallyBlockContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFinallyBlock(this);
}


antlrcpp::Any JavaLabeledParser::FinallyBlockContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitFinallyBlock(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::FinallyBlockContext* JavaLabeledParser::finallyBlock() {
  FinallyBlockContext *_localctx = _tracker.createInstance<FinallyBlockContext>(_ctx, getState());
  enterRule(_localctx, 142, JavaLabeledParser::RuleFinallyBlock);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(987);
    match(JavaLabeledParser::FINALLY);
    setState(988);
    block();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ResourceSpecificationContext ------------------------------------------------------------------

JavaLabeledParser::ResourceSpecificationContext::ResourceSpecificationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ResourceSpecificationContext::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

JavaLabeledParser::ResourcesContext* JavaLabeledParser::ResourceSpecificationContext::resources() {
  return getRuleContext<JavaLabeledParser::ResourcesContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ResourceSpecificationContext::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::ResourceSpecificationContext::SEMI() {
  return getToken(JavaLabeledParser::SEMI, 0);
}


size_t JavaLabeledParser::ResourceSpecificationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleResourceSpecification;
}

void JavaLabeledParser::ResourceSpecificationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterResourceSpecification(this);
}

void JavaLabeledParser::ResourceSpecificationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitResourceSpecification(this);
}


antlrcpp::Any JavaLabeledParser::ResourceSpecificationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitResourceSpecification(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ResourceSpecificationContext* JavaLabeledParser::resourceSpecification() {
  ResourceSpecificationContext *_localctx = _tracker.createInstance<ResourceSpecificationContext>(_ctx, getState());
  enterRule(_localctx, 144, JavaLabeledParser::RuleResourceSpecification);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(990);
    match(JavaLabeledParser::LPAREN);
    setState(991);
    resources();
    setState(993);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::SEMI) {
      setState(992);
      match(JavaLabeledParser::SEMI);
    }
    setState(995);
    match(JavaLabeledParser::RPAREN);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ResourcesContext ------------------------------------------------------------------

JavaLabeledParser::ResourcesContext::ResourcesContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::ResourceContext *> JavaLabeledParser::ResourcesContext::resource() {
  return getRuleContexts<JavaLabeledParser::ResourceContext>();
}

JavaLabeledParser::ResourceContext* JavaLabeledParser::ResourcesContext::resource(size_t i) {
  return getRuleContext<JavaLabeledParser::ResourceContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ResourcesContext::SEMI() {
  return getTokens(JavaLabeledParser::SEMI);
}

tree::TerminalNode* JavaLabeledParser::ResourcesContext::SEMI(size_t i) {
  return getToken(JavaLabeledParser::SEMI, i);
}


size_t JavaLabeledParser::ResourcesContext::getRuleIndex() const {
  return JavaLabeledParser::RuleResources;
}

void JavaLabeledParser::ResourcesContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterResources(this);
}

void JavaLabeledParser::ResourcesContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitResources(this);
}


antlrcpp::Any JavaLabeledParser::ResourcesContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitResources(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ResourcesContext* JavaLabeledParser::resources() {
  ResourcesContext *_localctx = _tracker.createInstance<ResourcesContext>(_ctx, getState());
  enterRule(_localctx, 146, JavaLabeledParser::RuleResources);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(997);
    resource();
    setState(1002);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 117, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(998);
        match(JavaLabeledParser::SEMI);
        setState(999);
        resource(); 
      }
      setState(1004);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 117, _ctx);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ResourceContext ------------------------------------------------------------------

JavaLabeledParser::ResourceContext::ResourceContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::ClassOrInterfaceTypeContext* JavaLabeledParser::ResourceContext::classOrInterfaceType() {
  return getRuleContext<JavaLabeledParser::ClassOrInterfaceTypeContext>(0);
}

JavaLabeledParser::VariableDeclaratorIdContext* JavaLabeledParser::ResourceContext::variableDeclaratorId() {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorIdContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ResourceContext::ASSIGN() {
  return getToken(JavaLabeledParser::ASSIGN, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::ResourceContext::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

std::vector<JavaLabeledParser::VariableModifierContext *> JavaLabeledParser::ResourceContext::variableModifier() {
  return getRuleContexts<JavaLabeledParser::VariableModifierContext>();
}

JavaLabeledParser::VariableModifierContext* JavaLabeledParser::ResourceContext::variableModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::VariableModifierContext>(i);
}


size_t JavaLabeledParser::ResourceContext::getRuleIndex() const {
  return JavaLabeledParser::RuleResource;
}

void JavaLabeledParser::ResourceContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterResource(this);
}

void JavaLabeledParser::ResourceContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitResource(this);
}


antlrcpp::Any JavaLabeledParser::ResourceContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitResource(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ResourceContext* JavaLabeledParser::resource() {
  ResourceContext *_localctx = _tracker.createInstance<ResourceContext>(_ctx, getState());
  enterRule(_localctx, 148, JavaLabeledParser::RuleResource);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(1008);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 118, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(1005);
        variableModifier(); 
      }
      setState(1010);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 118, _ctx);
    }
    setState(1011);
    classOrInterfaceType();
    setState(1012);
    variableDeclaratorId();
    setState(1013);
    match(JavaLabeledParser::ASSIGN);
    setState(1014);
    expression(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SwitchBlockStatementGroupContext ------------------------------------------------------------------

JavaLabeledParser::SwitchBlockStatementGroupContext::SwitchBlockStatementGroupContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::SwitchLabelContext *> JavaLabeledParser::SwitchBlockStatementGroupContext::switchLabel() {
  return getRuleContexts<JavaLabeledParser::SwitchLabelContext>();
}

JavaLabeledParser::SwitchLabelContext* JavaLabeledParser::SwitchBlockStatementGroupContext::switchLabel(size_t i) {
  return getRuleContext<JavaLabeledParser::SwitchLabelContext>(i);
}

std::vector<JavaLabeledParser::BlockStatementContext *> JavaLabeledParser::SwitchBlockStatementGroupContext::blockStatement() {
  return getRuleContexts<JavaLabeledParser::BlockStatementContext>();
}

JavaLabeledParser::BlockStatementContext* JavaLabeledParser::SwitchBlockStatementGroupContext::blockStatement(size_t i) {
  return getRuleContext<JavaLabeledParser::BlockStatementContext>(i);
}


size_t JavaLabeledParser::SwitchBlockStatementGroupContext::getRuleIndex() const {
  return JavaLabeledParser::RuleSwitchBlockStatementGroup;
}

void JavaLabeledParser::SwitchBlockStatementGroupContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSwitchBlockStatementGroup(this);
}

void JavaLabeledParser::SwitchBlockStatementGroupContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSwitchBlockStatementGroup(this);
}


antlrcpp::Any JavaLabeledParser::SwitchBlockStatementGroupContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitSwitchBlockStatementGroup(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::SwitchBlockStatementGroupContext* JavaLabeledParser::switchBlockStatementGroup() {
  SwitchBlockStatementGroupContext *_localctx = _tracker.createInstance<SwitchBlockStatementGroupContext>(_ctx, getState());
  enterRule(_localctx, 150, JavaLabeledParser::RuleSwitchBlockStatementGroup);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1017); 
    _errHandler->sync(this);
    _la = _input->LA(1);
    do {
      setState(1016);
      switchLabel();
      setState(1019); 
      _errHandler->sync(this);
      _la = _input->LA(1);
    } while (_la == JavaLabeledParser::CASE

    || _la == JavaLabeledParser::DEFAULT);
    setState(1022); 
    _errHandler->sync(this);
    _la = _input->LA(1);
    do {
      setState(1021);
      blockStatement();
      setState(1024); 
      _errHandler->sync(this);
      _la = _input->LA(1);
    } while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::ABSTRACT)
      | (1ULL << JavaLabeledParser::ASSERT)
      | (1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BREAK)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::CLASS)
      | (1ULL << JavaLabeledParser::CONTINUE)
      | (1ULL << JavaLabeledParser::DO)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::FINAL)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::FOR)
      | (1ULL << JavaLabeledParser::IF)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::INTERFACE)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NEW)
      | (1ULL << JavaLabeledParser::PRIVATE)
      | (1ULL << JavaLabeledParser::PROTECTED)
      | (1ULL << JavaLabeledParser::PUBLIC)
      | (1ULL << JavaLabeledParser::RETURN)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::STATIC)
      | (1ULL << JavaLabeledParser::STRICTFP)
      | (1ULL << JavaLabeledParser::SUPER)
      | (1ULL << JavaLabeledParser::SWITCH)
      | (1ULL << JavaLabeledParser::SYNCHRONIZED)
      | (1ULL << JavaLabeledParser::THIS)
      | (1ULL << JavaLabeledParser::THROW)
      | (1ULL << JavaLabeledParser::TRY)
      | (1ULL << JavaLabeledParser::VOID)
      | (1ULL << JavaLabeledParser::WHILE)
      | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_LITERAL)
      | (1ULL << JavaLabeledParser::OCT_LITERAL)
      | (1ULL << JavaLabeledParser::BINARY_LITERAL)
      | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::BOOL_LITERAL)
      | (1ULL << JavaLabeledParser::CHAR_LITERAL)
      | (1ULL << JavaLabeledParser::STRING_LITERAL)
      | (1ULL << JavaLabeledParser::NULL_LITERAL)
      | (1ULL << JavaLabeledParser::LPAREN)
      | (1ULL << JavaLabeledParser::LBRACE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaLabeledParser::SEMI - 67))
      | (1ULL << (JavaLabeledParser::LT - 67))
      | (1ULL << (JavaLabeledParser::BANG - 67))
      | (1ULL << (JavaLabeledParser::TILDE - 67))
      | (1ULL << (JavaLabeledParser::INC - 67))
      | (1ULL << (JavaLabeledParser::DEC - 67))
      | (1ULL << (JavaLabeledParser::ADD - 67))
      | (1ULL << (JavaLabeledParser::SUB - 67))
      | (1ULL << (JavaLabeledParser::AT - 67))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 67)))) != 0));
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SwitchLabelContext ------------------------------------------------------------------

JavaLabeledParser::SwitchLabelContext::SwitchLabelContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::SwitchLabelContext::CASE() {
  return getToken(JavaLabeledParser::CASE, 0);
}

tree::TerminalNode* JavaLabeledParser::SwitchLabelContext::COLON() {
  return getToken(JavaLabeledParser::COLON, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::SwitchLabelContext::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::SwitchLabelContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

tree::TerminalNode* JavaLabeledParser::SwitchLabelContext::DEFAULT() {
  return getToken(JavaLabeledParser::DEFAULT, 0);
}


size_t JavaLabeledParser::SwitchLabelContext::getRuleIndex() const {
  return JavaLabeledParser::RuleSwitchLabel;
}

void JavaLabeledParser::SwitchLabelContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSwitchLabel(this);
}

void JavaLabeledParser::SwitchLabelContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSwitchLabel(this);
}


antlrcpp::Any JavaLabeledParser::SwitchLabelContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitSwitchLabel(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::SwitchLabelContext* JavaLabeledParser::switchLabel() {
  SwitchLabelContext *_localctx = _tracker.createInstance<SwitchLabelContext>(_ctx, getState());
  enterRule(_localctx, 152, JavaLabeledParser::RuleSwitchLabel);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1034);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::CASE: {
        enterOuterAlt(_localctx, 1);
        setState(1026);
        match(JavaLabeledParser::CASE);
        setState(1029);
        _errHandler->sync(this);
        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 121, _ctx)) {
        case 1: {
          setState(1027);
          antlrcpp::downCast<SwitchLabelContext *>(_localctx)->constantExpression = expression(0);
          break;
        }

        case 2: {
          setState(1028);
          antlrcpp::downCast<SwitchLabelContext *>(_localctx)->enumConstantName = match(JavaLabeledParser::IDENTIFIER);
          break;
        }

        default:
          break;
        }
        setState(1031);
        match(JavaLabeledParser::COLON);
        break;
      }

      case JavaLabeledParser::DEFAULT: {
        enterOuterAlt(_localctx, 2);
        setState(1032);
        match(JavaLabeledParser::DEFAULT);
        setState(1033);
        match(JavaLabeledParser::COLON);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ForControlContext ------------------------------------------------------------------

JavaLabeledParser::ForControlContext::ForControlContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::ForControlContext::getRuleIndex() const {
  return JavaLabeledParser::RuleForControl;
}

void JavaLabeledParser::ForControlContext::copyFrom(ForControlContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ForControl0Context ------------------------------------------------------------------

JavaLabeledParser::EnhancedForControlContext* JavaLabeledParser::ForControl0Context::enhancedForControl() {
  return getRuleContext<JavaLabeledParser::EnhancedForControlContext>(0);
}

JavaLabeledParser::ForControl0Context::ForControl0Context(ForControlContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ForControl0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterForControl0(this);
}
void JavaLabeledParser::ForControl0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitForControl0(this);
}

antlrcpp::Any JavaLabeledParser::ForControl0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitForControl0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ForControl1Context ------------------------------------------------------------------

std::vector<tree::TerminalNode *> JavaLabeledParser::ForControl1Context::SEMI() {
  return getTokens(JavaLabeledParser::SEMI);
}

tree::TerminalNode* JavaLabeledParser::ForControl1Context::SEMI(size_t i) {
  return getToken(JavaLabeledParser::SEMI, i);
}

JavaLabeledParser::ForInitContext* JavaLabeledParser::ForControl1Context::forInit() {
  return getRuleContext<JavaLabeledParser::ForInitContext>(0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::ForControl1Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

JavaLabeledParser::ExpressionListContext* JavaLabeledParser::ForControl1Context::expressionList() {
  return getRuleContext<JavaLabeledParser::ExpressionListContext>(0);
}

JavaLabeledParser::ForControl1Context::ForControl1Context(ForControlContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ForControl1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterForControl1(this);
}
void JavaLabeledParser::ForControl1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitForControl1(this);
}

antlrcpp::Any JavaLabeledParser::ForControl1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitForControl1(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::ForControlContext* JavaLabeledParser::forControl() {
  ForControlContext *_localctx = _tracker.createInstance<ForControlContext>(_ctx, getState());
  enterRule(_localctx, 154, JavaLabeledParser::RuleForControl);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1048);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 126, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ForControl0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(1036);
      enhancedForControl();
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ForControl1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(1038);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
        | (1ULL << JavaLabeledParser::BYTE)
        | (1ULL << JavaLabeledParser::CHAR)
        | (1ULL << JavaLabeledParser::DOUBLE)
        | (1ULL << JavaLabeledParser::FINAL)
        | (1ULL << JavaLabeledParser::FLOAT)
        | (1ULL << JavaLabeledParser::INT)
        | (1ULL << JavaLabeledParser::LONG)
        | (1ULL << JavaLabeledParser::NEW)
        | (1ULL << JavaLabeledParser::SHORT)
        | (1ULL << JavaLabeledParser::SUPER)
        | (1ULL << JavaLabeledParser::THIS)
        | (1ULL << JavaLabeledParser::VOID)
        | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
        | (1ULL << JavaLabeledParser::HEX_LITERAL)
        | (1ULL << JavaLabeledParser::OCT_LITERAL)
        | (1ULL << JavaLabeledParser::BINARY_LITERAL)
        | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
        | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
        | (1ULL << JavaLabeledParser::BOOL_LITERAL)
        | (1ULL << JavaLabeledParser::CHAR_LITERAL)
        | (1ULL << JavaLabeledParser::STRING_LITERAL)
        | (1ULL << JavaLabeledParser::NULL_LITERAL)
        | (1ULL << JavaLabeledParser::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
        | (1ULL << (JavaLabeledParser::BANG - 72))
        | (1ULL << (JavaLabeledParser::TILDE - 72))
        | (1ULL << (JavaLabeledParser::INC - 72))
        | (1ULL << (JavaLabeledParser::DEC - 72))
        | (1ULL << (JavaLabeledParser::ADD - 72))
        | (1ULL << (JavaLabeledParser::SUB - 72))
        | (1ULL << (JavaLabeledParser::AT - 72))
        | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
        setState(1037);
        forInit();
      }
      setState(1040);
      match(JavaLabeledParser::SEMI);
      setState(1042);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
        | (1ULL << JavaLabeledParser::BYTE)
        | (1ULL << JavaLabeledParser::CHAR)
        | (1ULL << JavaLabeledParser::DOUBLE)
        | (1ULL << JavaLabeledParser::FLOAT)
        | (1ULL << JavaLabeledParser::INT)
        | (1ULL << JavaLabeledParser::LONG)
        | (1ULL << JavaLabeledParser::NEW)
        | (1ULL << JavaLabeledParser::SHORT)
        | (1ULL << JavaLabeledParser::SUPER)
        | (1ULL << JavaLabeledParser::THIS)
        | (1ULL << JavaLabeledParser::VOID)
        | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
        | (1ULL << JavaLabeledParser::HEX_LITERAL)
        | (1ULL << JavaLabeledParser::OCT_LITERAL)
        | (1ULL << JavaLabeledParser::BINARY_LITERAL)
        | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
        | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
        | (1ULL << JavaLabeledParser::BOOL_LITERAL)
        | (1ULL << JavaLabeledParser::CHAR_LITERAL)
        | (1ULL << JavaLabeledParser::STRING_LITERAL)
        | (1ULL << JavaLabeledParser::NULL_LITERAL)
        | (1ULL << JavaLabeledParser::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
        | (1ULL << (JavaLabeledParser::BANG - 72))
        | (1ULL << (JavaLabeledParser::TILDE - 72))
        | (1ULL << (JavaLabeledParser::INC - 72))
        | (1ULL << (JavaLabeledParser::DEC - 72))
        | (1ULL << (JavaLabeledParser::ADD - 72))
        | (1ULL << (JavaLabeledParser::SUB - 72))
        | (1ULL << (JavaLabeledParser::AT - 72))
        | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
        setState(1041);
        expression(0);
      }
      setState(1044);
      match(JavaLabeledParser::SEMI);
      setState(1046);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
        | (1ULL << JavaLabeledParser::BYTE)
        | (1ULL << JavaLabeledParser::CHAR)
        | (1ULL << JavaLabeledParser::DOUBLE)
        | (1ULL << JavaLabeledParser::FLOAT)
        | (1ULL << JavaLabeledParser::INT)
        | (1ULL << JavaLabeledParser::LONG)
        | (1ULL << JavaLabeledParser::NEW)
        | (1ULL << JavaLabeledParser::SHORT)
        | (1ULL << JavaLabeledParser::SUPER)
        | (1ULL << JavaLabeledParser::THIS)
        | (1ULL << JavaLabeledParser::VOID)
        | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
        | (1ULL << JavaLabeledParser::HEX_LITERAL)
        | (1ULL << JavaLabeledParser::OCT_LITERAL)
        | (1ULL << JavaLabeledParser::BINARY_LITERAL)
        | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
        | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
        | (1ULL << JavaLabeledParser::BOOL_LITERAL)
        | (1ULL << JavaLabeledParser::CHAR_LITERAL)
        | (1ULL << JavaLabeledParser::STRING_LITERAL)
        | (1ULL << JavaLabeledParser::NULL_LITERAL)
        | (1ULL << JavaLabeledParser::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
        | (1ULL << (JavaLabeledParser::BANG - 72))
        | (1ULL << (JavaLabeledParser::TILDE - 72))
        | (1ULL << (JavaLabeledParser::INC - 72))
        | (1ULL << (JavaLabeledParser::DEC - 72))
        | (1ULL << (JavaLabeledParser::ADD - 72))
        | (1ULL << (JavaLabeledParser::SUB - 72))
        | (1ULL << (JavaLabeledParser::AT - 72))
        | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
        setState(1045);
        antlrcpp::downCast<ForControl1Context *>(_localctx)->forUpdate = expressionList();
      }
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ForInitContext ------------------------------------------------------------------

JavaLabeledParser::ForInitContext::ForInitContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::ForInitContext::getRuleIndex() const {
  return JavaLabeledParser::RuleForInit;
}

void JavaLabeledParser::ForInitContext::copyFrom(ForInitContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ForInit1Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionListContext* JavaLabeledParser::ForInit1Context::expressionList() {
  return getRuleContext<JavaLabeledParser::ExpressionListContext>(0);
}

JavaLabeledParser::ForInit1Context::ForInit1Context(ForInitContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ForInit1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterForInit1(this);
}
void JavaLabeledParser::ForInit1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitForInit1(this);
}

antlrcpp::Any JavaLabeledParser::ForInit1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitForInit1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ForInit0Context ------------------------------------------------------------------

JavaLabeledParser::LocalVariableDeclarationContext* JavaLabeledParser::ForInit0Context::localVariableDeclaration() {
  return getRuleContext<JavaLabeledParser::LocalVariableDeclarationContext>(0);
}

JavaLabeledParser::ForInit0Context::ForInit0Context(ForInitContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ForInit0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterForInit0(this);
}
void JavaLabeledParser::ForInit0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitForInit0(this);
}

antlrcpp::Any JavaLabeledParser::ForInit0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitForInit0(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::ForInitContext* JavaLabeledParser::forInit() {
  ForInitContext *_localctx = _tracker.createInstance<ForInitContext>(_ctx, getState());
  enterRule(_localctx, 156, JavaLabeledParser::RuleForInit);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1052);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 127, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ForInit0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(1050);
      localVariableDeclaration();
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::ForInit1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(1051);
      expressionList();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- EnhancedForControlContext ------------------------------------------------------------------

JavaLabeledParser::EnhancedForControlContext::EnhancedForControlContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::EnhancedForControlContext::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

JavaLabeledParser::VariableDeclaratorIdContext* JavaLabeledParser::EnhancedForControlContext::variableDeclaratorId() {
  return getRuleContext<JavaLabeledParser::VariableDeclaratorIdContext>(0);
}

tree::TerminalNode* JavaLabeledParser::EnhancedForControlContext::COLON() {
  return getToken(JavaLabeledParser::COLON, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::EnhancedForControlContext::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

std::vector<JavaLabeledParser::VariableModifierContext *> JavaLabeledParser::EnhancedForControlContext::variableModifier() {
  return getRuleContexts<JavaLabeledParser::VariableModifierContext>();
}

JavaLabeledParser::VariableModifierContext* JavaLabeledParser::EnhancedForControlContext::variableModifier(size_t i) {
  return getRuleContext<JavaLabeledParser::VariableModifierContext>(i);
}


size_t JavaLabeledParser::EnhancedForControlContext::getRuleIndex() const {
  return JavaLabeledParser::RuleEnhancedForControl;
}

void JavaLabeledParser::EnhancedForControlContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnhancedForControl(this);
}

void JavaLabeledParser::EnhancedForControlContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnhancedForControl(this);
}


antlrcpp::Any JavaLabeledParser::EnhancedForControlContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitEnhancedForControl(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::EnhancedForControlContext* JavaLabeledParser::enhancedForControl() {
  EnhancedForControlContext *_localctx = _tracker.createInstance<EnhancedForControlContext>(_ctx, getState());
  enterRule(_localctx, 158, JavaLabeledParser::RuleEnhancedForControl);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(1057);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 128, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(1054);
        variableModifier(); 
      }
      setState(1059);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 128, _ctx);
    }
    setState(1060);
    typeType();
    setState(1061);
    variableDeclaratorId();
    setState(1062);
    match(JavaLabeledParser::COLON);
    setState(1063);
    expression(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ParExpressionContext ------------------------------------------------------------------

JavaLabeledParser::ParExpressionContext::ParExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ParExpressionContext::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::ParExpressionContext::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ParExpressionContext::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}


size_t JavaLabeledParser::ParExpressionContext::getRuleIndex() const {
  return JavaLabeledParser::RuleParExpression;
}

void JavaLabeledParser::ParExpressionContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterParExpression(this);
}

void JavaLabeledParser::ParExpressionContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitParExpression(this);
}


antlrcpp::Any JavaLabeledParser::ParExpressionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitParExpression(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ParExpressionContext* JavaLabeledParser::parExpression() {
  ParExpressionContext *_localctx = _tracker.createInstance<ParExpressionContext>(_ctx, getState());
  enterRule(_localctx, 160, JavaLabeledParser::RuleParExpression);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1065);
    match(JavaLabeledParser::LPAREN);
    setState(1066);
    expression(0);
    setState(1067);
    match(JavaLabeledParser::RPAREN);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExpressionListContext ------------------------------------------------------------------

JavaLabeledParser::ExpressionListContext::ExpressionListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::ExpressionListContext::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::ExpressionListContext::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ExpressionListContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::ExpressionListContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::ExpressionListContext::getRuleIndex() const {
  return JavaLabeledParser::RuleExpressionList;
}

void JavaLabeledParser::ExpressionListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpressionList(this);
}

void JavaLabeledParser::ExpressionListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpressionList(this);
}


antlrcpp::Any JavaLabeledParser::ExpressionListContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpressionList(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ExpressionListContext* JavaLabeledParser::expressionList() {
  ExpressionListContext *_localctx = _tracker.createInstance<ExpressionListContext>(_ctx, getState());
  enterRule(_localctx, 162, JavaLabeledParser::RuleExpressionList);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1069);
    expression(0);
    setState(1074);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::COMMA) {
      setState(1070);
      match(JavaLabeledParser::COMMA);
      setState(1071);
      expression(0);
      setState(1076);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- MethodCallContext ------------------------------------------------------------------

JavaLabeledParser::MethodCallContext::MethodCallContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::MethodCallContext::getRuleIndex() const {
  return JavaLabeledParser::RuleMethodCall;
}

void JavaLabeledParser::MethodCallContext::copyFrom(MethodCallContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- MethodCall0Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::MethodCall0Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

tree::TerminalNode* JavaLabeledParser::MethodCall0Context::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::MethodCall0Context::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::ExpressionListContext* JavaLabeledParser::MethodCall0Context::expressionList() {
  return getRuleContext<JavaLabeledParser::ExpressionListContext>(0);
}

JavaLabeledParser::MethodCall0Context::MethodCall0Context(MethodCallContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MethodCall0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodCall0(this);
}
void JavaLabeledParser::MethodCall0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodCall0(this);
}

antlrcpp::Any JavaLabeledParser::MethodCall0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMethodCall0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MethodCall1Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::MethodCall1Context::THIS() {
  return getToken(JavaLabeledParser::THIS, 0);
}

tree::TerminalNode* JavaLabeledParser::MethodCall1Context::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::MethodCall1Context::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::ExpressionListContext* JavaLabeledParser::MethodCall1Context::expressionList() {
  return getRuleContext<JavaLabeledParser::ExpressionListContext>(0);
}

JavaLabeledParser::MethodCall1Context::MethodCall1Context(MethodCallContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MethodCall1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodCall1(this);
}
void JavaLabeledParser::MethodCall1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodCall1(this);
}

antlrcpp::Any JavaLabeledParser::MethodCall1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMethodCall1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MethodCall2Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::MethodCall2Context::SUPER() {
  return getToken(JavaLabeledParser::SUPER, 0);
}

tree::TerminalNode* JavaLabeledParser::MethodCall2Context::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::MethodCall2Context::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::ExpressionListContext* JavaLabeledParser::MethodCall2Context::expressionList() {
  return getRuleContext<JavaLabeledParser::ExpressionListContext>(0);
}

JavaLabeledParser::MethodCall2Context::MethodCall2Context(MethodCallContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::MethodCall2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodCall2(this);
}
void JavaLabeledParser::MethodCall2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodCall2(this);
}

antlrcpp::Any JavaLabeledParser::MethodCall2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitMethodCall2(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::MethodCallContext* JavaLabeledParser::methodCall() {
  MethodCallContext *_localctx = _tracker.createInstance<MethodCallContext>(_ctx, getState());
  enterRule(_localctx, 164, JavaLabeledParser::RuleMethodCall);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1095);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::IDENTIFIER: {
        _localctx = _tracker.createInstance<JavaLabeledParser::MethodCall0Context>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(1077);
        match(JavaLabeledParser::IDENTIFIER);
        setState(1078);
        match(JavaLabeledParser::LPAREN);
        setState(1080);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
          | (1ULL << JavaLabeledParser::BYTE)
          | (1ULL << JavaLabeledParser::CHAR)
          | (1ULL << JavaLabeledParser::DOUBLE)
          | (1ULL << JavaLabeledParser::FLOAT)
          | (1ULL << JavaLabeledParser::INT)
          | (1ULL << JavaLabeledParser::LONG)
          | (1ULL << JavaLabeledParser::NEW)
          | (1ULL << JavaLabeledParser::SHORT)
          | (1ULL << JavaLabeledParser::SUPER)
          | (1ULL << JavaLabeledParser::THIS)
          | (1ULL << JavaLabeledParser::VOID)
          | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
          | (1ULL << JavaLabeledParser::HEX_LITERAL)
          | (1ULL << JavaLabeledParser::OCT_LITERAL)
          | (1ULL << JavaLabeledParser::BINARY_LITERAL)
          | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
          | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
          | (1ULL << JavaLabeledParser::BOOL_LITERAL)
          | (1ULL << JavaLabeledParser::CHAR_LITERAL)
          | (1ULL << JavaLabeledParser::STRING_LITERAL)
          | (1ULL << JavaLabeledParser::NULL_LITERAL)
          | (1ULL << JavaLabeledParser::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
          ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
          | (1ULL << (JavaLabeledParser::BANG - 72))
          | (1ULL << (JavaLabeledParser::TILDE - 72))
          | (1ULL << (JavaLabeledParser::INC - 72))
          | (1ULL << (JavaLabeledParser::DEC - 72))
          | (1ULL << (JavaLabeledParser::ADD - 72))
          | (1ULL << (JavaLabeledParser::SUB - 72))
          | (1ULL << (JavaLabeledParser::AT - 72))
          | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
          setState(1079);
          expressionList();
        }
        setState(1082);
        match(JavaLabeledParser::RPAREN);
        break;
      }

      case JavaLabeledParser::THIS: {
        _localctx = _tracker.createInstance<JavaLabeledParser::MethodCall1Context>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(1083);
        match(JavaLabeledParser::THIS);
        setState(1084);
        match(JavaLabeledParser::LPAREN);
        setState(1086);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
          | (1ULL << JavaLabeledParser::BYTE)
          | (1ULL << JavaLabeledParser::CHAR)
          | (1ULL << JavaLabeledParser::DOUBLE)
          | (1ULL << JavaLabeledParser::FLOAT)
          | (1ULL << JavaLabeledParser::INT)
          | (1ULL << JavaLabeledParser::LONG)
          | (1ULL << JavaLabeledParser::NEW)
          | (1ULL << JavaLabeledParser::SHORT)
          | (1ULL << JavaLabeledParser::SUPER)
          | (1ULL << JavaLabeledParser::THIS)
          | (1ULL << JavaLabeledParser::VOID)
          | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
          | (1ULL << JavaLabeledParser::HEX_LITERAL)
          | (1ULL << JavaLabeledParser::OCT_LITERAL)
          | (1ULL << JavaLabeledParser::BINARY_LITERAL)
          | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
          | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
          | (1ULL << JavaLabeledParser::BOOL_LITERAL)
          | (1ULL << JavaLabeledParser::CHAR_LITERAL)
          | (1ULL << JavaLabeledParser::STRING_LITERAL)
          | (1ULL << JavaLabeledParser::NULL_LITERAL)
          | (1ULL << JavaLabeledParser::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
          ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
          | (1ULL << (JavaLabeledParser::BANG - 72))
          | (1ULL << (JavaLabeledParser::TILDE - 72))
          | (1ULL << (JavaLabeledParser::INC - 72))
          | (1ULL << (JavaLabeledParser::DEC - 72))
          | (1ULL << (JavaLabeledParser::ADD - 72))
          | (1ULL << (JavaLabeledParser::SUB - 72))
          | (1ULL << (JavaLabeledParser::AT - 72))
          | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
          setState(1085);
          expressionList();
        }
        setState(1088);
        match(JavaLabeledParser::RPAREN);
        break;
      }

      case JavaLabeledParser::SUPER: {
        _localctx = _tracker.createInstance<JavaLabeledParser::MethodCall2Context>(_localctx);
        enterOuterAlt(_localctx, 3);
        setState(1089);
        match(JavaLabeledParser::SUPER);
        setState(1090);
        match(JavaLabeledParser::LPAREN);
        setState(1092);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
          | (1ULL << JavaLabeledParser::BYTE)
          | (1ULL << JavaLabeledParser::CHAR)
          | (1ULL << JavaLabeledParser::DOUBLE)
          | (1ULL << JavaLabeledParser::FLOAT)
          | (1ULL << JavaLabeledParser::INT)
          | (1ULL << JavaLabeledParser::LONG)
          | (1ULL << JavaLabeledParser::NEW)
          | (1ULL << JavaLabeledParser::SHORT)
          | (1ULL << JavaLabeledParser::SUPER)
          | (1ULL << JavaLabeledParser::THIS)
          | (1ULL << JavaLabeledParser::VOID)
          | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
          | (1ULL << JavaLabeledParser::HEX_LITERAL)
          | (1ULL << JavaLabeledParser::OCT_LITERAL)
          | (1ULL << JavaLabeledParser::BINARY_LITERAL)
          | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
          | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
          | (1ULL << JavaLabeledParser::BOOL_LITERAL)
          | (1ULL << JavaLabeledParser::CHAR_LITERAL)
          | (1ULL << JavaLabeledParser::STRING_LITERAL)
          | (1ULL << JavaLabeledParser::NULL_LITERAL)
          | (1ULL << JavaLabeledParser::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
          ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
          | (1ULL << (JavaLabeledParser::BANG - 72))
          | (1ULL << (JavaLabeledParser::TILDE - 72))
          | (1ULL << (JavaLabeledParser::INC - 72))
          | (1ULL << (JavaLabeledParser::DEC - 72))
          | (1ULL << (JavaLabeledParser::ADD - 72))
          | (1ULL << (JavaLabeledParser::SUB - 72))
          | (1ULL << (JavaLabeledParser::AT - 72))
          | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
          setState(1091);
          expressionList();
        }
        setState(1094);
        match(JavaLabeledParser::RPAREN);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExpressionContext ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext::ExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::ExpressionContext::getRuleIndex() const {
  return JavaLabeledParser::RuleExpression;
}

void JavaLabeledParser::ExpressionContext::copyFrom(ExpressionContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Expression8Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression8Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression8Context::TILDE() {
  return getToken(JavaLabeledParser::TILDE, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression8Context::BANG() {
  return getToken(JavaLabeledParser::BANG, 0);
}

JavaLabeledParser::Expression8Context::Expression8Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression8Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression8(this);
}
void JavaLabeledParser::Expression8Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression8(this);
}

antlrcpp::Any JavaLabeledParser::Expression8Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression8(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression10Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression10Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression10Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression10Context::ADD() {
  return getToken(JavaLabeledParser::ADD, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression10Context::SUB() {
  return getToken(JavaLabeledParser::SUB, 0);
}

JavaLabeledParser::Expression10Context::Expression10Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression10Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression10(this);
}
void JavaLabeledParser::Expression10Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression10(this);
}

antlrcpp::Any JavaLabeledParser::Expression10Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression10(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression9Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression9Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression9Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression9Context::MUL() {
  return getToken(JavaLabeledParser::MUL, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression9Context::DIV() {
  return getToken(JavaLabeledParser::DIV, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression9Context::MOD() {
  return getToken(JavaLabeledParser::MOD, 0);
}

JavaLabeledParser::Expression9Context::Expression9Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression9Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression9(this);
}
void JavaLabeledParser::Expression9Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression9(this);
}

antlrcpp::Any JavaLabeledParser::Expression9Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression9(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression12Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression12Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression12Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression12Context::LE() {
  return getToken(JavaLabeledParser::LE, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression12Context::GE() {
  return getToken(JavaLabeledParser::GE, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression12Context::GT() {
  return getToken(JavaLabeledParser::GT, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression12Context::LT() {
  return getToken(JavaLabeledParser::LT, 0);
}

JavaLabeledParser::Expression12Context::Expression12Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression12Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression12(this);
}
void JavaLabeledParser::Expression12Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression12(this);
}

antlrcpp::Any JavaLabeledParser::Expression12Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression12(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression11Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression11Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression11Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::Expression11Context::LT() {
  return getTokens(JavaLabeledParser::LT);
}

tree::TerminalNode* JavaLabeledParser::Expression11Context::LT(size_t i) {
  return getToken(JavaLabeledParser::LT, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::Expression11Context::GT() {
  return getTokens(JavaLabeledParser::GT);
}

tree::TerminalNode* JavaLabeledParser::Expression11Context::GT(size_t i) {
  return getToken(JavaLabeledParser::GT, i);
}

JavaLabeledParser::Expression11Context::Expression11Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression11Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression11(this);
}
void JavaLabeledParser::Expression11Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression11(this);
}

antlrcpp::Any JavaLabeledParser::Expression11Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression11(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression14Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression14Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression14Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression14Context::EQUAL() {
  return getToken(JavaLabeledParser::EQUAL, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression14Context::NOTEQUAL() {
  return getToken(JavaLabeledParser::NOTEQUAL, 0);
}

JavaLabeledParser::Expression14Context::Expression14Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression14Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression14(this);
}
void JavaLabeledParser::Expression14Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression14(this);
}

antlrcpp::Any JavaLabeledParser::Expression14Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression14(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression13Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression13Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::Expression13Context::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression13Context::INSTANCEOF() {
  return getToken(JavaLabeledParser::INSTANCEOF, 0);
}

JavaLabeledParser::Expression13Context::Expression13Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression13Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression13(this);
}
void JavaLabeledParser::Expression13Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression13(this);
}

antlrcpp::Any JavaLabeledParser::Expression13Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression13(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression16Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression16Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression16Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression16Context::CARET() {
  return getToken(JavaLabeledParser::CARET, 0);
}

JavaLabeledParser::Expression16Context::Expression16Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression16Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression16(this);
}
void JavaLabeledParser::Expression16Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression16(this);
}

antlrcpp::Any JavaLabeledParser::Expression16Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression16(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression15Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression15Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression15Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression15Context::BITAND() {
  return getToken(JavaLabeledParser::BITAND, 0);
}

JavaLabeledParser::Expression15Context::Expression15Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression15Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression15(this);
}
void JavaLabeledParser::Expression15Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression15(this);
}

antlrcpp::Any JavaLabeledParser::Expression15Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression15(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression18Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression18Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression18Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression18Context::AND() {
  return getToken(JavaLabeledParser::AND, 0);
}

JavaLabeledParser::Expression18Context::Expression18Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression18Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression18(this);
}
void JavaLabeledParser::Expression18Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression18(this);
}

antlrcpp::Any JavaLabeledParser::Expression18Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression18(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression17Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression17Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression17Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression17Context::BITOR() {
  return getToken(JavaLabeledParser::BITOR, 0);
}

JavaLabeledParser::Expression17Context::Expression17Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression17Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression17(this);
}
void JavaLabeledParser::Expression17Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression17(this);
}

antlrcpp::Any JavaLabeledParser::Expression17Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression17(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression19Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression19Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression19Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression19Context::OR() {
  return getToken(JavaLabeledParser::OR, 0);
}

JavaLabeledParser::Expression19Context::Expression19Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression19Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression19(this);
}
void JavaLabeledParser::Expression19Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression19(this);
}

antlrcpp::Any JavaLabeledParser::Expression19Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression19(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression6Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression6Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression6Context::INC() {
  return getToken(JavaLabeledParser::INC, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression6Context::DEC() {
  return getToken(JavaLabeledParser::DEC, 0);
}

JavaLabeledParser::Expression6Context::Expression6Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression6(this);
}
void JavaLabeledParser::Expression6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression6(this);
}

antlrcpp::Any JavaLabeledParser::Expression6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression7Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression7Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression7Context::ADD() {
  return getToken(JavaLabeledParser::ADD, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression7Context::SUB() {
  return getToken(JavaLabeledParser::SUB, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression7Context::INC() {
  return getToken(JavaLabeledParser::INC, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression7Context::DEC() {
  return getToken(JavaLabeledParser::DEC, 0);
}

JavaLabeledParser::Expression7Context::Expression7Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression7Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression7(this);
}
void JavaLabeledParser::Expression7Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression7(this);
}

antlrcpp::Any JavaLabeledParser::Expression7Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression7(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression4Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Expression4Context::NEW() {
  return getToken(JavaLabeledParser::NEW, 0);
}

JavaLabeledParser::CreatorContext* JavaLabeledParser::Expression4Context::creator() {
  return getRuleContext<JavaLabeledParser::CreatorContext>(0);
}

JavaLabeledParser::Expression4Context::Expression4Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression4(this);
}
void JavaLabeledParser::Expression4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression4(this);
}

antlrcpp::Any JavaLabeledParser::Expression4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression5Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Expression5Context::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::Expression5Context::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression5Context::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression5Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::Expression5Context::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::Expression5Context::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}

JavaLabeledParser::Expression5Context::Expression5Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression5(this);
}
void JavaLabeledParser::Expression5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression5(this);
}

antlrcpp::Any JavaLabeledParser::Expression5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression2Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression2Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression2Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression2Context::LBRACK() {
  return getToken(JavaLabeledParser::LBRACK, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression2Context::RBRACK() {
  return getToken(JavaLabeledParser::RBRACK, 0);
}

JavaLabeledParser::Expression2Context::Expression2Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression2(this);
}
void JavaLabeledParser::Expression2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression2(this);
}

antlrcpp::Any JavaLabeledParser::Expression2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression3Context ------------------------------------------------------------------

JavaLabeledParser::MethodCallContext* JavaLabeledParser::Expression3Context::methodCall() {
  return getRuleContext<JavaLabeledParser::MethodCallContext>(0);
}

JavaLabeledParser::Expression3Context::Expression3Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression3(this);
}
void JavaLabeledParser::Expression3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression3(this);
}

antlrcpp::Any JavaLabeledParser::Expression3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression0Context ------------------------------------------------------------------

JavaLabeledParser::PrimaryContext* JavaLabeledParser::Expression0Context::primary() {
  return getRuleContext<JavaLabeledParser::PrimaryContext>(0);
}

JavaLabeledParser::Expression0Context::Expression0Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression0(this);
}
void JavaLabeledParser::Expression0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression0(this);
}

antlrcpp::Any JavaLabeledParser::Expression0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression1Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression1Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression1Context::DOT() {
  return getToken(JavaLabeledParser::DOT, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression1Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::MethodCallContext* JavaLabeledParser::Expression1Context::methodCall() {
  return getRuleContext<JavaLabeledParser::MethodCallContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression1Context::THIS() {
  return getToken(JavaLabeledParser::THIS, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression1Context::NEW() {
  return getToken(JavaLabeledParser::NEW, 0);
}

JavaLabeledParser::InnerCreatorContext* JavaLabeledParser::Expression1Context::innerCreator() {
  return getRuleContext<JavaLabeledParser::InnerCreatorContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression1Context::SUPER() {
  return getToken(JavaLabeledParser::SUPER, 0);
}

JavaLabeledParser::SuperSuffixContext* JavaLabeledParser::Expression1Context::superSuffix() {
  return getRuleContext<JavaLabeledParser::SuperSuffixContext>(0);
}

JavaLabeledParser::ExplicitGenericInvocationContext* JavaLabeledParser::Expression1Context::explicitGenericInvocation() {
  return getRuleContext<JavaLabeledParser::ExplicitGenericInvocationContext>(0);
}

JavaLabeledParser::NonWildcardTypeArgumentsContext* JavaLabeledParser::Expression1Context::nonWildcardTypeArguments() {
  return getRuleContext<JavaLabeledParser::NonWildcardTypeArgumentsContext>(0);
}

JavaLabeledParser::Expression1Context::Expression1Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression1(this);
}
void JavaLabeledParser::Expression1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression1(this);
}

antlrcpp::Any JavaLabeledParser::Expression1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression21Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression21Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression21Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::ASSIGN() {
  return getToken(JavaLabeledParser::ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::ADD_ASSIGN() {
  return getToken(JavaLabeledParser::ADD_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::SUB_ASSIGN() {
  return getToken(JavaLabeledParser::SUB_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::MUL_ASSIGN() {
  return getToken(JavaLabeledParser::MUL_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::DIV_ASSIGN() {
  return getToken(JavaLabeledParser::DIV_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::AND_ASSIGN() {
  return getToken(JavaLabeledParser::AND_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::OR_ASSIGN() {
  return getToken(JavaLabeledParser::OR_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::XOR_ASSIGN() {
  return getToken(JavaLabeledParser::XOR_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::RSHIFT_ASSIGN() {
  return getToken(JavaLabeledParser::RSHIFT_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::URSHIFT_ASSIGN() {
  return getToken(JavaLabeledParser::URSHIFT_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::LSHIFT_ASSIGN() {
  return getToken(JavaLabeledParser::LSHIFT_ASSIGN, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression21Context::MOD_ASSIGN() {
  return getToken(JavaLabeledParser::MOD_ASSIGN, 0);
}

JavaLabeledParser::Expression21Context::Expression21Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression21Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression21(this);
}
void JavaLabeledParser::Expression21Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression21(this);
}

antlrcpp::Any JavaLabeledParser::Expression21Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression21(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression20Context ------------------------------------------------------------------

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::Expression20Context::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression20Context::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}

tree::TerminalNode* JavaLabeledParser::Expression20Context::COLON() {
  return getToken(JavaLabeledParser::COLON, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression20Context::QUESTION() {
  return getToken(JavaLabeledParser::QUESTION, 0);
}

JavaLabeledParser::Expression20Context::Expression20Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression20Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression20(this);
}
void JavaLabeledParser::Expression20Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression20(this);
}

antlrcpp::Any JavaLabeledParser::Expression20Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression20(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression23Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Expression23Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression23Context::COLONCOLON() {
  return getToken(JavaLabeledParser::COLONCOLON, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression23Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::TypeArgumentsContext* JavaLabeledParser::Expression23Context::typeArguments() {
  return getRuleContext<JavaLabeledParser::TypeArgumentsContext>(0);
}

JavaLabeledParser::Expression23Context::Expression23Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression23Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression23(this);
}
void JavaLabeledParser::Expression23Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression23(this);
}

antlrcpp::Any JavaLabeledParser::Expression23Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression23(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression22Context ------------------------------------------------------------------

JavaLabeledParser::LambdaExpressionContext* JavaLabeledParser::Expression22Context::lambdaExpression() {
  return getRuleContext<JavaLabeledParser::LambdaExpressionContext>(0);
}

JavaLabeledParser::Expression22Context::Expression22Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression22Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression22(this);
}
void JavaLabeledParser::Expression22Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression22(this);
}

antlrcpp::Any JavaLabeledParser::Expression22Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression22(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression25Context ------------------------------------------------------------------

JavaLabeledParser::ClassTypeContext* JavaLabeledParser::Expression25Context::classType() {
  return getRuleContext<JavaLabeledParser::ClassTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression25Context::COLONCOLON() {
  return getToken(JavaLabeledParser::COLONCOLON, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression25Context::NEW() {
  return getToken(JavaLabeledParser::NEW, 0);
}

JavaLabeledParser::TypeArgumentsContext* JavaLabeledParser::Expression25Context::typeArguments() {
  return getRuleContext<JavaLabeledParser::TypeArgumentsContext>(0);
}

JavaLabeledParser::Expression25Context::Expression25Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression25Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression25(this);
}
void JavaLabeledParser::Expression25Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression25(this);
}

antlrcpp::Any JavaLabeledParser::Expression25Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression25(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression24Context ------------------------------------------------------------------

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::Expression24Context::typeType() {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Expression24Context::COLONCOLON() {
  return getToken(JavaLabeledParser::COLONCOLON, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression24Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

tree::TerminalNode* JavaLabeledParser::Expression24Context::NEW() {
  return getToken(JavaLabeledParser::NEW, 0);
}

JavaLabeledParser::TypeArgumentsContext* JavaLabeledParser::Expression24Context::typeArguments() {
  return getRuleContext<JavaLabeledParser::TypeArgumentsContext>(0);
}

JavaLabeledParser::Expression24Context::Expression24Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Expression24Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression24(this);
}
void JavaLabeledParser::Expression24Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression24(this);
}

antlrcpp::Any JavaLabeledParser::Expression24Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExpression24(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::expression() {
   return expression(0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::expression(int precedence) {
  ParserRuleContext *parentContext = _ctx;
  size_t parentState = getState();
  JavaLabeledParser::ExpressionContext *_localctx = _tracker.createInstance<ExpressionContext>(_ctx, parentState);
  JavaLabeledParser::ExpressionContext *previousContext = _localctx;
  (void)previousContext; // Silence compiler, in case the context is not used by generated code.
  size_t startState = 166;
  enterRecursionRule(_localctx, 166, JavaLabeledParser::RuleExpression, precedence);

    size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    unrollRecursionContexts(parentContext);
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(1134);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 138, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<Expression0Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;

      setState(1098);
      primary();
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<Expression3Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1099);
      methodCall();
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<Expression4Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1100);
      match(JavaLabeledParser::NEW);
      setState(1101);
      creator();
      break;
    }

    case 4: {
      _localctx = _tracker.createInstance<Expression5Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1102);
      match(JavaLabeledParser::LPAREN);
      setState(1106);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 134, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(1103);
          annotation(); 
        }
        setState(1108);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 134, _ctx);
      }
      setState(1109);
      typeType();
      setState(1110);
      match(JavaLabeledParser::RPAREN);
      setState(1111);
      expression(21);
      break;
    }

    case 5: {
      _localctx = _tracker.createInstance<Expression7Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1113);
      antlrcpp::downCast<Expression7Context *>(_localctx)->prefix = _input->LT(1);
      _la = _input->LA(1);
      if (!(((((_la - 83) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 83)) & ((1ULL << (JavaLabeledParser::INC - 83))
        | (1ULL << (JavaLabeledParser::DEC - 83))
        | (1ULL << (JavaLabeledParser::ADD - 83))
        | (1ULL << (JavaLabeledParser::SUB - 83)))) != 0))) {
        antlrcpp::downCast<Expression7Context *>(_localctx)->prefix = _errHandler->recoverInline(this);
      }
      else {
        _errHandler->reportMatch(this);
        consume();
      }
      setState(1114);
      expression(19);
      break;
    }

    case 6: {
      _localctx = _tracker.createInstance<Expression8Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1115);
      antlrcpp::downCast<Expression8Context *>(_localctx)->prefix = _input->LT(1);
      _la = _input->LA(1);
      if (!(_la == JavaLabeledParser::BANG

      || _la == JavaLabeledParser::TILDE)) {
        antlrcpp::downCast<Expression8Context *>(_localctx)->prefix = _errHandler->recoverInline(this);
      }
      else {
        _errHandler->reportMatch(this);
        consume();
      }
      setState(1116);
      expression(18);
      break;
    }

    case 7: {
      _localctx = _tracker.createInstance<Expression22Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1117);
      lambdaExpression();
      break;
    }

    case 8: {
      _localctx = _tracker.createInstance<Expression24Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1118);
      typeType();
      setState(1119);
      match(JavaLabeledParser::COLONCOLON);
      setState(1125);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case JavaLabeledParser::LT:
        case JavaLabeledParser::IDENTIFIER: {
          setState(1121);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == JavaLabeledParser::LT) {
            setState(1120);
            typeArguments();
          }
          setState(1123);
          match(JavaLabeledParser::IDENTIFIER);
          break;
        }

        case JavaLabeledParser::NEW: {
          setState(1124);
          match(JavaLabeledParser::NEW);
          break;
        }

      default:
        throw NoViableAltException(this);
      }
      break;
    }

    case 9: {
      _localctx = _tracker.createInstance<Expression25Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1127);
      classType();
      setState(1128);
      match(JavaLabeledParser::COLONCOLON);
      setState(1130);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaLabeledParser::LT) {
        setState(1129);
        typeArguments();
      }
      setState(1132);
      match(JavaLabeledParser::NEW);
      break;
    }

    default:
      break;
    }
    _ctx->stop = _input->LT(-1);
    setState(1216);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 144, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        setState(1214);
        _errHandler->sync(this);
        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 143, _ctx)) {
        case 1: {
          auto newContext = _tracker.createInstance<Expression9Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1136);

          if (!(precpred(_ctx, 17))) throw FailedPredicateException(this, "precpred(_ctx, 17)");
          setState(1137);
          antlrcpp::downCast<Expression9Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(((((_la - 87) & ~ 0x3fULL) == 0) &&
            ((1ULL << (_la - 87)) & ((1ULL << (JavaLabeledParser::MUL - 87))
            | (1ULL << (JavaLabeledParser::DIV - 87))
            | (1ULL << (JavaLabeledParser::MOD - 87)))) != 0))) {
            antlrcpp::downCast<Expression9Context *>(_localctx)->bop = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(1138);
          expression(18);
          break;
        }

        case 2: {
          auto newContext = _tracker.createInstance<Expression10Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1139);

          if (!(precpred(_ctx, 16))) throw FailedPredicateException(this, "precpred(_ctx, 16)");
          setState(1140);
          antlrcpp::downCast<Expression10Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == JavaLabeledParser::ADD

          || _la == JavaLabeledParser::SUB)) {
            antlrcpp::downCast<Expression10Context *>(_localctx)->bop = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(1141);
          expression(17);
          break;
        }

        case 3: {
          auto newContext = _tracker.createInstance<Expression11Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1142);

          if (!(precpred(_ctx, 15))) throw FailedPredicateException(this, "precpred(_ctx, 15)");
          setState(1150);
          _errHandler->sync(this);
          switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 139, _ctx)) {
          case 1: {
            setState(1143);
            match(JavaLabeledParser::LT);
            setState(1144);
            match(JavaLabeledParser::LT);
            break;
          }

          case 2: {
            setState(1145);
            match(JavaLabeledParser::GT);
            setState(1146);
            match(JavaLabeledParser::GT);
            setState(1147);
            match(JavaLabeledParser::GT);
            break;
          }

          case 3: {
            setState(1148);
            match(JavaLabeledParser::GT);
            setState(1149);
            match(JavaLabeledParser::GT);
            break;
          }

          default:
            break;
          }
          setState(1152);
          expression(16);
          break;
        }

        case 4: {
          auto newContext = _tracker.createInstance<Expression12Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1153);

          if (!(precpred(_ctx, 14))) throw FailedPredicateException(this, "precpred(_ctx, 14)");
          setState(1154);
          antlrcpp::downCast<Expression12Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(((((_la - 71) & ~ 0x3fULL) == 0) &&
            ((1ULL << (_la - 71)) & ((1ULL << (JavaLabeledParser::GT - 71))
            | (1ULL << (JavaLabeledParser::LT - 71))
            | (1ULL << (JavaLabeledParser::LE - 71))
            | (1ULL << (JavaLabeledParser::GE - 71)))) != 0))) {
            antlrcpp::downCast<Expression12Context *>(_localctx)->bop = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(1155);
          expression(15);
          break;
        }

        case 5: {
          auto newContext = _tracker.createInstance<Expression14Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1156);

          if (!(precpred(_ctx, 12))) throw FailedPredicateException(this, "precpred(_ctx, 12)");
          setState(1157);
          antlrcpp::downCast<Expression14Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == JavaLabeledParser::EQUAL

          || _la == JavaLabeledParser::NOTEQUAL)) {
            antlrcpp::downCast<Expression14Context *>(_localctx)->bop = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(1158);
          expression(13);
          break;
        }

        case 6: {
          auto newContext = _tracker.createInstance<Expression15Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1159);

          if (!(precpred(_ctx, 11))) throw FailedPredicateException(this, "precpred(_ctx, 11)");
          setState(1160);
          antlrcpp::downCast<Expression15Context *>(_localctx)->bop = match(JavaLabeledParser::BITAND);
          setState(1161);
          expression(12);
          break;
        }

        case 7: {
          auto newContext = _tracker.createInstance<Expression16Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1162);

          if (!(precpred(_ctx, 10))) throw FailedPredicateException(this, "precpred(_ctx, 10)");
          setState(1163);
          antlrcpp::downCast<Expression16Context *>(_localctx)->bop = match(JavaLabeledParser::CARET);
          setState(1164);
          expression(11);
          break;
        }

        case 8: {
          auto newContext = _tracker.createInstance<Expression17Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1165);

          if (!(precpred(_ctx, 9))) throw FailedPredicateException(this, "precpred(_ctx, 9)");
          setState(1166);
          antlrcpp::downCast<Expression17Context *>(_localctx)->bop = match(JavaLabeledParser::BITOR);
          setState(1167);
          expression(10);
          break;
        }

        case 9: {
          auto newContext = _tracker.createInstance<Expression18Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1168);

          if (!(precpred(_ctx, 8))) throw FailedPredicateException(this, "precpred(_ctx, 8)");
          setState(1169);
          antlrcpp::downCast<Expression18Context *>(_localctx)->bop = match(JavaLabeledParser::AND);
          setState(1170);
          expression(9);
          break;
        }

        case 10: {
          auto newContext = _tracker.createInstance<Expression19Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1171);

          if (!(precpred(_ctx, 7))) throw FailedPredicateException(this, "precpred(_ctx, 7)");
          setState(1172);
          antlrcpp::downCast<Expression19Context *>(_localctx)->bop = match(JavaLabeledParser::OR);
          setState(1173);
          expression(8);
          break;
        }

        case 11: {
          auto newContext = _tracker.createInstance<Expression20Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1174);

          if (!(precpred(_ctx, 6))) throw FailedPredicateException(this, "precpred(_ctx, 6)");
          setState(1175);
          antlrcpp::downCast<Expression20Context *>(_localctx)->bop = match(JavaLabeledParser::QUESTION);
          setState(1176);
          expression(0);
          setState(1177);
          match(JavaLabeledParser::COLON);
          setState(1178);
          expression(6);
          break;
        }

        case 12: {
          auto newContext = _tracker.createInstance<Expression21Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1180);

          if (!(precpred(_ctx, 5))) throw FailedPredicateException(this, "precpred(_ctx, 5)");
          setState(1181);
          antlrcpp::downCast<Expression21Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(((((_la - 70) & ~ 0x3fULL) == 0) &&
            ((1ULL << (_la - 70)) & ((1ULL << (JavaLabeledParser::ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::ADD_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::SUB_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::MUL_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::DIV_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::AND_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::OR_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::XOR_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::MOD_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::LSHIFT_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::RSHIFT_ASSIGN - 70))
            | (1ULL << (JavaLabeledParser::URSHIFT_ASSIGN - 70)))) != 0))) {
            antlrcpp::downCast<Expression21Context *>(_localctx)->bop = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(1182);
          expression(5);
          break;
        }

        case 13: {
          auto newContext = _tracker.createInstance<Expression1Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1183);

          if (!(precpred(_ctx, 25))) throw FailedPredicateException(this, "precpred(_ctx, 25)");
          setState(1184);
          antlrcpp::downCast<Expression1Context *>(_localctx)->bop = match(JavaLabeledParser::DOT);
          setState(1196);
          _errHandler->sync(this);
          switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 141, _ctx)) {
          case 1: {
            setState(1185);
            match(JavaLabeledParser::IDENTIFIER);
            break;
          }

          case 2: {
            setState(1186);
            methodCall();
            break;
          }

          case 3: {
            setState(1187);
            match(JavaLabeledParser::THIS);
            break;
          }

          case 4: {
            setState(1188);
            match(JavaLabeledParser::NEW);
            setState(1190);
            _errHandler->sync(this);

            _la = _input->LA(1);
            if (_la == JavaLabeledParser::LT) {
              setState(1189);
              nonWildcardTypeArguments();
            }
            setState(1192);
            innerCreator();
            break;
          }

          case 5: {
            setState(1193);
            match(JavaLabeledParser::SUPER);
            setState(1194);
            superSuffix();
            break;
          }

          case 6: {
            setState(1195);
            explicitGenericInvocation();
            break;
          }

          default:
            break;
          }
          break;
        }

        case 14: {
          auto newContext = _tracker.createInstance<Expression2Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1198);

          if (!(precpred(_ctx, 24))) throw FailedPredicateException(this, "precpred(_ctx, 24)");
          setState(1199);
          match(JavaLabeledParser::LBRACK);
          setState(1200);
          expression(0);
          setState(1201);
          match(JavaLabeledParser::RBRACK);
          break;
        }

        case 15: {
          auto newContext = _tracker.createInstance<Expression6Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1203);

          if (!(precpred(_ctx, 20))) throw FailedPredicateException(this, "precpred(_ctx, 20)");
          setState(1204);
          antlrcpp::downCast<Expression6Context *>(_localctx)->postfix = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == JavaLabeledParser::INC

          || _la == JavaLabeledParser::DEC)) {
            antlrcpp::downCast<Expression6Context *>(_localctx)->postfix = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          break;
        }

        case 16: {
          auto newContext = _tracker.createInstance<Expression13Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1205);

          if (!(precpred(_ctx, 13))) throw FailedPredicateException(this, "precpred(_ctx, 13)");
          setState(1206);
          antlrcpp::downCast<Expression13Context *>(_localctx)->bop = match(JavaLabeledParser::INSTANCEOF);
          setState(1207);
          typeType();
          break;
        }

        case 17: {
          auto newContext = _tracker.createInstance<Expression23Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1208);

          if (!(precpred(_ctx, 3))) throw FailedPredicateException(this, "precpred(_ctx, 3)");
          setState(1209);
          match(JavaLabeledParser::COLONCOLON);
          setState(1211);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == JavaLabeledParser::LT) {
            setState(1210);
            typeArguments();
          }
          setState(1213);
          match(JavaLabeledParser::IDENTIFIER);
          break;
        }

        default:
          break;
        } 
      }
      setState(1218);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 144, _ctx);
    }
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }
  return _localctx;
}

//----------------- LambdaExpressionContext ------------------------------------------------------------------

JavaLabeledParser::LambdaExpressionContext::LambdaExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::LambdaParametersContext* JavaLabeledParser::LambdaExpressionContext::lambdaParameters() {
  return getRuleContext<JavaLabeledParser::LambdaParametersContext>(0);
}

tree::TerminalNode* JavaLabeledParser::LambdaExpressionContext::ARROW() {
  return getToken(JavaLabeledParser::ARROW, 0);
}

JavaLabeledParser::LambdaBodyContext* JavaLabeledParser::LambdaExpressionContext::lambdaBody() {
  return getRuleContext<JavaLabeledParser::LambdaBodyContext>(0);
}


size_t JavaLabeledParser::LambdaExpressionContext::getRuleIndex() const {
  return JavaLabeledParser::RuleLambdaExpression;
}

void JavaLabeledParser::LambdaExpressionContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaExpression(this);
}

void JavaLabeledParser::LambdaExpressionContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaExpression(this);
}


antlrcpp::Any JavaLabeledParser::LambdaExpressionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLambdaExpression(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::LambdaExpressionContext* JavaLabeledParser::lambdaExpression() {
  LambdaExpressionContext *_localctx = _tracker.createInstance<LambdaExpressionContext>(_ctx, getState());
  enterRule(_localctx, 168, JavaLabeledParser::RuleLambdaExpression);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1219);
    lambdaParameters();
    setState(1220);
    match(JavaLabeledParser::ARROW);
    setState(1221);
    lambdaBody();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LambdaParametersContext ------------------------------------------------------------------

JavaLabeledParser::LambdaParametersContext::LambdaParametersContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::LambdaParametersContext::getRuleIndex() const {
  return JavaLabeledParser::RuleLambdaParameters;
}

void JavaLabeledParser::LambdaParametersContext::copyFrom(LambdaParametersContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- LambdaParameters0Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::LambdaParameters0Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::LambdaParameters0Context::LambdaParameters0Context(LambdaParametersContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::LambdaParameters0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaParameters0(this);
}
void JavaLabeledParser::LambdaParameters0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaParameters0(this);
}

antlrcpp::Any JavaLabeledParser::LambdaParameters0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLambdaParameters0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- LambdaParameters1Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::LambdaParameters1Context::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::LambdaParameters1Context::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::FormalParameterListContext* JavaLabeledParser::LambdaParameters1Context::formalParameterList() {
  return getRuleContext<JavaLabeledParser::FormalParameterListContext>(0);
}

JavaLabeledParser::LambdaParameters1Context::LambdaParameters1Context(LambdaParametersContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::LambdaParameters1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaParameters1(this);
}
void JavaLabeledParser::LambdaParameters1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaParameters1(this);
}

antlrcpp::Any JavaLabeledParser::LambdaParameters1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLambdaParameters1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- LambdaParameters2Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::LambdaParameters2Context::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::LambdaParameters2Context::IDENTIFIER() {
  return getTokens(JavaLabeledParser::IDENTIFIER);
}

tree::TerminalNode* JavaLabeledParser::LambdaParameters2Context::IDENTIFIER(size_t i) {
  return getToken(JavaLabeledParser::IDENTIFIER, i);
}

tree::TerminalNode* JavaLabeledParser::LambdaParameters2Context::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::LambdaParameters2Context::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::LambdaParameters2Context::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}

JavaLabeledParser::LambdaParameters2Context::LambdaParameters2Context(LambdaParametersContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::LambdaParameters2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaParameters2(this);
}
void JavaLabeledParser::LambdaParameters2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaParameters2(this);
}

antlrcpp::Any JavaLabeledParser::LambdaParameters2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLambdaParameters2(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::LambdaParametersContext* JavaLabeledParser::lambdaParameters() {
  LambdaParametersContext *_localctx = _tracker.createInstance<LambdaParametersContext>(_ctx, getState());
  enterRule(_localctx, 170, JavaLabeledParser::RuleLambdaParameters);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1239);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 147, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::LambdaParameters0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(1223);
      match(JavaLabeledParser::IDENTIFIER);
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::LambdaParameters1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(1224);
      match(JavaLabeledParser::LPAREN);
      setState(1226);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
        | (1ULL << JavaLabeledParser::BYTE)
        | (1ULL << JavaLabeledParser::CHAR)
        | (1ULL << JavaLabeledParser::DOUBLE)
        | (1ULL << JavaLabeledParser::FINAL)
        | (1ULL << JavaLabeledParser::FLOAT)
        | (1ULL << JavaLabeledParser::INT)
        | (1ULL << JavaLabeledParser::LONG)
        | (1ULL << JavaLabeledParser::SHORT))) != 0) || _la == JavaLabeledParser::AT

      || _la == JavaLabeledParser::IDENTIFIER) {
        setState(1225);
        formalParameterList();
      }
      setState(1228);
      match(JavaLabeledParser::RPAREN);
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::LambdaParameters2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(1229);
      match(JavaLabeledParser::LPAREN);
      setState(1230);
      match(JavaLabeledParser::IDENTIFIER);
      setState(1235);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == JavaLabeledParser::COMMA) {
        setState(1231);
        match(JavaLabeledParser::COMMA);
        setState(1232);
        match(JavaLabeledParser::IDENTIFIER);
        setState(1237);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(1238);
      match(JavaLabeledParser::RPAREN);
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LambdaBodyContext ------------------------------------------------------------------

JavaLabeledParser::LambdaBodyContext::LambdaBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::LambdaBodyContext::getRuleIndex() const {
  return JavaLabeledParser::RuleLambdaBody;
}

void JavaLabeledParser::LambdaBodyContext::copyFrom(LambdaBodyContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- LambdaBody0Context ------------------------------------------------------------------

JavaLabeledParser::ExpressionContext* JavaLabeledParser::LambdaBody0Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

JavaLabeledParser::LambdaBody0Context::LambdaBody0Context(LambdaBodyContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::LambdaBody0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaBody0(this);
}
void JavaLabeledParser::LambdaBody0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaBody0(this);
}

antlrcpp::Any JavaLabeledParser::LambdaBody0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLambdaBody0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- LambdaBody1Context ------------------------------------------------------------------

JavaLabeledParser::BlockContext* JavaLabeledParser::LambdaBody1Context::block() {
  return getRuleContext<JavaLabeledParser::BlockContext>(0);
}

JavaLabeledParser::LambdaBody1Context::LambdaBody1Context(LambdaBodyContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::LambdaBody1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaBody1(this);
}
void JavaLabeledParser::LambdaBody1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaBody1(this);
}

antlrcpp::Any JavaLabeledParser::LambdaBody1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitLambdaBody1(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::LambdaBodyContext* JavaLabeledParser::lambdaBody() {
  LambdaBodyContext *_localctx = _tracker.createInstance<LambdaBodyContext>(_ctx, getState());
  enterRule(_localctx, 172, JavaLabeledParser::RuleLambdaBody);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1243);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::NEW:
      case JavaLabeledParser::SHORT:
      case JavaLabeledParser::SUPER:
      case JavaLabeledParser::THIS:
      case JavaLabeledParser::VOID:
      case JavaLabeledParser::DECIMAL_LITERAL:
      case JavaLabeledParser::HEX_LITERAL:
      case JavaLabeledParser::OCT_LITERAL:
      case JavaLabeledParser::BINARY_LITERAL:
      case JavaLabeledParser::FLOAT_LITERAL:
      case JavaLabeledParser::HEX_FLOAT_LITERAL:
      case JavaLabeledParser::BOOL_LITERAL:
      case JavaLabeledParser::CHAR_LITERAL:
      case JavaLabeledParser::STRING_LITERAL:
      case JavaLabeledParser::NULL_LITERAL:
      case JavaLabeledParser::LPAREN:
      case JavaLabeledParser::LT:
      case JavaLabeledParser::BANG:
      case JavaLabeledParser::TILDE:
      case JavaLabeledParser::INC:
      case JavaLabeledParser::DEC:
      case JavaLabeledParser::ADD:
      case JavaLabeledParser::SUB:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        _localctx = _tracker.createInstance<JavaLabeledParser::LambdaBody0Context>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(1241);
        expression(0);
        break;
      }

      case JavaLabeledParser::LBRACE: {
        _localctx = _tracker.createInstance<JavaLabeledParser::LambdaBody1Context>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(1242);
        block();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PrimaryContext ------------------------------------------------------------------

JavaLabeledParser::PrimaryContext::PrimaryContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::PrimaryContext::getRuleIndex() const {
  return JavaLabeledParser::RulePrimary;
}

void JavaLabeledParser::PrimaryContext::copyFrom(PrimaryContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Primary6Context ------------------------------------------------------------------

JavaLabeledParser::NonWildcardTypeArgumentsContext* JavaLabeledParser::Primary6Context::nonWildcardTypeArguments() {
  return getRuleContext<JavaLabeledParser::NonWildcardTypeArgumentsContext>(0);
}

JavaLabeledParser::ExplicitGenericInvocationSuffixContext* JavaLabeledParser::Primary6Context::explicitGenericInvocationSuffix() {
  return getRuleContext<JavaLabeledParser::ExplicitGenericInvocationSuffixContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Primary6Context::THIS() {
  return getToken(JavaLabeledParser::THIS, 0);
}

JavaLabeledParser::ArgumentsContext* JavaLabeledParser::Primary6Context::arguments() {
  return getRuleContext<JavaLabeledParser::ArgumentsContext>(0);
}

JavaLabeledParser::Primary6Context::Primary6Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Primary6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary6(this);
}
void JavaLabeledParser::Primary6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary6(this);
}

antlrcpp::Any JavaLabeledParser::Primary6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPrimary6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary2Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Primary2Context::SUPER() {
  return getToken(JavaLabeledParser::SUPER, 0);
}

JavaLabeledParser::Primary2Context::Primary2Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Primary2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary2(this);
}
void JavaLabeledParser::Primary2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary2(this);
}

antlrcpp::Any JavaLabeledParser::Primary2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPrimary2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary3Context ------------------------------------------------------------------

JavaLabeledParser::LiteralContext* JavaLabeledParser::Primary3Context::literal() {
  return getRuleContext<JavaLabeledParser::LiteralContext>(0);
}

JavaLabeledParser::Primary3Context::Primary3Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Primary3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary3(this);
}
void JavaLabeledParser::Primary3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary3(this);
}

antlrcpp::Any JavaLabeledParser::Primary3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPrimary3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary4Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Primary4Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::Primary4Context::Primary4Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Primary4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary4(this);
}
void JavaLabeledParser::Primary4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary4(this);
}

antlrcpp::Any JavaLabeledParser::Primary4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPrimary4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary5Context ------------------------------------------------------------------

JavaLabeledParser::TypeTypeOrVoidContext* JavaLabeledParser::Primary5Context::typeTypeOrVoid() {
  return getRuleContext<JavaLabeledParser::TypeTypeOrVoidContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Primary5Context::DOT() {
  return getToken(JavaLabeledParser::DOT, 0);
}

tree::TerminalNode* JavaLabeledParser::Primary5Context::CLASS() {
  return getToken(JavaLabeledParser::CLASS, 0);
}

JavaLabeledParser::Primary5Context::Primary5Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Primary5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary5(this);
}
void JavaLabeledParser::Primary5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary5(this);
}

antlrcpp::Any JavaLabeledParser::Primary5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPrimary5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary0Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Primary0Context::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::Primary0Context::expression() {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(0);
}

tree::TerminalNode* JavaLabeledParser::Primary0Context::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::Primary0Context::Primary0Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Primary0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary0(this);
}
void JavaLabeledParser::Primary0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary0(this);
}

antlrcpp::Any JavaLabeledParser::Primary0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPrimary0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary1Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::Primary1Context::THIS() {
  return getToken(JavaLabeledParser::THIS, 0);
}

JavaLabeledParser::Primary1Context::Primary1Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Primary1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary1(this);
}
void JavaLabeledParser::Primary1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary1(this);
}

antlrcpp::Any JavaLabeledParser::Primary1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPrimary1(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::PrimaryContext* JavaLabeledParser::primary() {
  PrimaryContext *_localctx = _tracker.createInstance<PrimaryContext>(_ctx, getState());
  enterRule(_localctx, 174, JavaLabeledParser::RulePrimary);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1263);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 150, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Primary0Context>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(1245);
      match(JavaLabeledParser::LPAREN);
      setState(1246);
      expression(0);
      setState(1247);
      match(JavaLabeledParser::RPAREN);
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Primary1Context>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(1249);
      match(JavaLabeledParser::THIS);
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Primary2Context>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(1250);
      match(JavaLabeledParser::SUPER);
      break;
    }

    case 4: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Primary3Context>(_localctx);
      enterOuterAlt(_localctx, 4);
      setState(1251);
      literal();
      break;
    }

    case 5: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Primary4Context>(_localctx);
      enterOuterAlt(_localctx, 5);
      setState(1252);
      match(JavaLabeledParser::IDENTIFIER);
      break;
    }

    case 6: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Primary5Context>(_localctx);
      enterOuterAlt(_localctx, 6);
      setState(1253);
      typeTypeOrVoid();
      setState(1254);
      match(JavaLabeledParser::DOT);
      setState(1255);
      match(JavaLabeledParser::CLASS);
      break;
    }

    case 7: {
      _localctx = _tracker.createInstance<JavaLabeledParser::Primary6Context>(_localctx);
      enterOuterAlt(_localctx, 7);
      setState(1257);
      nonWildcardTypeArguments();
      setState(1261);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case JavaLabeledParser::SUPER:
        case JavaLabeledParser::IDENTIFIER: {
          setState(1258);
          explicitGenericInvocationSuffix();
          break;
        }

        case JavaLabeledParser::THIS: {
          setState(1259);
          match(JavaLabeledParser::THIS);
          setState(1260);
          arguments();
          break;
        }

      default:
        throw NoViableAltException(this);
      }
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassTypeContext ------------------------------------------------------------------

JavaLabeledParser::ClassTypeContext::ClassTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ClassTypeContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::ClassOrInterfaceTypeContext* JavaLabeledParser::ClassTypeContext::classOrInterfaceType() {
  return getRuleContext<JavaLabeledParser::ClassOrInterfaceTypeContext>(0);
}

tree::TerminalNode* JavaLabeledParser::ClassTypeContext::DOT() {
  return getToken(JavaLabeledParser::DOT, 0);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::ClassTypeContext::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::ClassTypeContext::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}

JavaLabeledParser::TypeArgumentsContext* JavaLabeledParser::ClassTypeContext::typeArguments() {
  return getRuleContext<JavaLabeledParser::TypeArgumentsContext>(0);
}


size_t JavaLabeledParser::ClassTypeContext::getRuleIndex() const {
  return JavaLabeledParser::RuleClassType;
}

void JavaLabeledParser::ClassTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassType(this);
}

void JavaLabeledParser::ClassTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassType(this);
}


antlrcpp::Any JavaLabeledParser::ClassTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassType(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ClassTypeContext* JavaLabeledParser::classType() {
  ClassTypeContext *_localctx = _tracker.createInstance<ClassTypeContext>(_ctx, getState());
  enterRule(_localctx, 176, JavaLabeledParser::RuleClassType);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(1268);
    _errHandler->sync(this);

    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 151, _ctx)) {
    case 1: {
      setState(1265);
      classOrInterfaceType();
      setState(1266);
      match(JavaLabeledParser::DOT);
      break;
    }

    default:
      break;
    }
    setState(1273);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 152, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(1270);
        annotation(); 
      }
      setState(1275);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 152, _ctx);
    }
    setState(1276);
    match(JavaLabeledParser::IDENTIFIER);
    setState(1278);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::LT) {
      setState(1277);
      typeArguments();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- CreatorContext ------------------------------------------------------------------

JavaLabeledParser::CreatorContext::CreatorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::CreatorContext::getRuleIndex() const {
  return JavaLabeledParser::RuleCreator;
}

void JavaLabeledParser::CreatorContext::copyFrom(CreatorContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Creator1Context ------------------------------------------------------------------

JavaLabeledParser::CreatedNameContext* JavaLabeledParser::Creator1Context::createdName() {
  return getRuleContext<JavaLabeledParser::CreatedNameContext>(0);
}

JavaLabeledParser::ArrayCreatorRestContext* JavaLabeledParser::Creator1Context::arrayCreatorRest() {
  return getRuleContext<JavaLabeledParser::ArrayCreatorRestContext>(0);
}

JavaLabeledParser::ClassCreatorRestContext* JavaLabeledParser::Creator1Context::classCreatorRest() {
  return getRuleContext<JavaLabeledParser::ClassCreatorRestContext>(0);
}

JavaLabeledParser::Creator1Context::Creator1Context(CreatorContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Creator1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCreator1(this);
}
void JavaLabeledParser::Creator1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCreator1(this);
}

antlrcpp::Any JavaLabeledParser::Creator1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitCreator1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Creator0Context ------------------------------------------------------------------

JavaLabeledParser::NonWildcardTypeArgumentsContext* JavaLabeledParser::Creator0Context::nonWildcardTypeArguments() {
  return getRuleContext<JavaLabeledParser::NonWildcardTypeArgumentsContext>(0);
}

JavaLabeledParser::CreatedNameContext* JavaLabeledParser::Creator0Context::createdName() {
  return getRuleContext<JavaLabeledParser::CreatedNameContext>(0);
}

JavaLabeledParser::ClassCreatorRestContext* JavaLabeledParser::Creator0Context::classCreatorRest() {
  return getRuleContext<JavaLabeledParser::ClassCreatorRestContext>(0);
}

JavaLabeledParser::Creator0Context::Creator0Context(CreatorContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::Creator0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCreator0(this);
}
void JavaLabeledParser::Creator0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCreator0(this);
}

antlrcpp::Any JavaLabeledParser::Creator0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitCreator0(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::CreatorContext* JavaLabeledParser::creator() {
  CreatorContext *_localctx = _tracker.createInstance<CreatorContext>(_ctx, getState());
  enterRule(_localctx, 178, JavaLabeledParser::RuleCreator);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1289);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::LT: {
        _localctx = _tracker.createInstance<JavaLabeledParser::Creator0Context>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(1280);
        nonWildcardTypeArguments();
        setState(1281);
        createdName();
        setState(1282);
        classCreatorRest();
        break;
      }

      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::SHORT:
      case JavaLabeledParser::IDENTIFIER: {
        _localctx = _tracker.createInstance<JavaLabeledParser::Creator1Context>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(1284);
        createdName();
        setState(1287);
        _errHandler->sync(this);
        switch (_input->LA(1)) {
          case JavaLabeledParser::LBRACK: {
            setState(1285);
            arrayCreatorRest();
            break;
          }

          case JavaLabeledParser::LPAREN: {
            setState(1286);
            classCreatorRest();
            break;
          }

        default:
          throw NoViableAltException(this);
        }
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- CreatedNameContext ------------------------------------------------------------------

JavaLabeledParser::CreatedNameContext::CreatedNameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::CreatedNameContext::getRuleIndex() const {
  return JavaLabeledParser::RuleCreatedName;
}

void JavaLabeledParser::CreatedNameContext::copyFrom(CreatedNameContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- CreatedName0Context ------------------------------------------------------------------

std::vector<tree::TerminalNode *> JavaLabeledParser::CreatedName0Context::IDENTIFIER() {
  return getTokens(JavaLabeledParser::IDENTIFIER);
}

tree::TerminalNode* JavaLabeledParser::CreatedName0Context::IDENTIFIER(size_t i) {
  return getToken(JavaLabeledParser::IDENTIFIER, i);
}

std::vector<JavaLabeledParser::TypeArgumentsOrDiamondContext *> JavaLabeledParser::CreatedName0Context::typeArgumentsOrDiamond() {
  return getRuleContexts<JavaLabeledParser::TypeArgumentsOrDiamondContext>();
}

JavaLabeledParser::TypeArgumentsOrDiamondContext* JavaLabeledParser::CreatedName0Context::typeArgumentsOrDiamond(size_t i) {
  return getRuleContext<JavaLabeledParser::TypeArgumentsOrDiamondContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::CreatedName0Context::DOT() {
  return getTokens(JavaLabeledParser::DOT);
}

tree::TerminalNode* JavaLabeledParser::CreatedName0Context::DOT(size_t i) {
  return getToken(JavaLabeledParser::DOT, i);
}

JavaLabeledParser::CreatedName0Context::CreatedName0Context(CreatedNameContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::CreatedName0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCreatedName0(this);
}
void JavaLabeledParser::CreatedName0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCreatedName0(this);
}

antlrcpp::Any JavaLabeledParser::CreatedName0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitCreatedName0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- CreatedName1Context ------------------------------------------------------------------

JavaLabeledParser::PrimitiveTypeContext* JavaLabeledParser::CreatedName1Context::primitiveType() {
  return getRuleContext<JavaLabeledParser::PrimitiveTypeContext>(0);
}

JavaLabeledParser::CreatedName1Context::CreatedName1Context(CreatedNameContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::CreatedName1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCreatedName1(this);
}
void JavaLabeledParser::CreatedName1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCreatedName1(this);
}

antlrcpp::Any JavaLabeledParser::CreatedName1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitCreatedName1(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::CreatedNameContext* JavaLabeledParser::createdName() {
  CreatedNameContext *_localctx = _tracker.createInstance<CreatedNameContext>(_ctx, getState());
  enterRule(_localctx, 180, JavaLabeledParser::RuleCreatedName);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1306);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::IDENTIFIER: {
        _localctx = _tracker.createInstance<JavaLabeledParser::CreatedName0Context>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(1291);
        match(JavaLabeledParser::IDENTIFIER);
        setState(1293);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if (_la == JavaLabeledParser::LT) {
          setState(1292);
          typeArgumentsOrDiamond();
        }
        setState(1302);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while (_la == JavaLabeledParser::DOT) {
          setState(1295);
          match(JavaLabeledParser::DOT);
          setState(1296);
          match(JavaLabeledParser::IDENTIFIER);
          setState(1298);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == JavaLabeledParser::LT) {
            setState(1297);
            typeArgumentsOrDiamond();
          }
          setState(1304);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        break;
      }

      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::SHORT: {
        _localctx = _tracker.createInstance<JavaLabeledParser::CreatedName1Context>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(1305);
        primitiveType();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InnerCreatorContext ------------------------------------------------------------------

JavaLabeledParser::InnerCreatorContext::InnerCreatorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::InnerCreatorContext::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::ClassCreatorRestContext* JavaLabeledParser::InnerCreatorContext::classCreatorRest() {
  return getRuleContext<JavaLabeledParser::ClassCreatorRestContext>(0);
}

JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext* JavaLabeledParser::InnerCreatorContext::nonWildcardTypeArgumentsOrDiamond() {
  return getRuleContext<JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext>(0);
}


size_t JavaLabeledParser::InnerCreatorContext::getRuleIndex() const {
  return JavaLabeledParser::RuleInnerCreator;
}

void JavaLabeledParser::InnerCreatorContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInnerCreator(this);
}

void JavaLabeledParser::InnerCreatorContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInnerCreator(this);
}


antlrcpp::Any JavaLabeledParser::InnerCreatorContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitInnerCreator(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::InnerCreatorContext* JavaLabeledParser::innerCreator() {
  InnerCreatorContext *_localctx = _tracker.createInstance<InnerCreatorContext>(_ctx, getState());
  enterRule(_localctx, 182, JavaLabeledParser::RuleInnerCreator);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1308);
    match(JavaLabeledParser::IDENTIFIER);
    setState(1310);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaLabeledParser::LT) {
      setState(1309);
      nonWildcardTypeArgumentsOrDiamond();
    }
    setState(1312);
    classCreatorRest();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ArrayCreatorRestContext ------------------------------------------------------------------

JavaLabeledParser::ArrayCreatorRestContext::ArrayCreatorRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ArrayCreatorRestContext::LBRACK() {
  return getTokens(JavaLabeledParser::LBRACK);
}

tree::TerminalNode* JavaLabeledParser::ArrayCreatorRestContext::LBRACK(size_t i) {
  return getToken(JavaLabeledParser::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::ArrayCreatorRestContext::RBRACK() {
  return getTokens(JavaLabeledParser::RBRACK);
}

tree::TerminalNode* JavaLabeledParser::ArrayCreatorRestContext::RBRACK(size_t i) {
  return getToken(JavaLabeledParser::RBRACK, i);
}

JavaLabeledParser::ArrayInitializerContext* JavaLabeledParser::ArrayCreatorRestContext::arrayInitializer() {
  return getRuleContext<JavaLabeledParser::ArrayInitializerContext>(0);
}

std::vector<JavaLabeledParser::ExpressionContext *> JavaLabeledParser::ArrayCreatorRestContext::expression() {
  return getRuleContexts<JavaLabeledParser::ExpressionContext>();
}

JavaLabeledParser::ExpressionContext* JavaLabeledParser::ArrayCreatorRestContext::expression(size_t i) {
  return getRuleContext<JavaLabeledParser::ExpressionContext>(i);
}


size_t JavaLabeledParser::ArrayCreatorRestContext::getRuleIndex() const {
  return JavaLabeledParser::RuleArrayCreatorRest;
}

void JavaLabeledParser::ArrayCreatorRestContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterArrayCreatorRest(this);
}

void JavaLabeledParser::ArrayCreatorRestContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitArrayCreatorRest(this);
}


antlrcpp::Any JavaLabeledParser::ArrayCreatorRestContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitArrayCreatorRest(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ArrayCreatorRestContext* JavaLabeledParser::arrayCreatorRest() {
  ArrayCreatorRestContext *_localctx = _tracker.createInstance<ArrayCreatorRestContext>(_ctx, getState());
  enterRule(_localctx, 184, JavaLabeledParser::RuleArrayCreatorRest);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(1314);
    match(JavaLabeledParser::LBRACK);
    setState(1342);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::RBRACK: {
        setState(1315);
        match(JavaLabeledParser::RBRACK);
        setState(1320);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while (_la == JavaLabeledParser::LBRACK) {
          setState(1316);
          match(JavaLabeledParser::LBRACK);
          setState(1317);
          match(JavaLabeledParser::RBRACK);
          setState(1322);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        setState(1323);
        arrayInitializer();
        break;
      }

      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::NEW:
      case JavaLabeledParser::SHORT:
      case JavaLabeledParser::SUPER:
      case JavaLabeledParser::THIS:
      case JavaLabeledParser::VOID:
      case JavaLabeledParser::DECIMAL_LITERAL:
      case JavaLabeledParser::HEX_LITERAL:
      case JavaLabeledParser::OCT_LITERAL:
      case JavaLabeledParser::BINARY_LITERAL:
      case JavaLabeledParser::FLOAT_LITERAL:
      case JavaLabeledParser::HEX_FLOAT_LITERAL:
      case JavaLabeledParser::BOOL_LITERAL:
      case JavaLabeledParser::CHAR_LITERAL:
      case JavaLabeledParser::STRING_LITERAL:
      case JavaLabeledParser::NULL_LITERAL:
      case JavaLabeledParser::LPAREN:
      case JavaLabeledParser::LT:
      case JavaLabeledParser::BANG:
      case JavaLabeledParser::TILDE:
      case JavaLabeledParser::INC:
      case JavaLabeledParser::DEC:
      case JavaLabeledParser::ADD:
      case JavaLabeledParser::SUB:
      case JavaLabeledParser::AT:
      case JavaLabeledParser::IDENTIFIER: {
        setState(1324);
        expression(0);
        setState(1325);
        match(JavaLabeledParser::RBRACK);
        setState(1332);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 162, _ctx);
        while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
          if (alt == 1) {
            setState(1326);
            match(JavaLabeledParser::LBRACK);
            setState(1327);
            expression(0);
            setState(1328);
            match(JavaLabeledParser::RBRACK); 
          }
          setState(1334);
          _errHandler->sync(this);
          alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 162, _ctx);
        }
        setState(1339);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 163, _ctx);
        while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
          if (alt == 1) {
            setState(1335);
            match(JavaLabeledParser::LBRACK);
            setState(1336);
            match(JavaLabeledParser::RBRACK); 
          }
          setState(1341);
          _errHandler->sync(this);
          alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 163, _ctx);
        }
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassCreatorRestContext ------------------------------------------------------------------

JavaLabeledParser::ClassCreatorRestContext::ClassCreatorRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::ArgumentsContext* JavaLabeledParser::ClassCreatorRestContext::arguments() {
  return getRuleContext<JavaLabeledParser::ArgumentsContext>(0);
}

JavaLabeledParser::ClassBodyContext* JavaLabeledParser::ClassCreatorRestContext::classBody() {
  return getRuleContext<JavaLabeledParser::ClassBodyContext>(0);
}


size_t JavaLabeledParser::ClassCreatorRestContext::getRuleIndex() const {
  return JavaLabeledParser::RuleClassCreatorRest;
}

void JavaLabeledParser::ClassCreatorRestContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassCreatorRest(this);
}

void JavaLabeledParser::ClassCreatorRestContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassCreatorRest(this);
}


antlrcpp::Any JavaLabeledParser::ClassCreatorRestContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitClassCreatorRest(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ClassCreatorRestContext* JavaLabeledParser::classCreatorRest() {
  ClassCreatorRestContext *_localctx = _tracker.createInstance<ClassCreatorRestContext>(_ctx, getState());
  enterRule(_localctx, 186, JavaLabeledParser::RuleClassCreatorRest);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1344);
    arguments();
    setState(1346);
    _errHandler->sync(this);

    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 165, _ctx)) {
    case 1: {
      setState(1345);
      classBody();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExplicitGenericInvocationContext ------------------------------------------------------------------

JavaLabeledParser::ExplicitGenericInvocationContext::ExplicitGenericInvocationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::NonWildcardTypeArgumentsContext* JavaLabeledParser::ExplicitGenericInvocationContext::nonWildcardTypeArguments() {
  return getRuleContext<JavaLabeledParser::NonWildcardTypeArgumentsContext>(0);
}

JavaLabeledParser::ExplicitGenericInvocationSuffixContext* JavaLabeledParser::ExplicitGenericInvocationContext::explicitGenericInvocationSuffix() {
  return getRuleContext<JavaLabeledParser::ExplicitGenericInvocationSuffixContext>(0);
}


size_t JavaLabeledParser::ExplicitGenericInvocationContext::getRuleIndex() const {
  return JavaLabeledParser::RuleExplicitGenericInvocation;
}

void JavaLabeledParser::ExplicitGenericInvocationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExplicitGenericInvocation(this);
}

void JavaLabeledParser::ExplicitGenericInvocationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExplicitGenericInvocation(this);
}


antlrcpp::Any JavaLabeledParser::ExplicitGenericInvocationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExplicitGenericInvocation(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ExplicitGenericInvocationContext* JavaLabeledParser::explicitGenericInvocation() {
  ExplicitGenericInvocationContext *_localctx = _tracker.createInstance<ExplicitGenericInvocationContext>(_ctx, getState());
  enterRule(_localctx, 188, JavaLabeledParser::RuleExplicitGenericInvocation);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1348);
    nonWildcardTypeArguments();
    setState(1349);
    explicitGenericInvocationSuffix();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeArgumentsOrDiamondContext ------------------------------------------------------------------

JavaLabeledParser::TypeArgumentsOrDiamondContext::TypeArgumentsOrDiamondContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::TypeArgumentsOrDiamondContext::LT() {
  return getToken(JavaLabeledParser::LT, 0);
}

tree::TerminalNode* JavaLabeledParser::TypeArgumentsOrDiamondContext::GT() {
  return getToken(JavaLabeledParser::GT, 0);
}

JavaLabeledParser::TypeArgumentsContext* JavaLabeledParser::TypeArgumentsOrDiamondContext::typeArguments() {
  return getRuleContext<JavaLabeledParser::TypeArgumentsContext>(0);
}


size_t JavaLabeledParser::TypeArgumentsOrDiamondContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeArgumentsOrDiamond;
}

void JavaLabeledParser::TypeArgumentsOrDiamondContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeArgumentsOrDiamond(this);
}

void JavaLabeledParser::TypeArgumentsOrDiamondContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeArgumentsOrDiamond(this);
}


antlrcpp::Any JavaLabeledParser::TypeArgumentsOrDiamondContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeArgumentsOrDiamond(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeArgumentsOrDiamondContext* JavaLabeledParser::typeArgumentsOrDiamond() {
  TypeArgumentsOrDiamondContext *_localctx = _tracker.createInstance<TypeArgumentsOrDiamondContext>(_ctx, getState());
  enterRule(_localctx, 190, JavaLabeledParser::RuleTypeArgumentsOrDiamond);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1354);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 166, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(1351);
      match(JavaLabeledParser::LT);
      setState(1352);
      match(JavaLabeledParser::GT);
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(1353);
      typeArguments();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- NonWildcardTypeArgumentsOrDiamondContext ------------------------------------------------------------------

JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext::NonWildcardTypeArgumentsOrDiamondContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext::LT() {
  return getToken(JavaLabeledParser::LT, 0);
}

tree::TerminalNode* JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext::GT() {
  return getToken(JavaLabeledParser::GT, 0);
}

JavaLabeledParser::NonWildcardTypeArgumentsContext* JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext::nonWildcardTypeArguments() {
  return getRuleContext<JavaLabeledParser::NonWildcardTypeArgumentsContext>(0);
}


size_t JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext::getRuleIndex() const {
  return JavaLabeledParser::RuleNonWildcardTypeArgumentsOrDiamond;
}

void JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterNonWildcardTypeArgumentsOrDiamond(this);
}

void JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitNonWildcardTypeArgumentsOrDiamond(this);
}


antlrcpp::Any JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitNonWildcardTypeArgumentsOrDiamond(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::NonWildcardTypeArgumentsOrDiamondContext* JavaLabeledParser::nonWildcardTypeArgumentsOrDiamond() {
  NonWildcardTypeArgumentsOrDiamondContext *_localctx = _tracker.createInstance<NonWildcardTypeArgumentsOrDiamondContext>(_ctx, getState());
  enterRule(_localctx, 192, JavaLabeledParser::RuleNonWildcardTypeArgumentsOrDiamond);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1359);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 167, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(1356);
      match(JavaLabeledParser::LT);
      setState(1357);
      match(JavaLabeledParser::GT);
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(1358);
      nonWildcardTypeArguments();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- NonWildcardTypeArgumentsContext ------------------------------------------------------------------

JavaLabeledParser::NonWildcardTypeArgumentsContext::NonWildcardTypeArgumentsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::NonWildcardTypeArgumentsContext::LT() {
  return getToken(JavaLabeledParser::LT, 0);
}

JavaLabeledParser::TypeListContext* JavaLabeledParser::NonWildcardTypeArgumentsContext::typeList() {
  return getRuleContext<JavaLabeledParser::TypeListContext>(0);
}

tree::TerminalNode* JavaLabeledParser::NonWildcardTypeArgumentsContext::GT() {
  return getToken(JavaLabeledParser::GT, 0);
}


size_t JavaLabeledParser::NonWildcardTypeArgumentsContext::getRuleIndex() const {
  return JavaLabeledParser::RuleNonWildcardTypeArguments;
}

void JavaLabeledParser::NonWildcardTypeArgumentsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterNonWildcardTypeArguments(this);
}

void JavaLabeledParser::NonWildcardTypeArgumentsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitNonWildcardTypeArguments(this);
}


antlrcpp::Any JavaLabeledParser::NonWildcardTypeArgumentsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitNonWildcardTypeArguments(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::NonWildcardTypeArgumentsContext* JavaLabeledParser::nonWildcardTypeArguments() {
  NonWildcardTypeArgumentsContext *_localctx = _tracker.createInstance<NonWildcardTypeArgumentsContext>(_ctx, getState());
  enterRule(_localctx, 194, JavaLabeledParser::RuleNonWildcardTypeArguments);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1361);
    match(JavaLabeledParser::LT);
    setState(1362);
    typeList();
    setState(1363);
    match(JavaLabeledParser::GT);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeListContext ------------------------------------------------------------------

JavaLabeledParser::TypeListContext::TypeListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaLabeledParser::TypeTypeContext *> JavaLabeledParser::TypeListContext::typeType() {
  return getRuleContexts<JavaLabeledParser::TypeTypeContext>();
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::TypeListContext::typeType(size_t i) {
  return getRuleContext<JavaLabeledParser::TypeTypeContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::TypeListContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::TypeListContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::TypeListContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeList;
}

void JavaLabeledParser::TypeListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeList(this);
}

void JavaLabeledParser::TypeListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeList(this);
}


antlrcpp::Any JavaLabeledParser::TypeListContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeList(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeListContext* JavaLabeledParser::typeList() {
  TypeListContext *_localctx = _tracker.createInstance<TypeListContext>(_ctx, getState());
  enterRule(_localctx, 196, JavaLabeledParser::RuleTypeList);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1365);
    typeType();
    setState(1370);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::COMMA) {
      setState(1366);
      match(JavaLabeledParser::COMMA);
      setState(1367);
      typeType();
      setState(1372);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeTypeContext ------------------------------------------------------------------

JavaLabeledParser::TypeTypeContext::TypeTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaLabeledParser::ClassOrInterfaceTypeContext* JavaLabeledParser::TypeTypeContext::classOrInterfaceType() {
  return getRuleContext<JavaLabeledParser::ClassOrInterfaceTypeContext>(0);
}

JavaLabeledParser::PrimitiveTypeContext* JavaLabeledParser::TypeTypeContext::primitiveType() {
  return getRuleContext<JavaLabeledParser::PrimitiveTypeContext>(0);
}

std::vector<JavaLabeledParser::AnnotationContext *> JavaLabeledParser::TypeTypeContext::annotation() {
  return getRuleContexts<JavaLabeledParser::AnnotationContext>();
}

JavaLabeledParser::AnnotationContext* JavaLabeledParser::TypeTypeContext::annotation(size_t i) {
  return getRuleContext<JavaLabeledParser::AnnotationContext>(i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::TypeTypeContext::LBRACK() {
  return getTokens(JavaLabeledParser::LBRACK);
}

tree::TerminalNode* JavaLabeledParser::TypeTypeContext::LBRACK(size_t i) {
  return getToken(JavaLabeledParser::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::TypeTypeContext::RBRACK() {
  return getTokens(JavaLabeledParser::RBRACK);
}

tree::TerminalNode* JavaLabeledParser::TypeTypeContext::RBRACK(size_t i) {
  return getToken(JavaLabeledParser::RBRACK, i);
}


size_t JavaLabeledParser::TypeTypeContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeType;
}

void JavaLabeledParser::TypeTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeType(this);
}

void JavaLabeledParser::TypeTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeType(this);
}


antlrcpp::Any JavaLabeledParser::TypeTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeType(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeTypeContext* JavaLabeledParser::typeType() {
  TypeTypeContext *_localctx = _tracker.createInstance<TypeTypeContext>(_ctx, getState());
  enterRule(_localctx, 198, JavaLabeledParser::RuleTypeType);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(1376);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 169, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(1373);
        annotation(); 
      }
      setState(1378);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 169, _ctx);
    }
    setState(1381);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::IDENTIFIER: {
        setState(1379);
        classOrInterfaceType();
        break;
      }

      case JavaLabeledParser::BOOLEAN:
      case JavaLabeledParser::BYTE:
      case JavaLabeledParser::CHAR:
      case JavaLabeledParser::DOUBLE:
      case JavaLabeledParser::FLOAT:
      case JavaLabeledParser::INT:
      case JavaLabeledParser::LONG:
      case JavaLabeledParser::SHORT: {
        setState(1380);
        primitiveType();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
    setState(1393);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 172, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(1386);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while (_la == JavaLabeledParser::AT

        || _la == JavaLabeledParser::IDENTIFIER) {
          setState(1383);
          annotation();
          setState(1388);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        setState(1389);
        match(JavaLabeledParser::LBRACK);
        setState(1390);
        match(JavaLabeledParser::RBRACK); 
      }
      setState(1395);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 172, _ctx);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PrimitiveTypeContext ------------------------------------------------------------------

JavaLabeledParser::PrimitiveTypeContext::PrimitiveTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::PrimitiveTypeContext::BOOLEAN() {
  return getToken(JavaLabeledParser::BOOLEAN, 0);
}

tree::TerminalNode* JavaLabeledParser::PrimitiveTypeContext::CHAR() {
  return getToken(JavaLabeledParser::CHAR, 0);
}

tree::TerminalNode* JavaLabeledParser::PrimitiveTypeContext::BYTE() {
  return getToken(JavaLabeledParser::BYTE, 0);
}

tree::TerminalNode* JavaLabeledParser::PrimitiveTypeContext::SHORT() {
  return getToken(JavaLabeledParser::SHORT, 0);
}

tree::TerminalNode* JavaLabeledParser::PrimitiveTypeContext::INT() {
  return getToken(JavaLabeledParser::INT, 0);
}

tree::TerminalNode* JavaLabeledParser::PrimitiveTypeContext::LONG() {
  return getToken(JavaLabeledParser::LONG, 0);
}

tree::TerminalNode* JavaLabeledParser::PrimitiveTypeContext::FLOAT() {
  return getToken(JavaLabeledParser::FLOAT, 0);
}

tree::TerminalNode* JavaLabeledParser::PrimitiveTypeContext::DOUBLE() {
  return getToken(JavaLabeledParser::DOUBLE, 0);
}


size_t JavaLabeledParser::PrimitiveTypeContext::getRuleIndex() const {
  return JavaLabeledParser::RulePrimitiveType;
}

void JavaLabeledParser::PrimitiveTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimitiveType(this);
}

void JavaLabeledParser::PrimitiveTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimitiveType(this);
}


antlrcpp::Any JavaLabeledParser::PrimitiveTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitPrimitiveType(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::PrimitiveTypeContext* JavaLabeledParser::primitiveType() {
  PrimitiveTypeContext *_localctx = _tracker.createInstance<PrimitiveTypeContext>(_ctx, getState());
  enterRule(_localctx, 200, JavaLabeledParser::RulePrimitiveType);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1396);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::SHORT))) != 0))) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeArgumentsContext ------------------------------------------------------------------

JavaLabeledParser::TypeArgumentsContext::TypeArgumentsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::TypeArgumentsContext::LT() {
  return getToken(JavaLabeledParser::LT, 0);
}

std::vector<JavaLabeledParser::TypeArgumentContext *> JavaLabeledParser::TypeArgumentsContext::typeArgument() {
  return getRuleContexts<JavaLabeledParser::TypeArgumentContext>();
}

JavaLabeledParser::TypeArgumentContext* JavaLabeledParser::TypeArgumentsContext::typeArgument(size_t i) {
  return getRuleContext<JavaLabeledParser::TypeArgumentContext>(i);
}

tree::TerminalNode* JavaLabeledParser::TypeArgumentsContext::GT() {
  return getToken(JavaLabeledParser::GT, 0);
}

std::vector<tree::TerminalNode *> JavaLabeledParser::TypeArgumentsContext::COMMA() {
  return getTokens(JavaLabeledParser::COMMA);
}

tree::TerminalNode* JavaLabeledParser::TypeArgumentsContext::COMMA(size_t i) {
  return getToken(JavaLabeledParser::COMMA, i);
}


size_t JavaLabeledParser::TypeArgumentsContext::getRuleIndex() const {
  return JavaLabeledParser::RuleTypeArguments;
}

void JavaLabeledParser::TypeArgumentsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeArguments(this);
}

void JavaLabeledParser::TypeArgumentsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeArguments(this);
}


antlrcpp::Any JavaLabeledParser::TypeArgumentsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitTypeArguments(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::TypeArgumentsContext* JavaLabeledParser::typeArguments() {
  TypeArgumentsContext *_localctx = _tracker.createInstance<TypeArgumentsContext>(_ctx, getState());
  enterRule(_localctx, 202, JavaLabeledParser::RuleTypeArguments);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1398);
    match(JavaLabeledParser::LT);
    setState(1399);
    typeArgument();
    setState(1404);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaLabeledParser::COMMA) {
      setState(1400);
      match(JavaLabeledParser::COMMA);
      setState(1401);
      typeArgument();
      setState(1406);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(1407);
    match(JavaLabeledParser::GT);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SuperSuffixContext ------------------------------------------------------------------

JavaLabeledParser::SuperSuffixContext::SuperSuffixContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::SuperSuffixContext::getRuleIndex() const {
  return JavaLabeledParser::RuleSuperSuffix;
}

void JavaLabeledParser::SuperSuffixContext::copyFrom(SuperSuffixContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- SuperSuffix1Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::SuperSuffix1Context::DOT() {
  return getToken(JavaLabeledParser::DOT, 0);
}

tree::TerminalNode* JavaLabeledParser::SuperSuffix1Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::ArgumentsContext* JavaLabeledParser::SuperSuffix1Context::arguments() {
  return getRuleContext<JavaLabeledParser::ArgumentsContext>(0);
}

JavaLabeledParser::SuperSuffix1Context::SuperSuffix1Context(SuperSuffixContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::SuperSuffix1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSuperSuffix1(this);
}
void JavaLabeledParser::SuperSuffix1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSuperSuffix1(this);
}

antlrcpp::Any JavaLabeledParser::SuperSuffix1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitSuperSuffix1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- SuperSuffix0Context ------------------------------------------------------------------

JavaLabeledParser::ArgumentsContext* JavaLabeledParser::SuperSuffix0Context::arguments() {
  return getRuleContext<JavaLabeledParser::ArgumentsContext>(0);
}

JavaLabeledParser::SuperSuffix0Context::SuperSuffix0Context(SuperSuffixContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::SuperSuffix0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSuperSuffix0(this);
}
void JavaLabeledParser::SuperSuffix0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSuperSuffix0(this);
}

antlrcpp::Any JavaLabeledParser::SuperSuffix0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitSuperSuffix0(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::SuperSuffixContext* JavaLabeledParser::superSuffix() {
  SuperSuffixContext *_localctx = _tracker.createInstance<SuperSuffixContext>(_ctx, getState());
  enterRule(_localctx, 204, JavaLabeledParser::RuleSuperSuffix);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1415);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::LPAREN: {
        _localctx = _tracker.createInstance<JavaLabeledParser::SuperSuffix0Context>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(1409);
        arguments();
        break;
      }

      case JavaLabeledParser::DOT: {
        _localctx = _tracker.createInstance<JavaLabeledParser::SuperSuffix1Context>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(1410);
        match(JavaLabeledParser::DOT);
        setState(1411);
        match(JavaLabeledParser::IDENTIFIER);
        setState(1413);
        _errHandler->sync(this);

        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 174, _ctx)) {
        case 1: {
          setState(1412);
          arguments();
          break;
        }

        default:
          break;
        }
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExplicitGenericInvocationSuffixContext ------------------------------------------------------------------

JavaLabeledParser::ExplicitGenericInvocationSuffixContext::ExplicitGenericInvocationSuffixContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaLabeledParser::ExplicitGenericInvocationSuffixContext::getRuleIndex() const {
  return JavaLabeledParser::RuleExplicitGenericInvocationSuffix;
}

void JavaLabeledParser::ExplicitGenericInvocationSuffixContext::copyFrom(ExplicitGenericInvocationSuffixContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ExplicitGenericInvocationSuffix0Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::ExplicitGenericInvocationSuffix0Context::SUPER() {
  return getToken(JavaLabeledParser::SUPER, 0);
}

JavaLabeledParser::SuperSuffixContext* JavaLabeledParser::ExplicitGenericInvocationSuffix0Context::superSuffix() {
  return getRuleContext<JavaLabeledParser::SuperSuffixContext>(0);
}

JavaLabeledParser::ExplicitGenericInvocationSuffix0Context::ExplicitGenericInvocationSuffix0Context(ExplicitGenericInvocationSuffixContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ExplicitGenericInvocationSuffix0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExplicitGenericInvocationSuffix0(this);
}
void JavaLabeledParser::ExplicitGenericInvocationSuffix0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExplicitGenericInvocationSuffix0(this);
}

antlrcpp::Any JavaLabeledParser::ExplicitGenericInvocationSuffix0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExplicitGenericInvocationSuffix0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ExplicitGenericInvocationSuffix1Context ------------------------------------------------------------------

tree::TerminalNode* JavaLabeledParser::ExplicitGenericInvocationSuffix1Context::IDENTIFIER() {
  return getToken(JavaLabeledParser::IDENTIFIER, 0);
}

JavaLabeledParser::ArgumentsContext* JavaLabeledParser::ExplicitGenericInvocationSuffix1Context::arguments() {
  return getRuleContext<JavaLabeledParser::ArgumentsContext>(0);
}

JavaLabeledParser::ExplicitGenericInvocationSuffix1Context::ExplicitGenericInvocationSuffix1Context(ExplicitGenericInvocationSuffixContext *ctx) { copyFrom(ctx); }

void JavaLabeledParser::ExplicitGenericInvocationSuffix1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExplicitGenericInvocationSuffix1(this);
}
void JavaLabeledParser::ExplicitGenericInvocationSuffix1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExplicitGenericInvocationSuffix1(this);
}

antlrcpp::Any JavaLabeledParser::ExplicitGenericInvocationSuffix1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitExplicitGenericInvocationSuffix1(this);
  else
    return visitor->visitChildren(this);
}
JavaLabeledParser::ExplicitGenericInvocationSuffixContext* JavaLabeledParser::explicitGenericInvocationSuffix() {
  ExplicitGenericInvocationSuffixContext *_localctx = _tracker.createInstance<ExplicitGenericInvocationSuffixContext>(_ctx, getState());
  enterRule(_localctx, 206, JavaLabeledParser::RuleExplicitGenericInvocationSuffix);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(1421);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaLabeledParser::SUPER: {
        _localctx = _tracker.createInstance<JavaLabeledParser::ExplicitGenericInvocationSuffix0Context>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(1417);
        match(JavaLabeledParser::SUPER);
        setState(1418);
        superSuffix();
        break;
      }

      case JavaLabeledParser::IDENTIFIER: {
        _localctx = _tracker.createInstance<JavaLabeledParser::ExplicitGenericInvocationSuffix1Context>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(1419);
        match(JavaLabeledParser::IDENTIFIER);
        setState(1420);
        arguments();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ArgumentsContext ------------------------------------------------------------------

JavaLabeledParser::ArgumentsContext::ArgumentsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaLabeledParser::ArgumentsContext::LPAREN() {
  return getToken(JavaLabeledParser::LPAREN, 0);
}

tree::TerminalNode* JavaLabeledParser::ArgumentsContext::RPAREN() {
  return getToken(JavaLabeledParser::RPAREN, 0);
}

JavaLabeledParser::ExpressionListContext* JavaLabeledParser::ArgumentsContext::expressionList() {
  return getRuleContext<JavaLabeledParser::ExpressionListContext>(0);
}


size_t JavaLabeledParser::ArgumentsContext::getRuleIndex() const {
  return JavaLabeledParser::RuleArguments;
}

void JavaLabeledParser::ArgumentsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterArguments(this);
}

void JavaLabeledParser::ArgumentsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaLabeledParserListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitArguments(this);
}


antlrcpp::Any JavaLabeledParser::ArgumentsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaLabeledParserVisitor*>(visitor))
    return parserVisitor->visitArguments(this);
  else
    return visitor->visitChildren(this);
}

JavaLabeledParser::ArgumentsContext* JavaLabeledParser::arguments() {
  ArgumentsContext *_localctx = _tracker.createInstance<ArgumentsContext>(_ctx, getState());
  enterRule(_localctx, 208, JavaLabeledParser::RuleArguments);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(1423);
    match(JavaLabeledParser::LPAREN);
    setState(1425);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaLabeledParser::BOOLEAN)
      | (1ULL << JavaLabeledParser::BYTE)
      | (1ULL << JavaLabeledParser::CHAR)
      | (1ULL << JavaLabeledParser::DOUBLE)
      | (1ULL << JavaLabeledParser::FLOAT)
      | (1ULL << JavaLabeledParser::INT)
      | (1ULL << JavaLabeledParser::LONG)
      | (1ULL << JavaLabeledParser::NEW)
      | (1ULL << JavaLabeledParser::SHORT)
      | (1ULL << JavaLabeledParser::SUPER)
      | (1ULL << JavaLabeledParser::THIS)
      | (1ULL << JavaLabeledParser::VOID)
      | (1ULL << JavaLabeledParser::DECIMAL_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_LITERAL)
      | (1ULL << JavaLabeledParser::OCT_LITERAL)
      | (1ULL << JavaLabeledParser::BINARY_LITERAL)
      | (1ULL << JavaLabeledParser::FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::HEX_FLOAT_LITERAL)
      | (1ULL << JavaLabeledParser::BOOL_LITERAL)
      | (1ULL << JavaLabeledParser::CHAR_LITERAL)
      | (1ULL << JavaLabeledParser::STRING_LITERAL)
      | (1ULL << JavaLabeledParser::NULL_LITERAL)
      | (1ULL << JavaLabeledParser::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 72)) & ((1ULL << (JavaLabeledParser::LT - 72))
      | (1ULL << (JavaLabeledParser::BANG - 72))
      | (1ULL << (JavaLabeledParser::TILDE - 72))
      | (1ULL << (JavaLabeledParser::INC - 72))
      | (1ULL << (JavaLabeledParser::DEC - 72))
      | (1ULL << (JavaLabeledParser::ADD - 72))
      | (1ULL << (JavaLabeledParser::SUB - 72))
      | (1ULL << (JavaLabeledParser::AT - 72))
      | (1ULL << (JavaLabeledParser::IDENTIFIER - 72)))) != 0)) {
      setState(1424);
      expressionList();
    }
    setState(1427);
    match(JavaLabeledParser::RPAREN);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

bool JavaLabeledParser::sempred(RuleContext *context, size_t ruleIndex, size_t predicateIndex) {
  switch (ruleIndex) {
    case 83: return expressionSempred(antlrcpp::downCast<ExpressionContext *>(context), predicateIndex);

  default:
    break;
  }
  return true;
}

bool JavaLabeledParser::expressionSempred(ExpressionContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 0: return precpred(_ctx, 17);
    case 1: return precpred(_ctx, 16);
    case 2: return precpred(_ctx, 15);
    case 3: return precpred(_ctx, 14);
    case 4: return precpred(_ctx, 12);
    case 5: return precpred(_ctx, 11);
    case 6: return precpred(_ctx, 10);
    case 7: return precpred(_ctx, 9);
    case 8: return precpred(_ctx, 8);
    case 9: return precpred(_ctx, 7);
    case 10: return precpred(_ctx, 6);
    case 11: return precpred(_ctx, 5);
    case 12: return precpred(_ctx, 25);
    case 13: return precpred(_ctx, 24);
    case 14: return precpred(_ctx, 20);
    case 15: return precpred(_ctx, 13);
    case 16: return precpred(_ctx, 3);

  default:
    break;
  }
  return true;
}

// Static vars and initialization.
std::vector<dfa::DFA> JavaLabeledParser::_decisionToDFA;
atn::PredictionContextCache JavaLabeledParser::_sharedContextCache;

// We own the ATN which in turn owns the ATN states.
atn::ATN JavaLabeledParser::_atn;
std::vector<uint16_t> JavaLabeledParser::_serializedATN;

std::vector<std::string> JavaLabeledParser::_ruleNames = {
  "compilationUnit", "packageDeclaration", "importDeclaration", "typeDeclaration", 
  "modifier", "classOrInterfaceModifier", "variableModifier", "classDeclaration", 
  "typeParameters", "typeParameter", "typeBound", "enumDeclaration", "enumConstants", 
  "enumConstant", "enumBodyDeclarations", "interfaceDeclaration", "classBody", 
  "interfaceBody", "classBodyDeclaration", "memberDeclaration", "methodDeclaration", 
  "methodBody", "typeTypeOrVoid", "genericMethodDeclaration", "genericConstructorDeclaration", 
  "constructorDeclaration", "fieldDeclaration", "interfaceBodyDeclaration", 
  "interfaceMemberDeclaration", "constDeclaration", "constantDeclarator", 
  "interfaceMethodDeclaration", "interfaceMethodModifier", "genericInterfaceMethodDeclaration", 
  "variableDeclarators", "variableDeclarator", "variableDeclaratorId", "variableInitializer", 
  "arrayInitializer", "classOrInterfaceType", "typeArgument", "qualifiedNameList", 
  "formalParameters", "formalParameterList", "formalParameter", "lastFormalParameter", 
  "qualifiedName", "literal", "integerLiteral", "floatLiteral", "altAnnotationQualifiedName", 
  "annotation", "elementValuePairs", "elementValuePair", "elementValue", 
  "elementValueArrayInitializer", "annotationTypeDeclaration", "annotationTypeBody", 
  "annotationTypeElementDeclaration", "annotationTypeElementRest", "annotationMethodOrConstantRest", 
  "annotationMethodRest", "annotationConstantRest", "defaultValue", "block", 
  "blockStatement", "localVariableDeclaration", "localTypeDeclaration", 
  "statement", "catchClause", "catchType", "finallyBlock", "resourceSpecification", 
  "resources", "resource", "switchBlockStatementGroup", "switchLabel", "forControl", 
  "forInit", "enhancedForControl", "parExpression", "expressionList", "methodCall", 
  "expression", "lambdaExpression", "lambdaParameters", "lambdaBody", "primary", 
  "classType", "creator", "createdName", "innerCreator", "arrayCreatorRest", 
  "classCreatorRest", "explicitGenericInvocation", "typeArgumentsOrDiamond", 
  "nonWildcardTypeArgumentsOrDiamond", "nonWildcardTypeArguments", "typeList", 
  "typeType", "primitiveType", "typeArguments", "superSuffix", "explicitGenericInvocationSuffix", 
  "arguments"
};

std::vector<std::string> JavaLabeledParser::_literalNames = {
  "", "'abstract'", "'assert'", "'boolean'", "'break'", "'byte'", "'case'", 
  "'catch'", "'char'", "'class'", "'const'", "'continue'", "'default'", 
  "'do'", "'double'", "'else'", "'enum'", "'extends'", "'final'", "'finally'", 
  "'float'", "'for'", "'if'", "'goto'", "'implements'", "'import'", "'instanceof'", 
  "'int'", "'interface'", "'long'", "'native'", "'new'", "'package'", "'private'", 
  "'protected'", "'public'", "'return'", "'short'", "'static'", "'strictfp'", 
  "'super'", "'switch'", "'synchronized'", "'this'", "'throw'", "'throws'", 
  "'transient'", "'try'", "'void'", "'volatile'", "'while'", "", "", "", 
  "", "", "", "", "", "", "'null'", "'('", "')'", "'{'", "'}'", "'['", "']'", 
  "';'", "','", "'.'", "'='", "'>'", "'<'", "'!'", "'~'", "'\u003F'", "':'", 
  "'=='", "'<='", "'>='", "'!='", "'&&'", "'||'", "'++'", "'--'", "'+'", 
  "'-'", "'*'", "'/'", "'&'", "'|'", "'^'", "'%'", "'+='", "'-='", "'*='", 
  "'/='", "'&='", "'|='", "'^='", "'%='", "'<<='", "'>>='", "'>>>='", "'->'", 
  "'::'", "'@'", "'...'"
};

std::vector<std::string> JavaLabeledParser::_symbolicNames = {
  "", "ABSTRACT", "ASSERT", "BOOLEAN", "BREAK", "BYTE", "CASE", "CATCH", 
  "CHAR", "CLASS", "CONST", "CONTINUE", "DEFAULT", "DO", "DOUBLE", "ELSE", 
  "ENUM", "EXTENDS", "FINAL", "FINALLY", "FLOAT", "FOR", "IF", "GOTO", "IMPLEMENTS", 
  "IMPORT", "INSTANCEOF", "INT", "INTERFACE", "LONG", "NATIVE", "NEW", "PACKAGE", 
  "PRIVATE", "PROTECTED", "PUBLIC", "RETURN", "SHORT", "STATIC", "STRICTFP", 
  "SUPER", "SWITCH", "SYNCHRONIZED", "THIS", "THROW", "THROWS", "TRANSIENT", 
  "TRY", "VOID", "VOLATILE", "WHILE", "DECIMAL_LITERAL", "HEX_LITERAL", 
  "OCT_LITERAL", "BINARY_LITERAL", "FLOAT_LITERAL", "HEX_FLOAT_LITERAL", 
  "BOOL_LITERAL", "CHAR_LITERAL", "STRING_LITERAL", "NULL_LITERAL", "LPAREN", 
  "RPAREN", "LBRACE", "RBRACE", "LBRACK", "RBRACK", "SEMI", "COMMA", "DOT", 
  "ASSIGN", "GT", "LT", "BANG", "TILDE", "QUESTION", "COLON", "EQUAL", "LE", 
  "GE", "NOTEQUAL", "AND", "OR", "INC", "DEC", "ADD", "SUB", "MUL", "DIV", 
  "BITAND", "BITOR", "CARET", "MOD", "ADD_ASSIGN", "SUB_ASSIGN", "MUL_ASSIGN", 
  "DIV_ASSIGN", "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", "MOD_ASSIGN", "LSHIFT_ASSIGN", 
  "RSHIFT_ASSIGN", "URSHIFT_ASSIGN", "ARROW", "COLONCOLON", "AT", "ELLIPSIS", 
  "WS", "COMMENT", "LINE_COMMENT", "IDENTIFIER"
};

dfa::Vocabulary JavaLabeledParser::_vocabulary(_literalNames, _symbolicNames);

std::vector<std::string> JavaLabeledParser::_tokenNames;

JavaLabeledParser::Initializer::Initializer() {
	for (size_t i = 0; i < _symbolicNames.size(); ++i) {
		std::string name = _vocabulary.getLiteralName(i);
		if (name.empty()) {
			name = _vocabulary.getSymbolicName(i);
		}

		if (name.empty()) {
			_tokenNames.push_back("<INVALID>");
		} else {
      _tokenNames.push_back(name);
    }
	}

  static const uint16_t serializedATNSegment0[] = {
    0x3, 0x608b, 0xa72a, 0x8133, 0xb9ed, 0x417c, 0x3be7, 0x7786, 0x5964, 
       0x3, 0x71, 0x598, 0x4, 0x2, 0x9, 0x2, 0x4, 0x3, 0x9, 0x3, 0x4, 0x4, 
       0x9, 0x4, 0x4, 0x5, 0x9, 0x5, 0x4, 0x6, 0x9, 0x6, 0x4, 0x7, 0x9, 
       0x7, 0x4, 0x8, 0x9, 0x8, 0x4, 0x9, 0x9, 0x9, 0x4, 0xa, 0x9, 0xa, 
       0x4, 0xb, 0x9, 0xb, 0x4, 0xc, 0x9, 0xc, 0x4, 0xd, 0x9, 0xd, 0x4, 
       0xe, 0x9, 0xe, 0x4, 0xf, 0x9, 0xf, 0x4, 0x10, 0x9, 0x10, 0x4, 0x11, 
       0x9, 0x11, 0x4, 0x12, 0x9, 0x12, 0x4, 0x13, 0x9, 0x13, 0x4, 0x14, 
       0x9, 0x14, 0x4, 0x15, 0x9, 0x15, 0x4, 0x16, 0x9, 0x16, 0x4, 0x17, 
       0x9, 0x17, 0x4, 0x18, 0x9, 0x18, 0x4, 0x19, 0x9, 0x19, 0x4, 0x1a, 
       0x9, 0x1a, 0x4, 0x1b, 0x9, 0x1b, 0x4, 0x1c, 0x9, 0x1c, 0x4, 0x1d, 
       0x9, 0x1d, 0x4, 0x1e, 0x9, 0x1e, 0x4, 0x1f, 0x9, 0x1f, 0x4, 0x20, 
       0x9, 0x20, 0x4, 0x21, 0x9, 0x21, 0x4, 0x22, 0x9, 0x22, 0x4, 0x23, 
       0x9, 0x23, 0x4, 0x24, 0x9, 0x24, 0x4, 0x25, 0x9, 0x25, 0x4, 0x26, 
       0x9, 0x26, 0x4, 0x27, 0x9, 0x27, 0x4, 0x28, 0x9, 0x28, 0x4, 0x29, 
       0x9, 0x29, 0x4, 0x2a, 0x9, 0x2a, 0x4, 0x2b, 0x9, 0x2b, 0x4, 0x2c, 
       0x9, 0x2c, 0x4, 0x2d, 0x9, 0x2d, 0x4, 0x2e, 0x9, 0x2e, 0x4, 0x2f, 
       0x9, 0x2f, 0x4, 0x30, 0x9, 0x30, 0x4, 0x31, 0x9, 0x31, 0x4, 0x32, 
       0x9, 0x32, 0x4, 0x33, 0x9, 0x33, 0x4, 0x34, 0x9, 0x34, 0x4, 0x35, 
       0x9, 0x35, 0x4, 0x36, 0x9, 0x36, 0x4, 0x37, 0x9, 0x37, 0x4, 0x38, 
       0x9, 0x38, 0x4, 0x39, 0x9, 0x39, 0x4, 0x3a, 0x9, 0x3a, 0x4, 0x3b, 
       0x9, 0x3b, 0x4, 0x3c, 0x9, 0x3c, 0x4, 0x3d, 0x9, 0x3d, 0x4, 0x3e, 
       0x9, 0x3e, 0x4, 0x3f, 0x9, 0x3f, 0x4, 0x40, 0x9, 0x40, 0x4, 0x41, 
       0x9, 0x41, 0x4, 0x42, 0x9, 0x42, 0x4, 0x43, 0x9, 0x43, 0x4, 0x44, 
       0x9, 0x44, 0x4, 0x45, 0x9, 0x45, 0x4, 0x46, 0x9, 0x46, 0x4, 0x47, 
       0x9, 0x47, 0x4, 0x48, 0x9, 0x48, 0x4, 0x49, 0x9, 0x49, 0x4, 0x4a, 
       0x9, 0x4a, 0x4, 0x4b, 0x9, 0x4b, 0x4, 0x4c, 0x9, 0x4c, 0x4, 0x4d, 
       0x9, 0x4d, 0x4, 0x4e, 0x9, 0x4e, 0x4, 0x4f, 0x9, 0x4f, 0x4, 0x50, 
       0x9, 0x50, 0x4, 0x51, 0x9, 0x51, 0x4, 0x52, 0x9, 0x52, 0x4, 0x53, 
       0x9, 0x53, 0x4, 0x54, 0x9, 0x54, 0x4, 0x55, 0x9, 0x55, 0x4, 0x56, 
       0x9, 0x56, 0x4, 0x57, 0x9, 0x57, 0x4, 0x58, 0x9, 0x58, 0x4, 0x59, 
       0x9, 0x59, 0x4, 0x5a, 0x9, 0x5a, 0x4, 0x5b, 0x9, 0x5b, 0x4, 0x5c, 
       0x9, 0x5c, 0x4, 0x5d, 0x9, 0x5d, 0x4, 0x5e, 0x9, 0x5e, 0x4, 0x5f, 
       0x9, 0x5f, 0x4, 0x60, 0x9, 0x60, 0x4, 0x61, 0x9, 0x61, 0x4, 0x62, 
       0x9, 0x62, 0x4, 0x63, 0x9, 0x63, 0x4, 0x64, 0x9, 0x64, 0x4, 0x65, 
       0x9, 0x65, 0x4, 0x66, 0x9, 0x66, 0x4, 0x67, 0x9, 0x67, 0x4, 0x68, 
       0x9, 0x68, 0x4, 0x69, 0x9, 0x69, 0x4, 0x6a, 0x9, 0x6a, 0x3, 0x2, 
       0x5, 0x2, 0xd6, 0xa, 0x2, 0x3, 0x2, 0x7, 0x2, 0xd9, 0xa, 0x2, 0xc, 
       0x2, 0xe, 0x2, 0xdc, 0xb, 0x2, 0x3, 0x2, 0x7, 0x2, 0xdf, 0xa, 0x2, 
       0xc, 0x2, 0xe, 0x2, 0xe2, 0xb, 0x2, 0x3, 0x2, 0x3, 0x2, 0x3, 0x3, 
       0x7, 0x3, 0xe7, 0xa, 0x3, 0xc, 0x3, 0xe, 0x3, 0xea, 0xb, 0x3, 0x3, 
       0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x4, 0x3, 0x4, 0x5, 0x4, 
       0xf2, 0xa, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x5, 0x4, 0xf7, 0xa, 
       0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x5, 0x7, 0x5, 0xfc, 0xa, 0x5, 0xc, 
       0x5, 0xe, 0x5, 0xff, 0xb, 0x5, 0x3, 0x5, 0x3, 0x5, 0x3, 0x5, 0x3, 
       0x5, 0x5, 0x5, 0x105, 0xa, 0x5, 0x3, 0x5, 0x5, 0x5, 0x108, 0xa, 0x5, 
       0x3, 0x6, 0x3, 0x6, 0x3, 0x6, 0x3, 0x6, 0x3, 0x6, 0x5, 0x6, 0x10f, 
       0xa, 0x6, 0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 0x3, 
       0x7, 0x3, 0x7, 0x3, 0x7, 0x5, 0x7, 0x119, 0xa, 0x7, 0x3, 0x8, 0x3, 
       0x8, 0x5, 0x8, 0x11d, 0xa, 0x8, 0x3, 0x9, 0x3, 0x9, 0x3, 0x9, 0x5, 
       0x9, 0x122, 0xa, 0x9, 0x3, 0x9, 0x3, 0x9, 0x5, 0x9, 0x126, 0xa, 0x9, 
       0x3, 0x9, 0x3, 0x9, 0x5, 0x9, 0x12a, 0xa, 0x9, 0x3, 0x9, 0x3, 0x9, 
       0x3, 0xa, 0x3, 0xa, 0x3, 0xa, 0x3, 0xa, 0x7, 0xa, 0x132, 0xa, 0xa, 
       0xc, 0xa, 0xe, 0xa, 0x135, 0xb, 0xa, 0x3, 0xa, 0x3, 0xa, 0x3, 0xb, 
       0x7, 0xb, 0x13a, 0xa, 0xb, 0xc, 0xb, 0xe, 0xb, 0x13d, 0xb, 0xb, 0x3, 
       0xb, 0x3, 0xb, 0x3, 0xb, 0x7, 0xb, 0x142, 0xa, 0xb, 0xc, 0xb, 0xe, 
       0xb, 0x145, 0xb, 0xb, 0x3, 0xb, 0x5, 0xb, 0x148, 0xa, 0xb, 0x3, 0xc, 
       0x3, 0xc, 0x3, 0xc, 0x7, 0xc, 0x14d, 0xa, 0xc, 0xc, 0xc, 0xe, 0xc, 
       0x150, 0xb, 0xc, 0x3, 0xd, 0x3, 0xd, 0x3, 0xd, 0x3, 0xd, 0x5, 0xd, 
       0x156, 0xa, 0xd, 0x3, 0xd, 0x3, 0xd, 0x5, 0xd, 0x15a, 0xa, 0xd, 0x3, 
       0xd, 0x5, 0xd, 0x15d, 0xa, 0xd, 0x3, 0xd, 0x5, 0xd, 0x160, 0xa, 0xd, 
       0x3, 0xd, 0x3, 0xd, 0x3, 0xe, 0x3, 0xe, 0x3, 0xe, 0x7, 0xe, 0x167, 
       0xa, 0xe, 0xc, 0xe, 0xe, 0xe, 0x16a, 0xb, 0xe, 0x3, 0xf, 0x7, 0xf, 
       0x16d, 0xa, 0xf, 0xc, 0xf, 0xe, 0xf, 0x170, 0xb, 0xf, 0x3, 0xf, 0x3, 
       0xf, 0x5, 0xf, 0x174, 0xa, 0xf, 0x3, 0xf, 0x5, 0xf, 0x177, 0xa, 0xf, 
       0x3, 0x10, 0x3, 0x10, 0x7, 0x10, 0x17b, 0xa, 0x10, 0xc, 0x10, 0xe, 
       0x10, 0x17e, 0xb, 0x10, 0x3, 0x11, 0x3, 0x11, 0x3, 0x11, 0x5, 0x11, 
       0x183, 0xa, 0x11, 0x3, 0x11, 0x3, 0x11, 0x5, 0x11, 0x187, 0xa, 0x11, 
       0x3, 0x11, 0x3, 0x11, 0x3, 0x12, 0x3, 0x12, 0x7, 0x12, 0x18d, 0xa, 
       0x12, 0xc, 0x12, 0xe, 0x12, 0x190, 0xb, 0x12, 0x3, 0x12, 0x3, 0x12, 
       0x3, 0x13, 0x3, 0x13, 0x7, 0x13, 0x196, 0xa, 0x13, 0xc, 0x13, 0xe, 
       0x13, 0x199, 0xb, 0x13, 0x3, 0x13, 0x3, 0x13, 0x3, 0x14, 0x3, 0x14, 
       0x5, 0x14, 0x19f, 0xa, 0x14, 0x3, 0x14, 0x3, 0x14, 0x7, 0x14, 0x1a3, 
       0xa, 0x14, 0xc, 0x14, 0xe, 0x14, 0x1a6, 0xb, 0x14, 0x3, 0x14, 0x5, 
       0x14, 0x1a9, 0xa, 0x14, 0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 
       0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 0x5, 0x15, 
       0x1b4, 0xa, 0x15, 0x3, 0x16, 0x3, 0x16, 0x3, 0x16, 0x3, 0x16, 0x3, 
       0x16, 0x7, 0x16, 0x1bb, 0xa, 0x16, 0xc, 0x16, 0xe, 0x16, 0x1be, 0xb, 
       0x16, 0x3, 0x16, 0x3, 0x16, 0x5, 0x16, 0x1c2, 0xa, 0x16, 0x3, 0x16, 
       0x3, 0x16, 0x3, 0x17, 0x3, 0x17, 0x5, 0x17, 0x1c8, 0xa, 0x17, 0x3, 
       0x18, 0x3, 0x18, 0x5, 0x18, 0x1cc, 0xa, 0x18, 0x3, 0x19, 0x3, 0x19, 
       0x3, 0x19, 0x3, 0x1a, 0x3, 0x1a, 0x3, 0x1a, 0x3, 0x1b, 0x3, 0x1b, 
       0x3, 0x1b, 0x3, 0x1b, 0x5, 0x1b, 0x1d8, 0xa, 0x1b, 0x3, 0x1b, 0x3, 
       0x1b, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1d, 0x7, 
       0x1d, 0x1e1, 0xa, 0x1d, 0xc, 0x1d, 0xe, 0x1d, 0x1e4, 0xb, 0x1d, 0x3, 
       0x1d, 0x3, 0x1d, 0x5, 0x1d, 0x1e8, 0xa, 0x1d, 0x3, 0x1e, 0x3, 0x1e, 
       0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x5, 0x1e, 
       0x1f1, 0xa, 0x1e, 0x3, 0x1f, 0x3, 0x1f, 0x3, 0x1f, 0x3, 0x1f, 0x7, 
       0x1f, 0x1f7, 0xa, 0x1f, 0xc, 0x1f, 0xe, 0x1f, 0x1fa, 0xb, 0x1f, 0x3, 
       0x1f, 0x3, 0x1f, 0x3, 0x20, 0x3, 0x20, 0x3, 0x20, 0x7, 0x20, 0x201, 
       0xa, 0x20, 0xc, 0x20, 0xe, 0x20, 0x204, 0xb, 0x20, 0x3, 0x20, 0x3, 
       0x20, 0x3, 0x20, 0x3, 0x21, 0x7, 0x21, 0x20a, 0xa, 0x21, 0xc, 0x21, 
       0xe, 0x21, 0x20d, 0xb, 0x21, 0x3, 0x21, 0x3, 0x21, 0x3, 0x21, 0x7, 
       0x21, 0x212, 0xa, 0x21, 0xc, 0x21, 0xe, 0x21, 0x215, 0xb, 0x21, 0x3, 
       0x21, 0x3, 0x21, 0x5, 0x21, 0x219, 0xa, 0x21, 0x3, 0x21, 0x3, 0x21, 
       0x3, 0x21, 0x3, 0x21, 0x7, 0x21, 0x21f, 0xa, 0x21, 0xc, 0x21, 0xe, 
       0x21, 0x222, 0xb, 0x21, 0x3, 0x21, 0x3, 0x21, 0x5, 0x21, 0x226, 0xa, 
       0x21, 0x3, 0x21, 0x3, 0x21, 0x3, 0x22, 0x3, 0x22, 0x3, 0x22, 0x3, 
       0x22, 0x3, 0x22, 0x3, 0x22, 0x5, 0x22, 0x230, 0xa, 0x22, 0x3, 0x23, 
       0x3, 0x23, 0x3, 0x23, 0x3, 0x24, 0x3, 0x24, 0x3, 0x24, 0x7, 0x24, 
       0x238, 0xa, 0x24, 0xc, 0x24, 0xe, 0x24, 0x23b, 0xb, 0x24, 0x3, 0x25, 
       0x3, 0x25, 0x3, 0x25, 0x5, 0x25, 0x240, 0xa, 0x25, 0x3, 0x26, 0x3, 
       0x26, 0x3, 0x26, 0x7, 0x26, 0x245, 0xa, 0x26, 0xc, 0x26, 0xe, 0x26, 
       0x248, 0xb, 0x26, 0x3, 0x27, 0x3, 0x27, 0x5, 0x27, 0x24c, 0xa, 0x27, 
       0x3, 0x28, 0x3, 0x28, 0x3, 0x28, 0x3, 0x28, 0x7, 0x28, 0x252, 0xa, 
       0x28, 0xc, 0x28, 0xe, 0x28, 0x255, 0xb, 0x28, 0x3, 0x28, 0x5, 0x28, 
       0x258, 0xa, 0x28, 0x5, 0x28, 0x25a, 0xa, 0x28, 0x3, 0x28, 0x3, 0x28, 
       0x3, 0x29, 0x3, 0x29, 0x5, 0x29, 0x260, 0xa, 0x29, 0x3, 0x29, 0x3, 
       0x29, 0x3, 0x29, 0x5, 0x29, 0x265, 0xa, 0x29, 0x7, 0x29, 0x267, 0xa, 
       0x29, 0xc, 0x29, 0xe, 0x29, 0x26a, 0xb, 0x29, 0x3, 0x2a, 0x3, 0x2a, 
       0x7, 0x2a, 0x26e, 0xa, 0x2a, 0xc, 0x2a, 0xe, 0x2a, 0x271, 0xb, 0x2a, 
       0x3, 0x2a, 0x3, 0x2a, 0x3, 0x2a, 0x5, 0x2a, 0x276, 0xa, 0x2a, 0x5, 
       0x2a, 0x278, 0xa, 0x2a, 0x3, 0x2b, 0x3, 0x2b, 0x3, 0x2b, 0x7, 0x2b, 
       0x27d, 0xa, 0x2b, 0xc, 0x2b, 0xe, 0x2b, 0x280, 0xb, 0x2b, 0x3, 0x2c, 
       0x3, 0x2c, 0x5, 0x2c, 0x284, 0xa, 0x2c, 0x3, 0x2c, 0x3, 0x2c, 0x3, 
       0x2d, 0x3, 0x2d, 0x3, 0x2d, 0x7, 0x2d, 0x28b, 0xa, 0x2d, 0xc, 0x2d, 
       0xe, 0x2d, 0x28e, 0xb, 0x2d, 0x3, 0x2d, 0x3, 0x2d, 0x5, 0x2d, 0x292, 
       0xa, 0x2d, 0x3, 0x2d, 0x5, 0x2d, 0x295, 0xa, 0x2d, 0x3, 0x2e, 0x7, 
       0x2e, 0x298, 0xa, 0x2e, 0xc, 0x2e, 0xe, 0x2e, 0x29b, 0xb, 0x2e, 0x3, 
       0x2e, 0x3, 0x2e, 0x3, 0x2e, 0x3, 0x2f, 0x7, 0x2f, 0x2a1, 0xa, 0x2f, 
       0xc, 0x2f, 0xe, 0x2f, 0x2a4, 0xb, 0x2f, 0x3, 0x2f, 0x3, 0x2f, 0x7, 
       0x2f, 0x2a8, 0xa, 0x2f, 0xc, 0x2f, 0xe, 0x2f, 0x2ab, 0xb, 0x2f, 0x3, 
       0x2f, 0x3, 0x2f, 0x3, 0x2f, 0x3, 0x30, 0x3, 0x30, 0x3, 0x30, 0x7, 
       0x30, 0x2b3, 0xa, 0x30, 0xc, 0x30, 0xe, 0x30, 0x2b6, 0xb, 0x30, 0x3, 
       0x31, 0x3, 0x31, 0x3, 0x31, 0x3, 0x31, 0x3, 0x31, 0x3, 0x31, 0x5, 
       0x31, 0x2be, 0xa, 0x31, 0x3, 0x32, 0x3, 0x32, 0x3, 0x33, 0x3, 0x33, 
       0x3, 0x34, 0x3, 0x34, 0x7, 0x34, 0x2c6, 0xa, 0x34, 0xc, 0x34, 0xe, 
       0x34, 0x2c9, 0xb, 0x34, 0x3, 0x34, 0x3, 0x34, 0x3, 0x34, 0x3, 0x35, 
       0x3, 0x35, 0x3, 0x35, 0x5, 0x35, 0x2d1, 0xa, 0x35, 0x3, 0x35, 0x3, 
       0x35, 0x3, 0x35, 0x5, 0x35, 0x2d6, 0xa, 0x35, 0x3, 0x35, 0x5, 0x35, 
       0x2d9, 0xa, 0x35, 0x3, 0x36, 0x3, 0x36, 0x3, 0x36, 0x7, 0x36, 0x2de, 
       0xa, 0x36, 0xc, 0x36, 0xe, 0x36, 0x2e1, 0xb, 0x36, 0x3, 0x37, 0x3, 
       0x37, 0x3, 0x37, 0x3, 0x37, 0x3, 0x38, 0x3, 0x38, 0x3, 0x38, 0x5, 
       0x38, 0x2ea, 0xa, 0x38, 0x3, 0x39, 0x3, 0x39, 0x3, 0x39, 0x3, 0x39, 
       0x7, 0x39, 0x2f0, 0xa, 0x39, 0xc, 0x39, 0xe, 0x39, 0x2f3, 0xb, 0x39, 
       0x5, 0x39, 0x2f5, 0xa, 0x39, 0x3, 0x39, 0x5, 0x39, 0x2f8, 0xa, 0x39, 
       0x3, 0x39, 0x3, 0x39, 0x3, 0x3a, 0x3, 0x3a, 0x3, 0x3a, 0x3, 0x3a, 
       0x3, 0x3a, 0x3, 0x3b, 0x3, 0x3b, 0x7, 0x3b, 0x303, 0xa, 0x3b, 0xc, 
       0x3b, 0xe, 0x3b, 0x306, 0xb, 0x3b, 0x3, 0x3b, 0x3, 0x3b, 0x3, 0x3c, 
       0x7, 0x3c, 0x30b, 0xa, 0x3c, 0xc, 0x3c, 0xe, 0x3c, 0x30e, 0xb, 0x3c, 
       0x3, 0x3c, 0x3, 0x3c, 0x5, 0x3c, 0x312, 0xa, 0x3c, 0x3, 0x3d, 0x3, 
       0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x5, 0x3d, 0x31a, 
       0xa, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x5, 0x3d, 0x31e, 0xa, 0x3d, 0x3, 
       0x3d, 0x3, 0x3d, 0x5, 0x3d, 0x322, 0xa, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 
       0x5, 0x3d, 0x326, 0xa, 0x3d, 0x5, 0x3d, 0x328, 0xa, 0x3d, 0x3, 0x3e, 
       0x3, 0x3e, 0x5, 0x3e, 0x32c, 0xa, 0x3e, 0x3, 0x3f, 0x3, 0x3f, 0x3, 
       0x3f, 0x3, 0x3f, 0x5, 0x3f, 0x332, 0xa, 0x3f, 0x3, 0x40, 0x3, 0x40, 
       0x3, 0x41, 0x3, 0x41, 0x3, 0x41, 0x3, 0x42, 0x3, 0x42, 0x7, 0x42, 
       0x33b, 0xa, 0x42, 0xc, 0x42, 0xe, 0x42, 0x33e, 0xb, 0x42, 0x3, 0x42, 
       0x3, 0x42, 0x3, 0x43, 0x3, 0x43, 0x3, 0x43, 0x3, 0x43, 0x3, 0x43, 
       0x5, 0x43, 0x347, 0xa, 0x43, 0x3, 0x44, 0x7, 0x44, 0x34a, 0xa, 0x44, 
       0xc, 0x44, 0xe, 0x44, 0x34d, 0xb, 0x44, 0x3, 0x44, 0x3, 0x44, 0x3, 
       0x44, 0x3, 0x45, 0x7, 0x45, 0x353, 0xa, 0x45, 0xc, 0x45, 0xe, 0x45, 
       0x356, 0xb, 0x45, 0x3, 0x45, 0x3, 0x45, 0x5, 0x45, 0x35a, 0xa, 0x45, 
       0x3, 0x45, 0x5, 0x45, 0x35d, 0xa, 0x45, 0x3, 0x46, 0x3, 0x46, 0x3, 
       0x46, 0x3, 0x46, 0x3, 0x46, 0x5, 0x46, 0x364, 0xa, 0x46, 0x3, 0x46, 
       0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 
       0x5, 0x46, 0x36d, 0xa, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
       0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
       0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
       0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x6, 0x46, 0x382, 0xa, 0x46, 
       0xd, 0x46, 0xe, 0x46, 0x383, 0x3, 0x46, 0x5, 0x46, 0x387, 0xa, 0x46, 
       0x3, 0x46, 0x5, 0x46, 0x38a, 0xa, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
       0x46, 0x3, 0x46, 0x7, 0x46, 0x390, 0xa, 0x46, 0xc, 0x46, 0xe, 0x46, 
       0x393, 0xb, 0x46, 0x3, 0x46, 0x5, 0x46, 0x396, 0xa, 0x46, 0x3, 0x46, 
       0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x7, 0x46, 0x39c, 0xa, 0x46, 0xc, 
       0x46, 0xe, 0x46, 0x39f, 0xb, 0x46, 0x3, 0x46, 0x7, 0x46, 0x3a2, 0xa, 
       0x46, 0xc, 0x46, 0xe, 0x46, 0x3a5, 0xb, 0x46, 0x3, 0x46, 0x3, 0x46, 
       0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 
       0x5, 0x46, 0x3af, 0xa, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
       0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x5, 0x46, 0x3b8, 0xa, 0x46, 
       0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x5, 0x46, 0x3bd, 0xa, 0x46, 0x3, 
       0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
       0x46, 0x3, 0x46, 0x5, 0x46, 0x3c7, 0xa, 0x46, 0x3, 0x47, 0x3, 0x47, 
       0x3, 0x47, 0x7, 0x47, 0x3cc, 0xa, 0x47, 0xc, 0x47, 0xe, 0x47, 0x3cf, 
       0xb, 0x47, 0x3, 0x47, 0x3, 0x47, 0x3, 0x47, 0x3, 0x47, 0x3, 0x47, 
       0x3, 0x48, 0x3, 0x48, 0x3, 0x48, 0x7, 0x48, 0x3d9, 0xa, 0x48, 0xc, 
       0x48, 0xe, 0x48, 0x3dc, 0xb, 0x48, 0x3, 0x49, 0x3, 0x49, 0x3, 0x49, 
       0x3, 0x4a, 0x3, 0x4a, 0x3, 0x4a, 0x5, 0x4a, 0x3e4, 0xa, 0x4a, 0x3, 
       0x4a, 0x3, 0x4a, 0x3, 0x4b, 0x3, 0x4b, 0x3, 0x4b, 0x7, 0x4b, 0x3eb, 
       0xa, 0x4b, 0xc, 0x4b, 0xe, 0x4b, 0x3ee, 0xb, 0x4b, 0x3, 0x4c, 0x7, 
       0x4c, 0x3f1, 0xa, 0x4c, 0xc, 0x4c, 0xe, 0x4c, 0x3f4, 0xb, 0x4c, 0x3, 
       0x4c, 0x3, 0x4c, 0x3, 0x4c, 0x3, 0x4c, 0x3, 0x4c, 0x3, 0x4d, 0x6, 
       0x4d, 0x3fc, 0xa, 0x4d, 0xd, 0x4d, 0xe, 0x4d, 0x3fd, 0x3, 0x4d, 0x6, 
       0x4d, 0x401, 0xa, 0x4d, 0xd, 0x4d, 0xe, 0x4d, 0x402, 0x3, 0x4e, 0x3, 
       0x4e, 0x3, 0x4e, 0x5, 0x4e, 0x408, 0xa, 0x4e, 0x3, 0x4e, 0x3, 0x4e, 
       0x3, 0x4e, 0x5, 0x4e, 0x40d, 0xa, 0x4e, 0x3, 0x4f, 0x3, 0x4f, 0x5, 
       0x4f, 0x411, 0xa, 0x4f, 0x3, 0x4f, 0x3, 0x4f, 0x5, 0x4f, 0x415, 0xa, 
       0x4f, 0x3, 0x4f, 0x3, 0x4f, 0x5, 0x4f, 0x419, 0xa, 0x4f, 0x5, 0x4f, 
       0x41b, 0xa, 0x4f, 0x3, 0x50, 0x3, 0x50, 0x5, 0x50, 0x41f, 0xa, 0x50, 
       0x3, 0x51, 0x7, 0x51, 0x422, 0xa, 0x51, 0xc, 0x51, 0xe, 0x51, 0x425, 
       0xb, 0x51, 0x3, 0x51, 0x3, 0x51, 0x3, 0x51, 0x3, 0x51, 0x3, 0x51, 
       0x3, 0x52, 0x3, 0x52, 0x3, 0x52, 0x3, 0x52, 0x3, 0x53, 0x3, 0x53, 
       0x3, 0x53, 0x7, 0x53, 0x433, 0xa, 0x53, 0xc, 0x53, 0xe, 0x53, 0x436, 
       0xb, 0x53, 0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x5, 0x54, 0x43b, 0xa, 
       0x54, 0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x5, 0x54, 0x441, 
       0xa, 0x54, 0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x5, 0x54, 
       0x447, 0xa, 0x54, 0x3, 0x54, 0x5, 0x54, 0x44a, 0xa, 0x54, 0x3, 0x55, 
       0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
       0x7, 0x55, 0x453, 0xa, 0x55, 0xc, 0x55, 0xe, 0x55, 0x456, 0xb, 0x55, 
       0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
       0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
       0x5, 0x55, 0x464, 0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x468, 
       0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x46d, 0xa, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x471, 0xa, 0x55, 0x3, 0x55, 
       0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
       0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
       0x3, 0x55, 0x5, 0x55, 0x481, 0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 
       0x55, 0x4a9, 0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
       0x5, 0x55, 0x4af, 0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
       0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x4be, 0xa, 0x55, 
       0x3, 0x55, 0x7, 0x55, 0x4c1, 0xa, 0x55, 0xc, 0x55, 0xe, 0x55, 0x4c4, 
       0xb, 0x55, 0x3, 0x56, 0x3, 0x56, 0x3, 0x56, 0x3, 0x56, 0x3, 0x57, 
       0x3, 0x57, 0x3, 0x57, 0x5, 0x57, 0x4cd, 0xa, 0x57, 0x3, 0x57, 0x3, 
       0x57, 0x3, 0x57, 0x3, 0x57, 0x3, 0x57, 0x7, 0x57, 0x4d4, 0xa, 0x57, 
       0xc, 0x57, 0xe, 0x57, 0x4d7, 0xb, 0x57, 0x3, 0x57, 0x5, 0x57, 0x4da, 
       0xa, 0x57, 0x3, 0x58, 0x3, 0x58, 0x5, 0x58, 0x4de, 0xa, 0x58, 0x3, 
       0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 
       0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 
       0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x5, 0x59, 0x4f0, 0xa, 0x59, 
       0x5, 0x59, 0x4f2, 0xa, 0x59, 0x3, 0x5a, 0x3, 0x5a, 0x3, 0x5a, 0x5, 
       0x5a, 0x4f7, 0xa, 0x5a, 0x3, 0x5a, 0x7, 0x5a, 0x4fa, 0xa, 0x5a, 0xc, 
       0x5a, 0xe, 0x5a, 0x4fd, 0xb, 0x5a, 0x3, 0x5a, 0x3, 0x5a, 0x5, 0x5a, 
       0x501, 0xa, 0x5a, 0x3, 0x5b, 0x3, 0x5b, 0x3, 0x5b, 0x3, 0x5b, 0x3, 
       0x5b, 0x3, 0x5b, 0x3, 0x5b, 0x5, 0x5b, 0x50a, 0xa, 0x5b, 0x5, 0x5b, 
       0x50c, 0xa, 0x5b, 0x3, 0x5c, 0x3, 0x5c, 0x5, 0x5c, 0x510, 0xa, 0x5c, 
       0x3, 0x5c, 0x3, 0x5c, 0x3, 0x5c, 0x5, 0x5c, 0x515, 0xa, 0x5c, 0x7, 
       0x5c, 0x517, 0xa, 0x5c, 0xc, 0x5c, 0xe, 0x5c, 0x51a, 0xb, 0x5c, 0x3, 
       0x5c, 0x5, 0x5c, 0x51d, 0xa, 0x5c, 0x3, 0x5d, 0x3, 0x5d, 0x5, 0x5d, 
       0x521, 0xa, 0x5d, 0x3, 0x5d, 0x3, 0x5d, 0x3, 0x5e, 0x3, 0x5e, 0x3, 
       0x5e, 0x3, 0x5e, 0x7, 0x5e, 0x529, 0xa, 0x5e, 0xc, 0x5e, 0xe, 0x5e, 
       0x52c, 0xb, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x3, 
       0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x7, 0x5e, 0x535, 0xa, 0x5e, 0xc, 0x5e, 
       0xe, 0x5e, 0x538, 0xb, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x7, 0x5e, 0x53c, 
       0xa, 0x5e, 0xc, 0x5e, 0xe, 0x5e, 0x53f, 0xb, 0x5e, 0x5, 0x5e, 0x541, 
       0xa, 0x5e, 0x3, 0x5f, 0x3, 0x5f, 0x5, 0x5f, 0x545, 0xa, 0x5f, 0x3, 
       0x60, 0x3, 0x60, 0x3, 0x60, 0x3, 0x61, 0x3, 0x61, 0x3, 0x61, 0x5, 
       0x61, 0x54d, 0xa, 0x61, 0x3, 0x62, 0x3, 0x62, 0x3, 0x62, 0x5, 0x62, 
       0x552, 0xa, 0x62, 0x3, 0x63, 0x3, 0x63, 0x3, 0x63, 0x3, 0x63, 0x3, 
       0x64, 0x3, 0x64, 0x3, 0x64, 0x7, 0x64, 0x55b, 0xa, 0x64, 0xc, 0x64, 
       0xe, 0x64, 0x55e, 0xb, 0x64, 0x3, 0x65, 0x7, 0x65, 0x561, 0xa, 0x65, 
       0xc, 0x65, 0xe, 0x65, 0x564, 0xb, 0x65, 0x3, 0x65, 0x3, 0x65, 0x5, 
       0x65, 0x568, 0xa, 0x65, 0x3, 0x65, 0x7, 0x65, 0x56b, 0xa, 0x65, 0xc, 
       0x65, 0xe, 0x65, 0x56e, 0xb, 0x65, 0x3, 0x65, 0x3, 0x65, 0x7, 0x65, 
       0x572, 0xa, 0x65, 0xc, 0x65, 0xe, 0x65, 0x575, 0xb, 0x65, 0x3, 0x66, 
       0x3, 0x66, 0x3, 0x67, 0x3, 0x67, 0x3, 0x67, 0x3, 0x67, 0x7, 0x67, 
       0x57d, 0xa, 0x67, 0xc, 0x67, 0xe, 0x67, 0x580, 0xb, 0x67, 0x3, 0x67, 
       0x3, 0x67, 0x3, 0x68, 0x3, 0x68, 0x3, 0x68, 0x3, 0x68, 0x5, 0x68, 
       0x588, 0xa, 0x68, 0x5, 0x68, 0x58a, 0xa, 0x68, 0x3, 0x69, 0x3, 0x69, 
       0x3, 0x69, 0x3, 0x69, 0x5, 0x69, 0x590, 0xa, 0x69, 0x3, 0x6a, 0x3, 
       0x6a, 0x5, 0x6a, 0x594, 0xa, 0x6a, 0x3, 0x6a, 0x3, 0x6a, 0x3, 0x6a, 
       0x2, 0x3, 0xa8, 0x6b, 0x2, 0x4, 0x6, 0x8, 0xa, 0xc, 0xe, 0x10, 0x12, 
       0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e, 0x20, 0x22, 0x24, 0x26, 0x28, 
       0x2a, 0x2c, 0x2e, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e, 
       0x40, 0x42, 0x44, 0x46, 0x48, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x54, 
       0x56, 0x58, 0x5a, 0x5c, 0x5e, 0x60, 0x62, 0x64, 0x66, 0x68, 0x6a, 
       0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76, 0x78, 0x7a, 0x7c, 0x7e, 0x80, 
       0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e, 0x90, 0x92, 0x94, 0x96, 
       0x98, 0x9a, 0x9c, 0x9e, 0xa0, 0xa2, 0xa4, 0xa6, 0xa8, 0xaa, 0xac, 
       0xae, 0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe, 0xc0, 0xc2, 
       0xc4, 0xc6, 0xc8, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0x2, 0xe, 0x4, 0x2, 
       0x13, 0x13, 0x2a, 0x2a, 0x3, 0x2, 0x35, 0x38, 0x3, 0x2, 0x39, 0x3a, 
       0x3, 0x2, 0x55, 0x58, 0x3, 0x2, 0x4b, 0x4c, 0x4, 0x2, 0x59, 0x5a, 
       0x5e, 0x5e, 0x3, 0x2, 0x57, 0x58, 0x4, 0x2, 0x49, 0x4a, 0x50, 0x51, 
       0x4, 0x2, 0x4f, 0x4f, 0x52, 0x52, 0x4, 0x2, 0x48, 0x48, 0x5f, 0x69, 
       0x3, 0x2, 0x55, 0x56, 0xa, 0x2, 0x5, 0x5, 0x7, 0x7, 0xa, 0xa, 0x10, 
       0x10, 0x16, 0x16, 0x1d, 0x1d, 0x1f, 0x1f, 0x27, 0x27, 0x2, 0x637, 
       0x2, 0xd5, 0x3, 0x2, 0x2, 0x2, 0x4, 0xe8, 0x3, 0x2, 0x2, 0x2, 0x6, 
       0xef, 0x3, 0x2, 0x2, 0x2, 0x8, 0x107, 0x3, 0x2, 0x2, 0x2, 0xa, 0x10e, 
       0x3, 0x2, 0x2, 0x2, 0xc, 0x118, 0x3, 0x2, 0x2, 0x2, 0xe, 0x11c, 0x3, 
       0x2, 0x2, 0x2, 0x10, 0x11e, 0x3, 0x2, 0x2, 0x2, 0x12, 0x12d, 0x3, 
       0x2, 0x2, 0x2, 0x14, 0x13b, 0x3, 0x2, 0x2, 0x2, 0x16, 0x149, 0x3, 
       0x2, 0x2, 0x2, 0x18, 0x151, 0x3, 0x2, 0x2, 0x2, 0x1a, 0x163, 0x3, 
       0x2, 0x2, 0x2, 0x1c, 0x16e, 0x3, 0x2, 0x2, 0x2, 0x1e, 0x178, 0x3, 
       0x2, 0x2, 0x2, 0x20, 0x17f, 0x3, 0x2, 0x2, 0x2, 0x22, 0x18a, 0x3, 
       0x2, 0x2, 0x2, 0x24, 0x193, 0x3, 0x2, 0x2, 0x2, 0x26, 0x1a8, 0x3, 
       0x2, 0x2, 0x2, 0x28, 0x1b3, 0x3, 0x2, 0x2, 0x2, 0x2a, 0x1b5, 0x3, 
       0x2, 0x2, 0x2, 0x2c, 0x1c7, 0x3, 0x2, 0x2, 0x2, 0x2e, 0x1cb, 0x3, 
       0x2, 0x2, 0x2, 0x30, 0x1cd, 0x3, 0x2, 0x2, 0x2, 0x32, 0x1d0, 0x3, 
       0x2, 0x2, 0x2, 0x34, 0x1d3, 0x3, 0x2, 0x2, 0x2, 0x36, 0x1db, 0x3, 
       0x2, 0x2, 0x2, 0x38, 0x1e7, 0x3, 0x2, 0x2, 0x2, 0x3a, 0x1f0, 0x3, 
       0x2, 0x2, 0x2, 0x3c, 0x1f2, 0x3, 0x2, 0x2, 0x2, 0x3e, 0x1fd, 0x3, 
       0x2, 0x2, 0x2, 0x40, 0x20b, 0x3, 0x2, 0x2, 0x2, 0x42, 0x22f, 0x3, 
       0x2, 0x2, 0x2, 0x44, 0x231, 0x3, 0x2, 0x2, 0x2, 0x46, 0x234, 0x3, 
       0x2, 0x2, 0x2, 0x48, 0x23c, 0x3, 0x2, 0x2, 0x2, 0x4a, 0x241, 0x3, 
       0x2, 0x2, 0x2, 0x4c, 0x24b, 0x3, 0x2, 0x2, 0x2, 0x4e, 0x24d, 0x3, 
       0x2, 0x2, 0x2, 0x50, 0x25d, 0x3, 0x2, 0x2, 0x2, 0x52, 0x277, 0x3, 
       0x2, 0x2, 0x2, 0x54, 0x279, 0x3, 0x2, 0x2, 0x2, 0x56, 0x281, 0x3, 
       0x2, 0x2, 0x2, 0x58, 0x294, 0x3, 0x2, 0x2, 0x2, 0x5a, 0x299, 0x3, 
       0x2, 0x2, 0x2, 0x5c, 0x2a2, 0x3, 0x2, 0x2, 0x2, 0x5e, 0x2af, 0x3, 
       0x2, 0x2, 0x2, 0x60, 0x2bd, 0x3, 0x2, 0x2, 0x2, 0x62, 0x2bf, 0x3, 
       0x2, 0x2, 0x2, 0x64, 0x2c1, 0x3, 0x2, 0x2, 0x2, 0x66, 0x2c7, 0x3, 
       0x2, 0x2, 0x2, 0x68, 0x2d0, 0x3, 0x2, 0x2, 0x2, 0x6a, 0x2da, 0x3, 
       0x2, 0x2, 0x2, 0x6c, 0x2e2, 0x3, 0x2, 0x2, 0x2, 0x6e, 0x2e9, 0x3, 
       0x2, 0x2, 0x2, 0x70, 0x2eb, 0x3, 0x2, 0x2, 0x2, 0x72, 0x2fb, 0x3, 
       0x2, 0x2, 0x2, 0x74, 0x300, 0x3, 0x2, 0x2, 0x2, 0x76, 0x311, 0x3, 
       0x2, 0x2, 0x2, 0x78, 0x327, 0x3, 0x2, 0x2, 0x2, 0x7a, 0x32b, 0x3, 
       0x2, 0x2, 0x2, 0x7c, 0x32d, 0x3, 0x2, 0x2, 0x2, 0x7e, 0x333, 0x3, 
       0x2, 0x2, 0x2, 0x80, 0x335, 0x3, 0x2, 0x2, 0x2, 0x82, 0x338, 0x3, 
       0x2, 0x2, 0x2, 0x84, 0x346, 0x3, 0x2, 0x2, 0x2, 0x86, 0x34b, 0x3, 
       0x2, 0x2, 0x2, 0x88, 0x35c, 0x3, 0x2, 0x2, 0x2, 0x8a, 0x3c6, 0x3, 
       0x2, 0x2, 0x2, 0x8c, 0x3c8, 0x3, 0x2, 0x2, 0x2, 0x8e, 0x3d5, 0x3, 
       0x2, 0x2, 0x2, 0x90, 0x3dd, 0x3, 0x2, 0x2, 0x2, 0x92, 0x3e0, 0x3, 
       0x2, 0x2, 0x2, 0x94, 0x3e7, 0x3, 0x2, 0x2, 0x2, 0x96, 0x3f2, 0x3, 
       0x2, 0x2, 0x2, 0x98, 0x3fb, 0x3, 0x2, 0x2, 0x2, 0x9a, 0x40c, 0x3, 
       0x2, 0x2, 0x2, 0x9c, 0x41a, 0x3, 0x2, 0x2, 0x2, 0x9e, 0x41e, 0x3, 
       0x2, 0x2, 0x2, 0xa0, 0x423, 0x3, 0x2, 0x2, 0x2, 0xa2, 0x42b, 0x3, 
       0x2, 0x2, 0x2, 0xa4, 0x42f, 0x3, 0x2, 0x2, 0x2, 0xa6, 0x449, 0x3, 
       0x2, 0x2, 0x2, 0xa8, 0x470, 0x3, 0x2, 0x2, 0x2, 0xaa, 0x4c5, 0x3, 
       0x2, 0x2, 0x2, 0xac, 0x4d9, 0x3, 0x2, 0x2, 0x2, 0xae, 0x4dd, 0x3, 
       0x2, 0x2, 0x2, 0xb0, 0x4f1, 0x3, 0x2, 0x2, 0x2, 0xb2, 0x4f6, 0x3, 
       0x2, 0x2, 0x2, 0xb4, 0x50b, 0x3, 0x2, 0x2, 0x2, 0xb6, 0x51c, 0x3, 
       0x2, 0x2, 0x2, 0xb8, 0x51e, 0x3, 0x2, 0x2, 0x2, 0xba, 0x524, 0x3, 
       0x2, 0x2, 0x2, 0xbc, 0x542, 0x3, 0x2, 0x2, 0x2, 0xbe, 0x546, 0x3, 
       0x2, 0x2, 0x2, 0xc0, 0x54c, 0x3, 0x2, 0x2, 0x2, 0xc2, 0x551, 0x3, 
       0x2, 0x2, 0x2, 0xc4, 0x553, 0x3, 0x2, 0x2, 0x2, 0xc6, 0x557, 0x3, 
       0x2, 0x2, 0x2, 0xc8, 0x562, 0x3, 0x2, 0x2, 0x2, 0xca, 0x576, 0x3, 
       0x2, 0x2, 0x2, 0xcc, 0x578, 0x3, 0x2, 0x2, 0x2, 0xce, 0x589, 0x3, 
       0x2, 0x2, 0x2, 0xd0, 0x58f, 0x3, 0x2, 0x2, 0x2, 0xd2, 0x591, 0x3, 
       0x2, 0x2, 0x2, 0xd4, 0xd6, 0x5, 0x4, 0x3, 0x2, 0xd5, 0xd4, 0x3, 0x2, 
       0x2, 0x2, 0xd5, 0xd6, 0x3, 0x2, 0x2, 0x2, 0xd6, 0xda, 0x3, 0x2, 0x2, 
       0x2, 0xd7, 0xd9, 0x5, 0x6, 0x4, 0x2, 0xd8, 0xd7, 0x3, 0x2, 0x2, 0x2, 
       0xd9, 0xdc, 0x3, 0x2, 0x2, 0x2, 0xda, 0xd8, 0x3, 0x2, 0x2, 0x2, 0xda, 
       0xdb, 0x3, 0x2, 0x2, 0x2, 0xdb, 0xe0, 0x3, 0x2, 0x2, 0x2, 0xdc, 0xda, 
       0x3, 0x2, 0x2, 0x2, 0xdd, 0xdf, 0x5, 0x8, 0x5, 0x2, 0xde, 0xdd, 0x3, 
       0x2, 0x2, 0x2, 0xdf, 0xe2, 0x3, 0x2, 0x2, 0x2, 0xe0, 0xde, 0x3, 0x2, 
       0x2, 0x2, 0xe0, 0xe1, 0x3, 0x2, 0x2, 0x2, 0xe1, 0xe3, 0x3, 0x2, 0x2, 
       0x2, 0xe2, 0xe0, 0x3, 0x2, 0x2, 0x2, 0xe3, 0xe4, 0x7, 0x2, 0x2, 0x3, 
       0xe4, 0x3, 0x3, 0x2, 0x2, 0x2, 0xe5, 0xe7, 0x5, 0x68, 0x35, 0x2, 
       0xe6, 0xe5, 0x3, 0x2, 0x2, 0x2, 0xe7, 0xea, 0x3, 0x2, 0x2, 0x2, 0xe8, 
       0xe6, 0x3, 0x2, 0x2, 0x2, 0xe8, 0xe9, 0x3, 0x2, 0x2, 0x2, 0xe9, 0xeb, 
       0x3, 0x2, 0x2, 0x2, 0xea, 0xe8, 0x3, 0x2, 0x2, 0x2, 0xeb, 0xec, 0x7, 
       0x22, 0x2, 0x2, 0xec, 0xed, 0x5, 0x5e, 0x30, 0x2, 0xed, 0xee, 0x7, 
       0x45, 0x2, 0x2, 0xee, 0x5, 0x3, 0x2, 0x2, 0x2, 0xef, 0xf1, 0x7, 0x1b, 
       0x2, 0x2, 0xf0, 0xf2, 0x7, 0x28, 0x2, 0x2, 0xf1, 0xf0, 0x3, 0x2, 
       0x2, 0x2, 0xf1, 0xf2, 0x3, 0x2, 0x2, 0x2, 0xf2, 0xf3, 0x3, 0x2, 0x2, 
       0x2, 0xf3, 0xf6, 0x5, 0x5e, 0x30, 0x2, 0xf4, 0xf5, 0x7, 0x47, 0x2, 
       0x2, 0xf5, 0xf7, 0x7, 0x59, 0x2, 0x2, 0xf6, 0xf4, 0x3, 0x2, 0x2, 
       0x2, 0xf6, 0xf7, 0x3, 0x2, 0x2, 0x2, 0xf7, 0xf8, 0x3, 0x2, 0x2, 0x2, 
       0xf8, 0xf9, 0x7, 0x45, 0x2, 0x2, 0xf9, 0x7, 0x3, 0x2, 0x2, 0x2, 0xfa, 
       0xfc, 0x5, 0xc, 0x7, 0x2, 0xfb, 0xfa, 0x3, 0x2, 0x2, 0x2, 0xfc, 0xff, 
       0x3, 0x2, 0x2, 0x2, 0xfd, 0xfb, 0x3, 0x2, 0x2, 0x2, 0xfd, 0xfe, 0x3, 
       0x2, 0x2, 0x2, 0xfe, 0x104, 0x3, 0x2, 0x2, 0x2, 0xff, 0xfd, 0x3, 
       0x2, 0x2, 0x2, 0x100, 0x105, 0x5, 0x10, 0x9, 0x2, 0x101, 0x105, 0x5, 
       0x18, 0xd, 0x2, 0x102, 0x105, 0x5, 0x20, 0x11, 0x2, 0x103, 0x105, 
       0x5, 0x72, 0x3a, 0x2, 0x104, 0x100, 0x3, 0x2, 0x2, 0x2, 0x104, 0x101, 
       0x3, 0x2, 0x2, 0x2, 0x104, 0x102, 0x3, 0x2, 0x2, 0x2, 0x104, 0x103, 
       0x3, 0x2, 0x2, 0x2, 0x105, 0x108, 0x3, 0x2, 0x2, 0x2, 0x106, 0x108, 
       0x7, 0x45, 0x2, 0x2, 0x107, 0xfd, 0x3, 0x2, 0x2, 0x2, 0x107, 0x106, 
       0x3, 0x2, 0x2, 0x2, 0x108, 0x9, 0x3, 0x2, 0x2, 0x2, 0x109, 0x10f, 
       0x5, 0xc, 0x7, 0x2, 0x10a, 0x10f, 0x7, 0x20, 0x2, 0x2, 0x10b, 0x10f, 
       0x7, 0x2c, 0x2, 0x2, 0x10c, 0x10f, 0x7, 0x30, 0x2, 0x2, 0x10d, 0x10f, 
       0x7, 0x33, 0x2, 0x2, 0x10e, 0x109, 0x3, 0x2, 0x2, 0x2, 0x10e, 0x10a, 
       0x3, 0x2, 0x2, 0x2, 0x10e, 0x10b, 0x3, 0x2, 0x2, 0x2, 0x10e, 0x10c, 
       0x3, 0x2, 0x2, 0x2, 0x10e, 0x10d, 0x3, 0x2, 0x2, 0x2, 0x10f, 0xb, 
       0x3, 0x2, 0x2, 0x2, 0x110, 0x119, 0x5, 0x68, 0x35, 0x2, 0x111, 0x119, 
       0x7, 0x25, 0x2, 0x2, 0x112, 0x119, 0x7, 0x24, 0x2, 0x2, 0x113, 0x119, 
       0x7, 0x23, 0x2, 0x2, 0x114, 0x119, 0x7, 0x28, 0x2, 0x2, 0x115, 0x119, 
       0x7, 0x3, 0x2, 0x2, 0x116, 0x119, 0x7, 0x14, 0x2, 0x2, 0x117, 0x119, 
       0x7, 0x29, 0x2, 0x2, 0x118, 0x110, 0x3, 0x2, 0x2, 0x2, 0x118, 0x111, 
       0x3, 0x2, 0x2, 0x2, 0x118, 0x112, 0x3, 0x2, 0x2, 0x2, 0x118, 0x113, 
       0x3, 0x2, 0x2, 0x2, 0x118, 0x114, 0x3, 0x2, 0x2, 0x2, 0x118, 0x115, 
       0x3, 0x2, 0x2, 0x2, 0x118, 0x116, 0x3, 0x2, 0x2, 0x2, 0x118, 0x117, 
       0x3, 0x2, 0x2, 0x2, 0x119, 0xd, 0x3, 0x2, 0x2, 0x2, 0x11a, 0x11d, 
       0x7, 0x14, 0x2, 0x2, 0x11b, 0x11d, 0x5, 0x68, 0x35, 0x2, 0x11c, 0x11a, 
       0x3, 0x2, 0x2, 0x2, 0x11c, 0x11b, 0x3, 0x2, 0x2, 0x2, 0x11d, 0xf, 
       0x3, 0x2, 0x2, 0x2, 0x11e, 0x11f, 0x7, 0xb, 0x2, 0x2, 0x11f, 0x121, 
       0x7, 0x71, 0x2, 0x2, 0x120, 0x122, 0x5, 0x12, 0xa, 0x2, 0x121, 0x120, 
       0x3, 0x2, 0x2, 0x2, 0x121, 0x122, 0x3, 0x2, 0x2, 0x2, 0x122, 0x125, 
       0x3, 0x2, 0x2, 0x2, 0x123, 0x124, 0x7, 0x13, 0x2, 0x2, 0x124, 0x126, 
       0x5, 0xc8, 0x65, 0x2, 0x125, 0x123, 0x3, 0x2, 0x2, 0x2, 0x125, 0x126, 
       0x3, 0x2, 0x2, 0x2, 0x126, 0x129, 0x3, 0x2, 0x2, 0x2, 0x127, 0x128, 
       0x7, 0x1a, 0x2, 0x2, 0x128, 0x12a, 0x5, 0xc6, 0x64, 0x2, 0x129, 0x127, 
       0x3, 0x2, 0x2, 0x2, 0x129, 0x12a, 0x3, 0x2, 0x2, 0x2, 0x12a, 0x12b, 
       0x3, 0x2, 0x2, 0x2, 0x12b, 0x12c, 0x5, 0x22, 0x12, 0x2, 0x12c, 0x11, 
       0x3, 0x2, 0x2, 0x2, 0x12d, 0x12e, 0x7, 0x4a, 0x2, 0x2, 0x12e, 0x133, 
       0x5, 0x14, 0xb, 0x2, 0x12f, 0x130, 0x7, 0x46, 0x2, 0x2, 0x130, 0x132, 
       0x5, 0x14, 0xb, 0x2, 0x131, 0x12f, 0x3, 0x2, 0x2, 0x2, 0x132, 0x135, 
       0x3, 0x2, 0x2, 0x2, 0x133, 0x131, 0x3, 0x2, 0x2, 0x2, 0x133, 0x134, 
       0x3, 0x2, 0x2, 0x2, 0x134, 0x136, 0x3, 0x2, 0x2, 0x2, 0x135, 0x133, 
       0x3, 0x2, 0x2, 0x2, 0x136, 0x137, 0x7, 0x49, 0x2, 0x2, 0x137, 0x13, 
       0x3, 0x2, 0x2, 0x2, 0x138, 0x13a, 0x5, 0x68, 0x35, 0x2, 0x139, 0x138, 
       0x3, 0x2, 0x2, 0x2, 0x13a, 0x13d, 0x3, 0x2, 0x2, 0x2, 0x13b, 0x139, 
       0x3, 0x2, 0x2, 0x2, 0x13b, 0x13c, 0x3, 0x2, 0x2, 0x2, 0x13c, 0x13e, 
       0x3, 0x2, 0x2, 0x2, 0x13d, 0x13b, 0x3, 0x2, 0x2, 0x2, 0x13e, 0x147, 
       0x7, 0x71, 0x2, 0x2, 0x13f, 0x143, 0x7, 0x13, 0x2, 0x2, 0x140, 0x142, 
       0x5, 0x68, 0x35, 0x2, 0x141, 0x140, 0x3, 0x2, 0x2, 0x2, 0x142, 0x145, 
       0x3, 0x2, 0x2, 0x2, 0x143, 0x141, 0x3, 0x2, 0x2, 0x2, 0x143, 0x144, 
       0x3, 0x2, 0x2, 0x2, 0x144, 0x146, 0x3, 0x2, 0x2, 0x2, 0x145, 0x143, 
       0x3, 0x2, 0x2, 0x2, 0x146, 0x148, 0x5, 0x16, 0xc, 0x2, 0x147, 0x13f, 
       0x3, 0x2, 0x2, 0x2, 0x147, 0x148, 0x3, 0x2, 0x2, 0x2, 0x148, 0x15, 
       0x3, 0x2, 0x2, 0x2, 0x149, 0x14e, 0x5, 0xc8, 0x65, 0x2, 0x14a, 0x14b, 
       0x7, 0x5b, 0x2, 0x2, 0x14b, 0x14d, 0x5, 0xc8, 0x65, 0x2, 0x14c, 0x14a, 
       0x3, 0x2, 0x2, 0x2, 0x14d, 0x150, 0x3, 0x2, 0x2, 0x2, 0x14e, 0x14c, 
       0x3, 0x2, 0x2, 0x2, 0x14e, 0x14f, 0x3, 0x2, 0x2, 0x2, 0x14f, 0x17, 
       0x3, 0x2, 0x2, 0x2, 0x150, 0x14e, 0x3, 0x2, 0x2, 0x2, 0x151, 0x152, 
       0x7, 0x12, 0x2, 0x2, 0x152, 0x155, 0x7, 0x71, 0x2, 0x2, 0x153, 0x154, 
       0x7, 0x1a, 0x2, 0x2, 0x154, 0x156, 0x5, 0xc6, 0x64, 0x2, 0x155, 0x153, 
       0x3, 0x2, 0x2, 0x2, 0x155, 0x156, 0x3, 0x2, 0x2, 0x2, 0x156, 0x157, 
       0x3, 0x2, 0x2, 0x2, 0x157, 0x159, 0x7, 0x41, 0x2, 0x2, 0x158, 0x15a, 
       0x5, 0x1a, 0xe, 0x2, 0x159, 0x158, 0x3, 0x2, 0x2, 0x2, 0x159, 0x15a, 
       0x3, 0x2, 0x2, 0x2, 0x15a, 0x15c, 0x3, 0x2, 0x2, 0x2, 0x15b, 0x15d, 
       0x7, 0x46, 0x2, 0x2, 0x15c, 0x15b, 0x3, 0x2, 0x2, 0x2, 0x15c, 0x15d, 
       0x3, 0x2, 0x2, 0x2, 0x15d, 0x15f, 0x3, 0x2, 0x2, 0x2, 0x15e, 0x160, 
       0x5, 0x1e, 0x10, 0x2, 0x15f, 0x15e, 0x3, 0x2, 0x2, 0x2, 0x15f, 0x160, 
       0x3, 0x2, 0x2, 0x2, 0x160, 0x161, 0x3, 0x2, 0x2, 0x2, 0x161, 0x162, 
       0x7, 0x42, 0x2, 0x2, 0x162, 0x19, 0x3, 0x2, 0x2, 0x2, 0x163, 0x168, 
       0x5, 0x1c, 0xf, 0x2, 0x164, 0x165, 0x7, 0x46, 0x2, 0x2, 0x165, 0x167, 
       0x5, 0x1c, 0xf, 0x2, 0x166, 0x164, 0x3, 0x2, 0x2, 0x2, 0x167, 0x16a, 
       0x3, 0x2, 0x2, 0x2, 0x168, 0x166, 0x3, 0x2, 0x2, 0x2, 0x168, 0x169, 
       0x3, 0x2, 0x2, 0x2, 0x169, 0x1b, 0x3, 0x2, 0x2, 0x2, 0x16a, 0x168, 
       0x3, 0x2, 0x2, 0x2, 0x16b, 0x16d, 0x5, 0x68, 0x35, 0x2, 0x16c, 0x16b, 
       0x3, 0x2, 0x2, 0x2, 0x16d, 0x170, 0x3, 0x2, 0x2, 0x2, 0x16e, 0x16c, 
       0x3, 0x2, 0x2, 0x2, 0x16e, 0x16f, 0x3, 0x2, 0x2, 0x2, 0x16f, 0x171, 
       0x3, 0x2, 0x2, 0x2, 0x170, 0x16e, 0x3, 0x2, 0x2, 0x2, 0x171, 0x173, 
       0x7, 0x71, 0x2, 0x2, 0x172, 0x174, 0x5, 0xd2, 0x6a, 0x2, 0x173, 0x172, 
       0x3, 0x2, 0x2, 0x2, 0x173, 0x174, 0x3, 0x2, 0x2, 0x2, 0x174, 0x176, 
       0x3, 0x2, 0x2, 0x2, 0x175, 0x177, 0x5, 0x22, 0x12, 0x2, 0x176, 0x175, 
       0x3, 0x2, 0x2, 0x2, 0x176, 0x177, 0x3, 0x2, 0x2, 0x2, 0x177, 0x1d, 
       0x3, 0x2, 0x2, 0x2, 0x178, 0x17c, 0x7, 0x45, 0x2, 0x2, 0x179, 0x17b, 
       0x5, 0x26, 0x14, 0x2, 0x17a, 0x179, 0x3, 0x2, 0x2, 0x2, 0x17b, 0x17e, 
       0x3, 0x2, 0x2, 0x2, 0x17c, 0x17a, 0x3, 0x2, 0x2, 0x2, 0x17c, 0x17d, 
       0x3, 0x2, 0x2, 0x2, 0x17d, 0x1f, 0x3, 0x2, 0x2, 0x2, 0x17e, 0x17c, 
       0x3, 0x2, 0x2, 0x2, 0x17f, 0x180, 0x7, 0x1e, 0x2, 0x2, 0x180, 0x182, 
       0x7, 0x71, 0x2, 0x2, 0x181, 0x183, 0x5, 0x12, 0xa, 0x2, 0x182, 0x181, 
       0x3, 0x2, 0x2, 0x2, 0x182, 0x183, 0x3, 0x2, 0x2, 0x2, 0x183, 0x186, 
       0x3, 0x2, 0x2, 0x2, 0x184, 0x185, 0x7, 0x13, 0x2, 0x2, 0x185, 0x187, 
       0x5, 0xc6, 0x64, 0x2, 0x186, 0x184, 0x3, 0x2, 0x2, 0x2, 0x186, 0x187, 
       0x3, 0x2, 0x2, 0x2, 0x187, 0x188, 0x3, 0x2, 0x2, 0x2, 0x188, 0x189, 
       0x5, 0x24, 0x13, 0x2, 0x189, 0x21, 0x3, 0x2, 0x2, 0x2, 0x18a, 0x18e, 
       0x7, 0x41, 0x2, 0x2, 0x18b, 0x18d, 0x5, 0x26, 0x14, 0x2, 0x18c, 0x18b, 
       0x3, 0x2, 0x2, 0x2, 0x18d, 0x190, 0x3, 0x2, 0x2, 0x2, 0x18e, 0x18c, 
       0x3, 0x2, 0x2, 0x2, 0x18e, 0x18f, 0x3, 0x2, 0x2, 0x2, 0x18f, 0x191, 
       0x3, 0x2, 0x2, 0x2, 0x190, 0x18e, 0x3, 0x2, 0x2, 0x2, 0x191, 0x192, 
       0x7, 0x42, 0x2, 0x2, 0x192, 0x23, 0x3, 0x2, 0x2, 0x2, 0x193, 0x197, 
       0x7, 0x41, 0x2, 0x2, 0x194, 0x196, 0x5, 0x38, 0x1d, 0x2, 0x195, 0x194, 
       0x3, 0x2, 0x2, 0x2, 0x196, 0x199, 0x3, 0x2, 0x2, 0x2, 0x197, 0x195, 
       0x3, 0x2, 0x2, 0x2, 0x197, 0x198, 0x3, 0x2, 0x2, 0x2, 0x198, 0x19a, 
       0x3, 0x2, 0x2, 0x2, 0x199, 0x197, 0x3, 0x2, 0x2, 0x2, 0x19a, 0x19b, 
       0x7, 0x42, 0x2, 0x2, 0x19b, 0x25, 0x3, 0x2, 0x2, 0x2, 0x19c, 0x1a9, 
       0x7, 0x45, 0x2, 0x2, 0x19d, 0x19f, 0x7, 0x28, 0x2, 0x2, 0x19e, 0x19d, 
       0x3, 0x2, 0x2, 0x2, 0x19e, 0x19f, 0x3, 0x2, 0x2, 0x2, 0x19f, 0x1a0, 
       0x3, 0x2, 0x2, 0x2, 0x1a0, 0x1a9, 0x5, 0x82, 0x42, 0x2, 0x1a1, 0x1a3, 
       0x5, 0xa, 0x6, 0x2, 0x1a2, 0x1a1, 0x3, 0x2, 0x2, 0x2, 0x1a3, 0x1a6, 
       0x3, 0x2, 0x2, 0x2, 0x1a4, 0x1a2, 0x3, 0x2, 0x2, 0x2, 0x1a4, 0x1a5, 
       0x3, 0x2, 0x2, 0x2, 0x1a5, 0x1a7, 0x3, 0x2, 0x2, 0x2, 0x1a6, 0x1a4, 
       0x3, 0x2, 0x2, 0x2, 0x1a7, 0x1a9, 0x5, 0x28, 0x15, 0x2, 0x1a8, 0x19c, 
       0x3, 0x2, 0x2, 0x2, 0x1a8, 0x19e, 0x3, 0x2, 0x2, 0x2, 0x1a8, 0x1a4, 
       0x3, 0x2, 0x2, 0x2, 0x1a9, 0x27, 0x3, 0x2, 0x2, 0x2, 0x1aa, 0x1b4, 
       0x5, 0x2a, 0x16, 0x2, 0x1ab, 0x1b4, 0x5, 0x30, 0x19, 0x2, 0x1ac, 
       0x1b4, 0x5, 0x36, 0x1c, 0x2, 0x1ad, 0x1b4, 0x5, 0x34, 0x1b, 0x2, 
       0x1ae, 0x1b4, 0x5, 0x32, 0x1a, 0x2, 0x1af, 0x1b4, 0x5, 0x20, 0x11, 
       0x2, 0x1b0, 0x1b4, 0x5, 0x72, 0x3a, 0x2, 0x1b1, 0x1b4, 0x5, 0x10, 
       0x9, 0x2, 0x1b2, 0x1b4, 0x5, 0x18, 0xd, 0x2, 0x1b3, 0x1aa, 0x3, 0x2, 
       0x2, 0x2, 0x1b3, 0x1ab, 0x3, 0x2, 0x2, 0x2, 0x1b3, 0x1ac, 0x3, 0x2, 
       0x2, 0x2, 0x1b3, 0x1ad, 0x3, 0x2, 0x2, 0x2, 0x1b3, 0x1ae, 0x3, 0x2, 
       0x2, 0x2, 0x1b3, 0x1af, 0x3, 0x2, 0x2, 0x2, 0x1b3, 0x1b0, 0x3, 0x2, 
       0x2, 0x2, 0x1b3, 0x1b1, 0x3, 0x2, 0x2, 0x2, 0x1b3, 0x1b2, 0x3, 0x2, 
       0x2, 0x2, 0x1b4, 0x29, 0x3, 0x2, 0x2, 0x2, 0x1b5, 0x1b6, 0x5, 0x2e, 
       0x18, 0x2, 0x1b6, 0x1b7, 0x7, 0x71, 0x2, 0x2, 0x1b7, 0x1bc, 0x5, 
       0x56, 0x2c, 0x2, 0x1b8, 0x1b9, 0x7, 0x43, 0x2, 0x2, 0x1b9, 0x1bb, 
       0x7, 0x44, 0x2, 0x2, 0x1ba, 0x1b8, 0x3, 0x2, 0x2, 0x2, 0x1bb, 0x1be, 
       0x3, 0x2, 0x2, 0x2, 0x1bc, 0x1ba, 0x3, 0x2, 0x2, 0x2, 0x1bc, 0x1bd, 
       0x3, 0x2, 0x2, 0x2, 0x1bd, 0x1c1, 0x3, 0x2, 0x2, 0x2, 0x1be, 0x1bc, 
       0x3, 0x2, 0x2, 0x2, 0x1bf, 0x1c0, 0x7, 0x2f, 0x2, 0x2, 0x1c0, 0x1c2, 
       0x5, 0x54, 0x2b, 0x2, 0x1c1, 0x1bf, 0x3, 0x2, 0x2, 0x2, 0x1c1, 0x1c2, 
       0x3, 0x2, 0x2, 0x2, 0x1c2, 0x1c3, 0x3, 0x2, 0x2, 0x2, 0x1c3, 0x1c4, 
       0x5, 0x2c, 0x17, 0x2, 0x1c4, 0x2b, 0x3, 0x2, 0x2, 0x2, 0x1c5, 0x1c8, 
       0x5, 0x82, 0x42, 0x2, 0x1c6, 0x1c8, 0x7, 0x45, 0x2, 0x2, 0x1c7, 0x1c5, 
       0x3, 0x2, 0x2, 0x2, 0x1c7, 0x1c6, 0x3, 0x2, 0x2, 0x2, 0x1c8, 0x2d, 
       0x3, 0x2, 0x2, 0x2, 0x1c9, 0x1cc, 0x5, 0xc8, 0x65, 0x2, 0x1ca, 0x1cc, 
       0x7, 0x32, 0x2, 0x2, 0x1cb, 0x1c9, 0x3, 0x2, 0x2, 0x2, 0x1cb, 0x1ca, 
       0x3, 0x2, 0x2, 0x2, 0x1cc, 0x2f, 0x3, 0x2, 0x2, 0x2, 0x1cd, 0x1ce, 
       0x5, 0x12, 0xa, 0x2, 0x1ce, 0x1cf, 0x5, 0x2a, 0x16, 0x2, 0x1cf, 0x31, 
       0x3, 0x2, 0x2, 0x2, 0x1d0, 0x1d1, 0x5, 0x12, 0xa, 0x2, 0x1d1, 0x1d2, 
       0x5, 0x34, 0x1b, 0x2, 0x1d2, 0x33, 0x3, 0x2, 0x2, 0x2, 0x1d3, 0x1d4, 
       0x7, 0x71, 0x2, 0x2, 0x1d4, 0x1d7, 0x5, 0x56, 0x2c, 0x2, 0x1d5, 0x1d6, 
       0x7, 0x2f, 0x2, 0x2, 0x1d6, 0x1d8, 0x5, 0x54, 0x2b, 0x2, 0x1d7, 0x1d5, 
       0x3, 0x2, 0x2, 0x2, 0x1d7, 0x1d8, 0x3, 0x2, 0x2, 0x2, 0x1d8, 0x1d9, 
       0x3, 0x2, 0x2, 0x2, 0x1d9, 0x1da, 0x5, 0x82, 0x42, 0x2, 0x1da, 0x35, 
       0x3, 0x2, 0x2, 0x2, 0x1db, 0x1dc, 0x5, 0xc8, 0x65, 0x2, 0x1dc, 0x1dd, 
       0x5, 0x46, 0x24, 0x2, 0x1dd, 0x1de, 0x7, 0x45, 0x2, 0x2, 0x1de, 0x37, 
       0x3, 0x2, 0x2, 0x2, 0x1df, 0x1e1, 0x5, 0xa, 0x6, 0x2, 0x1e0, 0x1df, 
       0x3, 0x2, 0x2, 0x2, 0x1e1, 0x1e4, 0x3, 0x2, 0x2, 0x2, 0x1e2, 0x1e0, 
       0x3, 0x2, 0x2, 0x2, 0x1e2, 0x1e3, 0x3, 0x2, 0x2, 0x2, 0x1e3, 0x1e5, 
       0x3, 0x2, 0x2, 0x2, 0x1e4, 0x1e2, 0x3, 0x2, 0x2, 0x2, 0x1e5, 0x1e8, 
       0x5, 0x3a, 0x1e, 0x2, 0x1e6, 0x1e8, 0x7, 0x45, 0x2, 0x2, 0x1e7, 0x1e2, 
       0x3, 0x2, 0x2, 0x2, 0x1e7, 0x1e6, 0x3, 0x2, 0x2, 0x2, 0x1e8, 0x39, 
       0x3, 0x2, 0x2, 0x2, 0x1e9, 0x1f1, 0x5, 0x3c, 0x1f, 0x2, 0x1ea, 0x1f1, 
       0x5, 0x40, 0x21, 0x2, 0x1eb, 0x1f1, 0x5, 0x44, 0x23, 0x2, 0x1ec, 
       0x1f1, 0x5, 0x20, 0x11, 0x2, 0x1ed, 0x1f1, 0x5, 0x72, 0x3a, 0x2, 
       0x1ee, 0x1f1, 0x5, 0x10, 0x9, 0x2, 0x1ef, 0x1f1, 0x5, 0x18, 0xd, 
       0x2, 0x1f0, 0x1e9, 0x3, 0x2, 0x2, 0x2, 0x1f0, 0x1ea, 0x3, 0x2, 0x2, 
       0x2, 0x1f0, 0x1eb, 0x3, 0x2, 0x2, 0x2, 0x1f0, 0x1ec, 0x3, 0x2, 0x2, 
       0x2, 0x1f0, 0x1ed, 0x3, 0x2, 0x2, 0x2, 0x1f0, 0x1ee, 0x3, 0x2, 0x2, 
       0x2, 0x1f0, 0x1ef, 0x3, 0x2, 0x2, 0x2, 0x1f1, 0x3b, 0x3, 0x2, 0x2, 
       0x2, 0x1f2, 0x1f3, 0x5, 0xc8, 0x65, 0x2, 0x1f3, 0x1f8, 0x5, 0x3e, 
       0x20, 0x2, 0x1f4, 0x1f5, 0x7, 0x46, 0x2, 0x2, 0x1f5, 0x1f7, 0x5, 
       0x3e, 0x20, 0x2, 0x1f6, 0x1f4, 0x3, 0x2, 0x2, 0x2, 0x1f7, 0x1fa, 
       0x3, 0x2, 0x2, 0x2, 0x1f8, 0x1f6, 0x3, 0x2, 0x2, 0x2, 0x1f8, 0x1f9, 
       0x3, 0x2, 0x2, 0x2, 0x1f9, 0x1fb, 0x3, 0x2, 0x2, 0x2, 0x1fa, 0x1f8, 
       0x3, 0x2, 0x2, 0x2, 0x1fb, 0x1fc, 0x7, 0x45, 0x2, 0x2, 0x1fc, 0x3d, 
       0x3, 0x2, 0x2, 0x2, 0x1fd, 0x202, 0x7, 0x71, 0x2, 0x2, 0x1fe, 0x1ff, 
       0x7, 0x43, 0x2, 0x2, 0x1ff, 0x201, 0x7, 0x44, 0x2, 0x2, 0x200, 0x1fe, 
       0x3, 0x2, 0x2, 0x2, 0x201, 0x204, 0x3, 0x2, 0x2, 0x2, 0x202, 0x200, 
       0x3, 0x2, 0x2, 0x2, 0x202, 0x203, 0x3, 0x2, 0x2, 0x2, 0x203, 0x205, 
       0x3, 0x2, 0x2, 0x2, 0x204, 0x202, 0x3, 0x2, 0x2, 0x2, 0x205, 0x206, 
       0x7, 0x48, 0x2, 0x2, 0x206, 0x207, 0x5, 0x4c, 0x27, 0x2, 0x207, 0x3f, 
       0x3, 0x2, 0x2, 0x2, 0x208, 0x20a, 0x5, 0x42, 0x22, 0x2, 0x209, 0x208, 
       0x3, 0x2, 0x2, 0x2, 0x20a, 0x20d, 0x3, 0x2, 0x2, 0x2, 0x20b, 0x209, 
       0x3, 0x2, 0x2, 0x2, 0x20b, 0x20c, 0x3, 0x2, 0x2, 0x2, 0x20c, 0x218, 
       0x3, 0x2, 0x2, 0x2, 0x20d, 0x20b, 0x3, 0x2, 0x2, 0x2, 0x20e, 0x219, 
       0x5, 0x2e, 0x18, 0x2, 0x20f, 0x213, 0x5, 0x12, 0xa, 0x2, 0x210, 0x212, 
       0x5, 0x68, 0x35, 0x2, 0x211, 0x210, 0x3, 0x2, 0x2, 0x2, 0x212, 0x215, 
       0x3, 0x2, 0x2, 0x2, 0x213, 0x211, 0x3, 0x2, 0x2, 0x2, 0x213, 0x214, 
       0x3, 0x2, 0x2, 0x2, 0x214, 0x216, 0x3, 0x2, 0x2, 0x2, 0x215, 0x213, 
       0x3, 0x2, 0x2, 0x2, 0x216, 0x217, 0x5, 0x2e, 0x18, 0x2, 0x217, 0x219, 
       0x3, 0x2, 0x2, 0x2, 0x218, 0x20e, 0x3, 0x2, 0x2, 0x2, 0x218, 0x20f, 
       0x3, 0x2, 0x2, 0x2, 0x219, 0x21a, 0x3, 0x2, 0x2, 0x2, 0x21a, 0x21b, 
       0x7, 0x71, 0x2, 0x2, 0x21b, 0x220, 0x5, 0x56, 0x2c, 0x2, 0x21c, 0x21d, 
       0x7, 0x43, 0x2, 0x2, 0x21d, 0x21f, 0x7, 0x44, 0x2, 0x2, 0x21e, 0x21c, 
       0x3, 0x2, 0x2, 0x2, 0x21f, 0x222, 0x3, 0x2, 0x2, 0x2, 0x220, 0x21e, 
       0x3, 0x2, 0x2, 0x2, 0x220, 0x221, 0x3, 0x2, 0x2, 0x2, 0x221, 0x225, 
       0x3, 0x2, 0x2, 0x2, 0x222, 0x220, 0x3, 0x2, 0x2, 0x2, 0x223, 0x224, 
       0x7, 0x2f, 0x2, 0x2, 0x224, 0x226, 0x5, 0x54, 0x2b, 0x2, 0x225, 0x223, 
       0x3, 0x2, 0x2, 0x2, 0x225, 0x226, 0x3, 0x2, 0x2, 0x2, 0x226, 0x227, 
       0x3, 0x2, 0x2, 0x2, 0x227, 0x228, 0x5, 0x2c, 0x17, 0x2, 0x228, 0x41, 
       0x3, 0x2, 0x2, 0x2, 0x229, 0x230, 0x5, 0x68, 0x35, 0x2, 0x22a, 0x230, 
       0x7, 0x25, 0x2, 0x2, 0x22b, 0x230, 0x7, 0x3, 0x2, 0x2, 0x22c, 0x230, 
       0x7, 0xe, 0x2, 0x2, 0x22d, 0x230, 0x7, 0x28, 0x2, 0x2, 0x22e, 0x230, 
       0x7, 0x29, 0x2, 0x2, 0x22f, 0x229, 0x3, 0x2, 0x2, 0x2, 0x22f, 0x22a, 
       0x3, 0x2, 0x2, 0x2, 0x22f, 0x22b, 0x3, 0x2, 0x2, 0x2, 0x22f, 0x22c, 
       0x3, 0x2, 0x2, 0x2, 0x22f, 0x22d, 0x3, 0x2, 0x2, 0x2, 0x22f, 0x22e, 
       0x3, 0x2, 0x2, 0x2, 0x230, 0x43, 0x3, 0x2, 0x2, 0x2, 0x231, 0x232, 
       0x5, 0x12, 0xa, 0x2, 0x232, 0x233, 0x5, 0x40, 0x21, 0x2, 0x233, 0x45, 
       0x3, 0x2, 0x2, 0x2, 0x234, 0x239, 0x5, 0x48, 0x25, 0x2, 0x235, 0x236, 
       0x7, 0x46, 0x2, 0x2, 0x236, 0x238, 0x5, 0x48, 0x25, 0x2, 0x237, 0x235, 
       0x3, 0x2, 0x2, 0x2, 0x238, 0x23b, 0x3, 0x2, 0x2, 0x2, 0x239, 0x237, 
       0x3, 0x2, 0x2, 0x2, 0x239, 0x23a, 0x3, 0x2, 0x2, 0x2, 0x23a, 0x47, 
       0x3, 0x2, 0x2, 0x2, 0x23b, 0x239, 0x3, 0x2, 0x2, 0x2, 0x23c, 0x23f, 
       0x5, 0x4a, 0x26, 0x2, 0x23d, 0x23e, 0x7, 0x48, 0x2, 0x2, 0x23e, 0x240, 
       0x5, 0x4c, 0x27, 0x2, 0x23f, 0x23d, 0x3, 0x2, 0x2, 0x2, 0x23f, 0x240, 
       0x3, 0x2, 0x2, 0x2, 0x240, 0x49, 0x3, 0x2, 0x2, 0x2, 0x241, 0x246, 
       0x7, 0x71, 0x2, 0x2, 0x242, 0x243, 0x7, 0x43, 0x2, 0x2, 0x243, 0x245, 
       0x7, 0x44, 0x2, 0x2, 0x244, 0x242, 0x3, 0x2, 0x2, 0x2, 0x245, 0x248, 
       0x3, 0x2, 0x2, 0x2, 0x246, 0x244, 0x3, 0x2, 0x2, 0x2, 0x246, 0x247, 
       0x3, 0x2, 0x2, 0x2, 0x247, 0x4b, 0x3, 0x2, 0x2, 0x2, 0x248, 0x246, 
       0x3, 0x2, 0x2, 0x2, 0x249, 0x24c, 0x5, 0x4e, 0x28, 0x2, 0x24a, 0x24c, 
       0x5, 0xa8, 0x55, 0x2, 0x24b, 0x249, 0x3, 0x2, 0x2, 0x2, 0x24b, 0x24a, 
       0x3, 0x2, 0x2, 0x2, 0x24c, 0x4d, 0x3, 0x2, 0x2, 0x2, 0x24d, 0x259, 
       0x7, 0x41, 0x2, 0x2, 0x24e, 0x253, 0x5, 0x4c, 0x27, 0x2, 0x24f, 0x250, 
       0x7, 0x46, 0x2, 0x2, 0x250, 0x252, 0x5, 0x4c, 0x27, 0x2, 0x251, 0x24f, 
       0x3, 0x2, 0x2, 0x2, 0x252, 0x255, 0x3, 0x2, 0x2, 0x2, 0x253, 0x251, 
       0x3, 0x2, 0x2, 0x2, 0x253, 0x254, 0x3, 0x2, 0x2, 0x2, 0x254, 0x257, 
       0x3, 0x2, 0x2, 0x2, 0x255, 0x253, 0x3, 0x2, 0x2, 0x2, 0x256, 0x258, 
       0x7, 0x46, 0x2, 0x2, 0x257, 0x256, 0x3, 0x2, 0x2, 0x2, 0x257, 0x258, 
       0x3, 0x2, 0x2, 0x2, 0x258, 0x25a, 0x3, 0x2, 0x2, 0x2, 0x259, 0x24e, 
       0x3, 0x2, 0x2, 0x2, 0x259, 0x25a, 0x3, 0x2, 0x2, 0x2, 0x25a, 0x25b, 
       0x3, 0x2, 0x2, 0x2, 0x25b, 0x25c, 0x7, 0x42, 0x2, 0x2, 0x25c, 0x4f, 
       0x3, 0x2, 0x2, 0x2, 0x25d, 0x25f, 0x7, 0x71, 0x2, 0x2, 0x25e, 0x260, 
       0x5, 0xcc, 0x67, 0x2, 0x25f, 0x25e, 0x3, 0x2, 0x2, 0x2, 0x25f, 0x260, 
       0x3, 0x2, 0x2, 0x2, 0x260, 0x268, 0x3, 0x2, 0x2, 0x2, 0x261, 0x262, 
       0x7, 0x47, 0x2, 0x2, 0x262, 0x264, 0x7, 0x71, 0x2, 0x2, 0x263, 0x265, 
       0x5, 0xcc, 0x67, 0x2, 0x264, 0x263, 0x3, 0x2, 0x2, 0x2, 0x264, 0x265, 
       0x3, 0x2, 0x2, 0x2, 0x265, 0x267, 0x3, 0x2, 0x2, 0x2, 0x266, 0x261, 
       0x3, 0x2, 0x2, 0x2, 0x267, 0x26a, 0x3, 0x2, 0x2, 0x2, 0x268, 0x266, 
       0x3, 0x2, 0x2, 0x2, 0x268, 0x269, 0x3, 0x2, 0x2, 0x2, 0x269, 0x51, 
       0x3, 0x2, 0x2, 0x2, 0x26a, 0x268, 0x3, 0x2, 0x2, 0x2, 0x26b, 0x278, 
       0x5, 0xc8, 0x65, 0x2, 0x26c, 0x26e, 0x5, 0x68, 0x35, 0x2, 0x26d, 
       0x26c, 0x3, 0x2, 0x2, 0x2, 0x26e, 0x271, 0x3, 0x2, 0x2, 0x2, 0x26f, 
       0x26d, 0x3, 0x2, 0x2, 0x2, 0x26f, 0x270, 0x3, 0x2, 0x2, 0x2, 0x270, 
       0x272, 0x3, 0x2, 0x2, 0x2, 0x271, 0x26f, 0x3, 0x2, 0x2, 0x2, 0x272, 
       0x275, 0x7, 0x4d, 0x2, 0x2, 0x273, 0x274, 0x9, 0x2, 0x2, 0x2, 0x274, 
       0x276, 0x5, 0xc8, 0x65, 0x2, 0x275, 0x273, 0x3, 0x2, 0x2, 0x2, 0x275, 
       0x276, 0x3, 0x2, 0x2, 0x2, 0x276, 0x278, 0x3, 0x2, 0x2, 0x2, 0x277, 
       0x26b, 0x3, 0x2, 0x2, 0x2, 0x277, 0x26f, 0x3, 0x2, 0x2, 0x2, 0x278, 
       0x53, 0x3, 0x2, 0x2, 0x2, 0x279, 0x27e, 0x5, 0x5e, 0x30, 0x2, 0x27a, 
       0x27b, 0x7, 0x46, 0x2, 0x2, 0x27b, 0x27d, 0x5, 0x5e, 0x30, 0x2, 0x27c, 
       0x27a, 0x3, 0x2, 0x2, 0x2, 0x27d, 0x280, 0x3, 0x2, 0x2, 0x2, 0x27e, 
       0x27c, 0x3, 0x2, 0x2, 0x2, 0x27e, 0x27f, 0x3, 0x2, 0x2, 0x2, 0x27f, 
       0x55, 0x3, 0x2, 0x2, 0x2, 0x280, 0x27e, 0x3, 0x2, 0x2, 0x2, 0x281, 
       0x283, 0x7, 0x3f, 0x2, 0x2, 0x282, 0x284, 0x5, 0x58, 0x2d, 0x2, 0x283, 
       0x282, 0x3, 0x2, 0x2, 0x2, 0x283, 0x284, 0x3, 0x2, 0x2, 0x2, 0x284, 
       0x285, 0x3, 0x2, 0x2, 0x2, 0x285, 0x286, 0x7, 0x40, 0x2, 0x2, 0x286, 
       0x57, 0x3, 0x2, 0x2, 0x2, 0x287, 0x28c, 0x5, 0x5a, 0x2e, 0x2, 0x288, 
       0x289, 0x7, 0x46, 0x2, 0x2, 0x289, 0x28b, 0x5, 0x5a, 0x2e, 0x2, 0x28a, 
       0x288, 0x3, 0x2, 0x2, 0x2, 0x28b, 0x28e, 0x3, 0x2, 0x2, 0x2, 0x28c, 
       0x28a, 0x3, 0x2, 0x2, 0x2, 0x28c, 0x28d, 0x3, 0x2, 0x2, 0x2, 0x28d, 
       0x291, 0x3, 0x2, 0x2, 0x2, 0x28e, 0x28c, 0x3, 0x2, 0x2, 0x2, 0x28f, 
       0x290, 0x7, 0x46, 0x2, 0x2, 0x290, 0x292, 0x5, 0x5c, 0x2f, 0x2, 0x291, 
       0x28f, 0x3, 0x2, 0x2, 0x2, 0x291, 0x292, 0x3, 0x2, 0x2, 0x2, 0x292, 
       0x295, 0x3, 0x2, 0x2, 0x2, 0x293, 0x295, 0x5, 0x5c, 0x2f, 0x2, 0x294, 
       0x287, 0x3, 0x2, 0x2, 0x2, 0x294, 0x293, 0x3, 0x2, 0x2, 0x2, 0x295, 
       0x59, 0x3, 0x2, 0x2, 0x2, 0x296, 0x298, 0x5, 0xe, 0x8, 0x2, 0x297, 
       0x296, 0x3, 0x2, 0x2, 0x2, 0x298, 0x29b, 0x3, 0x2, 0x2, 0x2, 0x299, 
       0x297, 0x3, 0x2, 0x2, 0x2, 0x299, 0x29a, 0x3, 0x2, 0x2, 0x2, 0x29a, 
       0x29c, 0x3, 0x2, 0x2, 0x2, 0x29b, 0x299, 0x3, 0x2, 0x2, 0x2, 0x29c, 
       0x29d, 0x5, 0xc8, 0x65, 0x2, 0x29d, 0x29e, 0x5, 0x4a, 0x26, 0x2, 
       0x29e, 0x5b, 0x3, 0x2, 0x2, 0x2, 0x29f, 0x2a1, 0x5, 0xe, 0x8, 0x2, 
       0x2a0, 0x29f, 0x3, 0x2, 0x2, 0x2, 0x2a1, 0x2a4, 0x3, 0x2, 0x2, 0x2, 
       0x2a2, 0x2a0, 0x3, 0x2, 0x2, 0x2, 0x2a2, 0x2a3, 0x3, 0x2, 0x2, 0x2, 
       0x2a3, 0x2a5, 0x3, 0x2, 0x2, 0x2, 0x2a4, 0x2a2, 0x3, 0x2, 0x2, 0x2, 
       0x2a5, 0x2a9, 0x5, 0xc8, 0x65, 0x2, 0x2a6, 0x2a8, 0x5, 0x68, 0x35, 
       0x2, 0x2a7, 0x2a6, 0x3, 0x2, 0x2, 0x2, 0x2a8, 0x2ab, 0x3, 0x2, 0x2, 
       0x2, 0x2a9, 0x2a7, 0x3, 0x2, 0x2, 0x2, 0x2a9, 0x2aa, 0x3, 0x2, 0x2, 
       0x2, 0x2aa, 0x2ac, 0x3, 0x2, 0x2, 0x2, 0x2ab, 0x2a9, 0x3, 0x2, 0x2, 
       0x2, 0x2ac, 0x2ad, 0x7, 0x6d, 0x2, 0x2, 0x2ad, 0x2ae, 0x5, 0x4a, 
       0x26, 0x2, 0x2ae, 0x5d, 0x3, 0x2, 0x2, 0x2, 0x2af, 0x2b4, 0x7, 0x71, 
       0x2, 0x2, 0x2b0, 0x2b1, 0x7, 0x47, 0x2, 0x2, 0x2b1, 0x2b3, 0x7, 0x71, 
       0x2, 0x2, 0x2b2, 0x2b0, 0x3, 0x2, 0x2, 0x2, 0x2b3, 0x2b6, 0x3, 0x2, 
       0x2, 0x2, 0x2b4, 0x2b2, 0x3, 0x2, 0x2, 0x2, 0x2b4, 0x2b5, 0x3, 0x2, 
       0x2, 0x2, 0x2b5, 0x5f, 0x3, 0x2, 0x2, 0x2, 0x2b6, 0x2b4, 0x3, 0x2, 
       0x2, 0x2, 0x2b7, 0x2be, 0x5, 0x62, 0x32, 0x2, 0x2b8, 0x2be, 0x5, 
       0x64, 0x33, 0x2, 0x2b9, 0x2be, 0x7, 0x3c, 0x2, 0x2, 0x2ba, 0x2be, 
       0x7, 0x3d, 0x2, 0x2, 0x2bb, 0x2be, 0x7, 0x3b, 0x2, 0x2, 0x2bc, 0x2be, 
       0x7, 0x3e, 0x2, 0x2, 0x2bd, 0x2b7, 0x3, 0x2, 0x2, 0x2, 0x2bd, 0x2b8, 
       0x3, 0x2, 0x2, 0x2, 0x2bd, 0x2b9, 0x3, 0x2, 0x2, 0x2, 0x2bd, 0x2ba, 
       0x3, 0x2, 0x2, 0x2, 0x2bd, 0x2bb, 0x3, 0x2, 0x2, 0x2, 0x2bd, 0x2bc, 
       0x3, 0x2, 0x2, 0x2, 0x2be, 0x61, 0x3, 0x2, 0x2, 0x2, 0x2bf, 0x2c0, 
       0x9, 0x3, 0x2, 0x2, 0x2c0, 0x63, 0x3, 0x2, 0x2, 0x2, 0x2c1, 0x2c2, 
       0x9, 0x4, 0x2, 0x2, 0x2c2, 0x65, 0x3, 0x2, 0x2, 0x2, 0x2c3, 0x2c4, 
       0x7, 0x71, 0x2, 0x2, 0x2c4, 0x2c6, 0x7, 0x47, 0x2, 0x2, 0x2c5, 0x2c3, 
       0x3, 0x2, 0x2, 0x2, 0x2c6, 0x2c9, 0x3, 0x2, 0x2, 0x2, 0x2c7, 0x2c5, 
       0x3, 0x2, 0x2, 0x2, 0x2c7, 0x2c8, 0x3, 0x2, 0x2, 0x2, 0x2c8, 0x2ca, 
       0x3, 0x2, 0x2, 0x2, 0x2c9, 0x2c7, 0x3, 0x2, 0x2, 0x2, 0x2ca, 0x2cb, 
       0x7, 0x6c, 0x2, 0x2, 0x2cb, 0x2cc, 0x7, 0x71, 0x2, 0x2, 0x2cc, 0x67, 
       0x3, 0x2, 0x2, 0x2, 0x2cd, 0x2ce, 0x7, 0x6c, 0x2, 0x2, 0x2ce, 0x2d1, 
       0x5, 0x5e, 0x30, 0x2, 0x2cf, 0x2d1, 0x5, 0x66, 0x34, 0x2, 0x2d0, 
       0x2cd, 0x3, 0x2, 0x2, 0x2, 0x2d0, 0x2cf, 0x3, 0x2, 0x2, 0x2, 0x2d1, 
       0x2d8, 0x3, 0x2, 0x2, 0x2, 0x2d2, 0x2d5, 0x7, 0x3f, 0x2, 0x2, 0x2d3, 
       0x2d6, 0x5, 0x6a, 0x36, 0x2, 0x2d4, 0x2d6, 0x5, 0x6e, 0x38, 0x2, 
       0x2d5, 0x2d3, 0x3, 0x2, 0x2, 0x2, 0x2d5, 0x2d4, 0x3, 0x2, 0x2, 0x2, 
       0x2d5, 0x2d6, 0x3, 0x2, 0x2, 0x2, 0x2d6, 0x2d7, 0x3, 0x2, 0x2, 0x2, 
       0x2d7, 0x2d9, 0x7, 0x40, 0x2, 0x2, 0x2d8, 0x2d2, 0x3, 0x2, 0x2, 0x2, 
       0x2d8, 0x2d9, 0x3, 0x2, 0x2, 0x2, 0x2d9, 0x69, 0x3, 0x2, 0x2, 0x2, 
       0x2da, 0x2df, 0x5, 0x6c, 0x37, 0x2, 0x2db, 0x2dc, 0x7, 0x46, 0x2, 
       0x2, 0x2dc, 0x2de, 0x5, 0x6c, 0x37, 0x2, 0x2dd, 0x2db, 0x3, 0x2, 
       0x2, 0x2, 0x2de, 0x2e1, 0x3, 0x2, 0x2, 0x2, 0x2df, 0x2dd, 0x3, 0x2, 
       0x2, 0x2, 0x2df, 0x2e0, 0x3, 0x2, 0x2, 0x2, 0x2e0, 0x6b, 0x3, 0x2, 
       0x2, 0x2, 0x2e1, 0x2df, 0x3, 0x2, 0x2, 0x2, 0x2e2, 0x2e3, 0x7, 0x71, 
       0x2, 0x2, 0x2e3, 0x2e4, 0x7, 0x48, 0x2, 0x2, 0x2e4, 0x2e5, 0x5, 0x6e, 
       0x38, 0x2, 0x2e5, 0x6d, 0x3, 0x2, 0x2, 0x2, 0x2e6, 0x2ea, 0x5, 0xa8, 
       0x55, 0x2, 0x2e7, 0x2ea, 0x5, 0x68, 0x35, 0x2, 0x2e8, 0x2ea, 0x5, 
       0x70, 0x39, 0x2, 0x2e9, 0x2e6, 0x3, 0x2, 0x2, 0x2, 0x2e9, 0x2e7, 
       0x3, 0x2, 0x2, 0x2, 0x2e9, 0x2e8, 0x3, 0x2, 0x2, 0x2, 0x2ea, 0x6f, 
       0x3, 0x2, 0x2, 0x2, 0x2eb, 0x2f4, 0x7, 0x41, 0x2, 0x2, 0x2ec, 0x2f1, 
       0x5, 0x6e, 0x38, 0x2, 0x2ed, 0x2ee, 0x7, 0x46, 0x2, 0x2, 0x2ee, 0x2f0, 
       0x5, 0x6e, 0x38, 0x2, 0x2ef, 0x2ed, 0x3, 0x2, 0x2, 0x2, 0x2f0, 0x2f3, 
       0x3, 0x2, 0x2, 0x2, 0x2f1, 0x2ef, 0x3, 0x2, 0x2, 0x2, 0x2f1, 0x2f2, 
       0x3, 0x2, 0x2, 0x2, 0x2f2, 0x2f5, 0x3, 0x2, 0x2, 0x2, 0x2f3, 0x2f1, 
       0x3, 0x2, 0x2, 0x2, 0x2f4, 0x2ec, 0x3, 0x2, 0x2, 0x2, 0x2f4, 0x2f5, 
       0x3, 0x2, 0x2, 0x2, 0x2f5, 0x2f7, 0x3, 0x2, 0x2, 0x2, 0x2f6, 0x2f8, 
       0x7, 0x46, 0x2, 0x2, 0x2f7, 0x2f6, 0x3, 0x2, 0x2, 0x2, 0x2f7, 0x2f8, 
       0x3, 0x2, 0x2, 0x2, 0x2f8, 0x2f9, 0x3, 0x2, 0x2, 0x2, 0x2f9, 0x2fa, 
       0x7, 0x42, 0x2, 0x2, 0x2fa, 0x71, 0x3, 0x2, 0x2, 0x2, 0x2fb, 0x2fc, 
       0x7, 0x6c, 0x2, 0x2, 0x2fc, 0x2fd, 0x7, 0x1e, 0x2, 0x2, 0x2fd, 0x2fe, 
       0x7, 0x71, 0x2, 0x2, 0x2fe, 0x2ff, 0x5, 0x74, 0x3b, 0x2, 0x2ff, 0x73, 
       0x3, 0x2, 0x2, 0x2, 0x300, 0x304, 0x7, 0x41, 0x2, 0x2, 0x301, 0x303, 
       0x5, 0x76, 0x3c, 0x2, 0x302, 0x301, 0x3, 0x2, 0x2, 0x2, 0x303, 0x306, 
       0x3, 0x2, 0x2, 0x2, 0x304, 0x302, 0x3, 0x2, 0x2, 0x2, 0x304, 0x305, 
       0x3, 0x2, 0x2, 0x2, 0x305, 0x307, 0x3, 0x2, 0x2, 0x2, 0x306, 0x304, 
       0x3, 0x2, 0x2, 0x2, 0x307, 0x308, 0x7, 0x42, 0x2, 0x2, 0x308, 0x75, 
       0x3, 0x2, 0x2, 0x2, 0x309, 0x30b, 0x5, 0xa, 0x6, 0x2, 0x30a, 0x309, 
       0x3, 0x2, 0x2, 0x2, 0x30b, 0x30e, 0x3, 0x2, 0x2, 0x2, 0x30c, 0x30a, 
       0x3, 0x2, 0x2, 0x2, 0x30c, 0x30d, 0x3, 0x2, 0x2, 0x2, 0x30d, 0x30f, 
       0x3, 0x2, 0x2, 0x2, 0x30e, 0x30c, 0x3, 0x2, 0x2, 0x2, 0x30f, 0x312, 
       0x5, 0x78, 0x3d, 0x2, 0x310, 0x312, 0x7, 0x45, 0x2, 0x2, 0x311, 0x30c, 
       0x3, 0x2, 0x2, 0x2, 0x311, 0x310, 0x3, 0x2, 0x2, 0x2, 0x312, 0x77, 
       0x3, 0x2, 0x2, 0x2, 0x313, 0x314, 0x5, 0xc8, 0x65, 0x2, 0x314, 0x315, 
       0x5, 0x7a, 0x3e, 0x2, 0x315, 0x316, 0x7, 0x45, 0x2, 0x2, 0x316, 0x328, 
       0x3, 0x2, 0x2, 0x2, 0x317, 0x319, 0x5, 0x10, 0x9, 0x2, 0x318, 0x31a, 
       0x7, 0x45, 0x2, 0x2, 0x319, 0x318, 0x3, 0x2, 0x2, 0x2, 0x319, 0x31a, 
       0x3, 0x2, 0x2, 0x2, 0x31a, 0x328, 0x3, 0x2, 0x2, 0x2, 0x31b, 0x31d, 
       0x5, 0x20, 0x11, 0x2, 0x31c, 0x31e, 0x7, 0x45, 0x2, 0x2, 0x31d, 0x31c, 
       0x3, 0x2, 0x2, 0x2, 0x31d, 0x31e, 0x3, 0x2, 0x2, 0x2, 0x31e, 0x328, 
       0x3, 0x2, 0x2, 0x2, 0x31f, 0x321, 0x5, 0x18, 0xd, 0x2, 0x320, 0x322, 
       0x7, 0x45, 0x2, 0x2, 0x321, 0x320, 0x3, 0x2, 0x2, 0x2, 0x321, 0x322, 
       0x3, 0x2, 0x2, 0x2, 0x322, 0x328, 0x3, 0x2, 0x2, 0x2, 0x323, 0x325, 
       0x5, 0x72, 0x3a, 0x2, 0x324, 0x326, 0x7, 0x45, 0x2, 0x2, 0x325, 0x324, 
       0x3, 0x2, 0x2, 0x2, 0x325, 0x326, 0x3, 0x2, 0x2, 0x2, 0x326, 0x328, 
       0x3, 0x2, 0x2, 0x2, 0x327, 0x313, 0x3, 0x2, 0x2, 0x2, 0x327, 0x317, 
       0x3, 0x2, 0x2, 0x2, 0x327, 0x31b, 0x3, 0x2, 0x2, 0x2, 0x327, 0x31f, 
       0x3, 0x2, 0x2, 0x2, 0x327, 0x323, 0x3, 0x2, 0x2, 0x2, 0x328, 0x79, 
       0x3, 0x2, 0x2, 0x2, 0x329, 0x32c, 0x5, 0x7c, 0x3f, 0x2, 0x32a, 0x32c, 
       0x5, 0x7e, 0x40, 0x2, 0x32b, 0x329, 0x3, 0x2, 0x2, 0x2, 0x32b, 0x32a, 
       0x3, 0x2, 0x2, 0x2, 0x32c, 0x7b, 0x3, 0x2, 0x2, 0x2, 0x32d, 0x32e, 
       0x7, 0x71, 0x2, 0x2, 0x32e, 0x32f, 0x7, 0x3f, 0x2, 0x2, 0x32f, 0x331, 
       0x7, 0x40, 0x2, 0x2, 0x330, 0x332, 0x5, 0x80, 0x41, 0x2, 0x331, 0x330, 
       0x3, 0x2, 0x2, 0x2, 0x331, 0x332, 0x3, 0x2, 0x2, 0x2, 0x332, 0x7d, 
       0x3, 0x2, 0x2, 0x2, 0x333, 0x334, 0x5, 0x46, 0x24, 0x2, 0x334, 0x7f, 
       0x3, 0x2, 0x2, 0x2, 0x335, 0x336, 0x7, 0xe, 0x2, 0x2, 0x336, 0x337, 
       0x5, 0x6e, 0x38, 0x2, 0x337, 0x81, 0x3, 0x2, 0x2, 0x2, 0x338, 0x33c, 
       0x7, 0x41, 0x2, 0x2, 0x339, 0x33b, 0x5, 0x84, 0x43, 0x2, 0x33a, 0x339, 
       0x3, 0x2, 0x2, 0x2, 0x33b, 0x33e, 0x3, 0x2, 0x2, 0x2, 0x33c, 0x33a, 
       0x3, 0x2, 0x2, 0x2, 0x33c, 0x33d, 0x3, 0x2, 0x2, 0x2, 0x33d, 0x33f, 
       0x3, 0x2, 0x2, 0x2, 0x33e, 0x33c, 0x3, 0x2, 0x2, 0x2, 0x33f, 0x340, 
       0x7, 0x42, 0x2, 0x2, 0x340, 0x83, 0x3, 0x2, 0x2, 0x2, 0x341, 0x342, 
       0x5, 0x86, 0x44, 0x2, 0x342, 0x343, 0x7, 0x45, 0x2, 0x2, 0x343, 0x347, 
       0x3, 0x2, 0x2, 0x2, 0x344, 0x347, 0x5, 0x8a, 0x46, 0x2, 0x345, 0x347, 
       0x5, 0x88, 0x45, 0x2, 0x346, 0x341, 0x3, 0x2, 0x2, 0x2, 0x346, 0x344, 
       0x3, 0x2, 0x2, 0x2, 0x346, 0x345, 0x3, 0x2, 0x2, 0x2, 0x347, 0x85, 
       0x3, 0x2, 0x2, 0x2, 0x348, 0x34a, 0x5, 0xe, 0x8, 0x2, 0x349, 0x348, 
       0x3, 0x2, 0x2, 0x2, 0x34a, 0x34d, 0x3, 0x2, 0x2, 0x2, 0x34b, 0x349, 
       0x3, 0x2, 0x2, 0x2, 0x34b, 0x34c, 0x3, 0x2, 0x2, 0x2, 0x34c, 0x34e, 
       0x3, 0x2, 0x2, 0x2, 0x34d, 0x34b, 0x3, 0x2, 0x2, 0x2, 0x34e, 0x34f, 
       0x5, 0xc8, 0x65, 0x2, 0x34f, 0x350, 0x5, 0x46, 0x24, 0x2, 0x350, 
       0x87, 0x3, 0x2, 0x2, 0x2, 0x351, 0x353, 0x5, 0xc, 0x7, 0x2, 0x352, 
       0x351, 0x3, 0x2, 0x2, 0x2, 0x353, 0x356, 0x3, 0x2, 0x2, 0x2, 0x354, 
       0x352, 0x3, 0x2, 0x2, 0x2, 0x354, 0x355, 0x3, 0x2, 0x2, 0x2, 0x355, 
       0x359, 0x3, 0x2, 0x2, 0x2, 0x356, 0x354, 0x3, 0x2, 0x2, 0x2, 0x357, 
       0x35a, 0x5, 0x10, 0x9, 0x2, 0x358, 0x35a, 0x5, 0x20, 0x11, 0x2, 0x359, 
       0x357, 0x3, 0x2, 0x2, 0x2, 0x359, 0x358, 0x3, 0x2, 0x2, 0x2, 0x35a, 
       0x35d, 0x3, 0x2, 0x2, 0x2, 0x35b, 0x35d, 0x7, 0x45, 0x2, 0x2, 0x35c, 
       0x354, 0x3, 0x2, 0x2, 0x2, 0x35c, 0x35b, 0x3, 0x2, 0x2, 0x2, 0x35d, 
       0x89, 0x3, 0x2, 0x2, 0x2, 0x35e, 0x3c7, 0x5, 0x82, 0x42, 0x2, 0x35f, 
       0x360, 0x7, 0x4, 0x2, 0x2, 0x360, 0x363, 0x5, 0xa8, 0x55, 0x2, 0x361, 
       0x362, 0x7, 0x4e, 0x2, 0x2, 0x362, 0x364, 0x5, 0xa8, 0x55, 0x2, 0x363, 
       0x361, 0x3, 0x2, 0x2, 0x2, 0x363, 0x364, 0x3, 0x2, 0x2, 0x2, 0x364, 
       0x365, 0x3, 0x2, 0x2, 0x2, 0x365, 0x366, 0x7, 0x45, 0x2, 0x2, 0x366, 
       0x3c7, 0x3, 0x2, 0x2, 0x2, 0x367, 0x368, 0x7, 0x18, 0x2, 0x2, 0x368, 
       0x369, 0x5, 0xa2, 0x52, 0x2, 0x369, 0x36c, 0x5, 0x8a, 0x46, 0x2, 
       0x36a, 0x36b, 0x7, 0x11, 0x2, 0x2, 0x36b, 0x36d, 0x5, 0x8a, 0x46, 
       0x2, 0x36c, 0x36a, 0x3, 0x2, 0x2, 0x2, 0x36c, 0x36d, 0x3, 0x2, 0x2, 
       0x2, 0x36d, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x36e, 0x36f, 0x7, 0x17, 0x2, 
       0x2, 0x36f, 0x370, 0x7, 0x3f, 0x2, 0x2, 0x370, 0x371, 0x5, 0x9c, 
       0x4f, 0x2, 0x371, 0x372, 0x7, 0x40, 0x2, 0x2, 0x372, 0x373, 0x5, 
       0x8a, 0x46, 0x2, 0x373, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x374, 0x375, 
       0x7, 0x34, 0x2, 0x2, 0x375, 0x376, 0x5, 0xa2, 0x52, 0x2, 0x376, 0x377, 
       0x5, 0x8a, 0x46, 0x2, 0x377, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x378, 0x379, 
       0x7, 0xf, 0x2, 0x2, 0x379, 0x37a, 0x5, 0x8a, 0x46, 0x2, 0x37a, 0x37b, 
       0x7, 0x34, 0x2, 0x2, 0x37b, 0x37c, 0x5, 0xa2, 0x52, 0x2, 0x37c, 0x37d, 
       0x7, 0x45, 0x2, 0x2, 0x37d, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x37e, 0x37f, 
       0x7, 0x31, 0x2, 0x2, 0x37f, 0x389, 0x5, 0x82, 0x42, 0x2, 0x380, 0x382, 
       0x5, 0x8c, 0x47, 0x2, 0x381, 0x380, 0x3, 0x2, 0x2, 0x2, 0x382, 0x383, 
       0x3, 0x2, 0x2, 0x2, 0x383, 0x381, 0x3, 0x2, 0x2, 0x2, 0x383, 0x384, 
       0x3, 0x2, 0x2, 0x2, 0x384, 0x386, 0x3, 0x2, 0x2, 0x2, 0x385, 0x387, 
       0x5, 0x90, 0x49, 0x2, 0x386, 0x385, 0x3, 0x2, 0x2, 0x2, 0x386, 0x387, 
       0x3, 0x2, 0x2, 0x2, 0x387, 0x38a, 0x3, 0x2, 0x2, 0x2, 0x388, 0x38a, 
       0x5, 0x90, 0x49, 0x2, 0x389, 0x381, 0x3, 0x2, 0x2, 0x2, 0x389, 0x388, 
       0x3, 0x2, 0x2, 0x2, 0x38a, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x38b, 0x38c, 
       0x7, 0x31, 0x2, 0x2, 0x38c, 0x38d, 0x5, 0x92, 0x4a, 0x2, 0x38d, 0x391, 
       0x5, 0x82, 0x42, 0x2, 0x38e, 0x390, 0x5, 0x8c, 0x47, 0x2, 0x38f, 
       0x38e, 0x3, 0x2, 0x2, 0x2, 0x390, 0x393, 0x3, 0x2, 0x2, 0x2, 0x391, 
       0x38f, 0x3, 0x2, 0x2, 0x2, 0x391, 0x392, 0x3, 0x2, 0x2, 0x2, 0x392, 
       0x395, 0x3, 0x2, 0x2, 0x2, 0x393, 0x391, 0x3, 0x2, 0x2, 0x2, 0x394, 
       0x396, 0x5, 0x90, 0x49, 0x2, 0x395, 0x394, 0x3, 0x2, 0x2, 0x2, 0x395, 
       0x396, 0x3, 0x2, 0x2, 0x2, 0x396, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x397, 
       0x398, 0x7, 0x2b, 0x2, 0x2, 0x398, 0x399, 0x5, 0xa2, 0x52, 0x2, 0x399, 
       0x39d, 0x7, 0x41, 0x2, 0x2, 0x39a, 0x39c, 0x5, 0x98, 0x4d, 0x2, 0x39b, 
       0x39a, 0x3, 0x2, 0x2, 0x2, 0x39c, 0x39f, 0x3, 0x2, 0x2, 0x2, 0x39d, 
       0x39b, 0x3, 0x2, 0x2, 0x2, 0x39d, 0x39e, 0x3, 0x2, 0x2, 0x2, 0x39e, 
       0x3a3, 0x3, 0x2, 0x2, 0x2, 0x39f, 0x39d, 0x3, 0x2, 0x2, 0x2, 0x3a0, 
       0x3a2, 0x5, 0x9a, 0x4e, 0x2, 0x3a1, 0x3a0, 0x3, 0x2, 0x2, 0x2, 0x3a2, 
       0x3a5, 0x3, 0x2, 0x2, 0x2, 0x3a3, 0x3a1, 0x3, 0x2, 0x2, 0x2, 0x3a3, 
       0x3a4, 0x3, 0x2, 0x2, 0x2, 0x3a4, 0x3a6, 0x3, 0x2, 0x2, 0x2, 0x3a5, 
       0x3a3, 0x3, 0x2, 0x2, 0x2, 0x3a6, 0x3a7, 0x7, 0x42, 0x2, 0x2, 0x3a7, 
       0x3c7, 0x3, 0x2, 0x2, 0x2, 0x3a8, 0x3a9, 0x7, 0x2c, 0x2, 0x2, 0x3a9, 
       0x3aa, 0x5, 0xa2, 0x52, 0x2, 0x3aa, 0x3ab, 0x5, 0x82, 0x42, 0x2, 
       0x3ab, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x3ac, 0x3ae, 0x7, 0x26, 0x2, 0x2, 
       0x3ad, 0x3af, 0x5, 0xa8, 0x55, 0x2, 0x3ae, 0x3ad, 0x3, 0x2, 0x2, 
       0x2, 0x3ae, 0x3af, 0x3, 0x2, 0x2, 0x2, 0x3af, 0x3b0, 0x3, 0x2, 0x2, 
       0x2, 0x3b0, 0x3c7, 0x7, 0x45, 0x2, 0x2, 0x3b1, 0x3b2, 0x7, 0x2e, 
       0x2, 0x2, 0x3b2, 0x3b3, 0x5, 0xa8, 0x55, 0x2, 0x3b3, 0x3b4, 0x7, 
       0x45, 0x2, 0x2, 0x3b4, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x3b5, 0x3b7, 0x7, 
       0x6, 0x2, 0x2, 0x3b6, 0x3b8, 0x7, 0x71, 0x2, 0x2, 0x3b7, 0x3b6, 0x3, 
       0x2, 0x2, 0x2, 0x3b7, 0x3b8, 0x3, 0x2, 0x2, 0x2, 0x3b8, 0x3b9, 0x3, 
       0x2, 0x2, 0x2, 0x3b9, 0x3c7, 0x7, 0x45, 0x2, 0x2, 0x3ba, 0x3bc, 0x7, 
       0xd, 0x2, 0x2, 0x3bb, 0x3bd, 0x7, 0x71, 0x2, 0x2, 0x3bc, 0x3bb, 0x3, 
       0x2, 0x2, 0x2, 0x3bc, 0x3bd, 0x3, 0x2, 0x2, 0x2, 0x3bd, 0x3be, 0x3, 
       0x2, 0x2, 0x2, 0x3be, 0x3c7, 0x7, 0x45, 0x2, 0x2, 0x3bf, 0x3c7, 0x7, 
       0x45, 0x2, 0x2, 0x3c0, 0x3c1, 0x5, 0xa8, 0x55, 0x2, 0x3c1, 0x3c2, 
       0x7, 0x45, 0x2, 0x2, 0x3c2, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x3c3, 0x3c4, 
       0x7, 0x71, 0x2, 0x2, 0x3c4, 0x3c5, 0x7, 0x4e, 0x2, 0x2, 0x3c5, 0x3c7, 
       0x5, 0x8a, 0x46, 0x2, 0x3c6, 0x35e, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x35f, 
       0x3, 0x2, 0x2, 0x2, 0x3c6, 0x367, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x36e, 
       0x3, 0x2, 0x2, 0x2, 0x3c6, 0x374, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x378, 
       0x3, 0x2, 0x2, 0x2, 0x3c6, 0x37e, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x38b, 
       0x3, 0x2, 0x2, 0x2, 0x3c6, 0x397, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3a8, 
       0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3ac, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3b1, 
       0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3b5, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3ba, 
       0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3bf, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3c0, 
       0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3c3, 0x3, 0x2, 0x2, 0x2, 0x3c7, 0x8b, 
       0x3, 0x2, 0x2, 0x2, 0x3c8, 0x3c9, 0x7, 0x9, 0x2, 0x2, 0x3c9, 0x3cd, 
       0x7, 0x3f, 0x2, 0x2, 0x3ca, 0x3cc, 0x5, 0xe, 0x8, 0x2, 0x3cb, 0x3ca, 
       0x3, 0x2, 0x2, 0x2, 0x3cc, 0x3cf, 0x3, 0x2, 0x2, 0x2, 0x3cd, 0x3cb, 
       0x3, 0x2, 0x2, 0x2, 0x3cd, 0x3ce, 0x3, 0x2, 0x2, 0x2, 0x3ce, 0x3d0, 
       0x3, 0x2, 0x2, 0x2, 0x3cf, 0x3cd, 0x3, 0x2, 0x2, 0x2, 0x3d0, 0x3d1, 
       0x5, 0x8e, 0x48, 0x2, 0x3d1, 0x3d2, 0x7, 0x71, 0x2, 0x2, 0x3d2, 0x3d3, 
       0x7, 0x40, 0x2, 0x2, 0x3d3, 0x3d4, 0x5, 0x82, 0x42, 0x2, 0x3d4, 0x8d, 
       0x3, 0x2, 0x2, 0x2, 0x3d5, 0x3da, 0x5, 0x5e, 0x30, 0x2, 0x3d6, 0x3d7, 
       0x7, 0x5c, 0x2, 0x2, 0x3d7, 0x3d9, 0x5, 0x5e, 0x30, 0x2, 0x3d8, 0x3d6, 
       0x3, 0x2, 0x2, 0x2, 0x3d9, 0x3dc, 0x3, 0x2, 0x2, 0x2, 0x3da, 0x3d8, 
       0x3, 0x2, 0x2, 0x2, 0x3da, 0x3db, 0x3, 0x2, 0x2, 0x2, 0x3db, 0x8f, 
       0x3, 0x2, 0x2, 0x2, 0x3dc, 0x3da, 0x3, 0x2, 0x2, 0x2, 0x3dd, 0x3de, 
       0x7, 0x15, 0x2, 0x2, 0x3de, 0x3df, 0x5, 0x82, 0x42, 0x2, 0x3df, 0x91, 
       0x3, 0x2, 0x2, 0x2, 0x3e0, 0x3e1, 0x7, 0x3f, 0x2, 0x2, 0x3e1, 0x3e3, 
       0x5, 0x94, 0x4b, 0x2, 0x3e2, 0x3e4, 0x7, 0x45, 0x2, 0x2, 0x3e3, 0x3e2, 
       0x3, 0x2, 0x2, 0x2, 0x3e3, 0x3e4, 0x3, 0x2, 0x2, 0x2, 0x3e4, 0x3e5, 
       0x3, 0x2, 0x2, 0x2, 0x3e5, 0x3e6, 0x7, 0x40, 0x2, 0x2, 0x3e6, 0x93, 
       0x3, 0x2, 0x2, 0x2, 0x3e7, 0x3ec, 0x5, 0x96, 0x4c, 0x2, 0x3e8, 0x3e9, 
       0x7, 0x45, 0x2, 0x2, 0x3e9, 0x3eb, 0x5, 0x96, 0x4c, 0x2, 0x3ea, 0x3e8, 
       0x3, 0x2, 0x2, 0x2, 0x3eb, 0x3ee, 0x3, 0x2, 0x2, 0x2, 0x3ec, 0x3ea, 
       0x3, 0x2, 0x2, 0x2, 0x3ec, 0x3ed, 0x3, 0x2, 0x2, 0x2, 0x3ed, 0x95, 
       0x3, 0x2, 0x2, 0x2, 0x3ee, 0x3ec, 0x3, 0x2, 0x2, 0x2, 0x3ef, 0x3f1, 
       0x5, 0xe, 0x8, 0x2, 0x3f0, 0x3ef, 0x3, 0x2, 0x2, 0x2, 0x3f1, 0x3f4, 
       0x3, 0x2, 0x2, 0x2, 0x3f2, 0x3f0, 0x3, 0x2, 0x2, 0x2, 0x3f2, 0x3f3, 
       0x3, 0x2, 0x2, 0x2, 0x3f3, 0x3f5, 0x3, 0x2, 0x2, 0x2, 0x3f4, 0x3f2, 
       0x3, 0x2, 0x2, 0x2, 0x3f5, 0x3f6, 0x5, 0x50, 0x29, 0x2, 0x3f6, 0x3f7, 
       0x5, 0x4a, 0x26, 0x2, 0x3f7, 0x3f8, 0x7, 0x48, 0x2, 0x2, 0x3f8, 0x3f9, 
       0x5, 0xa8, 0x55, 0x2, 0x3f9, 0x97, 0x3, 0x2, 0x2, 0x2, 0x3fa, 0x3fc, 
       0x5, 0x9a, 0x4e, 0x2, 0x3fb, 0x3fa, 0x3, 0x2, 0x2, 0x2, 0x3fc, 0x3fd, 
       0x3, 0x2, 0x2, 0x2, 0x3fd, 0x3fb, 0x3, 0x2, 0x2, 0x2, 0x3fd, 0x3fe, 
       0x3, 0x2, 0x2, 0x2, 0x3fe, 0x400, 0x3, 0x2, 0x2, 0x2, 0x3ff, 0x401, 
       0x5, 0x84, 0x43, 0x2, 0x400, 0x3ff, 0x3, 0x2, 0x2, 0x2, 0x401, 0x402, 
       0x3, 0x2, 0x2, 0x2, 0x402, 0x400, 0x3, 0x2, 0x2, 0x2, 0x402, 0x403, 
       0x3, 0x2, 0x2, 0x2, 0x403, 0x99, 0x3, 0x2, 0x2, 0x2, 0x404, 0x407, 
       0x7, 0x8, 0x2, 0x2, 0x405, 0x408, 0x5, 0xa8, 0x55, 0x2, 0x406, 0x408, 
       0x7, 0x71, 0x2, 0x2, 0x407, 0x405, 0x3, 0x2, 0x2, 0x2, 0x407, 0x406, 
       0x3, 0x2, 0x2, 0x2, 0x408, 0x409, 0x3, 0x2, 0x2, 0x2, 0x409, 0x40d, 
       0x7, 0x4e, 0x2, 0x2, 0x40a, 0x40b, 0x7, 0xe, 0x2, 0x2, 0x40b, 0x40d, 
       0x7, 0x4e, 0x2, 0x2, 0x40c, 0x404, 0x3, 0x2, 0x2, 0x2, 0x40c, 0x40a, 
       0x3, 0x2, 0x2, 0x2, 0x40d, 0x9b, 0x3, 0x2, 0x2, 0x2, 0x40e, 0x41b, 
       0x5, 0xa0, 0x51, 0x2, 0x40f, 0x411, 0x5, 0x9e, 0x50, 0x2, 0x410, 
       0x40f, 0x3, 0x2, 0x2, 0x2, 0x410, 0x411, 0x3, 0x2, 0x2, 0x2, 0x411, 
       0x412, 0x3, 0x2, 0x2, 0x2, 0x412, 0x414, 0x7, 0x45, 0x2, 0x2, 0x413, 
       0x415, 0x5, 0xa8, 0x55, 0x2, 0x414, 0x413, 0x3, 0x2, 0x2, 0x2, 0x414, 
       0x415, 0x3, 0x2, 0x2, 0x2, 0x415, 0x416, 0x3, 0x2, 0x2, 0x2, 0x416, 
       0x418, 0x7, 0x45, 0x2, 0x2, 0x417, 0x419, 0x5, 0xa4, 0x53, 0x2, 0x418, 
       0x417, 0x3, 0x2, 0x2, 0x2, 0x418, 0x419, 0x3, 0x2, 0x2, 0x2, 0x419, 
       0x41b, 0x3, 0x2, 0x2, 0x2, 0x41a, 0x40e, 0x3, 0x2, 0x2, 0x2, 0x41a, 
       0x410, 0x3, 0x2, 0x2, 0x2, 0x41b, 0x9d, 0x3, 0x2, 0x2, 0x2, 0x41c, 
       0x41f, 0x5, 0x86, 0x44, 0x2, 0x41d, 0x41f, 0x5, 0xa4, 0x53, 0x2, 
       0x41e, 0x41c, 0x3, 0x2, 0x2, 0x2, 0x41e, 0x41d, 0x3, 0x2, 0x2, 0x2, 
       0x41f, 0x9f, 0x3, 0x2, 0x2, 0x2, 0x420, 0x422, 0x5, 0xe, 0x8, 0x2, 
       0x421, 0x420, 0x3, 0x2, 0x2, 0x2, 0x422, 0x425, 0x3, 0x2, 0x2, 0x2, 
       0x423, 0x421, 0x3, 0x2, 0x2, 0x2, 0x423, 0x424, 0x3, 0x2, 0x2, 0x2, 
       0x424, 0x426, 0x3, 0x2, 0x2, 0x2, 0x425, 0x423, 0x3, 0x2, 0x2, 0x2, 
       0x426, 0x427, 0x5, 0xc8, 0x65, 0x2, 0x427, 0x428, 0x5, 0x4a, 0x26, 
       0x2, 0x428, 0x429, 0x7, 0x4e, 0x2, 0x2, 0x429, 0x42a, 0x5, 0xa8, 
       0x55, 0x2, 0x42a, 0xa1, 0x3, 0x2, 0x2, 0x2, 0x42b, 0x42c, 0x7, 0x3f, 
       0x2, 0x2, 0x42c, 0x42d, 0x5, 0xa8, 0x55, 0x2, 0x42d, 0x42e, 0x7, 
       0x40, 0x2, 0x2, 0x42e, 0xa3, 0x3, 0x2, 0x2, 0x2, 0x42f, 0x434, 0x5, 
       0xa8, 0x55, 0x2, 0x430, 0x431, 0x7, 0x46, 0x2, 0x2, 0x431, 0x433, 
       0x5, 0xa8, 0x55, 0x2, 0x432, 0x430, 0x3, 0x2, 0x2, 0x2, 0x433, 0x436, 
       0x3, 0x2, 0x2, 0x2, 0x434, 0x432, 0x3, 0x2, 0x2, 0x2, 0x434, 0x435, 
       0x3, 0x2, 0x2, 0x2, 0x435, 0xa5, 0x3, 0x2, 0x2, 0x2, 0x436, 0x434, 
       0x3, 0x2, 0x2, 0x2, 0x437, 0x438, 0x7, 0x71, 0x2, 0x2, 0x438, 0x43a, 
       0x7, 0x3f, 0x2, 0x2, 0x439, 0x43b, 0x5, 0xa4, 0x53, 0x2, 0x43a, 0x439, 
       0x3, 0x2, 0x2, 0x2, 0x43a, 0x43b, 0x3, 0x2, 0x2, 0x2, 0x43b, 0x43c, 
       0x3, 0x2, 0x2, 0x2, 0x43c, 0x44a, 0x7, 0x40, 0x2, 0x2, 0x43d, 0x43e, 
       0x7, 0x2d, 0x2, 0x2, 0x43e, 0x440, 0x7, 0x3f, 0x2, 0x2, 0x43f, 0x441, 
       0x5, 0xa4, 0x53, 0x2, 0x440, 0x43f, 0x3, 0x2, 0x2, 0x2, 0x440, 0x441, 
       0x3, 0x2, 0x2, 0x2, 0x441, 0x442, 0x3, 0x2, 0x2, 0x2, 0x442, 0x44a, 
       0x7, 0x40, 0x2, 0x2, 0x443, 0x444, 0x7, 0x2a, 0x2, 0x2, 0x444, 0x446, 
       0x7, 0x3f, 0x2, 0x2, 0x445, 0x447, 0x5, 0xa4, 0x53, 0x2, 0x446, 0x445, 
       0x3, 0x2, 0x2, 0x2, 0x446, 0x447, 0x3, 0x2, 0x2, 0x2, 0x447, 0x448, 
       0x3, 0x2, 0x2, 0x2, 0x448, 0x44a, 0x7, 0x40, 0x2, 0x2, 0x449, 0x437, 
       0x3, 0x2, 0x2, 0x2, 0x449, 0x43d, 0x3, 0x2, 0x2, 0x2, 0x449, 0x443, 
       0x3, 0x2, 0x2, 0x2, 0x44a, 0xa7, 0x3, 0x2, 0x2, 0x2, 0x44b, 0x44c, 
       0x8, 0x55, 0x1, 0x2, 0x44c, 0x471, 0x5, 0xb0, 0x59, 0x2, 0x44d, 0x471, 
       0x5, 0xa6, 0x54, 0x2, 0x44e, 0x44f, 0x7, 0x21, 0x2, 0x2, 0x44f, 0x471, 
       0x5, 0xb4, 0x5b, 0x2, 0x450, 0x454, 0x7, 0x3f, 0x2, 0x2, 0x451, 0x453, 
       0x5, 0x68, 0x35, 0x2, 0x452, 0x451, 0x3, 0x2, 0x2, 0x2, 0x453, 0x456, 
       0x3, 0x2, 0x2, 0x2, 0x454, 0x452, 0x3, 0x2, 0x2, 0x2, 0x454, 0x455, 
       0x3, 0x2, 0x2, 0x2, 0x455, 0x457, 0x3, 0x2, 0x2, 0x2, 0x456, 0x454, 
       0x3, 0x2, 0x2, 0x2, 0x457, 0x458, 0x5, 0xc8, 0x65, 0x2, 0x458, 0x459, 
       0x7, 0x40, 0x2, 0x2, 0x459, 0x45a, 0x5, 0xa8, 0x55, 0x17, 0x45a, 
       0x471, 0x3, 0x2, 0x2, 0x2, 0x45b, 0x45c, 0x9, 0x5, 0x2, 0x2, 0x45c, 
       0x471, 0x5, 0xa8, 0x55, 0x15, 0x45d, 0x45e, 0x9, 0x6, 0x2, 0x2, 0x45e, 
       0x471, 0x5, 0xa8, 0x55, 0x14, 0x45f, 0x471, 0x5, 0xaa, 0x56, 0x2, 
       0x460, 0x461, 0x5, 0xc8, 0x65, 0x2, 0x461, 0x467, 0x7, 0x6b, 0x2, 
       0x2, 0x462, 0x464, 0x5, 0xcc, 0x67, 0x2, 0x463, 0x462, 0x3, 0x2, 
       0x2, 0x2, 0x463, 0x464, 0x3, 0x2, 0x2, 0x2, 0x464, 0x465, 0x3, 0x2, 
       0x2, 0x2, 0x465, 0x468, 0x7, 0x71, 0x2, 0x2, 0x466, 0x468, 0x7, 0x21, 
       0x2, 0x2, 0x467, 0x463, 0x3, 0x2, 0x2, 0x2, 0x467, 0x466, 0x3, 0x2, 
       0x2, 0x2, 0x468, 0x471, 0x3, 0x2, 0x2, 0x2, 0x469, 0x46a, 0x5, 0xb2, 
       0x5a, 0x2, 0x46a, 0x46c, 0x7, 0x6b, 0x2, 0x2, 0x46b, 0x46d, 0x5, 
       0xcc, 0x67, 0x2, 0x46c, 0x46b, 0x3, 0x2, 0x2, 0x2, 0x46c, 0x46d, 
       0x3, 0x2, 0x2, 0x2, 0x46d, 0x46e, 0x3, 0x2, 0x2, 0x2, 0x46e, 0x46f, 
       0x7, 0x21, 0x2, 0x2, 0x46f, 0x471, 0x3, 0x2, 0x2, 0x2, 0x470, 0x44b, 
       0x3, 0x2, 0x2, 0x2, 0x470, 0x44d, 0x3, 0x2, 0x2, 0x2, 0x470, 0x44e, 
       0x3, 0x2, 0x2, 0x2, 0x470, 0x450, 0x3, 0x2, 0x2, 0x2, 0x470, 0x45b, 
       0x3, 0x2, 0x2, 0x2, 0x470, 0x45d, 0x3, 0x2, 0x2, 0x2, 0x470, 0x45f, 
       0x3, 0x2, 0x2, 0x2, 0x470, 0x460, 0x3, 0x2, 0x2, 0x2, 0x470, 0x469, 
       0x3, 0x2, 0x2, 0x2, 0x471, 0x4c2, 0x3, 0x2, 0x2, 0x2, 0x472, 0x473, 
       0xc, 0x13, 0x2, 0x2, 0x473, 0x474, 0x9, 0x7, 0x2, 0x2, 0x474, 0x4c1, 
       0x5, 0xa8, 0x55, 0x14, 0x475, 0x476, 0xc, 0x12, 0x2, 0x2, 0x476, 
       0x477, 0x9, 0x8, 0x2, 0x2, 0x477, 0x4c1, 0x5, 0xa8, 0x55, 0x13, 0x478, 
       0x480, 0xc, 0x11, 0x2, 0x2, 0x479, 0x47a, 0x7, 0x4a, 0x2, 0x2, 0x47a, 
       0x481, 0x7, 0x4a, 0x2, 0x2, 0x47b, 0x47c, 0x7, 0x49, 0x2, 0x2, 0x47c, 
       0x47d, 0x7, 0x49, 0x2, 0x2, 0x47d, 0x481, 0x7, 0x49, 0x2, 0x2, 0x47e, 
       0x47f, 0x7, 0x49, 0x2, 0x2, 0x47f, 0x481, 0x7, 0x49, 0x2, 0x2, 0x480, 
       0x479, 0x3, 0x2, 0x2, 0x2, 0x480, 0x47b, 0x3, 0x2, 0x2, 0x2, 0x480, 
       0x47e, 0x3, 0x2, 0x2, 0x2, 0x481, 0x482, 0x3, 0x2, 0x2, 0x2, 0x482, 
       0x4c1, 0x5, 0xa8, 0x55, 0x12, 0x483, 0x484, 0xc, 0x10, 0x2, 0x2, 
       0x484, 0x485, 0x9, 0x9, 0x2, 0x2, 0x485, 0x4c1, 0x5, 0xa8, 0x55, 
       0x11, 0x486, 0x487, 0xc, 0xe, 0x2, 0x2, 0x487, 0x488, 0x9, 0xa, 0x2, 
       0x2, 0x488, 0x4c1, 0x5, 0xa8, 0x55, 0xf, 0x489, 0x48a, 0xc, 0xd, 
       0x2, 0x2, 0x48a, 0x48b, 0x7, 0x5b, 0x2, 0x2, 0x48b, 0x4c1, 0x5, 0xa8, 
       0x55, 0xe, 0x48c, 0x48d, 0xc, 0xc, 0x2, 0x2, 0x48d, 0x48e, 0x7, 0x5d, 
       0x2, 0x2, 0x48e, 0x4c1, 0x5, 0xa8, 0x55, 0xd, 0x48f, 0x490, 0xc, 
       0xb, 0x2, 0x2, 0x490, 0x491, 0x7, 0x5c, 0x2, 0x2, 0x491, 0x4c1, 0x5, 
       0xa8, 0x55, 0xc, 0x492, 0x493, 0xc, 0xa, 0x2, 0x2, 0x493, 0x494, 
       0x7, 0x53, 0x2, 0x2, 0x494, 0x4c1, 0x5, 0xa8, 0x55, 0xb, 0x495, 0x496, 
       0xc, 0x9, 0x2, 0x2, 0x496, 0x497, 0x7, 0x54, 0x2, 0x2, 0x497, 0x4c1, 
       0x5, 0xa8, 0x55, 0xa, 0x498, 0x499, 0xc, 0x8, 0x2, 0x2, 0x499, 0x49a, 
       0x7, 0x4d, 0x2, 0x2, 0x49a, 0x49b, 0x5, 0xa8, 0x55, 0x2, 0x49b, 0x49c, 
       0x7, 0x4e, 0x2, 0x2, 0x49c, 0x49d, 0x5, 0xa8, 0x55, 0x8, 0x49d, 0x4c1, 
       0x3, 0x2, 0x2, 0x2, 0x49e, 0x49f, 0xc, 0x7, 0x2, 0x2, 0x49f, 0x4a0, 
       0x9, 0xb, 0x2, 0x2, 0x4a0, 0x4c1, 0x5, 0xa8, 0x55, 0x7, 0x4a1, 0x4a2, 
       0xc, 0x1b, 0x2, 0x2, 0x4a2, 0x4ae, 0x7, 0x47, 0x2, 0x2, 0x4a3, 0x4af, 
       0x7, 0x71, 0x2, 0x2, 0x4a4, 0x4af, 0x5, 0xa6, 0x54, 0x2, 0x4a5, 0x4af, 
       0x7, 0x2d, 0x2, 0x2, 0x4a6, 0x4a8, 0x7, 0x21, 0x2, 0x2, 0x4a7, 0x4a9, 
       0x5, 0xc4, 0x63, 0x2, 0x4a8, 0x4a7, 0x3, 0x2, 0x2, 0x2, 0x4a8, 0x4a9, 
       0x3, 0x2, 0x2, 0x2, 0x4a9, 0x4aa, 0x3, 0x2, 0x2, 0x2, 0x4aa, 0x4af, 
       0x5, 0xb8, 0x5d, 0x2, 0x4ab, 0x4ac, 0x7, 0x2a, 0x2, 0x2, 0x4ac, 0x4af, 
       0x5, 0xce, 0x68, 0x2, 0x4ad, 0x4af, 0x5, 0xbe, 0x60, 0x2, 0x4ae, 
       0x4a3, 0x3, 0x2, 0x2, 0x2, 0x4ae, 0x4a4, 0x3, 0x2, 0x2, 0x2, 0x4ae, 
       0x4a5, 0x3, 0x2, 0x2, 0x2, 0x4ae, 0x4a6, 0x3, 0x2, 0x2, 0x2, 0x4ae, 
       0x4ab, 0x3, 0x2, 0x2, 0x2, 0x4ae, 0x4ad, 0x3, 0x2, 0x2, 0x2, 0x4af, 
       0x4c1, 0x3, 0x2, 0x2, 0x2, 0x4b0, 0x4b1, 0xc, 0x1a, 0x2, 0x2, 0x4b1, 
       0x4b2, 0x7, 0x43, 0x2, 0x2, 0x4b2, 0x4b3, 0x5, 0xa8, 0x55, 0x2, 0x4b3, 
       0x4b4, 0x7, 0x44, 0x2, 0x2, 0x4b4, 0x4c1, 0x3, 0x2, 0x2, 0x2, 0x4b5, 
       0x4b6, 0xc, 0x16, 0x2, 0x2, 0x4b6, 0x4c1, 0x9, 0xc, 0x2, 0x2, 0x4b7, 
       0x4b8, 0xc, 0xf, 0x2, 0x2, 0x4b8, 0x4b9, 0x7, 0x1c, 0x2, 0x2, 0x4b9, 
       0x4c1, 0x5, 0xc8, 0x65, 0x2, 0x4ba, 0x4bb, 0xc, 0x5, 0x2, 0x2, 0x4bb, 
       0x4bd, 0x7, 0x6b, 0x2, 0x2, 0x4bc, 0x4be, 0x5, 0xcc, 0x67, 0x2, 0x4bd, 
       0x4bc, 0x3, 0x2, 0x2, 0x2, 0x4bd, 0x4be, 0x3, 0x2, 0x2, 0x2, 0x4be, 
       0x4bf, 0x3, 0x2, 0x2, 0x2, 0x4bf, 0x4c1, 0x7, 0x71, 0x2, 0x2, 0x4c0, 
       0x472, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x475, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
       0x478, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x483, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
       0x486, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x489, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
       0x48c, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x48f, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
       0x492, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x495, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
       0x498, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x49e, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
       0x4a1, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x4b0, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
       0x4b5, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x4b7, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
       0x4ba, 0x3, 0x2, 0x2, 0x2, 0x4c1, 0x4c4, 0x3, 0x2, 0x2, 0x2, 0x4c2, 
       0x4c0, 0x3, 0x2, 0x2, 0x2, 0x4c2, 0x4c3, 0x3, 0x2, 0x2, 0x2, 0x4c3, 
       0xa9, 0x3, 0x2, 0x2, 0x2, 0x4c4, 0x4c2, 0x3, 0x2, 0x2, 0x2, 0x4c5, 
       0x4c6, 0x5, 0xac, 0x57, 0x2, 0x4c6, 0x4c7, 0x7, 0x6a, 0x2, 0x2, 0x4c7, 
       0x4c8, 0x5, 0xae, 0x58, 0x2, 0x4c8, 0xab, 0x3, 0x2, 0x2, 0x2, 0x4c9, 
       0x4da, 0x7, 0x71, 0x2, 0x2, 0x4ca, 0x4cc, 0x7, 0x3f, 0x2, 0x2, 0x4cb, 
       0x4cd, 0x5, 0x58, 0x2d, 0x2, 0x4cc, 0x4cb, 0x3, 0x2, 0x2, 0x2, 0x4cc, 
       0x4cd, 0x3, 0x2, 0x2, 0x2, 0x4cd, 0x4ce, 0x3, 0x2, 0x2, 0x2, 0x4ce, 
       0x4da, 0x7, 0x40, 0x2, 0x2, 0x4cf, 0x4d0, 0x7, 0x3f, 0x2, 0x2, 0x4d0, 
       0x4d5, 0x7, 0x71, 0x2, 0x2, 0x4d1, 0x4d2, 0x7, 0x46, 0x2, 0x2, 0x4d2, 
       0x4d4, 0x7, 0x71, 0x2, 0x2, 0x4d3, 0x4d1, 0x3, 0x2, 0x2, 0x2, 0x4d4, 
       0x4d7, 0x3, 0x2, 0x2, 0x2, 0x4d5, 0x4d3, 0x3, 0x2, 0x2, 0x2, 0x4d5, 
       0x4d6, 0x3, 0x2, 0x2, 0x2, 0x4d6, 0x4d8, 0x3, 0x2, 0x2, 0x2, 0x4d7, 
       0x4d5, 0x3, 0x2, 0x2, 0x2, 0x4d8, 0x4da, 0x7, 0x40, 0x2, 0x2, 0x4d9, 
       0x4c9, 0x3, 0x2, 0x2, 0x2, 0x4d9, 0x4ca, 0x3, 0x2, 0x2, 0x2, 0x4d9, 
       0x4cf, 0x3, 0x2, 0x2, 0x2, 0x4da, 0xad, 0x3, 0x2, 0x2, 0x2, 0x4db, 
       0x4de, 0x5, 0xa8, 0x55, 0x2, 0x4dc, 0x4de, 0x5, 0x82, 0x42, 0x2, 
       0x4dd, 0x4db, 0x3, 0x2, 0x2, 0x2, 0x4dd, 0x4dc, 0x3, 0x2, 0x2, 0x2, 
       0x4de, 0xaf, 0x3, 0x2, 0x2, 0x2, 0x4df, 0x4e0, 0x7, 0x3f, 0x2, 0x2, 
       0x4e0, 0x4e1, 0x5, 0xa8, 0x55, 0x2, 0x4e1, 0x4e2, 0x7, 0x40, 0x2, 
       0x2, 0x4e2, 0x4f2, 0x3, 0x2, 0x2, 0x2, 0x4e3, 0x4f2, 0x7, 0x2d, 0x2, 
       0x2, 0x4e4, 0x4f2, 0x7, 0x2a, 0x2, 0x2, 0x4e5, 0x4f2, 0x5, 0x60, 
       0x31, 0x2, 0x4e6, 0x4f2, 0x7, 0x71, 0x2, 0x2, 0x4e7, 0x4e8, 0x5, 
       0x2e, 0x18, 0x2, 0x4e8, 0x4e9, 0x7, 0x47, 0x2, 0x2, 0x4e9, 0x4ea, 
       0x7, 0xb, 0x2, 0x2, 0x4ea, 0x4f2, 0x3, 0x2, 0x2, 0x2, 0x4eb, 0x4ef, 
       0x5, 0xc4, 0x63, 0x2, 0x4ec, 0x4f0, 0x5, 0xd0, 0x69, 0x2, 0x4ed, 
       0x4ee, 0x7, 0x2d, 0x2, 0x2, 0x4ee, 0x4f0, 0x5, 0xd2, 0x6a, 0x2, 0x4ef, 
       0x4ec, 0x3, 0x2, 0x2, 0x2, 0x4ef, 0x4ed, 0x3, 0x2, 0x2, 0x2, 0x4f0, 
       0x4f2, 0x3, 0x2, 0x2, 0x2, 0x4f1, 0x4df, 0x3, 0x2, 0x2, 0x2, 0x4f1, 
       0x4e3, 0x3, 0x2, 0x2, 0x2, 0x4f1, 0x4e4, 0x3, 0x2, 0x2, 0x2, 0x4f1, 
       0x4e5, 0x3, 0x2, 0x2, 0x2, 0x4f1, 0x4e6, 0x3, 0x2, 0x2, 0x2, 0x4f1, 
       0x4e7, 0x3, 0x2, 0x2, 0x2, 0x4f1, 0x4eb, 0x3, 0x2, 0x2, 0x2, 0x4f2, 
       0xb1, 0x3, 0x2, 0x2, 0x2, 0x4f3, 0x4f4, 0x5, 0x50, 0x29, 0x2, 0x4f4, 
       0x4f5, 0x7, 0x47, 0x2, 0x2, 0x4f5, 0x4f7, 0x3, 0x2, 0x2, 0x2, 0x4f6, 
       0x4f3, 0x3, 0x2, 0x2, 0x2, 0x4f6, 0x4f7, 0x3, 0x2, 0x2, 0x2, 0x4f7, 
       0x4fb, 0x3, 0x2, 0x2, 0x2, 0x4f8, 0x4fa, 0x5, 0x68, 0x35, 0x2, 0x4f9, 
       0x4f8, 0x3, 0x2, 0x2, 0x2, 0x4fa, 0x4fd, 0x3, 0x2, 0x2, 0x2, 0x4fb, 
       0x4f9, 0x3, 0x2, 0x2, 0x2, 0x4fb, 0x4fc, 0x3, 0x2, 0x2, 0x2, 0x4fc, 
       0x4fe, 0x3, 0x2, 0x2, 0x2, 0x4fd, 0x4fb, 0x3, 0x2, 0x2, 0x2, 0x4fe, 
       0x500, 0x7, 0x71, 0x2, 0x2, 0x4ff, 0x501, 0x5, 0xcc, 0x67, 0x2, 0x500, 
       0x4ff, 0x3, 0x2, 0x2, 0x2, 0x500, 0x501, 0x3, 0x2, 0x2, 0x2, 0x501, 
       0xb3, 0x3, 0x2, 0x2, 0x2, 0x502, 0x503, 0x5, 0xc4, 0x63, 0x2, 0x503, 
       0x504, 0x5, 0xb6, 0x5c, 0x2, 0x504, 0x505, 0x5, 0xbc, 0x5f, 0x2, 
       0x505, 0x50c, 0x3, 0x2, 0x2, 0x2, 0x506, 0x509, 0x5, 0xb6, 0x5c, 
       0x2, 0x507, 0x50a, 0x5, 0xba, 0x5e, 0x2, 0x508, 0x50a, 0x5, 0xbc, 
       0x5f, 0x2, 0x509, 0x507, 0x3, 0x2, 0x2, 0x2, 0x509, 0x508, 0x3, 0x2, 
       0x2, 0x2, 0x50a, 0x50c, 0x3, 0x2, 0x2, 0x2, 0x50b, 0x502, 0x3, 0x2, 
       0x2, 0x2, 0x50b, 0x506, 0x3, 0x2, 0x2, 0x2, 0x50c, 0xb5, 0x3, 0x2, 
       0x2, 0x2, 0x50d, 0x50f, 0x7, 0x71, 0x2, 0x2, 0x50e, 0x510, 0x5, 0xc0, 
       0x61, 0x2, 0x50f, 0x50e, 0x3, 0x2, 0x2, 0x2, 0x50f, 0x510, 0x3, 0x2, 
       0x2, 0x2, 0x510, 0x518, 0x3, 0x2, 0x2, 0x2, 0x511, 0x512, 0x7, 0x47, 
       0x2, 0x2, 0x512, 0x514, 0x7, 0x71, 0x2, 0x2, 0x513, 0x515, 0x5, 0xc0, 
       0x61, 0x2, 0x514, 0x513, 0x3, 0x2, 0x2, 0x2, 0x514, 0x515, 0x3, 0x2, 
       0x2, 0x2, 0x515, 0x517, 0x3, 0x2, 0x2, 0x2, 0x516, 0x511, 0x3, 0x2, 
       0x2, 0x2, 0x517, 0x51a, 0x3, 0x2, 0x2, 0x2, 0x518, 0x516, 0x3, 0x2, 
       0x2, 0x2, 0x518, 0x519, 0x3, 0x2, 0x2, 0x2, 0x519, 0x51d, 0x3, 0x2, 
       0x2, 0x2, 0x51a, 0x518, 0x3, 0x2, 0x2, 0x2, 0x51b, 0x51d, 0x5, 0xca, 
       0x66, 0x2, 0x51c, 0x50d, 0x3, 0x2, 0x2, 0x2, 0x51c, 0x51b, 0x3, 0x2, 
       0x2, 0x2, 0x51d, 0xb7, 0x3, 0x2, 0x2, 0x2, 0x51e, 0x520, 0x7, 0x71, 
       0x2, 0x2, 0x51f, 0x521, 0x5, 0xc2, 0x62, 0x2, 0x520, 0x51f, 0x3, 
       0x2, 0x2, 0x2, 0x520, 0x521, 0x3, 0x2, 0x2, 0x2, 0x521, 0x522, 0x3, 
       0x2, 0x2, 0x2, 0x522, 0x523, 0x5, 0xbc, 0x5f, 0x2, 0x523, 0xb9, 0x3, 
       0x2, 0x2, 0x2, 0x524, 0x540, 0x7, 0x43, 0x2, 0x2, 0x525, 0x52a, 0x7, 
       0x44, 0x2, 0x2, 0x526, 0x527, 0x7, 0x43, 0x2, 0x2, 0x527, 0x529, 
       0x7, 0x44, 0x2, 0x2, 0x528, 0x526, 0x3, 0x2, 0x2, 0x2, 0x529, 0x52c, 
       0x3, 0x2, 0x2, 0x2, 0x52a, 0x528, 0x3, 0x2, 0x2, 0x2, 0x52a, 0x52b, 
       0x3, 0x2, 0x2, 0x2, 0x52b, 0x52d, 0x3, 0x2, 0x2, 0x2, 0x52c, 0x52a, 
       0x3, 0x2, 0x2, 0x2, 0x52d, 0x541, 0x5, 0x4e, 0x28, 0x2, 0x52e, 0x52f, 
       0x5, 0xa8, 0x55, 0x2, 0x52f, 0x536, 0x7, 0x44, 0x2, 0x2, 0x530, 0x531, 
       0x7, 0x43, 0x2, 0x2, 0x531, 0x532, 0x5, 0xa8, 0x55, 0x2, 0x532, 0x533, 
       0x7, 0x44, 0x2, 0x2, 0x533, 0x535, 0x3, 0x2, 0x2, 0x2, 0x534, 0x530, 
       0x3, 0x2, 0x2, 0x2, 0x535, 0x538, 0x3, 0x2, 0x2, 0x2, 0x536, 0x534, 
       0x3, 0x2, 0x2, 0x2, 0x536, 0x537, 0x3, 0x2, 0x2, 0x2, 0x537, 0x53d, 
       0x3, 0x2, 0x2, 0x2, 0x538, 0x536, 0x3, 0x2, 0x2, 0x2, 0x539, 0x53a, 
       0x7, 0x43, 0x2, 0x2, 0x53a, 0x53c, 0x7, 0x44, 0x2, 0x2, 0x53b, 0x539, 
       0x3, 0x2, 0x2, 0x2, 0x53c, 0x53f, 0x3, 0x2, 0x2, 0x2, 0x53d, 0x53b, 
       0x3, 0x2, 0x2, 0x2, 0x53d, 0x53e, 0x3, 0x2, 0x2, 0x2, 0x53e, 0x541, 
       0x3, 0x2, 0x2, 0x2, 0x53f, 0x53d, 0x3, 0x2, 0x2, 0x2, 0x540, 0x525, 
       0x3, 0x2, 0x2, 0x2, 0x540, 0x52e, 0x3, 0x2, 0x2, 0x2, 0x541, 0xbb, 
       0x3, 0x2, 0x2, 0x2, 0x542, 0x544, 0x5, 0xd2, 0x6a, 0x2, 0x543, 0x545, 
       0x5, 0x22, 0x12, 0x2, 0x544, 0x543, 0x3, 0x2, 0x2, 0x2, 0x544, 0x545, 
       0x3, 0x2, 0x2, 0x2, 0x545, 0xbd, 0x3, 0x2, 0x2, 0x2, 0x546, 0x547, 
       0x5, 0xc4, 0x63, 0x2, 0x547, 0x548, 0x5, 0xd0, 0x69, 0x2, 0x548, 
       0xbf, 0x3, 0x2, 0x2, 0x2, 0x549, 0x54a, 0x7, 0x4a, 0x2, 0x2, 0x54a, 
       0x54d, 0x7, 0x49, 0x2, 0x2, 0x54b, 0x54d, 0x5, 0xcc, 0x67, 0x2, 0x54c, 
       0x549, 0x3, 0x2, 0x2, 0x2, 0x54c, 0x54b, 0x3, 0x2, 0x2, 0x2, 0x54d, 
       0xc1, 0x3, 0x2, 0x2, 0x2, 0x54e, 0x54f, 0x7, 0x4a, 0x2, 0x2, 0x54f, 
       0x552, 0x7, 0x49, 0x2, 0x2, 0x550, 0x552, 0x5, 0xc4, 0x63, 0x2, 0x551, 
       0x54e, 0x3, 0x2, 0x2, 0x2, 0x551, 0x550, 0x3, 0x2, 0x2, 0x2, 0x552, 
       0xc3, 0x3, 0x2, 0x2, 0x2, 0x553, 0x554, 0x7, 0x4a, 0x2, 0x2, 0x554, 
       0x555, 0x5, 0xc6, 0x64, 0x2, 0x555, 0x556, 0x7, 0x49, 0x2, 0x2, 0x556, 
       0xc5, 0x3, 0x2, 0x2, 0x2, 0x557, 0x55c, 0x5, 0xc8, 0x65, 0x2, 0x558, 
       0x559, 0x7, 0x46, 0x2, 0x2, 0x559, 0x55b, 0x5, 0xc8, 0x65, 0x2, 0x55a, 
       0x558, 0x3, 0x2, 0x2, 0x2, 0x55b, 0x55e, 0x3, 0x2, 0x2, 0x2, 0x55c, 
       0x55a, 0x3, 0x2, 0x2, 0x2, 0x55c, 0x55d, 0x3, 0x2, 0x2, 0x2, 0x55d, 
       0xc7, 0x3, 0x2, 0x2, 0x2, 0x55e, 0x55c, 0x3, 0x2, 0x2, 0x2, 0x55f, 
       0x561, 0x5, 0x68, 0x35, 0x2, 0x560, 0x55f, 0x3, 0x2, 0x2, 0x2, 0x561, 
       0x564, 0x3, 0x2, 0x2, 0x2, 0x562, 0x560, 0x3, 0x2, 0x2, 0x2, 0x562, 
       0x563, 0x3, 0x2, 0x2, 0x2, 0x563, 0x567, 0x3, 0x2, 0x2, 0x2, 0x564, 
       0x562, 0x3, 0x2, 0x2, 0x2, 0x565, 0x568, 0x5, 0x50, 0x29, 0x2, 0x566, 
       0x568, 0x5, 0xca, 0x66, 0x2, 0x567, 0x565, 0x3, 0x2, 0x2, 0x2, 0x567, 
       0x566, 0x3, 0x2, 0x2, 0x2, 0x568, 0x573, 0x3, 0x2, 0x2, 0x2, 0x569, 
       0x56b, 0x5, 0x68, 0x35, 0x2, 0x56a, 0x569, 0x3, 0x2, 0x2, 0x2, 0x56b, 
       0x56e, 0x3, 0x2, 0x2, 0x2, 0x56c, 0x56a, 0x3, 0x2, 0x2, 0x2, 0x56c, 
       0x56d, 0x3, 0x2, 0x2, 0x2, 0x56d, 0x56f, 0x3, 0x2, 0x2, 0x2, 0x56e, 
       0x56c, 0x3, 0x2, 0x2, 0x2, 0x56f, 0x570, 0x7, 0x43, 0x2, 0x2, 0x570, 
       0x572, 0x7, 0x44, 0x2, 0x2, 0x571, 0x56c, 0x3, 0x2, 0x2, 0x2, 0x572, 
       0x575, 0x3, 0x2, 0x2, 0x2, 0x573, 0x571, 0x3, 0x2, 0x2, 0x2, 0x573, 
       0x574, 0x3, 0x2, 0x2, 0x2, 0x574, 0xc9, 0x3, 0x2, 0x2, 0x2, 0x575, 
       0x573, 0x3, 0x2, 0x2, 0x2, 0x576, 0x577, 0x9, 0xd, 0x2, 0x2, 0x577, 
       0xcb, 0x3, 0x2, 0x2, 0x2, 0x578, 0x579, 0x7, 0x4a, 0x2, 0x2, 0x579, 
       0x57e, 0x5, 0x52, 0x2a, 0x2, 0x57a, 0x57b, 0x7, 0x46, 0x2, 0x2, 0x57b, 
       0x57d, 0x5, 0x52, 0x2a, 0x2, 0x57c, 0x57a, 0x3, 0x2, 0x2, 0x2, 0x57d, 
       0x580, 0x3, 0x2, 0x2, 0x2, 0x57e, 0x57c, 0x3, 0x2, 0x2, 0x2, 0x57e, 
       0x57f, 0x3, 0x2, 0x2, 0x2, 0x57f, 0x581, 0x3, 0x2, 0x2, 0x2, 0x580, 
       0x57e, 0x3, 0x2, 0x2, 0x2, 0x581, 0x582, 0x7, 0x49, 0x2, 0x2, 0x582, 
       0xcd, 0x3, 0x2, 0x2, 0x2, 0x583, 0x58a, 0x5, 0xd2, 0x6a, 0x2, 0x584, 
       0x585, 0x7, 0x47, 0x2, 0x2, 0x585, 0x587, 0x7, 0x71, 0x2, 0x2, 0x586, 
       0x588, 0x5, 0xd2, 0x6a, 0x2, 0x587, 0x586, 0x3, 0x2, 0x2, 0x2, 0x587, 
       0x588, 0x3, 0x2, 0x2, 0x2, 0x588, 0x58a, 0x3, 0x2, 0x2, 0x2, 0x589, 
       0x583, 0x3, 0x2, 0x2, 0x2, 0x589, 0x584, 0x3, 0x2, 0x2, 0x2, 0x58a, 
       0xcf, 0x3, 0x2, 0x2, 0x2, 0x58b, 0x58c, 0x7, 0x2a, 0x2, 0x2, 0x58c, 
       0x590, 0x5, 0xce, 0x68, 0x2, 0x58d, 0x58e, 0x7, 0x71, 0x2, 0x2, 0x58e, 
       0x590, 0x5, 0xd2, 0x6a, 0x2, 0x58f, 0x58b, 0x3, 0x2, 0x2, 0x2, 0x58f, 
       0x58d, 0x3, 0x2, 0x2, 0x2, 0x590, 0xd1, 0x3, 0x2, 0x2, 0x2, 0x591, 
       0x593, 0x7, 0x3f, 0x2, 0x2, 0x592, 0x594, 0x5, 0xa4, 0x53, 0x2, 0x593, 
       0x592, 0x3, 0x2, 0x2, 0x2, 0x593, 0x594, 0x3, 0x2, 0x2, 0x2, 0x594, 
       0x595, 0x3, 0x2, 0x2, 0x2, 0x595, 0x596, 0x7, 0x40, 0x2, 0x2, 0x596, 
       0xd3, 0x3, 0x2, 0x2, 0x2, 0xb4, 0xd5, 0xda, 0xe0, 0xe8, 0xf1, 0xf6, 
       0xfd, 0x104, 0x107, 0x10e, 0x118, 0x11c, 0x121, 0x125, 0x129, 0x133, 
       0x13b, 0x143, 0x147, 0x14e, 0x155, 0x159, 0x15c, 0x15f, 0x168, 0x16e, 
       0x173, 0x176, 0x17c, 0x182, 0x186, 0x18e, 0x197, 0x19e, 0x1a4, 0x1a8, 
       0x1b3, 0x1bc, 0x1c1, 0x1c7, 0x1cb, 0x1d7, 0x1e2, 0x1e7, 0x1f0, 0x1f8, 
       0x202, 0x20b, 0x213, 0x218, 0x220, 0x225, 0x22f, 0x239, 0x23f, 0x246, 
       0x24b, 0x253, 0x257, 0x259, 0x25f, 0x264, 0x268, 0x26f, 0x275, 0x277, 
       0x27e, 0x283, 0x28c, 0x291, 0x294, 0x299, 0x2a2, 0x2a9, 0x2b4, 0x2bd, 
       0x2c7, 0x2d0, 0x2d5, 0x2d8, 0x2df, 0x2e9, 0x2f1, 0x2f4, 0x2f7, 0x304, 
       0x30c, 0x311, 0x319, 0x31d, 0x321, 0x325, 0x327, 0x32b, 0x331, 0x33c, 
       0x346, 0x34b, 0x354, 0x359, 0x35c, 0x363, 0x36c, 0x383, 0x386, 0x389, 
       0x391, 0x395, 0x39d, 0x3a3, 0x3ae, 0x3b7, 0x3bc, 0x3c6, 0x3cd, 0x3da, 
       0x3e3, 0x3ec, 0x3f2, 0x3fd, 0x402, 0x407, 0x40c, 0x410, 0x414, 0x418, 
       0x41a, 0x41e, 0x423, 0x434, 0x43a, 0x440, 0x446, 0x449, 0x454, 0x463, 
       0x467, 0x46c, 0x470, 0x480, 0x4a8, 0x4ae, 0x4bd, 0x4c0, 0x4c2, 0x4cc, 
       0x4d5, 0x4d9, 0x4dd, 0x4ef, 0x4f1, 0x4f6, 0x4fb, 0x500, 0x509, 0x50b, 
       0x50f, 0x514, 0x518, 0x51c, 0x520, 0x52a, 0x536, 0x53d, 0x540, 0x544, 
       0x54c, 0x551, 0x55c, 0x562, 0x567, 0x56c, 0x573, 0x57e, 0x587, 0x589, 
       0x58f, 0x593, 
  };

  _serializedATN.insert(_serializedATN.end(), serializedATNSegment0,
    serializedATNSegment0 + sizeof(serializedATNSegment0) / sizeof(serializedATNSegment0[0]));


  atn::ATNDeserializer deserializer;
  _atn = deserializer.deserialize(_serializedATN);

  size_t count = _atn.getNumberOfDecisions();
  _decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    _decisionToDFA.emplace_back(_atn.getDecisionState(i), i);
  }
}

JavaLabeledParser::Initializer JavaLabeledParser::_init;
