from antlr4.TokenStreamRewriter import TokenStreamRewriter
from utils_listener import TokensInfo,SingleFileElement
from utils import Rewriter
from utils import get_program


def move_method_refactoring(source_filenames: list, package_name: str, class_name: str, method_name: str,target_class_name : str, filename_mapping = lambda x: x + ".rewritten.java"):
    program = get_program(source_filenames)
    _sourceclass = program.packages[package_name].classes[class_name]
    _targetclass = program.packages[package_name].classes[target_class_name]
    _method =program.packages[package_name].classes[class_name].methods[method_name]
    Rewriter_= Rewriter(program,filename_mapping)
    tokens_info = TokensInfo(_method.parser_context)
    param_tokens_info = TokensInfo(_method.formalparam_context)
    exp=[]
    exps= tokens_info.get_token_index(tokens_info.token_stream.tokens,tokens_info.start,tokens_info.stop)

    for token in exps:
            if token.text in _sourceclass.fields:
                exp.append(token.tokenIndex)
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
    class_tokens_info = TokensInfo(_targetclass.parser_context)
    singlefileelement = SingleFileElement(_method.parser_context,_method.filename)
    #strofmethod  =_method.get_text_from_file(_method.filename)

    token_stream_rewriter = TokenStreamRewriter(singlefileelement.get_token_stream())
    for index in exp:
        token_stream_rewriter.insertBeforeIndex(index=index,text=class_name +".")
    for inv in _method.body_method_invocations:
        if (inv.getText() == target_class_name):
            inv_tokens_info_target = TokensInfo(inv)
            token_stream_rewriter.replaceRange(from_idx=inv_tokens_info_target.start,to_idx=inv_tokens_info_target.stop+1,text=" ")

    strch = token_stream_rewriter.insertBeforeIndex(param_tokens_info.start,text= class_name + " " +str.lower(class_name)  +"," )
    strofmethod =token_stream_rewriter.getText(program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                           start=tokens_info.start,
                                                           stop=tokens_info.stop)
  #  print(token_stream_rewriter.getText(program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                         #  start=tokens_info.start,
                                                        #   stop=tokens_info.stop))


    Rewriter_.insert_before(tokens_info=class_tokens_info,text=strofmethod)
    Rewriter_.replace(tokens_info,"")

    Rewriter_.apply()

mylist = ["tests/move_method/s.java","tests/move_method/t.java","tests/move_method/test.java"]

move_method_refactoring(mylist,"tests.utils_test2","SAA","c","t")

