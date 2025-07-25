from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
from enum import Enum
import os
import io
import zipfile
import logging
from application.services.minio_training_controller import ModelTrainingService

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# FastAPI router instance - using the same prefix as export
router = APIRouter(tags=["Metrics Management"])


class MetricType(str, Enum):
    TESTABILITY = "testability"
    EVOSUITE = "evosuite"


def get_minio_controller():
    return ModelTrainingService(
        minio_endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
        minio_access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        minio_secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        bucket_name="metrics",
    )


@router.get("/metrics/{project_name}")
async def download_metrics(
    project_name: str,
    version_id: Optional[str] = None,
    metric_type: Optional[MetricType] = None,
):
    """
    Download metrics for a project. Can download specific metric type or all metrics as zip.
    """
    try:
        controller = get_minio_controller()
        metrics_bucket = "metrics"

        if version_id and metric_type:
            # Download specific metric file
            file_name = f"{project_name}_{metric_type}_{version_id}.csv"
            file_path = f"{project_name}/{version_id}/{file_name}"

            try:
                data = controller.minio_client.get_object(metrics_bucket, file_path)
                return StreamingResponse(
                    data,
                    media_type="text/csv",
                    headers={
                        "Content-Disposition": f'attachment; filename="{file_name}"'
                    },
                )
            except Exception as e:
                logger.error(f"Error downloading metric file: {str(e)}")
                raise HTTPException(
                    status_code=404, detail=f"Metric file not found: {file_path}"
                )

        else:
            # Download all metrics as zip
            try:
                prefix = (
                    f"{project_name}/{version_id}/"
                    if version_id
                    else f"{project_name}/"
                )
                objects = controller.minio_client.list_objects(
                    metrics_bucket, prefix=prefix, recursive=True
                )

                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for obj in objects:
                        # Filter by metric type if specified
                        if metric_type and f"_{metric_type}_" not in obj.object_name:
                            continue

                        data = controller.minio_client.get_object(
                            metrics_bucket, obj.object_name
                        ).read()

                        rel_path = obj.object_name.replace(f"{project_name}/", "", 1)
                        zip_file.writestr(rel_path, data)

                zip_buffer.seek(0)

                filename_parts = [project_name, "metrics"]
                if version_id:
                    filename_parts.append(version_id)
                if metric_type:
                    filename_parts.append(str(metric_type))
                filename = f"{'-'.join(filename_parts)}.zip"

                return StreamingResponse(
                    zip_buffer,
                    media_type="application/zip",
                    headers={
                        "Content-Disposition": f'attachment; filename="{filename}"'
                    },
                )
            except Exception as e:
                logger.error(f"Error creating metrics bundle: {str(e)}")
                raise HTTPException(
                    status_code=500, detail=f"Error creating metrics bundle: {str(e)}"
                )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error downloading metrics: {str(e)}"
        )


@router.get("/codesmells/{project_name}")
async def download_codesmells(project_name: str, version_id: Optional[str] = None):
    """
    Download code smells CSV for a project version.
    If version_id is provided, downloads the specific CSV file.
    Otherwise, downloads all code smells CSV files for the project as a zip.
    """
    try:
        controller = get_minio_controller()
        # Use environment variable MINIO_CODESMELLS_BUCKET or default to "code-smells" to match upload bucket
        codesmells_bucket = os.getenv("MINIO_CODESMELLS_BUCKET", "code-smells")

        if version_id:
            # Construct the file path based on project name and version_id
            file_path = f"{project_name}/{version_id}/code_smells_{project_name}_{version_id}.csv"
            file_name = f"code_smells_{project_name}_{version_id}.csv"
            try:
                data = controller.minio_client.get_object(codesmells_bucket, file_path)
                return StreamingResponse(
                    data,
                    media_type="text/csv",
                    headers={
                        "Content-Disposition": f'attachment; filename="{file_name}"'
                    },
                )
            except Exception as e:
                logger.error(f"Error downloading code smells file: {str(e)}")
                raise HTTPException(
                    status_code=404, detail=f"Code smells file not found: {file_path}"
                )
        else:
            # If no version_id is provided, download all code smells CSV files for this project as a zip
            # Files are stored in path format: {project_name}/{version_id}/code_smells_{project_name}_{version_id}.csv
            prefix = f"{project_name}/"
            objects = controller.minio_client.list_objects(
                codesmells_bucket, prefix=prefix, recursive=True
            )

            zip_buffer = io.BytesIO()
            file_found = False
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for obj in objects:
                    file_found = True
                    # Retrieve file contents and write into the zip using the object name as relative path
                    file_data = controller.minio_client.get_object(
                        codesmells_bucket, obj.object_name
                    ).read()
                    zip_file.writestr(obj.object_name, file_data)
                if not file_found:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No code smells files found for project {project_name}",
                    )
            zip_buffer.seek(0)
            zip_filename = f"{project_name}-codesmells.zip"
            return StreamingResponse(
                zip_buffer,
                media_type="application/zip",
                headers={
                    "Content-Disposition": f'attachment; filename="{zip_filename}"'
                },
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading code smells: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error downloading code smells: {str(e)}"
        )


