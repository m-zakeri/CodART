#!/usr/bin/env python3
"""
Celery task for loading trained models and making refactoring sequence predictions.
"""

import os
import sys
import torch
import numpy as np
import traceback
import io
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from minio import Minio

# Add paths for imports
sys.path.append('/app')
sys.path.append('/app/rl_module')

from celery import Celery
from codart.learner.sbr_initializer.utils.utility import logger

# Import your RL components
from codart.learner.tests.test_reinforcement.environment import RefactoringSequenceEnvironment
from codart.learner.tests.test_reinforcement.model import create_policy_module, create_value_module, create_probabilistic_actor
from codart.learner.tests.test_reinforcement.transformer import RefactoringTransform
from application.services.config_integration import get_integrated_config_manager

# Initialize Celery (reuse existing app)
from application.celery_workers.ml_training_task import app


@app.task(bind=True, name='ml_training_tasks.predict_refactoring_sequence')
def predict_refactoring_sequence_task(self,
                                      project_name: str,
                                      model_checkpoint: Optional[str] = None,
                                      max_steps: int = 10,
                                      temperature: float = 1.0):
    """
    Celery task for predicting optimal refactoring sequence using trained model.

    Args:
        project_name: Name of the project
        model_checkpoint: Specific checkpoint path (if None, uses latest)
        max_steps: Maximum number of refactoring steps to predict
        temperature: Sampling temperature for predictions

    Returns:
        Dict with prediction results
    """

    task_id = self.request.id
    logger.info(f"Starting prediction task {task_id} for project {project_name}")

    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Loading configuration...',
                'progress': 0,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Get configuration
        config_manager = get_integrated_config_manager()
        project_config = config_manager.get_project_specific_config(project_name)

        if not project_config:
            raise Exception(f"Project {project_name} not found in configuration")

        env_config = project_config['env_config']
        minio_config = project_config['minio_config']

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Loading model...',
                'progress': 20,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Load model
        model_info = load_model_from_minio(
            project_name=project_name,
            minio_config=minio_config,
            checkpoint_path=model_checkpoint
        )

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Initializing environment...',
                'progress': 40,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Create environment
        env = RefactoringSequenceEnvironment(**env_config)

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Generating predictions...',
                'progress': 60,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Generate predictions
        start_time = datetime.now()
        predictions = generate_refactoring_sequence(
            env=env,
            model_info=model_info,
            max_steps=max_steps,
            temperature=temperature
        )
        execution_time = (datetime.now() - start_time).total_seconds()

        # Calculate total expected improvement
        total_improvement = calculate_total_improvement(predictions)

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Finalizing results...',
                'progress': 90,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Create result
        result = {
            'project_name': project_name,
            'model_checkpoint': model_info['checkpoint_path'],
            'predictions': predictions,
            'total_expected_improvement': total_improvement,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"Prediction task {task_id} completed successfully")
        return result

    except Exception as e:
        error_message = f"Prediction failed: {str(e)}"
        error_traceback = traceback.format_exc()

        logger.error(f"Prediction task {task_id} failed: {error_message}")
        logger.error(f"Traceback: {error_traceback}")

        # Update task state to FAILURE
        self.update_state(
            state='FAILURE',
            meta={
                'status': 'Prediction failed',
                'error': error_message,
                'traceback': error_traceback,
                'timestamp': datetime.now().isoformat()
            }
        )

        raise Exception(error_message)


@app.task(bind=True, name='ml_training_tasks.load_model')
def load_model_task(self, project_name: str, checkpoint_path: Optional[str] = None):
    """
    Celery task for loading a specific model checkpoint.
    """

    task_id = self.request.id
    logger.info(f"Starting model loading task {task_id} for project {project_name}")

    try:
        # Get configuration
        config_manager = get_integrated_config_manager()
        project_config = config_manager.get_project_specific_config(project_name)

        if not project_config:
            raise Exception(f"Project {project_name} not found")

        minio_config = project_config['minio_config']

        # Load model
        model_info = load_model_from_minio(
            project_name=project_name,
            minio_config=minio_config,
            checkpoint_path=checkpoint_path
        )

        result = {
            'checkpoint_path': model_info['checkpoint_path'],
            'model_info': {
                'iteration': model_info.get('iteration', 'unknown'),
                'model_size': model_info.get('model_size', 'unknown'),
                'creation_date': model_info.get('creation_date', 'unknown'),
            },
            'status': 'loaded',
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"Model loading task {task_id} completed successfully")
        return result

    except Exception as e:
        error_message = f"Model loading failed: {str(e)}"
        logger.error(f"Model loading task {task_id} failed: {error_message}")
        raise Exception(error_message)


