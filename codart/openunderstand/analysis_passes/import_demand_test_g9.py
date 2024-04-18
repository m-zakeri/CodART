from antlr4 import *
from oudb.models import *
from oudb.api import open as db_open, create_db
from oudb.models import EntityModel, ReferenceModel


try:
    from openunderstand import ounderstand as und
except ImportError:
    print("Can not import ounderstand")
# E:\2\OpenUnderstand\benchmark\calculator_app\calculator_app.und
db = und.open(
    r"E:/comppppppp/OpenUnderstand/benchmark/calculator_app/calculator_app/calculator_app.und"
)

# ent = db.lookup("Admin", "method")[0]
for ent in db.ents():
    for ref in ent.refs(refkindstring="import demand"):

        create_db("../myOpenunder.db", project_dir="..\benchmark")

        ent, _ = EntityModel.get_or_create(
            _kind=1,
            _parent="None",
            _name=ref.scope().longname(),
            _longname=ref.ent().longname(),
            _contents=FileStream(ref.scope().longname(), encoding="utf-8"),
        )

        ReferenceModel.get_or_create(
            _kind=204,
            _file=ref.scope().longname(),
            _line=ref.line(),
            _column=ref.column(),
            _ent=ent.get_id(),
            _scope=ref.scope().longname(),
        )

        db = db_open("../myOpenunder.db")

        # print(f'ref.scope (entity performing reference       ===========>)\n:'
        #       f' "{ref.scope().longname()}", kind: "{ref.scope().kind()}"')
        #
        # print(f'ref.ent (entity being referenced      ==============>)\n\t:'
        #       f' "{ref.ent().longname()}", kind: "{ref.ent().kind()}"')
        #
        # print(f'File where the reference occurred: ================> "{ref.file().longname()}",'
        #       f' line: {ref.line()}'  , "\n" "*********" ,  ref.ent().name  ,"**" )
        #
        # print( "*","ref.ent =",  ref.ent(),"\n" ,"ref.scope =",ref.scope() ,"\n" ,"ref.file =", ref.file(),"\n"  ,"ref.line =",
        #        ref.line(),"\n" ,"ref.column =" , ref.column() ,"\n" ,"ref.kind =", ref.kind(),"\n" ,"ref.isforward =" ,ref.isforward(),
        #        "\n"  ,"ref.kindname =",ref.kindname(),"\n" ,"ref.ent().longname =",ref.ent().longname(),
        #        "\n" ,"ref.ent().name =",ref.ent().name ,"\n" ,"ref.ent().language  =  ",
        #        ref.ent().language(),"\n"  ,"ref.ent().kind =  ", ref.ent().kind(),
        #        "\n" ,"ref.ent().parent  =", ref.ent().parent() ,"\n" ,"ref.ent().type  =",
        #        ref.ent().type() ,"\n" ,"ref.ent().value  =",
        # ref.ent().value(),"\n" )
