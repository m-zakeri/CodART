from celery import Celery
from celery.result import AsyncResult
from application.services.minio_training_controller import ModelTrainingService
from fastapi import FastAPI, HTTPException, APIRouter
import os
from typing import List, Dict
from pydantic import BaseModel

# FastAPI app instance
app = APIRouter(prefix="/ml-training-tasks", tags=["ML Training Tasks"])


class DatasetInfo(BaseModel):
    name: str
    size: int
    last_modified: str
    path: str
    project_name: str
    metric_type: str


def get_minio_controller():
    return ModelTrainingService(
        minio_endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
        minio_access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        minio_secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
    )


@app.get("/metrics/api/v1/metrics", response_model=List[DatasetInfo])
async def get_all_metrics():
    """
    Retrieve all metrics from MinIO storage across all projects.
    """
    try:
        controller = get_minio_controller()
        bucket_name = os.getenv("MINIO_METRICS_BUCKET_NAME", "ml-models")
        metrics_list = []

        # List all objects in the metrics bucket
        objects = controller.minio_client.list_objects(bucket_name, recursive=True)

        for obj in objects:
            # Parse project name and metric type from the path
            path_parts = obj.object_name.split("/")
            if len(path_parts) >= 2:
                project_name = path_parts[0]
                metric_type = path_parts[1] if len(path_parts) > 1 else "unknown"

                metric_info = DatasetInfo(
                    name=obj.object_name,
                    size=obj.size,
                    last_modified=obj.last_modified.isoformat(),
                    path=f"/api/v1/metrics/{project_name}/{obj.object_name}",
                    project_name=project_name,
                    metric_type=metric_type,
                )
                metrics_list.append(metric_info)

        return metrics_list

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving metrics: {str(e)}"
        )


@app.get("/metrics/{project_name}")
async def get_project_metrics(project_name: str):
    """
    Retrieve all metrics for a specific project.
    """
    try:
        controller = get_minio_controller()
        bucket_name = os.getenv("MINIO_METRICS_BUCKET_NAME", "ml-models")
        metrics_list = []

        # List objects with project name prefix
        objects = controller.minio_client.list_objects(
            bucket_name, prefix=f"{project_name}/", recursive=True
        )

        for obj in objects:
            path_parts = obj.object_name.split("/")
            metric_type = path_parts[1] if len(path_parts) > 1 else "unknown"

            metric_info = DatasetInfo(
                name=obj.object_name,
                size=obj.size,
                last_modified=obj.last_modified.isoformat(),
                path=f"/api/v1/metrics/{project_name}/{obj.object_name}",
                project_name=project_name,
                metric_type=metric_type,
            )
            metrics_list.append(metric_info)

        if not metrics_list:
            raise HTTPException(
                status_code=404, detail=f"No metrics found for project {project_name}"
            )

        return metrics_list

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving project metrics: {str(e)}"
        )
