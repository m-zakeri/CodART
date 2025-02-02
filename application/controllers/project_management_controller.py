from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from typing import List, Dict, Optional
import tempfile
import shutil
from datetime import datetime
import understand as und
from codart.metrics.data_preparation_evo_suite_4 import PreProcess as PP
from codart.metrics.testability_prediction import PreProcess
import pandas as pd
import subprocess
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = APIRouter(prefix="/projects", tags=["Managing projects for analysis"])



class ProjectUploadConfig(BaseModel):
    project_name: str
    description: Optional[str] = None


class ExportConfig(BaseModel):
    project_name: str
    export_metrics: bool = True
    export_evo_metrics: bool = True
    n_jobs: int = 1


def git_restore(project_dir):
    """
        Git restore implementation
    """
    assert os.path.isdir(project_dir)
    assert os.path.isdir(os.path.join(project_dir, '.git'))
    subprocess.Popen(["git", "restore", "."], cwd=project_dir, stdout=open(os.devnull, 'wb')).wait()
    subprocess.Popen(["git", "clean", "-f", "-d"], cwd=project_dir, stdout=open(os.devnull, 'wb')).wait()


def create_understand_database(project_dir: str, db_dir: str) -> str:
    """Create Understand database"""
    db_name = os.path.basename(os.path.normpath(project_dir)) + ".und"
    db_path = os.path.join(db_dir, db_name)

    if os.path.exists(db_path):
        return db_path

    understand_cmd = ['und', 'create', '-db', db_path, '-languages', 'java']
    result = subprocess.run(understand_cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    if result.returncode != 0:
        error_ = result.stderr.decode('utf-8')
        logger.debug(f'return code: {result.returncode} msg: {error_}')
        raise Exception(f"Failed to create Understand database: {error_}")

    return db_path


@app.post("/api/projects/upload")
async def upload_project(
        file: UploadFile = File(...),
        config: ProjectUploadConfig = Body(...)
):
    """
    Upload a project and create its Understand database
    """
    try:
        # Create temporary directory for project
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            project_path = os.path.join(temp_dir, config.project_name)
            with open(project_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extract if it's a zip file
            if file.filename.endswith('.zip'):
                shutil.unpack_archive(project_path, temp_dir)

            # Create Understand database
            os.mkdir(project_path)
            db_dir = os.getenv('UNDERSTAND_DB_DIR', config.project_name+'.und')
            db_path = create_understand_database(temp_dir, db_dir)

            # Upload to MinIO
            controller = ModelTrainingController(
                minio_endpoint=os.getenv('MINIO_ENDPOINT', 'minio:9000'),
                minio_access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
                minio_secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
            )

            # Upload both project and database
            project_bucket = os.getenv('MINIO_PROJECT_BUCKET', 'projects')
            db_bucket = os.getenv('MINIO_DB_BUCKET', 'understand-dbs')

            metadata = {
                "description": config.description if config.description else "",
                "upload_date": datetime.now().isoformat(),
                "original_filename": file.filename
            }

            controller.minio_client.fput_object(
                project_bucket,
                config.project_name,
                project_path,
                metadata=metadata
            )

            controller.minio_client.fput_object(
                db_bucket,
                os.path.basename(db_path),
                db_path,
                metadata=metadata
            )

            return JSONResponse(
                status_code=200,
                content={
                    "message": "Project uploaded and analyzed successfully",
                    "project_name": config.project_name,
                    "db_path": db_path,
                    "metadata": metadata
                }
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing project: {str(e)}"
        )


@app.post("/api/datasets/export-metrics")
async def export_metrics(config: ExportConfig):
    """
    Export metrics for a project using both regular and EvoSuite processing
    """
    try:
        controller = ModelTrainingController(
            minio_endpoint=os.getenv('MINIO_ENDPOINT', 'minio:9000'),
            minio_access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            minio_secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin')
        )

        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Get project and database from MinIO
            project_bucket = os.getenv('MINIO_PROJECT_BUCKET', 'projects')
            db_bucket = os.getenv('MINIO_DB_BUCKET', 'understand-dbs')

            project_path = os.path.join(temp_dir, config.project_name)
            db_path = os.path.join(temp_dir, f"{config.project_name}.und")

            # Download project and database
            controller.minio_client.fget_object(project_bucket, config.project_name, project_path)
            controller.minio_client.fget_object(db_bucket, f"{config.project_name}.und", db_path)

            results = {}

            # Export regular metrics
            if config.export_metrics:
                metric_path = os.path.join(temp_dir, f"metrics_{config.project_name}.csv")
                p = PreProcess()
                df = p.compute_metrics_by_class_list(project_path=db_path, n_jobs=config.n_jobs)
                df.to_csv(metric_path, index=False)

                # Upload metrics to MinIO
                controller.minio_client.fput_object(
                    'datasets',
                    f"metrics_{config.project_name}.csv",
                    metric_path,
                    metadata={"type": "regular_metrics"}
                )
                results["metrics_path"] = f"metrics_{config.project_name}.csv"

            # Export EvoSuite metrics
            if config.export_evo_metrics:
                evo_metric_path = os.path.join(temp_dir, f"evo_metrics_{config.project_name}.csv")
                evop = PP()
                db = und.open(db_path)
                class_list = evop.extract_project_classes(db=db)

                if not isinstance(class_list, pd.DataFrame):
                    class_list = pd.DataFrame(class_list)
                if class_list.shape[1] == 1:
                    class_list.columns = ['Class']

                df = evop.compute_metrics_by_class_list(
                    class_list=class_list,
                    csv_path=evo_metric_path,
                    database=db,
                    project_name=config.project_name
                )
                df.to_csv(evo_metric_path, index=False)
                db.close()

                # Upload EvoSuite metrics to MinIO
                controller.minio_client.fput_object(
                    'datasets',
                    f"evo_metrics_{config.project_name}.csv",
                    evo_metric_path,
                    metadata={"type": "evo_metrics"}
                )
                results["evo_metrics_path"] = f"evo_metrics_{config.project_name}.csv"

            return JSONResponse(
                status_code=200,
                content={
                    "message": "Metrics exported successfully",
                    "project_name": config.project_name,
                    "results": results
                }
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting metrics: {str(e)}"
        )