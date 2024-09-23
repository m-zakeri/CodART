from abc import ABC, abstractmethod
import torch
import random

class TrainCodArt(ABC):
    """
        RL training parent class
    """


    def __init__(self, name: str = "",
                 num_episodes:int=1,
                 randomly_ending_episode:float= None,
                 model= None):
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


    def train(self, *args, **kwargs) -> bool:
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