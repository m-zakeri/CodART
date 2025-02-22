from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict

router = APIRouter(prefix="/ml-training-tasks", tags=["ML Training Tasks"])


class TrainingRequest(BaseModel):
    dataset_path: str
    ds_number: int
    model_version: Optional[str] = None


@router.post("/start-training")
async def start_training_task(request: TrainingRequest):
    """
    Start a Celery training task
    """
    try:
        # Dispatch Celery task
        task = train_dataset_task.delay(
            dataset_path=request.dataset_path,
            ds_number=request.ds_number,
            model_version=request.model_version
        )

        return {
            "task_id": task.id,
            "status": "Task queued",
            "dataset_number": request.ds_number
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    Get status of a specific training task
    """
    try:
        # Get Celery task result
        task_result = AsyncResult(task_id)

        # Retrieve task metadata
        metadata = task_metadata.get(task_id, {})

        return {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result if task_result.ready() else None,
            "metadata": metadata
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/cancel-task/{task_id}")
async def cancel_training_task(task_id: str):
    """
    Cancel a running training task
    """
    try:
        # Revoke the Celery task
        train_dataset_task.AsyncResult(task_id).revoke(terminate=True)

        # Update task metadata
        if task_id in task_metadata:
            task_metadata[task_id]['status'] = 'CANCELLED'

        return {"status": "Task cancelled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))