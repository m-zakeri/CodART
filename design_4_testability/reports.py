import json
import matplotlib.pyplot as plt
import os
import logging
import pandas as pd
import understand as und

from design_4_testability.class_diagram_extraction.class_diagram import ClassDiagram
from codart.refactoring_design_patterns.factory import Factory
from codart.refactoring_design_patterns.injection import Injection
from design_4_testability.evaluation.complexity import Complexity
from design_4_testability.evaluation.testability.design_testability_prediction2 import main as evaluate_testability
from design_4_testability.evaluation.testability.directory_utils import update_understand_database
from design_4_testability.utils.utils import File
import config


class Report:
    def __init__(self, java_project, reload_from_disk=True):
        self.java_project = java_project
        self.java_project_address = config.projects_info[java_project]['path']
        self.base_dirs = config.projects_info[java_project]['base_dirs']
        self.db_path_ = config.projects_info[java_project]['db_path']
        self.log_path_ = config.projects_info[java_project]['log_path']
        if reload_from_disk:
            self.reload_from_disk()

    def reload_from_disk(self):
        self.files = File.find_all_file(self.java_project_address, 'java')
        self.index_dic = File.indexing_files_directory(self.files, 'class_index.json', self.base_dirs)
        self.cd = ClassDiagram(self.java_project_address, self.base_dirs, self.files, self.index_dic)
        self.cd.make_class_diagram()
        # self.cd.set_stereotypes()
        self.cdg = self.cd.get_CDG()

    def restore_java_project(self):
        os.chdir(f"{config.BASE_DIR}{self.java_project}")
        os.popen("git restore .").close()
        os.popen("git clean -f -d").close()
        path = os.getcwd()
        path = os.path.abspath(os.path.join(path, os.pardir))
        path = os.path.abspath(os.path.join(path, os.pardir))
        os.chdir(path)
        update_understand_database(self.db_path_)

    def get_code_changes_rate(self):
        os.chdir(f"{config.BASE_DIR}{self.java_project}")
        tmp = os.popen("git diff --shortstat").read()
        tmp = tmp.split()
        path = os.getcwd()
        path = os.path.abspath(os.path.join(path, os.pardir))
        path = os.path.abspath(os.path.join(path, os.pardir))
        os.chdir(path)
        if len(tmp) > 0:
            return {"insertion": int(tmp[3]), "deletion": int(tmp[5])}
        else:
            return {"insertion": 0, "deletion": 0}

    def get_json_report(self, sensitivity, save=True, edit=True):
        pass

    def get_pandas_report(self, json_report, save=True):
        pass


