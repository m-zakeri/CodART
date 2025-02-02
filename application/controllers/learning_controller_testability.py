from celery import Celery
from celery.result import AsyncResult
from application.services.minio_training_controller import ModelTrainingController
from fastapi import FastAPI, HTTPException, APIRouter
import os
from typing import List, Dict
from pydantic import BaseModel

# FastAPI app instance
app =  APIRouter(prefix="/ml-training-tasks", tags=["ML Training Tasks"])



class DatasetInfo(BaseModel):
    name: str
    size: int
    last_modified: str
    path: str


@app.get("/api/datasets", response_model=List[DatasetInfo])
async def get_all_datasets():
    """
    Retrieve all datasets from MinIO storage.

    Returns:
        List[DatasetInfo]: List of dataset information including name, size, and last modified date
    """
    try:
        # Initialize MinIO Training Controller
        controller = ModelTrainingController(
            minio_endpoint=os.getenv('MINIO_ENDPOINT', 'minio:9000'),
            minio_access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            minio_secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
        )

        # Get bucket name from environment or use default
        bucket_name = os.getenv('MINIO_BUCKET_NAME', 'datasets')

        # List all objects in the datasets bucket
        datasets = []
        objects = controller.minio_client.list_objects(bucket_name)

        for obj in objects:
            dataset_info = DatasetInfo(
                name=obj.object_name,
                size=obj.size,
                last_modified=obj.last_modified.isoformat(),
                path=f"{bucket_name}/{obj.object_name}"
            )
            datasets.append(dataset_info)

        return datasets

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving datasets: {str(e)}"
        )


@app.get("/api/datasets/{dataset_name}")
async def get_dataset_details(dataset_name: str):
    """
    Get detailed information about a specific dataset.

    Args:
        dataset_name (str): Name of the dataset

    Returns:
        Dict: Detailed dataset information
    """
    try:
        controller = ModelTrainingController(
            minio_endpoint=os.getenv('MINIO_ENDPOINT', 'minio:9000'),
            minio_access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            minio_secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
        )

        bucket_name = os.getenv('MINIO_BUCKET_NAME', 'datasets')

        # Get object stats
        try:
            obj = controller.minio_client.stat_object(bucket_name, dataset_name)
            return {
                "name": obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified.isoformat(),
                "content_type": obj.content_type,
                "metadata": obj.metadata
            }
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset {dataset_name} not found"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving dataset details: {str(e)}"
        )