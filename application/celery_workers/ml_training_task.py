from celery import Celery
from application.services.minio_training_controller import ModelTrainingService
import os
import time
import traceback
import gc
from datetime import datetime
from logging import getLogger
from typing import Any, Dict, Optional

# Initialize SciTools Understand for the Celery worker
import sys
sys.path.append('/app/scitools/bin/linux64/Python')
os.environ['LD_LIBRARY_PATH'] = '/app/scitools/bin/linux64'
os.environ['STIHOME'] = '/app/scitools'

# Import after setting up the environment
from codart.learner.tests.test_reinforcement.train import RefactoringTrainer

# Try to import psutil, but don't fail if it's not available
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


logger = getLogger(__name__)

# Celery configuration
app = Celery(
    "ml_training_tasks",
    broker=os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0'),
)

# Configure Celery task settings
app.conf.update(
    task_track_started=True,
    task_time_limit=3600*24,
    task_soft_time_limit=2700*24,
    broker_url=os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    result_extended=True,
    task_send_sent_event=True,
    result_expires=3600,
    task_routes={
        'ml_training_tasks.train_refactoring_model': {'queue': 'ml_training'},
        'ml_training_tasks.evaluate_model': {'queue': 'ml_evaluation'},
    },
    # Add memory management settings
    worker_prefetch_multiplier=1,  # Prevent worker from prefetching too many tasks
    task_acks_late=True,  # Acknowledge tasks only after completion
    worker_max_tasks_per_child=1,  # Restart worker after each task to prevent memory leaks
    worker_max_memory_per_child=10000000,  # 10GB memory limit per child worker (in KB)
    task_reject_on_worker_lost=True,  # Reject tasks if worker is lost
    task_acks_on_failure_or_timeout=True,  # Acknowledge tasks even on failure/timeout
    # Fix deprecation warning for broker connection retry
    broker_connection_retry_on_startup=True,  # Keep retrying broker connections on startup
    # Suppress root user warning
    worker_disable_rate_limits=True,
)

# Suppress Celery's root user warning
import warnings
from celery.platforms import check_privileges
warnings.filterwarnings('ignore', category=UserWarning, module='celery.platforms')

# Global task metadata storage (consider using Redis or database in production)
task_metadata = {}


@app.task(bind=True)
def train_dataset_task(
    self, dataset_path, ds_number, model_version=None, project_name=None
):
    """
    Celery task for training machine learning dataset

    Args:
        dataset_path (str): Path to dataset in MinIO
        ds_number (int): Dataset number
        model_version (str, optional): Specific model version
        project_name (str, optional): Project name

    Returns:
        dict: Training results
    """
    try:
        # Update task metadata
        task_metadata[self.request.id] = {
            "status": "STARTED",
            "progress": 0,
            "start_time": time.time(),
            "dataset_path": dataset_path,
            "ds_number": ds_number,
            "model_version": model_version,
            "project_name": project_name,
        }

        # Initialize MinIO Training Controller
        controller = ModelTrainingService(
            minio_endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
            minio_access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            minio_secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
            bucket_name="metrics",
        )

        # Update progress
        self.update_state(state="PROGRESS", meta={"progress": 25})

        # Train dataset with project info
        results = controller.train_dataset_g7(
            ds_number=ds_number,
            dataset_path=dataset_path,
            project_name=project_name,
            project_version=model_version,
        )

        # Update final task metadata
        task_metadata[self.request.id].update(
            {"status": "COMPLETED", "progress": 100, "results": results}
        )

        return results

    except Exception as e:
        # Update error metadata
        task_metadata[self.request.id].update(
            {"status": "FAILED", "error": str(e), "traceback": traceback.format_exc()}
        )
        raise


