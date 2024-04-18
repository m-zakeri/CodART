"""
The script is used to test the definition of Understand and Open-ounderstand references kinds

"""

import os
from dotenv import load_dotenv

import oudb.api

load_dotenv()

PROJECT_ROOT_DIR = os.environ.get("PROJECT_ROOT_DIR")
UDB_ROOT_DIR = os.environ.get("UDB_ROOT_DIR")
INIT_POP_FILE = os.environ.get("INIT_POP_FILE")
BENCHMARK_INDEX = int(os.environ.get("BENCHMARK_INDEX", 0))
BENCHMARKS = {
    # Project Path
    "PROJ": [
        "10_water-simulator",  # 0
        "61_noen",  # 1
        "88_jopenchart",  # 2
        "104_vuze",  # 3
        "105_freemind",  # 4
        "107_weka",  # 5
        "commons-codec",  # 6
        "ganttproject_1_11_1_original",  # 7
        "jfreechart-master",  # 8
        "JSON20201115",  # 9
        "jvlt-1.3.2",  # 10
        "tabula-java",  # 11
    ],
    # Understand DB Path
    "UDB": [
        # '10_water-simulator.udb',
        "10_water-simulator.und",
        # '61_noen.udb',
        "61_noen.und",
        # '88_jopenchart.udb',
        "88_jopenchart.und",
        # '104_vuze.udb',  # Not ready
        "104_vuze.und",  # Not ready
        # '105_freemind.udb',
        "105_freemind.und",
        # '107_weka.udb',
        "107_weka.und",
        # 'commons-codec.udb',
        "commons-codec.und",
        # 'ganttproject_1_11_1_original.udb',
        "ganttproject_1_11_1_original.und",
        # 'jfreechart-master.udb',
        "jfreechart-master.und",
        # 'JSON20201115.udb',
        "JSON20201115.und",
        # 'jvlt-1.3.2.udb',
        "jvlt-1.3.2.und",
        # 'tabula-java.udb',
        "tabula-java.und",
    ],
}

PROJECT_PATH = os.path.join(
    PROJECT_ROOT_DIR, BENCHMARKS["PROJ"][BENCHMARK_INDEX]
).replace("/", "\\")
UDB_PATH = os.path.join(UDB_ROOT_DIR, BENCHMARKS["UDB"][BENCHMARK_INDEX]).replace(
    "/", "\\"
)

try:
    from openunderstand import ounderstand as und
except ImportError:
    print("Can not import ounderstand")


def test_open_understand():
    ent = oudb.api.lookup("Admin", "method")[0]
    print(ent, ent.simplename())
    for ref in ent.refs(entkindstring="method", unique=True):
        print(ref, ref.kind().longname())


def test_understand_kinds():
    db = und.open(UDB_PATH)

    for ent in db.ents("Java Class ~Unknown ~Unresolved"):
        # Example for metrics computation
        print(ent.longname())
        # With ounderstand API
        public_methods1 = ent.metric(["CountDeclMethodPublic"]).get(
            "CountDeclMethodPublic", 0
        )

        # With db query
        public_methods2 = len(ent.ents("Define", "Java Method Public Member"))

        print("With API", public_methods1, "\nWith query", public_methods2)

        quit()
        for ref in ent.refs("Declarein"):
            print(
                f'ref.scope (entity performing reference)\t: "{ref.scope().longname()}", kind: "{ref.scope().kind()}"'
            )
            print(
                f'ref.ent (entity being referenced)\t\t: "{ref.ent().longname()}", kind: "{ref.ent().kind()}"'
            )
            print(
                f'File where the reference occurred: "{ref.file().longname()}", line: {ref.line()}'
            )
            # quit()

            # print(f"Entity longname: {ent.longname()}")
            # print(f"Entity parent: {ent.parent()}")
            # print(f"Entity kind: {ent.kind()}")
            # print(f"Entity value: {ent.value()}")
            # print(f"Entity type: {ent.type()}")
            # print(f"Entity contents: {ent.contents()}")
            print("-" * 50)

            # print(f"File kind: {ref.file().kind()}")
            # print(f"Parent: {ref.file().parent()}, long name: {ref.file().longname()}")
            # print(f"Value: {ref.file().value()}, type: {ref.file().type()}")
            # print(f"Contents: {ref.file().contents()}, name: {ref.file().name()}")
            # print('-' * 50)

            # print(f"ref.line: {ref.line()}, ref.col: {ref.column()}, ref.file: {ref.file().name()}")
            # print('-' * 50)
            # print(f"ref.ent.longname:{ref.ent().longname()}, ref.ent.kind:{ref.ent().kind()}")
            # print(f"ref.ent.parent:{ref.ent().parent()}, ref.ent.value:{ref.ent().value()}, "
            #       f"ref.ent.type:{ref.ent().type()}")
            # print(f"ref.ent.contents:{ref.ent().contents()}")
            # print('-' * 50)


if __name__ == "__main__":
    test_understand_kinds()
