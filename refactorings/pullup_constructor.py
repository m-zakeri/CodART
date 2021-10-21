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
import collections

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

from utils.utils2 import parse_and_walk


class PullUpConstructorListener(JavaParserLabeledListener):
    def __init__(self, rewriter: TokenStreamRewriter, is_father: bool, class_name: str, has_father_con: bool,
                 common_sets: [], params: str):
        self.rewriter = rewriter
        self.is_father = is_father
        self.has_father_con = has_father_con
        self.class_name = class_name
        self.common_sets = common_sets
        self.params = params

        self.in_con = False
        self.delete = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_father:
            code = ""
            for var in self.common_sets:
                code += f"this.{var} = {var};\n"
            if self.has_father_con:
                pass
            else:
                self.rewriter.insertBeforeToken(
                    token=ctx.stop,
                    text=f"public {self.class_name}({self.params})" + "{\n" + code + "}"
                )

    def enterConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        if not self.is_father:
            self.in_con = True

    def exitConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        is_valid = False
        for i in self.common_sets:
            if i in ctx.getText():
                is_valid = True
                break
        if self.is_father and self.has_father_con and is_valid:
            code = ""
            for var in self.common_sets:
                code += f"this.{var} = {var};\n"
            self.rewriter.insertBeforeToken(
                token=ctx.stop,
                text=code
            )
        self.in_con = False

    def enterExpression1(self, ctx:JavaParserLabeled.Expression1Context):
        if self.in_con:
            identifier = str(ctx.IDENTIFIER())
            print(identifier, self.common_sets)
            if identifier in self.common_sets:
                self.delete = True

    def exitExpression21(self, ctx:JavaParserLabeled.Expression21Context):
        if self.delete:
            self.rewriter.delete(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex + 1
            )
        self.delete = False



def main(udb_path, source_package, target_class, class_names: list):
    if len(class_names) < 2:
        print("class_names is empty.")
        return None
    db = und.open(udb_path)
    parent_cons = []

    # Check children
    parent = db.lookup(f"{target_class}", "Class")
    if len(parent) != 1:
        print("Something is wrong!")
        return
    parent = parent[0]
    parent_file = db.lookup(f"{target_class}.java", "File")[0].longname()

    for i in parent.ents("Define", "Constructor"):
        parent_cons.append(i.parameters())

    # Find constructor entities group by signature
    constructors = {}

    for child in class_names:
        cons = db.lookup(f"{child}.{child}", "Constructor")
        for con in cons:
            if source_package not in con.parent().longname():
                print("Source package does not match.")
                return
            parameters = con.parameters()
            if parameters in constructors:
                constructors[parameters].append(con)
            else:
                constructors[parameters] = [con]

    # Find common statements
    for k in constructors:
        meta_data = {
            parent_file: {'is_father': True, 'has_father_con': k in parent_cons, 'class_name': parent.simplename()},
        }
        con = constructors[k][0]
        ents = []

        for ref in con.refs("Set"):
            data = {'is_father': False, 'has_father_con': k in parent_cons,
                    'class_name': con.parent().simplename()}
            if ref.file().longname() not in meta_data.keys():
                meta_data[ref.file().longname()] = data
            if target_class in ref.ent().longname():
                ents.append(ref.ent().simplename())

        for i in range(1, len(constructors[k])):
            con2 = constructors[k][i]
            for ref in con2.refs("Set"):
                data = {'is_father': False, 'has_father_con': k in parent_cons,
                        'class_name': con2.parent().simplename()}
                if ref.file().longname() not in meta_data.keys():
                    meta_data[ref.file().longname()] = data
                if target_class in ref.ent().longname():
                    ents.append(ref.ent().simplename())

        ents = [item for item, count in collections.Counter(ents).items() if count > 1]
        if len(meta_data.keys()) > 1:
            for file_name in meta_data:
                data = meta_data[file_name]
                parse_and_walk(
                    file_name,
                    PullUpConstructorListener,
                    has_write=True,
                    is_father=data['is_father'],
                    has_father_con=data['has_father_con'],
                    common_sets=ents,
                    class_name=data['class_name'],
                    params=k
                )


if __name__ == "__main__":
    main(
        "D:\Dev\JavaSample\JavaSample1.udb",
        "",
        "Employee",
        class_names=["Admin", "Manager", ]
    )
