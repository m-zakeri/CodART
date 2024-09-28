import torch
import torch.nn as nn
from learner.sbr_initializer.smell import SmellInitialization
from learner.abstraction import TrainCodArt
from codart.refactorings.handler import RefactoringManager
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.optimize import minimize
from learner.sbr_initializer.problem import ProblemManyObjective


class AlphaZeroModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(AlphaZeroModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.policy_head = nn.Linear(128, output_size)
        self.value_head = nn.Linear(128, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        policy = self.policy_head(x)
        value = self.value_head(x)
        return policy, value


class TrainerImplement(TrainCodArt):

    def __init__(self, input_size, output_size):
        super(TrainerImplement, self).__init__(
            name="AlphaZero",
            num_episodes=2,
            randomly_ending_episode=0.1,
            model=AlphaZeroModel(input_size=input_size, output_size=output_size),
        )
        self.refactoring_manager = RefactoringManager()
        self.problem = ProblemManyObjective()
        self.algorithm = UNSGA3(self.problem)
        self.res = minimize(
            problem=self.problem,
            algorithm=self.algorithm,
            termination=("n_gen", 5),
            save_history=True,
            seed=42,
        )

    def start(self):
        st = SmellInitialization()
        st.generate_population()

    def get_state(self):
        pass

    def get_optimizer(self):
        pass

    def search(self, state):
        pass

    def action(self, action_probs=None, *args, **kwargs) -> bool:
        pass

    def reward_function(self, state, action):
        pass

    def save(self, file_path: str = "", *args, **kwargs) -> None:
        torch.save(self.model.state_dict(), file_path)

    def load(self, file_path: str = "", *args, **kwargs) -> None:
        self.model.load_state_dict(torch.load(file_path))
        self.model.eval()

    def get_output(self, input_data, *args, **kwargs) -> bool:
        with torch.no_grad():
            input_tensor = torch.FloatTensor(input_data)
            policy, _ = self.model(input_tensor)
            return policy.numpy()
