"""

"""

from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement
from refactorings.pullup_constructor_get_cons import get_cons
from refactorings.utils.utils2 import Rewriter, get_program, get_filenames_in_dir


class PullUpConstructorRefactoring:
    def __init__(self, source_filenames: list, package_name: str, class_name: str, method_key: str,
                 filename_mapping=lambda x: x):
        """
        """
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_name = class_name
        self.method_key = method_key
        self.filename_mapping = filename_mapping

    def do_refactor(self):
        program = get_program(self.source_filenames)  # getting the program packages
        _sourceclass = program.packages[self.package_name].classes[self.class_name]
        target_class_name = _sourceclass.superclass_name
        removemethod, removemethod1 = get_cons(program, self.package_name, target_class_name, self.method_key,
                                         self.class_name)  # Similar cons in other classes
        _targetclass = program.packages[self.package_name].classes[target_class_name]
        _method_name = program.packages[self.package_name].classes[self.class_name].methods[self.method_key]
        tokens_info = TokensInfo(_method_name.parser_context)

        if not _method_name.is_constructor:
            return False

        Rewriter_ = Rewriter(program, self.filename_mapping)
        for remove in removemethod:
            flag2 = False
            _methodd = removemethod[remove]
            not_present = removemethod1
            if _methodd is not None:
                _methodds = _methodd[0]
                _method = program.packages[self.package_name].classes[remove].methods[str(_methodds)]
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

        class_tokens_info = TokensInfo(_targetclass.parser_context.classBody())
        class_tokens_info.stop = class_tokens_info.start
        singlefileelement = SingleFileElement(_method_name.parser_context, _method_name.filename)
        token_stream_rewriter = TokenStreamRewriter(singlefileelement.get_token_stream())
        strofmethod = token_stream_rewriter.getText(program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                    start=tokens_info.start,
                                                    stop=tokens_info.stop)
        strofmethod = strofmethod.replace(_method_name.class_name, target_class_name)

        Rewriter_.insert_after(tokens_info=class_tokens_info, text=strofmethod)
        Rewriter_.apply()

        return True


if __name__ == "__main__":
    mylist = get_filenames_in_dir('../tests/pullup_constructor')
    print(mylist)
    if PullUpConstructorRefactoring(mylist, "tests.utils_test2", "sourceclass", "(String,String,int)").do_refactor():
        print("Success!")
    else:
        print("Cannot refactor.")
