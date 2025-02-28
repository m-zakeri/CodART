from collections import defaultdict
from typing import Optional
import numpy as np
import torch
import tqdm
from tensordict import TensorDict, TensorDictBase
from tensordict.nn import TensorDictModule
from torch import nn
from torchrl.data import BoundedTensorSpec, CompositeSpec, UnboundedContinuousTensorSpec
from torchrl.envs import (
    CatTensors,
    EnvBase,
    Transform,
    TransformedEnv,
    UnsqueezeTransform,
)
from torchrl.envs.transforms.transforms import _apply_to_composite
from torchrl.envs.utils import check_env_specs, step_mdp
from codart.utility.directory_utils import update_understand_database
from codart.refactorings.handler import RefactoringManager, RefactoringOperation
from codart.metrics.qmood import DesignQualityAttributes
from multiprocessing import Process, Array
import pandas as pd
import os
from codart.learner.sbr_initializer.utils.utility import logger, config
from codart.learner.sbr_initializer.smell import SmellInitialization
from multiprocessing import Process, Array
import io
from datetime import datetime
from minio import Minio
from typing import Dict, Any


class RefactoringSequenceEnvironment(EnvBase):
    metadata = {}
    batch_locked = False

    def __init__(
        self,
        udb_path: str = "/home/y/jflex/jflex.und",
        n_obj: int = 8,
        lower_band: int = 1,
        upper_bound: int = 50,
        population_size: int = 100,
        device: Optional[str] = None,
        seed=None,
        project_name: str = "",
    ):
        super().__init__(device=device, batch_size=[])
        self.project_name = project_name
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.udb_path = udb_path
        self.n_obj = n_obj
        self.generator = SmellInitialization(
            udb_path=udb_path,
            n_obj=n_obj,
            lower_band=lower_band,
            upper_band=upper_bound,
            population_size=population_size,
        )
        self._make_spec(action=self.generator.generate_an_action())
        if seed is None:
            seed = torch.empty((), dtype=torch.int64).random_().item()
        self.set_seed(seed)

    _reset = EnvBase._reset
    _step = EnvBase._step
    _set_seed = EnvBase._set_seed

    def _set_seed(self, seed: Optional[int]):
        rng = torch.manual_seed(seed)
        self.rng = rng

    def _step(self, action: RefactoringOperation):
        action.execute()
        update_understand_database(udb_path=self.udb_path)
        reward = self.reward()
        done = torch.zeros_like(reward, dtype=torch.bool)
        out = TensorDict(
            {
                "refactoring": action.get_refactoring().name,
                "params": action.get_refactoring().params,
                "reward": reward.view(-1, 1),
                "done": done.view(-1, 1),
            },
            action.shape,
        )
        return out

    def _reset(self, action: RefactoringOperation):
        if action is None or action.is_empty():
            action = self.generator.generate_an_action()
        update_understand_database(udb_path=self.udb_path)
        out = TensorDict(
            {
                "refactoring": action.get_refactoring().name,
                "params": action.get_refactoring().params,
                # "done": torch.zeros(action.shape, dtype=torch.bool, device=self.device),
            },
            batch_size=action.shape,
        )
        return out

    def _make_spec(self, action: RefactoringOperation):
        self.observation_spec = CompositeSpec(
            refactoring=BoundedTensorSpec(
                low=0,
                high=5.0,
                dtype=torch.float32,
            ),
            params=self.make_composite_from_td(action),
        )
        self.state_spec = self.observation_spec.clone()
        self.action_spec = BoundedTensorSpec(
            low=0,
            high=1000,
            dtype=torch.float32,
        )
        self.reward_spec = UnboundedContinuousTensorSpec(
            shape=(*action.get_refactoring().shape, 1)
        )

    def make_composite_from_td(self, action: RefactoringOperation):
        composite = CompositeSpec(
            {
                key: (
                    self.make_composite_from_td(action)
                    if isinstance(tensor, TensorDictBase)
                    else UnboundedContinuousTensorSpec(
                        dtype=tensor.dtype, device=tensor.device, shape=tensor.shape
                    )
                )
                for key, tensor in action.get_refactoring().params.items()
            },
            shape=action.shape,
        )
        return composite

    def reward_function(self):
        return np.array(self.calculate_metrics(), dtype=float)

    def calculate_metrics(self):
        objective_values = []
        arr = Array("d", range(self.n_obj))
        qmood_quality_attributes = DesignQualityAttributes(udb_path=self.udb_path)
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
                        self.udb_path,
                        arr,
                    ),
                )
                p3 = Process(
                    target=self.calc_modularity_objective,
                    args=(
                        self.udb_path,
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
        return objective_values

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

    def log_design_metrics(self, design_metrics: Dict[str, Any]):
        """
        Log design metrics to MinIO storage.
        """
        try:
            if not self.project_name:
                logger.warning("Project name not set, using 'unknown_project'")
                self.project_name = "unknown_project"

            # Create DataFrame from metrics
            df_design_metrics = pd.DataFrame(data=design_metrics)

            # Generate timestamp for the file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Construct the object path in MinIO
            metrics_path = (
                f"{self.project_name}/design_metrics/design_metrics_log_{timestamp}.csv"
            )

            # Try to load existing metrics file if it exists
            try:
                existing_data = self.minio_client.get_object(
                    self.metrics_bucket,
                    f"{self.project_name}/design_metrics/latest.csv",
                )
                df_existing = pd.read_csv(existing_data)
                df_result = pd.concat(
                    [df_existing, df_design_metrics], ignore_index=True
                )
            except Exception as e:
                print(e)
                df_result = df_design_metrics

            # Convert DataFrame to CSV in memory
            csv_buffer = io.StringIO()
            df_result.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            csv_data = csv_buffer.getvalue()

            # Save timestamped version
            self.minio_client.put_object(
                self.metrics_bucket,
                metrics_path,
                data=io.BytesIO(csv_data.encode()),
                length=len(csv_data),
            )

            # Also save as latest version
            self.minio_client.put_object(
                self.metrics_bucket,
                f"{self.project_name}/design_metrics/latest.csv",
                data=io.BytesIO(csv_data.encode()),
                length=len(csv_data),
            )

            # Save metrics metadata
            metadata = {
                "timestamp": timestamp,
                "project_name": self.project_name,
                "metrics_count": len(design_metrics),
                "total_records": len(df_result),
            }

            metadata_buffer = io.BytesIO(str(metadata).encode())
            self.minio_client.put_object(
                self.metrics_bucket,
                f"{self.project_name}/design_metrics/metadata.json",
                data=metadata_buffer,
                length=len(str(metadata)),
            )

            logger.info(f"Design metrics saved to MinIO: {metrics_path}")

        except Exception as e:
            logger.error(
                f"Error saving design metrics to MinIO: {str(e)}", exc_info=True
            )
            raise


# env = RefactoringSequenceEnvironment()
# env.to(env.device)
# check_env_specs(env)
#
# print("observation_spec:", env.observation_spec)
# print("state_spec:", env.state_spec)
# print("reward_spec:", env.reward_spec)
