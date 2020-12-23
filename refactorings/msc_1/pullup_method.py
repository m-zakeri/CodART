from antlr4.TokenStreamRewriter import TokenStreamRewriter
from utils_listener import TokensInfo,SingleFileElement

from refactorings.msc_1.pullup_method1 import pullup_method
from utils import Rewriter
from utils import get_program


def pullup_method_refactoring(source_filenames: list, package_name: str, class_name: str, method_name: str, filename_mapping = lambda x: x + ".rewritten.java"):
    program = get_program(source_filenames)

    _sourceclass = program.packages[package_name].classes[class_name]
    target_class_name = _sourceclass.superclass_name
    removemethod = pullup_method(source_filenames, package_name,target_class_name, method_name, class_name)
    _targetclass = program.packages[package_name].classes[target_class_name]
    _method1 =program.packages[package_name].classes[class_name].methods[method_name]
    Rewriter_= Rewriter(program,filename_mapping)
    for remove in removemethod:
     _methodd=removemethod[remove]
     if _methodd == None:
        break
     _methodds = _methodd[0]
     _method =program.packages[package_name].classes[remove].methods[_methodds]
     tokens_info = TokensInfo(_method.parser_context)

     class_tokens_info = TokensInfo(_targetclass.parser_context)
     singlefileelement = SingleFileElement(_method.parser_context, _method.filename)
     # strofmethod  =_method.get_text_from_file(_method.filename)
     token_stream_rewriter = TokenStreamRewriter(singlefileelement.get_token_stream())
     strofmethod = token_stream_rewriter.getText(program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                start=tokens_info.start,
                                                stop=tokens_info.stop)
    #print(strofmethod)
     Rewriter_.insert_before(tokens_info=class_tokens_info,text=strofmethod)
     Rewriter_.replace(tokens_info,"")
     Rewriter_.apply()
    for package_name in program.packages:
        package = program.packages[package_name]
        for class_ in package.classes:
            _class = package.classes[class_]
            for method_ in _class.methods:
                __method = _class.methods[method_]
                for inv in __method.body_method_invocations:
                    invc = __method.body_method_invocations[inv]
                    if (invc[0] == method_name):
                        inv_tokens_info = TokensInfo(inv)
                        Rewriter_.replace(inv_tokens_info, target_class_name)
                        Rewriter_.apply()
    #print(_sourceclass)
    #print(_targetclass)
    #print(_method)
    #print(_method.parser_context.start)
    #print(_method.parser_context.stop)
mylist = ["tests/pullup_method/Test.java","tests/pullup_method/sourceclass.java","tests/pullup_method/superclass.java"]
pullup_method_refactoring(mylist,"tests.utils_test2","sourceclass","b")