def load_model_from_minio(project_name: str, minio_config: Dict[str, Any], checkpoint_path: Optional[str] = None) -> \
Dict[str, Any]:
    """
    Load a trained model from MinIO storage.

    Args:
        project_name: Name of the project
        minio_config: MinIO configuration
        checkpoint_path: Specific checkpoint path (if None, finds latest)

    Returns:
        Dict containing loaded model components and metadata
    """

    try:
        # Create MinIO client
        minio_client = Minio(
            endpoint=minio_config['endpoint'],
            access_key=minio_config['access_key'],
            secret_key=minio_config['secret_key'],
            secure=minio_config.get('secure', False)
        )

        bucket_name = minio_config['results_bucket']

        # Find checkpoint if not specified
        if checkpoint_path is None:
            checkpoint_path = find_latest_checkpoint(minio_client, bucket_name, project_name)

        if not checkpoint_path:
            raise Exception(f"No model checkpoints found for project {project_name}")

        logger.info(f"Loading model from: {checkpoint_path}")

        # Download checkpoint file
        checkpoint_data = minio_client.get_object(bucket_name, checkpoint_path)
        checkpoint_bytes = checkpoint_data.read()

        # Load checkpoint
        checkpoint_buffer = io.BytesIO(checkpoint_bytes)
        checkpoint = torch.load(checkpoint_buffer, map_location='cpu')

        # Extract model components
        policy_state_dict = checkpoint.get('policy_state_dict')
        value_state_dict = checkpoint.get('value_state_dict')
        actor_state_dict = checkpoint.get('actor_state_dict')
        env_config = checkpoint.get('env_config', {})

        if not policy_state_dict:
            raise Exception("Policy state dict not found in checkpoint")

        # Get model metadata
        model_metadata = {
            'checkpoint_path': checkpoint_path,
            'iteration': checkpoint.get('iteration', 'unknown'),
            'model_size': len(checkpoint_bytes),
            'creation_date': datetime.now().isoformat(),
            'env_config': env_config
        }

        return {
            'policy_state_dict': policy_state_dict,
            'value_state_dict': value_state_dict,
            'actor_state_dict': actor_state_dict,
            'env_config': env_config,
            **model_metadata
        }

    except Exception as e:
        logger.error(f"Failed to load model from MinIO: {e}")
        raise Exception(f"Model loading failed: {str(e)}")


def find_latest_checkpoint(minio_client: Minio, bucket_name: str, project_name: str) -> Optional[str]:
    """Find the latest checkpoint for a project."""

    try:
        prefix = f"{project_name}/checkpoints/"
        objects = minio_client.list_objects(bucket_name, prefix=prefix, recursive=True)

        checkpoints = []
        for obj in objects:
            if obj.object_name.endswith('.pth'):
                checkpoints.append((obj.object_name, obj.last_modified))

        if not checkpoints:
            return None

        # Sort by modification time and return latest
        checkpoints.sort(key=lambda x: x[1], reverse=True)
        return checkpoints[0][0]

    except Exception as e:
        logger.error(f"Failed to find latest checkpoint: {e}")
        return None


def generate_refactoring_sequence(env: 'RefactoringSequenceEnvironment',
                                  model_info: Dict[str, Any],
                                  max_steps: int = 10,
                                  temperature: float = 1.0) -> List[Dict[str, Any]]:
    """
    Generate a sequence of refactoring predictions using the loaded model.

    Args:
        env: Environment instance
        model_info: Loaded model information
        max_steps: Maximum number of refactoring steps
        temperature: Sampling temperature

    Returns:
        List of refactoring predictions
    """

    try:
        # Recreate model architecture
        policy_module = create_policy_module(env)
        value_module = create_value_module(env)
        actor = create_probabilistic_actor(policy_module, env)

        # Load model weights
        policy_module.load_state_dict(model_info['policy_state_dict'])
        value_module.load_state_dict(model_info['value_state_dict'])
        if model_info.get('actor_state_dict'):
            actor.load_state_dict(model_info['actor_state_dict'])

        # Set to evaluation mode
        policy_module.eval()
        value_module.eval()
        actor.eval()

        predictions = []
        current_observation = env.reset()

        logger.info(f"Starting prediction sequence with {max_steps} max steps")

        for step in range(max_steps):
            with torch.no_grad():
                # Get policy output
                policy_output = policy_module(current_observation)

                # Apply temperature sampling for refactoring type selection
                if 'refactoring_logits' in policy_output:
                    logits = policy_output['refactoring_logits'] / temperature
                    refactoring_probs = torch.softmax(logits, dim=-1)
                    refactoring_type_idx = torch.multinomial(refactoring_probs, 1).item()
                else:
                    refactoring_type_idx = 0

                # Map to refactoring type name
                refactoring_types = [
                    "Move Method", "Extract Class", "Extract Method",
                    "Pull Up Method", "Push Down Method", "Move Class"
                ]
                refactoring_type = refactoring_types[refactoring_type_idx]

                # Get confidence score
                confidence = refactoring_probs[
                    refactoring_type_idx].item() if 'refactoring_logits' in policy_output else 0.5

                # Get value estimation for expected improvement
                state_value = value_module(current_observation)
                if torch.is_tensor(state_value):
                    expected_improvements = state_value.cpu().numpy().flatten()
                else:
                    expected_improvements = np.zeros(env.n_obj)

                # Create refactoring action - use fallback if method doesn't exist
                try:
                    if hasattr(env, 'convert_policy_action_to_refactoring'):
                        action = env.convert_policy_action_to_refactoring(policy_output)
                    else:
                        # Fallback to generating an action using the generator
                        action = env.generator.generate_an_action()
                        logger.warning("convert_policy_action_to_refactoring method not found, using random action")
                except Exception as e:
                    logger.warning(f"Failed to convert policy action: {e}, using random action")
                    action = env.generator.generate_an_action()

                # Get refactoring parameters
                refactoring_params = extract_refactoring_parameters(action)

                # Execute step
                next_observation = env.step(action)

                # Get actual improvement (reward)
                actual_reward = next_observation.get('reward', torch.zeros(env.n_obj))
                if torch.is_tensor(actual_reward):
                    actual_reward = actual_reward.cpu().numpy().flatten()

                # Create prediction entry
                prediction = {
                    'step': step + 1,
                    'refactoring_type': refactoring_type,
                    'confidence': float(confidence),
                    'parameters': refactoring_params,
                    'expected_improvement': {
                        f'objective_{i}': float(expected_improvements[i])
                        for i in range(min(len(expected_improvements), env.n_obj))
                    },
                    'actual_improvement': {
                        f'objective_{i}': float(actual_reward[i])
                        for i in range(min(len(actual_reward), env.n_obj))
                    }
                }

                predictions.append(prediction)

                # Update observation for next step
                current_observation = next_observation

                # Check if done
                if next_observation.get('done', torch.tensor([False])).item():
                    logger.info(f"Environment signaled done at step {step + 1}")
                    break

                logger.info(f"Step {step + 1}: {refactoring_type} (confidence: {confidence:.3f})")

        logger.info(f"Generated {len(predictions)} refactoring predictions")
        return predictions

    except Exception as e:
        logger.error(f"Failed to generate refactoring sequence: {e}")
        raise Exception(f"Prediction generation failed: {str(e)}")


