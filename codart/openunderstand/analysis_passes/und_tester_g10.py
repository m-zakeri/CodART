from openunderstand import ounderstand as und
from analysis_passes.g10_import_importby import get_project_info

PRJ_INDEX = 0
REF_NAME = "origin"


def test_understand_kinds():
    info = get_project_info(PRJ_INDEX, REF_NAME)
    db = und.open(info["DB_PATH"])
    for ent in db.ents():
        for ref in ent.refs("Import"):
            print(f"1. ref name: {ref.kindname()}")
            print(
                f"2. ref scope: {ref.scope().longname()} || kind: {ref.scope().kind()}"
            )
            print(f"3. ref ent: {ref.ent().longname()} || kind: {ref.ent().kind()}")
            print(f"4. file location: {ref.file().longname()} || line: {ref.line()}")
            print("-" * 25)
