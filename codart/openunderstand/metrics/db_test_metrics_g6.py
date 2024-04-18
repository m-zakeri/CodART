from count_decl_method_all import count_decl_method_all
from count_decl_method_default import count_decl_method_default
from count_decl_method_private import count_decl_method_private
from count_decl_method_protected import count_decl_method_protected


def test_all_metrics(db_path):
    print("Our Results \n")
    print("All methods : ", count_decl_method_all(db_path))
    print("Default methods : ", count_decl_method_default(db_path))
    print("Private methods : ", count_decl_method_private(db_path))
    print("Protected methods : ", count_decl_method_protected(db_path))


if __name__ == "__main__":
    test_all_metrics("../../benchmark2_database.oudb")
