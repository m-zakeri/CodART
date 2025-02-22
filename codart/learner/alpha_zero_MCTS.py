import torch
from torch import optim
from codart.learner.sbr_initializer.smell import SmellInitialization
from codart.learner.abstraction import TrainCodArt
from codart.refactorings.handler import RefactoringManager, RefactoringOperation
from codart.metrics.qmood import DesignQualityAttributes
import os
import numpy as np
from codart.utility.directory_utils import update_understand_database
from multiprocessing import Process, Array
from codart.learner.sbr_initializer.utils.utility import logger, config
from codart.learner.cod2vec.interactive_predictor import InteractivePredictor
from transformers import AutoTokenizer, GPTBigCodeForCausalLM
from abstraction_configs import critic, policy


class TrainerImplement(TrainCodArt):

    def __init__(
        self,
        n_obj: int = 8,
        evaluate_in_parallel: bool = True,
        verbose_design_metrics: bool = True,
        pretrained_model_path: str = os.path.join("bigcode", "gpt_bigcode-santacoder"),
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_path)
        self.gpt_model = GPTBigCodeForCausalLM.from_pretrained(pretrained_model_path)
        if torch.cuda.is_available():
            self.gpt_model = self.gpt_model.half().cuda()
        super(TrainerImplement, self).__init__(
            name="PPO",
            num_episodes=2,
            randomly_ending_episode=0.1,
        )

        self.udb_path: str = os.path.join(
            str(config["Config"]["db_address"]), str(config["Config"]["db_name"])
        )
        self.refactoring_manager = RefactoringManager()
        self.n_obj = n_obj
        self.evaluate_in_parallel = (evaluate_in_parallel,)
        self.verbose_design_metrics = (verbose_design_metrics,)
        self.generator = SmellInitialization()
        self.interactive_predictor = InteractivePredictor()
        self.pretrained_model_path: str = pretrained_model_path

    def start(self):
        self.model.load_state_dict(state_dict=torch.load(self.pretrained_model_path))
        self.refactoring_manager.add_operation(self.generator.generate_an_action())

    def get_state(self):
        return {
            "metrics": self.calculate_metrics(),
            "codes": self.interactive_predictor.predict(),
        }

    def get_optimizer(self):
        return optim.Adam(self.model.parameters(), lr=0.001)

    def search(self, state):
        self.refactoring_manager.add_operation(self.generator.generate_an_action())
        with torch.no_grad():
            input_tensor = torch.FloatTensor(state)
            policy, _ = self.model(input_tensor)
            return policy.numpy()

    def action(
        self, action_probs: RefactoringOperation = None, *args, **kwargs
    ) -> bool:
        action_probs.execute()
        update_understand_database(udb_path=self.udb_path)
        if action_probs is None:
            raise ValueError("Action probabilities must be provided.")
        action_probs = torch.tensor(action_probs.get_refactoring()).float()
        action = torch.multinomial(
            torch.softmax(torch.FloatTensor(action_probs), dim=0), 1
        )
        return action.item()

    def reward_function(self, state, action):
        return np.array(state["metrics"], dtype=float)

    def save(self, file_path: str = "", *args, **kwargs) -> None:
        torch.save(self.replay_buffer.state_dict(), file_path)
        torch.save(self.gpt_model.state_dict(), file_path)

    def load(
        self, file_path_rl: str = "", file_path_gpt: str = "", *args, **kwargs
    ) -> None:
        self.replay_buffer.load_state_dict(torch.load(file_path_rl))
        self.gpt_model.load_state_dict(torch.load(file_path_gpt))
        self.replay_buffer.eval()
        self.gpt_model.eval()

    def get_output(self, input_data, *args, **kwargs) -> bool:
        with torch.no_grad():
            input_tensor = torch.FloatTensor(input_data)
            policy, _ = self.model(input_tensor)
            return policy.numpy()

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

            objective_values.append([-1 * i for i in arr])
            logger.info(f"Objective values for individual {k}: {[i for i in arr]}")
        return objective_values
