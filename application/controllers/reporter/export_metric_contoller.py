from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from typing import List, Optional
from datetime import datetime
import understand as und
from codart.metrics.data_preparation_evo_suite_4 import PreProcess as PP
from codart.metrics.testability_prediction import PreProcess
import pandas as pd
import logging
from minio import Minio
import tempfile
import redis
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = APIRouter(prefix="/metrics", tags=["Metrics Management"])

# Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

# MinIO connection
minio_client = Minio(
    os.getenv('MINIO_ENDPOINT', 'minio:9000'),
    access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
    secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
    secure=False
)

# Ensure metrics bucket exists
METRICS_BUCKET = "metrics"
if not minio_client.bucket_exists(METRICS_BUCKET):
    minio_client.make_bucket(METRICS_BUCKET)


class MetricType(str, Enum):
    TESTABILITY = "testability"
    EVOSUITE = "evosuite"


class MetricExportConfig(BaseModel):
    project_name: str
    version_id: Optional[str] = None
    metric_types: List[MetricType]
    n_jobs: int = 1


class MetricInfo(BaseModel):
    project_name: str
    version_id: str
    metric_type: MetricType
    file_path: str
    created_at: str


def save_metric_info(metric_info: dict):
    """Save metric information to Redis"""
    key = f"metrics:{metric_info['project_name']}:{metric_info['version_id']}:{metric_info['metric_type']}"
    redis_client.hmset(key, metric_info)
    # Add to project metrics set
    redis_client.sadd(f"project:{metric_info['project_name']}:metrics", key)


def get_metric_info(project_name: str, version_id: str, metric_type: str) -> Optional[dict]:
    """Retrieve metric information from Redis"""
    key = f"metrics:{project_name}:{version_id}:{metric_type}"
    return redis_client.hgetall(key)


@app.post("/api/v1/metrics/export")
async def export_metrics(config: MetricExportConfig):
    """Export metrics for a project"""
    try:
        # Get project info from Redis
        if config.version_id:
            project_info = redis_client.hgetall(f"project:{config.project_name}:version:{config.version_id}")
        else:
            version_id = redis_client.get(f"project:{config.project_name}:latest")
            if not version_id:
                raise HTTPException(status_code=404, detail="Project not found")
            project_info = redis_client.hgetall(f"project:{config.project_name}:version:{version_id}")
            config.version_id = version_id

        if not project_info:
            raise HTTPException(status_code=404, detail="Project version not found")

        results = {}

        with tempfile.TemporaryDirectory() as temp_dir:
            for metric_type in config.metric_types:
                try:
                    metric_filename = f"{config.project_name}_{metric_type}_{config.version_id}.csv"
                    metric_path = os.path.join(temp_dir, metric_filename)

                    if metric_type == MetricType.TESTABILITY:
                        # Generate testability metrics
                        p = PreProcess()
                        df = p.compute_metrics_by_class_list(
                            project_path=project_info['db_path'],
                            n_jobs=config.n_jobs
                        )
                        df.to_csv(metric_path, index=False)

                    elif metric_type == MetricType.EVOSUITE:
                        # Generate EvoSuite metrics
                        evop = PP()
                        db = und.open(project_info['db_path'])
                        class_list = evop.extract_project_classes(db=db)

                        if not isinstance(class_list, pd.DataFrame):
                            class_list = pd.DataFrame(class_list)
                        if class_list.shape[1] == 1:
                            class_list.columns = ['Class']

                        df = evop.compute_metrics_by_class_list(
                            class_list=class_list,
                            csv_path=metric_path,
                            database=db,
                            project_name=config.project_name
                        )
                        df.to_csv(metric_path, index=False)
                        db.close()

                    # Upload to MinIO
                    minio_client.fput_object(
                        METRICS_BUCKET,
                        f"{config.project_name}/{config.version_id}/{metric_filename}",
                        metric_path
                    )

                    # Save metric info to Redis
                    metric_info = {
                        "project_name": config.project_name,
                        "version_id": config.version_id,
                        "metric_type": metric_type,
                        "file_path": f"{METRICS_BUCKET}/{config.project_name}/{config.version_id}/{metric_filename}",
                        "created_at": datetime.now().isoformat()
                    }
                    save_metric_info(metric_info)
                    results[metric_type] = metric_info

                except Exception as e:
                    logger.error(f"Error generating {metric_type} metrics: {str(e)}")
                    results[metric_type] = {"error": str(e)}

        return JSONResponse(
            status_code=200,
            content={
                "message": "Metrics exported successfully",
                "project_name": config.project_name,
                "version_id": config.version_id,
                "results": results
            }
        )

    except Exception as e:
        logger.error(f"Error exporting metrics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error exporting metrics: {str(e)}")


@app.get("/api/v1/metrics/{project_name}")
async def list_metrics(project_name: str, version_id: Optional[str] = None):
    """List all metrics for a project"""
    try:
        metrics = []
        if version_id:
            # Get metrics for specific version
            for metric_type in MetricType:
                metric_info = get_metric_info(project_name, version_id, metric_type)
                if metric_info:
                    metrics.append(metric_info)
        else:
            # Get all metrics for project
            metric_keys = redis_client.smembers(f"project:{project_name}:metrics")
            for key in metric_keys:
                metric_info = redis_client.hgetall(key)
                if metric_info:
                    metrics.append(metric_info)

        if not metrics:
            raise HTTPException(status_code=404, detail="No metrics found for project")

        return JSONResponse(content={"metrics": metrics})

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing metrics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error listing metrics: {str(e)}")


@app.delete("/api/v1/metrics/{project_name}")
async def delete_metrics(
        project_name: str,
        version_id: Optional[str] = None,
        metric_type: Optional[MetricType] = None
):
    """Delete metrics for a project"""
    try:
        if version_id and metric_type:
            # Delete specific metric
            metric_info = get_metric_info(project_name, version_id, metric_type)
            if not metric_info:
                raise HTTPException(status_code=404, detail="Metric not found")

            # Delete from MinIO
            minio_client.remove_object(METRICS_BUCKET, f"{project_name}/{version_id}/{metric_type}.csv")

            # Delete from Redis
            key = f"metrics:{project_name}:{version_id}:{metric_type}"
            await redis_client.delete(key)
            await redis_client.srem(f"project:{project_name}:metrics", key)

        else:
            # Delete all metrics for project or version
            metric_keys = redis_client.smembers(f"project:{project_name}:metrics")
            for key in metric_keys:
                metric_info = redis_client.hgetall(key)
                if metric_info:
                    if not version_id or metric_info['version_id'] == version_id:
                        # Delete from MinIO
                        try:
                            minio_client.remove_object(
                                METRICS_BUCKET,
                                f"{project_name}/{metric_info['version_id']}/{metric_info['metric_type']}.csv"
                            )
                        except Exception as e:
                            logger.warning(f"Error deleting file from MinIO: {str(e)}")

                        # Delete from Redis
                        await redis_client.delete(key)
                        await redis_client.srem(f"project:{project_name}:metrics", key)

        return JSONResponse(
            status_code=200,
            content={"message": f"Metrics deleted successfully for project {project_name}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting metrics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error deleting metrics: {str(e)}")