@app.task(bind=True, name='ml_training_tasks.train_refactoring_model')
def train_refactoring_model(self,
                            env_config: Dict[str, Any],
                            minio_config: Dict[str, Any],
                            training_options: Optional[Dict[str, Any]] = None):
    """
    Celery task for training refactoring sequence model.

    Args:
        env_config: Environment configuration
        minio_config: MinIO configuration for result storage
        training_options: Additional training options

    Returns:
        Dict with training results and status
    """

    task_id = self.request.id
    logger.info(f"Starting training task {task_id}")
    
    # Monitor initial memory usage if psutil is available
    if HAS_PSUTIL:
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        logger.info(f"Initial memory usage: {initial_memory:.2f} MB")
    else:
        initial_memory = 0
        logger.info("psutil not available, memory monitoring disabled")

    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Initializing training...',
                'progress': 0,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Validate configurations
        _validate_config(env_config, 'Environment')
        _validate_config(minio_config, 'MinIO')

        # Store original project name for file lookups
        original_project_name = env_config['project_name']
        
        # Add task ID to project name for unique identification if not already set
        if not env_config['project_name'].endswith(f"_task_{task_id}"):
            env_config['project_name'] = f"{env_config['project_name']}_task_{task_id}"

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Creating trainer...',
                'progress': 10,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Create trainer with progress callback
        def progress_callback(iteration, total_iterations, metrics):
            progress = min(90, 10 + (iteration / total_iterations) * 80)
            self.update_state(
                state='PROGRESS',
                meta={
                    'status': f'Training iteration {iteration}/{total_iterations}',
                    'progress': progress,
                    'iteration': iteration,
                    'metrics': metrics,
                    'timestamp': datetime.now().isoformat()
                }
            )

        # Ensure database exists before training
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Checking/creating database...',
                'progress': 8,
                'timestamp': datetime.now().isoformat()
            }
        )
        
        # Check if database exists and create if needed
        udb_path = env_config.get('udb_path', '')
        if udb_path and not os.path.exists(udb_path):
            try:
                from codart.utility.directory_utils import create_understand_database
                import hashlib
                
                # Extract project info from path
                path_parts = udb_path.split('/')
                if len(path_parts) >= 4:
                    project_name = path_parts[-3]
                    version_id = path_parts[-2]
                    project_path = f"/opt/projects/{project_name}/{version_id}"
                    
                    if os.path.exists(project_path):
                        os.makedirs(os.path.dirname(udb_path), exist_ok=True)
                        create_understand_database(project_path, os.path.dirname(udb_path))
                        logger.info(f"Created database at {udb_path}")
                    else:
                        logger.warning(f"Project path {project_path} not found, proceeding with fallback")
                else:
                    logger.warning(f"Could not parse database path {udb_path}, proceeding with fallback")
            except Exception as e:
                logger.error(f"Failed to create database: {e}")
                logger.warning("Proceeding with fallback mode")

        # Pass the original project name for file lookups
        trainer = RefactoringTrainer(
            env_config={**env_config, 'original_project_name': original_project_name},
            minio_config=minio_config
        )

        # Add progress callback to trainer
        trainer.progress_callback = progress_callback

        # Handle resume/fine-tuning if specified
        if training_options and training_options.get('resume_from_checkpoint'):
            checkpoint_path = training_options.get('checkpoint_path')
            fine_tune = training_options.get('fine_tune', False)
            
            self.update_state(
                state='PROGRESS',
                meta={
                    'status': f'Loading checkpoint for {"fine-tuning" if fine_tune else "resuming"}...',
                    'progress': 12,
                    'timestamp': datetime.now().isoformat()
                }
            )

            try:
                if checkpoint_path:
                    # Load specific checkpoint
                    trainer.load_checkpoint(minio_path=checkpoint_path, fine_tune=fine_tune)
                else:
                    # Find and load latest checkpoint
                    available_checkpoints = trainer.list_available_checkpoints()
                    if available_checkpoints:
                        # Look for final checkpoint first, then latest
                        latest_checkpoint = None
                        for cp in available_checkpoints:
                            if 'final' in cp:
                                latest_checkpoint = cp
                                break
                        if not latest_checkpoint:
                            latest_checkpoint = available_checkpoints[0]
                        
                        trainer.load_checkpoint(minio_path=latest_checkpoint, fine_tune=fine_tune)
                        logger.info(f"Loaded checkpoint: {latest_checkpoint}")
                    else:
                        logger.warning("No checkpoints found, starting from scratch")

            except Exception as e:
                logger.error(f"Failed to load checkpoint: {e}")
                if training_options.get('require_checkpoint', False):
                    raise
                else:
                    logger.warning("Continuing with fresh training despite checkpoint load failure")

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Starting training...',
                'progress': 15,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Start training
        trainer.train()

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Training completed, saving results...',
                'progress': 95,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Get final metrics
        final_metrics = trainer.training_metrics[-10:] if trainer.training_metrics else []

        # Create result summary
        result = {
            'status': 'SUCCESS',
            'task_id': task_id,
            'project_name': env_config['project_name'],
            'total_iterations': trainer.current_iteration,
            'final_metrics': final_metrics,
            'minio_bucket': minio_config['results_bucket'],
            'training_completed_at': datetime.now().isoformat(),
            'message': 'Training completed successfully'
        }

        logger.info(f"Training task {task_id} completed successfully")
        
        # Monitor final memory usage and cleanup if psutil is available
        if HAS_PSUTIL:
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            logger.info(f"Final memory usage: {final_memory:.2f} MB (increase: {final_memory - initial_memory:.2f} MB)")
        else:
            logger.info("Training completed (memory monitoring disabled)")
        
        # Force garbage collection
        gc.collect()
        
        return result

    except Exception as e:
        error_message = f"Training failed: {str(e)}"
        error_traceback = traceback.format_exc()

        logger.error(f"Training task {task_id} failed: {error_message}")
        logger.error(f"Traceback: {error_traceback}")

        # Update task state to FAILURE
        self.update_state(
            state='FAILURE',
            meta={
                'status': 'Training failed',
                'error': error_message,
                'traceback': error_traceback,
                'timestamp': datetime.now().isoformat()
            }
        )

        # Force garbage collection even on failure
        gc.collect()
        
        # Return failure result instead of raising to avoid serialization issues
        return {
            'status': 'FAILURE',
            'error': error_message,
            'traceback': error_traceback,
            'timestamp': datetime.now().isoformat()
        }


