from antlr4 import CommonTokenStream, ParserRuleContext

from codart.cfg_generator.src.antlr.gen.JavaLexer import JavaLexer


def extract_exact_text(token_stream: CommonTokenStream, rule: ParserRuleContext) -> str:
    return token_stream.getText(rule.start.tokenIndex, rule.stop.tokenIndex)


def is_break(rule: ParserRuleContext) -> bool:
    if not hasattr(rule, 'symbol'):
        return rule.start.type == JavaLexer.BREAK


def is_return(rule: ParserRuleContext) -> bool:
    if not hasattr(rule, 'symbol'):
        return rule.start.type == JavaLexer.RETURN


def is_continue(rule: ParserRuleContext) -> bool:
    if not hasattr(rule, 'symbol'):
        return rule.start.type == JavaLexer.CONTINUE


def is_throw(rule: ParserRuleContext) -> bool:
    if not hasattr(rule, 'symbol'):
        return rule.start.type == JavaLexer.THROW