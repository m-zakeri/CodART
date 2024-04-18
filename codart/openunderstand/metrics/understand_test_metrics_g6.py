"""
The script is used to test the definition of Understand and Open-ounderstand references kinds

"""

import os

from dotenv import load_dotenv
import understand as und

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

try:
    import understand as und
except ImportError:
    import understand as und

    print("Can not import ounderstand")


def test_open_understand():
    ent = oudb.api.lookup("Admin", "method")[0]
    print(ent, ent.simplename())
    for ref in ent.refs(entkindstring="method", unique=True):
        print(ref, ref.kind().longname())


def test_understand_kinds():
    db = und.open(
        r"../../benchmark/SalaryCalculator-master/SalaryCalculator-master.und"
    )
    und_all_results = {}
    und_default_results = {}
    und_private_results = {}
    und_protected_results = {}

    print("Understand Results \n")
    for ent in db.ents("Java Class ~Unknown ~Unresolved"):
        ent_name = ent.name()
        all_methods = ent.metric(["CountDeclMethodAll"]).get("CountDeclMethodAll", 0)
        und_all_results[ent_name] = all_methods

        default_methods = ent.metric(["CountDeclMethodDefault"]).get(
            "CountDeclMethodDefault", 0
        )
        und_default_results[ent_name] = default_methods

        private_methods = ent.metric(["CountDeclMethodPrivate"]).get(
            "CountDeclMethodPrivate", 0
        )
        und_private_results[ent_name] = private_methods

        protected_methods = ent.metric(["CountDeclMethodProtected"]).get(
            "CountDeclMethodProtected", 0
        )
        und_protected_results[ent_name] = protected_methods

    print("All methods : ", und_all_results)
    print("Default methods : ", und_default_results)
    print("Private methods : ", und_private_results)
    print("Protected methods : ", und_protected_results)


if __name__ == "__main__":
    test_understand_kinds()
