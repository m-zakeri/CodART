
// Generated from D:/AnacondaProjects/CodART/grammars\JavaParserLabeled.g4 by ANTLR 4.9.1


#include "JavaParserLabeledListener.h"
#include "JavaParserLabeledVisitor.h"

#include "JavaParserLabeled.h"


using namespace antlrcpp;
using namespace antlr4;

JavaParserLabeled::JavaParserLabeled(TokenStream *input) : Parser(input) {
  _interpreter = new atn::ParserATNSimulator(this, _atn, _decisionToDFA, _sharedContextCache);
}

JavaParserLabeled::~JavaParserLabeled() {
  delete _interpreter;
}

std::string JavaParserLabeled::getGrammarFileName() const {
  return "JavaParserLabeled.g4";
}

const std::vector<std::string>& JavaParserLabeled::getRuleNames() const {
  return _ruleNames;
}

dfa::Vocabulary& JavaParserLabeled::getVocabulary() const {
  return _vocabulary;
}


//----------------- CompilationUnitContext ------------------------------------------------------------------

JavaParserLabeled::CompilationUnitContext::CompilationUnitContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::CompilationUnitContext::EOF() {
  return getToken(JavaParserLabeled::EOF, 0);
}

JavaParserLabeled::PackageDeclarationContext* JavaParserLabeled::CompilationUnitContext::packageDeclaration() {
  return getRuleContext<JavaParserLabeled::PackageDeclarationContext>(0);
}

std::vector<JavaParserLabeled::ImportDeclarationContext *> JavaParserLabeled::CompilationUnitContext::importDeclaration() {
  return getRuleContexts<JavaParserLabeled::ImportDeclarationContext>();
}

JavaParserLabeled::ImportDeclarationContext* JavaParserLabeled::CompilationUnitContext::importDeclaration(size_t i) {
  return getRuleContext<JavaParserLabeled::ImportDeclarationContext>(i);
}

std::vector<JavaParserLabeled::TypeDeclarationContext *> JavaParserLabeled::CompilationUnitContext::typeDeclaration() {
  return getRuleContexts<JavaParserLabeled::TypeDeclarationContext>();
}

JavaParserLabeled::TypeDeclarationContext* JavaParserLabeled::CompilationUnitContext::typeDeclaration(size_t i) {
  return getRuleContext<JavaParserLabeled::TypeDeclarationContext>(i);
}


size_t JavaParserLabeled::CompilationUnitContext::getRuleIndex() const {
  return JavaParserLabeled::RuleCompilationUnit;
}

void JavaParserLabeled::CompilationUnitContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCompilationUnit(this);
}

void JavaParserLabeled::CompilationUnitContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCompilationUnit(this);
}


antlrcpp::Any JavaParserLabeled::CompilationUnitContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitCompilationUnit(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::CompilationUnitContext* JavaParserLabeled::compilationUnit() {
  CompilationUnitContext *_localctx = _tracker.createInstance<CompilationUnitContext>(_ctx, getState());
  enterRule(_localctx, 0, JavaParserLabeled::RuleCompilationUnit);
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
    while (_la == JavaParserLabeled::IMPORT) {
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
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::ABSTRACT)
      | (1ULL << JavaParserLabeled::CLASS)
      | (1ULL << JavaParserLabeled::ENUM)
      | (1ULL << JavaParserLabeled::FINAL)
      | (1ULL << JavaParserLabeled::INTERFACE)
      | (1ULL << JavaParserLabeled::PRIVATE)
      | (1ULL << JavaParserLabeled::PROTECTED)
      | (1ULL << JavaParserLabeled::PUBLIC)
      | (1ULL << JavaParserLabeled::STATIC)
      | (1ULL << JavaParserLabeled::STRICTFP))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaParserLabeled::SEMI - 67))
      | (1ULL << (JavaParserLabeled::AT - 67))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 67)))) != 0)) {
      setState(219);
      typeDeclaration();
      setState(224);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(225);
    match(JavaParserLabeled::EOF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PackageDeclarationContext ------------------------------------------------------------------

JavaParserLabeled::PackageDeclarationContext::PackageDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::PackageDeclarationContext::PACKAGE() {
  return getToken(JavaParserLabeled::PACKAGE, 0);
}

JavaParserLabeled::QualifiedNameContext* JavaParserLabeled::PackageDeclarationContext::qualifiedName() {
  return getRuleContext<JavaParserLabeled::QualifiedNameContext>(0);
}

tree::TerminalNode* JavaParserLabeled::PackageDeclarationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::PackageDeclarationContext::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::PackageDeclarationContext::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}


size_t JavaParserLabeled::PackageDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RulePackageDeclaration;
}

void JavaParserLabeled::PackageDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPackageDeclaration(this);
}

void JavaParserLabeled::PackageDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPackageDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::PackageDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPackageDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::PackageDeclarationContext* JavaParserLabeled::packageDeclaration() {
  PackageDeclarationContext *_localctx = _tracker.createInstance<PackageDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 2, JavaParserLabeled::RulePackageDeclaration);
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
    while (_la == JavaParserLabeled::AT

    || _la == JavaParserLabeled::IDENTIFIER) {
      setState(227);
      annotation();
      setState(232);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(233);
    match(JavaParserLabeled::PACKAGE);
    setState(234);
    qualifiedName();
    setState(235);
    match(JavaParserLabeled::SEMI);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ImportDeclarationContext ------------------------------------------------------------------

JavaParserLabeled::ImportDeclarationContext::ImportDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ImportDeclarationContext::IMPORT() {
  return getToken(JavaParserLabeled::IMPORT, 0);
}

JavaParserLabeled::QualifiedNameContext* JavaParserLabeled::ImportDeclarationContext::qualifiedName() {
  return getRuleContext<JavaParserLabeled::QualifiedNameContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ImportDeclarationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

tree::TerminalNode* JavaParserLabeled::ImportDeclarationContext::STATIC() {
  return getToken(JavaParserLabeled::STATIC, 0);
}

tree::TerminalNode* JavaParserLabeled::ImportDeclarationContext::DOT() {
  return getToken(JavaParserLabeled::DOT, 0);
}

tree::TerminalNode* JavaParserLabeled::ImportDeclarationContext::MUL() {
  return getToken(JavaParserLabeled::MUL, 0);
}


size_t JavaParserLabeled::ImportDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleImportDeclaration;
}

void JavaParserLabeled::ImportDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterImportDeclaration(this);
}

void JavaParserLabeled::ImportDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitImportDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::ImportDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitImportDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ImportDeclarationContext* JavaParserLabeled::importDeclaration() {
  ImportDeclarationContext *_localctx = _tracker.createInstance<ImportDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 4, JavaParserLabeled::RuleImportDeclaration);
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
    match(JavaParserLabeled::IMPORT);
    setState(239);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::STATIC) {
      setState(238);
      match(JavaParserLabeled::STATIC);
    }
    setState(241);
    qualifiedName();
    setState(244);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::DOT) {
      setState(242);
      match(JavaParserLabeled::DOT);
      setState(243);
      match(JavaParserLabeled::MUL);
    }
    setState(246);
    match(JavaParserLabeled::SEMI);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeDeclarationContext ------------------------------------------------------------------

JavaParserLabeled::TypeDeclarationContext::TypeDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::ClassDeclarationContext* JavaParserLabeled::TypeDeclarationContext::classDeclaration() {
  return getRuleContext<JavaParserLabeled::ClassDeclarationContext>(0);
}

JavaParserLabeled::EnumDeclarationContext* JavaParserLabeled::TypeDeclarationContext::enumDeclaration() {
  return getRuleContext<JavaParserLabeled::EnumDeclarationContext>(0);
}

JavaParserLabeled::InterfaceDeclarationContext* JavaParserLabeled::TypeDeclarationContext::interfaceDeclaration() {
  return getRuleContext<JavaParserLabeled::InterfaceDeclarationContext>(0);
}

JavaParserLabeled::AnnotationTypeDeclarationContext* JavaParserLabeled::TypeDeclarationContext::annotationTypeDeclaration() {
  return getRuleContext<JavaParserLabeled::AnnotationTypeDeclarationContext>(0);
}

std::vector<JavaParserLabeled::ClassOrInterfaceModifierContext *> JavaParserLabeled::TypeDeclarationContext::classOrInterfaceModifier() {
  return getRuleContexts<JavaParserLabeled::ClassOrInterfaceModifierContext>();
}

JavaParserLabeled::ClassOrInterfaceModifierContext* JavaParserLabeled::TypeDeclarationContext::classOrInterfaceModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::ClassOrInterfaceModifierContext>(i);
}

tree::TerminalNode* JavaParserLabeled::TypeDeclarationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}


size_t JavaParserLabeled::TypeDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeDeclaration;
}

void JavaParserLabeled::TypeDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeDeclaration(this);
}

void JavaParserLabeled::TypeDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::TypeDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeDeclarationContext* JavaParserLabeled::typeDeclaration() {
  TypeDeclarationContext *_localctx = _tracker.createInstance<TypeDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 6, JavaParserLabeled::RuleTypeDeclaration);

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
      case JavaParserLabeled::ABSTRACT:
      case JavaParserLabeled::CLASS:
      case JavaParserLabeled::ENUM:
      case JavaParserLabeled::FINAL:
      case JavaParserLabeled::INTERFACE:
      case JavaParserLabeled::PRIVATE:
      case JavaParserLabeled::PROTECTED:
      case JavaParserLabeled::PUBLIC:
      case JavaParserLabeled::STATIC:
      case JavaParserLabeled::STRICTFP:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
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
          case JavaParserLabeled::CLASS: {
            setState(254);
            classDeclaration();
            break;
          }

          case JavaParserLabeled::ENUM: {
            setState(255);
            enumDeclaration();
            break;
          }

          case JavaParserLabeled::INTERFACE: {
            setState(256);
            interfaceDeclaration();
            break;
          }

          case JavaParserLabeled::AT: {
            setState(257);
            annotationTypeDeclaration();
            break;
          }

        default:
          throw NoViableAltException(this);
        }
        break;
      }

      case JavaParserLabeled::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(260);
        match(JavaParserLabeled::SEMI);
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

JavaParserLabeled::ModifierContext::ModifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::ClassOrInterfaceModifierContext* JavaParserLabeled::ModifierContext::classOrInterfaceModifier() {
  return getRuleContext<JavaParserLabeled::ClassOrInterfaceModifierContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ModifierContext::NATIVE() {
  return getToken(JavaParserLabeled::NATIVE, 0);
}

tree::TerminalNode* JavaParserLabeled::ModifierContext::SYNCHRONIZED() {
  return getToken(JavaParserLabeled::SYNCHRONIZED, 0);
}

tree::TerminalNode* JavaParserLabeled::ModifierContext::TRANSIENT() {
  return getToken(JavaParserLabeled::TRANSIENT, 0);
}

tree::TerminalNode* JavaParserLabeled::ModifierContext::VOLATILE() {
  return getToken(JavaParserLabeled::VOLATILE, 0);
}


size_t JavaParserLabeled::ModifierContext::getRuleIndex() const {
  return JavaParserLabeled::RuleModifier;
}

void JavaParserLabeled::ModifierContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterModifier(this);
}

void JavaParserLabeled::ModifierContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitModifier(this);
}


antlrcpp::Any JavaParserLabeled::ModifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitModifier(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ModifierContext* JavaParserLabeled::modifier() {
  ModifierContext *_localctx = _tracker.createInstance<ModifierContext>(_ctx, getState());
  enterRule(_localctx, 8, JavaParserLabeled::RuleModifier);

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
      case JavaParserLabeled::ABSTRACT:
      case JavaParserLabeled::FINAL:
      case JavaParserLabeled::PRIVATE:
      case JavaParserLabeled::PROTECTED:
      case JavaParserLabeled::PUBLIC:
      case JavaParserLabeled::STATIC:
      case JavaParserLabeled::STRICTFP:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(263);
        classOrInterfaceModifier();
        break;
      }

      case JavaParserLabeled::NATIVE: {
        enterOuterAlt(_localctx, 2);
        setState(264);
        match(JavaParserLabeled::NATIVE);
        break;
      }

      case JavaParserLabeled::SYNCHRONIZED: {
        enterOuterAlt(_localctx, 3);
        setState(265);
        match(JavaParserLabeled::SYNCHRONIZED);
        break;
      }

      case JavaParserLabeled::TRANSIENT: {
        enterOuterAlt(_localctx, 4);
        setState(266);
        match(JavaParserLabeled::TRANSIENT);
        break;
      }

      case JavaParserLabeled::VOLATILE: {
        enterOuterAlt(_localctx, 5);
        setState(267);
        match(JavaParserLabeled::VOLATILE);
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

JavaParserLabeled::ClassOrInterfaceModifierContext::ClassOrInterfaceModifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::ClassOrInterfaceModifierContext::annotation() {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceModifierContext::PUBLIC() {
  return getToken(JavaParserLabeled::PUBLIC, 0);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceModifierContext::PROTECTED() {
  return getToken(JavaParserLabeled::PROTECTED, 0);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceModifierContext::PRIVATE() {
  return getToken(JavaParserLabeled::PRIVATE, 0);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceModifierContext::STATIC() {
  return getToken(JavaParserLabeled::STATIC, 0);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceModifierContext::ABSTRACT() {
  return getToken(JavaParserLabeled::ABSTRACT, 0);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceModifierContext::FINAL() {
  return getToken(JavaParserLabeled::FINAL, 0);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceModifierContext::STRICTFP() {
  return getToken(JavaParserLabeled::STRICTFP, 0);
}


size_t JavaParserLabeled::ClassOrInterfaceModifierContext::getRuleIndex() const {
  return JavaParserLabeled::RuleClassOrInterfaceModifier;
}

void JavaParserLabeled::ClassOrInterfaceModifierContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassOrInterfaceModifier(this);
}

void JavaParserLabeled::ClassOrInterfaceModifierContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassOrInterfaceModifier(this);
}


antlrcpp::Any JavaParserLabeled::ClassOrInterfaceModifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassOrInterfaceModifier(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ClassOrInterfaceModifierContext* JavaParserLabeled::classOrInterfaceModifier() {
  ClassOrInterfaceModifierContext *_localctx = _tracker.createInstance<ClassOrInterfaceModifierContext>(_ctx, getState());
  enterRule(_localctx, 10, JavaParserLabeled::RuleClassOrInterfaceModifier);

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
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(270);
        annotation();
        break;
      }

      case JavaParserLabeled::PUBLIC: {
        enterOuterAlt(_localctx, 2);
        setState(271);
        match(JavaParserLabeled::PUBLIC);
        break;
      }

      case JavaParserLabeled::PROTECTED: {
        enterOuterAlt(_localctx, 3);
        setState(272);
        match(JavaParserLabeled::PROTECTED);
        break;
      }

      case JavaParserLabeled::PRIVATE: {
        enterOuterAlt(_localctx, 4);
        setState(273);
        match(JavaParserLabeled::PRIVATE);
        break;
      }

      case JavaParserLabeled::STATIC: {
        enterOuterAlt(_localctx, 5);
        setState(274);
        match(JavaParserLabeled::STATIC);
        break;
      }

      case JavaParserLabeled::ABSTRACT: {
        enterOuterAlt(_localctx, 6);
        setState(275);
        match(JavaParserLabeled::ABSTRACT);
        break;
      }

      case JavaParserLabeled::FINAL: {
        enterOuterAlt(_localctx, 7);
        setState(276);
        match(JavaParserLabeled::FINAL);
        break;
      }

      case JavaParserLabeled::STRICTFP: {
        enterOuterAlt(_localctx, 8);
        setState(277);
        match(JavaParserLabeled::STRICTFP);
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

JavaParserLabeled::VariableModifierContext::VariableModifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::VariableModifierContext::FINAL() {
  return getToken(JavaParserLabeled::FINAL, 0);
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::VariableModifierContext::annotation() {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(0);
}


size_t JavaParserLabeled::VariableModifierContext::getRuleIndex() const {
  return JavaParserLabeled::RuleVariableModifier;
}

void JavaParserLabeled::VariableModifierContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableModifier(this);
}

void JavaParserLabeled::VariableModifierContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableModifier(this);
}


antlrcpp::Any JavaParserLabeled::VariableModifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitVariableModifier(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::VariableModifierContext* JavaParserLabeled::variableModifier() {
  VariableModifierContext *_localctx = _tracker.createInstance<VariableModifierContext>(_ctx, getState());
  enterRule(_localctx, 12, JavaParserLabeled::RuleVariableModifier);

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
      case JavaParserLabeled::FINAL: {
        enterOuterAlt(_localctx, 1);
        setState(280);
        match(JavaParserLabeled::FINAL);
        break;
      }

      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
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

JavaParserLabeled::ClassDeclarationContext::ClassDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ClassDeclarationContext::CLASS() {
  return getToken(JavaParserLabeled::CLASS, 0);
}

tree::TerminalNode* JavaParserLabeled::ClassDeclarationContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::ClassBodyContext* JavaParserLabeled::ClassDeclarationContext::classBody() {
  return getRuleContext<JavaParserLabeled::ClassBodyContext>(0);
}

JavaParserLabeled::TypeParametersContext* JavaParserLabeled::ClassDeclarationContext::typeParameters() {
  return getRuleContext<JavaParserLabeled::TypeParametersContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ClassDeclarationContext::EXTENDS() {
  return getToken(JavaParserLabeled::EXTENDS, 0);
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::ClassDeclarationContext::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ClassDeclarationContext::IMPLEMENTS() {
  return getToken(JavaParserLabeled::IMPLEMENTS, 0);
}

JavaParserLabeled::TypeListContext* JavaParserLabeled::ClassDeclarationContext::typeList() {
  return getRuleContext<JavaParserLabeled::TypeListContext>(0);
}


size_t JavaParserLabeled::ClassDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleClassDeclaration;
}

void JavaParserLabeled::ClassDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassDeclaration(this);
}

void JavaParserLabeled::ClassDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::ClassDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ClassDeclarationContext* JavaParserLabeled::classDeclaration() {
  ClassDeclarationContext *_localctx = _tracker.createInstance<ClassDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 14, JavaParserLabeled::RuleClassDeclaration);
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
    match(JavaParserLabeled::CLASS);
    setState(285);
    match(JavaParserLabeled::IDENTIFIER);
    setState(287);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::LT) {
      setState(286);
      typeParameters();
    }
    setState(291);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::EXTENDS) {
      setState(289);
      match(JavaParserLabeled::EXTENDS);
      setState(290);
      typeType();
    }
    setState(295);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::IMPLEMENTS) {
      setState(293);
      match(JavaParserLabeled::IMPLEMENTS);
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

JavaParserLabeled::TypeParametersContext::TypeParametersContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::TypeParametersContext::LT() {
  return getToken(JavaParserLabeled::LT, 0);
}

std::vector<JavaParserLabeled::TypeParameterContext *> JavaParserLabeled::TypeParametersContext::typeParameter() {
  return getRuleContexts<JavaParserLabeled::TypeParameterContext>();
}

JavaParserLabeled::TypeParameterContext* JavaParserLabeled::TypeParametersContext::typeParameter(size_t i) {
  return getRuleContext<JavaParserLabeled::TypeParameterContext>(i);
}

tree::TerminalNode* JavaParserLabeled::TypeParametersContext::GT() {
  return getToken(JavaParserLabeled::GT, 0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::TypeParametersContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::TypeParametersContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::TypeParametersContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeParameters;
}

void JavaParserLabeled::TypeParametersContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeParameters(this);
}

void JavaParserLabeled::TypeParametersContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeParameters(this);
}


antlrcpp::Any JavaParserLabeled::TypeParametersContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeParameters(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeParametersContext* JavaParserLabeled::typeParameters() {
  TypeParametersContext *_localctx = _tracker.createInstance<TypeParametersContext>(_ctx, getState());
  enterRule(_localctx, 16, JavaParserLabeled::RuleTypeParameters);
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
    match(JavaParserLabeled::LT);
    setState(300);
    typeParameter();
    setState(305);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaParserLabeled::COMMA) {
      setState(301);
      match(JavaParserLabeled::COMMA);
      setState(302);
      typeParameter();
      setState(307);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(308);
    match(JavaParserLabeled::GT);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeParameterContext ------------------------------------------------------------------

JavaParserLabeled::TypeParameterContext::TypeParameterContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::TypeParameterContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::TypeParameterContext::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::TypeParameterContext::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}

tree::TerminalNode* JavaParserLabeled::TypeParameterContext::EXTENDS() {
  return getToken(JavaParserLabeled::EXTENDS, 0);
}

JavaParserLabeled::TypeBoundContext* JavaParserLabeled::TypeParameterContext::typeBound() {
  return getRuleContext<JavaParserLabeled::TypeBoundContext>(0);
}


size_t JavaParserLabeled::TypeParameterContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeParameter;
}

void JavaParserLabeled::TypeParameterContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeParameter(this);
}

void JavaParserLabeled::TypeParameterContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeParameter(this);
}


antlrcpp::Any JavaParserLabeled::TypeParameterContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeParameter(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeParameterContext* JavaParserLabeled::typeParameter() {
  TypeParameterContext *_localctx = _tracker.createInstance<TypeParameterContext>(_ctx, getState());
  enterRule(_localctx, 18, JavaParserLabeled::RuleTypeParameter);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(325);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::EXTENDS) {
      setState(317);
      match(JavaParserLabeled::EXTENDS);
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

JavaParserLabeled::TypeBoundContext::TypeBoundContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::TypeTypeContext *> JavaParserLabeled::TypeBoundContext::typeType() {
  return getRuleContexts<JavaParserLabeled::TypeTypeContext>();
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::TypeBoundContext::typeType(size_t i) {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::TypeBoundContext::BITAND() {
  return getTokens(JavaParserLabeled::BITAND);
}

tree::TerminalNode* JavaParserLabeled::TypeBoundContext::BITAND(size_t i) {
  return getToken(JavaParserLabeled::BITAND, i);
}


size_t JavaParserLabeled::TypeBoundContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeBound;
}

void JavaParserLabeled::TypeBoundContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeBound(this);
}

void JavaParserLabeled::TypeBoundContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeBound(this);
}


antlrcpp::Any JavaParserLabeled::TypeBoundContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeBound(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeBoundContext* JavaParserLabeled::typeBound() {
  TypeBoundContext *_localctx = _tracker.createInstance<TypeBoundContext>(_ctx, getState());
  enterRule(_localctx, 20, JavaParserLabeled::RuleTypeBound);
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
    while (_la == JavaParserLabeled::BITAND) {
      setState(328);
      match(JavaParserLabeled::BITAND);
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

JavaParserLabeled::EnumDeclarationContext::EnumDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::EnumDeclarationContext::ENUM() {
  return getToken(JavaParserLabeled::ENUM, 0);
}

tree::TerminalNode* JavaParserLabeled::EnumDeclarationContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

tree::TerminalNode* JavaParserLabeled::EnumDeclarationContext::LBRACE() {
  return getToken(JavaParserLabeled::LBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::EnumDeclarationContext::RBRACE() {
  return getToken(JavaParserLabeled::RBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::EnumDeclarationContext::IMPLEMENTS() {
  return getToken(JavaParserLabeled::IMPLEMENTS, 0);
}

JavaParserLabeled::TypeListContext* JavaParserLabeled::EnumDeclarationContext::typeList() {
  return getRuleContext<JavaParserLabeled::TypeListContext>(0);
}

JavaParserLabeled::EnumConstantsContext* JavaParserLabeled::EnumDeclarationContext::enumConstants() {
  return getRuleContext<JavaParserLabeled::EnumConstantsContext>(0);
}

tree::TerminalNode* JavaParserLabeled::EnumDeclarationContext::COMMA() {
  return getToken(JavaParserLabeled::COMMA, 0);
}

JavaParserLabeled::EnumBodyDeclarationsContext* JavaParserLabeled::EnumDeclarationContext::enumBodyDeclarations() {
  return getRuleContext<JavaParserLabeled::EnumBodyDeclarationsContext>(0);
}


size_t JavaParserLabeled::EnumDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleEnumDeclaration;
}

void JavaParserLabeled::EnumDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnumDeclaration(this);
}

void JavaParserLabeled::EnumDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnumDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::EnumDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitEnumDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::EnumDeclarationContext* JavaParserLabeled::enumDeclaration() {
  EnumDeclarationContext *_localctx = _tracker.createInstance<EnumDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 22, JavaParserLabeled::RuleEnumDeclaration);
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
    match(JavaParserLabeled::ENUM);
    setState(336);
    match(JavaParserLabeled::IDENTIFIER);
    setState(339);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::IMPLEMENTS) {
      setState(337);
      match(JavaParserLabeled::IMPLEMENTS);
      setState(338);
      typeList();
    }
    setState(341);
    match(JavaParserLabeled::LBRACE);
    setState(343);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::AT

    || _la == JavaParserLabeled::IDENTIFIER) {
      setState(342);
      enumConstants();
    }
    setState(346);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::COMMA) {
      setState(345);
      match(JavaParserLabeled::COMMA);
    }
    setState(349);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::SEMI) {
      setState(348);
      enumBodyDeclarations();
    }
    setState(351);
    match(JavaParserLabeled::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- EnumConstantsContext ------------------------------------------------------------------

JavaParserLabeled::EnumConstantsContext::EnumConstantsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::EnumConstantContext *> JavaParserLabeled::EnumConstantsContext::enumConstant() {
  return getRuleContexts<JavaParserLabeled::EnumConstantContext>();
}

JavaParserLabeled::EnumConstantContext* JavaParserLabeled::EnumConstantsContext::enumConstant(size_t i) {
  return getRuleContext<JavaParserLabeled::EnumConstantContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::EnumConstantsContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::EnumConstantsContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::EnumConstantsContext::getRuleIndex() const {
  return JavaParserLabeled::RuleEnumConstants;
}

void JavaParserLabeled::EnumConstantsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnumConstants(this);
}

void JavaParserLabeled::EnumConstantsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnumConstants(this);
}


antlrcpp::Any JavaParserLabeled::EnumConstantsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitEnumConstants(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::EnumConstantsContext* JavaParserLabeled::enumConstants() {
  EnumConstantsContext *_localctx = _tracker.createInstance<EnumConstantsContext>(_ctx, getState());
  enterRule(_localctx, 24, JavaParserLabeled::RuleEnumConstants);

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
        match(JavaParserLabeled::COMMA);
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

JavaParserLabeled::EnumConstantContext::EnumConstantContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::EnumConstantContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::EnumConstantContext::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::EnumConstantContext::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}

JavaParserLabeled::ArgumentsContext* JavaParserLabeled::EnumConstantContext::arguments() {
  return getRuleContext<JavaParserLabeled::ArgumentsContext>(0);
}

JavaParserLabeled::ClassBodyContext* JavaParserLabeled::EnumConstantContext::classBody() {
  return getRuleContext<JavaParserLabeled::ClassBodyContext>(0);
}


size_t JavaParserLabeled::EnumConstantContext::getRuleIndex() const {
  return JavaParserLabeled::RuleEnumConstant;
}

void JavaParserLabeled::EnumConstantContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnumConstant(this);
}

void JavaParserLabeled::EnumConstantContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnumConstant(this);
}


antlrcpp::Any JavaParserLabeled::EnumConstantContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitEnumConstant(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::EnumConstantContext* JavaParserLabeled::enumConstant() {
  EnumConstantContext *_localctx = _tracker.createInstance<EnumConstantContext>(_ctx, getState());
  enterRule(_localctx, 26, JavaParserLabeled::RuleEnumConstant);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(369);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::LPAREN) {
      setState(368);
      arguments();
    }
    setState(372);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::LBRACE) {
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

JavaParserLabeled::EnumBodyDeclarationsContext::EnumBodyDeclarationsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::EnumBodyDeclarationsContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

std::vector<JavaParserLabeled::ClassBodyDeclarationContext *> JavaParserLabeled::EnumBodyDeclarationsContext::classBodyDeclaration() {
  return getRuleContexts<JavaParserLabeled::ClassBodyDeclarationContext>();
}

JavaParserLabeled::ClassBodyDeclarationContext* JavaParserLabeled::EnumBodyDeclarationsContext::classBodyDeclaration(size_t i) {
  return getRuleContext<JavaParserLabeled::ClassBodyDeclarationContext>(i);
}


size_t JavaParserLabeled::EnumBodyDeclarationsContext::getRuleIndex() const {
  return JavaParserLabeled::RuleEnumBodyDeclarations;
}

void JavaParserLabeled::EnumBodyDeclarationsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnumBodyDeclarations(this);
}

void JavaParserLabeled::EnumBodyDeclarationsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnumBodyDeclarations(this);
}


antlrcpp::Any JavaParserLabeled::EnumBodyDeclarationsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitEnumBodyDeclarations(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::EnumBodyDeclarationsContext* JavaParserLabeled::enumBodyDeclarations() {
  EnumBodyDeclarationsContext *_localctx = _tracker.createInstance<EnumBodyDeclarationsContext>(_ctx, getState());
  enterRule(_localctx, 28, JavaParserLabeled::RuleEnumBodyDeclarations);
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
    match(JavaParserLabeled::SEMI);
    setState(378);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::ABSTRACT)
      | (1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::CLASS)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::ENUM)
      | (1ULL << JavaParserLabeled::FINAL)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::INTERFACE)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NATIVE)
      | (1ULL << JavaParserLabeled::PRIVATE)
      | (1ULL << JavaParserLabeled::PROTECTED)
      | (1ULL << JavaParserLabeled::PUBLIC)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::STATIC)
      | (1ULL << JavaParserLabeled::STRICTFP)
      | (1ULL << JavaParserLabeled::SYNCHRONIZED)
      | (1ULL << JavaParserLabeled::TRANSIENT)
      | (1ULL << JavaParserLabeled::VOID)
      | (1ULL << JavaParserLabeled::VOLATILE)
      | (1ULL << JavaParserLabeled::LBRACE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaParserLabeled::SEMI - 67))
      | (1ULL << (JavaParserLabeled::LT - 67))
      | (1ULL << (JavaParserLabeled::AT - 67))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 67)))) != 0)) {
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

JavaParserLabeled::InterfaceDeclarationContext::InterfaceDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::InterfaceDeclarationContext::INTERFACE() {
  return getToken(JavaParserLabeled::INTERFACE, 0);
}

tree::TerminalNode* JavaParserLabeled::InterfaceDeclarationContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::InterfaceBodyContext* JavaParserLabeled::InterfaceDeclarationContext::interfaceBody() {
  return getRuleContext<JavaParserLabeled::InterfaceBodyContext>(0);
}

JavaParserLabeled::TypeParametersContext* JavaParserLabeled::InterfaceDeclarationContext::typeParameters() {
  return getRuleContext<JavaParserLabeled::TypeParametersContext>(0);
}

tree::TerminalNode* JavaParserLabeled::InterfaceDeclarationContext::EXTENDS() {
  return getToken(JavaParserLabeled::EXTENDS, 0);
}

JavaParserLabeled::TypeListContext* JavaParserLabeled::InterfaceDeclarationContext::typeList() {
  return getRuleContext<JavaParserLabeled::TypeListContext>(0);
}


size_t JavaParserLabeled::InterfaceDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleInterfaceDeclaration;
}

void JavaParserLabeled::InterfaceDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceDeclaration(this);
}

void JavaParserLabeled::InterfaceDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::InterfaceDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::InterfaceDeclarationContext* JavaParserLabeled::interfaceDeclaration() {
  InterfaceDeclarationContext *_localctx = _tracker.createInstance<InterfaceDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 30, JavaParserLabeled::RuleInterfaceDeclaration);
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
    match(JavaParserLabeled::INTERFACE);
    setState(382);
    match(JavaParserLabeled::IDENTIFIER);
    setState(384);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::LT) {
      setState(383);
      typeParameters();
    }
    setState(388);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::EXTENDS) {
      setState(386);
      match(JavaParserLabeled::EXTENDS);
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

JavaParserLabeled::ClassBodyContext::ClassBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ClassBodyContext::LBRACE() {
  return getToken(JavaParserLabeled::LBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::ClassBodyContext::RBRACE() {
  return getToken(JavaParserLabeled::RBRACE, 0);
}

std::vector<JavaParserLabeled::ClassBodyDeclarationContext *> JavaParserLabeled::ClassBodyContext::classBodyDeclaration() {
  return getRuleContexts<JavaParserLabeled::ClassBodyDeclarationContext>();
}

JavaParserLabeled::ClassBodyDeclarationContext* JavaParserLabeled::ClassBodyContext::classBodyDeclaration(size_t i) {
  return getRuleContext<JavaParserLabeled::ClassBodyDeclarationContext>(i);
}


size_t JavaParserLabeled::ClassBodyContext::getRuleIndex() const {
  return JavaParserLabeled::RuleClassBody;
}

void JavaParserLabeled::ClassBodyContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassBody(this);
}

void JavaParserLabeled::ClassBodyContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassBody(this);
}


antlrcpp::Any JavaParserLabeled::ClassBodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassBody(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ClassBodyContext* JavaParserLabeled::classBody() {
  ClassBodyContext *_localctx = _tracker.createInstance<ClassBodyContext>(_ctx, getState());
  enterRule(_localctx, 32, JavaParserLabeled::RuleClassBody);
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
    match(JavaParserLabeled::LBRACE);
    setState(396);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::ABSTRACT)
      | (1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::CLASS)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::ENUM)
      | (1ULL << JavaParserLabeled::FINAL)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::INTERFACE)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NATIVE)
      | (1ULL << JavaParserLabeled::PRIVATE)
      | (1ULL << JavaParserLabeled::PROTECTED)
      | (1ULL << JavaParserLabeled::PUBLIC)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::STATIC)
      | (1ULL << JavaParserLabeled::STRICTFP)
      | (1ULL << JavaParserLabeled::SYNCHRONIZED)
      | (1ULL << JavaParserLabeled::TRANSIENT)
      | (1ULL << JavaParserLabeled::VOID)
      | (1ULL << JavaParserLabeled::VOLATILE)
      | (1ULL << JavaParserLabeled::LBRACE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaParserLabeled::SEMI - 67))
      | (1ULL << (JavaParserLabeled::LT - 67))
      | (1ULL << (JavaParserLabeled::AT - 67))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 67)))) != 0)) {
      setState(393);
      classBodyDeclaration();
      setState(398);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(399);
    match(JavaParserLabeled::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InterfaceBodyContext ------------------------------------------------------------------

JavaParserLabeled::InterfaceBodyContext::InterfaceBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::InterfaceBodyContext::LBRACE() {
  return getToken(JavaParserLabeled::LBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::InterfaceBodyContext::RBRACE() {
  return getToken(JavaParserLabeled::RBRACE, 0);
}

std::vector<JavaParserLabeled::InterfaceBodyDeclarationContext *> JavaParserLabeled::InterfaceBodyContext::interfaceBodyDeclaration() {
  return getRuleContexts<JavaParserLabeled::InterfaceBodyDeclarationContext>();
}

JavaParserLabeled::InterfaceBodyDeclarationContext* JavaParserLabeled::InterfaceBodyContext::interfaceBodyDeclaration(size_t i) {
  return getRuleContext<JavaParserLabeled::InterfaceBodyDeclarationContext>(i);
}


size_t JavaParserLabeled::InterfaceBodyContext::getRuleIndex() const {
  return JavaParserLabeled::RuleInterfaceBody;
}

void JavaParserLabeled::InterfaceBodyContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceBody(this);
}

void JavaParserLabeled::InterfaceBodyContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceBody(this);
}


antlrcpp::Any JavaParserLabeled::InterfaceBodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceBody(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::InterfaceBodyContext* JavaParserLabeled::interfaceBody() {
  InterfaceBodyContext *_localctx = _tracker.createInstance<InterfaceBodyContext>(_ctx, getState());
  enterRule(_localctx, 34, JavaParserLabeled::RuleInterfaceBody);
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
    match(JavaParserLabeled::LBRACE);
    setState(405);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::ABSTRACT)
      | (1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::CLASS)
      | (1ULL << JavaParserLabeled::DEFAULT)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::ENUM)
      | (1ULL << JavaParserLabeled::FINAL)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::INTERFACE)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NATIVE)
      | (1ULL << JavaParserLabeled::PRIVATE)
      | (1ULL << JavaParserLabeled::PROTECTED)
      | (1ULL << JavaParserLabeled::PUBLIC)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::STATIC)
      | (1ULL << JavaParserLabeled::STRICTFP)
      | (1ULL << JavaParserLabeled::SYNCHRONIZED)
      | (1ULL << JavaParserLabeled::TRANSIENT)
      | (1ULL << JavaParserLabeled::VOID)
      | (1ULL << JavaParserLabeled::VOLATILE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaParserLabeled::SEMI - 67))
      | (1ULL << (JavaParserLabeled::LT - 67))
      | (1ULL << (JavaParserLabeled::AT - 67))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 67)))) != 0)) {
      setState(402);
      interfaceBodyDeclaration();
      setState(407);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(408);
    match(JavaParserLabeled::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassBodyDeclarationContext ------------------------------------------------------------------

JavaParserLabeled::ClassBodyDeclarationContext::ClassBodyDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::ClassBodyDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleClassBodyDeclaration;
}

void JavaParserLabeled::ClassBodyDeclarationContext::copyFrom(ClassBodyDeclarationContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ClassBodyDeclaration1Context ------------------------------------------------------------------

JavaParserLabeled::BlockContext* JavaParserLabeled::ClassBodyDeclaration1Context::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ClassBodyDeclaration1Context::STATIC() {
  return getToken(JavaParserLabeled::STATIC, 0);
}

JavaParserLabeled::ClassBodyDeclaration1Context::ClassBodyDeclaration1Context(ClassBodyDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ClassBodyDeclaration1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassBodyDeclaration1(this);
}
void JavaParserLabeled::ClassBodyDeclaration1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassBodyDeclaration1(this);
}

antlrcpp::Any JavaParserLabeled::ClassBodyDeclaration1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassBodyDeclaration1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ClassBodyDeclaration0Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::ClassBodyDeclaration0Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::ClassBodyDeclaration0Context::ClassBodyDeclaration0Context(ClassBodyDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ClassBodyDeclaration0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassBodyDeclaration0(this);
}
void JavaParserLabeled::ClassBodyDeclaration0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassBodyDeclaration0(this);
}

antlrcpp::Any JavaParserLabeled::ClassBodyDeclaration0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassBodyDeclaration0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ClassBodyDeclaration2Context ------------------------------------------------------------------

JavaParserLabeled::MemberDeclarationContext* JavaParserLabeled::ClassBodyDeclaration2Context::memberDeclaration() {
  return getRuleContext<JavaParserLabeled::MemberDeclarationContext>(0);
}

std::vector<JavaParserLabeled::ModifierContext *> JavaParserLabeled::ClassBodyDeclaration2Context::modifier() {
  return getRuleContexts<JavaParserLabeled::ModifierContext>();
}

JavaParserLabeled::ModifierContext* JavaParserLabeled::ClassBodyDeclaration2Context::modifier(size_t i) {
  return getRuleContext<JavaParserLabeled::ModifierContext>(i);
}

JavaParserLabeled::ClassBodyDeclaration2Context::ClassBodyDeclaration2Context(ClassBodyDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ClassBodyDeclaration2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassBodyDeclaration2(this);
}
void JavaParserLabeled::ClassBodyDeclaration2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassBodyDeclaration2(this);
}

antlrcpp::Any JavaParserLabeled::ClassBodyDeclaration2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassBodyDeclaration2(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::ClassBodyDeclarationContext* JavaParserLabeled::classBodyDeclaration() {
  ClassBodyDeclarationContext *_localctx = _tracker.createInstance<ClassBodyDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 36, JavaParserLabeled::RuleClassBodyDeclaration);
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
      _localctx = dynamic_cast<ClassBodyDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::ClassBodyDeclaration0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(410);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 2: {
      _localctx = dynamic_cast<ClassBodyDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::ClassBodyDeclaration1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(412);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaParserLabeled::STATIC) {
        setState(411);
        match(JavaParserLabeled::STATIC);
      }
      setState(414);
      block();
      break;
    }

    case 3: {
      _localctx = dynamic_cast<ClassBodyDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::ClassBodyDeclaration2Context>(_localctx));
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

JavaParserLabeled::MemberDeclarationContext::MemberDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::MemberDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleMemberDeclaration;
}

void JavaParserLabeled::MemberDeclarationContext::copyFrom(MemberDeclarationContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- MemberDeclaration8Context ------------------------------------------------------------------

JavaParserLabeled::EnumDeclarationContext* JavaParserLabeled::MemberDeclaration8Context::enumDeclaration() {
  return getRuleContext<JavaParserLabeled::EnumDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration8Context::MemberDeclaration8Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration8Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration8(this);
}
void JavaParserLabeled::MemberDeclaration8Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration8(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration8Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration8(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration0Context ------------------------------------------------------------------

JavaParserLabeled::MethodDeclarationContext* JavaParserLabeled::MemberDeclaration0Context::methodDeclaration() {
  return getRuleContext<JavaParserLabeled::MethodDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration0Context::MemberDeclaration0Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration0(this);
}
void JavaParserLabeled::MemberDeclaration0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration0(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration1Context ------------------------------------------------------------------

JavaParserLabeled::GenericMethodDeclarationContext* JavaParserLabeled::MemberDeclaration1Context::genericMethodDeclaration() {
  return getRuleContext<JavaParserLabeled::GenericMethodDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration1Context::MemberDeclaration1Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration1(this);
}
void JavaParserLabeled::MemberDeclaration1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration1(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration2Context ------------------------------------------------------------------

JavaParserLabeled::FieldDeclarationContext* JavaParserLabeled::MemberDeclaration2Context::fieldDeclaration() {
  return getRuleContext<JavaParserLabeled::FieldDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration2Context::MemberDeclaration2Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration2(this);
}
void JavaParserLabeled::MemberDeclaration2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration2(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration3Context ------------------------------------------------------------------

JavaParserLabeled::ConstructorDeclarationContext* JavaParserLabeled::MemberDeclaration3Context::constructorDeclaration() {
  return getRuleContext<JavaParserLabeled::ConstructorDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration3Context::MemberDeclaration3Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration3(this);
}
void JavaParserLabeled::MemberDeclaration3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration3(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration4Context ------------------------------------------------------------------

JavaParserLabeled::GenericConstructorDeclarationContext* JavaParserLabeled::MemberDeclaration4Context::genericConstructorDeclaration() {
  return getRuleContext<JavaParserLabeled::GenericConstructorDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration4Context::MemberDeclaration4Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration4(this);
}
void JavaParserLabeled::MemberDeclaration4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration4(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration5Context ------------------------------------------------------------------

JavaParserLabeled::InterfaceDeclarationContext* JavaParserLabeled::MemberDeclaration5Context::interfaceDeclaration() {
  return getRuleContext<JavaParserLabeled::InterfaceDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration5Context::MemberDeclaration5Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration5(this);
}
void JavaParserLabeled::MemberDeclaration5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration5(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration6Context ------------------------------------------------------------------

JavaParserLabeled::AnnotationTypeDeclarationContext* JavaParserLabeled::MemberDeclaration6Context::annotationTypeDeclaration() {
  return getRuleContext<JavaParserLabeled::AnnotationTypeDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration6Context::MemberDeclaration6Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration6(this);
}
void JavaParserLabeled::MemberDeclaration6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration6(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MemberDeclaration7Context ------------------------------------------------------------------

JavaParserLabeled::ClassDeclarationContext* JavaParserLabeled::MemberDeclaration7Context::classDeclaration() {
  return getRuleContext<JavaParserLabeled::ClassDeclarationContext>(0);
}

JavaParserLabeled::MemberDeclaration7Context::MemberDeclaration7Context(MemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MemberDeclaration7Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMemberDeclaration7(this);
}
void JavaParserLabeled::MemberDeclaration7Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMemberDeclaration7(this);
}

antlrcpp::Any JavaParserLabeled::MemberDeclaration7Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMemberDeclaration7(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::MemberDeclarationContext* JavaParserLabeled::memberDeclaration() {
  MemberDeclarationContext *_localctx = _tracker.createInstance<MemberDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 38, JavaParserLabeled::RuleMemberDeclaration);

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
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(424);
      methodDeclaration();
      break;
    }

    case 2: {
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(425);
      genericMethodDeclaration();
      break;
    }

    case 3: {
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration2Context>(_localctx));
      enterOuterAlt(_localctx, 3);
      setState(426);
      fieldDeclaration();
      break;
    }

    case 4: {
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration3Context>(_localctx));
      enterOuterAlt(_localctx, 4);
      setState(427);
      constructorDeclaration();
      break;
    }

    case 5: {
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration4Context>(_localctx));
      enterOuterAlt(_localctx, 5);
      setState(428);
      genericConstructorDeclaration();
      break;
    }

    case 6: {
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration5Context>(_localctx));
      enterOuterAlt(_localctx, 6);
      setState(429);
      interfaceDeclaration();
      break;
    }

    case 7: {
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration6Context>(_localctx));
      enterOuterAlt(_localctx, 7);
      setState(430);
      annotationTypeDeclaration();
      break;
    }

    case 8: {
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration7Context>(_localctx));
      enterOuterAlt(_localctx, 8);
      setState(431);
      classDeclaration();
      break;
    }

    case 9: {
      _localctx = dynamic_cast<MemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::MemberDeclaration8Context>(_localctx));
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

JavaParserLabeled::MethodDeclarationContext::MethodDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeTypeOrVoidContext* JavaParserLabeled::MethodDeclarationContext::typeTypeOrVoid() {
  return getRuleContext<JavaParserLabeled::TypeTypeOrVoidContext>(0);
}

tree::TerminalNode* JavaParserLabeled::MethodDeclarationContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::FormalParametersContext* JavaParserLabeled::MethodDeclarationContext::formalParameters() {
  return getRuleContext<JavaParserLabeled::FormalParametersContext>(0);
}

JavaParserLabeled::MethodBodyContext* JavaParserLabeled::MethodDeclarationContext::methodBody() {
  return getRuleContext<JavaParserLabeled::MethodBodyContext>(0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::MethodDeclarationContext::LBRACK() {
  return getTokens(JavaParserLabeled::LBRACK);
}

tree::TerminalNode* JavaParserLabeled::MethodDeclarationContext::LBRACK(size_t i) {
  return getToken(JavaParserLabeled::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::MethodDeclarationContext::RBRACK() {
  return getTokens(JavaParserLabeled::RBRACK);
}

tree::TerminalNode* JavaParserLabeled::MethodDeclarationContext::RBRACK(size_t i) {
  return getToken(JavaParserLabeled::RBRACK, i);
}

tree::TerminalNode* JavaParserLabeled::MethodDeclarationContext::THROWS() {
  return getToken(JavaParserLabeled::THROWS, 0);
}

JavaParserLabeled::QualifiedNameListContext* JavaParserLabeled::MethodDeclarationContext::qualifiedNameList() {
  return getRuleContext<JavaParserLabeled::QualifiedNameListContext>(0);
}


size_t JavaParserLabeled::MethodDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleMethodDeclaration;
}

void JavaParserLabeled::MethodDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodDeclaration(this);
}

void JavaParserLabeled::MethodDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::MethodDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMethodDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::MethodDeclarationContext* JavaParserLabeled::methodDeclaration() {
  MethodDeclarationContext *_localctx = _tracker.createInstance<MethodDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 40, JavaParserLabeled::RuleMethodDeclaration);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(437);
    formalParameters();
    setState(442);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaParserLabeled::LBRACK) {
      setState(438);
      match(JavaParserLabeled::LBRACK);
      setState(439);
      match(JavaParserLabeled::RBRACK);
      setState(444);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(447);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::THROWS) {
      setState(445);
      match(JavaParserLabeled::THROWS);
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

JavaParserLabeled::MethodBodyContext::MethodBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::BlockContext* JavaParserLabeled::MethodBodyContext::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

tree::TerminalNode* JavaParserLabeled::MethodBodyContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}


size_t JavaParserLabeled::MethodBodyContext::getRuleIndex() const {
  return JavaParserLabeled::RuleMethodBody;
}

void JavaParserLabeled::MethodBodyContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodBody(this);
}

void JavaParserLabeled::MethodBodyContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodBody(this);
}


antlrcpp::Any JavaParserLabeled::MethodBodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMethodBody(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::MethodBodyContext* JavaParserLabeled::methodBody() {
  MethodBodyContext *_localctx = _tracker.createInstance<MethodBodyContext>(_ctx, getState());
  enterRule(_localctx, 42, JavaParserLabeled::RuleMethodBody);

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
      case JavaParserLabeled::LBRACE: {
        enterOuterAlt(_localctx, 1);
        setState(451);
        block();
        break;
      }

      case JavaParserLabeled::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(452);
        match(JavaParserLabeled::SEMI);
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

JavaParserLabeled::TypeTypeOrVoidContext::TypeTypeOrVoidContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::TypeTypeOrVoidContext::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::TypeTypeOrVoidContext::VOID() {
  return getToken(JavaParserLabeled::VOID, 0);
}


size_t JavaParserLabeled::TypeTypeOrVoidContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeTypeOrVoid;
}

void JavaParserLabeled::TypeTypeOrVoidContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeTypeOrVoid(this);
}

void JavaParserLabeled::TypeTypeOrVoidContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeTypeOrVoid(this);
}


antlrcpp::Any JavaParserLabeled::TypeTypeOrVoidContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeTypeOrVoid(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeTypeOrVoidContext* JavaParserLabeled::typeTypeOrVoid() {
  TypeTypeOrVoidContext *_localctx = _tracker.createInstance<TypeTypeOrVoidContext>(_ctx, getState());
  enterRule(_localctx, 44, JavaParserLabeled::RuleTypeTypeOrVoid);

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
      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::SHORT:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(455);
        typeType();
        break;
      }

      case JavaParserLabeled::VOID: {
        enterOuterAlt(_localctx, 2);
        setState(456);
        match(JavaParserLabeled::VOID);
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

JavaParserLabeled::GenericMethodDeclarationContext::GenericMethodDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeParametersContext* JavaParserLabeled::GenericMethodDeclarationContext::typeParameters() {
  return getRuleContext<JavaParserLabeled::TypeParametersContext>(0);
}

JavaParserLabeled::MethodDeclarationContext* JavaParserLabeled::GenericMethodDeclarationContext::methodDeclaration() {
  return getRuleContext<JavaParserLabeled::MethodDeclarationContext>(0);
}


size_t JavaParserLabeled::GenericMethodDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleGenericMethodDeclaration;
}

void JavaParserLabeled::GenericMethodDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterGenericMethodDeclaration(this);
}

void JavaParserLabeled::GenericMethodDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitGenericMethodDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::GenericMethodDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitGenericMethodDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::GenericMethodDeclarationContext* JavaParserLabeled::genericMethodDeclaration() {
  GenericMethodDeclarationContext *_localctx = _tracker.createInstance<GenericMethodDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 46, JavaParserLabeled::RuleGenericMethodDeclaration);

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

JavaParserLabeled::GenericConstructorDeclarationContext::GenericConstructorDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeParametersContext* JavaParserLabeled::GenericConstructorDeclarationContext::typeParameters() {
  return getRuleContext<JavaParserLabeled::TypeParametersContext>(0);
}

JavaParserLabeled::ConstructorDeclarationContext* JavaParserLabeled::GenericConstructorDeclarationContext::constructorDeclaration() {
  return getRuleContext<JavaParserLabeled::ConstructorDeclarationContext>(0);
}


size_t JavaParserLabeled::GenericConstructorDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleGenericConstructorDeclaration;
}

void JavaParserLabeled::GenericConstructorDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterGenericConstructorDeclaration(this);
}

void JavaParserLabeled::GenericConstructorDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitGenericConstructorDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::GenericConstructorDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitGenericConstructorDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::GenericConstructorDeclarationContext* JavaParserLabeled::genericConstructorDeclaration() {
  GenericConstructorDeclarationContext *_localctx = _tracker.createInstance<GenericConstructorDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 48, JavaParserLabeled::RuleGenericConstructorDeclaration);

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

JavaParserLabeled::ConstructorDeclarationContext::ConstructorDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ConstructorDeclarationContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::FormalParametersContext* JavaParserLabeled::ConstructorDeclarationContext::formalParameters() {
  return getRuleContext<JavaParserLabeled::FormalParametersContext>(0);
}

JavaParserLabeled::BlockContext* JavaParserLabeled::ConstructorDeclarationContext::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ConstructorDeclarationContext::THROWS() {
  return getToken(JavaParserLabeled::THROWS, 0);
}

JavaParserLabeled::QualifiedNameListContext* JavaParserLabeled::ConstructorDeclarationContext::qualifiedNameList() {
  return getRuleContext<JavaParserLabeled::QualifiedNameListContext>(0);
}


size_t JavaParserLabeled::ConstructorDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleConstructorDeclaration;
}

void JavaParserLabeled::ConstructorDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterConstructorDeclaration(this);
}

void JavaParserLabeled::ConstructorDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitConstructorDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::ConstructorDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitConstructorDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ConstructorDeclarationContext* JavaParserLabeled::constructorDeclaration() {
  ConstructorDeclarationContext *_localctx = _tracker.createInstance<ConstructorDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 50, JavaParserLabeled::RuleConstructorDeclaration);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(466);
    formalParameters();
    setState(469);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::THROWS) {
      setState(467);
      match(JavaParserLabeled::THROWS);
      setState(468);
      qualifiedNameList();
    }
    setState(471);
    dynamic_cast<ConstructorDeclarationContext *>(_localctx)->constructorBody = block();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FieldDeclarationContext ------------------------------------------------------------------

JavaParserLabeled::FieldDeclarationContext::FieldDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::FieldDeclarationContext::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

JavaParserLabeled::VariableDeclaratorsContext* JavaParserLabeled::FieldDeclarationContext::variableDeclarators() {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorsContext>(0);
}

tree::TerminalNode* JavaParserLabeled::FieldDeclarationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}


size_t JavaParserLabeled::FieldDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleFieldDeclaration;
}

void JavaParserLabeled::FieldDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFieldDeclaration(this);
}

void JavaParserLabeled::FieldDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFieldDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::FieldDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitFieldDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::FieldDeclarationContext* JavaParserLabeled::fieldDeclaration() {
  FieldDeclarationContext *_localctx = _tracker.createInstance<FieldDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 52, JavaParserLabeled::RuleFieldDeclaration);

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
    match(JavaParserLabeled::SEMI);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InterfaceBodyDeclarationContext ------------------------------------------------------------------

JavaParserLabeled::InterfaceBodyDeclarationContext::InterfaceBodyDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::InterfaceMemberDeclarationContext* JavaParserLabeled::InterfaceBodyDeclarationContext::interfaceMemberDeclaration() {
  return getRuleContext<JavaParserLabeled::InterfaceMemberDeclarationContext>(0);
}

std::vector<JavaParserLabeled::ModifierContext *> JavaParserLabeled::InterfaceBodyDeclarationContext::modifier() {
  return getRuleContexts<JavaParserLabeled::ModifierContext>();
}

JavaParserLabeled::ModifierContext* JavaParserLabeled::InterfaceBodyDeclarationContext::modifier(size_t i) {
  return getRuleContext<JavaParserLabeled::ModifierContext>(i);
}

tree::TerminalNode* JavaParserLabeled::InterfaceBodyDeclarationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}


size_t JavaParserLabeled::InterfaceBodyDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleInterfaceBodyDeclaration;
}

void JavaParserLabeled::InterfaceBodyDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceBodyDeclaration(this);
}

void JavaParserLabeled::InterfaceBodyDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceBodyDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::InterfaceBodyDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceBodyDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::InterfaceBodyDeclarationContext* JavaParserLabeled::interfaceBodyDeclaration() {
  InterfaceBodyDeclarationContext *_localctx = _tracker.createInstance<InterfaceBodyDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 54, JavaParserLabeled::RuleInterfaceBodyDeclaration);

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
      case JavaParserLabeled::ABSTRACT:
      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::CLASS:
      case JavaParserLabeled::DEFAULT:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::ENUM:
      case JavaParserLabeled::FINAL:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::INTERFACE:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::NATIVE:
      case JavaParserLabeled::PRIVATE:
      case JavaParserLabeled::PROTECTED:
      case JavaParserLabeled::PUBLIC:
      case JavaParserLabeled::SHORT:
      case JavaParserLabeled::STATIC:
      case JavaParserLabeled::STRICTFP:
      case JavaParserLabeled::SYNCHRONIZED:
      case JavaParserLabeled::TRANSIENT:
      case JavaParserLabeled::VOID:
      case JavaParserLabeled::VOLATILE:
      case JavaParserLabeled::LT:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
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

      case JavaParserLabeled::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(484);
        match(JavaParserLabeled::SEMI);
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

JavaParserLabeled::InterfaceMemberDeclarationContext::InterfaceMemberDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::InterfaceMemberDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleInterfaceMemberDeclaration;
}

void JavaParserLabeled::InterfaceMemberDeclarationContext::copyFrom(InterfaceMemberDeclarationContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- InterfaceMemberDeclaration6Context ------------------------------------------------------------------

JavaParserLabeled::EnumDeclarationContext* JavaParserLabeled::InterfaceMemberDeclaration6Context::enumDeclaration() {
  return getRuleContext<JavaParserLabeled::EnumDeclarationContext>(0);
}

JavaParserLabeled::InterfaceMemberDeclaration6Context::InterfaceMemberDeclaration6Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::InterfaceMemberDeclaration6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration6(this);
}
void JavaParserLabeled::InterfaceMemberDeclaration6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration6(this);
}

antlrcpp::Any JavaParserLabeled::InterfaceMemberDeclaration6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration5Context ------------------------------------------------------------------

JavaParserLabeled::ClassDeclarationContext* JavaParserLabeled::InterfaceMemberDeclaration5Context::classDeclaration() {
  return getRuleContext<JavaParserLabeled::ClassDeclarationContext>(0);
}

JavaParserLabeled::InterfaceMemberDeclaration5Context::InterfaceMemberDeclaration5Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::InterfaceMemberDeclaration5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration5(this);
}
void JavaParserLabeled::InterfaceMemberDeclaration5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration5(this);
}

antlrcpp::Any JavaParserLabeled::InterfaceMemberDeclaration5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration4Context ------------------------------------------------------------------

JavaParserLabeled::AnnotationTypeDeclarationContext* JavaParserLabeled::InterfaceMemberDeclaration4Context::annotationTypeDeclaration() {
  return getRuleContext<JavaParserLabeled::AnnotationTypeDeclarationContext>(0);
}

JavaParserLabeled::InterfaceMemberDeclaration4Context::InterfaceMemberDeclaration4Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::InterfaceMemberDeclaration4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration4(this);
}
void JavaParserLabeled::InterfaceMemberDeclaration4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration4(this);
}

antlrcpp::Any JavaParserLabeled::InterfaceMemberDeclaration4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration3Context ------------------------------------------------------------------

JavaParserLabeled::InterfaceDeclarationContext* JavaParserLabeled::InterfaceMemberDeclaration3Context::interfaceDeclaration() {
  return getRuleContext<JavaParserLabeled::InterfaceDeclarationContext>(0);
}

JavaParserLabeled::InterfaceMemberDeclaration3Context::InterfaceMemberDeclaration3Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::InterfaceMemberDeclaration3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration3(this);
}
void JavaParserLabeled::InterfaceMemberDeclaration3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration3(this);
}

antlrcpp::Any JavaParserLabeled::InterfaceMemberDeclaration3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration2Context ------------------------------------------------------------------

JavaParserLabeled::GenericInterfaceMethodDeclarationContext* JavaParserLabeled::InterfaceMemberDeclaration2Context::genericInterfaceMethodDeclaration() {
  return getRuleContext<JavaParserLabeled::GenericInterfaceMethodDeclarationContext>(0);
}

JavaParserLabeled::InterfaceMemberDeclaration2Context::InterfaceMemberDeclaration2Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::InterfaceMemberDeclaration2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration2(this);
}
void JavaParserLabeled::InterfaceMemberDeclaration2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration2(this);
}

antlrcpp::Any JavaParserLabeled::InterfaceMemberDeclaration2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration1Context ------------------------------------------------------------------

JavaParserLabeled::InterfaceMethodDeclarationContext* JavaParserLabeled::InterfaceMemberDeclaration1Context::interfaceMethodDeclaration() {
  return getRuleContext<JavaParserLabeled::InterfaceMethodDeclarationContext>(0);
}

JavaParserLabeled::InterfaceMemberDeclaration1Context::InterfaceMemberDeclaration1Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::InterfaceMemberDeclaration1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration1(this);
}
void JavaParserLabeled::InterfaceMemberDeclaration1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration1(this);
}

antlrcpp::Any JavaParserLabeled::InterfaceMemberDeclaration1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- InterfaceMemberDeclaration0Context ------------------------------------------------------------------

JavaParserLabeled::ConstDeclarationContext* JavaParserLabeled::InterfaceMemberDeclaration0Context::constDeclaration() {
  return getRuleContext<JavaParserLabeled::ConstDeclarationContext>(0);
}

JavaParserLabeled::InterfaceMemberDeclaration0Context::InterfaceMemberDeclaration0Context(InterfaceMemberDeclarationContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::InterfaceMemberDeclaration0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMemberDeclaration0(this);
}
void JavaParserLabeled::InterfaceMemberDeclaration0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMemberDeclaration0(this);
}

antlrcpp::Any JavaParserLabeled::InterfaceMemberDeclaration0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMemberDeclaration0(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::InterfaceMemberDeclarationContext* JavaParserLabeled::interfaceMemberDeclaration() {
  InterfaceMemberDeclarationContext *_localctx = _tracker.createInstance<InterfaceMemberDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 56, JavaParserLabeled::RuleInterfaceMemberDeclaration);

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
      _localctx = dynamic_cast<InterfaceMemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::InterfaceMemberDeclaration0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(487);
      constDeclaration();
      break;
    }

    case 2: {
      _localctx = dynamic_cast<InterfaceMemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::InterfaceMemberDeclaration1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(488);
      interfaceMethodDeclaration();
      break;
    }

    case 3: {
      _localctx = dynamic_cast<InterfaceMemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::InterfaceMemberDeclaration2Context>(_localctx));
      enterOuterAlt(_localctx, 3);
      setState(489);
      genericInterfaceMethodDeclaration();
      break;
    }

    case 4: {
      _localctx = dynamic_cast<InterfaceMemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::InterfaceMemberDeclaration3Context>(_localctx));
      enterOuterAlt(_localctx, 4);
      setState(490);
      interfaceDeclaration();
      break;
    }

    case 5: {
      _localctx = dynamic_cast<InterfaceMemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::InterfaceMemberDeclaration4Context>(_localctx));
      enterOuterAlt(_localctx, 5);
      setState(491);
      annotationTypeDeclaration();
      break;
    }

    case 6: {
      _localctx = dynamic_cast<InterfaceMemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::InterfaceMemberDeclaration5Context>(_localctx));
      enterOuterAlt(_localctx, 6);
      setState(492);
      classDeclaration();
      break;
    }

    case 7: {
      _localctx = dynamic_cast<InterfaceMemberDeclarationContext *>(_tracker.createInstance<JavaParserLabeled::InterfaceMemberDeclaration6Context>(_localctx));
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

JavaParserLabeled::ConstDeclarationContext::ConstDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::ConstDeclarationContext::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

std::vector<JavaParserLabeled::ConstantDeclaratorContext *> JavaParserLabeled::ConstDeclarationContext::constantDeclarator() {
  return getRuleContexts<JavaParserLabeled::ConstantDeclaratorContext>();
}

JavaParserLabeled::ConstantDeclaratorContext* JavaParserLabeled::ConstDeclarationContext::constantDeclarator(size_t i) {
  return getRuleContext<JavaParserLabeled::ConstantDeclaratorContext>(i);
}

tree::TerminalNode* JavaParserLabeled::ConstDeclarationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ConstDeclarationContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::ConstDeclarationContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::ConstDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleConstDeclaration;
}

void JavaParserLabeled::ConstDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterConstDeclaration(this);
}

void JavaParserLabeled::ConstDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitConstDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::ConstDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitConstDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ConstDeclarationContext* JavaParserLabeled::constDeclaration() {
  ConstDeclarationContext *_localctx = _tracker.createInstance<ConstDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 58, JavaParserLabeled::RuleConstDeclaration);
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
    while (_la == JavaParserLabeled::COMMA) {
      setState(498);
      match(JavaParserLabeled::COMMA);
      setState(499);
      constantDeclarator();
      setState(504);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(505);
    match(JavaParserLabeled::SEMI);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ConstantDeclaratorContext ------------------------------------------------------------------

JavaParserLabeled::ConstantDeclaratorContext::ConstantDeclaratorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ConstantDeclaratorContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

tree::TerminalNode* JavaParserLabeled::ConstantDeclaratorContext::ASSIGN() {
  return getToken(JavaParserLabeled::ASSIGN, 0);
}

JavaParserLabeled::VariableInitializerContext* JavaParserLabeled::ConstantDeclaratorContext::variableInitializer() {
  return getRuleContext<JavaParserLabeled::VariableInitializerContext>(0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ConstantDeclaratorContext::LBRACK() {
  return getTokens(JavaParserLabeled::LBRACK);
}

tree::TerminalNode* JavaParserLabeled::ConstantDeclaratorContext::LBRACK(size_t i) {
  return getToken(JavaParserLabeled::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ConstantDeclaratorContext::RBRACK() {
  return getTokens(JavaParserLabeled::RBRACK);
}

tree::TerminalNode* JavaParserLabeled::ConstantDeclaratorContext::RBRACK(size_t i) {
  return getToken(JavaParserLabeled::RBRACK, i);
}


size_t JavaParserLabeled::ConstantDeclaratorContext::getRuleIndex() const {
  return JavaParserLabeled::RuleConstantDeclarator;
}

void JavaParserLabeled::ConstantDeclaratorContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterConstantDeclarator(this);
}

void JavaParserLabeled::ConstantDeclaratorContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitConstantDeclarator(this);
}


antlrcpp::Any JavaParserLabeled::ConstantDeclaratorContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitConstantDeclarator(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ConstantDeclaratorContext* JavaParserLabeled::constantDeclarator() {
  ConstantDeclaratorContext *_localctx = _tracker.createInstance<ConstantDeclaratorContext>(_ctx, getState());
  enterRule(_localctx, 60, JavaParserLabeled::RuleConstantDeclarator);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(512);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaParserLabeled::LBRACK) {
      setState(508);
      match(JavaParserLabeled::LBRACK);
      setState(509);
      match(JavaParserLabeled::RBRACK);
      setState(514);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(515);
    match(JavaParserLabeled::ASSIGN);
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

JavaParserLabeled::InterfaceMethodDeclarationContext::InterfaceMethodDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodDeclarationContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::FormalParametersContext* JavaParserLabeled::InterfaceMethodDeclarationContext::formalParameters() {
  return getRuleContext<JavaParserLabeled::FormalParametersContext>(0);
}

JavaParserLabeled::MethodBodyContext* JavaParserLabeled::InterfaceMethodDeclarationContext::methodBody() {
  return getRuleContext<JavaParserLabeled::MethodBodyContext>(0);
}

JavaParserLabeled::TypeTypeOrVoidContext* JavaParserLabeled::InterfaceMethodDeclarationContext::typeTypeOrVoid() {
  return getRuleContext<JavaParserLabeled::TypeTypeOrVoidContext>(0);
}

JavaParserLabeled::TypeParametersContext* JavaParserLabeled::InterfaceMethodDeclarationContext::typeParameters() {
  return getRuleContext<JavaParserLabeled::TypeParametersContext>(0);
}

std::vector<JavaParserLabeled::InterfaceMethodModifierContext *> JavaParserLabeled::InterfaceMethodDeclarationContext::interfaceMethodModifier() {
  return getRuleContexts<JavaParserLabeled::InterfaceMethodModifierContext>();
}

JavaParserLabeled::InterfaceMethodModifierContext* JavaParserLabeled::InterfaceMethodDeclarationContext::interfaceMethodModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::InterfaceMethodModifierContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::InterfaceMethodDeclarationContext::LBRACK() {
  return getTokens(JavaParserLabeled::LBRACK);
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodDeclarationContext::LBRACK(size_t i) {
  return getToken(JavaParserLabeled::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::InterfaceMethodDeclarationContext::RBRACK() {
  return getTokens(JavaParserLabeled::RBRACK);
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodDeclarationContext::RBRACK(size_t i) {
  return getToken(JavaParserLabeled::RBRACK, i);
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodDeclarationContext::THROWS() {
  return getToken(JavaParserLabeled::THROWS, 0);
}

JavaParserLabeled::QualifiedNameListContext* JavaParserLabeled::InterfaceMethodDeclarationContext::qualifiedNameList() {
  return getRuleContext<JavaParserLabeled::QualifiedNameListContext>(0);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::InterfaceMethodDeclarationContext::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::InterfaceMethodDeclarationContext::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}


size_t JavaParserLabeled::InterfaceMethodDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleInterfaceMethodDeclaration;
}

void JavaParserLabeled::InterfaceMethodDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMethodDeclaration(this);
}

void JavaParserLabeled::InterfaceMethodDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMethodDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::InterfaceMethodDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMethodDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::InterfaceMethodDeclarationContext* JavaParserLabeled::interfaceMethodDeclaration() {
  InterfaceMethodDeclarationContext *_localctx = _tracker.createInstance<InterfaceMethodDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 62, JavaParserLabeled::RuleInterfaceMethodDeclaration);
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
      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::SHORT:
      case JavaParserLabeled::VOID:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        setState(524);
        typeTypeOrVoid();
        break;
      }

      case JavaParserLabeled::LT: {
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(537);
    formalParameters();
    setState(542);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaParserLabeled::LBRACK) {
      setState(538);
      match(JavaParserLabeled::LBRACK);
      setState(539);
      match(JavaParserLabeled::RBRACK);
      setState(544);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(547);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::THROWS) {
      setState(545);
      match(JavaParserLabeled::THROWS);
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

JavaParserLabeled::InterfaceMethodModifierContext::InterfaceMethodModifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::InterfaceMethodModifierContext::annotation() {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(0);
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodModifierContext::PUBLIC() {
  return getToken(JavaParserLabeled::PUBLIC, 0);
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodModifierContext::ABSTRACT() {
  return getToken(JavaParserLabeled::ABSTRACT, 0);
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodModifierContext::DEFAULT() {
  return getToken(JavaParserLabeled::DEFAULT, 0);
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodModifierContext::STATIC() {
  return getToken(JavaParserLabeled::STATIC, 0);
}

tree::TerminalNode* JavaParserLabeled::InterfaceMethodModifierContext::STRICTFP() {
  return getToken(JavaParserLabeled::STRICTFP, 0);
}


size_t JavaParserLabeled::InterfaceMethodModifierContext::getRuleIndex() const {
  return JavaParserLabeled::RuleInterfaceMethodModifier;
}

void JavaParserLabeled::InterfaceMethodModifierContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInterfaceMethodModifier(this);
}

void JavaParserLabeled::InterfaceMethodModifierContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInterfaceMethodModifier(this);
}


antlrcpp::Any JavaParserLabeled::InterfaceMethodModifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInterfaceMethodModifier(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::InterfaceMethodModifierContext* JavaParserLabeled::interfaceMethodModifier() {
  InterfaceMethodModifierContext *_localctx = _tracker.createInstance<InterfaceMethodModifierContext>(_ctx, getState());
  enterRule(_localctx, 64, JavaParserLabeled::RuleInterfaceMethodModifier);

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
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(551);
        annotation();
        break;
      }

      case JavaParserLabeled::PUBLIC: {
        enterOuterAlt(_localctx, 2);
        setState(552);
        match(JavaParserLabeled::PUBLIC);
        break;
      }

      case JavaParserLabeled::ABSTRACT: {
        enterOuterAlt(_localctx, 3);
        setState(553);
        match(JavaParserLabeled::ABSTRACT);
        break;
      }

      case JavaParserLabeled::DEFAULT: {
        enterOuterAlt(_localctx, 4);
        setState(554);
        match(JavaParserLabeled::DEFAULT);
        break;
      }

      case JavaParserLabeled::STATIC: {
        enterOuterAlt(_localctx, 5);
        setState(555);
        match(JavaParserLabeled::STATIC);
        break;
      }

      case JavaParserLabeled::STRICTFP: {
        enterOuterAlt(_localctx, 6);
        setState(556);
        match(JavaParserLabeled::STRICTFP);
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

JavaParserLabeled::GenericInterfaceMethodDeclarationContext::GenericInterfaceMethodDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeParametersContext* JavaParserLabeled::GenericInterfaceMethodDeclarationContext::typeParameters() {
  return getRuleContext<JavaParserLabeled::TypeParametersContext>(0);
}

JavaParserLabeled::InterfaceMethodDeclarationContext* JavaParserLabeled::GenericInterfaceMethodDeclarationContext::interfaceMethodDeclaration() {
  return getRuleContext<JavaParserLabeled::InterfaceMethodDeclarationContext>(0);
}


size_t JavaParserLabeled::GenericInterfaceMethodDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleGenericInterfaceMethodDeclaration;
}

void JavaParserLabeled::GenericInterfaceMethodDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterGenericInterfaceMethodDeclaration(this);
}

void JavaParserLabeled::GenericInterfaceMethodDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitGenericInterfaceMethodDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::GenericInterfaceMethodDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitGenericInterfaceMethodDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::GenericInterfaceMethodDeclarationContext* JavaParserLabeled::genericInterfaceMethodDeclaration() {
  GenericInterfaceMethodDeclarationContext *_localctx = _tracker.createInstance<GenericInterfaceMethodDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 66, JavaParserLabeled::RuleGenericInterfaceMethodDeclaration);

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

JavaParserLabeled::VariableDeclaratorsContext::VariableDeclaratorsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::VariableDeclaratorContext *> JavaParserLabeled::VariableDeclaratorsContext::variableDeclarator() {
  return getRuleContexts<JavaParserLabeled::VariableDeclaratorContext>();
}

JavaParserLabeled::VariableDeclaratorContext* JavaParserLabeled::VariableDeclaratorsContext::variableDeclarator(size_t i) {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::VariableDeclaratorsContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::VariableDeclaratorsContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::VariableDeclaratorsContext::getRuleIndex() const {
  return JavaParserLabeled::RuleVariableDeclarators;
}

void JavaParserLabeled::VariableDeclaratorsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableDeclarators(this);
}

void JavaParserLabeled::VariableDeclaratorsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableDeclarators(this);
}


antlrcpp::Any JavaParserLabeled::VariableDeclaratorsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitVariableDeclarators(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::VariableDeclaratorsContext* JavaParserLabeled::variableDeclarators() {
  VariableDeclaratorsContext *_localctx = _tracker.createInstance<VariableDeclaratorsContext>(_ctx, getState());
  enterRule(_localctx, 68, JavaParserLabeled::RuleVariableDeclarators);
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
    while (_la == JavaParserLabeled::COMMA) {
      setState(563);
      match(JavaParserLabeled::COMMA);
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

JavaParserLabeled::VariableDeclaratorContext::VariableDeclaratorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::VariableDeclaratorIdContext* JavaParserLabeled::VariableDeclaratorContext::variableDeclaratorId() {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorIdContext>(0);
}

tree::TerminalNode* JavaParserLabeled::VariableDeclaratorContext::ASSIGN() {
  return getToken(JavaParserLabeled::ASSIGN, 0);
}

JavaParserLabeled::VariableInitializerContext* JavaParserLabeled::VariableDeclaratorContext::variableInitializer() {
  return getRuleContext<JavaParserLabeled::VariableInitializerContext>(0);
}


size_t JavaParserLabeled::VariableDeclaratorContext::getRuleIndex() const {
  return JavaParserLabeled::RuleVariableDeclarator;
}

void JavaParserLabeled::VariableDeclaratorContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableDeclarator(this);
}

void JavaParserLabeled::VariableDeclaratorContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableDeclarator(this);
}


antlrcpp::Any JavaParserLabeled::VariableDeclaratorContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitVariableDeclarator(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::VariableDeclaratorContext* JavaParserLabeled::variableDeclarator() {
  VariableDeclaratorContext *_localctx = _tracker.createInstance<VariableDeclaratorContext>(_ctx, getState());
  enterRule(_localctx, 70, JavaParserLabeled::RuleVariableDeclarator);
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
    if (_la == JavaParserLabeled::ASSIGN) {
      setState(571);
      match(JavaParserLabeled::ASSIGN);
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

JavaParserLabeled::VariableDeclaratorIdContext::VariableDeclaratorIdContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::VariableDeclaratorIdContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::VariableDeclaratorIdContext::LBRACK() {
  return getTokens(JavaParserLabeled::LBRACK);
}

tree::TerminalNode* JavaParserLabeled::VariableDeclaratorIdContext::LBRACK(size_t i) {
  return getToken(JavaParserLabeled::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::VariableDeclaratorIdContext::RBRACK() {
  return getTokens(JavaParserLabeled::RBRACK);
}

tree::TerminalNode* JavaParserLabeled::VariableDeclaratorIdContext::RBRACK(size_t i) {
  return getToken(JavaParserLabeled::RBRACK, i);
}


size_t JavaParserLabeled::VariableDeclaratorIdContext::getRuleIndex() const {
  return JavaParserLabeled::RuleVariableDeclaratorId;
}

void JavaParserLabeled::VariableDeclaratorIdContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableDeclaratorId(this);
}

void JavaParserLabeled::VariableDeclaratorIdContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableDeclaratorId(this);
}


antlrcpp::Any JavaParserLabeled::VariableDeclaratorIdContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitVariableDeclaratorId(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::VariableDeclaratorIdContext* JavaParserLabeled::variableDeclaratorId() {
  VariableDeclaratorIdContext *_localctx = _tracker.createInstance<VariableDeclaratorIdContext>(_ctx, getState());
  enterRule(_localctx, 72, JavaParserLabeled::RuleVariableDeclaratorId);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(580);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaParserLabeled::LBRACK) {
      setState(576);
      match(JavaParserLabeled::LBRACK);
      setState(577);
      match(JavaParserLabeled::RBRACK);
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

JavaParserLabeled::VariableInitializerContext::VariableInitializerContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::VariableInitializerContext::getRuleIndex() const {
  return JavaParserLabeled::RuleVariableInitializer;
}

void JavaParserLabeled::VariableInitializerContext::copyFrom(VariableInitializerContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- VariableInitializer1Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::VariableInitializer1Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

JavaParserLabeled::VariableInitializer1Context::VariableInitializer1Context(VariableInitializerContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::VariableInitializer1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableInitializer1(this);
}
void JavaParserLabeled::VariableInitializer1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableInitializer1(this);
}

antlrcpp::Any JavaParserLabeled::VariableInitializer1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitVariableInitializer1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- VariableInitializer0Context ------------------------------------------------------------------

JavaParserLabeled::ArrayInitializerContext* JavaParserLabeled::VariableInitializer0Context::arrayInitializer() {
  return getRuleContext<JavaParserLabeled::ArrayInitializerContext>(0);
}

JavaParserLabeled::VariableInitializer0Context::VariableInitializer0Context(VariableInitializerContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::VariableInitializer0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVariableInitializer0(this);
}
void JavaParserLabeled::VariableInitializer0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVariableInitializer0(this);
}

antlrcpp::Any JavaParserLabeled::VariableInitializer0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitVariableInitializer0(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::VariableInitializerContext* JavaParserLabeled::variableInitializer() {
  VariableInitializerContext *_localctx = _tracker.createInstance<VariableInitializerContext>(_ctx, getState());
  enterRule(_localctx, 74, JavaParserLabeled::RuleVariableInitializer);

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
      case JavaParserLabeled::LBRACE: {
        _localctx = dynamic_cast<VariableInitializerContext *>(_tracker.createInstance<JavaParserLabeled::VariableInitializer0Context>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(583);
        arrayInitializer();
        break;
      }

      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::NEW:
      case JavaParserLabeled::SHORT:
      case JavaParserLabeled::SUPER:
      case JavaParserLabeled::THIS:
      case JavaParserLabeled::VOID:
      case JavaParserLabeled::DECIMAL_LITERAL:
      case JavaParserLabeled::HEX_LITERAL:
      case JavaParserLabeled::OCT_LITERAL:
      case JavaParserLabeled::BINARY_LITERAL:
      case JavaParserLabeled::FLOAT_LITERAL:
      case JavaParserLabeled::HEX_FLOAT_LITERAL:
      case JavaParserLabeled::BOOL_LITERAL:
      case JavaParserLabeled::CHAR_LITERAL:
      case JavaParserLabeled::STRING_LITERAL:
      case JavaParserLabeled::NULL_LITERAL:
      case JavaParserLabeled::LPAREN:
      case JavaParserLabeled::LT:
      case JavaParserLabeled::BANG:
      case JavaParserLabeled::TILDE:
      case JavaParserLabeled::INC:
      case JavaParserLabeled::DEC:
      case JavaParserLabeled::ADD:
      case JavaParserLabeled::SUB:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        _localctx = dynamic_cast<VariableInitializerContext *>(_tracker.createInstance<JavaParserLabeled::VariableInitializer1Context>(_localctx));
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

JavaParserLabeled::ArrayInitializerContext::ArrayInitializerContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ArrayInitializerContext::LBRACE() {
  return getToken(JavaParserLabeled::LBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::ArrayInitializerContext::RBRACE() {
  return getToken(JavaParserLabeled::RBRACE, 0);
}

std::vector<JavaParserLabeled::VariableInitializerContext *> JavaParserLabeled::ArrayInitializerContext::variableInitializer() {
  return getRuleContexts<JavaParserLabeled::VariableInitializerContext>();
}

JavaParserLabeled::VariableInitializerContext* JavaParserLabeled::ArrayInitializerContext::variableInitializer(size_t i) {
  return getRuleContext<JavaParserLabeled::VariableInitializerContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ArrayInitializerContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::ArrayInitializerContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::ArrayInitializerContext::getRuleIndex() const {
  return JavaParserLabeled::RuleArrayInitializer;
}

void JavaParserLabeled::ArrayInitializerContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterArrayInitializer(this);
}

void JavaParserLabeled::ArrayInitializerContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitArrayInitializer(this);
}


antlrcpp::Any JavaParserLabeled::ArrayInitializerContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitArrayInitializer(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ArrayInitializerContext* JavaParserLabeled::arrayInitializer() {
  ArrayInitializerContext *_localctx = _tracker.createInstance<ArrayInitializerContext>(_ctx, getState());
  enterRule(_localctx, 76, JavaParserLabeled::RuleArrayInitializer);
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
    match(JavaParserLabeled::LBRACE);
    setState(599);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NEW)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::SUPER)
      | (1ULL << JavaParserLabeled::THIS)
      | (1ULL << JavaParserLabeled::VOID)
      | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_LITERAL)
      | (1ULL << JavaParserLabeled::OCT_LITERAL)
      | (1ULL << JavaParserLabeled::BINARY_LITERAL)
      | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::BOOL_LITERAL)
      | (1ULL << JavaParserLabeled::CHAR_LITERAL)
      | (1ULL << JavaParserLabeled::STRING_LITERAL)
      | (1ULL << JavaParserLabeled::NULL_LITERAL)
      | (1ULL << JavaParserLabeled::LPAREN)
      | (1ULL << JavaParserLabeled::LBRACE))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
      | (1ULL << (JavaParserLabeled::BANG - 72))
      | (1ULL << (JavaParserLabeled::TILDE - 72))
      | (1ULL << (JavaParserLabeled::INC - 72))
      | (1ULL << (JavaParserLabeled::DEC - 72))
      | (1ULL << (JavaParserLabeled::ADD - 72))
      | (1ULL << (JavaParserLabeled::SUB - 72))
      | (1ULL << (JavaParserLabeled::AT - 72))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
      setState(588);
      variableInitializer();
      setState(593);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 57, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(589);
          match(JavaParserLabeled::COMMA);
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
      if (_la == JavaParserLabeled::COMMA) {
        setState(596);
        match(JavaParserLabeled::COMMA);
      }
    }
    setState(601);
    match(JavaParserLabeled::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ClassOrInterfaceTypeContext ------------------------------------------------------------------

JavaParserLabeled::ClassOrInterfaceTypeContext::ClassOrInterfaceTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ClassOrInterfaceTypeContext::IDENTIFIER() {
  return getTokens(JavaParserLabeled::IDENTIFIER);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceTypeContext::IDENTIFIER(size_t i) {
  return getToken(JavaParserLabeled::IDENTIFIER, i);
}

std::vector<JavaParserLabeled::TypeArgumentsContext *> JavaParserLabeled::ClassOrInterfaceTypeContext::typeArguments() {
  return getRuleContexts<JavaParserLabeled::TypeArgumentsContext>();
}

JavaParserLabeled::TypeArgumentsContext* JavaParserLabeled::ClassOrInterfaceTypeContext::typeArguments(size_t i) {
  return getRuleContext<JavaParserLabeled::TypeArgumentsContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ClassOrInterfaceTypeContext::DOT() {
  return getTokens(JavaParserLabeled::DOT);
}

tree::TerminalNode* JavaParserLabeled::ClassOrInterfaceTypeContext::DOT(size_t i) {
  return getToken(JavaParserLabeled::DOT, i);
}


size_t JavaParserLabeled::ClassOrInterfaceTypeContext::getRuleIndex() const {
  return JavaParserLabeled::RuleClassOrInterfaceType;
}

void JavaParserLabeled::ClassOrInterfaceTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassOrInterfaceType(this);
}

void JavaParserLabeled::ClassOrInterfaceTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassOrInterfaceType(this);
}


antlrcpp::Any JavaParserLabeled::ClassOrInterfaceTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassOrInterfaceType(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ClassOrInterfaceTypeContext* JavaParserLabeled::classOrInterfaceType() {
  ClassOrInterfaceTypeContext *_localctx = _tracker.createInstance<ClassOrInterfaceTypeContext>(_ctx, getState());
  enterRule(_localctx, 78, JavaParserLabeled::RuleClassOrInterfaceType);

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
    match(JavaParserLabeled::IDENTIFIER);
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
        match(JavaParserLabeled::DOT);
        setState(608);
        match(JavaParserLabeled::IDENTIFIER);
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

JavaParserLabeled::TypeArgumentContext::TypeArgumentContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::TypeArgumentContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeArgument;
}

void JavaParserLabeled::TypeArgumentContext::copyFrom(TypeArgumentContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- TypeArgument0Context ------------------------------------------------------------------

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::TypeArgument0Context::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::TypeArgument0Context::QUESTION() {
  return getToken(JavaParserLabeled::QUESTION, 0);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::TypeArgument0Context::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::TypeArgument0Context::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}

tree::TerminalNode* JavaParserLabeled::TypeArgument0Context::EXTENDS() {
  return getToken(JavaParserLabeled::EXTENDS, 0);
}

tree::TerminalNode* JavaParserLabeled::TypeArgument0Context::SUPER() {
  return getToken(JavaParserLabeled::SUPER, 0);
}

JavaParserLabeled::TypeArgument0Context::TypeArgument0Context(TypeArgumentContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::TypeArgument0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeArgument0(this);
}
void JavaParserLabeled::TypeArgument0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeArgument0(this);
}

antlrcpp::Any JavaParserLabeled::TypeArgument0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeArgument0(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::TypeArgumentContext* JavaParserLabeled::typeArgument() {
  TypeArgumentContext *_localctx = _tracker.createInstance<TypeArgumentContext>(_ctx, getState());
  enterRule(_localctx, 80, JavaParserLabeled::RuleTypeArgument);
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
      _localctx = dynamic_cast<TypeArgumentContext *>(_tracker.createInstance<JavaParserLabeled::TypeArgument0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(617);
      typeType();
      break;
    }

    case 2: {
      _localctx = dynamic_cast<TypeArgumentContext *>(_tracker.createInstance<JavaParserLabeled::TypeArgument0Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(621);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == JavaParserLabeled::AT

      || _la == JavaParserLabeled::IDENTIFIER) {
        setState(618);
        annotation();
        setState(623);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(624);
      match(JavaParserLabeled::QUESTION);
      setState(627);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaParserLabeled::EXTENDS

      || _la == JavaParserLabeled::SUPER) {
        setState(625);
        _la = _input->LA(1);
        if (!(_la == JavaParserLabeled::EXTENDS

        || _la == JavaParserLabeled::SUPER)) {
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

JavaParserLabeled::QualifiedNameListContext::QualifiedNameListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::QualifiedNameContext *> JavaParserLabeled::QualifiedNameListContext::qualifiedName() {
  return getRuleContexts<JavaParserLabeled::QualifiedNameContext>();
}

JavaParserLabeled::QualifiedNameContext* JavaParserLabeled::QualifiedNameListContext::qualifiedName(size_t i) {
  return getRuleContext<JavaParserLabeled::QualifiedNameContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::QualifiedNameListContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::QualifiedNameListContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::QualifiedNameListContext::getRuleIndex() const {
  return JavaParserLabeled::RuleQualifiedNameList;
}

void JavaParserLabeled::QualifiedNameListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterQualifiedNameList(this);
}

void JavaParserLabeled::QualifiedNameListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitQualifiedNameList(this);
}


antlrcpp::Any JavaParserLabeled::QualifiedNameListContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitQualifiedNameList(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::QualifiedNameListContext* JavaParserLabeled::qualifiedNameList() {
  QualifiedNameListContext *_localctx = _tracker.createInstance<QualifiedNameListContext>(_ctx, getState());
  enterRule(_localctx, 82, JavaParserLabeled::RuleQualifiedNameList);
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
    while (_la == JavaParserLabeled::COMMA) {
      setState(632);
      match(JavaParserLabeled::COMMA);
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

JavaParserLabeled::FormalParametersContext::FormalParametersContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::FormalParametersContext::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::FormalParametersContext::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::FormalParameterListContext* JavaParserLabeled::FormalParametersContext::formalParameterList() {
  return getRuleContext<JavaParserLabeled::FormalParameterListContext>(0);
}


size_t JavaParserLabeled::FormalParametersContext::getRuleIndex() const {
  return JavaParserLabeled::RuleFormalParameters;
}

void JavaParserLabeled::FormalParametersContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormalParameters(this);
}

void JavaParserLabeled::FormalParametersContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormalParameters(this);
}


antlrcpp::Any JavaParserLabeled::FormalParametersContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitFormalParameters(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::FormalParametersContext* JavaParserLabeled::formalParameters() {
  FormalParametersContext *_localctx = _tracker.createInstance<FormalParametersContext>(_ctx, getState());
  enterRule(_localctx, 84, JavaParserLabeled::RuleFormalParameters);
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
    match(JavaParserLabeled::LPAREN);
    setState(641);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::FINAL)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::SHORT))) != 0) || _la == JavaParserLabeled::AT

    || _la == JavaParserLabeled::IDENTIFIER) {
      setState(640);
      formalParameterList();
    }
    setState(643);
    match(JavaParserLabeled::RPAREN);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FormalParameterListContext ------------------------------------------------------------------

JavaParserLabeled::FormalParameterListContext::FormalParameterListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::FormalParameterListContext::getRuleIndex() const {
  return JavaParserLabeled::RuleFormalParameterList;
}

void JavaParserLabeled::FormalParameterListContext::copyFrom(FormalParameterListContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- FormalParameterList1Context ------------------------------------------------------------------

JavaParserLabeled::LastFormalParameterContext* JavaParserLabeled::FormalParameterList1Context::lastFormalParameter() {
  return getRuleContext<JavaParserLabeled::LastFormalParameterContext>(0);
}

JavaParserLabeled::FormalParameterList1Context::FormalParameterList1Context(FormalParameterListContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::FormalParameterList1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormalParameterList1(this);
}
void JavaParserLabeled::FormalParameterList1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormalParameterList1(this);
}

antlrcpp::Any JavaParserLabeled::FormalParameterList1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitFormalParameterList1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- FormalParameterList0Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::FormalParameterContext *> JavaParserLabeled::FormalParameterList0Context::formalParameter() {
  return getRuleContexts<JavaParserLabeled::FormalParameterContext>();
}

JavaParserLabeled::FormalParameterContext* JavaParserLabeled::FormalParameterList0Context::formalParameter(size_t i) {
  return getRuleContext<JavaParserLabeled::FormalParameterContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::FormalParameterList0Context::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::FormalParameterList0Context::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}

JavaParserLabeled::LastFormalParameterContext* JavaParserLabeled::FormalParameterList0Context::lastFormalParameter() {
  return getRuleContext<JavaParserLabeled::LastFormalParameterContext>(0);
}

JavaParserLabeled::FormalParameterList0Context::FormalParameterList0Context(FormalParameterListContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::FormalParameterList0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormalParameterList0(this);
}
void JavaParserLabeled::FormalParameterList0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormalParameterList0(this);
}

antlrcpp::Any JavaParserLabeled::FormalParameterList0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitFormalParameterList0(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::FormalParameterListContext* JavaParserLabeled::formalParameterList() {
  FormalParameterListContext *_localctx = _tracker.createInstance<FormalParameterListContext>(_ctx, getState());
  enterRule(_localctx, 86, JavaParserLabeled::RuleFormalParameterList);
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
      _localctx = dynamic_cast<FormalParameterListContext *>(_tracker.createInstance<JavaParserLabeled::FormalParameterList0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(645);
      formalParameter();
      setState(650);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 68, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(646);
          match(JavaParserLabeled::COMMA);
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
      if (_la == JavaParserLabeled::COMMA) {
        setState(653);
        match(JavaParserLabeled::COMMA);
        setState(654);
        lastFormalParameter();
      }
      break;
    }

    case 2: {
      _localctx = dynamic_cast<FormalParameterListContext *>(_tracker.createInstance<JavaParserLabeled::FormalParameterList1Context>(_localctx));
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

JavaParserLabeled::FormalParameterContext::FormalParameterContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::FormalParameterContext::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

JavaParserLabeled::VariableDeclaratorIdContext* JavaParserLabeled::FormalParameterContext::variableDeclaratorId() {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorIdContext>(0);
}

std::vector<JavaParserLabeled::VariableModifierContext *> JavaParserLabeled::FormalParameterContext::variableModifier() {
  return getRuleContexts<JavaParserLabeled::VariableModifierContext>();
}

JavaParserLabeled::VariableModifierContext* JavaParserLabeled::FormalParameterContext::variableModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::VariableModifierContext>(i);
}


size_t JavaParserLabeled::FormalParameterContext::getRuleIndex() const {
  return JavaParserLabeled::RuleFormalParameter;
}

void JavaParserLabeled::FormalParameterContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormalParameter(this);
}

void JavaParserLabeled::FormalParameterContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormalParameter(this);
}


antlrcpp::Any JavaParserLabeled::FormalParameterContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitFormalParameter(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::FormalParameterContext* JavaParserLabeled::formalParameter() {
  FormalParameterContext *_localctx = _tracker.createInstance<FormalParameterContext>(_ctx, getState());
  enterRule(_localctx, 88, JavaParserLabeled::RuleFormalParameter);

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

JavaParserLabeled::LastFormalParameterContext::LastFormalParameterContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::LastFormalParameterContext::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::LastFormalParameterContext::ELLIPSIS() {
  return getToken(JavaParserLabeled::ELLIPSIS, 0);
}

JavaParserLabeled::VariableDeclaratorIdContext* JavaParserLabeled::LastFormalParameterContext::variableDeclaratorId() {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorIdContext>(0);
}

std::vector<JavaParserLabeled::VariableModifierContext *> JavaParserLabeled::LastFormalParameterContext::variableModifier() {
  return getRuleContexts<JavaParserLabeled::VariableModifierContext>();
}

JavaParserLabeled::VariableModifierContext* JavaParserLabeled::LastFormalParameterContext::variableModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::VariableModifierContext>(i);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::LastFormalParameterContext::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::LastFormalParameterContext::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}


size_t JavaParserLabeled::LastFormalParameterContext::getRuleIndex() const {
  return JavaParserLabeled::RuleLastFormalParameter;
}

void JavaParserLabeled::LastFormalParameterContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLastFormalParameter(this);
}

void JavaParserLabeled::LastFormalParameterContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLastFormalParameter(this);
}


antlrcpp::Any JavaParserLabeled::LastFormalParameterContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLastFormalParameter(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::LastFormalParameterContext* JavaParserLabeled::lastFormalParameter() {
  LastFormalParameterContext *_localctx = _tracker.createInstance<LastFormalParameterContext>(_ctx, getState());
  enterRule(_localctx, 90, JavaParserLabeled::RuleLastFormalParameter);
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
    while (_la == JavaParserLabeled::AT

    || _la == JavaParserLabeled::IDENTIFIER) {
      setState(676);
      annotation();
      setState(681);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(682);
    match(JavaParserLabeled::ELLIPSIS);
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

JavaParserLabeled::QualifiedNameContext::QualifiedNameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> JavaParserLabeled::QualifiedNameContext::IDENTIFIER() {
  return getTokens(JavaParserLabeled::IDENTIFIER);
}

tree::TerminalNode* JavaParserLabeled::QualifiedNameContext::IDENTIFIER(size_t i) {
  return getToken(JavaParserLabeled::IDENTIFIER, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::QualifiedNameContext::DOT() {
  return getTokens(JavaParserLabeled::DOT);
}

tree::TerminalNode* JavaParserLabeled::QualifiedNameContext::DOT(size_t i) {
  return getToken(JavaParserLabeled::DOT, i);
}


size_t JavaParserLabeled::QualifiedNameContext::getRuleIndex() const {
  return JavaParserLabeled::RuleQualifiedName;
}

void JavaParserLabeled::QualifiedNameContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterQualifiedName(this);
}

void JavaParserLabeled::QualifiedNameContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitQualifiedName(this);
}


antlrcpp::Any JavaParserLabeled::QualifiedNameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitQualifiedName(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::QualifiedNameContext* JavaParserLabeled::qualifiedName() {
  QualifiedNameContext *_localctx = _tracker.createInstance<QualifiedNameContext>(_ctx, getState());
  enterRule(_localctx, 92, JavaParserLabeled::RuleQualifiedName);

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
    match(JavaParserLabeled::IDENTIFIER);
    setState(690);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 74, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(686);
        match(JavaParserLabeled::DOT);
        setState(687);
        match(JavaParserLabeled::IDENTIFIER); 
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

JavaParserLabeled::LiteralContext::LiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::LiteralContext::getRuleIndex() const {
  return JavaParserLabeled::RuleLiteral;
}

void JavaParserLabeled::LiteralContext::copyFrom(LiteralContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Literal2Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Literal2Context::CHAR_LITERAL() {
  return getToken(JavaParserLabeled::CHAR_LITERAL, 0);
}

JavaParserLabeled::Literal2Context::Literal2Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Literal2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral2(this);
}
void JavaParserLabeled::Literal2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral2(this);
}

antlrcpp::Any JavaParserLabeled::Literal2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLiteral2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal1Context ------------------------------------------------------------------

JavaParserLabeled::FloatLiteralContext* JavaParserLabeled::Literal1Context::floatLiteral() {
  return getRuleContext<JavaParserLabeled::FloatLiteralContext>(0);
}

JavaParserLabeled::Literal1Context::Literal1Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Literal1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral1(this);
}
void JavaParserLabeled::Literal1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral1(this);
}

antlrcpp::Any JavaParserLabeled::Literal1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLiteral1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal0Context ------------------------------------------------------------------

JavaParserLabeled::IntegerLiteralContext* JavaParserLabeled::Literal0Context::integerLiteral() {
  return getRuleContext<JavaParserLabeled::IntegerLiteralContext>(0);
}

JavaParserLabeled::Literal0Context::Literal0Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Literal0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral0(this);
}
void JavaParserLabeled::Literal0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral0(this);
}

antlrcpp::Any JavaParserLabeled::Literal0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLiteral0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal5Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Literal5Context::NULL_LITERAL() {
  return getToken(JavaParserLabeled::NULL_LITERAL, 0);
}

JavaParserLabeled::Literal5Context::Literal5Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Literal5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral5(this);
}
void JavaParserLabeled::Literal5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral5(this);
}

antlrcpp::Any JavaParserLabeled::Literal5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLiteral5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal4Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Literal4Context::BOOL_LITERAL() {
  return getToken(JavaParserLabeled::BOOL_LITERAL, 0);
}

JavaParserLabeled::Literal4Context::Literal4Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Literal4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral4(this);
}
void JavaParserLabeled::Literal4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral4(this);
}

antlrcpp::Any JavaParserLabeled::Literal4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLiteral4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Literal3Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Literal3Context::STRING_LITERAL() {
  return getToken(JavaParserLabeled::STRING_LITERAL, 0);
}

JavaParserLabeled::Literal3Context::Literal3Context(LiteralContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Literal3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral3(this);
}
void JavaParserLabeled::Literal3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral3(this);
}

antlrcpp::Any JavaParserLabeled::Literal3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLiteral3(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::LiteralContext* JavaParserLabeled::literal() {
  LiteralContext *_localctx = _tracker.createInstance<LiteralContext>(_ctx, getState());
  enterRule(_localctx, 94, JavaParserLabeled::RuleLiteral);

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
      case JavaParserLabeled::DECIMAL_LITERAL:
      case JavaParserLabeled::HEX_LITERAL:
      case JavaParserLabeled::OCT_LITERAL:
      case JavaParserLabeled::BINARY_LITERAL: {
        _localctx = dynamic_cast<LiteralContext *>(_tracker.createInstance<JavaParserLabeled::Literal0Context>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(693);
        integerLiteral();
        break;
      }

      case JavaParserLabeled::FLOAT_LITERAL:
      case JavaParserLabeled::HEX_FLOAT_LITERAL: {
        _localctx = dynamic_cast<LiteralContext *>(_tracker.createInstance<JavaParserLabeled::Literal1Context>(_localctx));
        enterOuterAlt(_localctx, 2);
        setState(694);
        floatLiteral();
        break;
      }

      case JavaParserLabeled::CHAR_LITERAL: {
        _localctx = dynamic_cast<LiteralContext *>(_tracker.createInstance<JavaParserLabeled::Literal2Context>(_localctx));
        enterOuterAlt(_localctx, 3);
        setState(695);
        match(JavaParserLabeled::CHAR_LITERAL);
        break;
      }

      case JavaParserLabeled::STRING_LITERAL: {
        _localctx = dynamic_cast<LiteralContext *>(_tracker.createInstance<JavaParserLabeled::Literal3Context>(_localctx));
        enterOuterAlt(_localctx, 4);
        setState(696);
        match(JavaParserLabeled::STRING_LITERAL);
        break;
      }

      case JavaParserLabeled::BOOL_LITERAL: {
        _localctx = dynamic_cast<LiteralContext *>(_tracker.createInstance<JavaParserLabeled::Literal4Context>(_localctx));
        enterOuterAlt(_localctx, 5);
        setState(697);
        match(JavaParserLabeled::BOOL_LITERAL);
        break;
      }

      case JavaParserLabeled::NULL_LITERAL: {
        _localctx = dynamic_cast<LiteralContext *>(_tracker.createInstance<JavaParserLabeled::Literal5Context>(_localctx));
        enterOuterAlt(_localctx, 6);
        setState(698);
        match(JavaParserLabeled::NULL_LITERAL);
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

JavaParserLabeled::IntegerLiteralContext::IntegerLiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::IntegerLiteralContext::DECIMAL_LITERAL() {
  return getToken(JavaParserLabeled::DECIMAL_LITERAL, 0);
}

tree::TerminalNode* JavaParserLabeled::IntegerLiteralContext::HEX_LITERAL() {
  return getToken(JavaParserLabeled::HEX_LITERAL, 0);
}

tree::TerminalNode* JavaParserLabeled::IntegerLiteralContext::OCT_LITERAL() {
  return getToken(JavaParserLabeled::OCT_LITERAL, 0);
}

tree::TerminalNode* JavaParserLabeled::IntegerLiteralContext::BINARY_LITERAL() {
  return getToken(JavaParserLabeled::BINARY_LITERAL, 0);
}


size_t JavaParserLabeled::IntegerLiteralContext::getRuleIndex() const {
  return JavaParserLabeled::RuleIntegerLiteral;
}

void JavaParserLabeled::IntegerLiteralContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterIntegerLiteral(this);
}

void JavaParserLabeled::IntegerLiteralContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitIntegerLiteral(this);
}


antlrcpp::Any JavaParserLabeled::IntegerLiteralContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitIntegerLiteral(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::IntegerLiteralContext* JavaParserLabeled::integerLiteral() {
  IntegerLiteralContext *_localctx = _tracker.createInstance<IntegerLiteralContext>(_ctx, getState());
  enterRule(_localctx, 96, JavaParserLabeled::RuleIntegerLiteral);
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
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::DECIMAL_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_LITERAL)
      | (1ULL << JavaParserLabeled::OCT_LITERAL)
      | (1ULL << JavaParserLabeled::BINARY_LITERAL))) != 0))) {
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

JavaParserLabeled::FloatLiteralContext::FloatLiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::FloatLiteralContext::FLOAT_LITERAL() {
  return getToken(JavaParserLabeled::FLOAT_LITERAL, 0);
}

tree::TerminalNode* JavaParserLabeled::FloatLiteralContext::HEX_FLOAT_LITERAL() {
  return getToken(JavaParserLabeled::HEX_FLOAT_LITERAL, 0);
}


size_t JavaParserLabeled::FloatLiteralContext::getRuleIndex() const {
  return JavaParserLabeled::RuleFloatLiteral;
}

void JavaParserLabeled::FloatLiteralContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFloatLiteral(this);
}

void JavaParserLabeled::FloatLiteralContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFloatLiteral(this);
}


antlrcpp::Any JavaParserLabeled::FloatLiteralContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitFloatLiteral(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::FloatLiteralContext* JavaParserLabeled::floatLiteral() {
  FloatLiteralContext *_localctx = _tracker.createInstance<FloatLiteralContext>(_ctx, getState());
  enterRule(_localctx, 98, JavaParserLabeled::RuleFloatLiteral);
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
    if (!(_la == JavaParserLabeled::FLOAT_LITERAL

    || _la == JavaParserLabeled::HEX_FLOAT_LITERAL)) {
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

JavaParserLabeled::AltAnnotationQualifiedNameContext::AltAnnotationQualifiedNameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::AltAnnotationQualifiedNameContext::AT() {
  return getToken(JavaParserLabeled::AT, 0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::AltAnnotationQualifiedNameContext::IDENTIFIER() {
  return getTokens(JavaParserLabeled::IDENTIFIER);
}

tree::TerminalNode* JavaParserLabeled::AltAnnotationQualifiedNameContext::IDENTIFIER(size_t i) {
  return getToken(JavaParserLabeled::IDENTIFIER, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::AltAnnotationQualifiedNameContext::DOT() {
  return getTokens(JavaParserLabeled::DOT);
}

tree::TerminalNode* JavaParserLabeled::AltAnnotationQualifiedNameContext::DOT(size_t i) {
  return getToken(JavaParserLabeled::DOT, i);
}


size_t JavaParserLabeled::AltAnnotationQualifiedNameContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAltAnnotationQualifiedName;
}

void JavaParserLabeled::AltAnnotationQualifiedNameContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAltAnnotationQualifiedName(this);
}

void JavaParserLabeled::AltAnnotationQualifiedNameContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAltAnnotationQualifiedName(this);
}


antlrcpp::Any JavaParserLabeled::AltAnnotationQualifiedNameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAltAnnotationQualifiedName(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::AltAnnotationQualifiedNameContext* JavaParserLabeled::altAnnotationQualifiedName() {
  AltAnnotationQualifiedNameContext *_localctx = _tracker.createInstance<AltAnnotationQualifiedNameContext>(_ctx, getState());
  enterRule(_localctx, 100, JavaParserLabeled::RuleAltAnnotationQualifiedName);
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
    while (_la == JavaParserLabeled::IDENTIFIER) {
      setState(705);
      match(JavaParserLabeled::IDENTIFIER);
      setState(706);
      match(JavaParserLabeled::DOT);
      setState(711);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(712);
    match(JavaParserLabeled::AT);
    setState(713);
    match(JavaParserLabeled::IDENTIFIER);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationContext ------------------------------------------------------------------

JavaParserLabeled::AnnotationContext::AnnotationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::AnnotationContext::AT() {
  return getToken(JavaParserLabeled::AT, 0);
}

JavaParserLabeled::QualifiedNameContext* JavaParserLabeled::AnnotationContext::qualifiedName() {
  return getRuleContext<JavaParserLabeled::QualifiedNameContext>(0);
}

JavaParserLabeled::AltAnnotationQualifiedNameContext* JavaParserLabeled::AnnotationContext::altAnnotationQualifiedName() {
  return getRuleContext<JavaParserLabeled::AltAnnotationQualifiedNameContext>(0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationContext::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationContext::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::ElementValuePairsContext* JavaParserLabeled::AnnotationContext::elementValuePairs() {
  return getRuleContext<JavaParserLabeled::ElementValuePairsContext>(0);
}

JavaParserLabeled::ElementValueContext* JavaParserLabeled::AnnotationContext::elementValue() {
  return getRuleContext<JavaParserLabeled::ElementValueContext>(0);
}


size_t JavaParserLabeled::AnnotationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAnnotation;
}

void JavaParserLabeled::AnnotationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotation(this);
}

void JavaParserLabeled::AnnotationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotation(this);
}


antlrcpp::Any JavaParserLabeled::AnnotationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotation(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::annotation() {
  AnnotationContext *_localctx = _tracker.createInstance<AnnotationContext>(_ctx, getState());
  enterRule(_localctx, 102, JavaParserLabeled::RuleAnnotation);
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
      match(JavaParserLabeled::AT);
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
    if (_la == JavaParserLabeled::LPAREN) {
      setState(720);
      match(JavaParserLabeled::LPAREN);
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
      match(JavaParserLabeled::RPAREN);
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

JavaParserLabeled::ElementValuePairsContext::ElementValuePairsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::ElementValuePairContext *> JavaParserLabeled::ElementValuePairsContext::elementValuePair() {
  return getRuleContexts<JavaParserLabeled::ElementValuePairContext>();
}

JavaParserLabeled::ElementValuePairContext* JavaParserLabeled::ElementValuePairsContext::elementValuePair(size_t i) {
  return getRuleContext<JavaParserLabeled::ElementValuePairContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ElementValuePairsContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::ElementValuePairsContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::ElementValuePairsContext::getRuleIndex() const {
  return JavaParserLabeled::RuleElementValuePairs;
}

void JavaParserLabeled::ElementValuePairsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValuePairs(this);
}

void JavaParserLabeled::ElementValuePairsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValuePairs(this);
}


antlrcpp::Any JavaParserLabeled::ElementValuePairsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitElementValuePairs(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ElementValuePairsContext* JavaParserLabeled::elementValuePairs() {
  ElementValuePairsContext *_localctx = _tracker.createInstance<ElementValuePairsContext>(_ctx, getState());
  enterRule(_localctx, 104, JavaParserLabeled::RuleElementValuePairs);
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
    while (_la == JavaParserLabeled::COMMA) {
      setState(729);
      match(JavaParserLabeled::COMMA);
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

JavaParserLabeled::ElementValuePairContext::ElementValuePairContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ElementValuePairContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

tree::TerminalNode* JavaParserLabeled::ElementValuePairContext::ASSIGN() {
  return getToken(JavaParserLabeled::ASSIGN, 0);
}

JavaParserLabeled::ElementValueContext* JavaParserLabeled::ElementValuePairContext::elementValue() {
  return getRuleContext<JavaParserLabeled::ElementValueContext>(0);
}


size_t JavaParserLabeled::ElementValuePairContext::getRuleIndex() const {
  return JavaParserLabeled::RuleElementValuePair;
}

void JavaParserLabeled::ElementValuePairContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValuePair(this);
}

void JavaParserLabeled::ElementValuePairContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValuePair(this);
}


antlrcpp::Any JavaParserLabeled::ElementValuePairContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitElementValuePair(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ElementValuePairContext* JavaParserLabeled::elementValuePair() {
  ElementValuePairContext *_localctx = _tracker.createInstance<ElementValuePairContext>(_ctx, getState());
  enterRule(_localctx, 106, JavaParserLabeled::RuleElementValuePair);

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
    match(JavaParserLabeled::IDENTIFIER);
    setState(737);
    match(JavaParserLabeled::ASSIGN);
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

JavaParserLabeled::ElementValueContext::ElementValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::ElementValueContext::getRuleIndex() const {
  return JavaParserLabeled::RuleElementValue;
}

void JavaParserLabeled::ElementValueContext::copyFrom(ElementValueContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ElementValue0Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::ElementValue0Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

JavaParserLabeled::ElementValue0Context::ElementValue0Context(ElementValueContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ElementValue0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValue0(this);
}
void JavaParserLabeled::ElementValue0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValue0(this);
}

antlrcpp::Any JavaParserLabeled::ElementValue0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitElementValue0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ElementValue2Context ------------------------------------------------------------------

JavaParserLabeled::ElementValueArrayInitializerContext* JavaParserLabeled::ElementValue2Context::elementValueArrayInitializer() {
  return getRuleContext<JavaParserLabeled::ElementValueArrayInitializerContext>(0);
}

JavaParserLabeled::ElementValue2Context::ElementValue2Context(ElementValueContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ElementValue2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValue2(this);
}
void JavaParserLabeled::ElementValue2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValue2(this);
}

antlrcpp::Any JavaParserLabeled::ElementValue2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitElementValue2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ElementValue1Context ------------------------------------------------------------------

JavaParserLabeled::AnnotationContext* JavaParserLabeled::ElementValue1Context::annotation() {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(0);
}

JavaParserLabeled::ElementValue1Context::ElementValue1Context(ElementValueContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ElementValue1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValue1(this);
}
void JavaParserLabeled::ElementValue1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValue1(this);
}

antlrcpp::Any JavaParserLabeled::ElementValue1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitElementValue1(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::ElementValueContext* JavaParserLabeled::elementValue() {
  ElementValueContext *_localctx = _tracker.createInstance<ElementValueContext>(_ctx, getState());
  enterRule(_localctx, 108, JavaParserLabeled::RuleElementValue);

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
      _localctx = dynamic_cast<ElementValueContext *>(_tracker.createInstance<JavaParserLabeled::ElementValue0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(740);
      expression(0);
      break;
    }

    case 2: {
      _localctx = dynamic_cast<ElementValueContext *>(_tracker.createInstance<JavaParserLabeled::ElementValue1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(741);
      annotation();
      break;
    }

    case 3: {
      _localctx = dynamic_cast<ElementValueContext *>(_tracker.createInstance<JavaParserLabeled::ElementValue2Context>(_localctx));
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

JavaParserLabeled::ElementValueArrayInitializerContext::ElementValueArrayInitializerContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ElementValueArrayInitializerContext::LBRACE() {
  return getToken(JavaParserLabeled::LBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::ElementValueArrayInitializerContext::RBRACE() {
  return getToken(JavaParserLabeled::RBRACE, 0);
}

std::vector<JavaParserLabeled::ElementValueContext *> JavaParserLabeled::ElementValueArrayInitializerContext::elementValue() {
  return getRuleContexts<JavaParserLabeled::ElementValueContext>();
}

JavaParserLabeled::ElementValueContext* JavaParserLabeled::ElementValueArrayInitializerContext::elementValue(size_t i) {
  return getRuleContext<JavaParserLabeled::ElementValueContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ElementValueArrayInitializerContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::ElementValueArrayInitializerContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::ElementValueArrayInitializerContext::getRuleIndex() const {
  return JavaParserLabeled::RuleElementValueArrayInitializer;
}

void JavaParserLabeled::ElementValueArrayInitializerContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterElementValueArrayInitializer(this);
}

void JavaParserLabeled::ElementValueArrayInitializerContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitElementValueArrayInitializer(this);
}


antlrcpp::Any JavaParserLabeled::ElementValueArrayInitializerContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitElementValueArrayInitializer(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ElementValueArrayInitializerContext* JavaParserLabeled::elementValueArrayInitializer() {
  ElementValueArrayInitializerContext *_localctx = _tracker.createInstance<ElementValueArrayInitializerContext>(_ctx, getState());
  enterRule(_localctx, 110, JavaParserLabeled::RuleElementValueArrayInitializer);
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
    match(JavaParserLabeled::LBRACE);
    setState(754);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NEW)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::SUPER)
      | (1ULL << JavaParserLabeled::THIS)
      | (1ULL << JavaParserLabeled::VOID)
      | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_LITERAL)
      | (1ULL << JavaParserLabeled::OCT_LITERAL)
      | (1ULL << JavaParserLabeled::BINARY_LITERAL)
      | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::BOOL_LITERAL)
      | (1ULL << JavaParserLabeled::CHAR_LITERAL)
      | (1ULL << JavaParserLabeled::STRING_LITERAL)
      | (1ULL << JavaParserLabeled::NULL_LITERAL)
      | (1ULL << JavaParserLabeled::LPAREN)
      | (1ULL << JavaParserLabeled::LBRACE))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
      | (1ULL << (JavaParserLabeled::BANG - 72))
      | (1ULL << (JavaParserLabeled::TILDE - 72))
      | (1ULL << (JavaParserLabeled::INC - 72))
      | (1ULL << (JavaParserLabeled::DEC - 72))
      | (1ULL << (JavaParserLabeled::ADD - 72))
      | (1ULL << (JavaParserLabeled::SUB - 72))
      | (1ULL << (JavaParserLabeled::AT - 72))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
      setState(746);
      elementValue();
      setState(751);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 82, _ctx);
      while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
        if (alt == 1) {
          setState(747);
          match(JavaParserLabeled::COMMA);
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
    if (_la == JavaParserLabeled::COMMA) {
      setState(756);
      match(JavaParserLabeled::COMMA);
    }
    setState(759);
    match(JavaParserLabeled::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationTypeDeclarationContext ------------------------------------------------------------------

JavaParserLabeled::AnnotationTypeDeclarationContext::AnnotationTypeDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeDeclarationContext::AT() {
  return getToken(JavaParserLabeled::AT, 0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeDeclarationContext::INTERFACE() {
  return getToken(JavaParserLabeled::INTERFACE, 0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeDeclarationContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::AnnotationTypeBodyContext* JavaParserLabeled::AnnotationTypeDeclarationContext::annotationTypeBody() {
  return getRuleContext<JavaParserLabeled::AnnotationTypeBodyContext>(0);
}


size_t JavaParserLabeled::AnnotationTypeDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAnnotationTypeDeclaration;
}

void JavaParserLabeled::AnnotationTypeDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeDeclaration(this);
}

void JavaParserLabeled::AnnotationTypeDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::AnnotationTypeDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::AnnotationTypeDeclarationContext* JavaParserLabeled::annotationTypeDeclaration() {
  AnnotationTypeDeclarationContext *_localctx = _tracker.createInstance<AnnotationTypeDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 112, JavaParserLabeled::RuleAnnotationTypeDeclaration);

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
    match(JavaParserLabeled::AT);
    setState(762);
    match(JavaParserLabeled::INTERFACE);
    setState(763);
    match(JavaParserLabeled::IDENTIFIER);
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

JavaParserLabeled::AnnotationTypeBodyContext::AnnotationTypeBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeBodyContext::LBRACE() {
  return getToken(JavaParserLabeled::LBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeBodyContext::RBRACE() {
  return getToken(JavaParserLabeled::RBRACE, 0);
}

std::vector<JavaParserLabeled::AnnotationTypeElementDeclarationContext *> JavaParserLabeled::AnnotationTypeBodyContext::annotationTypeElementDeclaration() {
  return getRuleContexts<JavaParserLabeled::AnnotationTypeElementDeclarationContext>();
}

JavaParserLabeled::AnnotationTypeElementDeclarationContext* JavaParserLabeled::AnnotationTypeBodyContext::annotationTypeElementDeclaration(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationTypeElementDeclarationContext>(i);
}


size_t JavaParserLabeled::AnnotationTypeBodyContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAnnotationTypeBody;
}

void JavaParserLabeled::AnnotationTypeBodyContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeBody(this);
}

void JavaParserLabeled::AnnotationTypeBodyContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeBody(this);
}


antlrcpp::Any JavaParserLabeled::AnnotationTypeBodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeBody(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::AnnotationTypeBodyContext* JavaParserLabeled::annotationTypeBody() {
  AnnotationTypeBodyContext *_localctx = _tracker.createInstance<AnnotationTypeBodyContext>(_ctx, getState());
  enterRule(_localctx, 114, JavaParserLabeled::RuleAnnotationTypeBody);
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
    match(JavaParserLabeled::LBRACE);
    setState(770);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::ABSTRACT)
      | (1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::CLASS)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::ENUM)
      | (1ULL << JavaParserLabeled::FINAL)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::INTERFACE)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NATIVE)
      | (1ULL << JavaParserLabeled::PRIVATE)
      | (1ULL << JavaParserLabeled::PROTECTED)
      | (1ULL << JavaParserLabeled::PUBLIC)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::STATIC)
      | (1ULL << JavaParserLabeled::STRICTFP)
      | (1ULL << JavaParserLabeled::SYNCHRONIZED)
      | (1ULL << JavaParserLabeled::TRANSIENT)
      | (1ULL << JavaParserLabeled::VOLATILE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaParserLabeled::SEMI - 67))
      | (1ULL << (JavaParserLabeled::AT - 67))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 67)))) != 0)) {
      setState(767);
      annotationTypeElementDeclaration();
      setState(772);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(773);
    match(JavaParserLabeled::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AnnotationTypeElementDeclarationContext ------------------------------------------------------------------

JavaParserLabeled::AnnotationTypeElementDeclarationContext::AnnotationTypeElementDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::AnnotationTypeElementRestContext* JavaParserLabeled::AnnotationTypeElementDeclarationContext::annotationTypeElementRest() {
  return getRuleContext<JavaParserLabeled::AnnotationTypeElementRestContext>(0);
}

std::vector<JavaParserLabeled::ModifierContext *> JavaParserLabeled::AnnotationTypeElementDeclarationContext::modifier() {
  return getRuleContexts<JavaParserLabeled::ModifierContext>();
}

JavaParserLabeled::ModifierContext* JavaParserLabeled::AnnotationTypeElementDeclarationContext::modifier(size_t i) {
  return getRuleContext<JavaParserLabeled::ModifierContext>(i);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeElementDeclarationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}


size_t JavaParserLabeled::AnnotationTypeElementDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAnnotationTypeElementDeclaration;
}

void JavaParserLabeled::AnnotationTypeElementDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementDeclaration(this);
}

void JavaParserLabeled::AnnotationTypeElementDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::AnnotationTypeElementDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::AnnotationTypeElementDeclarationContext* JavaParserLabeled::annotationTypeElementDeclaration() {
  AnnotationTypeElementDeclarationContext *_localctx = _tracker.createInstance<AnnotationTypeElementDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 116, JavaParserLabeled::RuleAnnotationTypeElementDeclaration);

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
      case JavaParserLabeled::ABSTRACT:
      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::CLASS:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::ENUM:
      case JavaParserLabeled::FINAL:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::INTERFACE:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::NATIVE:
      case JavaParserLabeled::PRIVATE:
      case JavaParserLabeled::PROTECTED:
      case JavaParserLabeled::PUBLIC:
      case JavaParserLabeled::SHORT:
      case JavaParserLabeled::STATIC:
      case JavaParserLabeled::STRICTFP:
      case JavaParserLabeled::SYNCHRONIZED:
      case JavaParserLabeled::TRANSIENT:
      case JavaParserLabeled::VOLATILE:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
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

      case JavaParserLabeled::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(782);
        match(JavaParserLabeled::SEMI);
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

JavaParserLabeled::AnnotationTypeElementRestContext::AnnotationTypeElementRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::AnnotationTypeElementRestContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAnnotationTypeElementRest;
}

void JavaParserLabeled::AnnotationTypeElementRestContext::copyFrom(AnnotationTypeElementRestContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- AnnotationTypeElementRest0Context ------------------------------------------------------------------

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::AnnotationTypeElementRest0Context::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

JavaParserLabeled::AnnotationMethodOrConstantRestContext* JavaParserLabeled::AnnotationTypeElementRest0Context::annotationMethodOrConstantRest() {
  return getRuleContext<JavaParserLabeled::AnnotationMethodOrConstantRestContext>(0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeElementRest0Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::AnnotationTypeElementRest0Context::AnnotationTypeElementRest0Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::AnnotationTypeElementRest0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest0(this);
}
void JavaParserLabeled::AnnotationTypeElementRest0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest0(this);
}

antlrcpp::Any JavaParserLabeled::AnnotationTypeElementRest0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationTypeElementRest1Context ------------------------------------------------------------------

JavaParserLabeled::ClassDeclarationContext* JavaParserLabeled::AnnotationTypeElementRest1Context::classDeclaration() {
  return getRuleContext<JavaParserLabeled::ClassDeclarationContext>(0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeElementRest1Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::AnnotationTypeElementRest1Context::AnnotationTypeElementRest1Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::AnnotationTypeElementRest1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest1(this);
}
void JavaParserLabeled::AnnotationTypeElementRest1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest1(this);
}

antlrcpp::Any JavaParserLabeled::AnnotationTypeElementRest1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationTypeElementRest2Context ------------------------------------------------------------------

JavaParserLabeled::InterfaceDeclarationContext* JavaParserLabeled::AnnotationTypeElementRest2Context::interfaceDeclaration() {
  return getRuleContext<JavaParserLabeled::InterfaceDeclarationContext>(0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeElementRest2Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::AnnotationTypeElementRest2Context::AnnotationTypeElementRest2Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::AnnotationTypeElementRest2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest2(this);
}
void JavaParserLabeled::AnnotationTypeElementRest2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest2(this);
}

antlrcpp::Any JavaParserLabeled::AnnotationTypeElementRest2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationTypeElementRest3Context ------------------------------------------------------------------

JavaParserLabeled::EnumDeclarationContext* JavaParserLabeled::AnnotationTypeElementRest3Context::enumDeclaration() {
  return getRuleContext<JavaParserLabeled::EnumDeclarationContext>(0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeElementRest3Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::AnnotationTypeElementRest3Context::AnnotationTypeElementRest3Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::AnnotationTypeElementRest3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest3(this);
}
void JavaParserLabeled::AnnotationTypeElementRest3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest3(this);
}

antlrcpp::Any JavaParserLabeled::AnnotationTypeElementRest3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationTypeElementRest4Context ------------------------------------------------------------------

JavaParserLabeled::AnnotationTypeDeclarationContext* JavaParserLabeled::AnnotationTypeElementRest4Context::annotationTypeDeclaration() {
  return getRuleContext<JavaParserLabeled::AnnotationTypeDeclarationContext>(0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationTypeElementRest4Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::AnnotationTypeElementRest4Context::AnnotationTypeElementRest4Context(AnnotationTypeElementRestContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::AnnotationTypeElementRest4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationTypeElementRest4(this);
}
void JavaParserLabeled::AnnotationTypeElementRest4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationTypeElementRest4(this);
}

antlrcpp::Any JavaParserLabeled::AnnotationTypeElementRest4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationTypeElementRest4(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::AnnotationTypeElementRestContext* JavaParserLabeled::annotationTypeElementRest() {
  AnnotationTypeElementRestContext *_localctx = _tracker.createInstance<AnnotationTypeElementRestContext>(_ctx, getState());
  enterRule(_localctx, 118, JavaParserLabeled::RuleAnnotationTypeElementRest);

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
      _localctx = dynamic_cast<AnnotationTypeElementRestContext *>(_tracker.createInstance<JavaParserLabeled::AnnotationTypeElementRest0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(785);
      typeType();
      setState(786);
      annotationMethodOrConstantRest();
      setState(787);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 2: {
      _localctx = dynamic_cast<AnnotationTypeElementRestContext *>(_tracker.createInstance<JavaParserLabeled::AnnotationTypeElementRest1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(789);
      classDeclaration();
      setState(791);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 88, _ctx)) {
      case 1: {
        setState(790);
        match(JavaParserLabeled::SEMI);
        break;
      }

      default:
        break;
      }
      break;
    }

    case 3: {
      _localctx = dynamic_cast<AnnotationTypeElementRestContext *>(_tracker.createInstance<JavaParserLabeled::AnnotationTypeElementRest2Context>(_localctx));
      enterOuterAlt(_localctx, 3);
      setState(793);
      interfaceDeclaration();
      setState(795);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 89, _ctx)) {
      case 1: {
        setState(794);
        match(JavaParserLabeled::SEMI);
        break;
      }

      default:
        break;
      }
      break;
    }

    case 4: {
      _localctx = dynamic_cast<AnnotationTypeElementRestContext *>(_tracker.createInstance<JavaParserLabeled::AnnotationTypeElementRest3Context>(_localctx));
      enterOuterAlt(_localctx, 4);
      setState(797);
      enumDeclaration();
      setState(799);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 90, _ctx)) {
      case 1: {
        setState(798);
        match(JavaParserLabeled::SEMI);
        break;
      }

      default:
        break;
      }
      break;
    }

    case 5: {
      _localctx = dynamic_cast<AnnotationTypeElementRestContext *>(_tracker.createInstance<JavaParserLabeled::AnnotationTypeElementRest4Context>(_localctx));
      enterOuterAlt(_localctx, 5);
      setState(801);
      annotationTypeDeclaration();
      setState(803);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 91, _ctx)) {
      case 1: {
        setState(802);
        match(JavaParserLabeled::SEMI);
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

JavaParserLabeled::AnnotationMethodOrConstantRestContext::AnnotationMethodOrConstantRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::AnnotationMethodOrConstantRestContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAnnotationMethodOrConstantRest;
}

void JavaParserLabeled::AnnotationMethodOrConstantRestContext::copyFrom(AnnotationMethodOrConstantRestContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- AnnotationMethodOrConstantRest0Context ------------------------------------------------------------------

JavaParserLabeled::AnnotationMethodRestContext* JavaParserLabeled::AnnotationMethodOrConstantRest0Context::annotationMethodRest() {
  return getRuleContext<JavaParserLabeled::AnnotationMethodRestContext>(0);
}

JavaParserLabeled::AnnotationMethodOrConstantRest0Context::AnnotationMethodOrConstantRest0Context(AnnotationMethodOrConstantRestContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::AnnotationMethodOrConstantRest0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationMethodOrConstantRest0(this);
}
void JavaParserLabeled::AnnotationMethodOrConstantRest0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationMethodOrConstantRest0(this);
}

antlrcpp::Any JavaParserLabeled::AnnotationMethodOrConstantRest0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationMethodOrConstantRest0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AnnotationMethodOrConstantRest1Context ------------------------------------------------------------------

JavaParserLabeled::AnnotationConstantRestContext* JavaParserLabeled::AnnotationMethodOrConstantRest1Context::annotationConstantRest() {
  return getRuleContext<JavaParserLabeled::AnnotationConstantRestContext>(0);
}

JavaParserLabeled::AnnotationMethodOrConstantRest1Context::AnnotationMethodOrConstantRest1Context(AnnotationMethodOrConstantRestContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::AnnotationMethodOrConstantRest1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationMethodOrConstantRest1(this);
}
void JavaParserLabeled::AnnotationMethodOrConstantRest1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationMethodOrConstantRest1(this);
}

antlrcpp::Any JavaParserLabeled::AnnotationMethodOrConstantRest1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationMethodOrConstantRest1(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::AnnotationMethodOrConstantRestContext* JavaParserLabeled::annotationMethodOrConstantRest() {
  AnnotationMethodOrConstantRestContext *_localctx = _tracker.createInstance<AnnotationMethodOrConstantRestContext>(_ctx, getState());
  enterRule(_localctx, 120, JavaParserLabeled::RuleAnnotationMethodOrConstantRest);

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
      _localctx = dynamic_cast<AnnotationMethodOrConstantRestContext *>(_tracker.createInstance<JavaParserLabeled::AnnotationMethodOrConstantRest0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(807);
      annotationMethodRest();
      break;
    }

    case 2: {
      _localctx = dynamic_cast<AnnotationMethodOrConstantRestContext *>(_tracker.createInstance<JavaParserLabeled::AnnotationMethodOrConstantRest1Context>(_localctx));
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

JavaParserLabeled::AnnotationMethodRestContext::AnnotationMethodRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::AnnotationMethodRestContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationMethodRestContext::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::AnnotationMethodRestContext::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::DefaultValueContext* JavaParserLabeled::AnnotationMethodRestContext::defaultValue() {
  return getRuleContext<JavaParserLabeled::DefaultValueContext>(0);
}


size_t JavaParserLabeled::AnnotationMethodRestContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAnnotationMethodRest;
}

void JavaParserLabeled::AnnotationMethodRestContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationMethodRest(this);
}

void JavaParserLabeled::AnnotationMethodRestContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationMethodRest(this);
}


antlrcpp::Any JavaParserLabeled::AnnotationMethodRestContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationMethodRest(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::AnnotationMethodRestContext* JavaParserLabeled::annotationMethodRest() {
  AnnotationMethodRestContext *_localctx = _tracker.createInstance<AnnotationMethodRestContext>(_ctx, getState());
  enterRule(_localctx, 122, JavaParserLabeled::RuleAnnotationMethodRest);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(812);
    match(JavaParserLabeled::LPAREN);
    setState(813);
    match(JavaParserLabeled::RPAREN);
    setState(815);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::DEFAULT) {
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

JavaParserLabeled::AnnotationConstantRestContext::AnnotationConstantRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::VariableDeclaratorsContext* JavaParserLabeled::AnnotationConstantRestContext::variableDeclarators() {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorsContext>(0);
}


size_t JavaParserLabeled::AnnotationConstantRestContext::getRuleIndex() const {
  return JavaParserLabeled::RuleAnnotationConstantRest;
}

void JavaParserLabeled::AnnotationConstantRestContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAnnotationConstantRest(this);
}

void JavaParserLabeled::AnnotationConstantRestContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAnnotationConstantRest(this);
}


antlrcpp::Any JavaParserLabeled::AnnotationConstantRestContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitAnnotationConstantRest(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::AnnotationConstantRestContext* JavaParserLabeled::annotationConstantRest() {
  AnnotationConstantRestContext *_localctx = _tracker.createInstance<AnnotationConstantRestContext>(_ctx, getState());
  enterRule(_localctx, 124, JavaParserLabeled::RuleAnnotationConstantRest);

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

JavaParserLabeled::DefaultValueContext::DefaultValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::DefaultValueContext::DEFAULT() {
  return getToken(JavaParserLabeled::DEFAULT, 0);
}

JavaParserLabeled::ElementValueContext* JavaParserLabeled::DefaultValueContext::elementValue() {
  return getRuleContext<JavaParserLabeled::ElementValueContext>(0);
}


size_t JavaParserLabeled::DefaultValueContext::getRuleIndex() const {
  return JavaParserLabeled::RuleDefaultValue;
}

void JavaParserLabeled::DefaultValueContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterDefaultValue(this);
}

void JavaParserLabeled::DefaultValueContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitDefaultValue(this);
}


antlrcpp::Any JavaParserLabeled::DefaultValueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitDefaultValue(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::DefaultValueContext* JavaParserLabeled::defaultValue() {
  DefaultValueContext *_localctx = _tracker.createInstance<DefaultValueContext>(_ctx, getState());
  enterRule(_localctx, 126, JavaParserLabeled::RuleDefaultValue);

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
    match(JavaParserLabeled::DEFAULT);
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

JavaParserLabeled::BlockContext::BlockContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::BlockContext::LBRACE() {
  return getToken(JavaParserLabeled::LBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::BlockContext::RBRACE() {
  return getToken(JavaParserLabeled::RBRACE, 0);
}

std::vector<JavaParserLabeled::BlockStatementContext *> JavaParserLabeled::BlockContext::blockStatement() {
  return getRuleContexts<JavaParserLabeled::BlockStatementContext>();
}

JavaParserLabeled::BlockStatementContext* JavaParserLabeled::BlockContext::blockStatement(size_t i) {
  return getRuleContext<JavaParserLabeled::BlockStatementContext>(i);
}


size_t JavaParserLabeled::BlockContext::getRuleIndex() const {
  return JavaParserLabeled::RuleBlock;
}

void JavaParserLabeled::BlockContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlock(this);
}

void JavaParserLabeled::BlockContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlock(this);
}


antlrcpp::Any JavaParserLabeled::BlockContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitBlock(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::BlockContext* JavaParserLabeled::block() {
  BlockContext *_localctx = _tracker.createInstance<BlockContext>(_ctx, getState());
  enterRule(_localctx, 128, JavaParserLabeled::RuleBlock);
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
    match(JavaParserLabeled::LBRACE);
    setState(826);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::ABSTRACT)
      | (1ULL << JavaParserLabeled::ASSERT)
      | (1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BREAK)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::CLASS)
      | (1ULL << JavaParserLabeled::CONTINUE)
      | (1ULL << JavaParserLabeled::DO)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::FINAL)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::FOR)
      | (1ULL << JavaParserLabeled::IF)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::INTERFACE)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NEW)
      | (1ULL << JavaParserLabeled::PRIVATE)
      | (1ULL << JavaParserLabeled::PROTECTED)
      | (1ULL << JavaParserLabeled::PUBLIC)
      | (1ULL << JavaParserLabeled::RETURN)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::STATIC)
      | (1ULL << JavaParserLabeled::STRICTFP)
      | (1ULL << JavaParserLabeled::SUPER)
      | (1ULL << JavaParserLabeled::SWITCH)
      | (1ULL << JavaParserLabeled::SYNCHRONIZED)
      | (1ULL << JavaParserLabeled::THIS)
      | (1ULL << JavaParserLabeled::THROW)
      | (1ULL << JavaParserLabeled::TRY)
      | (1ULL << JavaParserLabeled::VOID)
      | (1ULL << JavaParserLabeled::WHILE)
      | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_LITERAL)
      | (1ULL << JavaParserLabeled::OCT_LITERAL)
      | (1ULL << JavaParserLabeled::BINARY_LITERAL)
      | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::BOOL_LITERAL)
      | (1ULL << JavaParserLabeled::CHAR_LITERAL)
      | (1ULL << JavaParserLabeled::STRING_LITERAL)
      | (1ULL << JavaParserLabeled::NULL_LITERAL)
      | (1ULL << JavaParserLabeled::LPAREN)
      | (1ULL << JavaParserLabeled::LBRACE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaParserLabeled::SEMI - 67))
      | (1ULL << (JavaParserLabeled::LT - 67))
      | (1ULL << (JavaParserLabeled::BANG - 67))
      | (1ULL << (JavaParserLabeled::TILDE - 67))
      | (1ULL << (JavaParserLabeled::INC - 67))
      | (1ULL << (JavaParserLabeled::DEC - 67))
      | (1ULL << (JavaParserLabeled::ADD - 67))
      | (1ULL << (JavaParserLabeled::SUB - 67))
      | (1ULL << (JavaParserLabeled::AT - 67))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 67)))) != 0)) {
      setState(823);
      blockStatement();
      setState(828);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(829);
    match(JavaParserLabeled::RBRACE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- BlockStatementContext ------------------------------------------------------------------

JavaParserLabeled::BlockStatementContext::BlockStatementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::BlockStatementContext::getRuleIndex() const {
  return JavaParserLabeled::RuleBlockStatement;
}

void JavaParserLabeled::BlockStatementContext::copyFrom(BlockStatementContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- BlockStatement1Context ------------------------------------------------------------------

JavaParserLabeled::StatementContext* JavaParserLabeled::BlockStatement1Context::statement() {
  return getRuleContext<JavaParserLabeled::StatementContext>(0);
}

JavaParserLabeled::BlockStatement1Context::BlockStatement1Context(BlockStatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::BlockStatement1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlockStatement1(this);
}
void JavaParserLabeled::BlockStatement1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlockStatement1(this);
}

antlrcpp::Any JavaParserLabeled::BlockStatement1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitBlockStatement1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- BlockStatement0Context ------------------------------------------------------------------

JavaParserLabeled::LocalVariableDeclarationContext* JavaParserLabeled::BlockStatement0Context::localVariableDeclaration() {
  return getRuleContext<JavaParserLabeled::LocalVariableDeclarationContext>(0);
}

tree::TerminalNode* JavaParserLabeled::BlockStatement0Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::BlockStatement0Context::BlockStatement0Context(BlockStatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::BlockStatement0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlockStatement0(this);
}
void JavaParserLabeled::BlockStatement0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlockStatement0(this);
}

antlrcpp::Any JavaParserLabeled::BlockStatement0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitBlockStatement0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- BlockStatement2Context ------------------------------------------------------------------

JavaParserLabeled::LocalTypeDeclarationContext* JavaParserLabeled::BlockStatement2Context::localTypeDeclaration() {
  return getRuleContext<JavaParserLabeled::LocalTypeDeclarationContext>(0);
}

JavaParserLabeled::BlockStatement2Context::BlockStatement2Context(BlockStatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::BlockStatement2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlockStatement2(this);
}
void JavaParserLabeled::BlockStatement2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlockStatement2(this);
}

antlrcpp::Any JavaParserLabeled::BlockStatement2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitBlockStatement2(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::BlockStatementContext* JavaParserLabeled::blockStatement() {
  BlockStatementContext *_localctx = _tracker.createInstance<BlockStatementContext>(_ctx, getState());
  enterRule(_localctx, 130, JavaParserLabeled::RuleBlockStatement);

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
      _localctx = dynamic_cast<BlockStatementContext *>(_tracker.createInstance<JavaParserLabeled::BlockStatement0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(831);
      localVariableDeclaration();
      setState(832);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 2: {
      _localctx = dynamic_cast<BlockStatementContext *>(_tracker.createInstance<JavaParserLabeled::BlockStatement1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(834);
      statement();
      break;
    }

    case 3: {
      _localctx = dynamic_cast<BlockStatementContext *>(_tracker.createInstance<JavaParserLabeled::BlockStatement2Context>(_localctx));
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

JavaParserLabeled::LocalVariableDeclarationContext::LocalVariableDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::LocalVariableDeclarationContext::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

JavaParserLabeled::VariableDeclaratorsContext* JavaParserLabeled::LocalVariableDeclarationContext::variableDeclarators() {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorsContext>(0);
}

std::vector<JavaParserLabeled::VariableModifierContext *> JavaParserLabeled::LocalVariableDeclarationContext::variableModifier() {
  return getRuleContexts<JavaParserLabeled::VariableModifierContext>();
}

JavaParserLabeled::VariableModifierContext* JavaParserLabeled::LocalVariableDeclarationContext::variableModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::VariableModifierContext>(i);
}


size_t JavaParserLabeled::LocalVariableDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleLocalVariableDeclaration;
}

void JavaParserLabeled::LocalVariableDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLocalVariableDeclaration(this);
}

void JavaParserLabeled::LocalVariableDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLocalVariableDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::LocalVariableDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLocalVariableDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::LocalVariableDeclarationContext* JavaParserLabeled::localVariableDeclaration() {
  LocalVariableDeclarationContext *_localctx = _tracker.createInstance<LocalVariableDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 132, JavaParserLabeled::RuleLocalVariableDeclaration);

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

JavaParserLabeled::LocalTypeDeclarationContext::LocalTypeDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::ClassDeclarationContext* JavaParserLabeled::LocalTypeDeclarationContext::classDeclaration() {
  return getRuleContext<JavaParserLabeled::ClassDeclarationContext>(0);
}

JavaParserLabeled::InterfaceDeclarationContext* JavaParserLabeled::LocalTypeDeclarationContext::interfaceDeclaration() {
  return getRuleContext<JavaParserLabeled::InterfaceDeclarationContext>(0);
}

std::vector<JavaParserLabeled::ClassOrInterfaceModifierContext *> JavaParserLabeled::LocalTypeDeclarationContext::classOrInterfaceModifier() {
  return getRuleContexts<JavaParserLabeled::ClassOrInterfaceModifierContext>();
}

JavaParserLabeled::ClassOrInterfaceModifierContext* JavaParserLabeled::LocalTypeDeclarationContext::classOrInterfaceModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::ClassOrInterfaceModifierContext>(i);
}

tree::TerminalNode* JavaParserLabeled::LocalTypeDeclarationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}


size_t JavaParserLabeled::LocalTypeDeclarationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleLocalTypeDeclaration;
}

void JavaParserLabeled::LocalTypeDeclarationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLocalTypeDeclaration(this);
}

void JavaParserLabeled::LocalTypeDeclarationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLocalTypeDeclaration(this);
}


antlrcpp::Any JavaParserLabeled::LocalTypeDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLocalTypeDeclaration(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::LocalTypeDeclarationContext* JavaParserLabeled::localTypeDeclaration() {
  LocalTypeDeclarationContext *_localctx = _tracker.createInstance<LocalTypeDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 134, JavaParserLabeled::RuleLocalTypeDeclaration);
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
      case JavaParserLabeled::ABSTRACT:
      case JavaParserLabeled::CLASS:
      case JavaParserLabeled::FINAL:
      case JavaParserLabeled::INTERFACE:
      case JavaParserLabeled::PRIVATE:
      case JavaParserLabeled::PROTECTED:
      case JavaParserLabeled::PUBLIC:
      case JavaParserLabeled::STATIC:
      case JavaParserLabeled::STRICTFP:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        enterOuterAlt(_localctx, 1);
        setState(850);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << JavaParserLabeled::ABSTRACT)
          | (1ULL << JavaParserLabeled::FINAL)
          | (1ULL << JavaParserLabeled::PRIVATE)
          | (1ULL << JavaParserLabeled::PROTECTED)
          | (1ULL << JavaParserLabeled::PUBLIC)
          | (1ULL << JavaParserLabeled::STATIC)
          | (1ULL << JavaParserLabeled::STRICTFP))) != 0) || _la == JavaParserLabeled::AT

        || _la == JavaParserLabeled::IDENTIFIER) {
          setState(847);
          classOrInterfaceModifier();
          setState(852);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        setState(855);
        _errHandler->sync(this);
        switch (_input->LA(1)) {
          case JavaParserLabeled::CLASS: {
            setState(853);
            classDeclaration();
            break;
          }

          case JavaParserLabeled::INTERFACE: {
            setState(854);
            interfaceDeclaration();
            break;
          }

        default:
          throw NoViableAltException(this);
        }
        break;
      }

      case JavaParserLabeled::SEMI: {
        enterOuterAlt(_localctx, 2);
        setState(857);
        match(JavaParserLabeled::SEMI);
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

JavaParserLabeled::StatementContext::StatementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::StatementContext::getRuleIndex() const {
  return JavaParserLabeled::RuleStatement;
}

void JavaParserLabeled::StatementContext::copyFrom(StatementContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Statement14Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement14Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::Statement14Context::Statement14Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement14Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement14(this);
}
void JavaParserLabeled::Statement14Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement14(this);
}

antlrcpp::Any JavaParserLabeled::Statement14Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement14(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement15Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement15Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Statement15Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

JavaParserLabeled::Statement15Context::Statement15Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement15Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement15(this);
}
void JavaParserLabeled::Statement15Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement15(this);
}

antlrcpp::Any JavaParserLabeled::Statement15Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement15(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement12Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement12Context::BREAK() {
  return getToken(JavaParserLabeled::BREAK, 0);
}

tree::TerminalNode* JavaParserLabeled::Statement12Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

tree::TerminalNode* JavaParserLabeled::Statement12Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::Statement12Context::Statement12Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement12Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement12(this);
}
void JavaParserLabeled::Statement12Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement12(this);
}

antlrcpp::Any JavaParserLabeled::Statement12Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement12(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement13Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement13Context::CONTINUE() {
  return getToken(JavaParserLabeled::CONTINUE, 0);
}

tree::TerminalNode* JavaParserLabeled::Statement13Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

tree::TerminalNode* JavaParserLabeled::Statement13Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::Statement13Context::Statement13Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement13Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement13(this);
}
void JavaParserLabeled::Statement13Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement13(this);
}

antlrcpp::Any JavaParserLabeled::Statement13Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement13(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement9Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement9Context::SYNCHRONIZED() {
  return getToken(JavaParserLabeled::SYNCHRONIZED, 0);
}

JavaParserLabeled::ParExpressionContext* JavaParserLabeled::Statement9Context::parExpression() {
  return getRuleContext<JavaParserLabeled::ParExpressionContext>(0);
}

JavaParserLabeled::BlockContext* JavaParserLabeled::Statement9Context::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

JavaParserLabeled::Statement9Context::Statement9Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement9Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement9(this);
}
void JavaParserLabeled::Statement9Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement9(this);
}

antlrcpp::Any JavaParserLabeled::Statement9Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement9(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement7Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement7Context::TRY() {
  return getToken(JavaParserLabeled::TRY, 0);
}

JavaParserLabeled::ResourceSpecificationContext* JavaParserLabeled::Statement7Context::resourceSpecification() {
  return getRuleContext<JavaParserLabeled::ResourceSpecificationContext>(0);
}

JavaParserLabeled::BlockContext* JavaParserLabeled::Statement7Context::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

std::vector<JavaParserLabeled::CatchClauseContext *> JavaParserLabeled::Statement7Context::catchClause() {
  return getRuleContexts<JavaParserLabeled::CatchClauseContext>();
}

JavaParserLabeled::CatchClauseContext* JavaParserLabeled::Statement7Context::catchClause(size_t i) {
  return getRuleContext<JavaParserLabeled::CatchClauseContext>(i);
}

JavaParserLabeled::FinallyBlockContext* JavaParserLabeled::Statement7Context::finallyBlock() {
  return getRuleContext<JavaParserLabeled::FinallyBlockContext>(0);
}

JavaParserLabeled::Statement7Context::Statement7Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement7Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement7(this);
}
void JavaParserLabeled::Statement7Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement7(this);
}

antlrcpp::Any JavaParserLabeled::Statement7Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement7(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement16Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement16Context::COLON() {
  return getToken(JavaParserLabeled::COLON, 0);
}

JavaParserLabeled::StatementContext* JavaParserLabeled::Statement16Context::statement() {
  return getRuleContext<JavaParserLabeled::StatementContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Statement16Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::Statement16Context::Statement16Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement16Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement16(this);
}
void JavaParserLabeled::Statement16Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement16(this);
}

antlrcpp::Any JavaParserLabeled::Statement16Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement16(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement8Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement8Context::SWITCH() {
  return getToken(JavaParserLabeled::SWITCH, 0);
}

JavaParserLabeled::ParExpressionContext* JavaParserLabeled::Statement8Context::parExpression() {
  return getRuleContext<JavaParserLabeled::ParExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Statement8Context::LBRACE() {
  return getToken(JavaParserLabeled::LBRACE, 0);
}

tree::TerminalNode* JavaParserLabeled::Statement8Context::RBRACE() {
  return getToken(JavaParserLabeled::RBRACE, 0);
}

std::vector<JavaParserLabeled::SwitchBlockStatementGroupContext *> JavaParserLabeled::Statement8Context::switchBlockStatementGroup() {
  return getRuleContexts<JavaParserLabeled::SwitchBlockStatementGroupContext>();
}

JavaParserLabeled::SwitchBlockStatementGroupContext* JavaParserLabeled::Statement8Context::switchBlockStatementGroup(size_t i) {
  return getRuleContext<JavaParserLabeled::SwitchBlockStatementGroupContext>(i);
}

std::vector<JavaParserLabeled::SwitchLabelContext *> JavaParserLabeled::Statement8Context::switchLabel() {
  return getRuleContexts<JavaParserLabeled::SwitchLabelContext>();
}

JavaParserLabeled::SwitchLabelContext* JavaParserLabeled::Statement8Context::switchLabel(size_t i) {
  return getRuleContext<JavaParserLabeled::SwitchLabelContext>(i);
}

JavaParserLabeled::Statement8Context::Statement8Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement8Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement8(this);
}
void JavaParserLabeled::Statement8Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement8(this);
}

antlrcpp::Any JavaParserLabeled::Statement8Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement8(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement5Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement5Context::DO() {
  return getToken(JavaParserLabeled::DO, 0);
}

JavaParserLabeled::StatementContext* JavaParserLabeled::Statement5Context::statement() {
  return getRuleContext<JavaParserLabeled::StatementContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Statement5Context::WHILE() {
  return getToken(JavaParserLabeled::WHILE, 0);
}

JavaParserLabeled::ParExpressionContext* JavaParserLabeled::Statement5Context::parExpression() {
  return getRuleContext<JavaParserLabeled::ParExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Statement5Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::Statement5Context::Statement5Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement5(this);
}
void JavaParserLabeled::Statement5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement5(this);
}

antlrcpp::Any JavaParserLabeled::Statement5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement6Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement6Context::TRY() {
  return getToken(JavaParserLabeled::TRY, 0);
}

JavaParserLabeled::BlockContext* JavaParserLabeled::Statement6Context::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

JavaParserLabeled::FinallyBlockContext* JavaParserLabeled::Statement6Context::finallyBlock() {
  return getRuleContext<JavaParserLabeled::FinallyBlockContext>(0);
}

std::vector<JavaParserLabeled::CatchClauseContext *> JavaParserLabeled::Statement6Context::catchClause() {
  return getRuleContexts<JavaParserLabeled::CatchClauseContext>();
}

JavaParserLabeled::CatchClauseContext* JavaParserLabeled::Statement6Context::catchClause(size_t i) {
  return getRuleContext<JavaParserLabeled::CatchClauseContext>(i);
}

JavaParserLabeled::Statement6Context::Statement6Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement6(this);
}
void JavaParserLabeled::Statement6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement6(this);
}

antlrcpp::Any JavaParserLabeled::Statement6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement3Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement3Context::FOR() {
  return getToken(JavaParserLabeled::FOR, 0);
}

tree::TerminalNode* JavaParserLabeled::Statement3Context::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

JavaParserLabeled::ForControlContext* JavaParserLabeled::Statement3Context::forControl() {
  return getRuleContext<JavaParserLabeled::ForControlContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Statement3Context::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::StatementContext* JavaParserLabeled::Statement3Context::statement() {
  return getRuleContext<JavaParserLabeled::StatementContext>(0);
}

JavaParserLabeled::Statement3Context::Statement3Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement3(this);
}
void JavaParserLabeled::Statement3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement3(this);
}

antlrcpp::Any JavaParserLabeled::Statement3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement4Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement4Context::WHILE() {
  return getToken(JavaParserLabeled::WHILE, 0);
}

JavaParserLabeled::ParExpressionContext* JavaParserLabeled::Statement4Context::parExpression() {
  return getRuleContext<JavaParserLabeled::ParExpressionContext>(0);
}

JavaParserLabeled::StatementContext* JavaParserLabeled::Statement4Context::statement() {
  return getRuleContext<JavaParserLabeled::StatementContext>(0);
}

JavaParserLabeled::Statement4Context::Statement4Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement4(this);
}
void JavaParserLabeled::Statement4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement4(this);
}

antlrcpp::Any JavaParserLabeled::Statement4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement1Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement1Context::ASSERT() {
  return getToken(JavaParserLabeled::ASSERT, 0);
}

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Statement1Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Statement1Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Statement1Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

tree::TerminalNode* JavaParserLabeled::Statement1Context::COLON() {
  return getToken(JavaParserLabeled::COLON, 0);
}

JavaParserLabeled::Statement1Context::Statement1Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement1(this);
}
void JavaParserLabeled::Statement1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement1(this);
}

antlrcpp::Any JavaParserLabeled::Statement1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement2Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement2Context::IF() {
  return getToken(JavaParserLabeled::IF, 0);
}

JavaParserLabeled::ParExpressionContext* JavaParserLabeled::Statement2Context::parExpression() {
  return getRuleContext<JavaParserLabeled::ParExpressionContext>(0);
}

std::vector<JavaParserLabeled::StatementContext *> JavaParserLabeled::Statement2Context::statement() {
  return getRuleContexts<JavaParserLabeled::StatementContext>();
}

JavaParserLabeled::StatementContext* JavaParserLabeled::Statement2Context::statement(size_t i) {
  return getRuleContext<JavaParserLabeled::StatementContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Statement2Context::ELSE() {
  return getToken(JavaParserLabeled::ELSE, 0);
}

JavaParserLabeled::Statement2Context::Statement2Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement2(this);
}
void JavaParserLabeled::Statement2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement2(this);
}

antlrcpp::Any JavaParserLabeled::Statement2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement0Context ------------------------------------------------------------------

JavaParserLabeled::BlockContext* JavaParserLabeled::Statement0Context::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

JavaParserLabeled::Statement0Context::Statement0Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement0(this);
}
void JavaParserLabeled::Statement0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement0(this);
}

antlrcpp::Any JavaParserLabeled::Statement0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement10Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement10Context::RETURN() {
  return getToken(JavaParserLabeled::RETURN, 0);
}

tree::TerminalNode* JavaParserLabeled::Statement10Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Statement10Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

JavaParserLabeled::Statement10Context::Statement10Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement10Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement10(this);
}
void JavaParserLabeled::Statement10Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement10(this);
}

antlrcpp::Any JavaParserLabeled::Statement10Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement10(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Statement11Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Statement11Context::THROW() {
  return getToken(JavaParserLabeled::THROW, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Statement11Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Statement11Context::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}

JavaParserLabeled::Statement11Context::Statement11Context(StatementContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Statement11Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement11(this);
}
void JavaParserLabeled::Statement11Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement11(this);
}

antlrcpp::Any JavaParserLabeled::Statement11Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitStatement11(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::StatementContext* JavaParserLabeled::statement() {
  StatementContext *_localctx = _tracker.createInstance<StatementContext>(_ctx, getState());
  enterRule(_localctx, 136, JavaParserLabeled::RuleStatement);
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
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(860);
      dynamic_cast<Statement0Context *>(_localctx)->blockLabel = block();
      break;
    }

    case 2: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(861);
      match(JavaParserLabeled::ASSERT);
      setState(862);
      expression(0);
      setState(865);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaParserLabeled::COLON) {
        setState(863);
        match(JavaParserLabeled::COLON);
        setState(864);
        expression(0);
      }
      setState(867);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 3: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement2Context>(_localctx));
      enterOuterAlt(_localctx, 3);
      setState(869);
      match(JavaParserLabeled::IF);
      setState(870);
      parExpression();
      setState(871);
      statement();
      setState(874);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 102, _ctx)) {
      case 1: {
        setState(872);
        match(JavaParserLabeled::ELSE);
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
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement3Context>(_localctx));
      enterOuterAlt(_localctx, 4);
      setState(876);
      match(JavaParserLabeled::FOR);
      setState(877);
      match(JavaParserLabeled::LPAREN);
      setState(878);
      forControl();
      setState(879);
      match(JavaParserLabeled::RPAREN);
      setState(880);
      statement();
      break;
    }

    case 5: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement4Context>(_localctx));
      enterOuterAlt(_localctx, 5);
      setState(882);
      match(JavaParserLabeled::WHILE);
      setState(883);
      parExpression();
      setState(884);
      statement();
      break;
    }

    case 6: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement5Context>(_localctx));
      enterOuterAlt(_localctx, 6);
      setState(886);
      match(JavaParserLabeled::DO);
      setState(887);
      statement();
      setState(888);
      match(JavaParserLabeled::WHILE);
      setState(889);
      parExpression();
      setState(890);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 7: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement6Context>(_localctx));
      enterOuterAlt(_localctx, 7);
      setState(892);
      match(JavaParserLabeled::TRY);
      setState(893);
      block();
      setState(903);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case JavaParserLabeled::CATCH: {
          setState(895); 
          _errHandler->sync(this);
          _la = _input->LA(1);
          do {
            setState(894);
            catchClause();
            setState(897); 
            _errHandler->sync(this);
            _la = _input->LA(1);
          } while (_la == JavaParserLabeled::CATCH);
          setState(900);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == JavaParserLabeled::FINALLY) {
            setState(899);
            finallyBlock();
          }
          break;
        }

        case JavaParserLabeled::FINALLY: {
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
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement7Context>(_localctx));
      enterOuterAlt(_localctx, 8);
      setState(905);
      match(JavaParserLabeled::TRY);
      setState(906);
      resourceSpecification();
      setState(907);
      block();
      setState(911);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == JavaParserLabeled::CATCH) {
        setState(908);
        catchClause();
        setState(913);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(915);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaParserLabeled::FINALLY) {
        setState(914);
        finallyBlock();
      }
      break;
    }

    case 9: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement8Context>(_localctx));
      enterOuterAlt(_localctx, 9);
      setState(917);
      match(JavaParserLabeled::SWITCH);
      setState(918);
      parExpression();
      setState(919);
      match(JavaParserLabeled::LBRACE);
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
      while (_la == JavaParserLabeled::CASE

      || _la == JavaParserLabeled::DEFAULT) {
        setState(926);
        switchLabel();
        setState(931);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(932);
      match(JavaParserLabeled::RBRACE);
      break;
    }

    case 10: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement9Context>(_localctx));
      enterOuterAlt(_localctx, 10);
      setState(934);
      match(JavaParserLabeled::SYNCHRONIZED);
      setState(935);
      parExpression();
      setState(936);
      block();
      break;
    }

    case 11: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement10Context>(_localctx));
      enterOuterAlt(_localctx, 11);
      setState(938);
      match(JavaParserLabeled::RETURN);
      setState(940);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
        | (1ULL << JavaParserLabeled::BYTE)
        | (1ULL << JavaParserLabeled::CHAR)
        | (1ULL << JavaParserLabeled::DOUBLE)
        | (1ULL << JavaParserLabeled::FLOAT)
        | (1ULL << JavaParserLabeled::INT)
        | (1ULL << JavaParserLabeled::LONG)
        | (1ULL << JavaParserLabeled::NEW)
        | (1ULL << JavaParserLabeled::SHORT)
        | (1ULL << JavaParserLabeled::SUPER)
        | (1ULL << JavaParserLabeled::THIS)
        | (1ULL << JavaParserLabeled::VOID)
        | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
        | (1ULL << JavaParserLabeled::HEX_LITERAL)
        | (1ULL << JavaParserLabeled::OCT_LITERAL)
        | (1ULL << JavaParserLabeled::BINARY_LITERAL)
        | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
        | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
        | (1ULL << JavaParserLabeled::BOOL_LITERAL)
        | (1ULL << JavaParserLabeled::CHAR_LITERAL)
        | (1ULL << JavaParserLabeled::STRING_LITERAL)
        | (1ULL << JavaParserLabeled::NULL_LITERAL)
        | (1ULL << JavaParserLabeled::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
        | (1ULL << (JavaParserLabeled::BANG - 72))
        | (1ULL << (JavaParserLabeled::TILDE - 72))
        | (1ULL << (JavaParserLabeled::INC - 72))
        | (1ULL << (JavaParserLabeled::DEC - 72))
        | (1ULL << (JavaParserLabeled::ADD - 72))
        | (1ULL << (JavaParserLabeled::SUB - 72))
        | (1ULL << (JavaParserLabeled::AT - 72))
        | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
        setState(939);
        expression(0);
      }
      setState(942);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 12: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement11Context>(_localctx));
      enterOuterAlt(_localctx, 12);
      setState(943);
      match(JavaParserLabeled::THROW);
      setState(944);
      expression(0);
      setState(945);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 13: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement12Context>(_localctx));
      enterOuterAlt(_localctx, 13);
      setState(947);
      match(JavaParserLabeled::BREAK);
      setState(949);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaParserLabeled::IDENTIFIER) {
        setState(948);
        match(JavaParserLabeled::IDENTIFIER);
      }
      setState(951);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 14: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement13Context>(_localctx));
      enterOuterAlt(_localctx, 14);
      setState(952);
      match(JavaParserLabeled::CONTINUE);
      setState(954);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaParserLabeled::IDENTIFIER) {
        setState(953);
        match(JavaParserLabeled::IDENTIFIER);
      }
      setState(956);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 15: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement14Context>(_localctx));
      enterOuterAlt(_localctx, 15);
      setState(957);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 16: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement15Context>(_localctx));
      enterOuterAlt(_localctx, 16);
      setState(958);
      dynamic_cast<Statement15Context *>(_localctx)->statementExpression = expression(0);
      setState(959);
      match(JavaParserLabeled::SEMI);
      break;
    }

    case 17: {
      _localctx = dynamic_cast<StatementContext *>(_tracker.createInstance<JavaParserLabeled::Statement16Context>(_localctx));
      enterOuterAlt(_localctx, 17);
      setState(961);
      dynamic_cast<Statement16Context *>(_localctx)->identifierLabel = match(JavaParserLabeled::IDENTIFIER);
      setState(962);
      match(JavaParserLabeled::COLON);
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

JavaParserLabeled::CatchClauseContext::CatchClauseContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::CatchClauseContext::CATCH() {
  return getToken(JavaParserLabeled::CATCH, 0);
}

tree::TerminalNode* JavaParserLabeled::CatchClauseContext::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

JavaParserLabeled::CatchTypeContext* JavaParserLabeled::CatchClauseContext::catchType() {
  return getRuleContext<JavaParserLabeled::CatchTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::CatchClauseContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

tree::TerminalNode* JavaParserLabeled::CatchClauseContext::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::BlockContext* JavaParserLabeled::CatchClauseContext::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

std::vector<JavaParserLabeled::VariableModifierContext *> JavaParserLabeled::CatchClauseContext::variableModifier() {
  return getRuleContexts<JavaParserLabeled::VariableModifierContext>();
}

JavaParserLabeled::VariableModifierContext* JavaParserLabeled::CatchClauseContext::variableModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::VariableModifierContext>(i);
}


size_t JavaParserLabeled::CatchClauseContext::getRuleIndex() const {
  return JavaParserLabeled::RuleCatchClause;
}

void JavaParserLabeled::CatchClauseContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCatchClause(this);
}

void JavaParserLabeled::CatchClauseContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCatchClause(this);
}


antlrcpp::Any JavaParserLabeled::CatchClauseContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitCatchClause(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::CatchClauseContext* JavaParserLabeled::catchClause() {
  CatchClauseContext *_localctx = _tracker.createInstance<CatchClauseContext>(_ctx, getState());
  enterRule(_localctx, 138, JavaParserLabeled::RuleCatchClause);

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
    match(JavaParserLabeled::CATCH);
    setState(967);
    match(JavaParserLabeled::LPAREN);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(976);
    match(JavaParserLabeled::RPAREN);
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

JavaParserLabeled::CatchTypeContext::CatchTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::QualifiedNameContext *> JavaParserLabeled::CatchTypeContext::qualifiedName() {
  return getRuleContexts<JavaParserLabeled::QualifiedNameContext>();
}

JavaParserLabeled::QualifiedNameContext* JavaParserLabeled::CatchTypeContext::qualifiedName(size_t i) {
  return getRuleContext<JavaParserLabeled::QualifiedNameContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::CatchTypeContext::BITOR() {
  return getTokens(JavaParserLabeled::BITOR);
}

tree::TerminalNode* JavaParserLabeled::CatchTypeContext::BITOR(size_t i) {
  return getToken(JavaParserLabeled::BITOR, i);
}


size_t JavaParserLabeled::CatchTypeContext::getRuleIndex() const {
  return JavaParserLabeled::RuleCatchType;
}

void JavaParserLabeled::CatchTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCatchType(this);
}

void JavaParserLabeled::CatchTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCatchType(this);
}


antlrcpp::Any JavaParserLabeled::CatchTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitCatchType(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::CatchTypeContext* JavaParserLabeled::catchType() {
  CatchTypeContext *_localctx = _tracker.createInstance<CatchTypeContext>(_ctx, getState());
  enterRule(_localctx, 140, JavaParserLabeled::RuleCatchType);
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
    while (_la == JavaParserLabeled::BITOR) {
      setState(980);
      match(JavaParserLabeled::BITOR);
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

JavaParserLabeled::FinallyBlockContext::FinallyBlockContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::FinallyBlockContext::FINALLY() {
  return getToken(JavaParserLabeled::FINALLY, 0);
}

JavaParserLabeled::BlockContext* JavaParserLabeled::FinallyBlockContext::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}


size_t JavaParserLabeled::FinallyBlockContext::getRuleIndex() const {
  return JavaParserLabeled::RuleFinallyBlock;
}

void JavaParserLabeled::FinallyBlockContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFinallyBlock(this);
}

void JavaParserLabeled::FinallyBlockContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFinallyBlock(this);
}


antlrcpp::Any JavaParserLabeled::FinallyBlockContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitFinallyBlock(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::FinallyBlockContext* JavaParserLabeled::finallyBlock() {
  FinallyBlockContext *_localctx = _tracker.createInstance<FinallyBlockContext>(_ctx, getState());
  enterRule(_localctx, 142, JavaParserLabeled::RuleFinallyBlock);

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
    match(JavaParserLabeled::FINALLY);
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

JavaParserLabeled::ResourceSpecificationContext::ResourceSpecificationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ResourceSpecificationContext::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

JavaParserLabeled::ResourcesContext* JavaParserLabeled::ResourceSpecificationContext::resources() {
  return getRuleContext<JavaParserLabeled::ResourcesContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ResourceSpecificationContext::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::ResourceSpecificationContext::SEMI() {
  return getToken(JavaParserLabeled::SEMI, 0);
}


size_t JavaParserLabeled::ResourceSpecificationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleResourceSpecification;
}

void JavaParserLabeled::ResourceSpecificationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterResourceSpecification(this);
}

void JavaParserLabeled::ResourceSpecificationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitResourceSpecification(this);
}


antlrcpp::Any JavaParserLabeled::ResourceSpecificationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitResourceSpecification(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ResourceSpecificationContext* JavaParserLabeled::resourceSpecification() {
  ResourceSpecificationContext *_localctx = _tracker.createInstance<ResourceSpecificationContext>(_ctx, getState());
  enterRule(_localctx, 144, JavaParserLabeled::RuleResourceSpecification);
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
    match(JavaParserLabeled::LPAREN);
    setState(991);
    resources();
    setState(993);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::SEMI) {
      setState(992);
      match(JavaParserLabeled::SEMI);
    }
    setState(995);
    match(JavaParserLabeled::RPAREN);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ResourcesContext ------------------------------------------------------------------

JavaParserLabeled::ResourcesContext::ResourcesContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::ResourceContext *> JavaParserLabeled::ResourcesContext::resource() {
  return getRuleContexts<JavaParserLabeled::ResourceContext>();
}

JavaParserLabeled::ResourceContext* JavaParserLabeled::ResourcesContext::resource(size_t i) {
  return getRuleContext<JavaParserLabeled::ResourceContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ResourcesContext::SEMI() {
  return getTokens(JavaParserLabeled::SEMI);
}

tree::TerminalNode* JavaParserLabeled::ResourcesContext::SEMI(size_t i) {
  return getToken(JavaParserLabeled::SEMI, i);
}


size_t JavaParserLabeled::ResourcesContext::getRuleIndex() const {
  return JavaParserLabeled::RuleResources;
}

void JavaParserLabeled::ResourcesContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterResources(this);
}

void JavaParserLabeled::ResourcesContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitResources(this);
}


antlrcpp::Any JavaParserLabeled::ResourcesContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitResources(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ResourcesContext* JavaParserLabeled::resources() {
  ResourcesContext *_localctx = _tracker.createInstance<ResourcesContext>(_ctx, getState());
  enterRule(_localctx, 146, JavaParserLabeled::RuleResources);

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
        match(JavaParserLabeled::SEMI);
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

JavaParserLabeled::ResourceContext::ResourceContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::ClassOrInterfaceTypeContext* JavaParserLabeled::ResourceContext::classOrInterfaceType() {
  return getRuleContext<JavaParserLabeled::ClassOrInterfaceTypeContext>(0);
}

JavaParserLabeled::VariableDeclaratorIdContext* JavaParserLabeled::ResourceContext::variableDeclaratorId() {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorIdContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ResourceContext::ASSIGN() {
  return getToken(JavaParserLabeled::ASSIGN, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::ResourceContext::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

std::vector<JavaParserLabeled::VariableModifierContext *> JavaParserLabeled::ResourceContext::variableModifier() {
  return getRuleContexts<JavaParserLabeled::VariableModifierContext>();
}

JavaParserLabeled::VariableModifierContext* JavaParserLabeled::ResourceContext::variableModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::VariableModifierContext>(i);
}


size_t JavaParserLabeled::ResourceContext::getRuleIndex() const {
  return JavaParserLabeled::RuleResource;
}

void JavaParserLabeled::ResourceContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterResource(this);
}

void JavaParserLabeled::ResourceContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitResource(this);
}


antlrcpp::Any JavaParserLabeled::ResourceContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitResource(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ResourceContext* JavaParserLabeled::resource() {
  ResourceContext *_localctx = _tracker.createInstance<ResourceContext>(_ctx, getState());
  enterRule(_localctx, 148, JavaParserLabeled::RuleResource);

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
    match(JavaParserLabeled::ASSIGN);
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

JavaParserLabeled::SwitchBlockStatementGroupContext::SwitchBlockStatementGroupContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::SwitchLabelContext *> JavaParserLabeled::SwitchBlockStatementGroupContext::switchLabel() {
  return getRuleContexts<JavaParserLabeled::SwitchLabelContext>();
}

JavaParserLabeled::SwitchLabelContext* JavaParserLabeled::SwitchBlockStatementGroupContext::switchLabel(size_t i) {
  return getRuleContext<JavaParserLabeled::SwitchLabelContext>(i);
}

std::vector<JavaParserLabeled::BlockStatementContext *> JavaParserLabeled::SwitchBlockStatementGroupContext::blockStatement() {
  return getRuleContexts<JavaParserLabeled::BlockStatementContext>();
}

JavaParserLabeled::BlockStatementContext* JavaParserLabeled::SwitchBlockStatementGroupContext::blockStatement(size_t i) {
  return getRuleContext<JavaParserLabeled::BlockStatementContext>(i);
}


size_t JavaParserLabeled::SwitchBlockStatementGroupContext::getRuleIndex() const {
  return JavaParserLabeled::RuleSwitchBlockStatementGroup;
}

void JavaParserLabeled::SwitchBlockStatementGroupContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSwitchBlockStatementGroup(this);
}

void JavaParserLabeled::SwitchBlockStatementGroupContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSwitchBlockStatementGroup(this);
}


antlrcpp::Any JavaParserLabeled::SwitchBlockStatementGroupContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitSwitchBlockStatementGroup(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::SwitchBlockStatementGroupContext* JavaParserLabeled::switchBlockStatementGroup() {
  SwitchBlockStatementGroupContext *_localctx = _tracker.createInstance<SwitchBlockStatementGroupContext>(_ctx, getState());
  enterRule(_localctx, 150, JavaParserLabeled::RuleSwitchBlockStatementGroup);
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
    } while (_la == JavaParserLabeled::CASE

    || _la == JavaParserLabeled::DEFAULT);
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
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::ABSTRACT)
      | (1ULL << JavaParserLabeled::ASSERT)
      | (1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BREAK)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::CLASS)
      | (1ULL << JavaParserLabeled::CONTINUE)
      | (1ULL << JavaParserLabeled::DO)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::FINAL)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::FOR)
      | (1ULL << JavaParserLabeled::IF)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::INTERFACE)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NEW)
      | (1ULL << JavaParserLabeled::PRIVATE)
      | (1ULL << JavaParserLabeled::PROTECTED)
      | (1ULL << JavaParserLabeled::PUBLIC)
      | (1ULL << JavaParserLabeled::RETURN)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::STATIC)
      | (1ULL << JavaParserLabeled::STRICTFP)
      | (1ULL << JavaParserLabeled::SUPER)
      | (1ULL << JavaParserLabeled::SWITCH)
      | (1ULL << JavaParserLabeled::SYNCHRONIZED)
      | (1ULL << JavaParserLabeled::THIS)
      | (1ULL << JavaParserLabeled::THROW)
      | (1ULL << JavaParserLabeled::TRY)
      | (1ULL << JavaParserLabeled::VOID)
      | (1ULL << JavaParserLabeled::WHILE)
      | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_LITERAL)
      | (1ULL << JavaParserLabeled::OCT_LITERAL)
      | (1ULL << JavaParserLabeled::BINARY_LITERAL)
      | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::BOOL_LITERAL)
      | (1ULL << JavaParserLabeled::CHAR_LITERAL)
      | (1ULL << JavaParserLabeled::STRING_LITERAL)
      | (1ULL << JavaParserLabeled::NULL_LITERAL)
      | (1ULL << JavaParserLabeled::LPAREN)
      | (1ULL << JavaParserLabeled::LBRACE))) != 0) || ((((_la - 67) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 67)) & ((1ULL << (JavaParserLabeled::SEMI - 67))
      | (1ULL << (JavaParserLabeled::LT - 67))
      | (1ULL << (JavaParserLabeled::BANG - 67))
      | (1ULL << (JavaParserLabeled::TILDE - 67))
      | (1ULL << (JavaParserLabeled::INC - 67))
      | (1ULL << (JavaParserLabeled::DEC - 67))
      | (1ULL << (JavaParserLabeled::ADD - 67))
      | (1ULL << (JavaParserLabeled::SUB - 67))
      | (1ULL << (JavaParserLabeled::AT - 67))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 67)))) != 0));
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SwitchLabelContext ------------------------------------------------------------------

JavaParserLabeled::SwitchLabelContext::SwitchLabelContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::SwitchLabelContext::CASE() {
  return getToken(JavaParserLabeled::CASE, 0);
}

tree::TerminalNode* JavaParserLabeled::SwitchLabelContext::COLON() {
  return getToken(JavaParserLabeled::COLON, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::SwitchLabelContext::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::SwitchLabelContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

tree::TerminalNode* JavaParserLabeled::SwitchLabelContext::DEFAULT() {
  return getToken(JavaParserLabeled::DEFAULT, 0);
}


size_t JavaParserLabeled::SwitchLabelContext::getRuleIndex() const {
  return JavaParserLabeled::RuleSwitchLabel;
}

void JavaParserLabeled::SwitchLabelContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSwitchLabel(this);
}

void JavaParserLabeled::SwitchLabelContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSwitchLabel(this);
}


antlrcpp::Any JavaParserLabeled::SwitchLabelContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitSwitchLabel(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::SwitchLabelContext* JavaParserLabeled::switchLabel() {
  SwitchLabelContext *_localctx = _tracker.createInstance<SwitchLabelContext>(_ctx, getState());
  enterRule(_localctx, 152, JavaParserLabeled::RuleSwitchLabel);

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
      case JavaParserLabeled::CASE: {
        enterOuterAlt(_localctx, 1);
        setState(1026);
        match(JavaParserLabeled::CASE);
        setState(1029);
        _errHandler->sync(this);
        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 121, _ctx)) {
        case 1: {
          setState(1027);
          dynamic_cast<SwitchLabelContext *>(_localctx)->constantExpression = expression(0);
          break;
        }

        case 2: {
          setState(1028);
          dynamic_cast<SwitchLabelContext *>(_localctx)->enumConstantName = match(JavaParserLabeled::IDENTIFIER);
          break;
        }

        default:
          break;
        }
        setState(1031);
        match(JavaParserLabeled::COLON);
        break;
      }

      case JavaParserLabeled::DEFAULT: {
        enterOuterAlt(_localctx, 2);
        setState(1032);
        match(JavaParserLabeled::DEFAULT);
        setState(1033);
        match(JavaParserLabeled::COLON);
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

JavaParserLabeled::ForControlContext::ForControlContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::ForControlContext::getRuleIndex() const {
  return JavaParserLabeled::RuleForControl;
}

void JavaParserLabeled::ForControlContext::copyFrom(ForControlContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ForControl0Context ------------------------------------------------------------------

JavaParserLabeled::EnhancedForControlContext* JavaParserLabeled::ForControl0Context::enhancedForControl() {
  return getRuleContext<JavaParserLabeled::EnhancedForControlContext>(0);
}

JavaParserLabeled::ForControl0Context::ForControl0Context(ForControlContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ForControl0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterForControl0(this);
}
void JavaParserLabeled::ForControl0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitForControl0(this);
}

antlrcpp::Any JavaParserLabeled::ForControl0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitForControl0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ForControl1Context ------------------------------------------------------------------

std::vector<tree::TerminalNode *> JavaParserLabeled::ForControl1Context::SEMI() {
  return getTokens(JavaParserLabeled::SEMI);
}

tree::TerminalNode* JavaParserLabeled::ForControl1Context::SEMI(size_t i) {
  return getToken(JavaParserLabeled::SEMI, i);
}

JavaParserLabeled::ForInitContext* JavaParserLabeled::ForControl1Context::forInit() {
  return getRuleContext<JavaParserLabeled::ForInitContext>(0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::ForControl1Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

JavaParserLabeled::ExpressionListContext* JavaParserLabeled::ForControl1Context::expressionList() {
  return getRuleContext<JavaParserLabeled::ExpressionListContext>(0);
}

JavaParserLabeled::ForControl1Context::ForControl1Context(ForControlContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ForControl1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterForControl1(this);
}
void JavaParserLabeled::ForControl1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitForControl1(this);
}

antlrcpp::Any JavaParserLabeled::ForControl1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitForControl1(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::ForControlContext* JavaParserLabeled::forControl() {
  ForControlContext *_localctx = _tracker.createInstance<ForControlContext>(_ctx, getState());
  enterRule(_localctx, 154, JavaParserLabeled::RuleForControl);
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
      _localctx = dynamic_cast<ForControlContext *>(_tracker.createInstance<JavaParserLabeled::ForControl0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(1036);
      enhancedForControl();
      break;
    }

    case 2: {
      _localctx = dynamic_cast<ForControlContext *>(_tracker.createInstance<JavaParserLabeled::ForControl1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(1038);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
        | (1ULL << JavaParserLabeled::BYTE)
        | (1ULL << JavaParserLabeled::CHAR)
        | (1ULL << JavaParserLabeled::DOUBLE)
        | (1ULL << JavaParserLabeled::FINAL)
        | (1ULL << JavaParserLabeled::FLOAT)
        | (1ULL << JavaParserLabeled::INT)
        | (1ULL << JavaParserLabeled::LONG)
        | (1ULL << JavaParserLabeled::NEW)
        | (1ULL << JavaParserLabeled::SHORT)
        | (1ULL << JavaParserLabeled::SUPER)
        | (1ULL << JavaParserLabeled::THIS)
        | (1ULL << JavaParserLabeled::VOID)
        | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
        | (1ULL << JavaParserLabeled::HEX_LITERAL)
        | (1ULL << JavaParserLabeled::OCT_LITERAL)
        | (1ULL << JavaParserLabeled::BINARY_LITERAL)
        | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
        | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
        | (1ULL << JavaParserLabeled::BOOL_LITERAL)
        | (1ULL << JavaParserLabeled::CHAR_LITERAL)
        | (1ULL << JavaParserLabeled::STRING_LITERAL)
        | (1ULL << JavaParserLabeled::NULL_LITERAL)
        | (1ULL << JavaParserLabeled::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
        | (1ULL << (JavaParserLabeled::BANG - 72))
        | (1ULL << (JavaParserLabeled::TILDE - 72))
        | (1ULL << (JavaParserLabeled::INC - 72))
        | (1ULL << (JavaParserLabeled::DEC - 72))
        | (1ULL << (JavaParserLabeled::ADD - 72))
        | (1ULL << (JavaParserLabeled::SUB - 72))
        | (1ULL << (JavaParserLabeled::AT - 72))
        | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
        setState(1037);
        forInit();
      }
      setState(1040);
      match(JavaParserLabeled::SEMI);
      setState(1042);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
        | (1ULL << JavaParserLabeled::BYTE)
        | (1ULL << JavaParserLabeled::CHAR)
        | (1ULL << JavaParserLabeled::DOUBLE)
        | (1ULL << JavaParserLabeled::FLOAT)
        | (1ULL << JavaParserLabeled::INT)
        | (1ULL << JavaParserLabeled::LONG)
        | (1ULL << JavaParserLabeled::NEW)
        | (1ULL << JavaParserLabeled::SHORT)
        | (1ULL << JavaParserLabeled::SUPER)
        | (1ULL << JavaParserLabeled::THIS)
        | (1ULL << JavaParserLabeled::VOID)
        | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
        | (1ULL << JavaParserLabeled::HEX_LITERAL)
        | (1ULL << JavaParserLabeled::OCT_LITERAL)
        | (1ULL << JavaParserLabeled::BINARY_LITERAL)
        | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
        | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
        | (1ULL << JavaParserLabeled::BOOL_LITERAL)
        | (1ULL << JavaParserLabeled::CHAR_LITERAL)
        | (1ULL << JavaParserLabeled::STRING_LITERAL)
        | (1ULL << JavaParserLabeled::NULL_LITERAL)
        | (1ULL << JavaParserLabeled::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
        | (1ULL << (JavaParserLabeled::BANG - 72))
        | (1ULL << (JavaParserLabeled::TILDE - 72))
        | (1ULL << (JavaParserLabeled::INC - 72))
        | (1ULL << (JavaParserLabeled::DEC - 72))
        | (1ULL << (JavaParserLabeled::ADD - 72))
        | (1ULL << (JavaParserLabeled::SUB - 72))
        | (1ULL << (JavaParserLabeled::AT - 72))
        | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
        setState(1041);
        expression(0);
      }
      setState(1044);
      match(JavaParserLabeled::SEMI);
      setState(1046);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
        | (1ULL << JavaParserLabeled::BYTE)
        | (1ULL << JavaParserLabeled::CHAR)
        | (1ULL << JavaParserLabeled::DOUBLE)
        | (1ULL << JavaParserLabeled::FLOAT)
        | (1ULL << JavaParserLabeled::INT)
        | (1ULL << JavaParserLabeled::LONG)
        | (1ULL << JavaParserLabeled::NEW)
        | (1ULL << JavaParserLabeled::SHORT)
        | (1ULL << JavaParserLabeled::SUPER)
        | (1ULL << JavaParserLabeled::THIS)
        | (1ULL << JavaParserLabeled::VOID)
        | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
        | (1ULL << JavaParserLabeled::HEX_LITERAL)
        | (1ULL << JavaParserLabeled::OCT_LITERAL)
        | (1ULL << JavaParserLabeled::BINARY_LITERAL)
        | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
        | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
        | (1ULL << JavaParserLabeled::BOOL_LITERAL)
        | (1ULL << JavaParserLabeled::CHAR_LITERAL)
        | (1ULL << JavaParserLabeled::STRING_LITERAL)
        | (1ULL << JavaParserLabeled::NULL_LITERAL)
        | (1ULL << JavaParserLabeled::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
        | (1ULL << (JavaParserLabeled::BANG - 72))
        | (1ULL << (JavaParserLabeled::TILDE - 72))
        | (1ULL << (JavaParserLabeled::INC - 72))
        | (1ULL << (JavaParserLabeled::DEC - 72))
        | (1ULL << (JavaParserLabeled::ADD - 72))
        | (1ULL << (JavaParserLabeled::SUB - 72))
        | (1ULL << (JavaParserLabeled::AT - 72))
        | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
        setState(1045);
        dynamic_cast<ForControl1Context *>(_localctx)->forUpdate = expressionList();
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

JavaParserLabeled::ForInitContext::ForInitContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::ForInitContext::getRuleIndex() const {
  return JavaParserLabeled::RuleForInit;
}

void JavaParserLabeled::ForInitContext::copyFrom(ForInitContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ForInit1Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionListContext* JavaParserLabeled::ForInit1Context::expressionList() {
  return getRuleContext<JavaParserLabeled::ExpressionListContext>(0);
}

JavaParserLabeled::ForInit1Context::ForInit1Context(ForInitContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ForInit1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterForInit1(this);
}
void JavaParserLabeled::ForInit1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitForInit1(this);
}

antlrcpp::Any JavaParserLabeled::ForInit1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitForInit1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ForInit0Context ------------------------------------------------------------------

JavaParserLabeled::LocalVariableDeclarationContext* JavaParserLabeled::ForInit0Context::localVariableDeclaration() {
  return getRuleContext<JavaParserLabeled::LocalVariableDeclarationContext>(0);
}

JavaParserLabeled::ForInit0Context::ForInit0Context(ForInitContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ForInit0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterForInit0(this);
}
void JavaParserLabeled::ForInit0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitForInit0(this);
}

antlrcpp::Any JavaParserLabeled::ForInit0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitForInit0(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::ForInitContext* JavaParserLabeled::forInit() {
  ForInitContext *_localctx = _tracker.createInstance<ForInitContext>(_ctx, getState());
  enterRule(_localctx, 156, JavaParserLabeled::RuleForInit);

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
      _localctx = dynamic_cast<ForInitContext *>(_tracker.createInstance<JavaParserLabeled::ForInit0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(1050);
      localVariableDeclaration();
      break;
    }

    case 2: {
      _localctx = dynamic_cast<ForInitContext *>(_tracker.createInstance<JavaParserLabeled::ForInit1Context>(_localctx));
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

JavaParserLabeled::EnhancedForControlContext::EnhancedForControlContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::EnhancedForControlContext::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

JavaParserLabeled::VariableDeclaratorIdContext* JavaParserLabeled::EnhancedForControlContext::variableDeclaratorId() {
  return getRuleContext<JavaParserLabeled::VariableDeclaratorIdContext>(0);
}

tree::TerminalNode* JavaParserLabeled::EnhancedForControlContext::COLON() {
  return getToken(JavaParserLabeled::COLON, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::EnhancedForControlContext::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

std::vector<JavaParserLabeled::VariableModifierContext *> JavaParserLabeled::EnhancedForControlContext::variableModifier() {
  return getRuleContexts<JavaParserLabeled::VariableModifierContext>();
}

JavaParserLabeled::VariableModifierContext* JavaParserLabeled::EnhancedForControlContext::variableModifier(size_t i) {
  return getRuleContext<JavaParserLabeled::VariableModifierContext>(i);
}


size_t JavaParserLabeled::EnhancedForControlContext::getRuleIndex() const {
  return JavaParserLabeled::RuleEnhancedForControl;
}

void JavaParserLabeled::EnhancedForControlContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterEnhancedForControl(this);
}

void JavaParserLabeled::EnhancedForControlContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitEnhancedForControl(this);
}


antlrcpp::Any JavaParserLabeled::EnhancedForControlContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitEnhancedForControl(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::EnhancedForControlContext* JavaParserLabeled::enhancedForControl() {
  EnhancedForControlContext *_localctx = _tracker.createInstance<EnhancedForControlContext>(_ctx, getState());
  enterRule(_localctx, 158, JavaParserLabeled::RuleEnhancedForControl);

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
    match(JavaParserLabeled::COLON);
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

JavaParserLabeled::ParExpressionContext::ParExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ParExpressionContext::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::ParExpressionContext::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ParExpressionContext::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}


size_t JavaParserLabeled::ParExpressionContext::getRuleIndex() const {
  return JavaParserLabeled::RuleParExpression;
}

void JavaParserLabeled::ParExpressionContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterParExpression(this);
}

void JavaParserLabeled::ParExpressionContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitParExpression(this);
}


antlrcpp::Any JavaParserLabeled::ParExpressionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitParExpression(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ParExpressionContext* JavaParserLabeled::parExpression() {
  ParExpressionContext *_localctx = _tracker.createInstance<ParExpressionContext>(_ctx, getState());
  enterRule(_localctx, 160, JavaParserLabeled::RuleParExpression);

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
    match(JavaParserLabeled::LPAREN);
    setState(1066);
    expression(0);
    setState(1067);
    match(JavaParserLabeled::RPAREN);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExpressionListContext ------------------------------------------------------------------

JavaParserLabeled::ExpressionListContext::ExpressionListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::ExpressionListContext::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::ExpressionListContext::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ExpressionListContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::ExpressionListContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::ExpressionListContext::getRuleIndex() const {
  return JavaParserLabeled::RuleExpressionList;
}

void JavaParserLabeled::ExpressionListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpressionList(this);
}

void JavaParserLabeled::ExpressionListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpressionList(this);
}


antlrcpp::Any JavaParserLabeled::ExpressionListContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpressionList(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ExpressionListContext* JavaParserLabeled::expressionList() {
  ExpressionListContext *_localctx = _tracker.createInstance<ExpressionListContext>(_ctx, getState());
  enterRule(_localctx, 162, JavaParserLabeled::RuleExpressionList);
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
    while (_la == JavaParserLabeled::COMMA) {
      setState(1070);
      match(JavaParserLabeled::COMMA);
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

JavaParserLabeled::MethodCallContext::MethodCallContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::MethodCallContext::getRuleIndex() const {
  return JavaParserLabeled::RuleMethodCall;
}

void JavaParserLabeled::MethodCallContext::copyFrom(MethodCallContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- MethodCall0Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::MethodCall0Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

tree::TerminalNode* JavaParserLabeled::MethodCall0Context::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::MethodCall0Context::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::ExpressionListContext* JavaParserLabeled::MethodCall0Context::expressionList() {
  return getRuleContext<JavaParserLabeled::ExpressionListContext>(0);
}

JavaParserLabeled::MethodCall0Context::MethodCall0Context(MethodCallContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MethodCall0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodCall0(this);
}
void JavaParserLabeled::MethodCall0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodCall0(this);
}

antlrcpp::Any JavaParserLabeled::MethodCall0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMethodCall0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MethodCall1Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::MethodCall1Context::THIS() {
  return getToken(JavaParserLabeled::THIS, 0);
}

tree::TerminalNode* JavaParserLabeled::MethodCall1Context::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::MethodCall1Context::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::ExpressionListContext* JavaParserLabeled::MethodCall1Context::expressionList() {
  return getRuleContext<JavaParserLabeled::ExpressionListContext>(0);
}

JavaParserLabeled::MethodCall1Context::MethodCall1Context(MethodCallContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MethodCall1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodCall1(this);
}
void JavaParserLabeled::MethodCall1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodCall1(this);
}

antlrcpp::Any JavaParserLabeled::MethodCall1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMethodCall1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MethodCall2Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::MethodCall2Context::SUPER() {
  return getToken(JavaParserLabeled::SUPER, 0);
}

tree::TerminalNode* JavaParserLabeled::MethodCall2Context::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::MethodCall2Context::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::ExpressionListContext* JavaParserLabeled::MethodCall2Context::expressionList() {
  return getRuleContext<JavaParserLabeled::ExpressionListContext>(0);
}

JavaParserLabeled::MethodCall2Context::MethodCall2Context(MethodCallContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::MethodCall2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterMethodCall2(this);
}
void JavaParserLabeled::MethodCall2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitMethodCall2(this);
}

antlrcpp::Any JavaParserLabeled::MethodCall2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitMethodCall2(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::MethodCallContext* JavaParserLabeled::methodCall() {
  MethodCallContext *_localctx = _tracker.createInstance<MethodCallContext>(_ctx, getState());
  enterRule(_localctx, 164, JavaParserLabeled::RuleMethodCall);
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
      case JavaParserLabeled::IDENTIFIER: {
        _localctx = dynamic_cast<MethodCallContext *>(_tracker.createInstance<JavaParserLabeled::MethodCall0Context>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(1077);
        match(JavaParserLabeled::IDENTIFIER);
        setState(1078);
        match(JavaParserLabeled::LPAREN);
        setState(1080);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
          | (1ULL << JavaParserLabeled::BYTE)
          | (1ULL << JavaParserLabeled::CHAR)
          | (1ULL << JavaParserLabeled::DOUBLE)
          | (1ULL << JavaParserLabeled::FLOAT)
          | (1ULL << JavaParserLabeled::INT)
          | (1ULL << JavaParserLabeled::LONG)
          | (1ULL << JavaParserLabeled::NEW)
          | (1ULL << JavaParserLabeled::SHORT)
          | (1ULL << JavaParserLabeled::SUPER)
          | (1ULL << JavaParserLabeled::THIS)
          | (1ULL << JavaParserLabeled::VOID)
          | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
          | (1ULL << JavaParserLabeled::HEX_LITERAL)
          | (1ULL << JavaParserLabeled::OCT_LITERAL)
          | (1ULL << JavaParserLabeled::BINARY_LITERAL)
          | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
          | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
          | (1ULL << JavaParserLabeled::BOOL_LITERAL)
          | (1ULL << JavaParserLabeled::CHAR_LITERAL)
          | (1ULL << JavaParserLabeled::STRING_LITERAL)
          | (1ULL << JavaParserLabeled::NULL_LITERAL)
          | (1ULL << JavaParserLabeled::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
          ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
          | (1ULL << (JavaParserLabeled::BANG - 72))
          | (1ULL << (JavaParserLabeled::TILDE - 72))
          | (1ULL << (JavaParserLabeled::INC - 72))
          | (1ULL << (JavaParserLabeled::DEC - 72))
          | (1ULL << (JavaParserLabeled::ADD - 72))
          | (1ULL << (JavaParserLabeled::SUB - 72))
          | (1ULL << (JavaParserLabeled::AT - 72))
          | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
          setState(1079);
          expressionList();
        }
        setState(1082);
        match(JavaParserLabeled::RPAREN);
        break;
      }

      case JavaParserLabeled::THIS: {
        _localctx = dynamic_cast<MethodCallContext *>(_tracker.createInstance<JavaParserLabeled::MethodCall1Context>(_localctx));
        enterOuterAlt(_localctx, 2);
        setState(1083);
        match(JavaParserLabeled::THIS);
        setState(1084);
        match(JavaParserLabeled::LPAREN);
        setState(1086);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
          | (1ULL << JavaParserLabeled::BYTE)
          | (1ULL << JavaParserLabeled::CHAR)
          | (1ULL << JavaParserLabeled::DOUBLE)
          | (1ULL << JavaParserLabeled::FLOAT)
          | (1ULL << JavaParserLabeled::INT)
          | (1ULL << JavaParserLabeled::LONG)
          | (1ULL << JavaParserLabeled::NEW)
          | (1ULL << JavaParserLabeled::SHORT)
          | (1ULL << JavaParserLabeled::SUPER)
          | (1ULL << JavaParserLabeled::THIS)
          | (1ULL << JavaParserLabeled::VOID)
          | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
          | (1ULL << JavaParserLabeled::HEX_LITERAL)
          | (1ULL << JavaParserLabeled::OCT_LITERAL)
          | (1ULL << JavaParserLabeled::BINARY_LITERAL)
          | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
          | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
          | (1ULL << JavaParserLabeled::BOOL_LITERAL)
          | (1ULL << JavaParserLabeled::CHAR_LITERAL)
          | (1ULL << JavaParserLabeled::STRING_LITERAL)
          | (1ULL << JavaParserLabeled::NULL_LITERAL)
          | (1ULL << JavaParserLabeled::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
          ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
          | (1ULL << (JavaParserLabeled::BANG - 72))
          | (1ULL << (JavaParserLabeled::TILDE - 72))
          | (1ULL << (JavaParserLabeled::INC - 72))
          | (1ULL << (JavaParserLabeled::DEC - 72))
          | (1ULL << (JavaParserLabeled::ADD - 72))
          | (1ULL << (JavaParserLabeled::SUB - 72))
          | (1ULL << (JavaParserLabeled::AT - 72))
          | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
          setState(1085);
          expressionList();
        }
        setState(1088);
        match(JavaParserLabeled::RPAREN);
        break;
      }

      case JavaParserLabeled::SUPER: {
        _localctx = dynamic_cast<MethodCallContext *>(_tracker.createInstance<JavaParserLabeled::MethodCall2Context>(_localctx));
        enterOuterAlt(_localctx, 3);
        setState(1089);
        match(JavaParserLabeled::SUPER);
        setState(1090);
        match(JavaParserLabeled::LPAREN);
        setState(1092);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
          | (1ULL << JavaParserLabeled::BYTE)
          | (1ULL << JavaParserLabeled::CHAR)
          | (1ULL << JavaParserLabeled::DOUBLE)
          | (1ULL << JavaParserLabeled::FLOAT)
          | (1ULL << JavaParserLabeled::INT)
          | (1ULL << JavaParserLabeled::LONG)
          | (1ULL << JavaParserLabeled::NEW)
          | (1ULL << JavaParserLabeled::SHORT)
          | (1ULL << JavaParserLabeled::SUPER)
          | (1ULL << JavaParserLabeled::THIS)
          | (1ULL << JavaParserLabeled::VOID)
          | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
          | (1ULL << JavaParserLabeled::HEX_LITERAL)
          | (1ULL << JavaParserLabeled::OCT_LITERAL)
          | (1ULL << JavaParserLabeled::BINARY_LITERAL)
          | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
          | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
          | (1ULL << JavaParserLabeled::BOOL_LITERAL)
          | (1ULL << JavaParserLabeled::CHAR_LITERAL)
          | (1ULL << JavaParserLabeled::STRING_LITERAL)
          | (1ULL << JavaParserLabeled::NULL_LITERAL)
          | (1ULL << JavaParserLabeled::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
          ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
          | (1ULL << (JavaParserLabeled::BANG - 72))
          | (1ULL << (JavaParserLabeled::TILDE - 72))
          | (1ULL << (JavaParserLabeled::INC - 72))
          | (1ULL << (JavaParserLabeled::DEC - 72))
          | (1ULL << (JavaParserLabeled::ADD - 72))
          | (1ULL << (JavaParserLabeled::SUB - 72))
          | (1ULL << (JavaParserLabeled::AT - 72))
          | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
          setState(1091);
          expressionList();
        }
        setState(1094);
        match(JavaParserLabeled::RPAREN);
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

JavaParserLabeled::ExpressionContext::ExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::ExpressionContext::getRuleIndex() const {
  return JavaParserLabeled::RuleExpression;
}

void JavaParserLabeled::ExpressionContext::copyFrom(ExpressionContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Expression8Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression8Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression8Context::TILDE() {
  return getToken(JavaParserLabeled::TILDE, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression8Context::BANG() {
  return getToken(JavaParserLabeled::BANG, 0);
}

JavaParserLabeled::Expression8Context::Expression8Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression8Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression8(this);
}
void JavaParserLabeled::Expression8Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression8(this);
}

antlrcpp::Any JavaParserLabeled::Expression8Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression8(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression10Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression10Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression10Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression10Context::ADD() {
  return getToken(JavaParserLabeled::ADD, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression10Context::SUB() {
  return getToken(JavaParserLabeled::SUB, 0);
}

JavaParserLabeled::Expression10Context::Expression10Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression10Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression10(this);
}
void JavaParserLabeled::Expression10Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression10(this);
}

antlrcpp::Any JavaParserLabeled::Expression10Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression10(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression9Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression9Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression9Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression9Context::MUL() {
  return getToken(JavaParserLabeled::MUL, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression9Context::DIV() {
  return getToken(JavaParserLabeled::DIV, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression9Context::MOD() {
  return getToken(JavaParserLabeled::MOD, 0);
}

JavaParserLabeled::Expression9Context::Expression9Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression9Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression9(this);
}
void JavaParserLabeled::Expression9Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression9(this);
}

antlrcpp::Any JavaParserLabeled::Expression9Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression9(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression12Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression12Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression12Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression12Context::LE() {
  return getToken(JavaParserLabeled::LE, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression12Context::GE() {
  return getToken(JavaParserLabeled::GE, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression12Context::GT() {
  return getToken(JavaParserLabeled::GT, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression12Context::LT() {
  return getToken(JavaParserLabeled::LT, 0);
}

JavaParserLabeled::Expression12Context::Expression12Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression12Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression12(this);
}
void JavaParserLabeled::Expression12Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression12(this);
}

antlrcpp::Any JavaParserLabeled::Expression12Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression12(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression11Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression11Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression11Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::Expression11Context::LT() {
  return getTokens(JavaParserLabeled::LT);
}

tree::TerminalNode* JavaParserLabeled::Expression11Context::LT(size_t i) {
  return getToken(JavaParserLabeled::LT, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::Expression11Context::GT() {
  return getTokens(JavaParserLabeled::GT);
}

tree::TerminalNode* JavaParserLabeled::Expression11Context::GT(size_t i) {
  return getToken(JavaParserLabeled::GT, i);
}

JavaParserLabeled::Expression11Context::Expression11Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression11Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression11(this);
}
void JavaParserLabeled::Expression11Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression11(this);
}

antlrcpp::Any JavaParserLabeled::Expression11Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression11(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression14Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression14Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression14Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression14Context::EQUAL() {
  return getToken(JavaParserLabeled::EQUAL, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression14Context::NOTEQUAL() {
  return getToken(JavaParserLabeled::NOTEQUAL, 0);
}

JavaParserLabeled::Expression14Context::Expression14Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression14Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression14(this);
}
void JavaParserLabeled::Expression14Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression14(this);
}

antlrcpp::Any JavaParserLabeled::Expression14Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression14(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression13Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression13Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::Expression13Context::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression13Context::INSTANCEOF() {
  return getToken(JavaParserLabeled::INSTANCEOF, 0);
}

JavaParserLabeled::Expression13Context::Expression13Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression13Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression13(this);
}
void JavaParserLabeled::Expression13Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression13(this);
}

antlrcpp::Any JavaParserLabeled::Expression13Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression13(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression16Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression16Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression16Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression16Context::CARET() {
  return getToken(JavaParserLabeled::CARET, 0);
}

JavaParserLabeled::Expression16Context::Expression16Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression16Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression16(this);
}
void JavaParserLabeled::Expression16Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression16(this);
}

antlrcpp::Any JavaParserLabeled::Expression16Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression16(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression15Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression15Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression15Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression15Context::BITAND() {
  return getToken(JavaParserLabeled::BITAND, 0);
}

JavaParserLabeled::Expression15Context::Expression15Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression15Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression15(this);
}
void JavaParserLabeled::Expression15Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression15(this);
}

antlrcpp::Any JavaParserLabeled::Expression15Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression15(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression18Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression18Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression18Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression18Context::AND() {
  return getToken(JavaParserLabeled::AND, 0);
}

JavaParserLabeled::Expression18Context::Expression18Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression18Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression18(this);
}
void JavaParserLabeled::Expression18Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression18(this);
}

antlrcpp::Any JavaParserLabeled::Expression18Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression18(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression17Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression17Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression17Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression17Context::BITOR() {
  return getToken(JavaParserLabeled::BITOR, 0);
}

JavaParserLabeled::Expression17Context::Expression17Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression17Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression17(this);
}
void JavaParserLabeled::Expression17Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression17(this);
}

antlrcpp::Any JavaParserLabeled::Expression17Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression17(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression19Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression19Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression19Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression19Context::OR() {
  return getToken(JavaParserLabeled::OR, 0);
}

JavaParserLabeled::Expression19Context::Expression19Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression19Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression19(this);
}
void JavaParserLabeled::Expression19Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression19(this);
}

antlrcpp::Any JavaParserLabeled::Expression19Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression19(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression6Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression6Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression6Context::INC() {
  return getToken(JavaParserLabeled::INC, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression6Context::DEC() {
  return getToken(JavaParserLabeled::DEC, 0);
}

JavaParserLabeled::Expression6Context::Expression6Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression6(this);
}
void JavaParserLabeled::Expression6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression6(this);
}

antlrcpp::Any JavaParserLabeled::Expression6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression7Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression7Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression7Context::ADD() {
  return getToken(JavaParserLabeled::ADD, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression7Context::SUB() {
  return getToken(JavaParserLabeled::SUB, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression7Context::INC() {
  return getToken(JavaParserLabeled::INC, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression7Context::DEC() {
  return getToken(JavaParserLabeled::DEC, 0);
}

JavaParserLabeled::Expression7Context::Expression7Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression7Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression7(this);
}
void JavaParserLabeled::Expression7Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression7(this);
}

antlrcpp::Any JavaParserLabeled::Expression7Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression7(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression4Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Expression4Context::NEW() {
  return getToken(JavaParserLabeled::NEW, 0);
}

JavaParserLabeled::CreatorContext* JavaParserLabeled::Expression4Context::creator() {
  return getRuleContext<JavaParserLabeled::CreatorContext>(0);
}

JavaParserLabeled::Expression4Context::Expression4Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression4(this);
}
void JavaParserLabeled::Expression4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression4(this);
}

antlrcpp::Any JavaParserLabeled::Expression4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression5Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Expression5Context::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::Expression5Context::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression5Context::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression5Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::Expression5Context::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::Expression5Context::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}

JavaParserLabeled::Expression5Context::Expression5Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression5(this);
}
void JavaParserLabeled::Expression5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression5(this);
}

antlrcpp::Any JavaParserLabeled::Expression5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression2Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression2Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression2Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression2Context::LBRACK() {
  return getToken(JavaParserLabeled::LBRACK, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression2Context::RBRACK() {
  return getToken(JavaParserLabeled::RBRACK, 0);
}

JavaParserLabeled::Expression2Context::Expression2Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression2(this);
}
void JavaParserLabeled::Expression2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression2(this);
}

antlrcpp::Any JavaParserLabeled::Expression2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression3Context ------------------------------------------------------------------

JavaParserLabeled::MethodCallContext* JavaParserLabeled::Expression3Context::methodCall() {
  return getRuleContext<JavaParserLabeled::MethodCallContext>(0);
}

JavaParserLabeled::Expression3Context::Expression3Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression3(this);
}
void JavaParserLabeled::Expression3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression3(this);
}

antlrcpp::Any JavaParserLabeled::Expression3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression0Context ------------------------------------------------------------------

JavaParserLabeled::PrimaryContext* JavaParserLabeled::Expression0Context::primary() {
  return getRuleContext<JavaParserLabeled::PrimaryContext>(0);
}

JavaParserLabeled::Expression0Context::Expression0Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression0(this);
}
void JavaParserLabeled::Expression0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression0(this);
}

antlrcpp::Any JavaParserLabeled::Expression0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression1Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression1Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression1Context::DOT() {
  return getToken(JavaParserLabeled::DOT, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression1Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::MethodCallContext* JavaParserLabeled::Expression1Context::methodCall() {
  return getRuleContext<JavaParserLabeled::MethodCallContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression1Context::THIS() {
  return getToken(JavaParserLabeled::THIS, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression1Context::NEW() {
  return getToken(JavaParserLabeled::NEW, 0);
}

JavaParserLabeled::InnerCreatorContext* JavaParserLabeled::Expression1Context::innerCreator() {
  return getRuleContext<JavaParserLabeled::InnerCreatorContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression1Context::SUPER() {
  return getToken(JavaParserLabeled::SUPER, 0);
}

JavaParserLabeled::SuperSuffixContext* JavaParserLabeled::Expression1Context::superSuffix() {
  return getRuleContext<JavaParserLabeled::SuperSuffixContext>(0);
}

JavaParserLabeled::ExplicitGenericInvocationContext* JavaParserLabeled::Expression1Context::explicitGenericInvocation() {
  return getRuleContext<JavaParserLabeled::ExplicitGenericInvocationContext>(0);
}

JavaParserLabeled::NonWildcardTypeArgumentsContext* JavaParserLabeled::Expression1Context::nonWildcardTypeArguments() {
  return getRuleContext<JavaParserLabeled::NonWildcardTypeArgumentsContext>(0);
}

JavaParserLabeled::Expression1Context::Expression1Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression1(this);
}
void JavaParserLabeled::Expression1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression1(this);
}

antlrcpp::Any JavaParserLabeled::Expression1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression21Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression21Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression21Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::ASSIGN() {
  return getToken(JavaParserLabeled::ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::ADD_ASSIGN() {
  return getToken(JavaParserLabeled::ADD_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::SUB_ASSIGN() {
  return getToken(JavaParserLabeled::SUB_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::MUL_ASSIGN() {
  return getToken(JavaParserLabeled::MUL_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::DIV_ASSIGN() {
  return getToken(JavaParserLabeled::DIV_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::AND_ASSIGN() {
  return getToken(JavaParserLabeled::AND_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::OR_ASSIGN() {
  return getToken(JavaParserLabeled::OR_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::XOR_ASSIGN() {
  return getToken(JavaParserLabeled::XOR_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::RSHIFT_ASSIGN() {
  return getToken(JavaParserLabeled::RSHIFT_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::URSHIFT_ASSIGN() {
  return getToken(JavaParserLabeled::URSHIFT_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::LSHIFT_ASSIGN() {
  return getToken(JavaParserLabeled::LSHIFT_ASSIGN, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression21Context::MOD_ASSIGN() {
  return getToken(JavaParserLabeled::MOD_ASSIGN, 0);
}

JavaParserLabeled::Expression21Context::Expression21Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression21Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression21(this);
}
void JavaParserLabeled::Expression21Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression21(this);
}

antlrcpp::Any JavaParserLabeled::Expression21Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression21(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression20Context ------------------------------------------------------------------

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::Expression20Context::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression20Context::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}

tree::TerminalNode* JavaParserLabeled::Expression20Context::COLON() {
  return getToken(JavaParserLabeled::COLON, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression20Context::QUESTION() {
  return getToken(JavaParserLabeled::QUESTION, 0);
}

JavaParserLabeled::Expression20Context::Expression20Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression20Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression20(this);
}
void JavaParserLabeled::Expression20Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression20(this);
}

antlrcpp::Any JavaParserLabeled::Expression20Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression20(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression23Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Expression23Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression23Context::COLONCOLON() {
  return getToken(JavaParserLabeled::COLONCOLON, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression23Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::TypeArgumentsContext* JavaParserLabeled::Expression23Context::typeArguments() {
  return getRuleContext<JavaParserLabeled::TypeArgumentsContext>(0);
}

JavaParserLabeled::Expression23Context::Expression23Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression23Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression23(this);
}
void JavaParserLabeled::Expression23Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression23(this);
}

antlrcpp::Any JavaParserLabeled::Expression23Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression23(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression22Context ------------------------------------------------------------------

JavaParserLabeled::LambdaExpressionContext* JavaParserLabeled::Expression22Context::lambdaExpression() {
  return getRuleContext<JavaParserLabeled::LambdaExpressionContext>(0);
}

JavaParserLabeled::Expression22Context::Expression22Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression22Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression22(this);
}
void JavaParserLabeled::Expression22Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression22(this);
}

antlrcpp::Any JavaParserLabeled::Expression22Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression22(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression25Context ------------------------------------------------------------------

JavaParserLabeled::ClassTypeContext* JavaParserLabeled::Expression25Context::classType() {
  return getRuleContext<JavaParserLabeled::ClassTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression25Context::COLONCOLON() {
  return getToken(JavaParserLabeled::COLONCOLON, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression25Context::NEW() {
  return getToken(JavaParserLabeled::NEW, 0);
}

JavaParserLabeled::TypeArgumentsContext* JavaParserLabeled::Expression25Context::typeArguments() {
  return getRuleContext<JavaParserLabeled::TypeArgumentsContext>(0);
}

JavaParserLabeled::Expression25Context::Expression25Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression25Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression25(this);
}
void JavaParserLabeled::Expression25Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression25(this);
}

antlrcpp::Any JavaParserLabeled::Expression25Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression25(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Expression24Context ------------------------------------------------------------------

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::Expression24Context::typeType() {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Expression24Context::COLONCOLON() {
  return getToken(JavaParserLabeled::COLONCOLON, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression24Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

tree::TerminalNode* JavaParserLabeled::Expression24Context::NEW() {
  return getToken(JavaParserLabeled::NEW, 0);
}

JavaParserLabeled::TypeArgumentsContext* JavaParserLabeled::Expression24Context::typeArguments() {
  return getRuleContext<JavaParserLabeled::TypeArgumentsContext>(0);
}

JavaParserLabeled::Expression24Context::Expression24Context(ExpressionContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Expression24Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression24(this);
}
void JavaParserLabeled::Expression24Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression24(this);
}

antlrcpp::Any JavaParserLabeled::Expression24Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExpression24(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::expression() {
   return expression(0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::expression(int precedence) {
  ParserRuleContext *parentContext = _ctx;
  size_t parentState = getState();
  JavaParserLabeled::ExpressionContext *_localctx = _tracker.createInstance<ExpressionContext>(_ctx, parentState);
  JavaParserLabeled::ExpressionContext *previousContext = _localctx;
  (void)previousContext; // Silence compiler, in case the context is not used by generated code.
  size_t startState = 166;
  enterRecursionRule(_localctx, 166, JavaParserLabeled::RuleExpression, precedence);

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
      match(JavaParserLabeled::NEW);
      setState(1101);
      creator();
      break;
    }

    case 4: {
      _localctx = _tracker.createInstance<Expression5Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1102);
      match(JavaParserLabeled::LPAREN);
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
      match(JavaParserLabeled::RPAREN);
      setState(1111);
      expression(21);
      break;
    }

    case 5: {
      _localctx = _tracker.createInstance<Expression7Context>(_localctx);
      _ctx = _localctx;
      previousContext = _localctx;
      setState(1113);
      dynamic_cast<Expression7Context *>(_localctx)->prefix = _input->LT(1);
      _la = _input->LA(1);
      if (!(((((_la - 83) & ~ 0x3fULL) == 0) &&
        ((1ULL << (_la - 83)) & ((1ULL << (JavaParserLabeled::INC - 83))
        | (1ULL << (JavaParserLabeled::DEC - 83))
        | (1ULL << (JavaParserLabeled::ADD - 83))
        | (1ULL << (JavaParserLabeled::SUB - 83)))) != 0))) {
        dynamic_cast<Expression7Context *>(_localctx)->prefix = _errHandler->recoverInline(this);
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
      dynamic_cast<Expression8Context *>(_localctx)->prefix = _input->LT(1);
      _la = _input->LA(1);
      if (!(_la == JavaParserLabeled::BANG

      || _la == JavaParserLabeled::TILDE)) {
        dynamic_cast<Expression8Context *>(_localctx)->prefix = _errHandler->recoverInline(this);
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
      match(JavaParserLabeled::COLONCOLON);
      setState(1125);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case JavaParserLabeled::LT:
        case JavaParserLabeled::IDENTIFIER: {
          setState(1121);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == JavaParserLabeled::LT) {
            setState(1120);
            typeArguments();
          }
          setState(1123);
          match(JavaParserLabeled::IDENTIFIER);
          break;
        }

        case JavaParserLabeled::NEW: {
          setState(1124);
          match(JavaParserLabeled::NEW);
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
      match(JavaParserLabeled::COLONCOLON);
      setState(1130);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == JavaParserLabeled::LT) {
        setState(1129);
        typeArguments();
      }
      setState(1132);
      match(JavaParserLabeled::NEW);
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
          dynamic_cast<Expression9Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(((((_la - 87) & ~ 0x3fULL) == 0) &&
            ((1ULL << (_la - 87)) & ((1ULL << (JavaParserLabeled::MUL - 87))
            | (1ULL << (JavaParserLabeled::DIV - 87))
            | (1ULL << (JavaParserLabeled::MOD - 87)))) != 0))) {
            dynamic_cast<Expression9Context *>(_localctx)->bop = _errHandler->recoverInline(this);
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
          dynamic_cast<Expression10Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == JavaParserLabeled::ADD

          || _la == JavaParserLabeled::SUB)) {
            dynamic_cast<Expression10Context *>(_localctx)->bop = _errHandler->recoverInline(this);
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
            match(JavaParserLabeled::LT);
            setState(1144);
            match(JavaParserLabeled::LT);
            break;
          }

          case 2: {
            setState(1145);
            match(JavaParserLabeled::GT);
            setState(1146);
            match(JavaParserLabeled::GT);
            setState(1147);
            match(JavaParserLabeled::GT);
            break;
          }

          case 3: {
            setState(1148);
            match(JavaParserLabeled::GT);
            setState(1149);
            match(JavaParserLabeled::GT);
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
          dynamic_cast<Expression12Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(((((_la - 71) & ~ 0x3fULL) == 0) &&
            ((1ULL << (_la - 71)) & ((1ULL << (JavaParserLabeled::GT - 71))
            | (1ULL << (JavaParserLabeled::LT - 71))
            | (1ULL << (JavaParserLabeled::LE - 71))
            | (1ULL << (JavaParserLabeled::GE - 71)))) != 0))) {
            dynamic_cast<Expression12Context *>(_localctx)->bop = _errHandler->recoverInline(this);
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
          dynamic_cast<Expression14Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == JavaParserLabeled::EQUAL

          || _la == JavaParserLabeled::NOTEQUAL)) {
            dynamic_cast<Expression14Context *>(_localctx)->bop = _errHandler->recoverInline(this);
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
          dynamic_cast<Expression15Context *>(_localctx)->bop = match(JavaParserLabeled::BITAND);
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
          dynamic_cast<Expression16Context *>(_localctx)->bop = match(JavaParserLabeled::CARET);
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
          dynamic_cast<Expression17Context *>(_localctx)->bop = match(JavaParserLabeled::BITOR);
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
          dynamic_cast<Expression18Context *>(_localctx)->bop = match(JavaParserLabeled::AND);
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
          dynamic_cast<Expression19Context *>(_localctx)->bop = match(JavaParserLabeled::OR);
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
          dynamic_cast<Expression20Context *>(_localctx)->bop = match(JavaParserLabeled::QUESTION);
          setState(1176);
          expression(0);
          setState(1177);
          match(JavaParserLabeled::COLON);
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
          dynamic_cast<Expression21Context *>(_localctx)->bop = _input->LT(1);
          _la = _input->LA(1);
          if (!(((((_la - 70) & ~ 0x3fULL) == 0) &&
            ((1ULL << (_la - 70)) & ((1ULL << (JavaParserLabeled::ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::ADD_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::SUB_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::MUL_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::DIV_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::AND_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::OR_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::XOR_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::MOD_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::LSHIFT_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::RSHIFT_ASSIGN - 70))
            | (1ULL << (JavaParserLabeled::URSHIFT_ASSIGN - 70)))) != 0))) {
            dynamic_cast<Expression21Context *>(_localctx)->bop = _errHandler->recoverInline(this);
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
          dynamic_cast<Expression1Context *>(_localctx)->bop = match(JavaParserLabeled::DOT);
          setState(1196);
          _errHandler->sync(this);
          switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 141, _ctx)) {
          case 1: {
            setState(1185);
            match(JavaParserLabeled::IDENTIFIER);
            break;
          }

          case 2: {
            setState(1186);
            methodCall();
            break;
          }

          case 3: {
            setState(1187);
            match(JavaParserLabeled::THIS);
            break;
          }

          case 4: {
            setState(1188);
            match(JavaParserLabeled::NEW);
            setState(1190);
            _errHandler->sync(this);

            _la = _input->LA(1);
            if (_la == JavaParserLabeled::LT) {
              setState(1189);
              nonWildcardTypeArguments();
            }
            setState(1192);
            innerCreator();
            break;
          }

          case 5: {
            setState(1193);
            match(JavaParserLabeled::SUPER);
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
          match(JavaParserLabeled::LBRACK);
          setState(1200);
          expression(0);
          setState(1201);
          match(JavaParserLabeled::RBRACK);
          break;
        }

        case 15: {
          auto newContext = _tracker.createInstance<Expression6Context>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(1203);

          if (!(precpred(_ctx, 20))) throw FailedPredicateException(this, "precpred(_ctx, 20)");
          setState(1204);
          dynamic_cast<Expression6Context *>(_localctx)->postfix = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == JavaParserLabeled::INC

          || _la == JavaParserLabeled::DEC)) {
            dynamic_cast<Expression6Context *>(_localctx)->postfix = _errHandler->recoverInline(this);
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
          dynamic_cast<Expression13Context *>(_localctx)->bop = match(JavaParserLabeled::INSTANCEOF);
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
          match(JavaParserLabeled::COLONCOLON);
          setState(1211);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == JavaParserLabeled::LT) {
            setState(1210);
            typeArguments();
          }
          setState(1213);
          match(JavaParserLabeled::IDENTIFIER);
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

JavaParserLabeled::LambdaExpressionContext::LambdaExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::LambdaParametersContext* JavaParserLabeled::LambdaExpressionContext::lambdaParameters() {
  return getRuleContext<JavaParserLabeled::LambdaParametersContext>(0);
}

tree::TerminalNode* JavaParserLabeled::LambdaExpressionContext::ARROW() {
  return getToken(JavaParserLabeled::ARROW, 0);
}

JavaParserLabeled::LambdaBodyContext* JavaParserLabeled::LambdaExpressionContext::lambdaBody() {
  return getRuleContext<JavaParserLabeled::LambdaBodyContext>(0);
}


size_t JavaParserLabeled::LambdaExpressionContext::getRuleIndex() const {
  return JavaParserLabeled::RuleLambdaExpression;
}

void JavaParserLabeled::LambdaExpressionContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaExpression(this);
}

void JavaParserLabeled::LambdaExpressionContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaExpression(this);
}


antlrcpp::Any JavaParserLabeled::LambdaExpressionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLambdaExpression(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::LambdaExpressionContext* JavaParserLabeled::lambdaExpression() {
  LambdaExpressionContext *_localctx = _tracker.createInstance<LambdaExpressionContext>(_ctx, getState());
  enterRule(_localctx, 168, JavaParserLabeled::RuleLambdaExpression);

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
    match(JavaParserLabeled::ARROW);
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

JavaParserLabeled::LambdaParametersContext::LambdaParametersContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::LambdaParametersContext::getRuleIndex() const {
  return JavaParserLabeled::RuleLambdaParameters;
}

void JavaParserLabeled::LambdaParametersContext::copyFrom(LambdaParametersContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- LambdaParameters0Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::LambdaParameters0Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::LambdaParameters0Context::LambdaParameters0Context(LambdaParametersContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::LambdaParameters0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaParameters0(this);
}
void JavaParserLabeled::LambdaParameters0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaParameters0(this);
}

antlrcpp::Any JavaParserLabeled::LambdaParameters0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLambdaParameters0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- LambdaParameters1Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::LambdaParameters1Context::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::LambdaParameters1Context::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::FormalParameterListContext* JavaParserLabeled::LambdaParameters1Context::formalParameterList() {
  return getRuleContext<JavaParserLabeled::FormalParameterListContext>(0);
}

JavaParserLabeled::LambdaParameters1Context::LambdaParameters1Context(LambdaParametersContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::LambdaParameters1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaParameters1(this);
}
void JavaParserLabeled::LambdaParameters1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaParameters1(this);
}

antlrcpp::Any JavaParserLabeled::LambdaParameters1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLambdaParameters1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- LambdaParameters2Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::LambdaParameters2Context::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::LambdaParameters2Context::IDENTIFIER() {
  return getTokens(JavaParserLabeled::IDENTIFIER);
}

tree::TerminalNode* JavaParserLabeled::LambdaParameters2Context::IDENTIFIER(size_t i) {
  return getToken(JavaParserLabeled::IDENTIFIER, i);
}

tree::TerminalNode* JavaParserLabeled::LambdaParameters2Context::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::LambdaParameters2Context::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::LambdaParameters2Context::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}

JavaParserLabeled::LambdaParameters2Context::LambdaParameters2Context(LambdaParametersContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::LambdaParameters2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaParameters2(this);
}
void JavaParserLabeled::LambdaParameters2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaParameters2(this);
}

antlrcpp::Any JavaParserLabeled::LambdaParameters2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLambdaParameters2(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::LambdaParametersContext* JavaParserLabeled::lambdaParameters() {
  LambdaParametersContext *_localctx = _tracker.createInstance<LambdaParametersContext>(_ctx, getState());
  enterRule(_localctx, 170, JavaParserLabeled::RuleLambdaParameters);
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
      _localctx = dynamic_cast<LambdaParametersContext *>(_tracker.createInstance<JavaParserLabeled::LambdaParameters0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(1223);
      match(JavaParserLabeled::IDENTIFIER);
      break;
    }

    case 2: {
      _localctx = dynamic_cast<LambdaParametersContext *>(_tracker.createInstance<JavaParserLabeled::LambdaParameters1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(1224);
      match(JavaParserLabeled::LPAREN);
      setState(1226);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
        | (1ULL << JavaParserLabeled::BYTE)
        | (1ULL << JavaParserLabeled::CHAR)
        | (1ULL << JavaParserLabeled::DOUBLE)
        | (1ULL << JavaParserLabeled::FINAL)
        | (1ULL << JavaParserLabeled::FLOAT)
        | (1ULL << JavaParserLabeled::INT)
        | (1ULL << JavaParserLabeled::LONG)
        | (1ULL << JavaParserLabeled::SHORT))) != 0) || _la == JavaParserLabeled::AT

      || _la == JavaParserLabeled::IDENTIFIER) {
        setState(1225);
        formalParameterList();
      }
      setState(1228);
      match(JavaParserLabeled::RPAREN);
      break;
    }

    case 3: {
      _localctx = dynamic_cast<LambdaParametersContext *>(_tracker.createInstance<JavaParserLabeled::LambdaParameters2Context>(_localctx));
      enterOuterAlt(_localctx, 3);
      setState(1229);
      match(JavaParserLabeled::LPAREN);
      setState(1230);
      match(JavaParserLabeled::IDENTIFIER);
      setState(1235);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == JavaParserLabeled::COMMA) {
        setState(1231);
        match(JavaParserLabeled::COMMA);
        setState(1232);
        match(JavaParserLabeled::IDENTIFIER);
        setState(1237);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(1238);
      match(JavaParserLabeled::RPAREN);
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

JavaParserLabeled::LambdaBodyContext::LambdaBodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::LambdaBodyContext::getRuleIndex() const {
  return JavaParserLabeled::RuleLambdaBody;
}

void JavaParserLabeled::LambdaBodyContext::copyFrom(LambdaBodyContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- LambdaBody0Context ------------------------------------------------------------------

JavaParserLabeled::ExpressionContext* JavaParserLabeled::LambdaBody0Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

JavaParserLabeled::LambdaBody0Context::LambdaBody0Context(LambdaBodyContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::LambdaBody0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaBody0(this);
}
void JavaParserLabeled::LambdaBody0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaBody0(this);
}

antlrcpp::Any JavaParserLabeled::LambdaBody0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLambdaBody0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- LambdaBody1Context ------------------------------------------------------------------

JavaParserLabeled::BlockContext* JavaParserLabeled::LambdaBody1Context::block() {
  return getRuleContext<JavaParserLabeled::BlockContext>(0);
}

JavaParserLabeled::LambdaBody1Context::LambdaBody1Context(LambdaBodyContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::LambdaBody1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLambdaBody1(this);
}
void JavaParserLabeled::LambdaBody1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLambdaBody1(this);
}

antlrcpp::Any JavaParserLabeled::LambdaBody1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitLambdaBody1(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::LambdaBodyContext* JavaParserLabeled::lambdaBody() {
  LambdaBodyContext *_localctx = _tracker.createInstance<LambdaBodyContext>(_ctx, getState());
  enterRule(_localctx, 172, JavaParserLabeled::RuleLambdaBody);

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
      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::NEW:
      case JavaParserLabeled::SHORT:
      case JavaParserLabeled::SUPER:
      case JavaParserLabeled::THIS:
      case JavaParserLabeled::VOID:
      case JavaParserLabeled::DECIMAL_LITERAL:
      case JavaParserLabeled::HEX_LITERAL:
      case JavaParserLabeled::OCT_LITERAL:
      case JavaParserLabeled::BINARY_LITERAL:
      case JavaParserLabeled::FLOAT_LITERAL:
      case JavaParserLabeled::HEX_FLOAT_LITERAL:
      case JavaParserLabeled::BOOL_LITERAL:
      case JavaParserLabeled::CHAR_LITERAL:
      case JavaParserLabeled::STRING_LITERAL:
      case JavaParserLabeled::NULL_LITERAL:
      case JavaParserLabeled::LPAREN:
      case JavaParserLabeled::LT:
      case JavaParserLabeled::BANG:
      case JavaParserLabeled::TILDE:
      case JavaParserLabeled::INC:
      case JavaParserLabeled::DEC:
      case JavaParserLabeled::ADD:
      case JavaParserLabeled::SUB:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        _localctx = dynamic_cast<LambdaBodyContext *>(_tracker.createInstance<JavaParserLabeled::LambdaBody0Context>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(1241);
        expression(0);
        break;
      }

      case JavaParserLabeled::LBRACE: {
        _localctx = dynamic_cast<LambdaBodyContext *>(_tracker.createInstance<JavaParserLabeled::LambdaBody1Context>(_localctx));
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

JavaParserLabeled::PrimaryContext::PrimaryContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::PrimaryContext::getRuleIndex() const {
  return JavaParserLabeled::RulePrimary;
}

void JavaParserLabeled::PrimaryContext::copyFrom(PrimaryContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Primary6Context ------------------------------------------------------------------

JavaParserLabeled::NonWildcardTypeArgumentsContext* JavaParserLabeled::Primary6Context::nonWildcardTypeArguments() {
  return getRuleContext<JavaParserLabeled::NonWildcardTypeArgumentsContext>(0);
}

JavaParserLabeled::ExplicitGenericInvocationSuffixContext* JavaParserLabeled::Primary6Context::explicitGenericInvocationSuffix() {
  return getRuleContext<JavaParserLabeled::ExplicitGenericInvocationSuffixContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Primary6Context::THIS() {
  return getToken(JavaParserLabeled::THIS, 0);
}

JavaParserLabeled::ArgumentsContext* JavaParserLabeled::Primary6Context::arguments() {
  return getRuleContext<JavaParserLabeled::ArgumentsContext>(0);
}

JavaParserLabeled::Primary6Context::Primary6Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Primary6Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary6(this);
}
void JavaParserLabeled::Primary6Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary6(this);
}

antlrcpp::Any JavaParserLabeled::Primary6Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPrimary6(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary2Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Primary2Context::SUPER() {
  return getToken(JavaParserLabeled::SUPER, 0);
}

JavaParserLabeled::Primary2Context::Primary2Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Primary2Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary2(this);
}
void JavaParserLabeled::Primary2Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary2(this);
}

antlrcpp::Any JavaParserLabeled::Primary2Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPrimary2(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary3Context ------------------------------------------------------------------

JavaParserLabeled::LiteralContext* JavaParserLabeled::Primary3Context::literal() {
  return getRuleContext<JavaParserLabeled::LiteralContext>(0);
}

JavaParserLabeled::Primary3Context::Primary3Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Primary3Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary3(this);
}
void JavaParserLabeled::Primary3Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary3(this);
}

antlrcpp::Any JavaParserLabeled::Primary3Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPrimary3(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary4Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Primary4Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::Primary4Context::Primary4Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Primary4Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary4(this);
}
void JavaParserLabeled::Primary4Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary4(this);
}

antlrcpp::Any JavaParserLabeled::Primary4Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPrimary4(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary5Context ------------------------------------------------------------------

JavaParserLabeled::TypeTypeOrVoidContext* JavaParserLabeled::Primary5Context::typeTypeOrVoid() {
  return getRuleContext<JavaParserLabeled::TypeTypeOrVoidContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Primary5Context::DOT() {
  return getToken(JavaParserLabeled::DOT, 0);
}

tree::TerminalNode* JavaParserLabeled::Primary5Context::CLASS() {
  return getToken(JavaParserLabeled::CLASS, 0);
}

JavaParserLabeled::Primary5Context::Primary5Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Primary5Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary5(this);
}
void JavaParserLabeled::Primary5Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary5(this);
}

antlrcpp::Any JavaParserLabeled::Primary5Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPrimary5(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary0Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Primary0Context::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::Primary0Context::expression() {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(0);
}

tree::TerminalNode* JavaParserLabeled::Primary0Context::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::Primary0Context::Primary0Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Primary0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary0(this);
}
void JavaParserLabeled::Primary0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary0(this);
}

antlrcpp::Any JavaParserLabeled::Primary0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPrimary0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Primary1Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::Primary1Context::THIS() {
  return getToken(JavaParserLabeled::THIS, 0);
}

JavaParserLabeled::Primary1Context::Primary1Context(PrimaryContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Primary1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimary1(this);
}
void JavaParserLabeled::Primary1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimary1(this);
}

antlrcpp::Any JavaParserLabeled::Primary1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPrimary1(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::PrimaryContext* JavaParserLabeled::primary() {
  PrimaryContext *_localctx = _tracker.createInstance<PrimaryContext>(_ctx, getState());
  enterRule(_localctx, 174, JavaParserLabeled::RulePrimary);

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
      _localctx = dynamic_cast<PrimaryContext *>(_tracker.createInstance<JavaParserLabeled::Primary0Context>(_localctx));
      enterOuterAlt(_localctx, 1);
      setState(1245);
      match(JavaParserLabeled::LPAREN);
      setState(1246);
      expression(0);
      setState(1247);
      match(JavaParserLabeled::RPAREN);
      break;
    }

    case 2: {
      _localctx = dynamic_cast<PrimaryContext *>(_tracker.createInstance<JavaParserLabeled::Primary1Context>(_localctx));
      enterOuterAlt(_localctx, 2);
      setState(1249);
      match(JavaParserLabeled::THIS);
      break;
    }

    case 3: {
      _localctx = dynamic_cast<PrimaryContext *>(_tracker.createInstance<JavaParserLabeled::Primary2Context>(_localctx));
      enterOuterAlt(_localctx, 3);
      setState(1250);
      match(JavaParserLabeled::SUPER);
      break;
    }

    case 4: {
      _localctx = dynamic_cast<PrimaryContext *>(_tracker.createInstance<JavaParserLabeled::Primary3Context>(_localctx));
      enterOuterAlt(_localctx, 4);
      setState(1251);
      literal();
      break;
    }

    case 5: {
      _localctx = dynamic_cast<PrimaryContext *>(_tracker.createInstance<JavaParserLabeled::Primary4Context>(_localctx));
      enterOuterAlt(_localctx, 5);
      setState(1252);
      match(JavaParserLabeled::IDENTIFIER);
      break;
    }

    case 6: {
      _localctx = dynamic_cast<PrimaryContext *>(_tracker.createInstance<JavaParserLabeled::Primary5Context>(_localctx));
      enterOuterAlt(_localctx, 6);
      setState(1253);
      typeTypeOrVoid();
      setState(1254);
      match(JavaParserLabeled::DOT);
      setState(1255);
      match(JavaParserLabeled::CLASS);
      break;
    }

    case 7: {
      _localctx = dynamic_cast<PrimaryContext *>(_tracker.createInstance<JavaParserLabeled::Primary6Context>(_localctx));
      enterOuterAlt(_localctx, 7);
      setState(1257);
      nonWildcardTypeArguments();
      setState(1261);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case JavaParserLabeled::SUPER:
        case JavaParserLabeled::IDENTIFIER: {
          setState(1258);
          explicitGenericInvocationSuffix();
          break;
        }

        case JavaParserLabeled::THIS: {
          setState(1259);
          match(JavaParserLabeled::THIS);
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

JavaParserLabeled::ClassTypeContext::ClassTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ClassTypeContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::ClassOrInterfaceTypeContext* JavaParserLabeled::ClassTypeContext::classOrInterfaceType() {
  return getRuleContext<JavaParserLabeled::ClassOrInterfaceTypeContext>(0);
}

tree::TerminalNode* JavaParserLabeled::ClassTypeContext::DOT() {
  return getToken(JavaParserLabeled::DOT, 0);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::ClassTypeContext::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::ClassTypeContext::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}

JavaParserLabeled::TypeArgumentsContext* JavaParserLabeled::ClassTypeContext::typeArguments() {
  return getRuleContext<JavaParserLabeled::TypeArgumentsContext>(0);
}


size_t JavaParserLabeled::ClassTypeContext::getRuleIndex() const {
  return JavaParserLabeled::RuleClassType;
}

void JavaParserLabeled::ClassTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassType(this);
}

void JavaParserLabeled::ClassTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassType(this);
}


antlrcpp::Any JavaParserLabeled::ClassTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassType(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ClassTypeContext* JavaParserLabeled::classType() {
  ClassTypeContext *_localctx = _tracker.createInstance<ClassTypeContext>(_ctx, getState());
  enterRule(_localctx, 176, JavaParserLabeled::RuleClassType);
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
      match(JavaParserLabeled::DOT);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(1278);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::LT) {
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

JavaParserLabeled::CreatorContext::CreatorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::CreatorContext::getRuleIndex() const {
  return JavaParserLabeled::RuleCreator;
}

void JavaParserLabeled::CreatorContext::copyFrom(CreatorContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- Creator1Context ------------------------------------------------------------------

JavaParserLabeled::CreatedNameContext* JavaParserLabeled::Creator1Context::createdName() {
  return getRuleContext<JavaParserLabeled::CreatedNameContext>(0);
}

JavaParserLabeled::ArrayCreatorRestContext* JavaParserLabeled::Creator1Context::arrayCreatorRest() {
  return getRuleContext<JavaParserLabeled::ArrayCreatorRestContext>(0);
}

JavaParserLabeled::ClassCreatorRestContext* JavaParserLabeled::Creator1Context::classCreatorRest() {
  return getRuleContext<JavaParserLabeled::ClassCreatorRestContext>(0);
}

JavaParserLabeled::Creator1Context::Creator1Context(CreatorContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Creator1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCreator1(this);
}
void JavaParserLabeled::Creator1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCreator1(this);
}

antlrcpp::Any JavaParserLabeled::Creator1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitCreator1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- Creator0Context ------------------------------------------------------------------

JavaParserLabeled::NonWildcardTypeArgumentsContext* JavaParserLabeled::Creator0Context::nonWildcardTypeArguments() {
  return getRuleContext<JavaParserLabeled::NonWildcardTypeArgumentsContext>(0);
}

JavaParserLabeled::CreatedNameContext* JavaParserLabeled::Creator0Context::createdName() {
  return getRuleContext<JavaParserLabeled::CreatedNameContext>(0);
}

JavaParserLabeled::ClassCreatorRestContext* JavaParserLabeled::Creator0Context::classCreatorRest() {
  return getRuleContext<JavaParserLabeled::ClassCreatorRestContext>(0);
}

JavaParserLabeled::Creator0Context::Creator0Context(CreatorContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::Creator0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCreator0(this);
}
void JavaParserLabeled::Creator0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCreator0(this);
}

antlrcpp::Any JavaParserLabeled::Creator0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitCreator0(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::CreatorContext* JavaParserLabeled::creator() {
  CreatorContext *_localctx = _tracker.createInstance<CreatorContext>(_ctx, getState());
  enterRule(_localctx, 178, JavaParserLabeled::RuleCreator);

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
      case JavaParserLabeled::LT: {
        _localctx = dynamic_cast<CreatorContext *>(_tracker.createInstance<JavaParserLabeled::Creator0Context>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(1280);
        nonWildcardTypeArguments();
        setState(1281);
        createdName();
        setState(1282);
        classCreatorRest();
        break;
      }

      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::SHORT:
      case JavaParserLabeled::IDENTIFIER: {
        _localctx = dynamic_cast<CreatorContext *>(_tracker.createInstance<JavaParserLabeled::Creator1Context>(_localctx));
        enterOuterAlt(_localctx, 2);
        setState(1284);
        createdName();
        setState(1287);
        _errHandler->sync(this);
        switch (_input->LA(1)) {
          case JavaParserLabeled::LBRACK: {
            setState(1285);
            arrayCreatorRest();
            break;
          }

          case JavaParserLabeled::LPAREN: {
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

JavaParserLabeled::CreatedNameContext::CreatedNameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::CreatedNameContext::getRuleIndex() const {
  return JavaParserLabeled::RuleCreatedName;
}

void JavaParserLabeled::CreatedNameContext::copyFrom(CreatedNameContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- CreatedName0Context ------------------------------------------------------------------

std::vector<tree::TerminalNode *> JavaParserLabeled::CreatedName0Context::IDENTIFIER() {
  return getTokens(JavaParserLabeled::IDENTIFIER);
}

tree::TerminalNode* JavaParserLabeled::CreatedName0Context::IDENTIFIER(size_t i) {
  return getToken(JavaParserLabeled::IDENTIFIER, i);
}

std::vector<JavaParserLabeled::TypeArgumentsOrDiamondContext *> JavaParserLabeled::CreatedName0Context::typeArgumentsOrDiamond() {
  return getRuleContexts<JavaParserLabeled::TypeArgumentsOrDiamondContext>();
}

JavaParserLabeled::TypeArgumentsOrDiamondContext* JavaParserLabeled::CreatedName0Context::typeArgumentsOrDiamond(size_t i) {
  return getRuleContext<JavaParserLabeled::TypeArgumentsOrDiamondContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::CreatedName0Context::DOT() {
  return getTokens(JavaParserLabeled::DOT);
}

tree::TerminalNode* JavaParserLabeled::CreatedName0Context::DOT(size_t i) {
  return getToken(JavaParserLabeled::DOT, i);
}

JavaParserLabeled::CreatedName0Context::CreatedName0Context(CreatedNameContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::CreatedName0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCreatedName0(this);
}
void JavaParserLabeled::CreatedName0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCreatedName0(this);
}

antlrcpp::Any JavaParserLabeled::CreatedName0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitCreatedName0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- CreatedName1Context ------------------------------------------------------------------

JavaParserLabeled::PrimitiveTypeContext* JavaParserLabeled::CreatedName1Context::primitiveType() {
  return getRuleContext<JavaParserLabeled::PrimitiveTypeContext>(0);
}

JavaParserLabeled::CreatedName1Context::CreatedName1Context(CreatedNameContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::CreatedName1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCreatedName1(this);
}
void JavaParserLabeled::CreatedName1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCreatedName1(this);
}

antlrcpp::Any JavaParserLabeled::CreatedName1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitCreatedName1(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::CreatedNameContext* JavaParserLabeled::createdName() {
  CreatedNameContext *_localctx = _tracker.createInstance<CreatedNameContext>(_ctx, getState());
  enterRule(_localctx, 180, JavaParserLabeled::RuleCreatedName);
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
      case JavaParserLabeled::IDENTIFIER: {
        _localctx = dynamic_cast<CreatedNameContext *>(_tracker.createInstance<JavaParserLabeled::CreatedName0Context>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(1291);
        match(JavaParserLabeled::IDENTIFIER);
        setState(1293);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if (_la == JavaParserLabeled::LT) {
          setState(1292);
          typeArgumentsOrDiamond();
        }
        setState(1302);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while (_la == JavaParserLabeled::DOT) {
          setState(1295);
          match(JavaParserLabeled::DOT);
          setState(1296);
          match(JavaParserLabeled::IDENTIFIER);
          setState(1298);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == JavaParserLabeled::LT) {
            setState(1297);
            typeArgumentsOrDiamond();
          }
          setState(1304);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        break;
      }

      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::SHORT: {
        _localctx = dynamic_cast<CreatedNameContext *>(_tracker.createInstance<JavaParserLabeled::CreatedName1Context>(_localctx));
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

JavaParserLabeled::InnerCreatorContext::InnerCreatorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::InnerCreatorContext::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::ClassCreatorRestContext* JavaParserLabeled::InnerCreatorContext::classCreatorRest() {
  return getRuleContext<JavaParserLabeled::ClassCreatorRestContext>(0);
}

JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext* JavaParserLabeled::InnerCreatorContext::nonWildcardTypeArgumentsOrDiamond() {
  return getRuleContext<JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext>(0);
}


size_t JavaParserLabeled::InnerCreatorContext::getRuleIndex() const {
  return JavaParserLabeled::RuleInnerCreator;
}

void JavaParserLabeled::InnerCreatorContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterInnerCreator(this);
}

void JavaParserLabeled::InnerCreatorContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitInnerCreator(this);
}


antlrcpp::Any JavaParserLabeled::InnerCreatorContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitInnerCreator(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::InnerCreatorContext* JavaParserLabeled::innerCreator() {
  InnerCreatorContext *_localctx = _tracker.createInstance<InnerCreatorContext>(_ctx, getState());
  enterRule(_localctx, 182, JavaParserLabeled::RuleInnerCreator);
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
    match(JavaParserLabeled::IDENTIFIER);
    setState(1310);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JavaParserLabeled::LT) {
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

JavaParserLabeled::ArrayCreatorRestContext::ArrayCreatorRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ArrayCreatorRestContext::LBRACK() {
  return getTokens(JavaParserLabeled::LBRACK);
}

tree::TerminalNode* JavaParserLabeled::ArrayCreatorRestContext::LBRACK(size_t i) {
  return getToken(JavaParserLabeled::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::ArrayCreatorRestContext::RBRACK() {
  return getTokens(JavaParserLabeled::RBRACK);
}

tree::TerminalNode* JavaParserLabeled::ArrayCreatorRestContext::RBRACK(size_t i) {
  return getToken(JavaParserLabeled::RBRACK, i);
}

JavaParserLabeled::ArrayInitializerContext* JavaParserLabeled::ArrayCreatorRestContext::arrayInitializer() {
  return getRuleContext<JavaParserLabeled::ArrayInitializerContext>(0);
}

std::vector<JavaParserLabeled::ExpressionContext *> JavaParserLabeled::ArrayCreatorRestContext::expression() {
  return getRuleContexts<JavaParserLabeled::ExpressionContext>();
}

JavaParserLabeled::ExpressionContext* JavaParserLabeled::ArrayCreatorRestContext::expression(size_t i) {
  return getRuleContext<JavaParserLabeled::ExpressionContext>(i);
}


size_t JavaParserLabeled::ArrayCreatorRestContext::getRuleIndex() const {
  return JavaParserLabeled::RuleArrayCreatorRest;
}

void JavaParserLabeled::ArrayCreatorRestContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterArrayCreatorRest(this);
}

void JavaParserLabeled::ArrayCreatorRestContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitArrayCreatorRest(this);
}


antlrcpp::Any JavaParserLabeled::ArrayCreatorRestContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitArrayCreatorRest(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ArrayCreatorRestContext* JavaParserLabeled::arrayCreatorRest() {
  ArrayCreatorRestContext *_localctx = _tracker.createInstance<ArrayCreatorRestContext>(_ctx, getState());
  enterRule(_localctx, 184, JavaParserLabeled::RuleArrayCreatorRest);
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
    match(JavaParserLabeled::LBRACK);
    setState(1342);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JavaParserLabeled::RBRACK: {
        setState(1315);
        match(JavaParserLabeled::RBRACK);
        setState(1320);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while (_la == JavaParserLabeled::LBRACK) {
          setState(1316);
          match(JavaParserLabeled::LBRACK);
          setState(1317);
          match(JavaParserLabeled::RBRACK);
          setState(1322);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        setState(1323);
        arrayInitializer();
        break;
      }

      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::NEW:
      case JavaParserLabeled::SHORT:
      case JavaParserLabeled::SUPER:
      case JavaParserLabeled::THIS:
      case JavaParserLabeled::VOID:
      case JavaParserLabeled::DECIMAL_LITERAL:
      case JavaParserLabeled::HEX_LITERAL:
      case JavaParserLabeled::OCT_LITERAL:
      case JavaParserLabeled::BINARY_LITERAL:
      case JavaParserLabeled::FLOAT_LITERAL:
      case JavaParserLabeled::HEX_FLOAT_LITERAL:
      case JavaParserLabeled::BOOL_LITERAL:
      case JavaParserLabeled::CHAR_LITERAL:
      case JavaParserLabeled::STRING_LITERAL:
      case JavaParserLabeled::NULL_LITERAL:
      case JavaParserLabeled::LPAREN:
      case JavaParserLabeled::LT:
      case JavaParserLabeled::BANG:
      case JavaParserLabeled::TILDE:
      case JavaParserLabeled::INC:
      case JavaParserLabeled::DEC:
      case JavaParserLabeled::ADD:
      case JavaParserLabeled::SUB:
      case JavaParserLabeled::AT:
      case JavaParserLabeled::IDENTIFIER: {
        setState(1324);
        expression(0);
        setState(1325);
        match(JavaParserLabeled::RBRACK);
        setState(1332);
        _errHandler->sync(this);
        alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 162, _ctx);
        while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
          if (alt == 1) {
            setState(1326);
            match(JavaParserLabeled::LBRACK);
            setState(1327);
            expression(0);
            setState(1328);
            match(JavaParserLabeled::RBRACK); 
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
            match(JavaParserLabeled::LBRACK);
            setState(1336);
            match(JavaParserLabeled::RBRACK); 
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

JavaParserLabeled::ClassCreatorRestContext::ClassCreatorRestContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::ArgumentsContext* JavaParserLabeled::ClassCreatorRestContext::arguments() {
  return getRuleContext<JavaParserLabeled::ArgumentsContext>(0);
}

JavaParserLabeled::ClassBodyContext* JavaParserLabeled::ClassCreatorRestContext::classBody() {
  return getRuleContext<JavaParserLabeled::ClassBodyContext>(0);
}


size_t JavaParserLabeled::ClassCreatorRestContext::getRuleIndex() const {
  return JavaParserLabeled::RuleClassCreatorRest;
}

void JavaParserLabeled::ClassCreatorRestContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterClassCreatorRest(this);
}

void JavaParserLabeled::ClassCreatorRestContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitClassCreatorRest(this);
}


antlrcpp::Any JavaParserLabeled::ClassCreatorRestContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitClassCreatorRest(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ClassCreatorRestContext* JavaParserLabeled::classCreatorRest() {
  ClassCreatorRestContext *_localctx = _tracker.createInstance<ClassCreatorRestContext>(_ctx, getState());
  enterRule(_localctx, 186, JavaParserLabeled::RuleClassCreatorRest);

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

JavaParserLabeled::ExplicitGenericInvocationContext::ExplicitGenericInvocationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::NonWildcardTypeArgumentsContext* JavaParserLabeled::ExplicitGenericInvocationContext::nonWildcardTypeArguments() {
  return getRuleContext<JavaParserLabeled::NonWildcardTypeArgumentsContext>(0);
}

JavaParserLabeled::ExplicitGenericInvocationSuffixContext* JavaParserLabeled::ExplicitGenericInvocationContext::explicitGenericInvocationSuffix() {
  return getRuleContext<JavaParserLabeled::ExplicitGenericInvocationSuffixContext>(0);
}


size_t JavaParserLabeled::ExplicitGenericInvocationContext::getRuleIndex() const {
  return JavaParserLabeled::RuleExplicitGenericInvocation;
}

void JavaParserLabeled::ExplicitGenericInvocationContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExplicitGenericInvocation(this);
}

void JavaParserLabeled::ExplicitGenericInvocationContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExplicitGenericInvocation(this);
}


antlrcpp::Any JavaParserLabeled::ExplicitGenericInvocationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExplicitGenericInvocation(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ExplicitGenericInvocationContext* JavaParserLabeled::explicitGenericInvocation() {
  ExplicitGenericInvocationContext *_localctx = _tracker.createInstance<ExplicitGenericInvocationContext>(_ctx, getState());
  enterRule(_localctx, 188, JavaParserLabeled::RuleExplicitGenericInvocation);

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

JavaParserLabeled::TypeArgumentsOrDiamondContext::TypeArgumentsOrDiamondContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::TypeArgumentsOrDiamondContext::LT() {
  return getToken(JavaParserLabeled::LT, 0);
}

tree::TerminalNode* JavaParserLabeled::TypeArgumentsOrDiamondContext::GT() {
  return getToken(JavaParserLabeled::GT, 0);
}

JavaParserLabeled::TypeArgumentsContext* JavaParserLabeled::TypeArgumentsOrDiamondContext::typeArguments() {
  return getRuleContext<JavaParserLabeled::TypeArgumentsContext>(0);
}


size_t JavaParserLabeled::TypeArgumentsOrDiamondContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeArgumentsOrDiamond;
}

void JavaParserLabeled::TypeArgumentsOrDiamondContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeArgumentsOrDiamond(this);
}

void JavaParserLabeled::TypeArgumentsOrDiamondContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeArgumentsOrDiamond(this);
}


antlrcpp::Any JavaParserLabeled::TypeArgumentsOrDiamondContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeArgumentsOrDiamond(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeArgumentsOrDiamondContext* JavaParserLabeled::typeArgumentsOrDiamond() {
  TypeArgumentsOrDiamondContext *_localctx = _tracker.createInstance<TypeArgumentsOrDiamondContext>(_ctx, getState());
  enterRule(_localctx, 190, JavaParserLabeled::RuleTypeArgumentsOrDiamond);

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
      match(JavaParserLabeled::LT);
      setState(1352);
      match(JavaParserLabeled::GT);
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

JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext::NonWildcardTypeArgumentsOrDiamondContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext::LT() {
  return getToken(JavaParserLabeled::LT, 0);
}

tree::TerminalNode* JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext::GT() {
  return getToken(JavaParserLabeled::GT, 0);
}

JavaParserLabeled::NonWildcardTypeArgumentsContext* JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext::nonWildcardTypeArguments() {
  return getRuleContext<JavaParserLabeled::NonWildcardTypeArgumentsContext>(0);
}


size_t JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext::getRuleIndex() const {
  return JavaParserLabeled::RuleNonWildcardTypeArgumentsOrDiamond;
}

void JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterNonWildcardTypeArgumentsOrDiamond(this);
}

void JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitNonWildcardTypeArgumentsOrDiamond(this);
}


antlrcpp::Any JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitNonWildcardTypeArgumentsOrDiamond(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::NonWildcardTypeArgumentsOrDiamondContext* JavaParserLabeled::nonWildcardTypeArgumentsOrDiamond() {
  NonWildcardTypeArgumentsOrDiamondContext *_localctx = _tracker.createInstance<NonWildcardTypeArgumentsOrDiamondContext>(_ctx, getState());
  enterRule(_localctx, 192, JavaParserLabeled::RuleNonWildcardTypeArgumentsOrDiamond);

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
      match(JavaParserLabeled::LT);
      setState(1357);
      match(JavaParserLabeled::GT);
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

JavaParserLabeled::NonWildcardTypeArgumentsContext::NonWildcardTypeArgumentsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::NonWildcardTypeArgumentsContext::LT() {
  return getToken(JavaParserLabeled::LT, 0);
}

JavaParserLabeled::TypeListContext* JavaParserLabeled::NonWildcardTypeArgumentsContext::typeList() {
  return getRuleContext<JavaParserLabeled::TypeListContext>(0);
}

tree::TerminalNode* JavaParserLabeled::NonWildcardTypeArgumentsContext::GT() {
  return getToken(JavaParserLabeled::GT, 0);
}


size_t JavaParserLabeled::NonWildcardTypeArgumentsContext::getRuleIndex() const {
  return JavaParserLabeled::RuleNonWildcardTypeArguments;
}

void JavaParserLabeled::NonWildcardTypeArgumentsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterNonWildcardTypeArguments(this);
}

void JavaParserLabeled::NonWildcardTypeArgumentsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitNonWildcardTypeArguments(this);
}


antlrcpp::Any JavaParserLabeled::NonWildcardTypeArgumentsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitNonWildcardTypeArguments(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::NonWildcardTypeArgumentsContext* JavaParserLabeled::nonWildcardTypeArguments() {
  NonWildcardTypeArgumentsContext *_localctx = _tracker.createInstance<NonWildcardTypeArgumentsContext>(_ctx, getState());
  enterRule(_localctx, 194, JavaParserLabeled::RuleNonWildcardTypeArguments);

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
    match(JavaParserLabeled::LT);
    setState(1362);
    typeList();
    setState(1363);
    match(JavaParserLabeled::GT);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TypeListContext ------------------------------------------------------------------

JavaParserLabeled::TypeListContext::TypeListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<JavaParserLabeled::TypeTypeContext *> JavaParserLabeled::TypeListContext::typeType() {
  return getRuleContexts<JavaParserLabeled::TypeTypeContext>();
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::TypeListContext::typeType(size_t i) {
  return getRuleContext<JavaParserLabeled::TypeTypeContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::TypeListContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::TypeListContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::TypeListContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeList;
}

void JavaParserLabeled::TypeListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeList(this);
}

void JavaParserLabeled::TypeListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeList(this);
}


antlrcpp::Any JavaParserLabeled::TypeListContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeList(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeListContext* JavaParserLabeled::typeList() {
  TypeListContext *_localctx = _tracker.createInstance<TypeListContext>(_ctx, getState());
  enterRule(_localctx, 196, JavaParserLabeled::RuleTypeList);
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
    while (_la == JavaParserLabeled::COMMA) {
      setState(1366);
      match(JavaParserLabeled::COMMA);
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

JavaParserLabeled::TypeTypeContext::TypeTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JavaParserLabeled::ClassOrInterfaceTypeContext* JavaParserLabeled::TypeTypeContext::classOrInterfaceType() {
  return getRuleContext<JavaParserLabeled::ClassOrInterfaceTypeContext>(0);
}

JavaParserLabeled::PrimitiveTypeContext* JavaParserLabeled::TypeTypeContext::primitiveType() {
  return getRuleContext<JavaParserLabeled::PrimitiveTypeContext>(0);
}

std::vector<JavaParserLabeled::AnnotationContext *> JavaParserLabeled::TypeTypeContext::annotation() {
  return getRuleContexts<JavaParserLabeled::AnnotationContext>();
}

JavaParserLabeled::AnnotationContext* JavaParserLabeled::TypeTypeContext::annotation(size_t i) {
  return getRuleContext<JavaParserLabeled::AnnotationContext>(i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::TypeTypeContext::LBRACK() {
  return getTokens(JavaParserLabeled::LBRACK);
}

tree::TerminalNode* JavaParserLabeled::TypeTypeContext::LBRACK(size_t i) {
  return getToken(JavaParserLabeled::LBRACK, i);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::TypeTypeContext::RBRACK() {
  return getTokens(JavaParserLabeled::RBRACK);
}

tree::TerminalNode* JavaParserLabeled::TypeTypeContext::RBRACK(size_t i) {
  return getToken(JavaParserLabeled::RBRACK, i);
}


size_t JavaParserLabeled::TypeTypeContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeType;
}

void JavaParserLabeled::TypeTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeType(this);
}

void JavaParserLabeled::TypeTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeType(this);
}


antlrcpp::Any JavaParserLabeled::TypeTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeType(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeTypeContext* JavaParserLabeled::typeType() {
  TypeTypeContext *_localctx = _tracker.createInstance<TypeTypeContext>(_ctx, getState());
  enterRule(_localctx, 198, JavaParserLabeled::RuleTypeType);
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
      case JavaParserLabeled::IDENTIFIER: {
        setState(1379);
        classOrInterfaceType();
        break;
      }

      case JavaParserLabeled::BOOLEAN:
      case JavaParserLabeled::BYTE:
      case JavaParserLabeled::CHAR:
      case JavaParserLabeled::DOUBLE:
      case JavaParserLabeled::FLOAT:
      case JavaParserLabeled::INT:
      case JavaParserLabeled::LONG:
      case JavaParserLabeled::SHORT: {
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
        while (_la == JavaParserLabeled::AT

        || _la == JavaParserLabeled::IDENTIFIER) {
          setState(1383);
          annotation();
          setState(1388);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        setState(1389);
        match(JavaParserLabeled::LBRACK);
        setState(1390);
        match(JavaParserLabeled::RBRACK); 
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

JavaParserLabeled::PrimitiveTypeContext::PrimitiveTypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::PrimitiveTypeContext::BOOLEAN() {
  return getToken(JavaParserLabeled::BOOLEAN, 0);
}

tree::TerminalNode* JavaParserLabeled::PrimitiveTypeContext::CHAR() {
  return getToken(JavaParserLabeled::CHAR, 0);
}

tree::TerminalNode* JavaParserLabeled::PrimitiveTypeContext::BYTE() {
  return getToken(JavaParserLabeled::BYTE, 0);
}

tree::TerminalNode* JavaParserLabeled::PrimitiveTypeContext::SHORT() {
  return getToken(JavaParserLabeled::SHORT, 0);
}

tree::TerminalNode* JavaParserLabeled::PrimitiveTypeContext::INT() {
  return getToken(JavaParserLabeled::INT, 0);
}

tree::TerminalNode* JavaParserLabeled::PrimitiveTypeContext::LONG() {
  return getToken(JavaParserLabeled::LONG, 0);
}

tree::TerminalNode* JavaParserLabeled::PrimitiveTypeContext::FLOAT() {
  return getToken(JavaParserLabeled::FLOAT, 0);
}

tree::TerminalNode* JavaParserLabeled::PrimitiveTypeContext::DOUBLE() {
  return getToken(JavaParserLabeled::DOUBLE, 0);
}


size_t JavaParserLabeled::PrimitiveTypeContext::getRuleIndex() const {
  return JavaParserLabeled::RulePrimitiveType;
}

void JavaParserLabeled::PrimitiveTypeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrimitiveType(this);
}

void JavaParserLabeled::PrimitiveTypeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrimitiveType(this);
}


antlrcpp::Any JavaParserLabeled::PrimitiveTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitPrimitiveType(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::PrimitiveTypeContext* JavaParserLabeled::primitiveType() {
  PrimitiveTypeContext *_localctx = _tracker.createInstance<PrimitiveTypeContext>(_ctx, getState());
  enterRule(_localctx, 200, JavaParserLabeled::RulePrimitiveType);
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
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::SHORT))) != 0))) {
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

JavaParserLabeled::TypeArgumentsContext::TypeArgumentsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::TypeArgumentsContext::LT() {
  return getToken(JavaParserLabeled::LT, 0);
}

std::vector<JavaParserLabeled::TypeArgumentContext *> JavaParserLabeled::TypeArgumentsContext::typeArgument() {
  return getRuleContexts<JavaParserLabeled::TypeArgumentContext>();
}

JavaParserLabeled::TypeArgumentContext* JavaParserLabeled::TypeArgumentsContext::typeArgument(size_t i) {
  return getRuleContext<JavaParserLabeled::TypeArgumentContext>(i);
}

tree::TerminalNode* JavaParserLabeled::TypeArgumentsContext::GT() {
  return getToken(JavaParserLabeled::GT, 0);
}

std::vector<tree::TerminalNode *> JavaParserLabeled::TypeArgumentsContext::COMMA() {
  return getTokens(JavaParserLabeled::COMMA);
}

tree::TerminalNode* JavaParserLabeled::TypeArgumentsContext::COMMA(size_t i) {
  return getToken(JavaParserLabeled::COMMA, i);
}


size_t JavaParserLabeled::TypeArgumentsContext::getRuleIndex() const {
  return JavaParserLabeled::RuleTypeArguments;
}

void JavaParserLabeled::TypeArgumentsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTypeArguments(this);
}

void JavaParserLabeled::TypeArgumentsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTypeArguments(this);
}


antlrcpp::Any JavaParserLabeled::TypeArgumentsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitTypeArguments(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::TypeArgumentsContext* JavaParserLabeled::typeArguments() {
  TypeArgumentsContext *_localctx = _tracker.createInstance<TypeArgumentsContext>(_ctx, getState());
  enterRule(_localctx, 202, JavaParserLabeled::RuleTypeArguments);
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
    match(JavaParserLabeled::LT);
    setState(1399);
    typeArgument();
    setState(1404);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JavaParserLabeled::COMMA) {
      setState(1400);
      match(JavaParserLabeled::COMMA);
      setState(1401);
      typeArgument();
      setState(1406);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(1407);
    match(JavaParserLabeled::GT);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SuperSuffixContext ------------------------------------------------------------------

JavaParserLabeled::SuperSuffixContext::SuperSuffixContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::SuperSuffixContext::getRuleIndex() const {
  return JavaParserLabeled::RuleSuperSuffix;
}

void JavaParserLabeled::SuperSuffixContext::copyFrom(SuperSuffixContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- SuperSuffix1Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::SuperSuffix1Context::DOT() {
  return getToken(JavaParserLabeled::DOT, 0);
}

tree::TerminalNode* JavaParserLabeled::SuperSuffix1Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::ArgumentsContext* JavaParserLabeled::SuperSuffix1Context::arguments() {
  return getRuleContext<JavaParserLabeled::ArgumentsContext>(0);
}

JavaParserLabeled::SuperSuffix1Context::SuperSuffix1Context(SuperSuffixContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::SuperSuffix1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSuperSuffix1(this);
}
void JavaParserLabeled::SuperSuffix1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSuperSuffix1(this);
}

antlrcpp::Any JavaParserLabeled::SuperSuffix1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitSuperSuffix1(this);
  else
    return visitor->visitChildren(this);
}
//----------------- SuperSuffix0Context ------------------------------------------------------------------

JavaParserLabeled::ArgumentsContext* JavaParserLabeled::SuperSuffix0Context::arguments() {
  return getRuleContext<JavaParserLabeled::ArgumentsContext>(0);
}

JavaParserLabeled::SuperSuffix0Context::SuperSuffix0Context(SuperSuffixContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::SuperSuffix0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSuperSuffix0(this);
}
void JavaParserLabeled::SuperSuffix0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSuperSuffix0(this);
}

antlrcpp::Any JavaParserLabeled::SuperSuffix0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitSuperSuffix0(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::SuperSuffixContext* JavaParserLabeled::superSuffix() {
  SuperSuffixContext *_localctx = _tracker.createInstance<SuperSuffixContext>(_ctx, getState());
  enterRule(_localctx, 204, JavaParserLabeled::RuleSuperSuffix);

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
      case JavaParserLabeled::LPAREN: {
        _localctx = dynamic_cast<SuperSuffixContext *>(_tracker.createInstance<JavaParserLabeled::SuperSuffix0Context>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(1409);
        arguments();
        break;
      }

      case JavaParserLabeled::DOT: {
        _localctx = dynamic_cast<SuperSuffixContext *>(_tracker.createInstance<JavaParserLabeled::SuperSuffix1Context>(_localctx));
        enterOuterAlt(_localctx, 2);
        setState(1410);
        match(JavaParserLabeled::DOT);
        setState(1411);
        match(JavaParserLabeled::IDENTIFIER);
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

JavaParserLabeled::ExplicitGenericInvocationSuffixContext::ExplicitGenericInvocationSuffixContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t JavaParserLabeled::ExplicitGenericInvocationSuffixContext::getRuleIndex() const {
  return JavaParserLabeled::RuleExplicitGenericInvocationSuffix;
}

void JavaParserLabeled::ExplicitGenericInvocationSuffixContext::copyFrom(ExplicitGenericInvocationSuffixContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- ExplicitGenericInvocationSuffix0Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::ExplicitGenericInvocationSuffix0Context::SUPER() {
  return getToken(JavaParserLabeled::SUPER, 0);
}

JavaParserLabeled::SuperSuffixContext* JavaParserLabeled::ExplicitGenericInvocationSuffix0Context::superSuffix() {
  return getRuleContext<JavaParserLabeled::SuperSuffixContext>(0);
}

JavaParserLabeled::ExplicitGenericInvocationSuffix0Context::ExplicitGenericInvocationSuffix0Context(ExplicitGenericInvocationSuffixContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ExplicitGenericInvocationSuffix0Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExplicitGenericInvocationSuffix0(this);
}
void JavaParserLabeled::ExplicitGenericInvocationSuffix0Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExplicitGenericInvocationSuffix0(this);
}

antlrcpp::Any JavaParserLabeled::ExplicitGenericInvocationSuffix0Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExplicitGenericInvocationSuffix0(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ExplicitGenericInvocationSuffix1Context ------------------------------------------------------------------

tree::TerminalNode* JavaParserLabeled::ExplicitGenericInvocationSuffix1Context::IDENTIFIER() {
  return getToken(JavaParserLabeled::IDENTIFIER, 0);
}

JavaParserLabeled::ArgumentsContext* JavaParserLabeled::ExplicitGenericInvocationSuffix1Context::arguments() {
  return getRuleContext<JavaParserLabeled::ArgumentsContext>(0);
}

JavaParserLabeled::ExplicitGenericInvocationSuffix1Context::ExplicitGenericInvocationSuffix1Context(ExplicitGenericInvocationSuffixContext *ctx) { copyFrom(ctx); }

void JavaParserLabeled::ExplicitGenericInvocationSuffix1Context::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExplicitGenericInvocationSuffix1(this);
}
void JavaParserLabeled::ExplicitGenericInvocationSuffix1Context::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExplicitGenericInvocationSuffix1(this);
}

antlrcpp::Any JavaParserLabeled::ExplicitGenericInvocationSuffix1Context::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitExplicitGenericInvocationSuffix1(this);
  else
    return visitor->visitChildren(this);
}
JavaParserLabeled::ExplicitGenericInvocationSuffixContext* JavaParserLabeled::explicitGenericInvocationSuffix() {
  ExplicitGenericInvocationSuffixContext *_localctx = _tracker.createInstance<ExplicitGenericInvocationSuffixContext>(_ctx, getState());
  enterRule(_localctx, 206, JavaParserLabeled::RuleExplicitGenericInvocationSuffix);

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
      case JavaParserLabeled::SUPER: {
        _localctx = dynamic_cast<ExplicitGenericInvocationSuffixContext *>(_tracker.createInstance<JavaParserLabeled::ExplicitGenericInvocationSuffix0Context>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(1417);
        match(JavaParserLabeled::SUPER);
        setState(1418);
        superSuffix();
        break;
      }

      case JavaParserLabeled::IDENTIFIER: {
        _localctx = dynamic_cast<ExplicitGenericInvocationSuffixContext *>(_tracker.createInstance<JavaParserLabeled::ExplicitGenericInvocationSuffix1Context>(_localctx));
        enterOuterAlt(_localctx, 2);
        setState(1419);
        match(JavaParserLabeled::IDENTIFIER);
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

JavaParserLabeled::ArgumentsContext::ArgumentsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JavaParserLabeled::ArgumentsContext::LPAREN() {
  return getToken(JavaParserLabeled::LPAREN, 0);
}

tree::TerminalNode* JavaParserLabeled::ArgumentsContext::RPAREN() {
  return getToken(JavaParserLabeled::RPAREN, 0);
}

JavaParserLabeled::ExpressionListContext* JavaParserLabeled::ArgumentsContext::expressionList() {
  return getRuleContext<JavaParserLabeled::ExpressionListContext>(0);
}


size_t JavaParserLabeled::ArgumentsContext::getRuleIndex() const {
  return JavaParserLabeled::RuleArguments;
}

void JavaParserLabeled::ArgumentsContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterArguments(this);
}

void JavaParserLabeled::ArgumentsContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JavaParserLabeledListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitArguments(this);
}


antlrcpp::Any JavaParserLabeled::ArgumentsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JavaParserLabeledVisitor*>(visitor))
    return parserVisitor->visitArguments(this);
  else
    return visitor->visitChildren(this);
}

JavaParserLabeled::ArgumentsContext* JavaParserLabeled::arguments() {
  ArgumentsContext *_localctx = _tracker.createInstance<ArgumentsContext>(_ctx, getState());
  enterRule(_localctx, 208, JavaParserLabeled::RuleArguments);
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
    match(JavaParserLabeled::LPAREN);
    setState(1425);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << JavaParserLabeled::BOOLEAN)
      | (1ULL << JavaParserLabeled::BYTE)
      | (1ULL << JavaParserLabeled::CHAR)
      | (1ULL << JavaParserLabeled::DOUBLE)
      | (1ULL << JavaParserLabeled::FLOAT)
      | (1ULL << JavaParserLabeled::INT)
      | (1ULL << JavaParserLabeled::LONG)
      | (1ULL << JavaParserLabeled::NEW)
      | (1ULL << JavaParserLabeled::SHORT)
      | (1ULL << JavaParserLabeled::SUPER)
      | (1ULL << JavaParserLabeled::THIS)
      | (1ULL << JavaParserLabeled::VOID)
      | (1ULL << JavaParserLabeled::DECIMAL_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_LITERAL)
      | (1ULL << JavaParserLabeled::OCT_LITERAL)
      | (1ULL << JavaParserLabeled::BINARY_LITERAL)
      | (1ULL << JavaParserLabeled::FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::HEX_FLOAT_LITERAL)
      | (1ULL << JavaParserLabeled::BOOL_LITERAL)
      | (1ULL << JavaParserLabeled::CHAR_LITERAL)
      | (1ULL << JavaParserLabeled::STRING_LITERAL)
      | (1ULL << JavaParserLabeled::NULL_LITERAL)
      | (1ULL << JavaParserLabeled::LPAREN))) != 0) || ((((_la - 72) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 72)) & ((1ULL << (JavaParserLabeled::LT - 72))
      | (1ULL << (JavaParserLabeled::BANG - 72))
      | (1ULL << (JavaParserLabeled::TILDE - 72))
      | (1ULL << (JavaParserLabeled::INC - 72))
      | (1ULL << (JavaParserLabeled::DEC - 72))
      | (1ULL << (JavaParserLabeled::ADD - 72))
      | (1ULL << (JavaParserLabeled::SUB - 72))
      | (1ULL << (JavaParserLabeled::AT - 72))
      | (1ULL << (JavaParserLabeled::IDENTIFIER - 72)))) != 0)) {
      setState(1424);
      expressionList();
    }
    setState(1427);
    match(JavaParserLabeled::RPAREN);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

bool JavaParserLabeled::sempred(RuleContext *context, size_t ruleIndex, size_t predicateIndex) {
  switch (ruleIndex) {
    case 83: return expressionSempred(dynamic_cast<ExpressionContext *>(context), predicateIndex);

  default:
    break;
  }
  return true;
}

bool JavaParserLabeled::expressionSempred(ExpressionContext *_localctx, size_t predicateIndex) {
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
std::vector<dfa::DFA> JavaParserLabeled::_decisionToDFA;
atn::PredictionContextCache JavaParserLabeled::_sharedContextCache;

// We own the ATN which in turn owns the ATN states.
atn::ATN JavaParserLabeled::_atn;
std::vector<uint16_t> JavaParserLabeled::_serializedATN;

std::vector<std::string> JavaParserLabeled::_ruleNames = {
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

std::vector<std::string> JavaParserLabeled::_literalNames = {
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

std::vector<std::string> JavaParserLabeled::_symbolicNames = {
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

dfa::Vocabulary JavaParserLabeled::_vocabulary(_literalNames, _symbolicNames);

std::vector<std::string> JavaParserLabeled::_tokenNames;

JavaParserLabeled::Initializer::Initializer() {
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

  _serializedATN = {
    0x3, 0x608b, 0xa72a, 0x8133, 0xb9ed, 0x417c, 0x3be7, 0x7786, 0x5964, 
    0x3, 0x71, 0x598, 0x4, 0x2, 0x9, 0x2, 0x4, 0x3, 0x9, 0x3, 0x4, 0x4, 
    0x9, 0x4, 0x4, 0x5, 0x9, 0x5, 0x4, 0x6, 0x9, 0x6, 0x4, 0x7, 0x9, 0x7, 
    0x4, 0x8, 0x9, 0x8, 0x4, 0x9, 0x9, 0x9, 0x4, 0xa, 0x9, 0xa, 0x4, 0xb, 
    0x9, 0xb, 0x4, 0xc, 0x9, 0xc, 0x4, 0xd, 0x9, 0xd, 0x4, 0xe, 0x9, 0xe, 
    0x4, 0xf, 0x9, 0xf, 0x4, 0x10, 0x9, 0x10, 0x4, 0x11, 0x9, 0x11, 0x4, 
    0x12, 0x9, 0x12, 0x4, 0x13, 0x9, 0x13, 0x4, 0x14, 0x9, 0x14, 0x4, 0x15, 
    0x9, 0x15, 0x4, 0x16, 0x9, 0x16, 0x4, 0x17, 0x9, 0x17, 0x4, 0x18, 0x9, 
    0x18, 0x4, 0x19, 0x9, 0x19, 0x4, 0x1a, 0x9, 0x1a, 0x4, 0x1b, 0x9, 0x1b, 
    0x4, 0x1c, 0x9, 0x1c, 0x4, 0x1d, 0x9, 0x1d, 0x4, 0x1e, 0x9, 0x1e, 0x4, 
    0x1f, 0x9, 0x1f, 0x4, 0x20, 0x9, 0x20, 0x4, 0x21, 0x9, 0x21, 0x4, 0x22, 
    0x9, 0x22, 0x4, 0x23, 0x9, 0x23, 0x4, 0x24, 0x9, 0x24, 0x4, 0x25, 0x9, 
    0x25, 0x4, 0x26, 0x9, 0x26, 0x4, 0x27, 0x9, 0x27, 0x4, 0x28, 0x9, 0x28, 
    0x4, 0x29, 0x9, 0x29, 0x4, 0x2a, 0x9, 0x2a, 0x4, 0x2b, 0x9, 0x2b, 0x4, 
    0x2c, 0x9, 0x2c, 0x4, 0x2d, 0x9, 0x2d, 0x4, 0x2e, 0x9, 0x2e, 0x4, 0x2f, 
    0x9, 0x2f, 0x4, 0x30, 0x9, 0x30, 0x4, 0x31, 0x9, 0x31, 0x4, 0x32, 0x9, 
    0x32, 0x4, 0x33, 0x9, 0x33, 0x4, 0x34, 0x9, 0x34, 0x4, 0x35, 0x9, 0x35, 
    0x4, 0x36, 0x9, 0x36, 0x4, 0x37, 0x9, 0x37, 0x4, 0x38, 0x9, 0x38, 0x4, 
    0x39, 0x9, 0x39, 0x4, 0x3a, 0x9, 0x3a, 0x4, 0x3b, 0x9, 0x3b, 0x4, 0x3c, 
    0x9, 0x3c, 0x4, 0x3d, 0x9, 0x3d, 0x4, 0x3e, 0x9, 0x3e, 0x4, 0x3f, 0x9, 
    0x3f, 0x4, 0x40, 0x9, 0x40, 0x4, 0x41, 0x9, 0x41, 0x4, 0x42, 0x9, 0x42, 
    0x4, 0x43, 0x9, 0x43, 0x4, 0x44, 0x9, 0x44, 0x4, 0x45, 0x9, 0x45, 0x4, 
    0x46, 0x9, 0x46, 0x4, 0x47, 0x9, 0x47, 0x4, 0x48, 0x9, 0x48, 0x4, 0x49, 
    0x9, 0x49, 0x4, 0x4a, 0x9, 0x4a, 0x4, 0x4b, 0x9, 0x4b, 0x4, 0x4c, 0x9, 
    0x4c, 0x4, 0x4d, 0x9, 0x4d, 0x4, 0x4e, 0x9, 0x4e, 0x4, 0x4f, 0x9, 0x4f, 
    0x4, 0x50, 0x9, 0x50, 0x4, 0x51, 0x9, 0x51, 0x4, 0x52, 0x9, 0x52, 0x4, 
    0x53, 0x9, 0x53, 0x4, 0x54, 0x9, 0x54, 0x4, 0x55, 0x9, 0x55, 0x4, 0x56, 
    0x9, 0x56, 0x4, 0x57, 0x9, 0x57, 0x4, 0x58, 0x9, 0x58, 0x4, 0x59, 0x9, 
    0x59, 0x4, 0x5a, 0x9, 0x5a, 0x4, 0x5b, 0x9, 0x5b, 0x4, 0x5c, 0x9, 0x5c, 
    0x4, 0x5d, 0x9, 0x5d, 0x4, 0x5e, 0x9, 0x5e, 0x4, 0x5f, 0x9, 0x5f, 0x4, 
    0x60, 0x9, 0x60, 0x4, 0x61, 0x9, 0x61, 0x4, 0x62, 0x9, 0x62, 0x4, 0x63, 
    0x9, 0x63, 0x4, 0x64, 0x9, 0x64, 0x4, 0x65, 0x9, 0x65, 0x4, 0x66, 0x9, 
    0x66, 0x4, 0x67, 0x9, 0x67, 0x4, 0x68, 0x9, 0x68, 0x4, 0x69, 0x9, 0x69, 
    0x4, 0x6a, 0x9, 0x6a, 0x3, 0x2, 0x5, 0x2, 0xd6, 0xa, 0x2, 0x3, 0x2, 
    0x7, 0x2, 0xd9, 0xa, 0x2, 0xc, 0x2, 0xe, 0x2, 0xdc, 0xb, 0x2, 0x3, 0x2, 
    0x7, 0x2, 0xdf, 0xa, 0x2, 0xc, 0x2, 0xe, 0x2, 0xe2, 0xb, 0x2, 0x3, 0x2, 
    0x3, 0x2, 0x3, 0x3, 0x7, 0x3, 0xe7, 0xa, 0x3, 0xc, 0x3, 0xe, 0x3, 0xea, 
    0xb, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x4, 0x3, 0x4, 
    0x5, 0x4, 0xf2, 0xa, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x5, 0x4, 0xf7, 
    0xa, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x5, 0x7, 0x5, 0xfc, 0xa, 0x5, 0xc, 
    0x5, 0xe, 0x5, 0xff, 0xb, 0x5, 0x3, 0x5, 0x3, 0x5, 0x3, 0x5, 0x3, 0x5, 
    0x5, 0x5, 0x105, 0xa, 0x5, 0x3, 0x5, 0x5, 0x5, 0x108, 0xa, 0x5, 0x3, 
    0x6, 0x3, 0x6, 0x3, 0x6, 0x3, 0x6, 0x3, 0x6, 0x5, 0x6, 0x10f, 0xa, 0x6, 
    0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 
    0x3, 0x7, 0x5, 0x7, 0x119, 0xa, 0x7, 0x3, 0x8, 0x3, 0x8, 0x5, 0x8, 0x11d, 
    0xa, 0x8, 0x3, 0x9, 0x3, 0x9, 0x3, 0x9, 0x5, 0x9, 0x122, 0xa, 0x9, 0x3, 
    0x9, 0x3, 0x9, 0x5, 0x9, 0x126, 0xa, 0x9, 0x3, 0x9, 0x3, 0x9, 0x5, 0x9, 
    0x12a, 0xa, 0x9, 0x3, 0x9, 0x3, 0x9, 0x3, 0xa, 0x3, 0xa, 0x3, 0xa, 0x3, 
    0xa, 0x7, 0xa, 0x132, 0xa, 0xa, 0xc, 0xa, 0xe, 0xa, 0x135, 0xb, 0xa, 
    0x3, 0xa, 0x3, 0xa, 0x3, 0xb, 0x7, 0xb, 0x13a, 0xa, 0xb, 0xc, 0xb, 0xe, 
    0xb, 0x13d, 0xb, 0xb, 0x3, 0xb, 0x3, 0xb, 0x3, 0xb, 0x7, 0xb, 0x142, 
    0xa, 0xb, 0xc, 0xb, 0xe, 0xb, 0x145, 0xb, 0xb, 0x3, 0xb, 0x5, 0xb, 0x148, 
    0xa, 0xb, 0x3, 0xc, 0x3, 0xc, 0x3, 0xc, 0x7, 0xc, 0x14d, 0xa, 0xc, 0xc, 
    0xc, 0xe, 0xc, 0x150, 0xb, 0xc, 0x3, 0xd, 0x3, 0xd, 0x3, 0xd, 0x3, 0xd, 
    0x5, 0xd, 0x156, 0xa, 0xd, 0x3, 0xd, 0x3, 0xd, 0x5, 0xd, 0x15a, 0xa, 
    0xd, 0x3, 0xd, 0x5, 0xd, 0x15d, 0xa, 0xd, 0x3, 0xd, 0x5, 0xd, 0x160, 
    0xa, 0xd, 0x3, 0xd, 0x3, 0xd, 0x3, 0xe, 0x3, 0xe, 0x3, 0xe, 0x7, 0xe, 
    0x167, 0xa, 0xe, 0xc, 0xe, 0xe, 0xe, 0x16a, 0xb, 0xe, 0x3, 0xf, 0x7, 
    0xf, 0x16d, 0xa, 0xf, 0xc, 0xf, 0xe, 0xf, 0x170, 0xb, 0xf, 0x3, 0xf, 
    0x3, 0xf, 0x5, 0xf, 0x174, 0xa, 0xf, 0x3, 0xf, 0x5, 0xf, 0x177, 0xa, 
    0xf, 0x3, 0x10, 0x3, 0x10, 0x7, 0x10, 0x17b, 0xa, 0x10, 0xc, 0x10, 0xe, 
    0x10, 0x17e, 0xb, 0x10, 0x3, 0x11, 0x3, 0x11, 0x3, 0x11, 0x5, 0x11, 
    0x183, 0xa, 0x11, 0x3, 0x11, 0x3, 0x11, 0x5, 0x11, 0x187, 0xa, 0x11, 
    0x3, 0x11, 0x3, 0x11, 0x3, 0x12, 0x3, 0x12, 0x7, 0x12, 0x18d, 0xa, 0x12, 
    0xc, 0x12, 0xe, 0x12, 0x190, 0xb, 0x12, 0x3, 0x12, 0x3, 0x12, 0x3, 0x13, 
    0x3, 0x13, 0x7, 0x13, 0x196, 0xa, 0x13, 0xc, 0x13, 0xe, 0x13, 0x199, 
    0xb, 0x13, 0x3, 0x13, 0x3, 0x13, 0x3, 0x14, 0x3, 0x14, 0x5, 0x14, 0x19f, 
    0xa, 0x14, 0x3, 0x14, 0x3, 0x14, 0x7, 0x14, 0x1a3, 0xa, 0x14, 0xc, 0x14, 
    0xe, 0x14, 0x1a6, 0xb, 0x14, 0x3, 0x14, 0x5, 0x14, 0x1a9, 0xa, 0x14, 
    0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 0x3, 0x15, 0x3, 
    0x15, 0x3, 0x15, 0x3, 0x15, 0x5, 0x15, 0x1b4, 0xa, 0x15, 0x3, 0x16, 
    0x3, 0x16, 0x3, 0x16, 0x3, 0x16, 0x3, 0x16, 0x7, 0x16, 0x1bb, 0xa, 0x16, 
    0xc, 0x16, 0xe, 0x16, 0x1be, 0xb, 0x16, 0x3, 0x16, 0x3, 0x16, 0x5, 0x16, 
    0x1c2, 0xa, 0x16, 0x3, 0x16, 0x3, 0x16, 0x3, 0x17, 0x3, 0x17, 0x5, 0x17, 
    0x1c8, 0xa, 0x17, 0x3, 0x18, 0x3, 0x18, 0x5, 0x18, 0x1cc, 0xa, 0x18, 
    0x3, 0x19, 0x3, 0x19, 0x3, 0x19, 0x3, 0x1a, 0x3, 0x1a, 0x3, 0x1a, 0x3, 
    0x1b, 0x3, 0x1b, 0x3, 0x1b, 0x3, 0x1b, 0x5, 0x1b, 0x1d8, 0xa, 0x1b, 
    0x3, 0x1b, 0x3, 0x1b, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 
    0x1d, 0x7, 0x1d, 0x1e1, 0xa, 0x1d, 0xc, 0x1d, 0xe, 0x1d, 0x1e4, 0xb, 
    0x1d, 0x3, 0x1d, 0x3, 0x1d, 0x5, 0x1d, 0x1e8, 0xa, 0x1d, 0x3, 0x1e, 
    0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x5, 
    0x1e, 0x1f1, 0xa, 0x1e, 0x3, 0x1f, 0x3, 0x1f, 0x3, 0x1f, 0x3, 0x1f, 
    0x7, 0x1f, 0x1f7, 0xa, 0x1f, 0xc, 0x1f, 0xe, 0x1f, 0x1fa, 0xb, 0x1f, 
    0x3, 0x1f, 0x3, 0x1f, 0x3, 0x20, 0x3, 0x20, 0x3, 0x20, 0x7, 0x20, 0x201, 
    0xa, 0x20, 0xc, 0x20, 0xe, 0x20, 0x204, 0xb, 0x20, 0x3, 0x20, 0x3, 0x20, 
    0x3, 0x20, 0x3, 0x21, 0x7, 0x21, 0x20a, 0xa, 0x21, 0xc, 0x21, 0xe, 0x21, 
    0x20d, 0xb, 0x21, 0x3, 0x21, 0x3, 0x21, 0x3, 0x21, 0x7, 0x21, 0x212, 
    0xa, 0x21, 0xc, 0x21, 0xe, 0x21, 0x215, 0xb, 0x21, 0x3, 0x21, 0x3, 0x21, 
    0x5, 0x21, 0x219, 0xa, 0x21, 0x3, 0x21, 0x3, 0x21, 0x3, 0x21, 0x3, 0x21, 
    0x7, 0x21, 0x21f, 0xa, 0x21, 0xc, 0x21, 0xe, 0x21, 0x222, 0xb, 0x21, 
    0x3, 0x21, 0x3, 0x21, 0x5, 0x21, 0x226, 0xa, 0x21, 0x3, 0x21, 0x3, 0x21, 
    0x3, 0x22, 0x3, 0x22, 0x3, 0x22, 0x3, 0x22, 0x3, 0x22, 0x3, 0x22, 0x5, 
    0x22, 0x230, 0xa, 0x22, 0x3, 0x23, 0x3, 0x23, 0x3, 0x23, 0x3, 0x24, 
    0x3, 0x24, 0x3, 0x24, 0x7, 0x24, 0x238, 0xa, 0x24, 0xc, 0x24, 0xe, 0x24, 
    0x23b, 0xb, 0x24, 0x3, 0x25, 0x3, 0x25, 0x3, 0x25, 0x5, 0x25, 0x240, 
    0xa, 0x25, 0x3, 0x26, 0x3, 0x26, 0x3, 0x26, 0x7, 0x26, 0x245, 0xa, 0x26, 
    0xc, 0x26, 0xe, 0x26, 0x248, 0xb, 0x26, 0x3, 0x27, 0x3, 0x27, 0x5, 0x27, 
    0x24c, 0xa, 0x27, 0x3, 0x28, 0x3, 0x28, 0x3, 0x28, 0x3, 0x28, 0x7, 0x28, 
    0x252, 0xa, 0x28, 0xc, 0x28, 0xe, 0x28, 0x255, 0xb, 0x28, 0x3, 0x28, 
    0x5, 0x28, 0x258, 0xa, 0x28, 0x5, 0x28, 0x25a, 0xa, 0x28, 0x3, 0x28, 
    0x3, 0x28, 0x3, 0x29, 0x3, 0x29, 0x5, 0x29, 0x260, 0xa, 0x29, 0x3, 0x29, 
    0x3, 0x29, 0x3, 0x29, 0x5, 0x29, 0x265, 0xa, 0x29, 0x7, 0x29, 0x267, 
    0xa, 0x29, 0xc, 0x29, 0xe, 0x29, 0x26a, 0xb, 0x29, 0x3, 0x2a, 0x3, 0x2a, 
    0x7, 0x2a, 0x26e, 0xa, 0x2a, 0xc, 0x2a, 0xe, 0x2a, 0x271, 0xb, 0x2a, 
    0x3, 0x2a, 0x3, 0x2a, 0x3, 0x2a, 0x5, 0x2a, 0x276, 0xa, 0x2a, 0x5, 0x2a, 
    0x278, 0xa, 0x2a, 0x3, 0x2b, 0x3, 0x2b, 0x3, 0x2b, 0x7, 0x2b, 0x27d, 
    0xa, 0x2b, 0xc, 0x2b, 0xe, 0x2b, 0x280, 0xb, 0x2b, 0x3, 0x2c, 0x3, 0x2c, 
    0x5, 0x2c, 0x284, 0xa, 0x2c, 0x3, 0x2c, 0x3, 0x2c, 0x3, 0x2d, 0x3, 0x2d, 
    0x3, 0x2d, 0x7, 0x2d, 0x28b, 0xa, 0x2d, 0xc, 0x2d, 0xe, 0x2d, 0x28e, 
    0xb, 0x2d, 0x3, 0x2d, 0x3, 0x2d, 0x5, 0x2d, 0x292, 0xa, 0x2d, 0x3, 0x2d, 
    0x5, 0x2d, 0x295, 0xa, 0x2d, 0x3, 0x2e, 0x7, 0x2e, 0x298, 0xa, 0x2e, 
    0xc, 0x2e, 0xe, 0x2e, 0x29b, 0xb, 0x2e, 0x3, 0x2e, 0x3, 0x2e, 0x3, 0x2e, 
    0x3, 0x2f, 0x7, 0x2f, 0x2a1, 0xa, 0x2f, 0xc, 0x2f, 0xe, 0x2f, 0x2a4, 
    0xb, 0x2f, 0x3, 0x2f, 0x3, 0x2f, 0x7, 0x2f, 0x2a8, 0xa, 0x2f, 0xc, 0x2f, 
    0xe, 0x2f, 0x2ab, 0xb, 0x2f, 0x3, 0x2f, 0x3, 0x2f, 0x3, 0x2f, 0x3, 0x30, 
    0x3, 0x30, 0x3, 0x30, 0x7, 0x30, 0x2b3, 0xa, 0x30, 0xc, 0x30, 0xe, 0x30, 
    0x2b6, 0xb, 0x30, 0x3, 0x31, 0x3, 0x31, 0x3, 0x31, 0x3, 0x31, 0x3, 0x31, 
    0x3, 0x31, 0x5, 0x31, 0x2be, 0xa, 0x31, 0x3, 0x32, 0x3, 0x32, 0x3, 0x33, 
    0x3, 0x33, 0x3, 0x34, 0x3, 0x34, 0x7, 0x34, 0x2c6, 0xa, 0x34, 0xc, 0x34, 
    0xe, 0x34, 0x2c9, 0xb, 0x34, 0x3, 0x34, 0x3, 0x34, 0x3, 0x34, 0x3, 0x35, 
    0x3, 0x35, 0x3, 0x35, 0x5, 0x35, 0x2d1, 0xa, 0x35, 0x3, 0x35, 0x3, 0x35, 
    0x3, 0x35, 0x5, 0x35, 0x2d6, 0xa, 0x35, 0x3, 0x35, 0x5, 0x35, 0x2d9, 
    0xa, 0x35, 0x3, 0x36, 0x3, 0x36, 0x3, 0x36, 0x7, 0x36, 0x2de, 0xa, 0x36, 
    0xc, 0x36, 0xe, 0x36, 0x2e1, 0xb, 0x36, 0x3, 0x37, 0x3, 0x37, 0x3, 0x37, 
    0x3, 0x37, 0x3, 0x38, 0x3, 0x38, 0x3, 0x38, 0x5, 0x38, 0x2ea, 0xa, 0x38, 
    0x3, 0x39, 0x3, 0x39, 0x3, 0x39, 0x3, 0x39, 0x7, 0x39, 0x2f0, 0xa, 0x39, 
    0xc, 0x39, 0xe, 0x39, 0x2f3, 0xb, 0x39, 0x5, 0x39, 0x2f5, 0xa, 0x39, 
    0x3, 0x39, 0x5, 0x39, 0x2f8, 0xa, 0x39, 0x3, 0x39, 0x3, 0x39, 0x3, 0x3a, 
    0x3, 0x3a, 0x3, 0x3a, 0x3, 0x3a, 0x3, 0x3a, 0x3, 0x3b, 0x3, 0x3b, 0x7, 
    0x3b, 0x303, 0xa, 0x3b, 0xc, 0x3b, 0xe, 0x3b, 0x306, 0xb, 0x3b, 0x3, 
    0x3b, 0x3, 0x3b, 0x3, 0x3c, 0x7, 0x3c, 0x30b, 0xa, 0x3c, 0xc, 0x3c, 
    0xe, 0x3c, 0x30e, 0xb, 0x3c, 0x3, 0x3c, 0x3, 0x3c, 0x5, 0x3c, 0x312, 
    0xa, 0x3c, 0x3, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x3, 
    0x3d, 0x5, 0x3d, 0x31a, 0xa, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x5, 0x3d, 
    0x31e, 0xa, 0x3d, 0x3, 0x3d, 0x3, 0x3d, 0x5, 0x3d, 0x322, 0xa, 0x3d, 
    0x3, 0x3d, 0x3, 0x3d, 0x5, 0x3d, 0x326, 0xa, 0x3d, 0x5, 0x3d, 0x328, 
    0xa, 0x3d, 0x3, 0x3e, 0x3, 0x3e, 0x5, 0x3e, 0x32c, 0xa, 0x3e, 0x3, 0x3f, 
    0x3, 0x3f, 0x3, 0x3f, 0x3, 0x3f, 0x5, 0x3f, 0x332, 0xa, 0x3f, 0x3, 0x40, 
    0x3, 0x40, 0x3, 0x41, 0x3, 0x41, 0x3, 0x41, 0x3, 0x42, 0x3, 0x42, 0x7, 
    0x42, 0x33b, 0xa, 0x42, 0xc, 0x42, 0xe, 0x42, 0x33e, 0xb, 0x42, 0x3, 
    0x42, 0x3, 0x42, 0x3, 0x43, 0x3, 0x43, 0x3, 0x43, 0x3, 0x43, 0x3, 0x43, 
    0x5, 0x43, 0x347, 0xa, 0x43, 0x3, 0x44, 0x7, 0x44, 0x34a, 0xa, 0x44, 
    0xc, 0x44, 0xe, 0x44, 0x34d, 0xb, 0x44, 0x3, 0x44, 0x3, 0x44, 0x3, 0x44, 
    0x3, 0x45, 0x7, 0x45, 0x353, 0xa, 0x45, 0xc, 0x45, 0xe, 0x45, 0x356, 
    0xb, 0x45, 0x3, 0x45, 0x3, 0x45, 0x5, 0x45, 0x35a, 0xa, 0x45, 0x3, 0x45, 
    0x5, 0x45, 0x35d, 0xa, 0x45, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 
    0x3, 0x46, 0x5, 0x46, 0x364, 0xa, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 
    0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x5, 0x46, 0x36d, 0xa, 0x46, 
    0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
    0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 
    0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x6, 
    0x46, 0x382, 0xa, 0x46, 0xd, 0x46, 0xe, 0x46, 0x383, 0x3, 0x46, 0x5, 
    0x46, 0x387, 0xa, 0x46, 0x3, 0x46, 0x5, 0x46, 0x38a, 0xa, 0x46, 0x3, 
    0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x7, 0x46, 0x390, 0xa, 0x46, 
    0xc, 0x46, 0xe, 0x46, 0x393, 0xb, 0x46, 0x3, 0x46, 0x5, 0x46, 0x396, 
    0xa, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x7, 0x46, 0x39c, 
    0xa, 0x46, 0xc, 0x46, 0xe, 0x46, 0x39f, 0xb, 0x46, 0x3, 0x46, 0x7, 0x46, 
    0x3a2, 0xa, 0x46, 0xc, 0x46, 0xe, 0x46, 0x3a5, 0xb, 0x46, 0x3, 0x46, 
    0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
    0x46, 0x5, 0x46, 0x3af, 0xa, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 
    0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x5, 0x46, 0x3b8, 0xa, 0x46, 
    0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x5, 0x46, 0x3bd, 0xa, 0x46, 0x3, 0x46, 
    0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 0x46, 0x3, 
    0x46, 0x5, 0x46, 0x3c7, 0xa, 0x46, 0x3, 0x47, 0x3, 0x47, 0x3, 0x47, 
    0x7, 0x47, 0x3cc, 0xa, 0x47, 0xc, 0x47, 0xe, 0x47, 0x3cf, 0xb, 0x47, 
    0x3, 0x47, 0x3, 0x47, 0x3, 0x47, 0x3, 0x47, 0x3, 0x47, 0x3, 0x48, 0x3, 
    0x48, 0x3, 0x48, 0x7, 0x48, 0x3d9, 0xa, 0x48, 0xc, 0x48, 0xe, 0x48, 
    0x3dc, 0xb, 0x48, 0x3, 0x49, 0x3, 0x49, 0x3, 0x49, 0x3, 0x4a, 0x3, 0x4a, 
    0x3, 0x4a, 0x5, 0x4a, 0x3e4, 0xa, 0x4a, 0x3, 0x4a, 0x3, 0x4a, 0x3, 0x4b, 
    0x3, 0x4b, 0x3, 0x4b, 0x7, 0x4b, 0x3eb, 0xa, 0x4b, 0xc, 0x4b, 0xe, 0x4b, 
    0x3ee, 0xb, 0x4b, 0x3, 0x4c, 0x7, 0x4c, 0x3f1, 0xa, 0x4c, 0xc, 0x4c, 
    0xe, 0x4c, 0x3f4, 0xb, 0x4c, 0x3, 0x4c, 0x3, 0x4c, 0x3, 0x4c, 0x3, 0x4c, 
    0x3, 0x4c, 0x3, 0x4d, 0x6, 0x4d, 0x3fc, 0xa, 0x4d, 0xd, 0x4d, 0xe, 0x4d, 
    0x3fd, 0x3, 0x4d, 0x6, 0x4d, 0x401, 0xa, 0x4d, 0xd, 0x4d, 0xe, 0x4d, 
    0x402, 0x3, 0x4e, 0x3, 0x4e, 0x3, 0x4e, 0x5, 0x4e, 0x408, 0xa, 0x4e, 
    0x3, 0x4e, 0x3, 0x4e, 0x3, 0x4e, 0x5, 0x4e, 0x40d, 0xa, 0x4e, 0x3, 0x4f, 
    0x3, 0x4f, 0x5, 0x4f, 0x411, 0xa, 0x4f, 0x3, 0x4f, 0x3, 0x4f, 0x5, 0x4f, 
    0x415, 0xa, 0x4f, 0x3, 0x4f, 0x3, 0x4f, 0x5, 0x4f, 0x419, 0xa, 0x4f, 
    0x5, 0x4f, 0x41b, 0xa, 0x4f, 0x3, 0x50, 0x3, 0x50, 0x5, 0x50, 0x41f, 
    0xa, 0x50, 0x3, 0x51, 0x7, 0x51, 0x422, 0xa, 0x51, 0xc, 0x51, 0xe, 0x51, 
    0x425, 0xb, 0x51, 0x3, 0x51, 0x3, 0x51, 0x3, 0x51, 0x3, 0x51, 0x3, 0x51, 
    0x3, 0x52, 0x3, 0x52, 0x3, 0x52, 0x3, 0x52, 0x3, 0x53, 0x3, 0x53, 0x3, 
    0x53, 0x7, 0x53, 0x433, 0xa, 0x53, 0xc, 0x53, 0xe, 0x53, 0x436, 0xb, 
    0x53, 0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x5, 0x54, 0x43b, 0xa, 0x54, 
    0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x5, 0x54, 0x441, 0xa, 0x54, 
    0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x3, 0x54, 0x5, 0x54, 0x447, 0xa, 0x54, 
    0x3, 0x54, 0x5, 0x54, 0x44a, 0xa, 0x54, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
    0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x7, 0x55, 0x453, 0xa, 0x55, 
    0xc, 0x55, 0xe, 0x55, 0x456, 0xb, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
    0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
    0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x464, 0xa, 0x55, 0x3, 0x55, 
    0x3, 0x55, 0x5, 0x55, 0x468, 0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
    0x5, 0x55, 0x46d, 0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x471, 
    0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
    0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
    0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x481, 0xa, 0x55, 0x3, 0x55, 0x3, 0x55, 
    0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
    0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
    0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
    0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
    0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
    0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x4a9, 0xa, 0x55, 
    0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x5, 0x55, 0x4af, 0xa, 0x55, 
    0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 
    0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 0x3, 0x55, 
    0x5, 0x55, 0x4be, 0xa, 0x55, 0x3, 0x55, 0x7, 0x55, 0x4c1, 0xa, 0x55, 
    0xc, 0x55, 0xe, 0x55, 0x4c4, 0xb, 0x55, 0x3, 0x56, 0x3, 0x56, 0x3, 0x56, 
    0x3, 0x56, 0x3, 0x57, 0x3, 0x57, 0x3, 0x57, 0x5, 0x57, 0x4cd, 0xa, 0x57, 
    0x3, 0x57, 0x3, 0x57, 0x3, 0x57, 0x3, 0x57, 0x3, 0x57, 0x7, 0x57, 0x4d4, 
    0xa, 0x57, 0xc, 0x57, 0xe, 0x57, 0x4d7, 0xb, 0x57, 0x3, 0x57, 0x5, 0x57, 
    0x4da, 0xa, 0x57, 0x3, 0x58, 0x3, 0x58, 0x5, 0x58, 0x4de, 0xa, 0x58, 
    0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 
    0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 
    0x3, 0x59, 0x3, 0x59, 0x3, 0x59, 0x5, 0x59, 0x4f0, 0xa, 0x59, 0x5, 0x59, 
    0x4f2, 0xa, 0x59, 0x3, 0x5a, 0x3, 0x5a, 0x3, 0x5a, 0x5, 0x5a, 0x4f7, 
    0xa, 0x5a, 0x3, 0x5a, 0x7, 0x5a, 0x4fa, 0xa, 0x5a, 0xc, 0x5a, 0xe, 0x5a, 
    0x4fd, 0xb, 0x5a, 0x3, 0x5a, 0x3, 0x5a, 0x5, 0x5a, 0x501, 0xa, 0x5a, 
    0x3, 0x5b, 0x3, 0x5b, 0x3, 0x5b, 0x3, 0x5b, 0x3, 0x5b, 0x3, 0x5b, 0x3, 
    0x5b, 0x5, 0x5b, 0x50a, 0xa, 0x5b, 0x5, 0x5b, 0x50c, 0xa, 0x5b, 0x3, 
    0x5c, 0x3, 0x5c, 0x5, 0x5c, 0x510, 0xa, 0x5c, 0x3, 0x5c, 0x3, 0x5c, 
    0x3, 0x5c, 0x5, 0x5c, 0x515, 0xa, 0x5c, 0x7, 0x5c, 0x517, 0xa, 0x5c, 
    0xc, 0x5c, 0xe, 0x5c, 0x51a, 0xb, 0x5c, 0x3, 0x5c, 0x5, 0x5c, 0x51d, 
    0xa, 0x5c, 0x3, 0x5d, 0x3, 0x5d, 0x5, 0x5d, 0x521, 0xa, 0x5d, 0x3, 0x5d, 
    0x3, 0x5d, 0x3, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x7, 0x5e, 0x529, 
    0xa, 0x5e, 0xc, 0x5e, 0xe, 0x5e, 0x52c, 0xb, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 
    0x3, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 0x7, 0x5e, 0x535, 
    0xa, 0x5e, 0xc, 0x5e, 0xe, 0x5e, 0x538, 0xb, 0x5e, 0x3, 0x5e, 0x3, 0x5e, 
    0x7, 0x5e, 0x53c, 0xa, 0x5e, 0xc, 0x5e, 0xe, 0x5e, 0x53f, 0xb, 0x5e, 
    0x5, 0x5e, 0x541, 0xa, 0x5e, 0x3, 0x5f, 0x3, 0x5f, 0x5, 0x5f, 0x545, 
    0xa, 0x5f, 0x3, 0x60, 0x3, 0x60, 0x3, 0x60, 0x3, 0x61, 0x3, 0x61, 0x3, 
    0x61, 0x5, 0x61, 0x54d, 0xa, 0x61, 0x3, 0x62, 0x3, 0x62, 0x3, 0x62, 
    0x5, 0x62, 0x552, 0xa, 0x62, 0x3, 0x63, 0x3, 0x63, 0x3, 0x63, 0x3, 0x63, 
    0x3, 0x64, 0x3, 0x64, 0x3, 0x64, 0x7, 0x64, 0x55b, 0xa, 0x64, 0xc, 0x64, 
    0xe, 0x64, 0x55e, 0xb, 0x64, 0x3, 0x65, 0x7, 0x65, 0x561, 0xa, 0x65, 
    0xc, 0x65, 0xe, 0x65, 0x564, 0xb, 0x65, 0x3, 0x65, 0x3, 0x65, 0x5, 0x65, 
    0x568, 0xa, 0x65, 0x3, 0x65, 0x7, 0x65, 0x56b, 0xa, 0x65, 0xc, 0x65, 
    0xe, 0x65, 0x56e, 0xb, 0x65, 0x3, 0x65, 0x3, 0x65, 0x7, 0x65, 0x572, 
    0xa, 0x65, 0xc, 0x65, 0xe, 0x65, 0x575, 0xb, 0x65, 0x3, 0x66, 0x3, 0x66, 
    0x3, 0x67, 0x3, 0x67, 0x3, 0x67, 0x3, 0x67, 0x7, 0x67, 0x57d, 0xa, 0x67, 
    0xc, 0x67, 0xe, 0x67, 0x580, 0xb, 0x67, 0x3, 0x67, 0x3, 0x67, 0x3, 0x68, 
    0x3, 0x68, 0x3, 0x68, 0x3, 0x68, 0x5, 0x68, 0x588, 0xa, 0x68, 0x5, 0x68, 
    0x58a, 0xa, 0x68, 0x3, 0x69, 0x3, 0x69, 0x3, 0x69, 0x3, 0x69, 0x5, 0x69, 
    0x590, 0xa, 0x69, 0x3, 0x6a, 0x3, 0x6a, 0x5, 0x6a, 0x594, 0xa, 0x6a, 
    0x3, 0x6a, 0x3, 0x6a, 0x3, 0x6a, 0x2, 0x3, 0xa8, 0x6b, 0x2, 0x4, 0x6, 
    0x8, 0xa, 0xc, 0xe, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e, 
    0x20, 0x22, 0x24, 0x26, 0x28, 0x2a, 0x2c, 0x2e, 0x30, 0x32, 0x34, 0x36, 
    0x38, 0x3a, 0x3c, 0x3e, 0x40, 0x42, 0x44, 0x46, 0x48, 0x4a, 0x4c, 0x4e, 
    0x50, 0x52, 0x54, 0x56, 0x58, 0x5a, 0x5c, 0x5e, 0x60, 0x62, 0x64, 0x66, 
    0x68, 0x6a, 0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76, 0x78, 0x7a, 0x7c, 0x7e, 
    0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e, 0x90, 0x92, 0x94, 0x96, 
    0x98, 0x9a, 0x9c, 0x9e, 0xa0, 0xa2, 0xa4, 0xa6, 0xa8, 0xaa, 0xac, 0xae, 
    0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe, 0xc0, 0xc2, 0xc4, 0xc6, 
    0xc8, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0x2, 0xe, 0x4, 0x2, 0x13, 0x13, 
    0x2a, 0x2a, 0x3, 0x2, 0x35, 0x38, 0x3, 0x2, 0x39, 0x3a, 0x3, 0x2, 0x55, 
    0x58, 0x3, 0x2, 0x4b, 0x4c, 0x4, 0x2, 0x59, 0x5a, 0x5e, 0x5e, 0x3, 0x2, 
    0x57, 0x58, 0x4, 0x2, 0x49, 0x4a, 0x50, 0x51, 0x4, 0x2, 0x4f, 0x4f, 
    0x52, 0x52, 0x4, 0x2, 0x48, 0x48, 0x5f, 0x69, 0x3, 0x2, 0x55, 0x56, 
    0xa, 0x2, 0x5, 0x5, 0x7, 0x7, 0xa, 0xa, 0x10, 0x10, 0x16, 0x16, 0x1d, 
    0x1d, 0x1f, 0x1f, 0x27, 0x27, 0x2, 0x637, 0x2, 0xd5, 0x3, 0x2, 0x2, 
    0x2, 0x4, 0xe8, 0x3, 0x2, 0x2, 0x2, 0x6, 0xef, 0x3, 0x2, 0x2, 0x2, 0x8, 
    0x107, 0x3, 0x2, 0x2, 0x2, 0xa, 0x10e, 0x3, 0x2, 0x2, 0x2, 0xc, 0x118, 
    0x3, 0x2, 0x2, 0x2, 0xe, 0x11c, 0x3, 0x2, 0x2, 0x2, 0x10, 0x11e, 0x3, 
    0x2, 0x2, 0x2, 0x12, 0x12d, 0x3, 0x2, 0x2, 0x2, 0x14, 0x13b, 0x3, 0x2, 
    0x2, 0x2, 0x16, 0x149, 0x3, 0x2, 0x2, 0x2, 0x18, 0x151, 0x3, 0x2, 0x2, 
    0x2, 0x1a, 0x163, 0x3, 0x2, 0x2, 0x2, 0x1c, 0x16e, 0x3, 0x2, 0x2, 0x2, 
    0x1e, 0x178, 0x3, 0x2, 0x2, 0x2, 0x20, 0x17f, 0x3, 0x2, 0x2, 0x2, 0x22, 
    0x18a, 0x3, 0x2, 0x2, 0x2, 0x24, 0x193, 0x3, 0x2, 0x2, 0x2, 0x26, 0x1a8, 
    0x3, 0x2, 0x2, 0x2, 0x28, 0x1b3, 0x3, 0x2, 0x2, 0x2, 0x2a, 0x1b5, 0x3, 
    0x2, 0x2, 0x2, 0x2c, 0x1c7, 0x3, 0x2, 0x2, 0x2, 0x2e, 0x1cb, 0x3, 0x2, 
    0x2, 0x2, 0x30, 0x1cd, 0x3, 0x2, 0x2, 0x2, 0x32, 0x1d0, 0x3, 0x2, 0x2, 
    0x2, 0x34, 0x1d3, 0x3, 0x2, 0x2, 0x2, 0x36, 0x1db, 0x3, 0x2, 0x2, 0x2, 
    0x38, 0x1e7, 0x3, 0x2, 0x2, 0x2, 0x3a, 0x1f0, 0x3, 0x2, 0x2, 0x2, 0x3c, 
    0x1f2, 0x3, 0x2, 0x2, 0x2, 0x3e, 0x1fd, 0x3, 0x2, 0x2, 0x2, 0x40, 0x20b, 
    0x3, 0x2, 0x2, 0x2, 0x42, 0x22f, 0x3, 0x2, 0x2, 0x2, 0x44, 0x231, 0x3, 
    0x2, 0x2, 0x2, 0x46, 0x234, 0x3, 0x2, 0x2, 0x2, 0x48, 0x23c, 0x3, 0x2, 
    0x2, 0x2, 0x4a, 0x241, 0x3, 0x2, 0x2, 0x2, 0x4c, 0x24b, 0x3, 0x2, 0x2, 
    0x2, 0x4e, 0x24d, 0x3, 0x2, 0x2, 0x2, 0x50, 0x25d, 0x3, 0x2, 0x2, 0x2, 
    0x52, 0x277, 0x3, 0x2, 0x2, 0x2, 0x54, 0x279, 0x3, 0x2, 0x2, 0x2, 0x56, 
    0x281, 0x3, 0x2, 0x2, 0x2, 0x58, 0x294, 0x3, 0x2, 0x2, 0x2, 0x5a, 0x299, 
    0x3, 0x2, 0x2, 0x2, 0x5c, 0x2a2, 0x3, 0x2, 0x2, 0x2, 0x5e, 0x2af, 0x3, 
    0x2, 0x2, 0x2, 0x60, 0x2bd, 0x3, 0x2, 0x2, 0x2, 0x62, 0x2bf, 0x3, 0x2, 
    0x2, 0x2, 0x64, 0x2c1, 0x3, 0x2, 0x2, 0x2, 0x66, 0x2c7, 0x3, 0x2, 0x2, 
    0x2, 0x68, 0x2d0, 0x3, 0x2, 0x2, 0x2, 0x6a, 0x2da, 0x3, 0x2, 0x2, 0x2, 
    0x6c, 0x2e2, 0x3, 0x2, 0x2, 0x2, 0x6e, 0x2e9, 0x3, 0x2, 0x2, 0x2, 0x70, 
    0x2eb, 0x3, 0x2, 0x2, 0x2, 0x72, 0x2fb, 0x3, 0x2, 0x2, 0x2, 0x74, 0x300, 
    0x3, 0x2, 0x2, 0x2, 0x76, 0x311, 0x3, 0x2, 0x2, 0x2, 0x78, 0x327, 0x3, 
    0x2, 0x2, 0x2, 0x7a, 0x32b, 0x3, 0x2, 0x2, 0x2, 0x7c, 0x32d, 0x3, 0x2, 
    0x2, 0x2, 0x7e, 0x333, 0x3, 0x2, 0x2, 0x2, 0x80, 0x335, 0x3, 0x2, 0x2, 
    0x2, 0x82, 0x338, 0x3, 0x2, 0x2, 0x2, 0x84, 0x346, 0x3, 0x2, 0x2, 0x2, 
    0x86, 0x34b, 0x3, 0x2, 0x2, 0x2, 0x88, 0x35c, 0x3, 0x2, 0x2, 0x2, 0x8a, 
    0x3c6, 0x3, 0x2, 0x2, 0x2, 0x8c, 0x3c8, 0x3, 0x2, 0x2, 0x2, 0x8e, 0x3d5, 
    0x3, 0x2, 0x2, 0x2, 0x90, 0x3dd, 0x3, 0x2, 0x2, 0x2, 0x92, 0x3e0, 0x3, 
    0x2, 0x2, 0x2, 0x94, 0x3e7, 0x3, 0x2, 0x2, 0x2, 0x96, 0x3f2, 0x3, 0x2, 
    0x2, 0x2, 0x98, 0x3fb, 0x3, 0x2, 0x2, 0x2, 0x9a, 0x40c, 0x3, 0x2, 0x2, 
    0x2, 0x9c, 0x41a, 0x3, 0x2, 0x2, 0x2, 0x9e, 0x41e, 0x3, 0x2, 0x2, 0x2, 
    0xa0, 0x423, 0x3, 0x2, 0x2, 0x2, 0xa2, 0x42b, 0x3, 0x2, 0x2, 0x2, 0xa4, 
    0x42f, 0x3, 0x2, 0x2, 0x2, 0xa6, 0x449, 0x3, 0x2, 0x2, 0x2, 0xa8, 0x470, 
    0x3, 0x2, 0x2, 0x2, 0xaa, 0x4c5, 0x3, 0x2, 0x2, 0x2, 0xac, 0x4d9, 0x3, 
    0x2, 0x2, 0x2, 0xae, 0x4dd, 0x3, 0x2, 0x2, 0x2, 0xb0, 0x4f1, 0x3, 0x2, 
    0x2, 0x2, 0xb2, 0x4f6, 0x3, 0x2, 0x2, 0x2, 0xb4, 0x50b, 0x3, 0x2, 0x2, 
    0x2, 0xb6, 0x51c, 0x3, 0x2, 0x2, 0x2, 0xb8, 0x51e, 0x3, 0x2, 0x2, 0x2, 
    0xba, 0x524, 0x3, 0x2, 0x2, 0x2, 0xbc, 0x542, 0x3, 0x2, 0x2, 0x2, 0xbe, 
    0x546, 0x3, 0x2, 0x2, 0x2, 0xc0, 0x54c, 0x3, 0x2, 0x2, 0x2, 0xc2, 0x551, 
    0x3, 0x2, 0x2, 0x2, 0xc4, 0x553, 0x3, 0x2, 0x2, 0x2, 0xc6, 0x557, 0x3, 
    0x2, 0x2, 0x2, 0xc8, 0x562, 0x3, 0x2, 0x2, 0x2, 0xca, 0x576, 0x3, 0x2, 
    0x2, 0x2, 0xcc, 0x578, 0x3, 0x2, 0x2, 0x2, 0xce, 0x589, 0x3, 0x2, 0x2, 
    0x2, 0xd0, 0x58f, 0x3, 0x2, 0x2, 0x2, 0xd2, 0x591, 0x3, 0x2, 0x2, 0x2, 
    0xd4, 0xd6, 0x5, 0x4, 0x3, 0x2, 0xd5, 0xd4, 0x3, 0x2, 0x2, 0x2, 0xd5, 
    0xd6, 0x3, 0x2, 0x2, 0x2, 0xd6, 0xda, 0x3, 0x2, 0x2, 0x2, 0xd7, 0xd9, 
    0x5, 0x6, 0x4, 0x2, 0xd8, 0xd7, 0x3, 0x2, 0x2, 0x2, 0xd9, 0xdc, 0x3, 
    0x2, 0x2, 0x2, 0xda, 0xd8, 0x3, 0x2, 0x2, 0x2, 0xda, 0xdb, 0x3, 0x2, 
    0x2, 0x2, 0xdb, 0xe0, 0x3, 0x2, 0x2, 0x2, 0xdc, 0xda, 0x3, 0x2, 0x2, 
    0x2, 0xdd, 0xdf, 0x5, 0x8, 0x5, 0x2, 0xde, 0xdd, 0x3, 0x2, 0x2, 0x2, 
    0xdf, 0xe2, 0x3, 0x2, 0x2, 0x2, 0xe0, 0xde, 0x3, 0x2, 0x2, 0x2, 0xe0, 
    0xe1, 0x3, 0x2, 0x2, 0x2, 0xe1, 0xe3, 0x3, 0x2, 0x2, 0x2, 0xe2, 0xe0, 
    0x3, 0x2, 0x2, 0x2, 0xe3, 0xe4, 0x7, 0x2, 0x2, 0x3, 0xe4, 0x3, 0x3, 
    0x2, 0x2, 0x2, 0xe5, 0xe7, 0x5, 0x68, 0x35, 0x2, 0xe6, 0xe5, 0x3, 0x2, 
    0x2, 0x2, 0xe7, 0xea, 0x3, 0x2, 0x2, 0x2, 0xe8, 0xe6, 0x3, 0x2, 0x2, 
    0x2, 0xe8, 0xe9, 0x3, 0x2, 0x2, 0x2, 0xe9, 0xeb, 0x3, 0x2, 0x2, 0x2, 
    0xea, 0xe8, 0x3, 0x2, 0x2, 0x2, 0xeb, 0xec, 0x7, 0x22, 0x2, 0x2, 0xec, 
    0xed, 0x5, 0x5e, 0x30, 0x2, 0xed, 0xee, 0x7, 0x45, 0x2, 0x2, 0xee, 0x5, 
    0x3, 0x2, 0x2, 0x2, 0xef, 0xf1, 0x7, 0x1b, 0x2, 0x2, 0xf0, 0xf2, 0x7, 
    0x28, 0x2, 0x2, 0xf1, 0xf0, 0x3, 0x2, 0x2, 0x2, 0xf1, 0xf2, 0x3, 0x2, 
    0x2, 0x2, 0xf2, 0xf3, 0x3, 0x2, 0x2, 0x2, 0xf3, 0xf6, 0x5, 0x5e, 0x30, 
    0x2, 0xf4, 0xf5, 0x7, 0x47, 0x2, 0x2, 0xf5, 0xf7, 0x7, 0x59, 0x2, 0x2, 
    0xf6, 0xf4, 0x3, 0x2, 0x2, 0x2, 0xf6, 0xf7, 0x3, 0x2, 0x2, 0x2, 0xf7, 
    0xf8, 0x3, 0x2, 0x2, 0x2, 0xf8, 0xf9, 0x7, 0x45, 0x2, 0x2, 0xf9, 0x7, 
    0x3, 0x2, 0x2, 0x2, 0xfa, 0xfc, 0x5, 0xc, 0x7, 0x2, 0xfb, 0xfa, 0x3, 
    0x2, 0x2, 0x2, 0xfc, 0xff, 0x3, 0x2, 0x2, 0x2, 0xfd, 0xfb, 0x3, 0x2, 
    0x2, 0x2, 0xfd, 0xfe, 0x3, 0x2, 0x2, 0x2, 0xfe, 0x104, 0x3, 0x2, 0x2, 
    0x2, 0xff, 0xfd, 0x3, 0x2, 0x2, 0x2, 0x100, 0x105, 0x5, 0x10, 0x9, 0x2, 
    0x101, 0x105, 0x5, 0x18, 0xd, 0x2, 0x102, 0x105, 0x5, 0x20, 0x11, 0x2, 
    0x103, 0x105, 0x5, 0x72, 0x3a, 0x2, 0x104, 0x100, 0x3, 0x2, 0x2, 0x2, 
    0x104, 0x101, 0x3, 0x2, 0x2, 0x2, 0x104, 0x102, 0x3, 0x2, 0x2, 0x2, 
    0x104, 0x103, 0x3, 0x2, 0x2, 0x2, 0x105, 0x108, 0x3, 0x2, 0x2, 0x2, 
    0x106, 0x108, 0x7, 0x45, 0x2, 0x2, 0x107, 0xfd, 0x3, 0x2, 0x2, 0x2, 
    0x107, 0x106, 0x3, 0x2, 0x2, 0x2, 0x108, 0x9, 0x3, 0x2, 0x2, 0x2, 0x109, 
    0x10f, 0x5, 0xc, 0x7, 0x2, 0x10a, 0x10f, 0x7, 0x20, 0x2, 0x2, 0x10b, 
    0x10f, 0x7, 0x2c, 0x2, 0x2, 0x10c, 0x10f, 0x7, 0x30, 0x2, 0x2, 0x10d, 
    0x10f, 0x7, 0x33, 0x2, 0x2, 0x10e, 0x109, 0x3, 0x2, 0x2, 0x2, 0x10e, 
    0x10a, 0x3, 0x2, 0x2, 0x2, 0x10e, 0x10b, 0x3, 0x2, 0x2, 0x2, 0x10e, 
    0x10c, 0x3, 0x2, 0x2, 0x2, 0x10e, 0x10d, 0x3, 0x2, 0x2, 0x2, 0x10f, 
    0xb, 0x3, 0x2, 0x2, 0x2, 0x110, 0x119, 0x5, 0x68, 0x35, 0x2, 0x111, 
    0x119, 0x7, 0x25, 0x2, 0x2, 0x112, 0x119, 0x7, 0x24, 0x2, 0x2, 0x113, 
    0x119, 0x7, 0x23, 0x2, 0x2, 0x114, 0x119, 0x7, 0x28, 0x2, 0x2, 0x115, 
    0x119, 0x7, 0x3, 0x2, 0x2, 0x116, 0x119, 0x7, 0x14, 0x2, 0x2, 0x117, 
    0x119, 0x7, 0x29, 0x2, 0x2, 0x118, 0x110, 0x3, 0x2, 0x2, 0x2, 0x118, 
    0x111, 0x3, 0x2, 0x2, 0x2, 0x118, 0x112, 0x3, 0x2, 0x2, 0x2, 0x118, 
    0x113, 0x3, 0x2, 0x2, 0x2, 0x118, 0x114, 0x3, 0x2, 0x2, 0x2, 0x118, 
    0x115, 0x3, 0x2, 0x2, 0x2, 0x118, 0x116, 0x3, 0x2, 0x2, 0x2, 0x118, 
    0x117, 0x3, 0x2, 0x2, 0x2, 0x119, 0xd, 0x3, 0x2, 0x2, 0x2, 0x11a, 0x11d, 
    0x7, 0x14, 0x2, 0x2, 0x11b, 0x11d, 0x5, 0x68, 0x35, 0x2, 0x11c, 0x11a, 
    0x3, 0x2, 0x2, 0x2, 0x11c, 0x11b, 0x3, 0x2, 0x2, 0x2, 0x11d, 0xf, 0x3, 
    0x2, 0x2, 0x2, 0x11e, 0x11f, 0x7, 0xb, 0x2, 0x2, 0x11f, 0x121, 0x7, 
    0x71, 0x2, 0x2, 0x120, 0x122, 0x5, 0x12, 0xa, 0x2, 0x121, 0x120, 0x3, 
    0x2, 0x2, 0x2, 0x121, 0x122, 0x3, 0x2, 0x2, 0x2, 0x122, 0x125, 0x3, 
    0x2, 0x2, 0x2, 0x123, 0x124, 0x7, 0x13, 0x2, 0x2, 0x124, 0x126, 0x5, 
    0xc8, 0x65, 0x2, 0x125, 0x123, 0x3, 0x2, 0x2, 0x2, 0x125, 0x126, 0x3, 
    0x2, 0x2, 0x2, 0x126, 0x129, 0x3, 0x2, 0x2, 0x2, 0x127, 0x128, 0x7, 
    0x1a, 0x2, 0x2, 0x128, 0x12a, 0x5, 0xc6, 0x64, 0x2, 0x129, 0x127, 0x3, 
    0x2, 0x2, 0x2, 0x129, 0x12a, 0x3, 0x2, 0x2, 0x2, 0x12a, 0x12b, 0x3, 
    0x2, 0x2, 0x2, 0x12b, 0x12c, 0x5, 0x22, 0x12, 0x2, 0x12c, 0x11, 0x3, 
    0x2, 0x2, 0x2, 0x12d, 0x12e, 0x7, 0x4a, 0x2, 0x2, 0x12e, 0x133, 0x5, 
    0x14, 0xb, 0x2, 0x12f, 0x130, 0x7, 0x46, 0x2, 0x2, 0x130, 0x132, 0x5, 
    0x14, 0xb, 0x2, 0x131, 0x12f, 0x3, 0x2, 0x2, 0x2, 0x132, 0x135, 0x3, 
    0x2, 0x2, 0x2, 0x133, 0x131, 0x3, 0x2, 0x2, 0x2, 0x133, 0x134, 0x3, 
    0x2, 0x2, 0x2, 0x134, 0x136, 0x3, 0x2, 0x2, 0x2, 0x135, 0x133, 0x3, 
    0x2, 0x2, 0x2, 0x136, 0x137, 0x7, 0x49, 0x2, 0x2, 0x137, 0x13, 0x3, 
    0x2, 0x2, 0x2, 0x138, 0x13a, 0x5, 0x68, 0x35, 0x2, 0x139, 0x138, 0x3, 
    0x2, 0x2, 0x2, 0x13a, 0x13d, 0x3, 0x2, 0x2, 0x2, 0x13b, 0x139, 0x3, 
    0x2, 0x2, 0x2, 0x13b, 0x13c, 0x3, 0x2, 0x2, 0x2, 0x13c, 0x13e, 0x3, 
    0x2, 0x2, 0x2, 0x13d, 0x13b, 0x3, 0x2, 0x2, 0x2, 0x13e, 0x147, 0x7, 
    0x71, 0x2, 0x2, 0x13f, 0x143, 0x7, 0x13, 0x2, 0x2, 0x140, 0x142, 0x5, 
    0x68, 0x35, 0x2, 0x141, 0x140, 0x3, 0x2, 0x2, 0x2, 0x142, 0x145, 0x3, 
    0x2, 0x2, 0x2, 0x143, 0x141, 0x3, 0x2, 0x2, 0x2, 0x143, 0x144, 0x3, 
    0x2, 0x2, 0x2, 0x144, 0x146, 0x3, 0x2, 0x2, 0x2, 0x145, 0x143, 0x3, 
    0x2, 0x2, 0x2, 0x146, 0x148, 0x5, 0x16, 0xc, 0x2, 0x147, 0x13f, 0x3, 
    0x2, 0x2, 0x2, 0x147, 0x148, 0x3, 0x2, 0x2, 0x2, 0x148, 0x15, 0x3, 0x2, 
    0x2, 0x2, 0x149, 0x14e, 0x5, 0xc8, 0x65, 0x2, 0x14a, 0x14b, 0x7, 0x5b, 
    0x2, 0x2, 0x14b, 0x14d, 0x5, 0xc8, 0x65, 0x2, 0x14c, 0x14a, 0x3, 0x2, 
    0x2, 0x2, 0x14d, 0x150, 0x3, 0x2, 0x2, 0x2, 0x14e, 0x14c, 0x3, 0x2, 
    0x2, 0x2, 0x14e, 0x14f, 0x3, 0x2, 0x2, 0x2, 0x14f, 0x17, 0x3, 0x2, 0x2, 
    0x2, 0x150, 0x14e, 0x3, 0x2, 0x2, 0x2, 0x151, 0x152, 0x7, 0x12, 0x2, 
    0x2, 0x152, 0x155, 0x7, 0x71, 0x2, 0x2, 0x153, 0x154, 0x7, 0x1a, 0x2, 
    0x2, 0x154, 0x156, 0x5, 0xc6, 0x64, 0x2, 0x155, 0x153, 0x3, 0x2, 0x2, 
    0x2, 0x155, 0x156, 0x3, 0x2, 0x2, 0x2, 0x156, 0x157, 0x3, 0x2, 0x2, 
    0x2, 0x157, 0x159, 0x7, 0x41, 0x2, 0x2, 0x158, 0x15a, 0x5, 0x1a, 0xe, 
    0x2, 0x159, 0x158, 0x3, 0x2, 0x2, 0x2, 0x159, 0x15a, 0x3, 0x2, 0x2, 
    0x2, 0x15a, 0x15c, 0x3, 0x2, 0x2, 0x2, 0x15b, 0x15d, 0x7, 0x46, 0x2, 
    0x2, 0x15c, 0x15b, 0x3, 0x2, 0x2, 0x2, 0x15c, 0x15d, 0x3, 0x2, 0x2, 
    0x2, 0x15d, 0x15f, 0x3, 0x2, 0x2, 0x2, 0x15e, 0x160, 0x5, 0x1e, 0x10, 
    0x2, 0x15f, 0x15e, 0x3, 0x2, 0x2, 0x2, 0x15f, 0x160, 0x3, 0x2, 0x2, 
    0x2, 0x160, 0x161, 0x3, 0x2, 0x2, 0x2, 0x161, 0x162, 0x7, 0x42, 0x2, 
    0x2, 0x162, 0x19, 0x3, 0x2, 0x2, 0x2, 0x163, 0x168, 0x5, 0x1c, 0xf, 
    0x2, 0x164, 0x165, 0x7, 0x46, 0x2, 0x2, 0x165, 0x167, 0x5, 0x1c, 0xf, 
    0x2, 0x166, 0x164, 0x3, 0x2, 0x2, 0x2, 0x167, 0x16a, 0x3, 0x2, 0x2, 
    0x2, 0x168, 0x166, 0x3, 0x2, 0x2, 0x2, 0x168, 0x169, 0x3, 0x2, 0x2, 
    0x2, 0x169, 0x1b, 0x3, 0x2, 0x2, 0x2, 0x16a, 0x168, 0x3, 0x2, 0x2, 0x2, 
    0x16b, 0x16d, 0x5, 0x68, 0x35, 0x2, 0x16c, 0x16b, 0x3, 0x2, 0x2, 0x2, 
    0x16d, 0x170, 0x3, 0x2, 0x2, 0x2, 0x16e, 0x16c, 0x3, 0x2, 0x2, 0x2, 
    0x16e, 0x16f, 0x3, 0x2, 0x2, 0x2, 0x16f, 0x171, 0x3, 0x2, 0x2, 0x2, 
    0x170, 0x16e, 0x3, 0x2, 0x2, 0x2, 0x171, 0x173, 0x7, 0x71, 0x2, 0x2, 
    0x172, 0x174, 0x5, 0xd2, 0x6a, 0x2, 0x173, 0x172, 0x3, 0x2, 0x2, 0x2, 
    0x173, 0x174, 0x3, 0x2, 0x2, 0x2, 0x174, 0x176, 0x3, 0x2, 0x2, 0x2, 
    0x175, 0x177, 0x5, 0x22, 0x12, 0x2, 0x176, 0x175, 0x3, 0x2, 0x2, 0x2, 
    0x176, 0x177, 0x3, 0x2, 0x2, 0x2, 0x177, 0x1d, 0x3, 0x2, 0x2, 0x2, 0x178, 
    0x17c, 0x7, 0x45, 0x2, 0x2, 0x179, 0x17b, 0x5, 0x26, 0x14, 0x2, 0x17a, 
    0x179, 0x3, 0x2, 0x2, 0x2, 0x17b, 0x17e, 0x3, 0x2, 0x2, 0x2, 0x17c, 
    0x17a, 0x3, 0x2, 0x2, 0x2, 0x17c, 0x17d, 0x3, 0x2, 0x2, 0x2, 0x17d, 
    0x1f, 0x3, 0x2, 0x2, 0x2, 0x17e, 0x17c, 0x3, 0x2, 0x2, 0x2, 0x17f, 0x180, 
    0x7, 0x1e, 0x2, 0x2, 0x180, 0x182, 0x7, 0x71, 0x2, 0x2, 0x181, 0x183, 
    0x5, 0x12, 0xa, 0x2, 0x182, 0x181, 0x3, 0x2, 0x2, 0x2, 0x182, 0x183, 
    0x3, 0x2, 0x2, 0x2, 0x183, 0x186, 0x3, 0x2, 0x2, 0x2, 0x184, 0x185, 
    0x7, 0x13, 0x2, 0x2, 0x185, 0x187, 0x5, 0xc6, 0x64, 0x2, 0x186, 0x184, 
    0x3, 0x2, 0x2, 0x2, 0x186, 0x187, 0x3, 0x2, 0x2, 0x2, 0x187, 0x188, 
    0x3, 0x2, 0x2, 0x2, 0x188, 0x189, 0x5, 0x24, 0x13, 0x2, 0x189, 0x21, 
    0x3, 0x2, 0x2, 0x2, 0x18a, 0x18e, 0x7, 0x41, 0x2, 0x2, 0x18b, 0x18d, 
    0x5, 0x26, 0x14, 0x2, 0x18c, 0x18b, 0x3, 0x2, 0x2, 0x2, 0x18d, 0x190, 
    0x3, 0x2, 0x2, 0x2, 0x18e, 0x18c, 0x3, 0x2, 0x2, 0x2, 0x18e, 0x18f, 
    0x3, 0x2, 0x2, 0x2, 0x18f, 0x191, 0x3, 0x2, 0x2, 0x2, 0x190, 0x18e, 
    0x3, 0x2, 0x2, 0x2, 0x191, 0x192, 0x7, 0x42, 0x2, 0x2, 0x192, 0x23, 
    0x3, 0x2, 0x2, 0x2, 0x193, 0x197, 0x7, 0x41, 0x2, 0x2, 0x194, 0x196, 
    0x5, 0x38, 0x1d, 0x2, 0x195, 0x194, 0x3, 0x2, 0x2, 0x2, 0x196, 0x199, 
    0x3, 0x2, 0x2, 0x2, 0x197, 0x195, 0x3, 0x2, 0x2, 0x2, 0x197, 0x198, 
    0x3, 0x2, 0x2, 0x2, 0x198, 0x19a, 0x3, 0x2, 0x2, 0x2, 0x199, 0x197, 
    0x3, 0x2, 0x2, 0x2, 0x19a, 0x19b, 0x7, 0x42, 0x2, 0x2, 0x19b, 0x25, 
    0x3, 0x2, 0x2, 0x2, 0x19c, 0x1a9, 0x7, 0x45, 0x2, 0x2, 0x19d, 0x19f, 
    0x7, 0x28, 0x2, 0x2, 0x19e, 0x19d, 0x3, 0x2, 0x2, 0x2, 0x19e, 0x19f, 
    0x3, 0x2, 0x2, 0x2, 0x19f, 0x1a0, 0x3, 0x2, 0x2, 0x2, 0x1a0, 0x1a9, 
    0x5, 0x82, 0x42, 0x2, 0x1a1, 0x1a3, 0x5, 0xa, 0x6, 0x2, 0x1a2, 0x1a1, 
    0x3, 0x2, 0x2, 0x2, 0x1a3, 0x1a6, 0x3, 0x2, 0x2, 0x2, 0x1a4, 0x1a2, 
    0x3, 0x2, 0x2, 0x2, 0x1a4, 0x1a5, 0x3, 0x2, 0x2, 0x2, 0x1a5, 0x1a7, 
    0x3, 0x2, 0x2, 0x2, 0x1a6, 0x1a4, 0x3, 0x2, 0x2, 0x2, 0x1a7, 0x1a9, 
    0x5, 0x28, 0x15, 0x2, 0x1a8, 0x19c, 0x3, 0x2, 0x2, 0x2, 0x1a8, 0x19e, 
    0x3, 0x2, 0x2, 0x2, 0x1a8, 0x1a4, 0x3, 0x2, 0x2, 0x2, 0x1a9, 0x27, 0x3, 
    0x2, 0x2, 0x2, 0x1aa, 0x1b4, 0x5, 0x2a, 0x16, 0x2, 0x1ab, 0x1b4, 0x5, 
    0x30, 0x19, 0x2, 0x1ac, 0x1b4, 0x5, 0x36, 0x1c, 0x2, 0x1ad, 0x1b4, 0x5, 
    0x34, 0x1b, 0x2, 0x1ae, 0x1b4, 0x5, 0x32, 0x1a, 0x2, 0x1af, 0x1b4, 0x5, 
    0x20, 0x11, 0x2, 0x1b0, 0x1b4, 0x5, 0x72, 0x3a, 0x2, 0x1b1, 0x1b4, 0x5, 
    0x10, 0x9, 0x2, 0x1b2, 0x1b4, 0x5, 0x18, 0xd, 0x2, 0x1b3, 0x1aa, 0x3, 
    0x2, 0x2, 0x2, 0x1b3, 0x1ab, 0x3, 0x2, 0x2, 0x2, 0x1b3, 0x1ac, 0x3, 
    0x2, 0x2, 0x2, 0x1b3, 0x1ad, 0x3, 0x2, 0x2, 0x2, 0x1b3, 0x1ae, 0x3, 
    0x2, 0x2, 0x2, 0x1b3, 0x1af, 0x3, 0x2, 0x2, 0x2, 0x1b3, 0x1b0, 0x3, 
    0x2, 0x2, 0x2, 0x1b3, 0x1b1, 0x3, 0x2, 0x2, 0x2, 0x1b3, 0x1b2, 0x3, 
    0x2, 0x2, 0x2, 0x1b4, 0x29, 0x3, 0x2, 0x2, 0x2, 0x1b5, 0x1b6, 0x5, 0x2e, 
    0x18, 0x2, 0x1b6, 0x1b7, 0x7, 0x71, 0x2, 0x2, 0x1b7, 0x1bc, 0x5, 0x56, 
    0x2c, 0x2, 0x1b8, 0x1b9, 0x7, 0x43, 0x2, 0x2, 0x1b9, 0x1bb, 0x7, 0x44, 
    0x2, 0x2, 0x1ba, 0x1b8, 0x3, 0x2, 0x2, 0x2, 0x1bb, 0x1be, 0x3, 0x2, 
    0x2, 0x2, 0x1bc, 0x1ba, 0x3, 0x2, 0x2, 0x2, 0x1bc, 0x1bd, 0x3, 0x2, 
    0x2, 0x2, 0x1bd, 0x1c1, 0x3, 0x2, 0x2, 0x2, 0x1be, 0x1bc, 0x3, 0x2, 
    0x2, 0x2, 0x1bf, 0x1c0, 0x7, 0x2f, 0x2, 0x2, 0x1c0, 0x1c2, 0x5, 0x54, 
    0x2b, 0x2, 0x1c1, 0x1bf, 0x3, 0x2, 0x2, 0x2, 0x1c1, 0x1c2, 0x3, 0x2, 
    0x2, 0x2, 0x1c2, 0x1c3, 0x3, 0x2, 0x2, 0x2, 0x1c3, 0x1c4, 0x5, 0x2c, 
    0x17, 0x2, 0x1c4, 0x2b, 0x3, 0x2, 0x2, 0x2, 0x1c5, 0x1c8, 0x5, 0x82, 
    0x42, 0x2, 0x1c6, 0x1c8, 0x7, 0x45, 0x2, 0x2, 0x1c7, 0x1c5, 0x3, 0x2, 
    0x2, 0x2, 0x1c7, 0x1c6, 0x3, 0x2, 0x2, 0x2, 0x1c8, 0x2d, 0x3, 0x2, 0x2, 
    0x2, 0x1c9, 0x1cc, 0x5, 0xc8, 0x65, 0x2, 0x1ca, 0x1cc, 0x7, 0x32, 0x2, 
    0x2, 0x1cb, 0x1c9, 0x3, 0x2, 0x2, 0x2, 0x1cb, 0x1ca, 0x3, 0x2, 0x2, 
    0x2, 0x1cc, 0x2f, 0x3, 0x2, 0x2, 0x2, 0x1cd, 0x1ce, 0x5, 0x12, 0xa, 
    0x2, 0x1ce, 0x1cf, 0x5, 0x2a, 0x16, 0x2, 0x1cf, 0x31, 0x3, 0x2, 0x2, 
    0x2, 0x1d0, 0x1d1, 0x5, 0x12, 0xa, 0x2, 0x1d1, 0x1d2, 0x5, 0x34, 0x1b, 
    0x2, 0x1d2, 0x33, 0x3, 0x2, 0x2, 0x2, 0x1d3, 0x1d4, 0x7, 0x71, 0x2, 
    0x2, 0x1d4, 0x1d7, 0x5, 0x56, 0x2c, 0x2, 0x1d5, 0x1d6, 0x7, 0x2f, 0x2, 
    0x2, 0x1d6, 0x1d8, 0x5, 0x54, 0x2b, 0x2, 0x1d7, 0x1d5, 0x3, 0x2, 0x2, 
    0x2, 0x1d7, 0x1d8, 0x3, 0x2, 0x2, 0x2, 0x1d8, 0x1d9, 0x3, 0x2, 0x2, 
    0x2, 0x1d9, 0x1da, 0x5, 0x82, 0x42, 0x2, 0x1da, 0x35, 0x3, 0x2, 0x2, 
    0x2, 0x1db, 0x1dc, 0x5, 0xc8, 0x65, 0x2, 0x1dc, 0x1dd, 0x5, 0x46, 0x24, 
    0x2, 0x1dd, 0x1de, 0x7, 0x45, 0x2, 0x2, 0x1de, 0x37, 0x3, 0x2, 0x2, 
    0x2, 0x1df, 0x1e1, 0x5, 0xa, 0x6, 0x2, 0x1e0, 0x1df, 0x3, 0x2, 0x2, 
    0x2, 0x1e1, 0x1e4, 0x3, 0x2, 0x2, 0x2, 0x1e2, 0x1e0, 0x3, 0x2, 0x2, 
    0x2, 0x1e2, 0x1e3, 0x3, 0x2, 0x2, 0x2, 0x1e3, 0x1e5, 0x3, 0x2, 0x2, 
    0x2, 0x1e4, 0x1e2, 0x3, 0x2, 0x2, 0x2, 0x1e5, 0x1e8, 0x5, 0x3a, 0x1e, 
    0x2, 0x1e6, 0x1e8, 0x7, 0x45, 0x2, 0x2, 0x1e7, 0x1e2, 0x3, 0x2, 0x2, 
    0x2, 0x1e7, 0x1e6, 0x3, 0x2, 0x2, 0x2, 0x1e8, 0x39, 0x3, 0x2, 0x2, 0x2, 
    0x1e9, 0x1f1, 0x5, 0x3c, 0x1f, 0x2, 0x1ea, 0x1f1, 0x5, 0x40, 0x21, 0x2, 
    0x1eb, 0x1f1, 0x5, 0x44, 0x23, 0x2, 0x1ec, 0x1f1, 0x5, 0x20, 0x11, 0x2, 
    0x1ed, 0x1f1, 0x5, 0x72, 0x3a, 0x2, 0x1ee, 0x1f1, 0x5, 0x10, 0x9, 0x2, 
    0x1ef, 0x1f1, 0x5, 0x18, 0xd, 0x2, 0x1f0, 0x1e9, 0x3, 0x2, 0x2, 0x2, 
    0x1f0, 0x1ea, 0x3, 0x2, 0x2, 0x2, 0x1f0, 0x1eb, 0x3, 0x2, 0x2, 0x2, 
    0x1f0, 0x1ec, 0x3, 0x2, 0x2, 0x2, 0x1f0, 0x1ed, 0x3, 0x2, 0x2, 0x2, 
    0x1f0, 0x1ee, 0x3, 0x2, 0x2, 0x2, 0x1f0, 0x1ef, 0x3, 0x2, 0x2, 0x2, 
    0x1f1, 0x3b, 0x3, 0x2, 0x2, 0x2, 0x1f2, 0x1f3, 0x5, 0xc8, 0x65, 0x2, 
    0x1f3, 0x1f8, 0x5, 0x3e, 0x20, 0x2, 0x1f4, 0x1f5, 0x7, 0x46, 0x2, 0x2, 
    0x1f5, 0x1f7, 0x5, 0x3e, 0x20, 0x2, 0x1f6, 0x1f4, 0x3, 0x2, 0x2, 0x2, 
    0x1f7, 0x1fa, 0x3, 0x2, 0x2, 0x2, 0x1f8, 0x1f6, 0x3, 0x2, 0x2, 0x2, 
    0x1f8, 0x1f9, 0x3, 0x2, 0x2, 0x2, 0x1f9, 0x1fb, 0x3, 0x2, 0x2, 0x2, 
    0x1fa, 0x1f8, 0x3, 0x2, 0x2, 0x2, 0x1fb, 0x1fc, 0x7, 0x45, 0x2, 0x2, 
    0x1fc, 0x3d, 0x3, 0x2, 0x2, 0x2, 0x1fd, 0x202, 0x7, 0x71, 0x2, 0x2, 
    0x1fe, 0x1ff, 0x7, 0x43, 0x2, 0x2, 0x1ff, 0x201, 0x7, 0x44, 0x2, 0x2, 
    0x200, 0x1fe, 0x3, 0x2, 0x2, 0x2, 0x201, 0x204, 0x3, 0x2, 0x2, 0x2, 
    0x202, 0x200, 0x3, 0x2, 0x2, 0x2, 0x202, 0x203, 0x3, 0x2, 0x2, 0x2, 
    0x203, 0x205, 0x3, 0x2, 0x2, 0x2, 0x204, 0x202, 0x3, 0x2, 0x2, 0x2, 
    0x205, 0x206, 0x7, 0x48, 0x2, 0x2, 0x206, 0x207, 0x5, 0x4c, 0x27, 0x2, 
    0x207, 0x3f, 0x3, 0x2, 0x2, 0x2, 0x208, 0x20a, 0x5, 0x42, 0x22, 0x2, 
    0x209, 0x208, 0x3, 0x2, 0x2, 0x2, 0x20a, 0x20d, 0x3, 0x2, 0x2, 0x2, 
    0x20b, 0x209, 0x3, 0x2, 0x2, 0x2, 0x20b, 0x20c, 0x3, 0x2, 0x2, 0x2, 
    0x20c, 0x218, 0x3, 0x2, 0x2, 0x2, 0x20d, 0x20b, 0x3, 0x2, 0x2, 0x2, 
    0x20e, 0x219, 0x5, 0x2e, 0x18, 0x2, 0x20f, 0x213, 0x5, 0x12, 0xa, 0x2, 
    0x210, 0x212, 0x5, 0x68, 0x35, 0x2, 0x211, 0x210, 0x3, 0x2, 0x2, 0x2, 
    0x212, 0x215, 0x3, 0x2, 0x2, 0x2, 0x213, 0x211, 0x3, 0x2, 0x2, 0x2, 
    0x213, 0x214, 0x3, 0x2, 0x2, 0x2, 0x214, 0x216, 0x3, 0x2, 0x2, 0x2, 
    0x215, 0x213, 0x3, 0x2, 0x2, 0x2, 0x216, 0x217, 0x5, 0x2e, 0x18, 0x2, 
    0x217, 0x219, 0x3, 0x2, 0x2, 0x2, 0x218, 0x20e, 0x3, 0x2, 0x2, 0x2, 
    0x218, 0x20f, 0x3, 0x2, 0x2, 0x2, 0x219, 0x21a, 0x3, 0x2, 0x2, 0x2, 
    0x21a, 0x21b, 0x7, 0x71, 0x2, 0x2, 0x21b, 0x220, 0x5, 0x56, 0x2c, 0x2, 
    0x21c, 0x21d, 0x7, 0x43, 0x2, 0x2, 0x21d, 0x21f, 0x7, 0x44, 0x2, 0x2, 
    0x21e, 0x21c, 0x3, 0x2, 0x2, 0x2, 0x21f, 0x222, 0x3, 0x2, 0x2, 0x2, 
    0x220, 0x21e, 0x3, 0x2, 0x2, 0x2, 0x220, 0x221, 0x3, 0x2, 0x2, 0x2, 
    0x221, 0x225, 0x3, 0x2, 0x2, 0x2, 0x222, 0x220, 0x3, 0x2, 0x2, 0x2, 
    0x223, 0x224, 0x7, 0x2f, 0x2, 0x2, 0x224, 0x226, 0x5, 0x54, 0x2b, 0x2, 
    0x225, 0x223, 0x3, 0x2, 0x2, 0x2, 0x225, 0x226, 0x3, 0x2, 0x2, 0x2, 
    0x226, 0x227, 0x3, 0x2, 0x2, 0x2, 0x227, 0x228, 0x5, 0x2c, 0x17, 0x2, 
    0x228, 0x41, 0x3, 0x2, 0x2, 0x2, 0x229, 0x230, 0x5, 0x68, 0x35, 0x2, 
    0x22a, 0x230, 0x7, 0x25, 0x2, 0x2, 0x22b, 0x230, 0x7, 0x3, 0x2, 0x2, 
    0x22c, 0x230, 0x7, 0xe, 0x2, 0x2, 0x22d, 0x230, 0x7, 0x28, 0x2, 0x2, 
    0x22e, 0x230, 0x7, 0x29, 0x2, 0x2, 0x22f, 0x229, 0x3, 0x2, 0x2, 0x2, 
    0x22f, 0x22a, 0x3, 0x2, 0x2, 0x2, 0x22f, 0x22b, 0x3, 0x2, 0x2, 0x2, 
    0x22f, 0x22c, 0x3, 0x2, 0x2, 0x2, 0x22f, 0x22d, 0x3, 0x2, 0x2, 0x2, 
    0x22f, 0x22e, 0x3, 0x2, 0x2, 0x2, 0x230, 0x43, 0x3, 0x2, 0x2, 0x2, 0x231, 
    0x232, 0x5, 0x12, 0xa, 0x2, 0x232, 0x233, 0x5, 0x40, 0x21, 0x2, 0x233, 
    0x45, 0x3, 0x2, 0x2, 0x2, 0x234, 0x239, 0x5, 0x48, 0x25, 0x2, 0x235, 
    0x236, 0x7, 0x46, 0x2, 0x2, 0x236, 0x238, 0x5, 0x48, 0x25, 0x2, 0x237, 
    0x235, 0x3, 0x2, 0x2, 0x2, 0x238, 0x23b, 0x3, 0x2, 0x2, 0x2, 0x239, 
    0x237, 0x3, 0x2, 0x2, 0x2, 0x239, 0x23a, 0x3, 0x2, 0x2, 0x2, 0x23a, 
    0x47, 0x3, 0x2, 0x2, 0x2, 0x23b, 0x239, 0x3, 0x2, 0x2, 0x2, 0x23c, 0x23f, 
    0x5, 0x4a, 0x26, 0x2, 0x23d, 0x23e, 0x7, 0x48, 0x2, 0x2, 0x23e, 0x240, 
    0x5, 0x4c, 0x27, 0x2, 0x23f, 0x23d, 0x3, 0x2, 0x2, 0x2, 0x23f, 0x240, 
    0x3, 0x2, 0x2, 0x2, 0x240, 0x49, 0x3, 0x2, 0x2, 0x2, 0x241, 0x246, 0x7, 
    0x71, 0x2, 0x2, 0x242, 0x243, 0x7, 0x43, 0x2, 0x2, 0x243, 0x245, 0x7, 
    0x44, 0x2, 0x2, 0x244, 0x242, 0x3, 0x2, 0x2, 0x2, 0x245, 0x248, 0x3, 
    0x2, 0x2, 0x2, 0x246, 0x244, 0x3, 0x2, 0x2, 0x2, 0x246, 0x247, 0x3, 
    0x2, 0x2, 0x2, 0x247, 0x4b, 0x3, 0x2, 0x2, 0x2, 0x248, 0x246, 0x3, 0x2, 
    0x2, 0x2, 0x249, 0x24c, 0x5, 0x4e, 0x28, 0x2, 0x24a, 0x24c, 0x5, 0xa8, 
    0x55, 0x2, 0x24b, 0x249, 0x3, 0x2, 0x2, 0x2, 0x24b, 0x24a, 0x3, 0x2, 
    0x2, 0x2, 0x24c, 0x4d, 0x3, 0x2, 0x2, 0x2, 0x24d, 0x259, 0x7, 0x41, 
    0x2, 0x2, 0x24e, 0x253, 0x5, 0x4c, 0x27, 0x2, 0x24f, 0x250, 0x7, 0x46, 
    0x2, 0x2, 0x250, 0x252, 0x5, 0x4c, 0x27, 0x2, 0x251, 0x24f, 0x3, 0x2, 
    0x2, 0x2, 0x252, 0x255, 0x3, 0x2, 0x2, 0x2, 0x253, 0x251, 0x3, 0x2, 
    0x2, 0x2, 0x253, 0x254, 0x3, 0x2, 0x2, 0x2, 0x254, 0x257, 0x3, 0x2, 
    0x2, 0x2, 0x255, 0x253, 0x3, 0x2, 0x2, 0x2, 0x256, 0x258, 0x7, 0x46, 
    0x2, 0x2, 0x257, 0x256, 0x3, 0x2, 0x2, 0x2, 0x257, 0x258, 0x3, 0x2, 
    0x2, 0x2, 0x258, 0x25a, 0x3, 0x2, 0x2, 0x2, 0x259, 0x24e, 0x3, 0x2, 
    0x2, 0x2, 0x259, 0x25a, 0x3, 0x2, 0x2, 0x2, 0x25a, 0x25b, 0x3, 0x2, 
    0x2, 0x2, 0x25b, 0x25c, 0x7, 0x42, 0x2, 0x2, 0x25c, 0x4f, 0x3, 0x2, 
    0x2, 0x2, 0x25d, 0x25f, 0x7, 0x71, 0x2, 0x2, 0x25e, 0x260, 0x5, 0xcc, 
    0x67, 0x2, 0x25f, 0x25e, 0x3, 0x2, 0x2, 0x2, 0x25f, 0x260, 0x3, 0x2, 
    0x2, 0x2, 0x260, 0x268, 0x3, 0x2, 0x2, 0x2, 0x261, 0x262, 0x7, 0x47, 
    0x2, 0x2, 0x262, 0x264, 0x7, 0x71, 0x2, 0x2, 0x263, 0x265, 0x5, 0xcc, 
    0x67, 0x2, 0x264, 0x263, 0x3, 0x2, 0x2, 0x2, 0x264, 0x265, 0x3, 0x2, 
    0x2, 0x2, 0x265, 0x267, 0x3, 0x2, 0x2, 0x2, 0x266, 0x261, 0x3, 0x2, 
    0x2, 0x2, 0x267, 0x26a, 0x3, 0x2, 0x2, 0x2, 0x268, 0x266, 0x3, 0x2, 
    0x2, 0x2, 0x268, 0x269, 0x3, 0x2, 0x2, 0x2, 0x269, 0x51, 0x3, 0x2, 0x2, 
    0x2, 0x26a, 0x268, 0x3, 0x2, 0x2, 0x2, 0x26b, 0x278, 0x5, 0xc8, 0x65, 
    0x2, 0x26c, 0x26e, 0x5, 0x68, 0x35, 0x2, 0x26d, 0x26c, 0x3, 0x2, 0x2, 
    0x2, 0x26e, 0x271, 0x3, 0x2, 0x2, 0x2, 0x26f, 0x26d, 0x3, 0x2, 0x2, 
    0x2, 0x26f, 0x270, 0x3, 0x2, 0x2, 0x2, 0x270, 0x272, 0x3, 0x2, 0x2, 
    0x2, 0x271, 0x26f, 0x3, 0x2, 0x2, 0x2, 0x272, 0x275, 0x7, 0x4d, 0x2, 
    0x2, 0x273, 0x274, 0x9, 0x2, 0x2, 0x2, 0x274, 0x276, 0x5, 0xc8, 0x65, 
    0x2, 0x275, 0x273, 0x3, 0x2, 0x2, 0x2, 0x275, 0x276, 0x3, 0x2, 0x2, 
    0x2, 0x276, 0x278, 0x3, 0x2, 0x2, 0x2, 0x277, 0x26b, 0x3, 0x2, 0x2, 
    0x2, 0x277, 0x26f, 0x3, 0x2, 0x2, 0x2, 0x278, 0x53, 0x3, 0x2, 0x2, 0x2, 
    0x279, 0x27e, 0x5, 0x5e, 0x30, 0x2, 0x27a, 0x27b, 0x7, 0x46, 0x2, 0x2, 
    0x27b, 0x27d, 0x5, 0x5e, 0x30, 0x2, 0x27c, 0x27a, 0x3, 0x2, 0x2, 0x2, 
    0x27d, 0x280, 0x3, 0x2, 0x2, 0x2, 0x27e, 0x27c, 0x3, 0x2, 0x2, 0x2, 
    0x27e, 0x27f, 0x3, 0x2, 0x2, 0x2, 0x27f, 0x55, 0x3, 0x2, 0x2, 0x2, 0x280, 
    0x27e, 0x3, 0x2, 0x2, 0x2, 0x281, 0x283, 0x7, 0x3f, 0x2, 0x2, 0x282, 
    0x284, 0x5, 0x58, 0x2d, 0x2, 0x283, 0x282, 0x3, 0x2, 0x2, 0x2, 0x283, 
    0x284, 0x3, 0x2, 0x2, 0x2, 0x284, 0x285, 0x3, 0x2, 0x2, 0x2, 0x285, 
    0x286, 0x7, 0x40, 0x2, 0x2, 0x286, 0x57, 0x3, 0x2, 0x2, 0x2, 0x287, 
    0x28c, 0x5, 0x5a, 0x2e, 0x2, 0x288, 0x289, 0x7, 0x46, 0x2, 0x2, 0x289, 
    0x28b, 0x5, 0x5a, 0x2e, 0x2, 0x28a, 0x288, 0x3, 0x2, 0x2, 0x2, 0x28b, 
    0x28e, 0x3, 0x2, 0x2, 0x2, 0x28c, 0x28a, 0x3, 0x2, 0x2, 0x2, 0x28c, 
    0x28d, 0x3, 0x2, 0x2, 0x2, 0x28d, 0x291, 0x3, 0x2, 0x2, 0x2, 0x28e, 
    0x28c, 0x3, 0x2, 0x2, 0x2, 0x28f, 0x290, 0x7, 0x46, 0x2, 0x2, 0x290, 
    0x292, 0x5, 0x5c, 0x2f, 0x2, 0x291, 0x28f, 0x3, 0x2, 0x2, 0x2, 0x291, 
    0x292, 0x3, 0x2, 0x2, 0x2, 0x292, 0x295, 0x3, 0x2, 0x2, 0x2, 0x293, 
    0x295, 0x5, 0x5c, 0x2f, 0x2, 0x294, 0x287, 0x3, 0x2, 0x2, 0x2, 0x294, 
    0x293, 0x3, 0x2, 0x2, 0x2, 0x295, 0x59, 0x3, 0x2, 0x2, 0x2, 0x296, 0x298, 
    0x5, 0xe, 0x8, 0x2, 0x297, 0x296, 0x3, 0x2, 0x2, 0x2, 0x298, 0x29b, 
    0x3, 0x2, 0x2, 0x2, 0x299, 0x297, 0x3, 0x2, 0x2, 0x2, 0x299, 0x29a, 
    0x3, 0x2, 0x2, 0x2, 0x29a, 0x29c, 0x3, 0x2, 0x2, 0x2, 0x29b, 0x299, 
    0x3, 0x2, 0x2, 0x2, 0x29c, 0x29d, 0x5, 0xc8, 0x65, 0x2, 0x29d, 0x29e, 
    0x5, 0x4a, 0x26, 0x2, 0x29e, 0x5b, 0x3, 0x2, 0x2, 0x2, 0x29f, 0x2a1, 
    0x5, 0xe, 0x8, 0x2, 0x2a0, 0x29f, 0x3, 0x2, 0x2, 0x2, 0x2a1, 0x2a4, 
    0x3, 0x2, 0x2, 0x2, 0x2a2, 0x2a0, 0x3, 0x2, 0x2, 0x2, 0x2a2, 0x2a3, 
    0x3, 0x2, 0x2, 0x2, 0x2a3, 0x2a5, 0x3, 0x2, 0x2, 0x2, 0x2a4, 0x2a2, 
    0x3, 0x2, 0x2, 0x2, 0x2a5, 0x2a9, 0x5, 0xc8, 0x65, 0x2, 0x2a6, 0x2a8, 
    0x5, 0x68, 0x35, 0x2, 0x2a7, 0x2a6, 0x3, 0x2, 0x2, 0x2, 0x2a8, 0x2ab, 
    0x3, 0x2, 0x2, 0x2, 0x2a9, 0x2a7, 0x3, 0x2, 0x2, 0x2, 0x2a9, 0x2aa, 
    0x3, 0x2, 0x2, 0x2, 0x2aa, 0x2ac, 0x3, 0x2, 0x2, 0x2, 0x2ab, 0x2a9, 
    0x3, 0x2, 0x2, 0x2, 0x2ac, 0x2ad, 0x7, 0x6d, 0x2, 0x2, 0x2ad, 0x2ae, 
    0x5, 0x4a, 0x26, 0x2, 0x2ae, 0x5d, 0x3, 0x2, 0x2, 0x2, 0x2af, 0x2b4, 
    0x7, 0x71, 0x2, 0x2, 0x2b0, 0x2b1, 0x7, 0x47, 0x2, 0x2, 0x2b1, 0x2b3, 
    0x7, 0x71, 0x2, 0x2, 0x2b2, 0x2b0, 0x3, 0x2, 0x2, 0x2, 0x2b3, 0x2b6, 
    0x3, 0x2, 0x2, 0x2, 0x2b4, 0x2b2, 0x3, 0x2, 0x2, 0x2, 0x2b4, 0x2b5, 
    0x3, 0x2, 0x2, 0x2, 0x2b5, 0x5f, 0x3, 0x2, 0x2, 0x2, 0x2b6, 0x2b4, 0x3, 
    0x2, 0x2, 0x2, 0x2b7, 0x2be, 0x5, 0x62, 0x32, 0x2, 0x2b8, 0x2be, 0x5, 
    0x64, 0x33, 0x2, 0x2b9, 0x2be, 0x7, 0x3c, 0x2, 0x2, 0x2ba, 0x2be, 0x7, 
    0x3d, 0x2, 0x2, 0x2bb, 0x2be, 0x7, 0x3b, 0x2, 0x2, 0x2bc, 0x2be, 0x7, 
    0x3e, 0x2, 0x2, 0x2bd, 0x2b7, 0x3, 0x2, 0x2, 0x2, 0x2bd, 0x2b8, 0x3, 
    0x2, 0x2, 0x2, 0x2bd, 0x2b9, 0x3, 0x2, 0x2, 0x2, 0x2bd, 0x2ba, 0x3, 
    0x2, 0x2, 0x2, 0x2bd, 0x2bb, 0x3, 0x2, 0x2, 0x2, 0x2bd, 0x2bc, 0x3, 
    0x2, 0x2, 0x2, 0x2be, 0x61, 0x3, 0x2, 0x2, 0x2, 0x2bf, 0x2c0, 0x9, 0x3, 
    0x2, 0x2, 0x2c0, 0x63, 0x3, 0x2, 0x2, 0x2, 0x2c1, 0x2c2, 0x9, 0x4, 0x2, 
    0x2, 0x2c2, 0x65, 0x3, 0x2, 0x2, 0x2, 0x2c3, 0x2c4, 0x7, 0x71, 0x2, 
    0x2, 0x2c4, 0x2c6, 0x7, 0x47, 0x2, 0x2, 0x2c5, 0x2c3, 0x3, 0x2, 0x2, 
    0x2, 0x2c6, 0x2c9, 0x3, 0x2, 0x2, 0x2, 0x2c7, 0x2c5, 0x3, 0x2, 0x2, 
    0x2, 0x2c7, 0x2c8, 0x3, 0x2, 0x2, 0x2, 0x2c8, 0x2ca, 0x3, 0x2, 0x2, 
    0x2, 0x2c9, 0x2c7, 0x3, 0x2, 0x2, 0x2, 0x2ca, 0x2cb, 0x7, 0x6c, 0x2, 
    0x2, 0x2cb, 0x2cc, 0x7, 0x71, 0x2, 0x2, 0x2cc, 0x67, 0x3, 0x2, 0x2, 
    0x2, 0x2cd, 0x2ce, 0x7, 0x6c, 0x2, 0x2, 0x2ce, 0x2d1, 0x5, 0x5e, 0x30, 
    0x2, 0x2cf, 0x2d1, 0x5, 0x66, 0x34, 0x2, 0x2d0, 0x2cd, 0x3, 0x2, 0x2, 
    0x2, 0x2d0, 0x2cf, 0x3, 0x2, 0x2, 0x2, 0x2d1, 0x2d8, 0x3, 0x2, 0x2, 
    0x2, 0x2d2, 0x2d5, 0x7, 0x3f, 0x2, 0x2, 0x2d3, 0x2d6, 0x5, 0x6a, 0x36, 
    0x2, 0x2d4, 0x2d6, 0x5, 0x6e, 0x38, 0x2, 0x2d5, 0x2d3, 0x3, 0x2, 0x2, 
    0x2, 0x2d5, 0x2d4, 0x3, 0x2, 0x2, 0x2, 0x2d5, 0x2d6, 0x3, 0x2, 0x2, 
    0x2, 0x2d6, 0x2d7, 0x3, 0x2, 0x2, 0x2, 0x2d7, 0x2d9, 0x7, 0x40, 0x2, 
    0x2, 0x2d8, 0x2d2, 0x3, 0x2, 0x2, 0x2, 0x2d8, 0x2d9, 0x3, 0x2, 0x2, 
    0x2, 0x2d9, 0x69, 0x3, 0x2, 0x2, 0x2, 0x2da, 0x2df, 0x5, 0x6c, 0x37, 
    0x2, 0x2db, 0x2dc, 0x7, 0x46, 0x2, 0x2, 0x2dc, 0x2de, 0x5, 0x6c, 0x37, 
    0x2, 0x2dd, 0x2db, 0x3, 0x2, 0x2, 0x2, 0x2de, 0x2e1, 0x3, 0x2, 0x2, 
    0x2, 0x2df, 0x2dd, 0x3, 0x2, 0x2, 0x2, 0x2df, 0x2e0, 0x3, 0x2, 0x2, 
    0x2, 0x2e0, 0x6b, 0x3, 0x2, 0x2, 0x2, 0x2e1, 0x2df, 0x3, 0x2, 0x2, 0x2, 
    0x2e2, 0x2e3, 0x7, 0x71, 0x2, 0x2, 0x2e3, 0x2e4, 0x7, 0x48, 0x2, 0x2, 
    0x2e4, 0x2e5, 0x5, 0x6e, 0x38, 0x2, 0x2e5, 0x6d, 0x3, 0x2, 0x2, 0x2, 
    0x2e6, 0x2ea, 0x5, 0xa8, 0x55, 0x2, 0x2e7, 0x2ea, 0x5, 0x68, 0x35, 0x2, 
    0x2e8, 0x2ea, 0x5, 0x70, 0x39, 0x2, 0x2e9, 0x2e6, 0x3, 0x2, 0x2, 0x2, 
    0x2e9, 0x2e7, 0x3, 0x2, 0x2, 0x2, 0x2e9, 0x2e8, 0x3, 0x2, 0x2, 0x2, 
    0x2ea, 0x6f, 0x3, 0x2, 0x2, 0x2, 0x2eb, 0x2f4, 0x7, 0x41, 0x2, 0x2, 
    0x2ec, 0x2f1, 0x5, 0x6e, 0x38, 0x2, 0x2ed, 0x2ee, 0x7, 0x46, 0x2, 0x2, 
    0x2ee, 0x2f0, 0x5, 0x6e, 0x38, 0x2, 0x2ef, 0x2ed, 0x3, 0x2, 0x2, 0x2, 
    0x2f0, 0x2f3, 0x3, 0x2, 0x2, 0x2, 0x2f1, 0x2ef, 0x3, 0x2, 0x2, 0x2, 
    0x2f1, 0x2f2, 0x3, 0x2, 0x2, 0x2, 0x2f2, 0x2f5, 0x3, 0x2, 0x2, 0x2, 
    0x2f3, 0x2f1, 0x3, 0x2, 0x2, 0x2, 0x2f4, 0x2ec, 0x3, 0x2, 0x2, 0x2, 
    0x2f4, 0x2f5, 0x3, 0x2, 0x2, 0x2, 0x2f5, 0x2f7, 0x3, 0x2, 0x2, 0x2, 
    0x2f6, 0x2f8, 0x7, 0x46, 0x2, 0x2, 0x2f7, 0x2f6, 0x3, 0x2, 0x2, 0x2, 
    0x2f7, 0x2f8, 0x3, 0x2, 0x2, 0x2, 0x2f8, 0x2f9, 0x3, 0x2, 0x2, 0x2, 
    0x2f9, 0x2fa, 0x7, 0x42, 0x2, 0x2, 0x2fa, 0x71, 0x3, 0x2, 0x2, 0x2, 
    0x2fb, 0x2fc, 0x7, 0x6c, 0x2, 0x2, 0x2fc, 0x2fd, 0x7, 0x1e, 0x2, 0x2, 
    0x2fd, 0x2fe, 0x7, 0x71, 0x2, 0x2, 0x2fe, 0x2ff, 0x5, 0x74, 0x3b, 0x2, 
    0x2ff, 0x73, 0x3, 0x2, 0x2, 0x2, 0x300, 0x304, 0x7, 0x41, 0x2, 0x2, 
    0x301, 0x303, 0x5, 0x76, 0x3c, 0x2, 0x302, 0x301, 0x3, 0x2, 0x2, 0x2, 
    0x303, 0x306, 0x3, 0x2, 0x2, 0x2, 0x304, 0x302, 0x3, 0x2, 0x2, 0x2, 
    0x304, 0x305, 0x3, 0x2, 0x2, 0x2, 0x305, 0x307, 0x3, 0x2, 0x2, 0x2, 
    0x306, 0x304, 0x3, 0x2, 0x2, 0x2, 0x307, 0x308, 0x7, 0x42, 0x2, 0x2, 
    0x308, 0x75, 0x3, 0x2, 0x2, 0x2, 0x309, 0x30b, 0x5, 0xa, 0x6, 0x2, 0x30a, 
    0x309, 0x3, 0x2, 0x2, 0x2, 0x30b, 0x30e, 0x3, 0x2, 0x2, 0x2, 0x30c, 
    0x30a, 0x3, 0x2, 0x2, 0x2, 0x30c, 0x30d, 0x3, 0x2, 0x2, 0x2, 0x30d, 
    0x30f, 0x3, 0x2, 0x2, 0x2, 0x30e, 0x30c, 0x3, 0x2, 0x2, 0x2, 0x30f, 
    0x312, 0x5, 0x78, 0x3d, 0x2, 0x310, 0x312, 0x7, 0x45, 0x2, 0x2, 0x311, 
    0x30c, 0x3, 0x2, 0x2, 0x2, 0x311, 0x310, 0x3, 0x2, 0x2, 0x2, 0x312, 
    0x77, 0x3, 0x2, 0x2, 0x2, 0x313, 0x314, 0x5, 0xc8, 0x65, 0x2, 0x314, 
    0x315, 0x5, 0x7a, 0x3e, 0x2, 0x315, 0x316, 0x7, 0x45, 0x2, 0x2, 0x316, 
    0x328, 0x3, 0x2, 0x2, 0x2, 0x317, 0x319, 0x5, 0x10, 0x9, 0x2, 0x318, 
    0x31a, 0x7, 0x45, 0x2, 0x2, 0x319, 0x318, 0x3, 0x2, 0x2, 0x2, 0x319, 
    0x31a, 0x3, 0x2, 0x2, 0x2, 0x31a, 0x328, 0x3, 0x2, 0x2, 0x2, 0x31b, 
    0x31d, 0x5, 0x20, 0x11, 0x2, 0x31c, 0x31e, 0x7, 0x45, 0x2, 0x2, 0x31d, 
    0x31c, 0x3, 0x2, 0x2, 0x2, 0x31d, 0x31e, 0x3, 0x2, 0x2, 0x2, 0x31e, 
    0x328, 0x3, 0x2, 0x2, 0x2, 0x31f, 0x321, 0x5, 0x18, 0xd, 0x2, 0x320, 
    0x322, 0x7, 0x45, 0x2, 0x2, 0x321, 0x320, 0x3, 0x2, 0x2, 0x2, 0x321, 
    0x322, 0x3, 0x2, 0x2, 0x2, 0x322, 0x328, 0x3, 0x2, 0x2, 0x2, 0x323, 
    0x325, 0x5, 0x72, 0x3a, 0x2, 0x324, 0x326, 0x7, 0x45, 0x2, 0x2, 0x325, 
    0x324, 0x3, 0x2, 0x2, 0x2, 0x325, 0x326, 0x3, 0x2, 0x2, 0x2, 0x326, 
    0x328, 0x3, 0x2, 0x2, 0x2, 0x327, 0x313, 0x3, 0x2, 0x2, 0x2, 0x327, 
    0x317, 0x3, 0x2, 0x2, 0x2, 0x327, 0x31b, 0x3, 0x2, 0x2, 0x2, 0x327, 
    0x31f, 0x3, 0x2, 0x2, 0x2, 0x327, 0x323, 0x3, 0x2, 0x2, 0x2, 0x328, 
    0x79, 0x3, 0x2, 0x2, 0x2, 0x329, 0x32c, 0x5, 0x7c, 0x3f, 0x2, 0x32a, 
    0x32c, 0x5, 0x7e, 0x40, 0x2, 0x32b, 0x329, 0x3, 0x2, 0x2, 0x2, 0x32b, 
    0x32a, 0x3, 0x2, 0x2, 0x2, 0x32c, 0x7b, 0x3, 0x2, 0x2, 0x2, 0x32d, 0x32e, 
    0x7, 0x71, 0x2, 0x2, 0x32e, 0x32f, 0x7, 0x3f, 0x2, 0x2, 0x32f, 0x331, 
    0x7, 0x40, 0x2, 0x2, 0x330, 0x332, 0x5, 0x80, 0x41, 0x2, 0x331, 0x330, 
    0x3, 0x2, 0x2, 0x2, 0x331, 0x332, 0x3, 0x2, 0x2, 0x2, 0x332, 0x7d, 0x3, 
    0x2, 0x2, 0x2, 0x333, 0x334, 0x5, 0x46, 0x24, 0x2, 0x334, 0x7f, 0x3, 
    0x2, 0x2, 0x2, 0x335, 0x336, 0x7, 0xe, 0x2, 0x2, 0x336, 0x337, 0x5, 
    0x6e, 0x38, 0x2, 0x337, 0x81, 0x3, 0x2, 0x2, 0x2, 0x338, 0x33c, 0x7, 
    0x41, 0x2, 0x2, 0x339, 0x33b, 0x5, 0x84, 0x43, 0x2, 0x33a, 0x339, 0x3, 
    0x2, 0x2, 0x2, 0x33b, 0x33e, 0x3, 0x2, 0x2, 0x2, 0x33c, 0x33a, 0x3, 
    0x2, 0x2, 0x2, 0x33c, 0x33d, 0x3, 0x2, 0x2, 0x2, 0x33d, 0x33f, 0x3, 
    0x2, 0x2, 0x2, 0x33e, 0x33c, 0x3, 0x2, 0x2, 0x2, 0x33f, 0x340, 0x7, 
    0x42, 0x2, 0x2, 0x340, 0x83, 0x3, 0x2, 0x2, 0x2, 0x341, 0x342, 0x5, 
    0x86, 0x44, 0x2, 0x342, 0x343, 0x7, 0x45, 0x2, 0x2, 0x343, 0x347, 0x3, 
    0x2, 0x2, 0x2, 0x344, 0x347, 0x5, 0x8a, 0x46, 0x2, 0x345, 0x347, 0x5, 
    0x88, 0x45, 0x2, 0x346, 0x341, 0x3, 0x2, 0x2, 0x2, 0x346, 0x344, 0x3, 
    0x2, 0x2, 0x2, 0x346, 0x345, 0x3, 0x2, 0x2, 0x2, 0x347, 0x85, 0x3, 0x2, 
    0x2, 0x2, 0x348, 0x34a, 0x5, 0xe, 0x8, 0x2, 0x349, 0x348, 0x3, 0x2, 
    0x2, 0x2, 0x34a, 0x34d, 0x3, 0x2, 0x2, 0x2, 0x34b, 0x349, 0x3, 0x2, 
    0x2, 0x2, 0x34b, 0x34c, 0x3, 0x2, 0x2, 0x2, 0x34c, 0x34e, 0x3, 0x2, 
    0x2, 0x2, 0x34d, 0x34b, 0x3, 0x2, 0x2, 0x2, 0x34e, 0x34f, 0x5, 0xc8, 
    0x65, 0x2, 0x34f, 0x350, 0x5, 0x46, 0x24, 0x2, 0x350, 0x87, 0x3, 0x2, 
    0x2, 0x2, 0x351, 0x353, 0x5, 0xc, 0x7, 0x2, 0x352, 0x351, 0x3, 0x2, 
    0x2, 0x2, 0x353, 0x356, 0x3, 0x2, 0x2, 0x2, 0x354, 0x352, 0x3, 0x2, 
    0x2, 0x2, 0x354, 0x355, 0x3, 0x2, 0x2, 0x2, 0x355, 0x359, 0x3, 0x2, 
    0x2, 0x2, 0x356, 0x354, 0x3, 0x2, 0x2, 0x2, 0x357, 0x35a, 0x5, 0x10, 
    0x9, 0x2, 0x358, 0x35a, 0x5, 0x20, 0x11, 0x2, 0x359, 0x357, 0x3, 0x2, 
    0x2, 0x2, 0x359, 0x358, 0x3, 0x2, 0x2, 0x2, 0x35a, 0x35d, 0x3, 0x2, 
    0x2, 0x2, 0x35b, 0x35d, 0x7, 0x45, 0x2, 0x2, 0x35c, 0x354, 0x3, 0x2, 
    0x2, 0x2, 0x35c, 0x35b, 0x3, 0x2, 0x2, 0x2, 0x35d, 0x89, 0x3, 0x2, 0x2, 
    0x2, 0x35e, 0x3c7, 0x5, 0x82, 0x42, 0x2, 0x35f, 0x360, 0x7, 0x4, 0x2, 
    0x2, 0x360, 0x363, 0x5, 0xa8, 0x55, 0x2, 0x361, 0x362, 0x7, 0x4e, 0x2, 
    0x2, 0x362, 0x364, 0x5, 0xa8, 0x55, 0x2, 0x363, 0x361, 0x3, 0x2, 0x2, 
    0x2, 0x363, 0x364, 0x3, 0x2, 0x2, 0x2, 0x364, 0x365, 0x3, 0x2, 0x2, 
    0x2, 0x365, 0x366, 0x7, 0x45, 0x2, 0x2, 0x366, 0x3c7, 0x3, 0x2, 0x2, 
    0x2, 0x367, 0x368, 0x7, 0x18, 0x2, 0x2, 0x368, 0x369, 0x5, 0xa2, 0x52, 
    0x2, 0x369, 0x36c, 0x5, 0x8a, 0x46, 0x2, 0x36a, 0x36b, 0x7, 0x11, 0x2, 
    0x2, 0x36b, 0x36d, 0x5, 0x8a, 0x46, 0x2, 0x36c, 0x36a, 0x3, 0x2, 0x2, 
    0x2, 0x36c, 0x36d, 0x3, 0x2, 0x2, 0x2, 0x36d, 0x3c7, 0x3, 0x2, 0x2, 
    0x2, 0x36e, 0x36f, 0x7, 0x17, 0x2, 0x2, 0x36f, 0x370, 0x7, 0x3f, 0x2, 
    0x2, 0x370, 0x371, 0x5, 0x9c, 0x4f, 0x2, 0x371, 0x372, 0x7, 0x40, 0x2, 
    0x2, 0x372, 0x373, 0x5, 0x8a, 0x46, 0x2, 0x373, 0x3c7, 0x3, 0x2, 0x2, 
    0x2, 0x374, 0x375, 0x7, 0x34, 0x2, 0x2, 0x375, 0x376, 0x5, 0xa2, 0x52, 
    0x2, 0x376, 0x377, 0x5, 0x8a, 0x46, 0x2, 0x377, 0x3c7, 0x3, 0x2, 0x2, 
    0x2, 0x378, 0x379, 0x7, 0xf, 0x2, 0x2, 0x379, 0x37a, 0x5, 0x8a, 0x46, 
    0x2, 0x37a, 0x37b, 0x7, 0x34, 0x2, 0x2, 0x37b, 0x37c, 0x5, 0xa2, 0x52, 
    0x2, 0x37c, 0x37d, 0x7, 0x45, 0x2, 0x2, 0x37d, 0x3c7, 0x3, 0x2, 0x2, 
    0x2, 0x37e, 0x37f, 0x7, 0x31, 0x2, 0x2, 0x37f, 0x389, 0x5, 0x82, 0x42, 
    0x2, 0x380, 0x382, 0x5, 0x8c, 0x47, 0x2, 0x381, 0x380, 0x3, 0x2, 0x2, 
    0x2, 0x382, 0x383, 0x3, 0x2, 0x2, 0x2, 0x383, 0x381, 0x3, 0x2, 0x2, 
    0x2, 0x383, 0x384, 0x3, 0x2, 0x2, 0x2, 0x384, 0x386, 0x3, 0x2, 0x2, 
    0x2, 0x385, 0x387, 0x5, 0x90, 0x49, 0x2, 0x386, 0x385, 0x3, 0x2, 0x2, 
    0x2, 0x386, 0x387, 0x3, 0x2, 0x2, 0x2, 0x387, 0x38a, 0x3, 0x2, 0x2, 
    0x2, 0x388, 0x38a, 0x5, 0x90, 0x49, 0x2, 0x389, 0x381, 0x3, 0x2, 0x2, 
    0x2, 0x389, 0x388, 0x3, 0x2, 0x2, 0x2, 0x38a, 0x3c7, 0x3, 0x2, 0x2, 
    0x2, 0x38b, 0x38c, 0x7, 0x31, 0x2, 0x2, 0x38c, 0x38d, 0x5, 0x92, 0x4a, 
    0x2, 0x38d, 0x391, 0x5, 0x82, 0x42, 0x2, 0x38e, 0x390, 0x5, 0x8c, 0x47, 
    0x2, 0x38f, 0x38e, 0x3, 0x2, 0x2, 0x2, 0x390, 0x393, 0x3, 0x2, 0x2, 
    0x2, 0x391, 0x38f, 0x3, 0x2, 0x2, 0x2, 0x391, 0x392, 0x3, 0x2, 0x2, 
    0x2, 0x392, 0x395, 0x3, 0x2, 0x2, 0x2, 0x393, 0x391, 0x3, 0x2, 0x2, 
    0x2, 0x394, 0x396, 0x5, 0x90, 0x49, 0x2, 0x395, 0x394, 0x3, 0x2, 0x2, 
    0x2, 0x395, 0x396, 0x3, 0x2, 0x2, 0x2, 0x396, 0x3c7, 0x3, 0x2, 0x2, 
    0x2, 0x397, 0x398, 0x7, 0x2b, 0x2, 0x2, 0x398, 0x399, 0x5, 0xa2, 0x52, 
    0x2, 0x399, 0x39d, 0x7, 0x41, 0x2, 0x2, 0x39a, 0x39c, 0x5, 0x98, 0x4d, 
    0x2, 0x39b, 0x39a, 0x3, 0x2, 0x2, 0x2, 0x39c, 0x39f, 0x3, 0x2, 0x2, 
    0x2, 0x39d, 0x39b, 0x3, 0x2, 0x2, 0x2, 0x39d, 0x39e, 0x3, 0x2, 0x2, 
    0x2, 0x39e, 0x3a3, 0x3, 0x2, 0x2, 0x2, 0x39f, 0x39d, 0x3, 0x2, 0x2, 
    0x2, 0x3a0, 0x3a2, 0x5, 0x9a, 0x4e, 0x2, 0x3a1, 0x3a0, 0x3, 0x2, 0x2, 
    0x2, 0x3a2, 0x3a5, 0x3, 0x2, 0x2, 0x2, 0x3a3, 0x3a1, 0x3, 0x2, 0x2, 
    0x2, 0x3a3, 0x3a4, 0x3, 0x2, 0x2, 0x2, 0x3a4, 0x3a6, 0x3, 0x2, 0x2, 
    0x2, 0x3a5, 0x3a3, 0x3, 0x2, 0x2, 0x2, 0x3a6, 0x3a7, 0x7, 0x42, 0x2, 
    0x2, 0x3a7, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x3a8, 0x3a9, 0x7, 0x2c, 0x2, 
    0x2, 0x3a9, 0x3aa, 0x5, 0xa2, 0x52, 0x2, 0x3aa, 0x3ab, 0x5, 0x82, 0x42, 
    0x2, 0x3ab, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x3ac, 0x3ae, 0x7, 0x26, 0x2, 
    0x2, 0x3ad, 0x3af, 0x5, 0xa8, 0x55, 0x2, 0x3ae, 0x3ad, 0x3, 0x2, 0x2, 
    0x2, 0x3ae, 0x3af, 0x3, 0x2, 0x2, 0x2, 0x3af, 0x3b0, 0x3, 0x2, 0x2, 
    0x2, 0x3b0, 0x3c7, 0x7, 0x45, 0x2, 0x2, 0x3b1, 0x3b2, 0x7, 0x2e, 0x2, 
    0x2, 0x3b2, 0x3b3, 0x5, 0xa8, 0x55, 0x2, 0x3b3, 0x3b4, 0x7, 0x45, 0x2, 
    0x2, 0x3b4, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x3b5, 0x3b7, 0x7, 0x6, 0x2, 
    0x2, 0x3b6, 0x3b8, 0x7, 0x71, 0x2, 0x2, 0x3b7, 0x3b6, 0x3, 0x2, 0x2, 
    0x2, 0x3b7, 0x3b8, 0x3, 0x2, 0x2, 0x2, 0x3b8, 0x3b9, 0x3, 0x2, 0x2, 
    0x2, 0x3b9, 0x3c7, 0x7, 0x45, 0x2, 0x2, 0x3ba, 0x3bc, 0x7, 0xd, 0x2, 
    0x2, 0x3bb, 0x3bd, 0x7, 0x71, 0x2, 0x2, 0x3bc, 0x3bb, 0x3, 0x2, 0x2, 
    0x2, 0x3bc, 0x3bd, 0x3, 0x2, 0x2, 0x2, 0x3bd, 0x3be, 0x3, 0x2, 0x2, 
    0x2, 0x3be, 0x3c7, 0x7, 0x45, 0x2, 0x2, 0x3bf, 0x3c7, 0x7, 0x45, 0x2, 
    0x2, 0x3c0, 0x3c1, 0x5, 0xa8, 0x55, 0x2, 0x3c1, 0x3c2, 0x7, 0x45, 0x2, 
    0x2, 0x3c2, 0x3c7, 0x3, 0x2, 0x2, 0x2, 0x3c3, 0x3c4, 0x7, 0x71, 0x2, 
    0x2, 0x3c4, 0x3c5, 0x7, 0x4e, 0x2, 0x2, 0x3c5, 0x3c7, 0x5, 0x8a, 0x46, 
    0x2, 0x3c6, 0x35e, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x35f, 0x3, 0x2, 0x2, 
    0x2, 0x3c6, 0x367, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x36e, 0x3, 0x2, 0x2, 
    0x2, 0x3c6, 0x374, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x378, 0x3, 0x2, 0x2, 
    0x2, 0x3c6, 0x37e, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x38b, 0x3, 0x2, 0x2, 
    0x2, 0x3c6, 0x397, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3a8, 0x3, 0x2, 0x2, 
    0x2, 0x3c6, 0x3ac, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3b1, 0x3, 0x2, 0x2, 
    0x2, 0x3c6, 0x3b5, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3ba, 0x3, 0x2, 0x2, 
    0x2, 0x3c6, 0x3bf, 0x3, 0x2, 0x2, 0x2, 0x3c6, 0x3c0, 0x3, 0x2, 0x2, 
    0x2, 0x3c6, 0x3c3, 0x3, 0x2, 0x2, 0x2, 0x3c7, 0x8b, 0x3, 0x2, 0x2, 0x2, 
    0x3c8, 0x3c9, 0x7, 0x9, 0x2, 0x2, 0x3c9, 0x3cd, 0x7, 0x3f, 0x2, 0x2, 
    0x3ca, 0x3cc, 0x5, 0xe, 0x8, 0x2, 0x3cb, 0x3ca, 0x3, 0x2, 0x2, 0x2, 
    0x3cc, 0x3cf, 0x3, 0x2, 0x2, 0x2, 0x3cd, 0x3cb, 0x3, 0x2, 0x2, 0x2, 
    0x3cd, 0x3ce, 0x3, 0x2, 0x2, 0x2, 0x3ce, 0x3d0, 0x3, 0x2, 0x2, 0x2, 
    0x3cf, 0x3cd, 0x3, 0x2, 0x2, 0x2, 0x3d0, 0x3d1, 0x5, 0x8e, 0x48, 0x2, 
    0x3d1, 0x3d2, 0x7, 0x71, 0x2, 0x2, 0x3d2, 0x3d3, 0x7, 0x40, 0x2, 0x2, 
    0x3d3, 0x3d4, 0x5, 0x82, 0x42, 0x2, 0x3d4, 0x8d, 0x3, 0x2, 0x2, 0x2, 
    0x3d5, 0x3da, 0x5, 0x5e, 0x30, 0x2, 0x3d6, 0x3d7, 0x7, 0x5c, 0x2, 0x2, 
    0x3d7, 0x3d9, 0x5, 0x5e, 0x30, 0x2, 0x3d8, 0x3d6, 0x3, 0x2, 0x2, 0x2, 
    0x3d9, 0x3dc, 0x3, 0x2, 0x2, 0x2, 0x3da, 0x3d8, 0x3, 0x2, 0x2, 0x2, 
    0x3da, 0x3db, 0x3, 0x2, 0x2, 0x2, 0x3db, 0x8f, 0x3, 0x2, 0x2, 0x2, 0x3dc, 
    0x3da, 0x3, 0x2, 0x2, 0x2, 0x3dd, 0x3de, 0x7, 0x15, 0x2, 0x2, 0x3de, 
    0x3df, 0x5, 0x82, 0x42, 0x2, 0x3df, 0x91, 0x3, 0x2, 0x2, 0x2, 0x3e0, 
    0x3e1, 0x7, 0x3f, 0x2, 0x2, 0x3e1, 0x3e3, 0x5, 0x94, 0x4b, 0x2, 0x3e2, 
    0x3e4, 0x7, 0x45, 0x2, 0x2, 0x3e3, 0x3e2, 0x3, 0x2, 0x2, 0x2, 0x3e3, 
    0x3e4, 0x3, 0x2, 0x2, 0x2, 0x3e4, 0x3e5, 0x3, 0x2, 0x2, 0x2, 0x3e5, 
    0x3e6, 0x7, 0x40, 0x2, 0x2, 0x3e6, 0x93, 0x3, 0x2, 0x2, 0x2, 0x3e7, 
    0x3ec, 0x5, 0x96, 0x4c, 0x2, 0x3e8, 0x3e9, 0x7, 0x45, 0x2, 0x2, 0x3e9, 
    0x3eb, 0x5, 0x96, 0x4c, 0x2, 0x3ea, 0x3e8, 0x3, 0x2, 0x2, 0x2, 0x3eb, 
    0x3ee, 0x3, 0x2, 0x2, 0x2, 0x3ec, 0x3ea, 0x3, 0x2, 0x2, 0x2, 0x3ec, 
    0x3ed, 0x3, 0x2, 0x2, 0x2, 0x3ed, 0x95, 0x3, 0x2, 0x2, 0x2, 0x3ee, 0x3ec, 
    0x3, 0x2, 0x2, 0x2, 0x3ef, 0x3f1, 0x5, 0xe, 0x8, 0x2, 0x3f0, 0x3ef, 
    0x3, 0x2, 0x2, 0x2, 0x3f1, 0x3f4, 0x3, 0x2, 0x2, 0x2, 0x3f2, 0x3f0, 
    0x3, 0x2, 0x2, 0x2, 0x3f2, 0x3f3, 0x3, 0x2, 0x2, 0x2, 0x3f3, 0x3f5, 
    0x3, 0x2, 0x2, 0x2, 0x3f4, 0x3f2, 0x3, 0x2, 0x2, 0x2, 0x3f5, 0x3f6, 
    0x5, 0x50, 0x29, 0x2, 0x3f6, 0x3f7, 0x5, 0x4a, 0x26, 0x2, 0x3f7, 0x3f8, 
    0x7, 0x48, 0x2, 0x2, 0x3f8, 0x3f9, 0x5, 0xa8, 0x55, 0x2, 0x3f9, 0x97, 
    0x3, 0x2, 0x2, 0x2, 0x3fa, 0x3fc, 0x5, 0x9a, 0x4e, 0x2, 0x3fb, 0x3fa, 
    0x3, 0x2, 0x2, 0x2, 0x3fc, 0x3fd, 0x3, 0x2, 0x2, 0x2, 0x3fd, 0x3fb, 
    0x3, 0x2, 0x2, 0x2, 0x3fd, 0x3fe, 0x3, 0x2, 0x2, 0x2, 0x3fe, 0x400, 
    0x3, 0x2, 0x2, 0x2, 0x3ff, 0x401, 0x5, 0x84, 0x43, 0x2, 0x400, 0x3ff, 
    0x3, 0x2, 0x2, 0x2, 0x401, 0x402, 0x3, 0x2, 0x2, 0x2, 0x402, 0x400, 
    0x3, 0x2, 0x2, 0x2, 0x402, 0x403, 0x3, 0x2, 0x2, 0x2, 0x403, 0x99, 0x3, 
    0x2, 0x2, 0x2, 0x404, 0x407, 0x7, 0x8, 0x2, 0x2, 0x405, 0x408, 0x5, 
    0xa8, 0x55, 0x2, 0x406, 0x408, 0x7, 0x71, 0x2, 0x2, 0x407, 0x405, 0x3, 
    0x2, 0x2, 0x2, 0x407, 0x406, 0x3, 0x2, 0x2, 0x2, 0x408, 0x409, 0x3, 
    0x2, 0x2, 0x2, 0x409, 0x40d, 0x7, 0x4e, 0x2, 0x2, 0x40a, 0x40b, 0x7, 
    0xe, 0x2, 0x2, 0x40b, 0x40d, 0x7, 0x4e, 0x2, 0x2, 0x40c, 0x404, 0x3, 
    0x2, 0x2, 0x2, 0x40c, 0x40a, 0x3, 0x2, 0x2, 0x2, 0x40d, 0x9b, 0x3, 0x2, 
    0x2, 0x2, 0x40e, 0x41b, 0x5, 0xa0, 0x51, 0x2, 0x40f, 0x411, 0x5, 0x9e, 
    0x50, 0x2, 0x410, 0x40f, 0x3, 0x2, 0x2, 0x2, 0x410, 0x411, 0x3, 0x2, 
    0x2, 0x2, 0x411, 0x412, 0x3, 0x2, 0x2, 0x2, 0x412, 0x414, 0x7, 0x45, 
    0x2, 0x2, 0x413, 0x415, 0x5, 0xa8, 0x55, 0x2, 0x414, 0x413, 0x3, 0x2, 
    0x2, 0x2, 0x414, 0x415, 0x3, 0x2, 0x2, 0x2, 0x415, 0x416, 0x3, 0x2, 
    0x2, 0x2, 0x416, 0x418, 0x7, 0x45, 0x2, 0x2, 0x417, 0x419, 0x5, 0xa4, 
    0x53, 0x2, 0x418, 0x417, 0x3, 0x2, 0x2, 0x2, 0x418, 0x419, 0x3, 0x2, 
    0x2, 0x2, 0x419, 0x41b, 0x3, 0x2, 0x2, 0x2, 0x41a, 0x40e, 0x3, 0x2, 
    0x2, 0x2, 0x41a, 0x410, 0x3, 0x2, 0x2, 0x2, 0x41b, 0x9d, 0x3, 0x2, 0x2, 
    0x2, 0x41c, 0x41f, 0x5, 0x86, 0x44, 0x2, 0x41d, 0x41f, 0x5, 0xa4, 0x53, 
    0x2, 0x41e, 0x41c, 0x3, 0x2, 0x2, 0x2, 0x41e, 0x41d, 0x3, 0x2, 0x2, 
    0x2, 0x41f, 0x9f, 0x3, 0x2, 0x2, 0x2, 0x420, 0x422, 0x5, 0xe, 0x8, 0x2, 
    0x421, 0x420, 0x3, 0x2, 0x2, 0x2, 0x422, 0x425, 0x3, 0x2, 0x2, 0x2, 
    0x423, 0x421, 0x3, 0x2, 0x2, 0x2, 0x423, 0x424, 0x3, 0x2, 0x2, 0x2, 
    0x424, 0x426, 0x3, 0x2, 0x2, 0x2, 0x425, 0x423, 0x3, 0x2, 0x2, 0x2, 
    0x426, 0x427, 0x5, 0xc8, 0x65, 0x2, 0x427, 0x428, 0x5, 0x4a, 0x26, 0x2, 
    0x428, 0x429, 0x7, 0x4e, 0x2, 0x2, 0x429, 0x42a, 0x5, 0xa8, 0x55, 0x2, 
    0x42a, 0xa1, 0x3, 0x2, 0x2, 0x2, 0x42b, 0x42c, 0x7, 0x3f, 0x2, 0x2, 
    0x42c, 0x42d, 0x5, 0xa8, 0x55, 0x2, 0x42d, 0x42e, 0x7, 0x40, 0x2, 0x2, 
    0x42e, 0xa3, 0x3, 0x2, 0x2, 0x2, 0x42f, 0x434, 0x5, 0xa8, 0x55, 0x2, 
    0x430, 0x431, 0x7, 0x46, 0x2, 0x2, 0x431, 0x433, 0x5, 0xa8, 0x55, 0x2, 
    0x432, 0x430, 0x3, 0x2, 0x2, 0x2, 0x433, 0x436, 0x3, 0x2, 0x2, 0x2, 
    0x434, 0x432, 0x3, 0x2, 0x2, 0x2, 0x434, 0x435, 0x3, 0x2, 0x2, 0x2, 
    0x435, 0xa5, 0x3, 0x2, 0x2, 0x2, 0x436, 0x434, 0x3, 0x2, 0x2, 0x2, 0x437, 
    0x438, 0x7, 0x71, 0x2, 0x2, 0x438, 0x43a, 0x7, 0x3f, 0x2, 0x2, 0x439, 
    0x43b, 0x5, 0xa4, 0x53, 0x2, 0x43a, 0x439, 0x3, 0x2, 0x2, 0x2, 0x43a, 
    0x43b, 0x3, 0x2, 0x2, 0x2, 0x43b, 0x43c, 0x3, 0x2, 0x2, 0x2, 0x43c, 
    0x44a, 0x7, 0x40, 0x2, 0x2, 0x43d, 0x43e, 0x7, 0x2d, 0x2, 0x2, 0x43e, 
    0x440, 0x7, 0x3f, 0x2, 0x2, 0x43f, 0x441, 0x5, 0xa4, 0x53, 0x2, 0x440, 
    0x43f, 0x3, 0x2, 0x2, 0x2, 0x440, 0x441, 0x3, 0x2, 0x2, 0x2, 0x441, 
    0x442, 0x3, 0x2, 0x2, 0x2, 0x442, 0x44a, 0x7, 0x40, 0x2, 0x2, 0x443, 
    0x444, 0x7, 0x2a, 0x2, 0x2, 0x444, 0x446, 0x7, 0x3f, 0x2, 0x2, 0x445, 
    0x447, 0x5, 0xa4, 0x53, 0x2, 0x446, 0x445, 0x3, 0x2, 0x2, 0x2, 0x446, 
    0x447, 0x3, 0x2, 0x2, 0x2, 0x447, 0x448, 0x3, 0x2, 0x2, 0x2, 0x448, 
    0x44a, 0x7, 0x40, 0x2, 0x2, 0x449, 0x437, 0x3, 0x2, 0x2, 0x2, 0x449, 
    0x43d, 0x3, 0x2, 0x2, 0x2, 0x449, 0x443, 0x3, 0x2, 0x2, 0x2, 0x44a, 
    0xa7, 0x3, 0x2, 0x2, 0x2, 0x44b, 0x44c, 0x8, 0x55, 0x1, 0x2, 0x44c, 
    0x471, 0x5, 0xb0, 0x59, 0x2, 0x44d, 0x471, 0x5, 0xa6, 0x54, 0x2, 0x44e, 
    0x44f, 0x7, 0x21, 0x2, 0x2, 0x44f, 0x471, 0x5, 0xb4, 0x5b, 0x2, 0x450, 
    0x454, 0x7, 0x3f, 0x2, 0x2, 0x451, 0x453, 0x5, 0x68, 0x35, 0x2, 0x452, 
    0x451, 0x3, 0x2, 0x2, 0x2, 0x453, 0x456, 0x3, 0x2, 0x2, 0x2, 0x454, 
    0x452, 0x3, 0x2, 0x2, 0x2, 0x454, 0x455, 0x3, 0x2, 0x2, 0x2, 0x455, 
    0x457, 0x3, 0x2, 0x2, 0x2, 0x456, 0x454, 0x3, 0x2, 0x2, 0x2, 0x457, 
    0x458, 0x5, 0xc8, 0x65, 0x2, 0x458, 0x459, 0x7, 0x40, 0x2, 0x2, 0x459, 
    0x45a, 0x5, 0xa8, 0x55, 0x17, 0x45a, 0x471, 0x3, 0x2, 0x2, 0x2, 0x45b, 
    0x45c, 0x9, 0x5, 0x2, 0x2, 0x45c, 0x471, 0x5, 0xa8, 0x55, 0x15, 0x45d, 
    0x45e, 0x9, 0x6, 0x2, 0x2, 0x45e, 0x471, 0x5, 0xa8, 0x55, 0x14, 0x45f, 
    0x471, 0x5, 0xaa, 0x56, 0x2, 0x460, 0x461, 0x5, 0xc8, 0x65, 0x2, 0x461, 
    0x467, 0x7, 0x6b, 0x2, 0x2, 0x462, 0x464, 0x5, 0xcc, 0x67, 0x2, 0x463, 
    0x462, 0x3, 0x2, 0x2, 0x2, 0x463, 0x464, 0x3, 0x2, 0x2, 0x2, 0x464, 
    0x465, 0x3, 0x2, 0x2, 0x2, 0x465, 0x468, 0x7, 0x71, 0x2, 0x2, 0x466, 
    0x468, 0x7, 0x21, 0x2, 0x2, 0x467, 0x463, 0x3, 0x2, 0x2, 0x2, 0x467, 
    0x466, 0x3, 0x2, 0x2, 0x2, 0x468, 0x471, 0x3, 0x2, 0x2, 0x2, 0x469, 
    0x46a, 0x5, 0xb2, 0x5a, 0x2, 0x46a, 0x46c, 0x7, 0x6b, 0x2, 0x2, 0x46b, 
    0x46d, 0x5, 0xcc, 0x67, 0x2, 0x46c, 0x46b, 0x3, 0x2, 0x2, 0x2, 0x46c, 
    0x46d, 0x3, 0x2, 0x2, 0x2, 0x46d, 0x46e, 0x3, 0x2, 0x2, 0x2, 0x46e, 
    0x46f, 0x7, 0x21, 0x2, 0x2, 0x46f, 0x471, 0x3, 0x2, 0x2, 0x2, 0x470, 
    0x44b, 0x3, 0x2, 0x2, 0x2, 0x470, 0x44d, 0x3, 0x2, 0x2, 0x2, 0x470, 
    0x44e, 0x3, 0x2, 0x2, 0x2, 0x470, 0x450, 0x3, 0x2, 0x2, 0x2, 0x470, 
    0x45b, 0x3, 0x2, 0x2, 0x2, 0x470, 0x45d, 0x3, 0x2, 0x2, 0x2, 0x470, 
    0x45f, 0x3, 0x2, 0x2, 0x2, 0x470, 0x460, 0x3, 0x2, 0x2, 0x2, 0x470, 
    0x469, 0x3, 0x2, 0x2, 0x2, 0x471, 0x4c2, 0x3, 0x2, 0x2, 0x2, 0x472, 
    0x473, 0xc, 0x13, 0x2, 0x2, 0x473, 0x474, 0x9, 0x7, 0x2, 0x2, 0x474, 
    0x4c1, 0x5, 0xa8, 0x55, 0x14, 0x475, 0x476, 0xc, 0x12, 0x2, 0x2, 0x476, 
    0x477, 0x9, 0x8, 0x2, 0x2, 0x477, 0x4c1, 0x5, 0xa8, 0x55, 0x13, 0x478, 
    0x480, 0xc, 0x11, 0x2, 0x2, 0x479, 0x47a, 0x7, 0x4a, 0x2, 0x2, 0x47a, 
    0x481, 0x7, 0x4a, 0x2, 0x2, 0x47b, 0x47c, 0x7, 0x49, 0x2, 0x2, 0x47c, 
    0x47d, 0x7, 0x49, 0x2, 0x2, 0x47d, 0x481, 0x7, 0x49, 0x2, 0x2, 0x47e, 
    0x47f, 0x7, 0x49, 0x2, 0x2, 0x47f, 0x481, 0x7, 0x49, 0x2, 0x2, 0x480, 
    0x479, 0x3, 0x2, 0x2, 0x2, 0x480, 0x47b, 0x3, 0x2, 0x2, 0x2, 0x480, 
    0x47e, 0x3, 0x2, 0x2, 0x2, 0x481, 0x482, 0x3, 0x2, 0x2, 0x2, 0x482, 
    0x4c1, 0x5, 0xa8, 0x55, 0x12, 0x483, 0x484, 0xc, 0x10, 0x2, 0x2, 0x484, 
    0x485, 0x9, 0x9, 0x2, 0x2, 0x485, 0x4c1, 0x5, 0xa8, 0x55, 0x11, 0x486, 
    0x487, 0xc, 0xe, 0x2, 0x2, 0x487, 0x488, 0x9, 0xa, 0x2, 0x2, 0x488, 
    0x4c1, 0x5, 0xa8, 0x55, 0xf, 0x489, 0x48a, 0xc, 0xd, 0x2, 0x2, 0x48a, 
    0x48b, 0x7, 0x5b, 0x2, 0x2, 0x48b, 0x4c1, 0x5, 0xa8, 0x55, 0xe, 0x48c, 
    0x48d, 0xc, 0xc, 0x2, 0x2, 0x48d, 0x48e, 0x7, 0x5d, 0x2, 0x2, 0x48e, 
    0x4c1, 0x5, 0xa8, 0x55, 0xd, 0x48f, 0x490, 0xc, 0xb, 0x2, 0x2, 0x490, 
    0x491, 0x7, 0x5c, 0x2, 0x2, 0x491, 0x4c1, 0x5, 0xa8, 0x55, 0xc, 0x492, 
    0x493, 0xc, 0xa, 0x2, 0x2, 0x493, 0x494, 0x7, 0x53, 0x2, 0x2, 0x494, 
    0x4c1, 0x5, 0xa8, 0x55, 0xb, 0x495, 0x496, 0xc, 0x9, 0x2, 0x2, 0x496, 
    0x497, 0x7, 0x54, 0x2, 0x2, 0x497, 0x4c1, 0x5, 0xa8, 0x55, 0xa, 0x498, 
    0x499, 0xc, 0x8, 0x2, 0x2, 0x499, 0x49a, 0x7, 0x4d, 0x2, 0x2, 0x49a, 
    0x49b, 0x5, 0xa8, 0x55, 0x2, 0x49b, 0x49c, 0x7, 0x4e, 0x2, 0x2, 0x49c, 
    0x49d, 0x5, 0xa8, 0x55, 0x8, 0x49d, 0x4c1, 0x3, 0x2, 0x2, 0x2, 0x49e, 
    0x49f, 0xc, 0x7, 0x2, 0x2, 0x49f, 0x4a0, 0x9, 0xb, 0x2, 0x2, 0x4a0, 
    0x4c1, 0x5, 0xa8, 0x55, 0x7, 0x4a1, 0x4a2, 0xc, 0x1b, 0x2, 0x2, 0x4a2, 
    0x4ae, 0x7, 0x47, 0x2, 0x2, 0x4a3, 0x4af, 0x7, 0x71, 0x2, 0x2, 0x4a4, 
    0x4af, 0x5, 0xa6, 0x54, 0x2, 0x4a5, 0x4af, 0x7, 0x2d, 0x2, 0x2, 0x4a6, 
    0x4a8, 0x7, 0x21, 0x2, 0x2, 0x4a7, 0x4a9, 0x5, 0xc4, 0x63, 0x2, 0x4a8, 
    0x4a7, 0x3, 0x2, 0x2, 0x2, 0x4a8, 0x4a9, 0x3, 0x2, 0x2, 0x2, 0x4a9, 
    0x4aa, 0x3, 0x2, 0x2, 0x2, 0x4aa, 0x4af, 0x5, 0xb8, 0x5d, 0x2, 0x4ab, 
    0x4ac, 0x7, 0x2a, 0x2, 0x2, 0x4ac, 0x4af, 0x5, 0xce, 0x68, 0x2, 0x4ad, 
    0x4af, 0x5, 0xbe, 0x60, 0x2, 0x4ae, 0x4a3, 0x3, 0x2, 0x2, 0x2, 0x4ae, 
    0x4a4, 0x3, 0x2, 0x2, 0x2, 0x4ae, 0x4a5, 0x3, 0x2, 0x2, 0x2, 0x4ae, 
    0x4a6, 0x3, 0x2, 0x2, 0x2, 0x4ae, 0x4ab, 0x3, 0x2, 0x2, 0x2, 0x4ae, 
    0x4ad, 0x3, 0x2, 0x2, 0x2, 0x4af, 0x4c1, 0x3, 0x2, 0x2, 0x2, 0x4b0, 
    0x4b1, 0xc, 0x1a, 0x2, 0x2, 0x4b1, 0x4b2, 0x7, 0x43, 0x2, 0x2, 0x4b2, 
    0x4b3, 0x5, 0xa8, 0x55, 0x2, 0x4b3, 0x4b4, 0x7, 0x44, 0x2, 0x2, 0x4b4, 
    0x4c1, 0x3, 0x2, 0x2, 0x2, 0x4b5, 0x4b6, 0xc, 0x16, 0x2, 0x2, 0x4b6, 
    0x4c1, 0x9, 0xc, 0x2, 0x2, 0x4b7, 0x4b8, 0xc, 0xf, 0x2, 0x2, 0x4b8, 
    0x4b9, 0x7, 0x1c, 0x2, 0x2, 0x4b9, 0x4c1, 0x5, 0xc8, 0x65, 0x2, 0x4ba, 
    0x4bb, 0xc, 0x5, 0x2, 0x2, 0x4bb, 0x4bd, 0x7, 0x6b, 0x2, 0x2, 0x4bc, 
    0x4be, 0x5, 0xcc, 0x67, 0x2, 0x4bd, 0x4bc, 0x3, 0x2, 0x2, 0x2, 0x4bd, 
    0x4be, 0x3, 0x2, 0x2, 0x2, 0x4be, 0x4bf, 0x3, 0x2, 0x2, 0x2, 0x4bf, 
    0x4c1, 0x7, 0x71, 0x2, 0x2, 0x4c0, 0x472, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
    0x475, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x478, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
    0x483, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x486, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
    0x489, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x48c, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
    0x48f, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x492, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
    0x495, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x498, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
    0x49e, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x4a1, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
    0x4b0, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x4b5, 0x3, 0x2, 0x2, 0x2, 0x4c0, 
    0x4b7, 0x3, 0x2, 0x2, 0x2, 0x4c0, 0x4ba, 0x3, 0x2, 0x2, 0x2, 0x4c1, 
    0x4c4, 0x3, 0x2, 0x2, 0x2, 0x4c2, 0x4c0, 0x3, 0x2, 0x2, 0x2, 0x4c2, 
    0x4c3, 0x3, 0x2, 0x2, 0x2, 0x4c3, 0xa9, 0x3, 0x2, 0x2, 0x2, 0x4c4, 0x4c2, 
    0x3, 0x2, 0x2, 0x2, 0x4c5, 0x4c6, 0x5, 0xac, 0x57, 0x2, 0x4c6, 0x4c7, 
    0x7, 0x6a, 0x2, 0x2, 0x4c7, 0x4c8, 0x5, 0xae, 0x58, 0x2, 0x4c8, 0xab, 
    0x3, 0x2, 0x2, 0x2, 0x4c9, 0x4da, 0x7, 0x71, 0x2, 0x2, 0x4ca, 0x4cc, 
    0x7, 0x3f, 0x2, 0x2, 0x4cb, 0x4cd, 0x5, 0x58, 0x2d, 0x2, 0x4cc, 0x4cb, 
    0x3, 0x2, 0x2, 0x2, 0x4cc, 0x4cd, 0x3, 0x2, 0x2, 0x2, 0x4cd, 0x4ce, 
    0x3, 0x2, 0x2, 0x2, 0x4ce, 0x4da, 0x7, 0x40, 0x2, 0x2, 0x4cf, 0x4d0, 
    0x7, 0x3f, 0x2, 0x2, 0x4d0, 0x4d5, 0x7, 0x71, 0x2, 0x2, 0x4d1, 0x4d2, 
    0x7, 0x46, 0x2, 0x2, 0x4d2, 0x4d4, 0x7, 0x71, 0x2, 0x2, 0x4d3, 0x4d1, 
    0x3, 0x2, 0x2, 0x2, 0x4d4, 0x4d7, 0x3, 0x2, 0x2, 0x2, 0x4d5, 0x4d3, 
    0x3, 0x2, 0x2, 0x2, 0x4d5, 0x4d6, 0x3, 0x2, 0x2, 0x2, 0x4d6, 0x4d8, 
    0x3, 0x2, 0x2, 0x2, 0x4d7, 0x4d5, 0x3, 0x2, 0x2, 0x2, 0x4d8, 0x4da, 
    0x7, 0x40, 0x2, 0x2, 0x4d9, 0x4c9, 0x3, 0x2, 0x2, 0x2, 0x4d9, 0x4ca, 
    0x3, 0x2, 0x2, 0x2, 0x4d9, 0x4cf, 0x3, 0x2, 0x2, 0x2, 0x4da, 0xad, 0x3, 
    0x2, 0x2, 0x2, 0x4db, 0x4de, 0x5, 0xa8, 0x55, 0x2, 0x4dc, 0x4de, 0x5, 
    0x82, 0x42, 0x2, 0x4dd, 0x4db, 0x3, 0x2, 0x2, 0x2, 0x4dd, 0x4dc, 0x3, 
    0x2, 0x2, 0x2, 0x4de, 0xaf, 0x3, 0x2, 0x2, 0x2, 0x4df, 0x4e0, 0x7, 0x3f, 
    0x2, 0x2, 0x4e0, 0x4e1, 0x5, 0xa8, 0x55, 0x2, 0x4e1, 0x4e2, 0x7, 0x40, 
    0x2, 0x2, 0x4e2, 0x4f2, 0x3, 0x2, 0x2, 0x2, 0x4e3, 0x4f2, 0x7, 0x2d, 
    0x2, 0x2, 0x4e4, 0x4f2, 0x7, 0x2a, 0x2, 0x2, 0x4e5, 0x4f2, 0x5, 0x60, 
    0x31, 0x2, 0x4e6, 0x4f2, 0x7, 0x71, 0x2, 0x2, 0x4e7, 0x4e8, 0x5, 0x2e, 
    0x18, 0x2, 0x4e8, 0x4e9, 0x7, 0x47, 0x2, 0x2, 0x4e9, 0x4ea, 0x7, 0xb, 
    0x2, 0x2, 0x4ea, 0x4f2, 0x3, 0x2, 0x2, 0x2, 0x4eb, 0x4ef, 0x5, 0xc4, 
    0x63, 0x2, 0x4ec, 0x4f0, 0x5, 0xd0, 0x69, 0x2, 0x4ed, 0x4ee, 0x7, 0x2d, 
    0x2, 0x2, 0x4ee, 0x4f0, 0x5, 0xd2, 0x6a, 0x2, 0x4ef, 0x4ec, 0x3, 0x2, 
    0x2, 0x2, 0x4ef, 0x4ed, 0x3, 0x2, 0x2, 0x2, 0x4f0, 0x4f2, 0x3, 0x2, 
    0x2, 0x2, 0x4f1, 0x4df, 0x3, 0x2, 0x2, 0x2, 0x4f1, 0x4e3, 0x3, 0x2, 
    0x2, 0x2, 0x4f1, 0x4e4, 0x3, 0x2, 0x2, 0x2, 0x4f1, 0x4e5, 0x3, 0x2, 
    0x2, 0x2, 0x4f1, 0x4e6, 0x3, 0x2, 0x2, 0x2, 0x4f1, 0x4e7, 0x3, 0x2, 
    0x2, 0x2, 0x4f1, 0x4eb, 0x3, 0x2, 0x2, 0x2, 0x4f2, 0xb1, 0x3, 0x2, 0x2, 
    0x2, 0x4f3, 0x4f4, 0x5, 0x50, 0x29, 0x2, 0x4f4, 0x4f5, 0x7, 0x47, 0x2, 
    0x2, 0x4f5, 0x4f7, 0x3, 0x2, 0x2, 0x2, 0x4f6, 0x4f3, 0x3, 0x2, 0x2, 
    0x2, 0x4f6, 0x4f7, 0x3, 0x2, 0x2, 0x2, 0x4f7, 0x4fb, 0x3, 0x2, 0x2, 
    0x2, 0x4f8, 0x4fa, 0x5, 0x68, 0x35, 0x2, 0x4f9, 0x4f8, 0x3, 0x2, 0x2, 
    0x2, 0x4fa, 0x4fd, 0x3, 0x2, 0x2, 0x2, 0x4fb, 0x4f9, 0x3, 0x2, 0x2, 
    0x2, 0x4fb, 0x4fc, 0x3, 0x2, 0x2, 0x2, 0x4fc, 0x4fe, 0x3, 0x2, 0x2, 
    0x2, 0x4fd, 0x4fb, 0x3, 0x2, 0x2, 0x2, 0x4fe, 0x500, 0x7, 0x71, 0x2, 
    0x2, 0x4ff, 0x501, 0x5, 0xcc, 0x67, 0x2, 0x500, 0x4ff, 0x3, 0x2, 0x2, 
    0x2, 0x500, 0x501, 0x3, 0x2, 0x2, 0x2, 0x501, 0xb3, 0x3, 0x2, 0x2, 0x2, 
    0x502, 0x503, 0x5, 0xc4, 0x63, 0x2, 0x503, 0x504, 0x5, 0xb6, 0x5c, 0x2, 
    0x504, 0x505, 0x5, 0xbc, 0x5f, 0x2, 0x505, 0x50c, 0x3, 0x2, 0x2, 0x2, 
    0x506, 0x509, 0x5, 0xb6, 0x5c, 0x2, 0x507, 0x50a, 0x5, 0xba, 0x5e, 0x2, 
    0x508, 0x50a, 0x5, 0xbc, 0x5f, 0x2, 0x509, 0x507, 0x3, 0x2, 0x2, 0x2, 
    0x509, 0x508, 0x3, 0x2, 0x2, 0x2, 0x50a, 0x50c, 0x3, 0x2, 0x2, 0x2, 
    0x50b, 0x502, 0x3, 0x2, 0x2, 0x2, 0x50b, 0x506, 0x3, 0x2, 0x2, 0x2, 
    0x50c, 0xb5, 0x3, 0x2, 0x2, 0x2, 0x50d, 0x50f, 0x7, 0x71, 0x2, 0x2, 
    0x50e, 0x510, 0x5, 0xc0, 0x61, 0x2, 0x50f, 0x50e, 0x3, 0x2, 0x2, 0x2, 
    0x50f, 0x510, 0x3, 0x2, 0x2, 0x2, 0x510, 0x518, 0x3, 0x2, 0x2, 0x2, 
    0x511, 0x512, 0x7, 0x47, 0x2, 0x2, 0x512, 0x514, 0x7, 0x71, 0x2, 0x2, 
    0x513, 0x515, 0x5, 0xc0, 0x61, 0x2, 0x514, 0x513, 0x3, 0x2, 0x2, 0x2, 
    0x514, 0x515, 0x3, 0x2, 0x2, 0x2, 0x515, 0x517, 0x3, 0x2, 0x2, 0x2, 
    0x516, 0x511, 0x3, 0x2, 0x2, 0x2, 0x517, 0x51a, 0x3, 0x2, 0x2, 0x2, 
    0x518, 0x516, 0x3, 0x2, 0x2, 0x2, 0x518, 0x519, 0x3, 0x2, 0x2, 0x2, 
    0x519, 0x51d, 0x3, 0x2, 0x2, 0x2, 0x51a, 0x518, 0x3, 0x2, 0x2, 0x2, 
    0x51b, 0x51d, 0x5, 0xca, 0x66, 0x2, 0x51c, 0x50d, 0x3, 0x2, 0x2, 0x2, 
    0x51c, 0x51b, 0x3, 0x2, 0x2, 0x2, 0x51d, 0xb7, 0x3, 0x2, 0x2, 0x2, 0x51e, 
    0x520, 0x7, 0x71, 0x2, 0x2, 0x51f, 0x521, 0x5, 0xc2, 0x62, 0x2, 0x520, 
    0x51f, 0x3, 0x2, 0x2, 0x2, 0x520, 0x521, 0x3, 0x2, 0x2, 0x2, 0x521, 
    0x522, 0x3, 0x2, 0x2, 0x2, 0x522, 0x523, 0x5, 0xbc, 0x5f, 0x2, 0x523, 
    0xb9, 0x3, 0x2, 0x2, 0x2, 0x524, 0x540, 0x7, 0x43, 0x2, 0x2, 0x525, 
    0x52a, 0x7, 0x44, 0x2, 0x2, 0x526, 0x527, 0x7, 0x43, 0x2, 0x2, 0x527, 
    0x529, 0x7, 0x44, 0x2, 0x2, 0x528, 0x526, 0x3, 0x2, 0x2, 0x2, 0x529, 
    0x52c, 0x3, 0x2, 0x2, 0x2, 0x52a, 0x528, 0x3, 0x2, 0x2, 0x2, 0x52a, 
    0x52b, 0x3, 0x2, 0x2, 0x2, 0x52b, 0x52d, 0x3, 0x2, 0x2, 0x2, 0x52c, 
    0x52a, 0x3, 0x2, 0x2, 0x2, 0x52d, 0x541, 0x5, 0x4e, 0x28, 0x2, 0x52e, 
    0x52f, 0x5, 0xa8, 0x55, 0x2, 0x52f, 0x536, 0x7, 0x44, 0x2, 0x2, 0x530, 
    0x531, 0x7, 0x43, 0x2, 0x2, 0x531, 0x532, 0x5, 0xa8, 0x55, 0x2, 0x532, 
    0x533, 0x7, 0x44, 0x2, 0x2, 0x533, 0x535, 0x3, 0x2, 0x2, 0x2, 0x534, 
    0x530, 0x3, 0x2, 0x2, 0x2, 0x535, 0x538, 0x3, 0x2, 0x2, 0x2, 0x536, 
    0x534, 0x3, 0x2, 0x2, 0x2, 0x536, 0x537, 0x3, 0x2, 0x2, 0x2, 0x537, 
    0x53d, 0x3, 0x2, 0x2, 0x2, 0x538, 0x536, 0x3, 0x2, 0x2, 0x2, 0x539, 
    0x53a, 0x7, 0x43, 0x2, 0x2, 0x53a, 0x53c, 0x7, 0x44, 0x2, 0x2, 0x53b, 
    0x539, 0x3, 0x2, 0x2, 0x2, 0x53c, 0x53f, 0x3, 0x2, 0x2, 0x2, 0x53d, 
    0x53b, 0x3, 0x2, 0x2, 0x2, 0x53d, 0x53e, 0x3, 0x2, 0x2, 0x2, 0x53e, 
    0x541, 0x3, 0x2, 0x2, 0x2, 0x53f, 0x53d, 0x3, 0x2, 0x2, 0x2, 0x540, 
    0x525, 0x3, 0x2, 0x2, 0x2, 0x540, 0x52e, 0x3, 0x2, 0x2, 0x2, 0x541, 
    0xbb, 0x3, 0x2, 0x2, 0x2, 0x542, 0x544, 0x5, 0xd2, 0x6a, 0x2, 0x543, 
    0x545, 0x5, 0x22, 0x12, 0x2, 0x544, 0x543, 0x3, 0x2, 0x2, 0x2, 0x544, 
    0x545, 0x3, 0x2, 0x2, 0x2, 0x545, 0xbd, 0x3, 0x2, 0x2, 0x2, 0x546, 0x547, 
    0x5, 0xc4, 0x63, 0x2, 0x547, 0x548, 0x5, 0xd0, 0x69, 0x2, 0x548, 0xbf, 
    0x3, 0x2, 0x2, 0x2, 0x549, 0x54a, 0x7, 0x4a, 0x2, 0x2, 0x54a, 0x54d, 
    0x7, 0x49, 0x2, 0x2, 0x54b, 0x54d, 0x5, 0xcc, 0x67, 0x2, 0x54c, 0x549, 
    0x3, 0x2, 0x2, 0x2, 0x54c, 0x54b, 0x3, 0x2, 0x2, 0x2, 0x54d, 0xc1, 0x3, 
    0x2, 0x2, 0x2, 0x54e, 0x54f, 0x7, 0x4a, 0x2, 0x2, 0x54f, 0x552, 0x7, 
    0x49, 0x2, 0x2, 0x550, 0x552, 0x5, 0xc4, 0x63, 0x2, 0x551, 0x54e, 0x3, 
    0x2, 0x2, 0x2, 0x551, 0x550, 0x3, 0x2, 0x2, 0x2, 0x552, 0xc3, 0x3, 0x2, 
    0x2, 0x2, 0x553, 0x554, 0x7, 0x4a, 0x2, 0x2, 0x554, 0x555, 0x5, 0xc6, 
    0x64, 0x2, 0x555, 0x556, 0x7, 0x49, 0x2, 0x2, 0x556, 0xc5, 0x3, 0x2, 
    0x2, 0x2, 0x557, 0x55c, 0x5, 0xc8, 0x65, 0x2, 0x558, 0x559, 0x7, 0x46, 
    0x2, 0x2, 0x559, 0x55b, 0x5, 0xc8, 0x65, 0x2, 0x55a, 0x558, 0x3, 0x2, 
    0x2, 0x2, 0x55b, 0x55e, 0x3, 0x2, 0x2, 0x2, 0x55c, 0x55a, 0x3, 0x2, 
    0x2, 0x2, 0x55c, 0x55d, 0x3, 0x2, 0x2, 0x2, 0x55d, 0xc7, 0x3, 0x2, 0x2, 
    0x2, 0x55e, 0x55c, 0x3, 0x2, 0x2, 0x2, 0x55f, 0x561, 0x5, 0x68, 0x35, 
    0x2, 0x560, 0x55f, 0x3, 0x2, 0x2, 0x2, 0x561, 0x564, 0x3, 0x2, 0x2, 
    0x2, 0x562, 0x560, 0x3, 0x2, 0x2, 0x2, 0x562, 0x563, 0x3, 0x2, 0x2, 
    0x2, 0x563, 0x567, 0x3, 0x2, 0x2, 0x2, 0x564, 0x562, 0x3, 0x2, 0x2, 
    0x2, 0x565, 0x568, 0x5, 0x50, 0x29, 0x2, 0x566, 0x568, 0x5, 0xca, 0x66, 
    0x2, 0x567, 0x565, 0x3, 0x2, 0x2, 0x2, 0x567, 0x566, 0x3, 0x2, 0x2, 
    0x2, 0x568, 0x573, 0x3, 0x2, 0x2, 0x2, 0x569, 0x56b, 0x5, 0x68, 0x35, 
    0x2, 0x56a, 0x569, 0x3, 0x2, 0x2, 0x2, 0x56b, 0x56e, 0x3, 0x2, 0x2, 
    0x2, 0x56c, 0x56a, 0x3, 0x2, 0x2, 0x2, 0x56c, 0x56d, 0x3, 0x2, 0x2, 
    0x2, 0x56d, 0x56f, 0x3, 0x2, 0x2, 0x2, 0x56e, 0x56c, 0x3, 0x2, 0x2, 
    0x2, 0x56f, 0x570, 0x7, 0x43, 0x2, 0x2, 0x570, 0x572, 0x7, 0x44, 0x2, 
    0x2, 0x571, 0x56c, 0x3, 0x2, 0x2, 0x2, 0x572, 0x575, 0x3, 0x2, 0x2, 
    0x2, 0x573, 0x571, 0x3, 0x2, 0x2, 0x2, 0x573, 0x574, 0x3, 0x2, 0x2, 
    0x2, 0x574, 0xc9, 0x3, 0x2, 0x2, 0x2, 0x575, 0x573, 0x3, 0x2, 0x2, 0x2, 
    0x576, 0x577, 0x9, 0xd, 0x2, 0x2, 0x577, 0xcb, 0x3, 0x2, 0x2, 0x2, 0x578, 
    0x579, 0x7, 0x4a, 0x2, 0x2, 0x579, 0x57e, 0x5, 0x52, 0x2a, 0x2, 0x57a, 
    0x57b, 0x7, 0x46, 0x2, 0x2, 0x57b, 0x57d, 0x5, 0x52, 0x2a, 0x2, 0x57c, 
    0x57a, 0x3, 0x2, 0x2, 0x2, 0x57d, 0x580, 0x3, 0x2, 0x2, 0x2, 0x57e, 
    0x57c, 0x3, 0x2, 0x2, 0x2, 0x57e, 0x57f, 0x3, 0x2, 0x2, 0x2, 0x57f, 
    0x581, 0x3, 0x2, 0x2, 0x2, 0x580, 0x57e, 0x3, 0x2, 0x2, 0x2, 0x581, 
    0x582, 0x7, 0x49, 0x2, 0x2, 0x582, 0xcd, 0x3, 0x2, 0x2, 0x2, 0x583, 
    0x58a, 0x5, 0xd2, 0x6a, 0x2, 0x584, 0x585, 0x7, 0x47, 0x2, 0x2, 0x585, 
    0x587, 0x7, 0x71, 0x2, 0x2, 0x586, 0x588, 0x5, 0xd2, 0x6a, 0x2, 0x587, 
    0x586, 0x3, 0x2, 0x2, 0x2, 0x587, 0x588, 0x3, 0x2, 0x2, 0x2, 0x588, 
    0x58a, 0x3, 0x2, 0x2, 0x2, 0x589, 0x583, 0x3, 0x2, 0x2, 0x2, 0x589, 
    0x584, 0x3, 0x2, 0x2, 0x2, 0x58a, 0xcf, 0x3, 0x2, 0x2, 0x2, 0x58b, 0x58c, 
    0x7, 0x2a, 0x2, 0x2, 0x58c, 0x590, 0x5, 0xce, 0x68, 0x2, 0x58d, 0x58e, 
    0x7, 0x71, 0x2, 0x2, 0x58e, 0x590, 0x5, 0xd2, 0x6a, 0x2, 0x58f, 0x58b, 
    0x3, 0x2, 0x2, 0x2, 0x58f, 0x58d, 0x3, 0x2, 0x2, 0x2, 0x590, 0xd1, 0x3, 
    0x2, 0x2, 0x2, 0x591, 0x593, 0x7, 0x3f, 0x2, 0x2, 0x592, 0x594, 0x5, 
    0xa4, 0x53, 0x2, 0x593, 0x592, 0x3, 0x2, 0x2, 0x2, 0x593, 0x594, 0x3, 
    0x2, 0x2, 0x2, 0x594, 0x595, 0x3, 0x2, 0x2, 0x2, 0x595, 0x596, 0x7, 
    0x40, 0x2, 0x2, 0x596, 0xd3, 0x3, 0x2, 0x2, 0x2, 0xb4, 0xd5, 0xda, 0xe0, 
    0xe8, 0xf1, 0xf6, 0xfd, 0x104, 0x107, 0x10e, 0x118, 0x11c, 0x121, 0x125, 
    0x129, 0x133, 0x13b, 0x143, 0x147, 0x14e, 0x155, 0x159, 0x15c, 0x15f, 
    0x168, 0x16e, 0x173, 0x176, 0x17c, 0x182, 0x186, 0x18e, 0x197, 0x19e, 
    0x1a4, 0x1a8, 0x1b3, 0x1bc, 0x1c1, 0x1c7, 0x1cb, 0x1d7, 0x1e2, 0x1e7, 
    0x1f0, 0x1f8, 0x202, 0x20b, 0x213, 0x218, 0x220, 0x225, 0x22f, 0x239, 
    0x23f, 0x246, 0x24b, 0x253, 0x257, 0x259, 0x25f, 0x264, 0x268, 0x26f, 
    0x275, 0x277, 0x27e, 0x283, 0x28c, 0x291, 0x294, 0x299, 0x2a2, 0x2a9, 
    0x2b4, 0x2bd, 0x2c7, 0x2d0, 0x2d5, 0x2d8, 0x2df, 0x2e9, 0x2f1, 0x2f4, 
    0x2f7, 0x304, 0x30c, 0x311, 0x319, 0x31d, 0x321, 0x325, 0x327, 0x32b, 
    0x331, 0x33c, 0x346, 0x34b, 0x354, 0x359, 0x35c, 0x363, 0x36c, 0x383, 
    0x386, 0x389, 0x391, 0x395, 0x39d, 0x3a3, 0x3ae, 0x3b7, 0x3bc, 0x3c6, 
    0x3cd, 0x3da, 0x3e3, 0x3ec, 0x3f2, 0x3fd, 0x402, 0x407, 0x40c, 0x410, 
    0x414, 0x418, 0x41a, 0x41e, 0x423, 0x434, 0x43a, 0x440, 0x446, 0x449, 
    0x454, 0x463, 0x467, 0x46c, 0x470, 0x480, 0x4a8, 0x4ae, 0x4bd, 0x4c0, 
    0x4c2, 0x4cc, 0x4d5, 0x4d9, 0x4dd, 0x4ef, 0x4f1, 0x4f6, 0x4fb, 0x500, 
    0x509, 0x50b, 0x50f, 0x514, 0x518, 0x51c, 0x520, 0x52a, 0x536, 0x53d, 
    0x540, 0x544, 0x54c, 0x551, 0x55c, 0x562, 0x567, 0x56c, 0x573, 0x57e, 
    0x587, 0x589, 0x58f, 0x593, 
  };

  atn::ATNDeserializer deserializer;
  _atn = deserializer.deserialize(_serializedATN);

  size_t count = _atn.getNumberOfDecisions();
  _decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    _decisionToDFA.emplace_back(_atn.getDecisionState(i), i);
  }
}

JavaParserLabeled::Initializer JavaParserLabeled::_init;
