from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from celery.result import AsyncResult
from datetime import datetime
import os
import json
import logging

from application.celery_workers.ml_training_task import (
    train_refactoring_model,
    evaluate_model,
    get_training_status,
    cleanup_old_results,
    list_training_results,
    app
)

try:
    from application.services.config_integration import get_integrated_config_manager
except ImportError:
    get_integrated_config_manager = None

logger = logging.getLogger(__name__)

# FastAPI router
router = APIRouter(prefix="/api/v1/ml-training", tags=["ML Training"])


# Enhanced Pydantic models
class EnvironmentConfig(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    udb_path: str = Field(..., description="Path to the Understand database file")
    n_obj: int = Field(8, description="Number of optimization objectives")
    lower_band: int = Field(1, description="Lower bound for population")
    upper_bound: int = Field(50, description="Upper bound for population")
    population_size: int = Field(100, description="Population size")
    version_id: str = Field("v1.0", description="Version identifier")
    project_path: str = Field(..., description="Path to project source code")
    evaluate_in_parallel: bool = Field(True, description="Enable parallel evaluation")
    verbose_design_metrics: bool = Field(True, description="Enable verbose metrics")


class MinIOConfig(BaseModel):
    endpoint: str = Field(..., description="MinIO endpoint")
    access_key: str = Field(..., description="MinIO access key")
    secret_key: str = Field(..., description="MinIO secret key")
    secure: bool = Field(False, description="Use secure connection")
    results_bucket: str = Field("ml-models", description="Bucket for storing results")


class TrainingOptions(BaseModel):
    frames_per_batch: Optional[int] = Field(6000, description="Frames per batch")
    n_iters: Optional[int] = Field(10, description="Number of iterations")
    num_epochs: Optional[int] = Field(30, description="Number of epochs")
    minibatch_size: Optional[int] = Field(400, description="Minibatch size")
    learning_rate: Optional[float] = Field(0.0003, description="Learning rate")
    max_grad_norm: Optional[float] = Field(1.0, description="Max gradient norm")
    max_steps: Optional[int] = Field(100, description="Max steps per episode")
    save_interval: Optional[int] = Field(100, description="Save checkpoint interval")
    evaluation_interval: Optional[int] = Field(50, description="Evaluation interval")
    use_normalization: bool = Field(True, description="Use reward/observation normalization")


class TrainingRequest(BaseModel):
    env_config: EnvironmentConfig
    minio_config: MinIOConfig
    training_options: Optional[TrainingOptions] = None


class TrainingResponse(BaseModel):
    task_id: str
    status: str
    message: str
    timestamp: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: Optional[float] = None
    current_iteration: Optional[int] = None
    metrics: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str


class ModelPredictionRequest(BaseModel):
    project_name: str = Field(..., description="Project name")
    model_checkpoint: Optional[str] = Field(None, description="Specific checkpoint path")
    max_steps: int = Field(10, description="Maximum refactoring steps to predict")
    temperature: float = Field(1.0, description="Sampling temperature for predictions")


class RefactoringPrediction(BaseModel):
    step: int
    refactoring_type: str
    confidence: float
    parameters: Dict[str, Any]
    expected_improvement: Dict[str, float]  # Objective improvements


class PredictionResponse(BaseModel):
    project_name: str
    model_checkpoint: str
    predictions: List[RefactoringPrediction]
    total_expected_improvement: Dict[str, float]
    execution_time: float
    timestamp: str


# =============================================================================
# TRAINING ENDPOINTS (Fixed and Enhanced)
# =============================================================================

@router.post("/train", response_model=TrainingResponse)
async def start_training(request: Optional[TrainingRequest] = None, project_name: Optional[str] = None):
    """
    Start a new refactoring sequence model training task.
    Can use either a complete TrainingRequest or just a project_name to load from Redis.
    """
    try:
        if get_integrated_config_manager is None:
            logger.warning("Config integration not available, using basic functionality")

        config_manager = get_integrated_config_manager() if get_integrated_config_manager else None

        if request:
            # Use provided configuration
            env_config = request.env_config.dict()
            minio_config = request.minio_config.dict()
            training_options = request.training_options.dict() if request.training_options else {}
        elif project_name and config_manager:
            # Load configuration from Redis and config files
            project_config = config_manager.get_project_specific_config(project_name)
            if not project_config:
                raise HTTPException(
                    status_code=404,
                    detail=f"Project {project_name} not found in Redis. Please upload the project first."
                )

            env_config = project_config['env_config']
            minio_config = project_config['minio_config']
            training_options = project_config['training_config']
        else:
            raise HTTPException(
                status_code=400,
                detail="Either provide a complete training request or a project_name"
            )

        udb_path = env_config['udb_path']
        if not udb_path.startswith(('http://', 'https://', 's3://')):
            if not os.path.exists(udb_path):
                raise HTTPException(
                    status_code=400,
                    detail=f"UDB file not found: {udb_path}"
                )

        # Start the Celery task
        task = train_refactoring_model.delay(
            env_config=env_config,
            minio_config=minio_config,
            training_options=training_options
        )

        return TrainingResponse(
            task_id=task.id,
            status="PENDING",
            message="Training task started successfully",
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start training: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start training: {str(e)}")


@router.post("/train/project/{project_name}")
async def start_training_for_project(project_name: str, training_options: Optional[dict] = None):
    """
    Start training for a specific project using configuration from Redis and config files.
    """
    try:
        if get_integrated_config_manager is None:
            raise HTTPException(status_code=500, detail="Configuration system not available")

        config_manager = get_integrated_config_manager()

        # Get project configuration from Redis
        project_config = config_manager.get_project_specific_config(project_name)
        if not project_config:
            raise HTTPException(
                status_code=404,
                detail=f"Project {project_name} not found. Please upload the project first."
            )

        # Override training options if provided
        if training_options:
            project_config['training_config'].update(training_options)

        # Start the Celery task
        task = train_refactoring_model.delay(
            env_config=project_config['env_config'],
            minio_config=project_config['minio_config'],
            training_options=project_config['training_config']
        )

        # Store training task info in Redis
        redis_client = config_manager.redis_client
        redis_client.hset(
            f"training_task:{task.id}",
            mapping={
                'project_name': project_name,
                'task_id': task.id,
                'status': 'PENDING',
                'created_at': datetime.now().isoformat(),
                'config': json.dumps(project_config)
            }
        )

        # Add task to project's training history
        redis_client.sadd(f"project:{project_name}:training_tasks", task.id)

        return TrainingResponse(
            task_id=task.id,
            status="PENDING",
            message=f"Training started for project {project_name}",
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start training for project {project_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start training: {str(e)}")


# =============================================================================
# MODEL LOADING AND PREDICTION ENDPOINTS (NEW)
# =============================================================================

@router.post("/predict", response_model=PredictionResponse)
async def predict_refactoring_sequence(request: ModelPredictionRequest):
    """
    Load a trained model and predict optimal refactoring sequence for a project.
    """
    try:
        from application.celery_workers.model_prediction_task import predict_refactoring_sequence_task

        # Start prediction task
        task = predict_refactoring_sequence_task.delay(
            project_name=request.project_name,
            model_checkpoint=request.model_checkpoint,
            max_steps=request.max_steps,
            temperature=request.temperature
        )

        # Wait for task completion (with timeout)
        result = task.get(timeout=300)  # 5 minutes timeout

        return PredictionResponse(**result)

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/models/{project_name}")
async def list_available_models(project_name: str):
    """
    List all available trained models for a project.
    """
    try:
        if get_integrated_config_manager is None:
            raise HTTPException(status_code=500, detail="Configuration system not available")

        config_manager = get_integrated_config_manager()
        minio_config = config_manager.get_minio_config()

        from minio import Minio

        # Create MinIO client
        minio_client = Minio(
            endpoint=minio_config['endpoint'],
            access_key=minio_config['access_key'],
            secret_key=minio_config['secret_key'],
            secure=minio_config.get('secure', False)
        )

        # List model checkpoints for the project
        prefix = f"{project_name}/checkpoints/"
        objects = minio_client.list_objects(
            minio_config['results_bucket'],
            prefix=prefix,
            recursive=True
        )

        models = []
        for obj in objects:
            if obj.object_name.endswith('.pth'):
                models.append({
                    'checkpoint_path': obj.object_name,
                    'size': obj.size,
                    'last_modified': obj.last_modified.isoformat(),
                    'checkpoint_name': os.path.basename(obj.object_name)
                })

        # Sort by modification date (newest first)
        models.sort(key=lambda x: x['last_modified'], reverse=True)

        return {
            'project_name': project_name,
            'available_models': models,
            'total_count': len(models),
            'latest_model': models[0] if models else None
        }

    except Exception as e:
        logger.error(f"Failed to list models for {project_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")


@router.post("/models/{project_name}/load")
async def load_model_for_inference(project_name: str, checkpoint_path: Optional[str] = None):
    """
    Load a specific model checkpoint for inference.
    """
    try:
        from application.celery_workers.model_prediction_task import load_model_task

        # Start model loading task
        task = load_model_task.delay(
            project_name=project_name,
            checkpoint_path=checkpoint_path
        )

        result = task.get(timeout=120)  # 2 minutes timeout

        return {
            'project_name': project_name,
            'checkpoint_path': result['checkpoint_path'],
            'model_info': result['model_info'],
            'status': 'loaded',
            'message': 'Model loaded successfully',
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to load model for {project_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")


# =============================================================================
# STATUS AND MONITORING ENDPOINTS (Fixed)
# =============================================================================

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Get the status of a training task.
    """
    try:
        result = AsyncResult(task_id, app=app)  # Fixed: use celery_app

        response_data = {
            'task_id': task_id,
            'status': result.status,
            'timestamp': datetime.now().isoformat()
        }

        # Add progress information if available
        if result.info and isinstance(result.info, dict):
            response_data.update({
                'progress': result.info.get('progress'),
                'current_iteration': result.info.get('iteration'),
                'metrics': result.info.get('metrics'),
                'error': result.info.get('error')
            })

        return TaskStatusResponse(**response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get task status: {str(e)}")


@router.get("/projects/{project_name}/training-history")
async def get_project_training_history(project_name: str):
    """
    Get training history for a specific project.
    """
    try:
        if get_integrated_config_manager is None:
            return {"training_history": [], "message": "Config system not available"}

        config_manager = get_integrated_config_manager()
        redis_client = config_manager.redis_client

        # Get all training tasks for this project
        task_ids = redis_client.smembers(f"project:{project_name}:training_tasks")

        training_history = []
        for task_id in task_ids:
            task_info = redis_client.hgetall(f"training_task:{task_id}")
            if task_info:
                # Get current task status
                result = AsyncResult(task_id, app=app)
                task_info['current_status'] = result.status

                if result.info and isinstance(result.info, dict):
                    task_info.update({
                        'progress': result.info.get('progress'),
                        'current_iteration': result.info.get('iteration'),
                        'metrics': result.info.get('metrics')
                    })

                training_history.append(task_info)

        # Sort by creation time (newest first)
        training_history.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        return {
            'project_name': project_name,
            'training_history': training_history,
            'total_tasks': len(training_history)
        }

    except Exception as e:
        logger.error(f"Error getting training history for {project_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get training history: {str(e)}")


# =============================================================================
# CONFIGURATION ENDPOINTS (Fixed and Enhanced)
# =============================================================================

@router.get("/config/default")
async def get_default_config():
    """
    Get default configuration for training using integrated config system.
    """
    try:
        if get_integrated_config_manager is None:
            # Fallback to basic config
            return {
                "env_config": {
                    "project_name": "example_project",
                    "udb_path": "/app/jflex/jflex.udb",
                    "n_obj": 8,
                    "lower_band": 10,
                    "upper_bound": 50,
                    "population_size": 100,
                    "version_id": "v1.0",
                    "project_path": "/app/jflex"
                },
                "minio_config": {
                    "endpoint": os.getenv("MINIO_ENDPOINT", "minio:9000"),
                    "access_key": os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
                    "secret_key": os.getenv("MINIO_SECRET_KEY", "minioadmin"),
                    "secure": False,
                    "results_bucket": "ml-models"
                },
                "training_options": {
                    "frames_per_batch": 6000,
                    "n_iters": 10,
                    "max_steps": 100,
                    "use_normalization": True
                }
            }

        config_manager = get_integrated_config_manager()

        return {
            "env_config": config_manager.get_environment_config(),
            "minio_config": config_manager.get_minio_config(),
            "training_config": config_manager.get_training_config(),
            "ppo_config": config_manager.get_ppo_config(),
            "refactoring_config": config_manager.get_refactoring_config(),
            "understand_config": config_manager.get_understand_config(),
        }

    except Exception as e:
        logger.error(f"Error getting default config: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting default config: {str(e)}")


@router.get("/config/projects")
async def get_available_projects():
    """
    Get all available projects from Redis for configuration.
    """
    try:
        if get_integrated_config_manager is None:
            return {"projects": {}, "total_count": 0, "message": "Config system not available"}

        config_manager = get_integrated_config_manager()
        projects = config_manager.get_redis_project_configs()

        return {
            "status": "success",
            "projects": projects,
            "total_count": len(projects)
        }

    except Exception as e:
        logger.error(f"Error getting available projects: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting projects: {str(e)}")


@router.get("/config/project/{project_name}")
async def get_project_config(project_name: str):
    """
    Get complete configuration for a specific project.
    """
    try:
        if get_integrated_config_manager is None:
            raise HTTPException(status_code=500, detail="Configuration system not available")

        config_manager = get_integrated_config_manager()
        project_config = config_manager.get_project_specific_config(project_name)

        if not project_config:
            raise HTTPException(status_code=404, detail=f"Project {project_name} not found")

        return project_config

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project config for {project_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting project config: {str(e)}")


# =============================================================================
# EXISTING ENDPOINTS (Fixed)
# =============================================================================

@router.delete("/cancel/{task_id}")
async def cancel_training(task_id: str):
    """Cancel a running training task."""
    try:
        app.control.revoke(task_id, terminate=True)  # Fixed: use celery_app

        return {
            "task_id": task_id,
            "status": "CANCELLED",
            "message": "Training task cancelled",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel task: {str(e)}")


@router.get("/results/{project_name}")
async def get_training_results(project_name: str):
    """Get all training results for a project."""
    try:
        if get_integrated_config_manager is None:
            raise HTTPException(status_code=500, detail="Configuration system not available")

        config_manager = get_integrated_config_manager()
        minio_config = config_manager.get_minio_config()

        # Use the list_training_results task
        task = list_training_results.delay(
            minio_config=minio_config,
            project_name=project_name
        )

        # Wait for the task to complete
        result = task.get(timeout=30)

        if result['status'] != 'SUCCESS':
            raise HTTPException(status_code=500, detail="Failed to retrieve results")

        # Convert to response format
        training_results = []
        for obj in result['results']:
            path_parts = obj['object_name'].split('/')
            result_type = path_parts[1] if len(path_parts) > 1 else 'unknown'

            training_results.append({
                'object_name': obj['object_name'],
                'size': obj['size'],
                'last_modified': obj['last_modified'],
                'project_name': project_name,
                'result_type': result_type
            })

        return training_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get training results: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check basic service connectivity
        config_available = get_integrated_config_manager is not None
        
        # Try to create config manager to test Redis connectivity
        redis_status = "unknown"
        if config_available:
            try:
                config_manager = get_integrated_config_manager()
                config_manager.redis_client.ping()
                redis_status = "healthy"
            except Exception as redis_e:
                redis_status = f"unhealthy: {str(redis_e)}"

        # Skip Celery inspection for now to avoid connection issues
        return {
            "status": "healthy",
            "service": "ml-training",
            "redis_status": redis_status,
            "config_system": "available" if config_available else "unavailable",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "ml-training",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }