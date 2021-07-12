"""
## Introduction

When subclasses grow and get developed separately, your code may have constructors that perform similar work.
Pull up constructor refactoring removes the repetitive method from subclasses and moves it to a superclass.


## Pre and Post Conditions

### Pre Conditions:
1. The source package, class and constructor should exist.
2. The order of the params in the constructor should be equal in the child classes.
3. empty package name is addressable using "".

### Post Conditions:

No specific Post Condition

"""

from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement
from refactorings.pullup_constructor_get_cons import get_cons
from refactorings.utils.utils2 import Rewriter, get_program, get_filenames_in_dir


class PullUpConstructorRefactoring:
    def __init__(self, source_filenames: list, package_name: str, class_name: str,
                 filename_mapping=lambda x: x):
        """
        The main function that does the process of pull up constructor refactoring.
               Removes the necessary constructor from the subclasses and moves them to a superclass.

               Args:
                      source_filenames (list): A list of file names to be processed

                      package_name (str): The name of the package in which the refactoring has to be done(contains the classes)

                      class_name (str): Name of the class in which the refactoring has to be done (pulling up the field from here)

                      filename_mapping (str): Mapping the file's name to the correct format so that it can be processed

               Returns:
                   No returns
        """
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_name = class_name
        self.filename_mapping = filename_mapping

    def do_refactor(self):
        program = get_program(self.source_filenames)  # getting the program packages
        package = self.package_name
        _sourceclass = program.packages[package].classes[self.class_name]
        target_class_name = _sourceclass.superclass_name
        removemethod, removemethod1 = get_cons(program, package, target_class_name,
                                               self.class_name)  # Similar cons in other classes
        _targetclass = program.packages[package].classes[target_class_name]
        mets = program.packages[package].classes[self.class_name].methods
        _method_name = []
        for methodName, method in mets.items():
            if method.is_constructor:
                _method_name = method
                break
        tokens_info = TokensInfo(_method_name.parser_context)

        if not _method_name.is_constructor:
            return False
        param_dict = {}
        len_params = {}

        Rewriter_ = Rewriter(program, self.filename_mapping)
        for remove in removemethod:
            flag2 = False
            _methodd = removemethod[remove]
            len_params[remove] = len(_methodd[0].split(","))
            not_present = removemethod1
            if _methodd is not None:
                _methodds = _methodd[0]
                _method = program.packages[package].classes[remove].methods[str(_methodds)]
                params = ""
                params2 = ""
                for param in _method.parameters:
                    flag = False
                    for x in not_present:
                        for y in x:
                            if param[1] in y:
                                flag = True
                                flag2 = True
                    if not flag:
                        params += param[1] + ","
                    params2 += param[0] + " " + param[1] + ","
                    flag = False
                param_dict[remove] = params2[:-1]
                _method_token_info = TokensInfo(_method.parser_context)
                if flag2:
                    str1 = ""
                    for x in not_present:
                        for y in x:
                            str1 += y + ";" + "\n\t"
                    Rewriter_.replace(_method_token_info, "public " + remove + "(" + params2[:-1] + ")"
                                      + "{\n\t" + "super(" + params[:-1] + ");" + "\n\t " + str1 + "}")
                else:
                    Rewriter_.replace(_method_token_info, "public " + remove + "(" + params2[:-1] + ")"
                                      + "{\n\t" + "super(" + params[:-1] + ");" + "\n\t}")
        has_cons = False
        parent_cons = []
        for method in _targetclass.methods:
            meth = _targetclass.methods[method]
            if meth.is_constructor:
                parent_cons = meth
                has_cons = True
                break

        if has_cons:
            for class_body_decl in _targetclass.parser_context.classBody().getChildren():
                if class_body_decl.getText() in ['{', '}']:
                    continue
                member_decl = class_body_decl.memberDeclaration()
                if member_decl is not None:
                    constructor = member_decl.constructorDeclaration()
                    if constructor is not None:
                        body = constructor.constructorBody  # Start token = '{'
                        class_tokens_info = TokensInfo(body)
                        class_tokens_info.stop = class_tokens_info.start  # Start and stop both point to the '{'
                        key = min(len_params, key=len_params.get)
                        _method_name1 = program.packages[package].classes[key].methods[removemethod[key][0]]
                        tokens_info = TokensInfo(_method_name1.parser_context.memberDeclaration()
                                                 .constructorDeclaration()
                                                 .constructorBody)
                        singlefileelement = SingleFileElement(_method_name1.parser_context, _method_name1.filename)
                        token_stream_rewriter = TokenStreamRewriter(singlefileelement.get_token_stream())
                        strofmethod = token_stream_rewriter.getText(
                            program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                            start=tokens_info.start,
                            stop=tokens_info.stop)
                        strofmethod = strofmethod.replace(_method_name1.class_name, target_class_name)\
                            .replace("{", "").replace("}", "")
                        a1 = parent_cons.body_text.replace("{", "").replace("}", "")
                        a2 = _method_name1.body_text.replace("}", "").replace("{", "")
                        if a2 not in a1:
                            Rewriter_.insert_after(tokens_info=class_tokens_info, text=strofmethod)
                            Rewriter_.apply()
                            break
            Rewriter_.apply()

        else:
            class_tokens_info = TokensInfo(_targetclass.parser_context.classBody())
            class_tokens_info.stop = class_tokens_info.start
            key = min(len_params, key=len_params.get)
            _method_name1 = program.packages[package].classes[key].methods[removemethod[key][0]]
            tokens_info = TokensInfo(_method_name1.parser_context)
            singlefileelement = SingleFileElement(_method_name1.parser_context, _method_name1.filename)
            token_stream_rewriter = TokenStreamRewriter(singlefileelement.get_token_stream())
            strofmethod = token_stream_rewriter.getText(program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                        start=tokens_info.start,
                                                        stop=tokens_info.stop)
            strofmethod = strofmethod.replace(_method_name1.class_name, target_class_name)

            Rewriter_.insert_after(tokens_info=class_tokens_info, text=strofmethod)
            Rewriter_.apply()

        return True


if __name__ == "__main__":
    mylist = get_filenames_in_dir('/data/Dev/JavaSample/')
    if PullUpConstructorRefactoring(mylist, "", "Manager").do_refactor():
        print("Success!")
    else:
        print("Cannot refactor.")