@app.task(bind=True, name='ml_training_tasks.evaluate_model')
def evaluate_model(self,
                   model_path: str,
                   env_config: Dict[str, Any],
                   minio_config: Dict[str, Any],
                   evaluation_episodes: int = 10):
    """
    Celery task for evaluating a trained model.

    Args:
        model_path: Path to the saved model (in MinIO)
        env_config: Environment configuration
        minio_config: MinIO configuration
        evaluation_episodes: Number of episodes for evaluation

    Returns:
        Dict with evaluation results
    """

    task_id = self.request.id
    logger.info(f"Starting evaluation task {task_id}")

    try:
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'Loading model...',
                'progress': 0,
                'timestamp': datetime.now().isoformat()
            }
        )

        # TODO: Implement model loading and evaluation
        # This would involve:
        # 1. Loading the model from MinIO
        # 2. Creating the environment
        # 3. Running evaluation episodes
        # 4. Collecting metrics
        # 5. Saving results back to MinIO

        # Placeholder implementation
        result = {
            'status': 'SUCCESS',
            'task_id': task_id,
            'model_path': model_path,
            'evaluation_episodes': evaluation_episodes,
            'mean_reward': 0.0,  # Placeholder
            'std_reward': 0.0,  # Placeholder
            'evaluation_completed_at': datetime.now().isoformat(),
            'message': 'Evaluation completed (placeholder implementation)'
        }

        logger.info(f"Evaluation task {task_id} completed")
        return result

    except Exception as e:
        error_message = f"Evaluation failed: {str(e)}"
        logger.error(f"Evaluation task {task_id} failed: {error_message}")

        self.update_state(
            state='FAILURE',
            meta={
                'status': 'Evaluation failed',
                'error': error_message,
                'timestamp': datetime.now().isoformat()
            }
        )

        raise


