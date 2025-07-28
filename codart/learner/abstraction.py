from abc import ABC, abstractmethod
import random
import os
import datetime
import pandas as pd
from codart.learner.abstraction_configs import *
from tqdm import tqdm
import matplotlib.pyplot as plt


class TrainCodArt(ABC):
    """
    RL training parent class
    """

    def __init__(
        self,
        name: str = "",
        num_episodes: int = 1,
        randomly_ending_episode: float = None,
        visualize: bool = True,
    ):
        self.collector = collector
        self.frames_per_batch = frames_per_batch
        self.replay_buffer = replay_buffer
        self.minibatch_size = minibatch_size
        self._name = name
        self._num_episodes = num_episodes
        self._random = randomly_ending_episode
        self.visualize = visualize
        self.logs = {
            "reward": [],
            "step_count": [],
            "eval reward (sum)": [],
            "eval step_count": [],
        }

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
        self.start()
        self.train()
        self.save()
        if self.visualize:  # If visualize is True, call the plot method
            self.visualize_logs()

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
        pbar = tqdm(total=self.num_episodes, desc="Episode")
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
                self.collector.collect(state, action, reward)
                state = self.get_state()
                if self.random is not None and random.random() < self.random:
                    done = True
            tensordict_data = collector.get_data()
            GAE(tensordict_data, params=self.model.critic_network_params)
            for _ in range(self.frames_per_batch // self.minibatch_size):
                subdata = self.replay_buffer.sample(self.minibatch_size)
                loss_vals = self.replay_buffer.train(subdata)
                loss_value = (
                    loss_vals["loss_objective"]
                    + loss_vals["loss_critic"]
                    + loss_vals["loss_entropy"]
                )

                optimizer.zero_grad()
                loss_value.backward()
                optimizer.step()
            episode_reward_mean = self.collector.get_mean_reward()
            pbar.set_description(
                f"Episode Reward Mean: {episode_reward_mean}", refresh=False
            )
            pbar.update()
        pbar.close()

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
            f"{config['Config']['PROJECT_NAME']}_design_metrics_log_{datetime.datetime.time()}.csv",
        )

        df_design_metrics = pd.DataFrame(data=design_metrics)
        if os.path.exists(design_metrics_path):
            df = pd.read_csv(design_metrics_path, index_col=False)
            df_result = pd.concat([df, df_design_metrics], ignore_index=True)
            df_result.to_csv(design_metrics_path, index=False)
        else:
            df_design_metrics.to_csv(design_metrics_path, index=False)

    def visualize_logs(self):
        """Visualize training results and save as PNG files."""
        # Define the directory where images will be saved
        save_dir = os.path.join(config["Config"]["PROJECT_LOG_DIR"], "visualizations")
        os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

        plt.figure(figsize=(10, 10))

        plt.subplot(2, 2, 1)
        plt.plot(self.logs["reward"], label="Training Rewards (Average)")
        plt.title("Training Rewards (Average)")
        plt.xlabel("Episodes")
        plt.ylabel("Reward")
        plt.grid()
        plt.savefig(
            os.path.join(save_dir, "training_rewards_average.png")
        )  # Save the figure

        plt.subplot(2, 2, 2)
        plt.plot(self.logs["step_count"], label="Max Step Count (Training)")
        plt.title("Max Step Count (Training)")
        plt.xlabel("Episodes")
        plt.ylabel("Step Count")
        plt.grid()
        plt.savefig(
            os.path.join(save_dir, "max_step_count_training.png")
        )  # Save the figure

        plt.subplot(2, 2, 3)
        plt.plot(self.logs["eval reward (sum)"], label="Return (Test)")
        plt.title("Return (Test)")
        plt.xlabel("Episodes")
        plt.ylabel("Return")
        plt.grid()
        plt.savefig(os.path.join(save_dir, "return_test.png"))  # Save the figure

        plt.subplot(2, 2, 4)
        plt.plot(self.logs["eval step_count"], label="Max Step Count (Test)")
        plt.title("Max Step Count (Test)")
        plt.xlabel("Episodes")
        plt.ylabel("Test Step Count")
        plt.grid()
        plt.savefig(
            os.path.join(save_dir, "max_step_count_test.png")
        )  # Save the figure

        plt.tight_layout()
        plt.show()