class FactoryReport(Report):
    def get_single_report(self, sensitivity, edit=True):
        report = {
            "java_project": self.java_project,
            "sensitivity": sensitivity,
            "testability": {"before": int(), "before_time": int(),
                            "after": int(), "after_time": int()},
            "complexity": {"before": int(), "before_time": int(),
                           "after": int(), "after_time": int()},
            "no_classes": {"before": int(), "after": int()},
            "no_relationships": {"before": int(), "after": int()},
            "code_changes_rate": int(),
            "cases": list()
            }

        # c = Complexity(self.cd)
        # matrix, complexity_time = c.get_matrix()
        # report["complexity"]["before"] = Complexity.get_sum_of_matrix(matrix)
        # report["complexity"]["before_time"] = complexity_time

        update_understand_database(self.db_path_)

        report["no_classes"]["before"] = len(self.cd.class_diagram_graph.nodes)
        report["no_relationships"]["before"] = len(self.cd.class_diagram_graph.edges)

        report["testability"]["before"], testability_time = evaluate_testability(
            self.db_path_,
            initial_value=1.0,
            verbose=False,
            log_path=self.log_path_
        )
        report["testability"]["before_time"] = testability_time

        f = Factory(self.index_dic, self.cd.class_diagram_graph, self.base_dirs)
        report["cases"] = f.refactor(
            sensitivity,
            edit=edit
        )

        if edit:
            self.reload_from_disk()

            # c = Complexity(self.cd)
            # matrix, complexity_time = c.get_matrix()
            # report["complexity"]["after"] = Complexity.get_sum_of_matrix(matrix)
            # report["complexity"]["after_time"] = complexity_time

            update_understand_database(self.db_path_)

            report["no_classes"]["after"] = len(self.cd.class_diagram_graph.nodes)
            report["no_relationships"]["after"] = len(self.cd.class_diagram_graph.edges)

            report["testability"]["after"], testability_time = evaluate_testability(
                self.db_path_,
                initial_value=1.0,
                verbose=False,
                log_path=self.log_path_
            )
            report["testability"]["after_time"] = testability_time

            code_changes_rate = self.get_code_changes_rate()
            report["code_changes_rate"] = code_changes_rate["insertion"] + code_changes_rate["deletion"]

        return report

    def get_list_of_report(self, no_of_samples, save=True, edit=True):
        reports = list()
        for sensitivity in range(1, no_of_samples + 1):
            reports.append(self.get_single_report(sensitivity / no_of_samples, edit=edit))
            if edit:
                self.restore_java_project()
                self.reload_from_disk()

            if save:
                with open(f"{config.D4T_LOG_DIR}{self.java_project}/{self.java_project}_factory_report.json", 'w') as f:
                    json.dump(reports, f, indent=4)
        return reports

    def show_cases_vs_sensitivity_chart(self, json_report, show=True, save=True):
        sensitivity_list = list()
        no_cases_list = list()
        for report in json_report:
            sensitivity_list.append(report["sensitivity"])
            no_cases_list.append(len(report["cases"]))

        plt.plot(sensitivity_list, no_cases_list)
        plt.title(self.java_project)
        plt.xlabel('sensitivity')
        plt.ylabel('number of cases')

        if save:
            plt.savefig(f"{config.D4T_LOG_DIR}{self.java_project}/cases_vs_sensitivity_chart.png")
        if show:
            plt.show()
        plt.clf()

    def show_avg_of_common_methods_vs_sensitivity_chart(self, json_report, show=True, save=True):
        sensitivity_list = list()
        avg_of_common_methods_list = list()
        for report in json_report:
            sensitivity_list.append(report["sensitivity"])
            avg_of_common_methods_list.append(FactoryReport.__get_avg_no_methods(report))

        plt.plot(sensitivity_list, avg_of_common_methods_list)
        plt.title(self.java_project)
        plt.xlabel('sensitivity')
        plt.ylabel('average number of common methods')

        if save:
            plt.savefig(f"{config.D4T_LOG_DIR}{self.java_project}/avg_of_common_methods_vs_sensitivity_chart.png")
        if show:
            plt.show()
        plt.clf()

    def show_avg_no_of_products_vs_sensitivity_chart(self, json_report, show=True, save=True):
        sensitivity_list = list()
        avg_of_common_methods_list = list()
        for report in json_report:
            sensitivity_list.append(report["sensitivity"])
            avg_of_common_methods_list.append(FactoryReport.__get_avg_no_products(report))

        plt.plot(sensitivity_list, avg_of_common_methods_list)
        plt.title(self.java_project)
        plt.xlabel('sensitivity')
        plt.ylabel('average number of products')

        if save:
            plt.savefig(f"{config.D4T_LOG_DIR}{self.java_project}/avg_number_of_products_vs_sensitivity_chart.png")
        if show:
            plt.show()
        plt.clf()

    def show_complexity_vs_sensitivity_chart(self, json_report, show=True, save=True):
        sensitivity_list = list()
        complexity_list = list()
        for report in json_report:
            sensitivity_list.append(report["sensitivity"])
            complexity_list.append(report["complexity"]["after"] - report["complexity"]["before"])

        plt.plot(sensitivity_list, complexity_list)
        plt.title(self.java_project)
        plt.xlabel('sensitivity')
        plt.ylabel('The rate of change of complexity')

        if save:
            plt.savefig(f"{config.D4T_LOG_DIR}{self.java_project}/complexity_vs_sensitivity_chart.png")
        if show:
            plt.show()
        plt.clf()

    def show_testability_vs_sensitivity_chart(self, json_report, show=True, save=True):
        sensitivity_list = list()
        testability_list = list()
        for report in json_report:
            sensitivity_list.append(report["sensitivity"])
            testability_list.append(((report["testability"]["after"] - report["testability"]["before"]) / report["testability"]["before"]) * 100)

        plt.plot(sensitivity_list, testability_list)
        plt.title(self.java_project)
        plt.xlabel('sensitivity')
        plt.ylabel('The rate of change of testability')

        if save:
            plt.savefig(f"{config.D4T_LOG_DIR}{self.java_project}/testability_vs_sensitivity_chart.png")
        if show:
            plt.show()
        plt.clf()

    def show_code_changed_rate_vs_sensitivity_chart(self, json_report, show=True, save=True):
        sensitivity_list = list()
        complexity_list = list()
        for report in json_report:
            sensitivity_list.append(report["sensitivity"])
            complexity_list.append(report["code_changes_rate"])

        plt.plot(sensitivity_list, complexity_list)
        plt.title(self.java_project)
        plt.xlabel('sensitivity')
        plt.ylabel('code changes rate')

        if save:
            plt.savefig(f"{config.D4T_LOG_DIR}{self.java_project}/code_changed_rate_vs_sensitivity_chart.png")
        if show:
            plt.show()
        plt.clf()

    @staticmethod
    def __get_avg_no_methods(json_report):
        a = 0
        b = 0
        for case in json_report["cases"]:
            b += 1
            a += len(case["products"]["methods"])
        if b == 0:
            return 0
        else:
            return round(a / b, 2)

    @staticmethod
    def __get_avg_no_products(json_report):
        a = 0
        b = 0
        for case in json_report["cases"]:
            b += 1
            a += len(case["products"]["classes"])
        if b == 0:
            return 0
        else:
            return round(a / b, 2)


