from collections import defaultdict
from typing import Optional
import numpy as np
import torch
import tqdm
from tensordict import TensorDict, TensorDictBase
from tensordict.nn import TensorDictModule
from torch import nn
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
from torchrl.data import Bounded, BoundedTensorSpec, CompositeSpec, UnboundedContinuousTensorSpec


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
            version_id: str = "",
            project_path: str = ""
    ):
        super().__init__(device=device, batch_size=[])
        self.project_name = project_name
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.udb_path = udb_path
        self.n_obj = n_obj
        self.evaluate_in_parallel = False  # Default value for evaluate_in_parallel
        self.verbose_design_metrics = False  # Default value for verbose_design_metrics
        self.generator = SmellInitialization(
            udb_path=udb_path,
            project_name=project_name,
            version_id=version_id,
            n_obj=n_obj,
            lower_band=lower_band,
            upper_band=upper_bound,
            population_size=population_size,
            project_path=project_path
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

    def _create_refactoring_from_tensordict(self, tensordict):
        """
        Convert a TensorDict to a RefactoringOperation.
        This is needed when TorchRL passes a TensorDict to the step method.

        Args:
            tensordict: The TensorDict containing action information

        Returns:
            A RefactoringOperation object
        """
        from codart.refactorings.abstraction import EmptyRefactoring
        from codart.refactorings.handler import (
            ExtractClass, MoveClass, PullupMethod, PushdownMethod, MoveMethod, ExtractMethod
        )

        try:
            # Extract relevant information from the tensordict
            refactoring_name = None
            params = {}

            if hasattr(tensordict, "get"):
                # Try to get refactoring name and params
                if "refactoring" in tensordict:
                    refactoring_name = tensordict.get("refactoring")

                if "params" in tensordict:
                    params = tensordict.get("params")

                # If tensordict has 'action' that is already a RefactoringOperation, use it
                if tensordict.get("action", None) is not None and isinstance(tensordict.get("action"),
                                                                             RefactoringOperation):
                    return tensordict.get("action")

            # Generate an action using the generator if we can't extract valid info from tensordict
            # This allows TorchRL's check_env_specs to work, which calls step with an empty tensordict
            action = self.generator.generate_an_action()
            logger.debug(f"Generated new action for TensorDict: {action.get_refactoring().name}")
            return action

        except Exception as e:
            logger.error(f"Error creating refactoring from tensordict: {e}", exc_info=True)
            # Return an empty refactoring as fallback
            return EmptyRefactoring()

    def _extract_param_value(self, params, key, default):
        """
        Helper method to extract parameter values from the nested structure.

        Args:
            params: Dictionary of parameters
            key: Parameter key to extract
            default: Default value if parameter not found

        Returns:
            The extracted parameter value or default
        """
        try:
            if key in params:
                # Handle the nested structure {"key": {"value": actual_value}}
                if isinstance(params[key], dict) and "value" in params[key]:
                    value = params[key]["value"]

                    # Convert string representations of lists back to actual lists
                    if default is not None and isinstance(default, list) and isinstance(value, str):
                        # Check if the string looks like a list representation
                        if value.startswith("[") and value.endswith("]"):
                            try:
                                # Convert string representation of list to actual list
                                import ast
                                return ast.literal_eval(value)
                            except:
                                # If conversion fails, return empty list
                                return []

                    return value
                else:
                    return params[key]
            return default
        except Exception as e:
            logger.warning(f"Error extracting parameter '{key}': {e}")
            return default

    def _step(self, tensordict_or_action):
        """
        Execute a step in the environment.

        Args:
            tensordict_or_action: Either a TensorDict or a RefactoringOperation

        Returns:
            TensorDict with the next state, reward, and done flag
        """
        # Convert TensorDict to RefactoringOperation if needed
        if isinstance(tensordict_or_action, (TensorDict, TensorDictBase)):
            action = self._create_refactoring_from_tensordict(tensordict_or_action)
        else:
            # It's already a RefactoringOperation
            action = tensordict_or_action

        try:
            # Add debug logging
            logger.debug(f"Executing refactoring: {action.get_refactoring().name}")
            success = action.execute()

            # Handle None return value
            if success is None:
                logger.error(f"Refactoring returned None for success status")
                success = False
        except Exception as e:
            logger.error(f"Error executing refactoring: {e}", exc_info=True)
            success = False

            # Only update the understand database if refactoring was successful
        if success:
            update_understand_database(udb_path=self.udb_path)
            reward = self.reward()

            # Make sure reward has correct shape
            if isinstance(reward, np.ndarray):
                # Log the shape before conversion
                logger.debug(f"Reward shape before conversion: {reward.shape}")

                # Convert numpy array to tensor with correct shape
                # This is crucial - reshape to [batch_size, n_obj]
                reward = torch.tensor(reward, dtype=torch.float32, device=self.device)

                # Ensure the reward has shape [batch_size, n_obj]
                if reward.shape != (action.shape[0], self.n_obj):
                    logger.warning(f"Reshaping reward from {reward.shape} to [{action.shape[0]}, {self.n_obj}]")
                    reward = reward.reshape(action.shape[0], self.n_obj)
        else:
            # If refactoring failed, provide a negative reward with correct shape
            # The key fix - ensure reward has correct shape [batch_size, n_obj]
            reward = torch.tensor([[-1.0] * self.n_obj] * action.shape[0],
                                  dtype=torch.float32, device=self.device)
            logger.debug(f"Created failure reward with shape {reward.shape}")

            # Set done flag
        done = torch.zeros_like(reward, dtype=torch.bool)

        # Create the output TensorDict with the results
        out = TensorDict(
            {
                "refactoring": action.get_refactoring().name,
                "params": action.get_refactoring().params,
                "reward": reward,  # This should now have correct shape
                "done": done.view(-1, 1),
                "success": torch.tensor([success], dtype=torch.bool, device=self.device),
            },
            action.shape,
        )
        return out

    def _reset(self, action: RefactoringOperation = None):
        if action is None:
            action = self.generator.generate_an_action()
        if action is not None and action.is_empty():
            action = self.generator.generate_an_action()

        update_understand_database(udb_path=self.udb_path)
        out = TensorDict(
            {
                "refactoring": action.get_refactoring().name,
                "params": action.get_refactoring().params,
            },
            batch_size=action.shape,
        )
        return out

    def _make_spec(self, action: RefactoringOperation):
        if action is None or action.is_empty():
            shape = (1,)
        else:
            shape = action.shape

        # Update to use low/high instead of minimum/maximum
        self.observation_spec = CompositeSpec(
            refactoring=Bounded(
                shape=shape,
                low=0,  # Use low instead of minimum
                high=5.0,  # Use high instead of maximum
                dtype=torch.float32,
            ),
            params=self.make_composite_from_td(action),
        )
        self.state_spec = self.observation_spec.clone()

        # Update action_spec
        self.action_spec = Bounded(
            shape=shape,
            low=0,  # Use low instead of minimum
            high=1000,  # Use high instead of maximum
            dtype=torch.float32,
        )

        # Make sure reward spec has consistent shape
        reward_shape = (*shape, 1)
        self.reward_spec = UnboundedContinuousTensorSpec(shape=reward_shape)

    def make_composite_from_td(self, action: RefactoringOperation):
        """
        Create a composite spec from a refactoring operation's parameters.

        This handles the nested dictionary structure in RefactoringModel.params
        where each parameter is a dict with a 'value' key containing a string.

        Args:
            action: A RefactoringOperation instance

        Returns:
            A CompositeSpec representing the structure of the action's parameters
        """
        # Handle None or empty actions
        if action is None or action.is_empty():
            return CompositeSpec(shape=(1,))

        try:
            # Get the refactoring model
            refactoring_model = action.get_refactoring()
            params = refactoring_model.params

            # Create a CompositeSpec with UnboundedContinuousTensorSpec for each parameter
            param_specs = {}
            for key, param_dict in params.items():
                # Each param_dict is expected to be {'value': str_value}
                if isinstance(param_dict, dict) and 'value' in param_dict:
                    # Create a spec for string values
                    param_specs[key] = UnboundedContinuousTensorSpec(
                        shape=(1,),
                        dtype=torch.float32,
                        device=self.device
                    )

            # Create the composite spec with all parameter specs
            composite = CompositeSpec(
                param_specs,
                shape=action.shape,
            )
            return composite
        except Exception as e:
            # Fallback to a basic composite spec if there's an error
            print(f"Warning: Error in make_composite_from_td: {e}")
            return CompositeSpec(shape=action.shape)

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

        objective_values = [[-1 * i for i in arr]]
        logger.info(f"Objective values: {[i for i in arr]}")
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
            if not hasattr(self, 'minio_client') or not hasattr(self, 'metrics_bucket'):
                logger.warning("MinIO client or metrics bucket not configured, skipping metrics logging")
                return

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

# env = RefactoringSequenceEnvironment()
# env.to(env.device)
# check_env_specs(env)
#
# print("observation_spec:", env.observation_spec)
# print("state_spec:", env.state_spec)
# print("reward_spec:", env.reward_spec)
