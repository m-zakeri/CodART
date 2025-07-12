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
        super().__init__(device=device, batch_size=[1])
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

    def _handle_refactoring_result(self, refactoring_result):
        """
        Safely handle refactoring results to prevent None returns
        """
        if refactoring_result is None:
            logger.warning("Refactoring returned None, treating as failure")
            return False
        elif isinstance(refactoring_result, bool):
            return refactoring_result
        else:
            # Handle other types (like strings, integers)
            success = bool(refactoring_result)
            logger.warning(f"Refactoring returned non-boolean: {refactoring_result}, converted to: {success}")
            return success

    def _create_consistent_tensordict(self, action, success, reward=None, is_done=False):
        """
        Create consistent TensorDict structure - Minimalist version to avoid spec conflicts
        """
        # Get refactoring info
        if hasattr(action, 'get_refactoring'):
            refactoring_name = action.get_refactoring().name
        else:
            refactoring_name = "Unknown"

        # Convert refactoring name to tensor (you can map names to numbers)
        refactoring_mapping = {
            "Move Method": 0.0,
            "Extract Class": 1.0,
            "Extract Method": 2.0,
            "Pull Up Method": 3.0,
            "Push Down Method": 4.0,
            "Move Class": 5.0,
            "Unknown": 0.0
        }
        refactoring_tensor = torch.tensor([refactoring_mapping.get(refactoring_name, 0.0)],
                                          dtype=torch.float32, device=self.device)

        # Create reward if not provided
        if reward is None:
            if success:
                try:
                    reward = self.reward()
                    if isinstance(reward, np.ndarray):
                        reward = torch.tensor(reward, dtype=torch.float32, device=self.device)
                        # Ensure reward has correct shape [batch_size, n_obj]
                        reward = reward.reshape(1, self.n_obj)
                except Exception as e:
                    logger.warning(f"Error calculating reward: {e}")
                    reward = torch.full((1, self.n_obj), 0.0, dtype=torch.float32, device=self.device)
            else:
                # Create failure reward with shape [1, n_obj]
                reward = torch.full((1, self.n_obj), -1.0, dtype=torch.float32, device=self.device)

        # Create minimalist TensorDict with only essential fields matching observation_spec
        base_dict = {
            "refactoring": refactoring_tensor,
            "refactoring_type": refactoring_tensor.clone(),
            "success": torch.tensor([success], dtype=torch.bool, device=self.device),
            # Add reward and done only in step, not in reset
        }

        # Add reward and done only for step operations
        if reward is not None:
            base_dict["reward"] = reward
            base_dict["done"] = torch.tensor([is_done], dtype=torch.bool, device=self.device)

        return TensorDict(base_dict, batch_size=[1])

    def _step(self, tensordict_or_action):
        """
        Execute a step in the environment with minimalist TensorDict structure.
        """
        logger.debug(f"Starting _step with batch_size: {self.batch_size}")

        # Convert TensorDict to RefactoringOperation if needed
        if isinstance(tensordict_or_action, (TensorDict, TensorDictBase)):
            action = self._create_refactoring_from_tensordict(tensordict_or_action)
        else:
            action = tensordict_or_action

        try:
            logger.debug(f"Executing refactoring: {action.get_refactoring().name}")
            raw_success = action.execute()
            success = self._handle_refactoring_result(raw_success)

        except Exception as e:
            logger.error(f"Error executing refactoring: {e}", exc_info=True)
            success = False

        # Only update the understand database if refactoring was successful
        if success:
            try:
                update_understand_database(udb_path=self.udb_path)
            except Exception as e:
                logger.error(f"Error updating understand database: {e}")

        # Calculate reward
        if success:
            try:
                reward = self.reward()
                if isinstance(reward, np.ndarray):
                    reward = torch.tensor(reward, dtype=torch.float32, device=self.device)
                    reward = reward.reshape(1, self.n_obj)
            except Exception as e:
                logger.error(f"Error calculating reward: {e}")
                reward = torch.full((1, self.n_obj), 0.0, dtype=torch.float32, device=self.device)
        else:
            reward = torch.full((1, self.n_obj), -1.0, dtype=torch.float32, device=self.device)

        # Create minimalist output
        out = TensorDict({
            "refactoring": torch.tensor([self._get_refactoring_id(action)], dtype=torch.float32, device=self.device),
            "refactoring_type": torch.tensor([self._get_refactoring_id(action)], dtype=torch.float32,
                                             device=self.device),
            "success": torch.tensor([success], dtype=torch.bool, device=self.device),
            "reward": reward,
            "done": torch.tensor([False], dtype=torch.bool, device=self.device),  # Episode continues
        }, batch_size=[1])

        logger.debug(f"Step output keys: {out.keys()}")
        return out

    def _reset(self, tensordict=None):
        """
        Reset the environment with minimalist TensorDict structure
        """
        # Generate an action
        action = self.generator.generate_an_action()
        if action is None or action.is_empty():
            action = self.generator.generate_an_action()

        try:
            update_understand_database(udb_path=self.udb_path)
        except Exception as e:
            logger.error(f"Error updating understand database in reset: {e}")

        # Create minimalist reset output (no reward or done in reset)
        out = TensorDict({
            "refactoring": torch.tensor([self._get_refactoring_id(action)], dtype=torch.float32, device=self.device),
            "refactoring_type": torch.tensor([self._get_refactoring_id(action)], dtype=torch.float32,
                                             device=self.device),
            "success": torch.tensor([True], dtype=torch.bool, device=self.device),  # Reset is always successful
        }, batch_size=[1])

        logger.debug(f"Reset output keys: {out.keys()}")
        return out

    def _get_refactoring_id(self, action):
        """Helper method to get refactoring ID"""
        if hasattr(action, 'get_refactoring'):
            refactoring_name = action.get_refactoring().name
        else:
            refactoring_name = "Unknown"

        refactoring_mapping = {
            "Move Method": 0.0,
            "Extract Class": 1.0,
            "Extract Method": 2.0,
            "Pull Up Method": 3.0,
            "Push Down Method": 4.0,
            "Move Class": 5.0,
            "Unknown": 0.0
        }
        return refactoring_mapping.get(refactoring_name, 0.0)

    def _make_spec(self, action: RefactoringOperation):
        """
        Create consistent specs that match the TensorDict structure - Fixed version
        """
        print(f"self.batch_size: {self.batch_size}")

        # Create observation spec that matches _step and _reset output
        # Use only the essential keys to avoid collisions
        self.observation_spec = CompositeSpec({
            "refactoring": UnboundedContinuousTensorSpec(
                shape=self.batch_size,
                dtype=torch.float32,
                device=self.device
            ),
            "refactoring_type": UnboundedContinuousTensorSpec(
                shape=self.batch_size,
                dtype=torch.float32,
                device=self.device
            ),
            "success": BoundedTensorSpec(
                shape=self.batch_size,
                low=0,
                high=1,
                dtype=torch.bool,
                device=self.device
            ),
        }, shape=self.batch_size)

        # Create separate state spec (can be same as observation for simplicity)
        self.state_spec = self.observation_spec.clone()

        # Create action spec
        self.action_spec = UnboundedContinuousTensorSpec(
            shape=self.batch_size,
            dtype=torch.float32,
            device=self.device
        )

        # Create reward spec
        self.reward_spec = UnboundedContinuousTensorSpec(
            shape=(*self.batch_size, self.n_obj),
            dtype=torch.float32,
            device=self.device
        )

    def reward(self):
        """Get reward as properly shaped tensor"""
        try:
            reward_array = self.reward_function()
            if isinstance(reward_array, np.ndarray):
                # Ensure it's the right shape [batch_size, n_obj]
                if len(reward_array.shape) == 2 and reward_array.shape[0] == 1:
                    return reward_array
                elif len(reward_array.shape) == 1:
                    return reward_array.reshape(1, -1)
                else:
                    # Flatten and reshape if needed
                    return reward_array.flatten().reshape(1, -1)[:, :self.n_obj]
            else:
                # Convert to numpy first
                reward_array = np.array(reward_array, dtype=float)
                return reward_array.reshape(1, -1)[:, :self.n_obj]
        except Exception as e:
            logger.error(f"Error in reward calculation: {e}")
            # Return default negative reward
            return np.full((1, self.n_obj), -1.0)

    def make_composite_from_td(self, action: RefactoringOperation):
        """
        Create a composite spec from a refactoring operation's parameters.
        """
        # Handle None or empty actions
        if action is None or action.is_empty():
            return CompositeSpec(shape=self.batch_size)

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
                        shape=self.batch_size,
                        dtype=torch.float32,
                        device=self.device
                    )

            # Create the composite spec with all parameter specs
            composite = CompositeSpec(
                param_specs,
                shape=self.batch_size,
            )
            return composite
        except Exception as e:
            # Fallback to a basic composite spec if there's an error
            print(f"Warning: Error in make_composite_from_td: {e}")
            return CompositeSpec(shape=self.batch_size)

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