class InjectionReport(Report):
    def get_single_report(self, edit=True, save=True):
        report = {
            "java_project": self.java_project,
            "testability": {"before": int(), "before_time": int(),
                            "after": int(), "after_time": int()},
            "no_classes": {"before": int(), "after": int()},
            "no_relationships": {"before": int(), "after": int()},
            "code_changes_rate": int(),
            "cases": dict()
            }

        update_understand_database(self.db_path_)

        report["no_classes"]["before"] = len(self.cd.class_diagram_graph.nodes)
        report["no_relationships"]["before"] = len(self.cd.class_diagram_graph.edges)

        report["testability"]["before"], testability_time = evaluate_testability(
            self.db_path_,
            initial_value=1.0,
            verbose=False,
            log_path=self.log_path_
        )
        report["testability"]["before_time"] = testability_time

        injection = Injection(self.base_dirs, self.index_dic, self.files, self.cd.class_diagram_graph)
        report['cases'] = injection.refactor()

        if edit:
            self.reload_from_disk()

            update_understand_database(self.db_path_)

            report["no_classes"]["after"] = len(self.cd.class_diagram_graph.nodes)
            report["no_relationships"]["after"] = len(self.cd.class_diagram_graph.edges)

            report["testability"]["after"], testability_time = evaluate_testability(
                self.db_path_,
                initial_value=1.0,
                verbose=False,
                log_path=self.log_path_
            )
            report["testability"]["after_time"] = testability_time

            code_changes_rate = self.get_code_changes_rate()
            report["code_changes_rate"] = code_changes_rate["insertion"] + code_changes_rate["deletion"]

        if save:
            with open(f"{config.D4T_LOG_DIR}{self.java_project}/{self.java_project}_injection_report.json", 'w') as f:
                json.dump(report, f, indent=4)

        return report


def find_best_sensitivity(factory_report):
    sensitivity = -1
    testability = 0
    for report in factory_report:
        if report['testability']['after'] > testability:
            sensitivity = report['sensitivity']
            testability = report['testability']['after']
    return sensitivity


def get_relative_improvement(before, after):
    return round((after - before) / before, 5) * 100


def get_final_csv_report(d4t_log_path):
    pandas_report = {
        "project": [],
        "sensitivity": [],
        "no_classes": [],
        "testability_original": [],
        "testability_after_factory": [],
        "testability_after_injection": [],
        "relative_improvement_after_factory": [],
        "relative_improvement_after_injection": [],
        "relative_improvement_total": [],
    }

    projects = [f for f in os.listdir(d4t_log_path) if not os.path.isfile(os.path.join(d4t_log_path, f))]
    for project in projects:
        report_path = os.path.join(d4t_log_path, project, f'{project}_final_report.json')
        if not os.path.exists(report_path):
            continue
        with open(report_path) as f:
            report = json.load(f)

            pandas_report["project"].append(report['factory']["java_project"])
            pandas_report["sensitivity"].append(report['factory']["sensitivity"])
            pandas_report["testability_original"].append(report['factory']["testability"]['before'])
            pandas_report["testability_after_factory"].append(report['factory']["testability"]['after'])
            pandas_report["testability_after_injection"].append(report['injection']["testability"]['after'])
            pandas_report["relative_improvement_after_factory"].append(
                get_relative_improvement(
                    pandas_report["testability_original"][-1],
                    pandas_report["testability_after_factory"][-1]
                )
            )
            pandas_report["relative_improvement_after_injection"].append(
                get_relative_improvement(
                    pandas_report["testability_after_factory"][-1],
                    pandas_report["testability_after_injection"][-1]
                )
            )
            pandas_report["relative_improvement_total"].append(
                get_relative_improvement(
                    pandas_report["testability_original"][-1],
                    pandas_report["testability_after_injection"][-1]
                )
            )
    df = pd.DataFrame(pandas_report).sort_values(by=['relative_improvement_total'], ascending=False)
    df.to_csv(f"{d4t_log_path}/final_report.csv", index=False)
    return df


logging.basicConfig(filename='errors.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    for java_project in config.projects_info:
        try:
            fr = Report(java_project, False)
            fr.restore_java_project()
            fr = FactoryReport(java_project, True)
            factory_report = fr.get_list_of_report(10)

            # with open(f"{config.BASE_DIR}/{java_project}/factory_report.json") as f:
            #     factory_report = json.load(f)

            # fr.show_testability_vs_sensitivity_chart(factory_report, show=False)
            # fr.show_cases_vs_sensitivity_chart(factory_report, show=False)
            # fr.show_avg_of_common_methods_vs_sensitivity_chart(factory_report, show=False)
            # fr.show_avg_no_of_products_vs_sensitivity_chart(factory_report, show=False)
            # # fr.show_complexity_vs_sensitivity_chart(factory_report)
            # fr.show_code_changed_rate_vs_sensitivity_chart(factory_report, show=False)

            sensitivity = find_best_sensitivity(factory_report)
            factory_report = fr.get_single_report(sensitivity)

            ir = InjectionReport(java_project)
            injection_report = ir.get_single_report(save=False)
            report = {'factory': factory_report, 'injection': injection_report}
            with open(f"{config.D4T_LOG_DIR}{java_project}/{java_project}_final_report.json", 'w') as f:
                json.dump(report, f, indent=4)
        except Exception as e:
            logger.error(java_project)
            logger.error(str(e))
            logger.error('-'*20)
