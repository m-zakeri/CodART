import torch
import torch.nn as nn
from tensordict.nn import TensorDictModule
from tensordict.nn.distributions import NormalParamExtractor
from torchrl.modules import ProbabilisticActor, TanhNormal
from torchrl.data import CompositeSpec, UnboundedContinuousTensorSpec
from torch.distributions import Categorical
from codart.learner.sbr_initializer.utils.utility import config


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

        # Continuous action parameters (mean and std)
        self.action_mean = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, action_size),
        )

        self.action_std = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, action_size),
            nn.Softplus(),  # Ensure positive std
        )

    def forward(self, observation):
        features = self.feature_extractor(observation)

        # Get refactoring type logits
        refactoring_logits = self.refactoring_policy(features)

        # Get continuous action parameters
        action_mean = self.action_mean(features)
        action_std = self.action_std(features) + 1e-6  # Add small epsilon for numerical stability

        return {
            'refactoring_logits': refactoring_logits,
            'action_mean': action_mean,
            'action_std': action_std
        }


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

    def forward(self, observation):
        features = self.feature_extractor(observation)
        values = self.value_head(features)
        return values


def create_policy_module(env):
    """Create TensorDictModule for the policy network"""

    # Create policy network
    policy_net = RefactoringPolicyNetwork(
        observation_size=3,  # Based on your observation spec
        n_refactoring_types=6,
        action_size=1
    )

    # Wrap in TensorDictModule
    policy_module = TensorDictModule(
        policy_net,
        in_keys=["refactoring", "refactoring_type", "success"],
        out_keys=["refactoring_logits", "action_mean", "action_std"]
    )

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

    return value_module


def create_probabilistic_actor(policy_module, env):
    """Create probabilistic actor for action sampling"""

    actor = ProbabilisticActor(
        module=policy_module,
        spec=env.action_spec,
        in_keys=["action_mean", "action_std"],
        out_keys=["action"],
        distribution_class=TanhNormal,
        distribution_kwargs={
            "low": torch.tensor(-1.0),
            "high": torch.tensor(1.0),
        },
        return_log_prob=True,
        log_prob_key="sample_log_prob",
    )

    return actor