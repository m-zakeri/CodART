from codart.metrics.testability_prediction import PreProcess
from codart.metrics.data_preparation_evo_suite_4 import PreProcess as pp
import understand as und

log_path = "/home/y/application.log"
metric_path = "/home/y/PycharmProjects/CodART/codart/metrics/learner_testability/data_model/DS_ALL_METRICS_JFLEX.csv"
evo_metric_path = "/home/y/PycharmProjects/CodART/codart/metrics/learner_testability/data_model/DS_EVO_METRICS_JFLEX.csv"
project_path = "/home/y/jflex/jflex.und"
# testability

# p = PreProcess()
# df = p.compute_metrics_by_class_list(project_path= project_path, n_jobs=3)
# df.to_csv(metric_path, index=False)

# evosuite

evop = pp()
db = und.open(project_path)
class_list = evop.extract_project_classes(db=db)
db.close()
df = evop.compute_metrics_by_class_list(class_list=class_list, csv_path=evo_metric_path, database=db, project_name='jflex')
df.to_csv(metric_path, index=False)
