import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import io
import os
import json
from datetime import datetime
from minio import Minio
from tensordict import TensorDict
from torchrl.collectors import SyncDataCollector
from torchrl.data.replay_buffers import ReplayBuffer
from torchrl.data.replay_buffers.samplers import SamplerWithoutReplacement
from torchrl.data.replay_buffers.storages import LazyTensorStorage
from torchrl.objectives import ClipPPOLoss, ValueEstimators
from torchrl.objectives.value import GAE
from torchrl.envs import RewardSum, TransformedEnv
from torchrl.envs.utils import check_env_specs
from tqdm import tqdm
from typing import Dict, Any, List, Optional

# Import your modules
from codart.learner.tests.test_reinforcement.environment import RefactoringSequenceEnvironment
from codart.learner.tests.test_reinforcement.model import create_policy_module, create_value_module, create_probabilistic_actor
from codart.learner.tests.test_reinforcement.transformer import RefactoringTransform
from codart.learner.sbr_initializer.utils.utility import config, logger


class RefactoringTrainer:
    """
    Trainer for refactoring sequence optimization using PPO with multi-objective rewards.
    """

    def __init__(self,
                 env_config: Dict[str, Any],
                 minio_config: Optional[Dict[str, Any]] = None):

        self.env_config = env_config
        self.minio_config = minio_config

        # Load training config from config file
        self.load_training_config()

        # Initialize device
        self.device = (
            torch.device(0)
            if torch.cuda.is_available()
            else torch.device("cpu")
        )

        # Initialize environment - filter config to only valid parameters
        valid_env_params = {
            'udb_path', 'n_obj', 'lower_band', 'upper_bound', 
            'population_size', 'device', 'seed', 'project_name', 
            'version_id', 'project_path'
        }
        filtered_env_config = {k: v for k, v in env_config.items() if k in valid_env_params}
        self.env = RefactoringSequenceEnvironment(**filtered_env_config)

        # Add transforms
        # self.env = TransformedEnv(
        #     self.env,
        #     RefactoringTransform()
        # )

        # Check environment specs - temporarily disabled to avoid TensorDict stacking issues
        # check_env_specs(self.env)

        # Initialize MinIO client if configured
        if minio_config:
            self.setup_minio_client()
        else:
            self.minio_client = None
            self.results_bucket = None

        # Initialize networks
        self.setup_networks()

        # Initialize data collection and replay buffer
        self.setup_data_collection()

        # Initialize loss and optimizer
        self.setup_loss_and_optimizer()

        # Training metrics storage
        self.training_metrics = []
        self.current_iteration = 0

    def load_training_config(self):
        """Load training configuration from config file"""
        self.frames_per_batch = config.getint("TRAINING", "frames_per_batch")
        self.n_iters = config.getint("TRAINING", "n_iters")
        self.total_frames = self.frames_per_batch * self.n_iters
        self.num_epochs = config.getint("TRAINING", "num_epochs")
        self.minibatch_size = config.getint("TRAINING", "minibatch_size")
        self.lr = config.getfloat("TRAINING", "learning_rate")
        self.max_grad_norm = config.getfloat("TRAINING", "max_grad_norm")
        self.max_steps = config.getint("TRAINING", "max_steps")

        # PPO specific config
        self.clip_epsilon = config.getfloat("PPO", "clip_epsilon")
        self.gamma = config.getfloat("PPO", "gamma")
        self.lmbda = config.getfloat("PPO", "lambda")
        self.entropy_eps = config.getfloat("PPO", "entropy_eps")

        logger.info(f"Training config loaded: {self.frames_per_batch} frames/batch, {self.n_iters} iterations")

    def setup_minio_client(self):
        """Setup MinIO client for result storage"""
        try:
            self.minio_client = Minio(
                endpoint=self.minio_config['endpoint'],
                access_key=self.minio_config['access_key'],
                secret_key=self.minio_config['secret_key'],
                secure=self.minio_config.get('secure', False)
            )
            self.results_bucket = self.minio_config.get('results_bucket', 'ml-models')

            # Create bucket if it doesn't exist
            if not self.minio_client.bucket_exists(self.results_bucket):
                self.minio_client.make_bucket(self.results_bucket)
                logger.info(f"Created MinIO bucket: {self.results_bucket}")

            logger.info("MinIO client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to setup MinIO client: {e}")
            self.minio_client = None
            self.results_bucket = None

    def setup_networks(self):
        """Initialize policy and value networks with enhanced error handling"""
        try:
            # Create policy and value modules
            self.policy_module = create_policy_module(self.env)
            self.value_module = create_value_module(self.env)

            # Create probabilistic actor
            self.actor = create_probabilistic_actor(self.policy_module, self.env)

            # Move to device
            self.policy_module.to(self.device)
            self.value_module.to(self.device)
            self.actor.to(self.device)

            logger.info("Networks initialized and moved to device")

            # Test networks with sample data
            self._test_networks()

        except Exception as e:
            logger.error(f"Error setting up networks: {e}", exc_info=True)
            raise

    def _test_networks(self):
        """Test networks with sample data to catch errors early"""
        try:
            logger.info("Testing networks with sample data...")

            # Create sample input matching environment output
            sample_input = TensorDict({
                "refactoring": torch.tensor([1.0], dtype=torch.float32, device=self.device),
                "refactoring_type": torch.tensor([2.0], dtype=torch.float32, device=self.device),
                "success": torch.tensor([True], dtype=torch.bool, device=self.device),
            }, batch_size=[1])

            # Test policy module
            with torch.no_grad():
                policy_output = self.policy_module(sample_input)
                logger.debug(f"Policy test output keys: {policy_output.keys()}")
                # Should now contain: 'refactoring_logits', 'loc', 'scale'

                # Test value module
                value_output = self.value_module(sample_input)
                logger.debug(f"Value test output keys: {value_output.keys()}")

                # Test actor - this should now work!
                actor_output = self.actor(sample_input)
                logger.debug(f"Actor test output keys: {actor_output.keys()}")

            logger.info("Network testing completed successfully")

        except Exception as e:
            logger.error(f"Network testing failed: {e}", exc_info=True)
            raise

    def setup_data_collection(self):
        """Setup data collector and replay buffer"""

        # Test the actor with a sample input first
        try:
            sample_input = self.env.reset()
            logger.debug(f"Sample input keys: {sample_input.keys()}")
            logger.debug(f"Sample input batch_size: {sample_input.batch_size}")

            # Test policy module
            with torch.no_grad():
                policy_output = self.policy_module(sample_input)
                logger.debug(f"Policy output keys: {policy_output.keys()}")

                # Test actor
                actor_output = self.actor(sample_input)
                logger.debug(f"Actor output keys: {actor_output.keys()}")

        except Exception as e:
            logger.error(f"Error testing networks: {e}", exc_info=True)
            raise

        # Data collector - create_env_fn is required for newer TorchRL versions
        def create_env_fn():
            # Return a fresh copy of the environment for each collector worker
            valid_env_params = {
                'udb_path', 'n_obj', 'lower_band', 'upper_bound',
                'population_size', 'device', 'seed', 'project_name',
                'version_id', 'project_path'
            }
            filtered_env_config = {k: v for k, v in self.env_config.items() if k in valid_env_params}

            from codart.learner.tests.test_reinforcement.environment import RefactoringSequenceEnvironment
            return RefactoringSequenceEnvironment(**filtered_env_config)

        try:
            self.collector = SyncDataCollector(
                create_env_fn=create_env_fn,
                policy=self.actor,
                device=self.device,
                storing_device=self.device,
                frames_per_batch=self.frames_per_batch,
                total_frames=self.total_frames,
            )
            logger.info("Data collector created successfully")
        except Exception as e:
            logger.error(f"Error creating data collector: {e}", exc_info=True)

            # Fallback: use the existing environment directly
            logger.info("Falling back to direct environment usage")
            self.collector = SyncDataCollector(
                env=self.env,
                policy=self.actor,
                device=self.device,
                storing_device=self.device,
                frames_per_batch=self.frames_per_batch,
                total_frames=self.total_frames,
            )

        # Replay buffer
        self.replay_buffer = ReplayBuffer(
            storage=LazyTensorStorage(self.frames_per_batch, device=self.device),
            sampler=SamplerWithoutReplacement(),
            batch_size=self.minibatch_size,
        )

        logger.info("Data collection and replay buffer initialized")

    def setup_loss_and_optimizer(self):
        """Setup loss function and optimizer with enhanced error handling"""
        try:
            # PPO Loss
            self.loss_module = ClipPPOLoss(
                actor_network=self.actor,
                critic_network=self.value_module,
                clip_epsilon=self.clip_epsilon,
                entropy_coef=self.entropy_eps,
                normalize_advantage=True,
            )

            # Set loss keys - make sure these match your environment output
            self.loss_module.set_keys(
                reward="reward",
                action="action",
                sample_log_prob="sample_log_prob",
                value="state_value",
                done="done",
            )

            # GAE value estimator
            self.loss_module.make_value_estimator(
                ValueEstimators.GAE,
                gamma=self.gamma,
                lmbda=self.lmbda
            )

            # Optimizer
            self.optimizer = torch.optim.Adam(
                self.loss_module.parameters(),
                lr=self.lr
            )

            logger.info("Loss function and optimizer initialized")

        except Exception as e:
            logger.error(f"Error setting up loss and optimizer: {e}", exc_info=True)
            raise

    def train(self):
        """Main training loop"""
        logger.info("Starting refactoring sequence training...")
        logger.info(f"Total frames: {self.total_frames}, Frames per batch: {self.frames_per_batch}")

        collected_frames = 0
        episode_rewards = []
        episode_lengths = []

        # Training loop
        pbar = tqdm(total=self.n_iters, desc="Training Progress")

        try:
            for batch_idx, batch in enumerate(self.collector):
                collected_frames += batch.numel()
                self.current_iteration = batch_idx

                # Add batch to replay buffer
                self.replay_buffer.extend(batch)

                # Calculate advantages using GAE
                with torch.no_grad():
                    batch = self.loss_module.value_estimator(batch)

                # PPO training epochs
                epoch_losses = []
                for epoch in range(self.num_epochs):
                    # Sample from replay buffer
                    if len(self.replay_buffer) < self.minibatch_size:
                        continue

                    sample = self.replay_buffer.sample()

                    # Calculate loss
                    loss_dict = self.loss_module(sample)
                    total_loss = (
                            loss_dict['loss_objective'] +
                            loss_dict['loss_critic'] +
                            loss_dict['loss_entropy']
                    )

                    # Backward pass
                    self.optimizer.zero_grad()
                    total_loss.backward()

                    # Gradient clipping
                    torch.nn.utils.clip_grad_norm_(
                        self.loss_module.parameters(),
                        self.max_grad_norm
                    )

                    self.optimizer.step()
                    epoch_losses.append(total_loss.item())

                # Calculate episode metrics
                if 'done' in batch and batch['done'].any():
                    episode_reward = self._extract_reward(batch['reward'])
                    episode_length = batch.get('step_count', torch.tensor([0])).float().mean().item()

                    episode_rewards.append(episode_reward)
                    episode_lengths.append(episode_length)

                    # Store training metrics
                    metrics = self._create_training_metrics(
                        batch_idx, collected_frames, episode_reward,
                        episode_length, loss_dict, epoch_losses
                    )

                    # Add multi-objective rewards
                    if batch['reward'].numel() > 1:
                        metrics.update(self._extract_objective_metrics(batch['reward']))

                    self.training_metrics.append(metrics)

                # Save checkpoint and results periodically
                if batch_idx % 100 == 0 and batch_idx > 0:
                    self.save_checkpoint(f"iteration_{batch_idx}")
                    self.save_training_results()

                # Evaluation
                if batch_idx % 50 == 0:
                    self.evaluate_and_save()

                # Update progress bar
                pbar.update(1)
                pbar.set_postfix({
                    'frames': collected_frames,
                    'avg_reward': np.mean(episode_rewards[-10:]) if episode_rewards else 0,
                    'loss': np.mean(epoch_losses) if epoch_losses else 0
                })

                # Break if we've reached total iterations
                if batch_idx >= self.n_iters - 1:
                    break

        except KeyboardInterrupt:
            logger.info("Training interrupted by user")
        except Exception as e:
            logger.error(f"Training failed: {e}", exc_info=True)
            raise
        finally:
            pbar.close()
            # Final save
            self.save_checkpoint('final')
            self.save_training_results()
            logger.info("Training completed!")

    def _extract_reward(self, reward_tensor):
        """Extract scalar reward from tensor"""
        if reward_tensor.numel() == 1:
            return reward_tensor.item()
        else:
            return reward_tensor.mean().item()

    def _create_training_metrics(self, batch_idx, collected_frames, episode_reward,
                                 episode_length, loss_dict, epoch_losses):
        """Create training metrics dictionary"""
        return {
            'iteration': batch_idx,
            'collected_frames': collected_frames,
            'episode_reward': episode_reward,
            'episode_length': episode_length,
            'loss_objective': loss_dict.get('loss_objective', torch.tensor(0)).item(),
            'loss_critic': loss_dict.get('loss_critic', torch.tensor(0)).item(),
            'loss_entropy': loss_dict.get('loss_entropy', torch.tensor(0)).item(),
            'total_loss': np.mean(epoch_losses) if epoch_losses else 0,
            'timestamp': datetime.now().isoformat()
        }

    def _extract_objective_metrics(self, reward_tensor):
        """Extract multi-objective metrics from reward tensor"""
        metrics = {}
        if len(reward_tensor.shape) > 1 and reward_tensor.shape[-1] > 1:
            for i in range(reward_tensor.shape[-1]):
                metrics[f'objective_{i}'] = reward_tensor[..., i].mean().item()
        return metrics

    def evaluate_and_save(self):
        """Evaluate the current policy and save results"""
        logger.info("Evaluating policy...")

        # Set policy to evaluation mode
        self.actor.eval()

        eval_rewards = []
        eval_metrics = []

        # Run evaluation episodes
        for episode in range(5):  # Evaluate on 5 episodes
            try:
                observation = self.env.reset()
                episode_reward = 0
                episode_metrics = []

                done = False
                step = 0

                while not done and step < self.max_steps:
                    # Get action from policy
                    with torch.no_grad():
                        action_dict = self.actor(observation)
                        action = action_dict.get('action', None)

                    # Take step
                    observation = self.env.step(action_dict)

                    # Extract reward and metrics
                    reward = observation.get('reward', torch.tensor([0.0]))
                    if torch.is_tensor(reward):
                        reward_val = reward.mean().item()
                    else:
                        reward_val = float(reward)

                    episode_reward += reward_val

                    # Store step metrics
                    step_metrics = {
                        'episode': episode,
                        'step': step,
                        'reward': reward_val,
                        'success': observation.get('success', torch.tensor([False])).item()
                    }

                    episode_metrics.append(step_metrics)

                    done = observation.get('done', torch.tensor([False])).item()
                    step += 1

                eval_rewards.append(episode_reward)
                eval_metrics.extend(episode_metrics)

            except Exception as e:
                logger.warning(f"Evaluation episode {episode} failed: {e}")
                continue

        # Calculate evaluation statistics
        if eval_rewards:
            eval_stats = {
                'iteration': self.current_iteration,
                'mean_reward': np.mean(eval_rewards),
                'std_reward': np.std(eval_rewards),
                'min_reward': np.min(eval_rewards),
                'max_reward': np.max(eval_rewards),
                'timestamp': datetime.now().isoformat()
            }

            # Save evaluation results
            self.save_evaluation_results(eval_stats, eval_metrics)

            logger.info(f"Evaluation completed. Mean reward: {eval_stats['mean_reward']:.4f}")

        # Set policy back to training mode
        self.actor.train()

    def save_checkpoint(self, checkpoint_name):
        """Save model checkpoint"""
        checkpoint = {
            'policy_state_dict': self.policy_module.state_dict(),
            'value_state_dict': self.value_module.state_dict(),
            'actor_state_dict': self.actor.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'iteration': self.current_iteration,
            'env_config': self.env_config,
            'training_metrics': self.training_metrics,
            'training_config': {
                'frames_per_batch': self.frames_per_batch,
                'n_iters': self.n_iters,
                'num_epochs': self.num_epochs,
                'minibatch_size': self.minibatch_size,
                'lr': self.lr,
                'max_grad_norm': self.max_grad_norm,
                'max_steps': self.max_steps
            }
        }

        # Save locally
        checkpoint_path = f'checkpoint_{checkpoint_name}.pth'
        torch.save(checkpoint, checkpoint_path)

        # Save to MinIO if configured
        if self.minio_client:
            try:
                with open(checkpoint_path, 'rb') as f:
                    self.minio_client.put_object(
                        bucket_name=self.results_bucket,
                        object_name=f"{self.env_config['project_name']}/checkpoints/{checkpoint_path}",
                        data=f,
                        length=os.path.getsize(checkpoint_path)
                    )
                logger.info(f"Checkpoint saved to MinIO: {checkpoint_path}")
            except Exception as e:
                logger.error(f"Error saving checkpoint to MinIO: {e}")

    def load_checkpoint(self, checkpoint_path: str = None, minio_path: str = None, fine_tune: bool = False):
        """
        Load model checkpoint for resuming training or fine-tuning
        
        Args:
            checkpoint_path: Local path to checkpoint file
            minio_path: MinIO path to checkpoint (format: project_name/checkpoints/checkpoint_name.pth)
            fine_tune: If True, only load model weights (not optimizer state or training metrics)
        """
        checkpoint = None
        
        if minio_path and self.minio_client:
            try:
                # Download from MinIO
                response = self.minio_client.get_object(self.results_bucket, minio_path)
                checkpoint_data = response.read()
                checkpoint = torch.load(io.BytesIO(checkpoint_data), map_location=self.device)
                logger.info(f"Checkpoint loaded from MinIO: {minio_path}")
            except Exception as e:
                logger.error(f"Error loading checkpoint from MinIO: {e}")
                raise
        elif checkpoint_path and os.path.exists(checkpoint_path):
            checkpoint = torch.load(checkpoint_path, map_location=self.device)
            logger.info(f"Checkpoint loaded from local file: {checkpoint_path}")
        else:
            raise ValueError("Either checkpoint_path or minio_path must be provided and valid")
        
        if checkpoint is None:
            raise ValueError("Failed to load checkpoint")
        
        # Load model weights
        self.policy_module.load_state_dict(checkpoint['policy_state_dict'])
        self.value_module.load_state_dict(checkpoint['value_state_dict'])
        self.actor.load_state_dict(checkpoint['actor_state_dict'])
        
        if not fine_tune:
            # Full resume - load optimizer state and training progress
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.current_iteration = checkpoint.get('iteration', 0)
            self.training_metrics = checkpoint.get('training_metrics', [])
            logger.info(f"Resuming training from iteration {self.current_iteration}")
        else:
            # Fine-tuning - reset training state but keep model weights
            self.current_iteration = 0
            self.training_metrics = []
            # Optionally adjust learning rate for fine-tuning
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = param_group['lr'] * 0.1  # Reduce LR for fine-tuning
            logger.info("Model loaded for fine-tuning with reduced learning rate")
        
        # Update environment config if provided in checkpoint
        if 'env_config' in checkpoint and not fine_tune:
            self.env_config.update(checkpoint['env_config'])
        
        return checkpoint

    def list_available_checkpoints(self, project_name: str = None) -> List[str]:
        """List available checkpoints in MinIO for a project"""
        available_checkpoints = []
        if not self.minio_client:
            return available_checkpoints
        
        target_project = project_name or self.env_config['project_name']
        prefix = f"{target_project}/checkpoints/"
        
        try:
            objects = self.minio_client.list_objects(self.results_bucket, prefix=prefix, recursive=True)
            for obj in objects:
                if obj.object_name.endswith('.pth'):
                    available_checkpoints.append(obj.object_name)
        except Exception as e:
            logger.error(f"Error listing checkpoints: {e}")
        
        return available_checkpoints

    def save_training_results(self):
        """Save training metrics to CSV and MinIO"""
        if not self.training_metrics:
            return

        # Create DataFrame
        df = pd.DataFrame(self.training_metrics)

        # Save locally
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"training_results_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)

        # Save to MinIO if configured
        if self.minio_client:
            try:
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()

                project_name = self.env_config['project_name']

                # Save timestamped version
                self.minio_client.put_object(
                    bucket_name=self.results_bucket,
                    object_name=f"{project_name}/training_results/{csv_filename}",
                    data=io.BytesIO(csv_data.encode()),
                    length=len(csv_data)
                )

                # Save as latest version
                self.minio_client.put_object(
                    bucket_name=self.results_bucket,
                    object_name=f"{project_name}/training_results/latest.csv",
                    data=io.BytesIO(csv_data.encode()),
                    length=len(csv_data)
                )

                logger.info(f"Training results saved to MinIO: {csv_filename}")

            except Exception as e:
                logger.error(f"Error saving training results to MinIO: {e}")

    def save_evaluation_results(self, eval_stats: Dict, eval_metrics: List[Dict]):
        """Save evaluation results to CSV and MinIO"""
        # Save evaluation statistics
        stats_df = pd.DataFrame([eval_stats])

        # Save detailed metrics
        metrics_df = pd.DataFrame(eval_metrics)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save locally
        stats_filename = f"evaluation_stats_{timestamp}.csv"
        metrics_filename = f"evaluation_metrics_{timestamp}.csv"

        stats_df.to_csv(stats_filename, index=False)
        if eval_metrics:
            metrics_df.to_csv(metrics_filename, index=False)

        # Save to MinIO if configured
        if self.minio_client:
            try:
                project_name = self.env_config['project_name']

                # Save stats
                stats_buffer = io.StringIO()
                stats_df.to_csv(stats_buffer, index=False)
                stats_data = stats_buffer.getvalue()

                self.minio_client.put_object(
                    bucket_name=self.results_bucket,
                    object_name=f"{project_name}/evaluation/{stats_filename}",
                    data=io.BytesIO(stats_data.encode()),
                    length=len(stats_data)
                )

                # Save metrics if available
                if eval_metrics:
                    metrics_buffer = io.StringIO()
                    metrics_df.to_csv(metrics_buffer, index=False)
                    metrics_data = metrics_buffer.getvalue()

                    self.minio_client.put_object(
                        bucket_name=self.results_bucket,
                        object_name=f"{project_name}/evaluation/{metrics_filename}",
                        data=io.BytesIO(metrics_data.encode()),
                        length=len(metrics_data)
                    )

                logger.info("Evaluation results saved to MinIO")

            except Exception as e:
                logger.error(f"Error saving evaluation results to MinIO: {e}")


def main():
    """Main training function"""

    # Environment configuration
    env_config = {
        'udb_path': config.get("ENVIRONMENT", "udb_path"),
        'n_obj': config.getint("ENVIRONMENT", "n_obj"),
        'lower_band': config.getint("ENVIRONMENT", "lower_band"),
        'upper_bound': config.getint("ENVIRONMENT", "upper_bound"),
        'population_size': config.getint("ENVIRONMENT", "population_size"),
        'project_name': config.get("ENVIRONMENT", "project_name"),
        'version_id': config.get("ENVIRONMENT", "version_id"),
        'project_path': config.get("ENVIRONMENT", "project_path")
    }

    # MinIO configuration
    minio_config = {
        'endpoint': config.get("MINIO", "endpoint"),
        'access_key': config.get("MINIO", "access_key"),
        'secret_key': config.get("MINIO", "secret_key"),
        'secure': config.getboolean("MINIO", "secure"),
        'results_bucket': config.get("MINIO", "results_bucket")
    }

    # Create trainer and start training
    trainer = RefactoringTrainer(
        env_config=env_config,
        minio_config=minio_config
    )

    trainer.train()


if __name__ == "__main__":
    main()