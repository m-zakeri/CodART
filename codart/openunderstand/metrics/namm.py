from antlr4 import *
from openunderstand.oudb.models import EntityModel
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class NAMMListener(JavaParserLabeledListener):
    def __init__(self):
        self.Mutator_num = 0
        self.Accessor_num = 0
        self.Accessor = []
        self.Mutator = []
        self.att = []

    @property
    def get_NAMM(self):
        self.compare()
        d = {}
        d["Accessor_num"] = self.Accessor_num
        d["Mutator_num"] = self.Mutator_num
        return d

    def enterBlockStatement1(self, ctx: JavaParserLabeled.BlockStatement1Context):
        id1 = ctx.children[0]
        t = type(id1)
        if t == JavaParserLabeled.Statement10Context:
            id2 = id1.children[1]
            id3 = id2
            while True:
                try:
                    id3 = id2.IDENTIFIER()
                    break
                except:
                    try:
                        id2 = id2.children[0]
                    except:
                        break
            try:
                self.Accessor.append(id3.getText())
            except:
                pass
        elif t == JavaParserLabeled.Statement15Context:
            id2 = id1.children[0]
            id3 = id2
            while True:
                try:
                    id3 = id2.children[0].IDENTIFIER()
                    break
                except:
                    try:
                        id2 = id2.children[0]
                    except:
                        break
            try:
                self.Mutator.append(id3.getText())
            except:
                pass

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        id = ctx.variableDeclarators().children[0].children[0].IDENTIFIER().getText()
        self.att.append(id)

    def compare(self):
        for item in self.Accessor:
            if item in self.att:
                self.Accessor_num += 1
        for item in self.Mutator:
            if item in self.att:
                self.Mutator_num += 1


def get_namm(ent_model=None, type_namm: str = "Mutator_num") -> int:
    """
    type: Accessor_num or Mutator_num
    """
    # enter file name here
    entity_longname = ent_model.longname()
    files = []
    if entity_longname is None:
        for ent in EntityModel.select().where(EntityModel._kind_id == 1):
            files.append(ent._contents)
        listener = NAMMListener()
    else:
        # search in db
        entity = EntityModel.get_or_none(_longname=entity_longname)
        if entity is None:
            print("there is not such an entity")
        else:
            current = entity
            parent = EntityModel.get_or_none(_id=current._parent_id)
            while current._parent_id is not None and not (70 <= parent._kind._id <= 73):
                current = EntityModel.get_or_none(_id=current._parent_id)
                parent = EntityModel.get_or_none(_id=current._parent_id)
            files.append(current._contents)
            listener = NAMMListener()

    for file_content in files:
        file_stream = InputStream(file_content)
        lexer = JavaLexer(file_stream)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        parse_tree = parser.compilationUnit()
        walker = ParseTreeWalker()
        walker.walk(listener=listener, t=parse_tree)
    return listener.get_NAMM[type_namm]