def extract_refactoring_parameters(action) -> Dict[str, Any]:
    """Extract parameters from a refactoring action."""

    try:
        if hasattr(action, 'get_refactoring'):
            refactoring = action.get_refactoring()
            if hasattr(refactoring, 'params'):
                # Clean up parameters for JSON serialization
                params = {}
                for key, value in refactoring.params.items():
                    if isinstance(value, dict) and 'value' in value:
                        params[key] = value['value']
                    else:
                        params[key] = str(value) if value is not None else ""
                return params

        return {"type": "unknown", "parameters": "not_available"}

    except Exception as e:
        logger.warning(f"Could not extract refactoring parameters: {e}")
        return {"type": "unknown", "parameters": "extraction_failed"}


def calculate_total_improvement(predictions: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate total expected improvement across all predictions."""

    try:
        total_improvement = {}

        if not predictions:
            return total_improvement

        # Get all objective keys from first prediction
        first_prediction = predictions[0]
        objective_keys = list(first_prediction.get('expected_improvement', {}).keys())

        # Sum improvements across all steps
        for key in objective_keys:
            total_improvement[key] = sum(
                pred.get('expected_improvement', {}).get(key, 0.0)
                for pred in predictions
            )

        return total_improvement

    except Exception as e:
        logger.warning(f"Could not calculate total improvement: {e}")
        return {}


# Additional utility tasks

@app.task(name='ml_training_tasks.batch_predict')
def batch_predict_projects(project_names: List[str],
                           max_steps: int = 10,
                           temperature: float = 1.0):
    """
    Run predictions for multiple projects in batch.
    """

    results = {}

    for project_name in project_names:
        try:
            logger.info(f"Starting batch prediction for {project_name}")

            result = predict_refactoring_sequence_task.apply(
                args=[project_name],
                kwargs={
                    'max_steps': max_steps,
                    'temperature': temperature
                }
            ).get()

            results[project_name] = {
                'status': 'success',
                'result': result
            }

        except Exception as e:
            logger.error(f"Batch prediction failed for {project_name}: {e}")
            results[project_name] = {
                'status': 'failed',
                'error': str(e)
            }

    return {
        'batch_results': results,
        'total_projects': len(project_names),
        'successful': len([r for r in results.values() if r['status'] == 'success']),
        'failed': len([r for r in results.values() if r['status'] == 'failed']),
        'timestamp': datetime.now().isoformat()
    }


@app.task(name='ml_training_tasks.compare_models')
def compare_models_task(project_name: str,
                        checkpoint_paths: List[str],
                        max_steps: int = 10):
    """
    Compare predictions from multiple model checkpoints.
    """

    try:
        comparisons = {}

        for checkpoint_path in checkpoint_paths:
            try:
                result = predict_refactoring_sequence_task.apply(
                    args=[project_name],
                    kwargs={
                        'model_checkpoint': checkpoint_path,
                        'max_steps': max_steps,
                        'temperature': 1.0
                    }
                ).get()

                comparisons[checkpoint_path] = result

            except Exception as e:
                logger.error(f"Model comparison failed for {checkpoint_path}: {e}")
                comparisons[checkpoint_path] = {'error': str(e)}

        return {
            'project_name': project_name,
            'model_comparisons': comparisons,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Model comparison task failed: {e}")
        raise Exception(f"Model comparison failed: {str(e)}")