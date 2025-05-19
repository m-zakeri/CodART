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
router = APIRouter(prefix="/download", tags=["Metrics Management"])


class MetricType(str, Enum):
    TESTABILITY = "testability"
    EVOSUITE = "evosuite"


def get_minio_controller():
    return ModelTrainingService(
        minio_endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
        minio_access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        minio_secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
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
        # Use environment variable MINIO_CODESMELLS_BUCKET or default to "sonarqube-reports"
        codesmells_bucket = os.getenv("MINIO_CODESMELLS_BUCKET", "sonarqube-reports")

        if version_id:
            # Construct the file name based on project name and version_id
            file_name = f"code_smells_{project_name}_{version_id}.csv"
            try:
                data = controller.minio_client.get_object(codesmells_bucket, file_name)
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
                    status_code=404, detail=f"Code smells file not found: {file_name}"
                )
        else:
            # If no version_id is provided, download all code smells CSV files for this project as a zip
            # We assume that all files follow the naming pattern "code_smells_{project_name}_<version>.csv"
            prefix = f"code_smells_{project_name}_"
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
        models_bucket = os.getenv("MINIO_MODELS_BUCKET", "models")

        try:
            prefix = (
                f"{project_name}/{version_id}/" if version_id else f"{project_name}/"
            )
            objects = controller.minio_client.list_objects(
                models_bucket, prefix=prefix, recursive=True
            )

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                model_files_found = False
                for obj in objects:
                    if obj.object_name.endswith(".joblib"):
                        model_files_found = True
                        data = controller.minio_client.get_object(
                            models_bucket, obj.object_name
                        ).read()

                        rel_path = obj.object_name.replace(f"{project_name}/", "", 1)
                        zip_file.writestr(rel_path, data)

            if not model_files_found:
                raise HTTPException(
                    status_code=404,
                    detail=f"No model files found for project {project_name}",
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
    Download specific joblib file for a project version.
    """
    try:
        controller = get_minio_controller()
        models_bucket = os.getenv("MINIO_MODELS_BUCKET", "models")

        # Construct the joblib file path
        if metric_type:
            file_name = f"{project_name}_{metric_type}_{version_id}.joblib"
        else:
            file_name = f"{project_name}_{version_id}.joblib"

        file_path = f"{project_name}/{version_id}/{file_name}"

        try:
            data = controller.minio_client.get_object(models_bucket, file_path)
            return StreamingResponse(
                data,
                media_type="application/octet-stream",
                headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
            )
        except Exception as e:
            logger.error(f"Error downloading joblib file: {str(e)}")
            raise HTTPException(
                status_code=404, detail=f"Joblib file not found: {file_path}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading joblib file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error downloading joblib file: {str(e)}"
        )
