from celery import Celery
from celery.result import AsyncResult
from application.services.minio_training_controller import ModelTrainingService
import os
import time
import traceback

# Celery configuration
app = Celery('ml_training_tasks',
             broker='amqp://guest:guest@rabbitmq:5672',
             backend='redis://redis:6379/')

# Configure Celery task settings
app.conf.update(
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max runtime
    task_soft_time_limit=2700,  # 45 minutes soft limit
)

# Global task metadata storage (consider using Redis or database in production)
task_metadata = {}


@app.task(bind=True)
def train_dataset_task(self, dataset_path, ds_number, model_version=None):
    """
    Celery task for training machine learning dataset

    Args:
        dataset_path (str): Path to dataset in MinIO
        ds_number (int): Dataset number
        model_version (str, optional): Specific model version

    Returns:
        dict: Training results
    """
    try:
        # Update task metadata
        task_metadata[self.request.id] = {
            'status': 'STARTED',
            'progress': 0,
            'start_time': time.time(),
            'dataset_path': dataset_path,
            'ds_number': ds_number
        }

        # Initialize MinIO Training Controller
        controller = ModelTrainingService(
            minio_endpoint=os.getenv('MINIO_ENDPOINT', 'minio:9000'),
            minio_access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            minio_secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
        )

        # Update progress
        self.update_state(state='PROGRESS', meta={'progress': 25})

        # Train dataset
        results = controller.train_dataset_g7(
            ds_number=ds_number,
            dataset_path=dataset_path
        )

        # Update final task metadata
        task_metadata[self.request.id].update({
            'status': 'COMPLETED',
            'progress': 100,
            'results': results
        })

        return results

    except Exception as e:
        # Update error metadata
        task_metadata[self.request.id].update({
            'status': 'FAILED',
            'error': str(e),
            'traceback': traceback.format_exc()
        })
        raise