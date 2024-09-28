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
        # Retrieve the current state related to refactoring operations
        return self.refactoring_manager.list_operations()

    def get_optimizer(self):
        return optim.Adam(self.model.parameters(), lr=0.001)

    def search(self, state):
        # Use the model to predict actions based on the current state
        with torch.no_grad():
            input_tensor = torch.FloatTensor(state)
            policy, _ = self.model(input_tensor)
            return policy.numpy()

    def action(self, action_probs=None, *args, **kwargs) -> bool:
        if action_probs is None:
            raise ValueError("Action probabilities must be provided.")
        action = torch.multinomial(torch.softmax(torch.FloatTensor(action_probs), dim=0), 1)
        return action.item()  # Return the chosen action

    def reward_function(self, state, action):
        # Evaluate the reward based on the chosen action
        if action < len(self.refactoring_manager.operations):
            operation = self.refactoring_manager.operations[action]
            # Execute the operation and define the reward based on its success
            operation.execute()
            return self.evaluate_operation(operation)  # Implement this method based on your metrics
        return 0

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
