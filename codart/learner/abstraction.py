from abc import ABC, abstractmethod
import torch
import random
import os
import datetime
from codart.learner.sbr_initializer.utils.utility import logger, config
import pandas as pd


class TrainCodArt(ABC):
    """
    RL training parent class
    """

    def __init__(
        self,
        name: str = "",
        num_episodes: int = 1,
        randomly_ending_episode: float = None,
        model=None,
    ):
        self._name = name
        self._num_episodes = num_episodes
        self._random = randomly_ending_episode
        self._model = model

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def num_episodes(self):
        return self._num_episodes

    @num_episodes.setter
    def num_episodes(self, value: int):
        self._num_episodes = value

    @property
    def random(self):
        return self._random

    @random.setter
    def random(self, value: float):
        self._random = value

    # Getter and setter for model
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    def do_training(self, *args, **kwargs) -> None:
        self.train()
        self.save()

    @abstractmethod
    def start(self):
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def get_state(self):
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def get_optimizer(self):
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def search(self, state):
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def reward_function(self, state, action):
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def action(self, action_probs=None, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")

    def train(self, *args, **kwargs) -> None:
        optimizer = self.get_optimizer()
        for episode in range(self.num_episodes):
            state = self.get_state()
            done = False
            states, actions, rewards = [], [], []
            while not done:
                action_probs = self.search(state)
                action = self.action(action_probs)
                reward = self.reward_function(state, action)
                states.append(state)
                actions.append(action)
                rewards.append(reward)
                state = self.get_state()
                if self.random is not None and random.random() < self.random:
                    done = True
            states_tensor = torch.FloatTensor(states)
            actions_tensor = torch.LongTensor(actions)
            rewards_tensor = torch.FloatTensor(rewards)
            policy, value = self.model(states_tensor)
            action_probs = policy.gather(1, actions_tensor.unsqueeze(1)).squeeze()
            loss = -torch.mean(torch.log(action_probs) * rewards_tensor)
            print("Episode {}, Loss: {}".format(episode, loss))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    @abstractmethod
    def save(self, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def load(self, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")

    @abstractmethod
    def get_output(self, *args, **kwargs) -> bool:
        raise NotImplementedError(f"{type(self).__name__} not implement")

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

    def log_design_metrics(self, design_metrics):
        design_metrics_path = os.path.join(
            config["Config"]["PROJECT_LOG_DIR"],
            f"{config["Config"]["PROJECT_NAME"]}_design_metrics_log_{datetime.datetime.time()}.csv",
        )

        df_design_metrics = pd.DataFrame(data=design_metrics)
        if os.path.exists(design_metrics_path):
            df = pd.read_csv(design_metrics_path, index_col=False)
            df_result = pd.concat([df, df_design_metrics], ignore_index=True)
            df_result.to_csv(design_metrics_path, index=False)
        else:
            df_design_metrics.to_csv(design_metrics_path, index=False)