@app.task(bind=True, name='ml_training_tasks.get_training_status')
def get_training_status(self, task_id: str):
    """
    Get the status of a training task.

    Args:
        task_id: The Celery task ID

    Returns:
        Dict with task status and metadata
    """

    try:
        from celery.result import AsyncResult

        result = AsyncResult(task_id, app=app)

        response = {
            'task_id': task_id,
            'status': result.status,
            'timestamp': datetime.now().isoformat()
        }

        if result.info:
            response.update(result.info)

        return response

    except Exception as e:
        logger.error(f"Error getting task status for {task_id}: {e}")
        return {
            'task_id': task_id,
            'status': 'ERROR',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def _validate_config(config: Dict[str, Any], config_name: str):
    """Validate configuration dictionary"""

    if not isinstance(config, dict):
        raise ValueError(f"{config_name} config must be a dictionary")

    required_keys = {
        'Environment': ['project_name', 'udb_path', 'n_obj'],
        'MinIO': ['endpoint', 'access_key', 'secret_key', 'results_bucket']
    }

    if config_name in required_keys:
        missing_keys = [key for key in required_keys[config_name] if key not in config]
        if missing_keys:
            raise ValueError(f"{config_name} config missing required keys: {missing_keys}")


# Additional utility tasks

@app.task(name='ml_training_tasks.cleanup_old_results')
def cleanup_old_results(minio_config: Dict[str, Any],
                        project_name: str,
                        days_old: int = 30):
    """
    Cleanup old training results from MinIO.

    Args:
        minio_config: MinIO configuration
        project_name: Project name
        days_old: Remove results older than this many days
    """

    try:
        from minio import Minio
        from datetime import datetime, timedelta

        minio_client = Minio(
            endpoint=minio_config['endpoint'],
            access_key=minio_config['access_key'],
            secret_key=minio_config['secret_key'],
            secure=minio_config.get('secure', False)
        )

        bucket_name = minio_config['results_bucket']
        cutoff_date = datetime.now() - timedelta(days=days_old)

        # List objects for the project
        objects = minio_client.list_objects(
            bucket_name,
            prefix=f"{project_name}/",
            recursive=True
        )

        deleted_count = 0
        for obj in objects:
            if obj.last_modified < cutoff_date:
                minio_client.remove_object(bucket_name, obj.object_name)
                deleted_count += 1

        logger.info(f"Cleanup completed: {deleted_count} objects removed for project {project_name}")

        return {
            'status': 'SUCCESS',
            'deleted_count': deleted_count,
            'cutoff_date': cutoff_date.isoformat(),
            'project_name': project_name
        }

    except Exception as e:
        logger.error(f"Cleanup failed for project {project_name}: {e}")
        raise


@app.task(name='ml_training_tasks.list_training_results')
def list_training_results(minio_config: Dict[str, Any],
                          project_name: str = None):
    """
    List available training results in MinIO.

    Args:
        minio_config: MinIO configuration
        project_name: Optional project name filter

    Returns:
        List of available results
    """

    try:
        from minio import Minio

        minio_client = Minio(
            endpoint=minio_config['endpoint'],
            access_key=minio_config['access_key'],
            secret_key=minio_config['secret_key'],
            secure=minio_config.get('secure', False)
        )

        bucket_name = minio_config['results_bucket']
        prefix = f"{project_name}/" if project_name else ""

        objects = minio_client.list_objects(
            bucket_name,
            prefix=prefix,
            recursive=True
        )

        results = []
        for obj in objects:
            results.append({
                'object_name': obj.object_name,
                'size': obj.size,
                'last_modified': obj.last_modified.isoformat(),
                'etag': obj.etag
            })

        return {
            'status': 'SUCCESS',
            'results': results,
            'total_count': len(results),
            'project_name': project_name
        }

    except Exception as e:
        logger.error(f"Failed to list results: {e}")
        raise
