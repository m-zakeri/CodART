from configparser import ConfigParser
import logging
import pandas as pd
import os
from pymoo.core.problem import Problem
import numpy as np
from multiprocessing import Process, Array
from codart.utility.directory_utils import update_understand_database, git_restore
from codart.metrics.qmood import DesignQualityAttributes


config = ConfigParser()
config.read("config.ini")
logger = logging.getLogger()


class ProblemManyObjective(Problem):

    def __init__(
        self,
        n_objectives: int = int(config["Config"]["OBJECTIVE"]),
        n_refactorings_lowerbound: int = int(config["Config"]["LOWER_BAND"]),
        n_refactorings_upperbound: int = int(config["Config"]["UPPER_BAND"]),
        evaluate_in_parallel: bool = bool(config["Config"]["evaluate_in_parallel"]),
        verbose_design_metrics: bool = bool(config["Config"]["verbose_design_metrics"]),
    ):

        super(ProblemManyObjective, self).__init__(
            n_var=1,
            n_obj=n_objectives,
            n_constr=0,
        )
        self.n_refactorings_lowerbound = n_refactorings_lowerbound
        self.n_refactorings_upperbound = n_refactorings_upperbound
        self.evaluate_in_parallel = evaluate_in_parallel
        self.verbose_design_metrics = verbose_design_metrics

    def _evaluate(self, x, out, *args, **kwargs):
        objective_values = []
        for k, individual_ in enumerate(x):
            # Stage 0: Git restore
            logger.debug("Executing git restore.")
            git_restore(config["Config"]["repo_address"])
            logger.debug("Updating understand database after git restore.")
            update_understand_database(
                os.path.join(
                    config["Config"]["db_address"], config["Config"]["db_name"]
                )
            )
            logger.debug(f"Reached an Individual with size {len(individual_[0])}")
            for refactoring_operation in individual_[0]:
                res = refactoring_operation.do_refactoring()
                logger.debug(
                    f"Updating understand database after {refactoring_operation.name}."
                )
                update_understand_database(config.UDB_PATH)

            arr = Array("d", range(self.n_obj))
            qmood_quality_attributes = DesignQualityAttributes(
                udb_path=os.path.join(
                    config["Config"]["db_address"], config["Config"]["db_name"]
                )
            )
            if self.evaluate_in_parallel:
                p1 = Process(
                    target=self.calc_qmood_objectives,
                    args=(
                        arr,
                        qmood_quality_attributes,
                    ),
                )
                if self.n_obj == 8:
                    p2 = Process(
                        target=self.calc_testability_objective,
                        args=(
                            os.path.join(
                                config["Config"]["db_address"],
                                config["Config"]["db_name"],
                            ),
                            arr,
                        ),
                    )
                    p3 = Process(
                        target=self.calc_modularity_objective,
                        args=(
                            os.path.join(
                                config["Config"]["db_address"],
                                config["Config"]["db_name"],
                            ),
                            arr,
                        ),
                    )
                    p1.start(), p2.start(), p3.start()
                    p1.join(), p2.join(), p3.join()
                else:
                    p1.start()
                    p1.join()
            else:
                arr[0] = qmood_quality_attributes.reusability
                arr[1] = qmood_quality_attributes.understandability
                arr[2] = qmood_quality_attributes.flexibility
                arr[3] = qmood_quality_attributes.functionality
                arr[4] = qmood_quality_attributes.effectiveness
                arr[5] = qmood_quality_attributes.extendability
                if self.n_obj == 8:
                    arr[6] = qmood_quality_attributes.testability
                    arr[7] = qmood_quality_attributes.modularity

                if self.verbose_design_metrics:
                    design_metrics = {
                        "DSC": [qmood_quality_attributes.DSC],
                        "NOH": [qmood_quality_attributes.NOH],
                        "ANA": [qmood_quality_attributes.ANA],
                        "MOA": [qmood_quality_attributes.MOA],
                        "DAM": [qmood_quality_attributes.DAM],
                        "CAMC": [qmood_quality_attributes.CAMC],
                        "CIS": [qmood_quality_attributes.CIS],
                        "NOM": [qmood_quality_attributes.NOM],
                        "DCC": [qmood_quality_attributes.DCC],
                        "MFA": [qmood_quality_attributes.MFA],
                        "NOP": [qmood_quality_attributes.NOP],
                    }
                    self.log_design_metrics(design_metrics)

                del qmood_quality_attributes

            objective_values.append([-1 * i for i in arr])
            logger.info(f"Objective values for individual {k}: {[i for i in arr]}")

        out["F"] = np.array(objective_values, dtype=float)

    def log_design_metrics(self, design_metrics):
        design_metrics_path = os.path.join(
            config.PROJECT_LOG_DIR,
            f"{config.PROJECT_NAME}_design_metrics_log_{config.global_execution_start_time}.csv",
        )

        df_design_metrics = pd.DataFrame(data=design_metrics)
        if os.path.exists(design_metrics_path):
            df = pd.read_csv(design_metrics_path, index_col=False)
            df_result = pd.concat([df, df_design_metrics], ignore_index=True)
            df_result.to_csv(design_metrics_path, index=False)
        else:
            df_design_metrics.to_csv(design_metrics_path, index=False)

    def calc_qmood_objectives(self, arr_, qmood_quality_attributes):
        arr_[0] = qmood_quality_attributes.reusability
        arr_[1] = qmood_quality_attributes.understandability
        arr_[2] = qmood_quality_attributes.flexibility
        arr_[3] = qmood_quality_attributes.functionality
        arr_[4] = qmood_quality_attributes.effectiveness
        arr_[5] = qmood_quality_attributes.extendability

    def calc_testability_objective(self, arr_, qmood_quality_attributes):
        arr_[6] = qmood_quality_attributes.testability

    def calc_modularity_objective(self, arr_, qmood_quality_attributes):
        arr_[7] = qmood_quality_attributes.modularity
