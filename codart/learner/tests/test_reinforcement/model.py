import torch
import torch.nn as nn
from tensordict.nn import TensorDictModule
from tensordict.nn.distributions import NormalParamExtractor
from torchrl.modules import ProbabilisticActor, TanhNormal
from torchrl.data import CompositeSpec
from torchrl.data.tensor_specs import UnboundedContinuousTensorSpec
from torch.distributions import Categorical
from codart.learner.sbr_initializer.utils.utility import config, logger


class RefactoringPolicyNetwork(nn.Module):
    """
    Policy network for refactoring sequence optimization.
    Handles discrete refactoring selection with continuous parameters.
    """

    def __init__(self,
                 observation_size: int = 3,  # refactoring, refactoring_type, success
                 n_refactoring_types: int = 6,  # number of refactoring types
                 hidden_size: int = None,
                 action_size: int = 1):
        super().__init__()

        # Get configuration from config
        if hidden_size is None:
            hidden_size = config.getint("PPO", "num_cells")

        depth = config.getint("PPO", "depth")

        # Create layers based on depth
        layers = []
        input_size = observation_size

        for i in range(depth):
            layers.extend([
                nn.Linear(input_size, hidden_size),
                nn.Tanh(),
            ])
            input_size = hidden_size

        self.feature_extractor = nn.Sequential(*layers)

        # Policy head for refactoring type selection (discrete)
        self.refactoring_policy = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, n_refactoring_types),
        )

        # Continuous action parameters - IMPORTANT: Use 'loc' and 'scale' for TanhNormal
        self.action_loc = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, action_size),
        )

        self.action_scale = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, action_size),
            nn.Softplus(),  # Ensure positive scale
        )

    def forward(self, refactoring, refactoring_type, success):
        """
        Forward pass that accepts individual tensors (TensorDictModule handles the extraction)
        """
        # Debug logging
        logger.debug(f"Policy network input shapes - refactoring: {refactoring.shape}, "
                     f"refactoring_type: {refactoring_type.shape}, success: {success.shape}")

        # Ensure tensors have the right shape and dtype
        refactoring = refactoring.float().unsqueeze(-1) if refactoring.dim() == 1 else refactoring.float()
        refactoring_type = refactoring_type.float().unsqueeze(
            -1) if refactoring_type.dim() == 1 else refactoring_type.float()
        success = success.float().unsqueeze(-1) if success.dim() == 1 else success.float()

        # Concatenate input features
        observation = torch.cat([refactoring, refactoring_type, success], dim=-1)
        logger.debug(f"Concatenated observation shape: {observation.shape}")

        features = self.feature_extractor(observation)

        # Get refactoring type logits
        refactoring_logits = self.refactoring_policy(features)

        # Get continuous action parameters - FIXED: Use 'loc' and 'scale'
        action_loc = self.action_loc(features)
        action_scale = self.action_scale(features) + 1e-6  # Add small epsilon for numerical stability

        logger.debug(f"Output shapes - refactoring_logits: {refactoring_logits.shape}, "
                     f"action_loc: {action_loc.shape}, action_scale: {action_scale.shape}")

        return refactoring_logits, action_loc, action_scale


class RefactoringValueNetwork(nn.Module):
    """
    Value network for multi-objective rewards estimation.
    """

    def __init__(self,
                 observation_size: int = 3,
                 n_objectives: int = 8,
                 hidden_size: int = None):
        super().__init__()

        # Get configuration from config
        if hidden_size is None:
            hidden_size = config.getint("PPO", "num_cells")

        depth = config.getint("PPO", "depth")

        # Create layers based on depth
        layers = []
        input_size = observation_size

        for i in range(depth):
            layers.extend([
                nn.Linear(input_size, hidden_size),
                nn.Tanh(),
            ])
            input_size = hidden_size

        self.feature_extractor = nn.Sequential(*layers)

        # Value head for multi-objective rewards
        self.value_head = nn.Linear(hidden_size, n_objectives)

    def forward(self, refactoring, refactoring_type, success):
        """
        Forward pass that accepts individual tensors (TensorDictModule handles the extraction)
        """
        # Debug logging
        logger.debug(f"Value network input shapes - refactoring: {refactoring.shape}, "
                     f"refactoring_type: {refactoring_type.shape}, success: {success.shape}")

        # Ensure tensors have the right shape and dtype
        refactoring = refactoring.float().unsqueeze(-1) if refactoring.dim() == 1 else refactoring.float()
        refactoring_type = refactoring_type.float().unsqueeze(
            -1) if refactoring_type.dim() == 1 else refactoring_type.float()
        success = success.float().unsqueeze(-1) if success.dim() == 1 else success.float()

        # Concatenate input features
        observation = torch.cat([refactoring, refactoring_type, success], dim=-1)
        features = self.feature_extractor(observation)
        values = self.value_head(features)

        logger.debug(f"Value output shape: {values.shape}")
        return values


def create_policy_module(env):
    """Create TensorDictModule for the policy network"""

    # Create policy network
    policy_net = RefactoringPolicyNetwork(
        observation_size=3,  # Based on your observation spec
        n_refactoring_types=6,
        action_size=1
    )

    # FIXED: Use correct output keys for TanhNormal distribution
    policy_module = TensorDictModule(
        policy_net,
        in_keys=["refactoring", "refactoring_type", "success"],
        out_keys=["refactoring_logits", "loc", "scale"]  # Changed from action_mean/action_std to loc/scale
    )

    logger.info("Policy module created successfully")
    return policy_module


def create_value_module(env):
    """Create value network for multi-objective rewards"""

    value_net = RefactoringValueNetwork(
        observation_size=3,  # observation size
        n_objectives=env.n_obj  # multi-objective output
    )

    value_module = TensorDictModule(
        value_net,
        in_keys=["refactoring", "refactoring_type", "success"],
        out_keys=["state_value"]
    )

    logger.info("Value module created successfully")
    return value_module


def create_probabilistic_actor(policy_module, env):
    """Create probabilistic actor for action sampling"""

    # FIXED: Use correct in_keys that match TanhNormal parameter names
    actor = ProbabilisticActor(
        module=policy_module,
        spec=env.action_spec,
        in_keys=["loc", "scale"],  # Changed from action_mean/action_std to loc/scale
        out_keys=["action"],
        distribution_class=TanhNormal,
        distribution_kwargs={
            "low": torch.tensor(-1.0),
            "high": torch.tensor(1.0),
        },
        return_log_prob=True,
        log_prob_key="sample_log_prob",
    )

    logger.info("Probabilistic actor created successfully")
    return actor