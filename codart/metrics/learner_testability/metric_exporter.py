from codart.metrics.testability_prediction import PreProcess
from codart.metrics.testability_prediction import PreProcess

log_path = "/home/y/application.log"
metric_path = "/home/y/PycharmProjects/CodART/codart/metrics/learner_testability/data_model/DS_ALL_METRICS_JFLEX.csv"


p = PreProcess()
df = p.compute_metrics_by_class_list(project_path="/home/y/jflex/jflex.und", n_jobs=3)
df.to_csv(metric_path, index=False)