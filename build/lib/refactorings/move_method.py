from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement


class MoveMethodRefactoring:
    def __init__(self, source_filenames: list, package_name: str, class_name: str, method_key: str,
                 target_class_name: str, target_package_name: str,
                 filename_mapping=lambda x: x + ".rewritten.java"):
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_name = class_name
        self.method_key = method_key
        self.target_class_name = target_class_name
        self.target_package_name = target_package_name
        self.filename_mapping = filename_mapping

    def do_refactor(self):
        program = get_program(self.source_filenames)
        static = 0

        if self.class_name not in program.packages[self.package_name].classes or self.target_class_name not in \
                program.packages[
                    self.target_package_name].classes or self.method_key not in \
                program.packages[self.package_name].classes[
                    self.class_name].methods:
            return False

        _sourceclass = program.packages[self.package_name].classes[self.class_name]
        _targetclass = program.packages[self.target_package_name].classes[self.target_class_name]
        _method = program.packages[self.package_name].classes[self.class_name].methods[self.method_key]

        if _method.is_constructor:
            return False

        Rewriter_ = Rewriter(program, lambda x: x)
        tokens_info = TokensInfo(_method.parser_context)  # tokens of ctx method
        param_tokens_info = TokensInfo(_method.formalparam_context)
        method_declaration_info = TokensInfo(_method.method_declaration_context)
        exp = []  # برای نگه داری متغیرهایی که داخل کلاس تعریف شدند و در بدنه متد استفاده شدند
        exps = tokens_info.get_token_index(tokens_info.token_stream.tokens, tokens_info.start, tokens_info.stop)

        # check that method is static or not
        for modifier in _method.modifiers:
            if modifier == "static":
                static = 1;

        for token in exps:
            if token.text in _sourceclass.fields:
                exp.append(token.tokenIndex)
            # check that where this method is call
        for package_names in program.packages:
            package = program.packages[package_names]
            for class_ in package.classes:
                _class = package.classes[class_]
                for method_ in _class.methods:
                    __method = _class.methods[method_]
                    for inv in __method.body_method_invocations:
                        invc = __method.body_method_invocations[inv]
                        method_name = self.method_key[:self.method_key.find('(')]
                        if invc[0] == method_name:
                            inv_tokens_info = TokensInfo(inv)
                            if static == 0:
                                class_token_info = TokensInfo(_class.body_context)
                                Rewriter_.insert_after_start(class_token_info, self.target_class_name + " " + str.lower(
                                    self.target_class_name) + "=" + "new " + self.target_class_name + "();")
                                Rewriter_.apply()
                            Rewriter_.insert_before_start(class_token_info,
                                                          "import " + self.target_package_name + "." + self.target_class_name + ";")
                            Rewriter_.replace(inv_tokens_info, self.target_class_name)
                        Rewriter_.apply()

        class_tokens_info = TokensInfo(_targetclass.parser_context)
        package_tokens_info = TokensInfo(program.packages[self.target_package_name].package_ctx)
        singlefileelement = SingleFileElement(_method.parser_context, _method.filename)
        token_stream_rewriter = TokenStreamRewriter(singlefileelement.get_token_stream())

        # insert name of source.java class befor param that define in body of classe (that use in method)
        for index in exp:
            token_stream_rewriter.insertBeforeIndex(index=index, text=str.lower(self.class_name) + ".")

        for inv in _method.body_method_invocations:
            if inv.getText() == self.target_class_name:
                inv_tokens_info_target = TokensInfo(inv)
                token_stream_rewriter.replaceRange(from_idx=inv_tokens_info_target.start,
                                                   to_idx=inv_tokens_info_target.stop + 1, text=" ")

            # insert source.java class befor methods of sourcr class that used in method
        for i in _method.body_method_invocations_without_typename:
            if i.getText() == self.class_name:
                ii = _method.body_method_invocations_without_typename[i]
                i_tokens = TokensInfo(ii[0])
                token_stream_rewriter.insertBeforeIndex(index=i_tokens.start, text=str.lower(self.class_name) + ".")

        # pass object of source.java class to method
        if param_tokens_info.start is not None:
            token_stream_rewriter.insertBeforeIndex(param_tokens_info.start,
                                                    text=self.class_name + " " + str.lower(self.class_name) + ",")
        else:
            token_stream_rewriter.insertBeforeIndex(method_declaration_info.stop,
                                                    text=self.class_name + " " + str.lower(self.class_name))

        strofmethod = token_stream_rewriter.getText(program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                    start=tokens_info.start,
                                                    stop=tokens_info.stop)

        Rewriter_.insert_before(tokens_info=class_tokens_info, text=strofmethod)
        Rewriter_.insert_after(package_tokens_info,
                               "import " + self.target_package_name + "." + self.target_class_name + ";")
        Rewriter_.replace(tokens_info, "")
        Rewriter_.apply()
        return True


if __name__ == "__main__":
    mylist = get_filenames_in_dir('/home/ali/Desktop/code/TestProject/')
    # mylist = get_filenames_in_dir('tests/movemethod_test')
    print("Testing move_method...")
    if MoveMethodRefactoring(mylist, "test_package", "AppChild1", "testFunc()",
                             "AppChild2", "test_package").do_refactor():
        # if move_method_refactoring(mylist, "ss", "source", "m(int)","target","sss"):
        print("Success!")
    else:
        print("Cannot refactor.")
