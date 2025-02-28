from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from celery.result import AsyncResult
from application.celery_workers.ml_training_task import train_dataset_task
import redis
import os

router = APIRouter(prefix="/ml-training-tasks", tags=["ML Training Tasks"])

# Create a Redis client (adjust host/port as needed)
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
)


class TrainingRequest(BaseModel):
    dataset_path: str
    ds_number: int
    model_version: Optional[str] = None
    project_name: Optional[str] = None


def save_task_metadata(task_id: str, data: dict):
    """
    Save task metadata in Redis under the key 'task_metadata:<task_id>'.
    """
    redis_client.hset(f"task_metadata:{task_id}", mapping=data)


def get_task_metadata(task_id: str) -> dict:
    """
    Retrieve task metadata from Redis.
    """
    return redis_client.hgetall(f"task_metadata:{task_id}")


def get_all_task_metadata() -> list:
    """
    Retrieve metadata for all tasks stored in Redis.
    """
    keys = redis_client.keys("task_metadata:*")
    tasks = []
    for key in keys:
        # The key format is 'task_metadata:<task_id>'
        task_id = key.split(":", 1)[1]
        data = redis_client.hgetall(key)
        tasks.append(
            {
                "task_id": task_id,
                "dataset_number": data.get("ds_number"),
                "model_version": data.get("model_version"),
            }
        )
    return tasks


@router.post("/start-training")
async def start_training_task(request: TrainingRequest):
    """
    Start a Celery training task and save its metadata in Redis.
    """
    try:
        # Dispatch Celery task
        task = train_dataset_task.delay(
            dataset_path=request.dataset_path,
            ds_number=request.ds_number,
            model_version=request.model_version,
            project_name=request.project_name,
        )

        # Save task metadata to Redis
        save_task_metadata(
            task.id,
            {
                "ds_number": str(request.ds_number),
                "model_version": request.model_version or "",
                "project_name": request.project_name or "",
                "status": "QUEUED",
            },
        )

        return {
            "task_id": task.id,
            "status": "Task queued",
            "dataset_number": request.ds_number,
            "project_name": request.project_name,
            "model_version": request.model_version,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    Get the status of a specific training task along with its metadata from Redis.
    """
    try:
        # Get Celery task result
        task_result = AsyncResult(task_id)

        # Retrieve task metadata from Redis
        metadata = get_task_metadata(task_id)

        return {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result if task_result.ready() else None,
            "metadata": metadata,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/cancel-task/{task_id}")
async def cancel_training_task(task_id: str):
    """
    Cancel a running training task and update its metadata in Redis.
    """
    try:
        # Revoke the Celery task
        task = AsyncResult(task_id)
        task.revoke(terminate=True)

        # Update task metadata in Redis
        key = f"task_metadata:{task_id}"
        if redis_client.exists(key):
            redis_client.hset(key, "status", "CANCELLED")

        return {"status": "Task cancelled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-tasks")
async def get_all_tasks():
    """
    Get a list of all task IDs, dataset numbers, and model versions from Redis.
    """
    try:
        tasks = get_all_task_metadata()
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
