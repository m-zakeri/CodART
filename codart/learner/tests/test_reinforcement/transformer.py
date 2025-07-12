import torch
import numpy as np
from tensordict import TensorDict
from torchrl.envs import Transform
from torchrl.data import CompositeSpec, UnboundedContinuousTensorSpec, BoundedTensorSpec
from codart.learner.sbr_initializer.utils.utility import logger


class RefactoringTransform(Transform):
    """
    Transform for refactoring environment to ensure consistent tensor shapes and types.
    """

    def __init__(self):
        super().__init__()
        self.reward_accumulator = 0.0
        self.step_count = 0

    def _apply_transform(self, tensordict: TensorDict) -> TensorDict:
        """Apply transform to tensordict"""

        # Ensure all tensors have consistent shapes and types
        for key, value in tensordict.items():
            if torch.is_tensor(value):
                # Ensure float32 dtype for continuous values
                if key in ['refactoring', 'refactoring_type', 'reward']:
                    tensordict[key] = value.float()
                # Ensure bool dtype for boolean values
                elif key in ['success', 'done']:
                    tensordict[key] = value.bool()

                # Ensure correct batch dimensions
                if value.ndim == 0:  # scalar
                    tensordict[key] = value.unsqueeze(0)
                elif value.ndim == 1 and key == 'reward':
                    # Ensure reward has shape [batch_size, n_objectives]
                    if value.shape[0] > 1:
                        tensordict[key] = value.unsqueeze(0)

        return tensordict

    def _reset(self, tensordict: TensorDict, tensordict_reset: TensorDict) -> TensorDict:
        """Reset transform state"""
        self.reward_accumulator = 0.0
        self.step_count = 0

        # Apply transform to reset tensordict
        transformed = self._apply_transform(tensordict_reset)

        # Add step count
        transformed['step_count'] = torch.tensor([0], dtype=torch.long)

        return transformed

    def _step(self, tensordict: TensorDict, next_tensordict: TensorDict) -> TensorDict:
        """Transform step output"""
        self.step_count += 1

        # Apply transform to next tensordict
        transformed = self._apply_transform(next_tensordict)

        # Add step count
        transformed['step_count'] = torch.tensor([self.step_count], dtype=torch.long)

        # Accumulate reward
        if 'reward' in transformed:
            reward = transformed['reward']
            if torch.is_tensor(reward):
                self.reward_accumulator += reward.mean().item()
            else:
                self.reward_accumulator += float(reward)

        # Add accumulated reward
        transformed['episode_reward'] = torch.tensor([self.reward_accumulator], dtype=torch.float32)

        return transformed

    def transform_observation_spec(self, observation_spec: CompositeSpec) -> CompositeSpec:
        """Transform observation spec to include additional keys"""
        new_spec = observation_spec.clone()

        # Add step count spec
        new_spec['step_count'] = BoundedTensorSpec(
            shape=torch.Size([1]),
            low=0,
            high=100000,  # Reasonable maximum step count
            dtype=torch.long
        )

        # Add episode reward spec
        new_spec['episode_reward'] = UnboundedContinuousTensorSpec(
            shape=torch.Size([1]),
            dtype=torch.float32
        )

        return new_spec

    def transform_reward_spec(self, reward_spec):
        """Transform reward spec if needed"""
        return reward_spec

    def transform_input_spec(self, input_spec):
        """Transform input spec if needed"""
        return input_spec


class RewardNormalizationTransform(Transform):
    """
    Transform to normalize multi-objective rewards.
    """

    def __init__(self, n_objectives: int = 8, running_mean_decay: float = 0.99):
        super().__init__()
        self.n_objectives = n_objectives
        self.running_mean_decay = running_mean_decay

        # Running statistics for normalization
        self.running_mean = torch.zeros(n_objectives)
        self.running_var = torch.ones(n_objectives)
        self.count = 0

    def _apply_transform(self, tensordict: TensorDict) -> TensorDict:
        """Apply reward normalization"""
        if 'reward' in tensordict:
            reward = tensordict['reward']

            if torch.is_tensor(reward) and reward.numel() >= self.n_objectives:
                # Reshape reward to [batch_size, n_objectives]
                if reward.ndim == 1:
                    reward = reward.unsqueeze(0)

                # Update running statistics
                self._update_running_stats(reward)

                # Normalize reward
                normalized_reward = (reward - self.running_mean) / (torch.sqrt(self.running_var) + 1e-8)
                tensordict['reward'] = normalized_reward

                # Store original reward for analysis
                tensordict['reward_raw'] = reward

        return tensordict

    def _update_running_stats(self, reward: torch.Tensor):
        """Update running mean and variance"""
        self.count += 1

        # Convert to same device as running stats
        reward = reward.to(self.running_mean.device)

        if self.count == 1:
            self.running_mean = reward.mean(dim=0)
            self.running_var = reward.var(dim=0, unbiased=False)
        else:
            # Exponential moving average
            batch_mean = reward.mean(dim=0)
            batch_var = reward.var(dim=0, unbiased=False)

            self.running_mean = (
                    self.running_mean_decay * self.running_mean +
                    (1 - self.running_mean_decay) * batch_mean
            )

            self.running_var = (
                    self.running_mean_decay * self.running_var +
                    (1 - self.running_mean_decay) * batch_var
            )

    def _reset(self, tensordict: TensorDict, tensordict_reset: TensorDict) -> TensorDict:
        """Reset transform"""
        return self._apply_transform(tensordict_reset)

    def _step(self, tensordict: TensorDict, next_tensordict: TensorDict) -> TensorDict:
        """Transform step output"""
        return self._apply_transform(next_tensordict)


class ObservationNormalizationTransform(Transform):
    """
    Transform to normalize observations.
    """

    def __init__(self, observation_keys: list = None):
        super().__init__()
        self.observation_keys = observation_keys or ['refactoring', 'refactoring_type']
        self.running_mean = {}
        self.running_var = {}
        self.count = 0

    def _apply_transform(self, tensordict: TensorDict) -> TensorDict:
        """Apply observation normalization"""
        self.count += 1

        for key in self.observation_keys:
            if key in tensordict:
                obs = tensordict[key]

                if torch.is_tensor(obs):
                    # Initialize running stats if needed
                    if key not in self.running_mean:
                        self.running_mean[key] = obs.float().mean()
                        self.running_var[key] = obs.float().var() + 1e-8
                    else:
                        # Update running stats
                        obs_mean = obs.float().mean()
                        obs_var = obs.float().var() + 1e-8

                        decay = 0.99
                        self.running_mean[key] = (
                                decay * self.running_mean[key] +
                                (1 - decay) * obs_mean
                        )
                        self.running_var[key] = (
                                decay * self.running_var[key] +
                                (1 - decay) * obs_var
                        )

                    # Normalize observation
                    normalized_obs = (
                            (obs.float() - self.running_mean[key]) /
                            torch.sqrt(self.running_var[key])
                    )
                    tensordict[key] = normalized_obs

        return tensordict

    def _reset(self, tensordict: TensorDict, tensordict_reset: TensorDict) -> TensorDict:
        """Reset transform"""
        return self._apply_transform(tensordict_reset)

    def _step(self, tensordict: TensorDict, next_tensordict: TensorDict) -> TensorDict:
        """Transform step output"""
        return self._apply_transform(next_tensordict)


class RefactoringActionTransform(Transform):
    """
    Transform to handle refactoring action conversion.
    """

    def __init__(self):
        super().__init__()
        self.refactoring_types = [
            "Move Method", "Extract Class", "Extract Method",
            "Pull Up Method", "Push Down Method", "Move Class"
        ]

    def _apply_to_action(self, action_tensordict: TensorDict) -> TensorDict:
        """Convert continuous action to refactoring operation"""
        if 'action' in action_tensordict:
            action = action_tensordict['action']

            # Convert continuous action to discrete refactoring type
            if torch.is_tensor(action):
                # Map action to refactoring type index
                action_normalized = torch.clamp(action, -1, 1)
                action_scaled = (action_normalized + 1) / 2  # Scale to [0, 1]
                refactoring_idx = (action_scaled * len(self.refactoring_types)).long()
                refactoring_idx = torch.clamp(refactoring_idx, 0, len(self.refactoring_types) - 1)

                action_tensordict['refactoring_type_idx'] = refactoring_idx
                action_tensordict['refactoring_type_name'] = self.refactoring_types[refactoring_idx.item()]

        return action_tensordict

    def _reset(self, tensordict: TensorDict, tensordict_reset: TensorDict) -> TensorDict:
        """Reset transform"""
        return tensordict_reset

    def _step(self, tensordict: TensorDict, next_tensordict: TensorDict) -> TensorDict:
        """Transform step output"""
        return next_tensordict


def create_transform_stack(env, use_normalization: bool = True):
    """
    Create a stack of transforms for the refactoring environment.

    Args:
        env: The base environment
        use_normalization: Whether to use normalization transforms

    Returns:
        List of transforms to apply
    """
    transforms = []

    # Basic refactoring transform (always applied)
    transforms.append(RefactoringTransform())

    # Action transform for refactoring operations
    transforms.append(RefactoringActionTransform())

    if use_normalization:
        # Observation normalization
        transforms.append(ObservationNormalizationTransform())

        # Reward normalization for multi-objective optimization
        transforms.append(RewardNormalizationTransform(n_objectives=env.n_obj))

    return transforms