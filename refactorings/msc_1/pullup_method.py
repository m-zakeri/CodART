from utils_listener import TokensInfo,SingleFileElement
from utils import Rewriter
from utils import get_program


def pullup_method_refactoring(source_filenames: list, package_name: str, class_name: str, method_name: str, filename_mapping = lambda x: x + ".rewritten.java"):
    program = get_program(source_filenames)
    _sourceclass = program.packages[package_name].classes[class_name]
    target_class_name = _sourceclass.superclass_name
    _targetclass = program.packages[package_name].classes[target_class_name]
    _method =program.packages[package_name].classes[class_name].methods[method_name]
    Rewriter_= Rewriter(program,filename_mapping)
    tokens_info = TokensInfo(_method.parser_context)
    for package_name in program.packages:
     package = program.packages[package_name]
     for class_ in package.classes:
        _class = package.classes[class_]
        for method_ in _class.methods:
            _method = _class.methods[method_]
            i=0
            for inv in _method.body_method_invocations:
                invc = _method.body_method_invocations[i]
                if(invc != None):
                    inv_tokens_info = TokensInfo(invc)
                    Rewriter_.replace(inv_tokens_info,target_class_name)
                    Rewriter_.apply()
                    i=i+1
    class_tokens_info = TokensInfo(_targetclass.parser_context)
    singlefileelement = SingleFileElement(_method.parser_context,_sourceclass.filename)
    strofmethod = singlefileelement.get_text_from_file()
    #print(strofmethod)
    Rewriter_.insert_before(tokens_info=class_tokens_info,text=strofmethod)
    Rewriter_.replace(tokens_info,"")
    Rewriter_.apply()
    #print(_sourceclass)
    #print(_targetclass)
    #print(_method)
    #print(_method.parser_context.start)
    #print(_method.parser_context.stop)
mylist = ["tests/pullup_method/Test.java","tests/pullup_method/sourceclass.java","tests/pullup_method/superclass.java"]
pullup_method_refactoring(mylist,"tests.utils_test2","sourceclass","d")