@router.get("/models/{project_name}")
async def download_models(project_name: str, version_id: Optional[str] = None):
    """
    Download joblib model files for a project.
    """
    try:
        controller = get_minio_controller()
        # Models are stored in metrics bucket under models/ path
        models_bucket = "metrics"

        try:
            # Look for models in the training format: models/DS*/project_name/version_id/
            prefix = f"models/"
            objects = controller.minio_client.list_objects(
                models_bucket, prefix=prefix, recursive=True
            )

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                model_files_found = False
                for obj in objects:
                    # Check if this object is a joblib file for our project/version
                    if (obj.object_name.endswith(".joblib") and
                        project_name in obj.object_name and
                        (not version_id or version_id in obj.object_name)):
                        
                        model_files_found = True
                        logger.info(f"Found model file: {obj.object_name}")
                        
                        data = controller.minio_client.get_object(
                            models_bucket, obj.object_name
                        ).read()

                        # Use just the filename for the zip
                        filename = obj.object_name.split('/')[-1]
                        zip_file.writestr(filename, data)

            if not model_files_found:
                raise HTTPException(
                    status_code=404,
                    detail=f"No trained model files found for project '{project_name}'{f' version \'{version_id}\'' if version_id else ''}. Train testability models first.",
                )

            zip_buffer.seek(0)

            filename = (
                f"{project_name}-models{f'-{version_id}' if version_id else ''}.zip"
            )

            return StreamingResponse(
                zip_buffer,
                media_type="application/zip",
                headers={"Content-Disposition": f'attachment; filename="{filename}"'},
            )

        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logger.error(f"Error creating models bundle: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Error creating models bundle: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading models: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error downloading models: {str(e)}"
        )


@router.get("/joblib/{project_name}/{version_id}")
async def download_specific_joblib(
    project_name: str, version_id: str, metric_type: Optional[MetricType] = None
):
    """
    Download joblib model files for a specific project version.
    Creates a zip bundle of all available model files for that project.
    """
    try:
        controller = get_minio_controller()
        # Model files are stored in the metrics bucket under models/ path (not metrics/models/)
        models_bucket = "metrics"

        # Look for model files in the testability training format: models/DS*/project_name/version_id/
        # Pattern: models/DS{ds_number}/{project_name}/{version_id}/{model_type}_DS{ds_number}.joblib
        prefix = f"models/"
        
        try:
            objects = controller.minio_client.list_objects(
                models_bucket, prefix=prefix, recursive=True
            )

            zip_buffer = io.BytesIO()
            model_files_found = False
            
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for obj in objects:
                    # Check if this object is a joblib file for our project/version
                    obj_path_parts = obj.object_name.split('/')
                    if (len(obj_path_parts) >= 4 and 
                        obj.object_name.endswith(".joblib") and
                        project_name in obj.object_name and
                        version_id in obj.object_name):
                        
                        model_files_found = True
                        logger.info(f"Found model file: {obj.object_name}")
                        
                        # Download the model data
                        data = controller.minio_client.get_object(
                            models_bucket, obj.object_name
                        ).read()

                        # Use just the filename for the zip
                        filename = obj.object_name.split('/')[-1]
                        zip_file.writestr(filename, data)

            if not model_files_found:
                raise HTTPException(
                    status_code=404,
                    detail=f"No trained model files found for project '{project_name}' version '{version_id}'. Train testability models first."
                )

            zip_buffer.seek(0)
            filename = f"{project_name}-{version_id}-models.zip"

            return StreamingResponse(
                zip_buffer,
                media_type="application/zip",
                headers={"Content-Disposition": f'attachment; filename="{filename}"'},
            )

        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logger.error(f"Error creating joblib bundle: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Error creating joblib bundle: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading joblib files: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error downloading joblib files: {str(e)}"
        )
