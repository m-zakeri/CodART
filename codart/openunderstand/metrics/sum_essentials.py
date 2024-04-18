from antlr4 import *
from openunderstand.oudb.models import EntityModel
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class EssentialListener(JavaParserLabeledListener):
    def __init__(self):
        self.index = 0
        self.layers = []
        self.counts = []
        self.sum = 0
        self.entered_switch = False

    @property
    def get_sum_essential(self):
        return self.sum

    # if
    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        self.index += 1
        if ctx.ELSE() is not None:
            self.layers.append(1)
        else:
            self.layers.append(0)
        self.counts.append(0)

    def exitStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        self.index -= 1
        if self.index == 0:
            while len(self.layers) != 0:
                last = self.layers.pop(0)
                if last > 0:
                    self.sum += self.counts.pop(0) + last
                else:
                    break
            self.layers = []
            self.counts = []

    # while
    def enterStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        if len(self.layers) == 0:
            self.sum += 1
        else:
            self.counts[-1] += 1

    # for
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        if len(self.layers) == 0:
            self.sum += 1
        else:
            self.counts[-1] += 1

    # do-while
    def enterStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        if len(self.layers) == 0:
            self.sum += 1
        else:
            self.counts[-1] += 1

    # switch
    def enterStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.entered_switch = True

    def exitStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.entered_switch = False

    def enterStatement12(self, ctx: JavaParserLabeled.Statement12Context):
        if not self.entered_switch:
            if self.layers[-1] < 2:
                self.layers[-1] += 1


def get_sum_essentials(ent_model=None):
    # enter file name here
    entity_longname = ent_model.longname()

    files = []
    # method = None
    if entity_longname is None:
        for ent in EntityModel.select().where(EntityModel._kind_id == 1):
            files.append(ent._contents)
        listener = EssentialListener()
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
            listener = EssentialListener()

    for file_content in files:
        file_stream = InputStream(file_content)
        lexer = JavaLexer(file_stream)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        parse_tree = parser.compilationUnit()

        walker = ParseTreeWalker()
        walker.walk(listener=listener, t=parse_tree)
    return listener.get_sum_essential
