from openunderstand import ounderstand as und
from utils_g10 import get_project_info, report_metric


REF_NAME = "origin"
PRJ_INDEX = 0
METRIC_NAME = "CountStmtExe"


def test():
    info = get_project_info(PRJ_INDEX, REF_NAME)
    db = und.open(info["DB_PATH"])

    project_metric_count = 0
    metric_list = []
    ent_kind_set = set()

    for ent in db.ents():
        ent_kind = ent.kind().__repr__()
        ent_metric = ent.metric([METRIC_NAME]).get(METRIC_NAME, 0)

        if ent_kind == "Java Package":
            continue

        if ent_metric and ent_kind.startswith("Java"):
            project_metric_count += ent_metric
            metric_list.append(
                {
                    "kind": ent_kind,
                    "name": ent.simplename(),
                    "val": ent_metric,
                    "longname": ent.longname(),
                }
            )
            ent_kind_set.add(ent_kind)

    report_metric(project_metric_count, ent_kind_set, metric_list, METRIC_NAME)


if __name__ == "__main__":
    test()
