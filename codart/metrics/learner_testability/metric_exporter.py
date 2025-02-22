from codart.metrics.data_preparation_evo_suite_4 import PreProcess as PP
from codart.metrics.testability_prediction import PreProcess
import understand as und
import pandas as pd

log_path = "/home/y/Desktop/codes/university/CodART/application.log"
metric_path = "/home/y/Desktop/codes/university/CodART/codart/metrics/learner_testability/data_model/DS_ALL_METRICS_JSON.csv"
evo_metric_path = "/home/y/Desktop/codes/university/CodART/codart/metrics/learner_testability/data_model/DS_EVO_METRICS_JSON.csv"
project_path = "/home/y/Desktop/codes/university/JSON-java/JSON-java.und"
# testability

p = PreProcess()
df = p.compute_metrics_by_class_list(project_path= project_path, n_jobs=1)
df.to_csv(metric_path, index=False)

# evosuite

# evop = PP()
# db = und.open(project_path)
# class_list = evop.extract_project_classes(db=db)
# print("Class list raw data:", class_list)
# if not isinstance(class_list, pd.DataFrame):
#     class_list = pd.DataFrame(class_list)
# print("Class list DataFrame columns:", class_list.columns)
# if class_list.shape[1] == 1:
#     class_list.columns = ['Class']
# print("Class list DataFrame after renaming if needed:", class_list)
# df = evop.compute_metrics_by_class_list(class_list=class_list, csv_path=evo_metric_path, database=db, project_name='JSON-java')
# df.to_csv(metric_path, index=False)
# db.close()