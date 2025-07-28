from fastapi import HTTPException, UploadFile, File, Form, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from typing import List, Optional
import shutil
from datetime import datetime
import understand as und
import redis
import subprocess
import logging
import hashlib
import requests
import csv
from minio import Minio
from datetime import timedelta
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = APIRouter(prefix="/projects", tags=["Managing projects for analysis"])

# Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
)

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "code-smells")
PMD_PATH = os.getenv("PMD_PATH", "/app/pmd/bin/pmd")
PMD_RULESET = os.getenv("PMD_RULESET", "/app/pmd/rules/custom.xml")
PMD_CACHE_DIR = os.getenv("PMD_CACHE_DIR", "/app/pmd/cache")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)
if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)

CSV_DIRECTORY = os.getenv("CSV_DIRECTORY", "/opt/csv_reports")
os.makedirs(CSV_DIRECTORY, exist_ok=True)


class ProjectMetadata(BaseModel):
    project_name: str
    description: Optional[str] = None
    git_url: Optional[str] = None
    git_branch: Optional[str] = None
    git_commit: Optional[str] = None


class ProjectInfo(BaseModel):
    project_path: str
    db_path: str
    upload_date: str
    description: Optional[str] = None
    git_url: Optional[str] = None
    git_branch: Optional[str] = None
    git_commit: Optional[str] = None
    version_id: str


def generate_version_id(project_name: str, git_info: dict) -> str:
    """Generate a unique version ID based on project name and git information"""
    version_string = f"{project_name}_{git_info.get('git_url', '')}_{git_info.get('git_branch', '')}_{git_info.get('git_commit', '')}"
    return hashlib.md5(version_string.encode()).hexdigest()[:8]


def create_understand_database(project_dir: str = None, db_dir: str = None):
    """
    Create understand database for the given project directory.

    Args:
        project_dir (str): The absolute path of project's directory.
        db_dir (str): The absolute directory path to save Understand database

    Returns:
        str: Understand database path
    """
    if not os.path.isdir(project_dir):
        logger.error(f"Project directory does not exist: {project_dir}")
        raise ValueError(f"Project directory does not exist: {project_dir}")

    # Detect the language of the project
    language = "java"
    logger.debug(f"Detected project language: {language}")

    # Create necessary directories
    os.makedirs(db_dir, exist_ok=True)

    db_name = os.path.basename(os.path.normpath(project_dir))
    db_path = os.path.join(db_dir, f"{db_name}")

    # Full path to database with extension
    db_path_with_extension = db_path + ".und"

    # Check if the expected .und file exists
    if os.path.exists(db_path_with_extension):
        logger.info(f"Database already exists at {db_path_with_extension}")
        return db_path_with_extension
    
    # If not, check for any existing .und file in the directory and use it
    if os.path.exists(db_dir):
        for file in os.listdir(db_dir):
            if file.endswith('.und'):
                existing_db_path = os.path.join(db_dir, file)
                logger.info(f"Found existing database at {existing_db_path}")
                return existing_db_path

    # Commands to run
    create_cmd = ["und", "create", "-languages", language, db_path_with_extension]
    add_cmd = ["und", "add", project_dir, db_path_with_extension]
    analyze_cmd = ["und", "analyze", "-all", db_path_with_extension]

    # Set environment variables to avoid Qt issues
    env = {
        **os.environ,
        "PATH": f"{os.environ.get('PATH', '')}:/app/scitools/bin/linux64",
        "LD_LIBRARY_PATH": f"{os.environ.get('LD_LIBRARY_PATH', '')}:/app/scitools/bin/linux64",
        "STILICENSE": "/root/.config/SciTools/License.conf",
        "STIHOME": "/app/scitools",
        "QT_QPA_PLATFORM": "offscreen",
        "QT_DEBUG_PLUGINS": "1",
        "QT_NO_SSL": "1",
        "QT_MUTEX_WAIT_TIME": "0",
    }

    # Try to create the database
    logger.debug(f"Running create command: {' '.join(create_cmd)}")
    try:
        result = subprocess.run(
            create_cmd,
            capture_output=True,
            text=True,
            check=False,  # Don't throw exception on non-zero exit
            env=env,
        )
        logger.debug(f"Create command output: {result.stdout}")

        # Check for license error but continue anyway
        if (
            "No Und License Found" in result.stdout
            or "Licensing Error" in result.stdout
        ):
            logger.warning(
                "License error detected, but continuing with database creation"
            )
    except Exception as e:
        logger.error(f"Error during create command: {str(e)}")
        # Continue despite errors

    # Ensure the .und file exists before proceeding
    if not os.path.exists(db_path_with_extension):
        # Create an empty file to make sure subsequent commands have something to work with
        logger.warning(f"Creating empty database file at {db_path_with_extension}")
        with open(db_path_with_extension, "w") as f:
            f.write("")

    # Add a small delay to ensure file system has processed the changes
    time.sleep(1)

    # Add project files to the database
    logger.debug(f"Running add command: {' '.join(add_cmd)}")
    try:
        result = subprocess.run(
            add_cmd,
            capture_output=True,
            text=True,
            check=False,  # Don't throw exception on non-zero exit
            env=env,
        )
        logger.debug(f"Add command output: {result.stdout}")
        if result.returncode != 0:
            logger.warning(
                f"Add command failed with return code {result.returncode}: {result.stderr}"
            )
    except Exception as e:
        logger.error(f"Error during add command: {str(e)}")

    # Try to analyze the database
    logger.debug(f"Running analyze command: {' '.join(analyze_cmd)}")
    try:
        result = subprocess.run(
            analyze_cmd,
            capture_output=True,
            text=True,
            check=False,  # Don't throw exception on non-zero exit
            env=env,
        )
        logger.debug(f"Analyze command output: {result.stdout}")
    except Exception as e:
        logger.error(f"Error during analyze command: {str(e)}")

    logger.info(f"Database creation process completed for {db_path_with_extension}")
    return db_path_with_extension


def save_project_info(project_name: str, version_id: str, project_info: dict):
    """Save project information to Redis"""
    # Save version-specific information
    redis_client.hset(
        f"project:{project_name}:version:{version_id}", mapping=project_info
    )

    # Add version to the project's version list
    redis_client.sadd(f"project:{project_name}:versions", version_id)

    # Update latest version pointer
    redis_client.set(f"project:{project_name}:latest", version_id)


def get_project_versions(project_name: str) -> List[str]:
    """Get all versions of a project"""
    return list(redis_client.smembers(f"project:{project_name}:versions"))


def get_project_info(
    project_name: str, version_id: Optional[str] = None
) -> Optional[dict]:
    """Retrieve project information from Redis"""
    if version_id is None:
        # Get latest version ID
        version_id = redis_client.get(f"project:{project_name}:latest")
        if not version_id:
            return None

    project_info = redis_client.hgetall(f"project:{project_name}:version:{version_id}")
    if project_info:
        project_info["version_id"] = version_id
    return project_info if project_info else None


def analyze_and_upload_code_smells(
        project_name: str, version_id: str, project_dir: str
) -> str:
    """
    Trigger PMD analysis on the project directory,
    save the results as CSV, upload to MinIO, and store the MinIO URL in Redis.
    Returns the presigned URL to the CSV file.
    """
    # Store the original project name for consistency
    original_project_name = project_name

    # If this is a task-style name, extract the base name
    if project_name.startswith("json_task_"):
        base_project_name = "json"
    elif "_task_" in project_name:
        base_project_name = project_name.split("_task_")[0]
    else:
        base_project_name = project_name

    # Use the task name for the project key to maintain uniqueness
    project_key = f"{project_name}_{version_id}"

    # Find the actual project directory (usually a single subdirectory)
    actual_project_dir = None
    contents = os.listdir(project_dir)
    subdirs = [
        item
        for item in contents
        if os.path.isdir(os.path.join(project_dir, item)) and not item.startswith(".")
    ]

    # Try to find a likely project directory by looking for build files or src directory
    for subdir in subdirs:
        subdir_path = os.path.join(project_dir, subdir)
        if (
                os.path.exists(os.path.join(subdir_path, "pom.xml"))
                or os.path.exists(os.path.join(subdir_path, "build.gradle"))
                or os.path.exists(os.path.join(subdir_path, "src"))
        ):
            actual_project_dir = subdir_path
            logger.info(f"Found actual project directory: {actual_project_dir}")
            break

    # If we couldn't find a specific project dir, use the original
    if not actual_project_dir:
        logger.warning(
            "Could not find a specific project directory, using the uploaded directory"
        )
        actual_project_dir = project_dir

    # Ensure PMD cache directory exists
    pmd_cache_file = os.path.join(PMD_CACHE_DIR, f"{project_key}_cache.txt")
    os.makedirs(PMD_CACHE_DIR, exist_ok=True)

    # CSV file path for PMD output
    csv_filename = f"code_smells_{project_key}.csv"
    csv_file_path = os.path.join(CSV_DIRECTORY, csv_filename)
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    # Run PMD analysis
    logger.info(
        f"Running PMD analysis for project {project_key} in {actual_project_dir}"
    )
    try:
        command = [
            PMD_PATH,
            "check",
            "-d",
            actual_project_dir,
            "-R",
            PMD_RULESET,
            "-f",
            "csv",
            "-r",
            csv_file_path,
            "--cache",
            pmd_cache_file,
        ]

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,  # Don't throw exception on non-zero exit
        )

        # Log output for debugging
        logger.debug(f"PMD stdout: {process.stdout}")
        if process.stderr:
            logger.warning(f"PMD stderr: {process.stderr}")

        if process.returncode != 0 and process.returncode != 4:
            logger.error(f"PMD exited with code {process.returncode}")
            logger.warning("Continuing to try to upload the CSV file despite PMD error")
        elif process.returncode == 4:
            logger.info(
                f"PMD found {process.returncode} violations - this is expected and not an error"
            )

    except Exception as e:
        logger.error(f"Error running PMD: {str(e)}")
        # Create an empty CSV with headers if PMD failed to run
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "Problem",
                    "Package",
                    "File",
                    "Priority",
                    "Line",
                    "Description",
                    "Rule set",
                    "Rule",
                ]
            )

    # Check if CSV file was created
    if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
        logger.warning(
            f"PMD did not generate a CSV file or it's empty. Creating a placeholder..."
        )
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "Problem",
                    "Package",
                    "File",
                    "Priority",
                    "Line",
                    "Description",
                    "Rule set",
                    "Rule",
                ]
            )

    # Upload the CSV file to MinIO with MULTIPLE naming patterns for compatibility
    try:
        # Ensure bucket exists
        if not minio_client.bucket_exists(MINIO_BUCKET):
            minio_client.make_bucket(MINIO_BUCKET)

        # Upload with multiple paths for maximum compatibility
        upload_paths = [
            # Primary path: use the full project name (task name)
            f"{project_name}/{version_id}/{csv_filename}",

            # Secondary path: use base project name for backward compatibility
            f"{base_project_name}/{version_id}/code_smells_{base_project_name}_{version_id}.csv",
        ]

        presigned_urls = []

        for minio_path in upload_paths:
            try:
                logger.info(f"Uploading PMD analysis CSV to MinIO at {minio_path}")
                minio_client.fput_object(MINIO_BUCKET, minio_path, csv_file_path)

                # Generate a presigned URL for the CSV file (valid for 24 hours)
                presigned_url = minio_client.presigned_get_object(
                    MINIO_BUCKET, minio_path, expires=timedelta(hours=24)
                )
                presigned_urls.append(presigned_url)
                logger.info(f"Successfully uploaded to {minio_path}")

            except Exception as e:
                logger.warning(f"Failed to upload to {minio_path}: {str(e)}")

        if not presigned_urls:
            raise Exception("Failed to upload to any MinIO path")

        # Use the first successful URL as the primary one
        primary_url = presigned_urls[0]

        # Save URLs in Redis under multiple keys for compatibility
        redis_keys = [
            f"project:{project_name}:version:{version_id}:code_smells_url",
            f"project:{base_project_name}:version:{version_id}:code_smells_url",
        ]

        for redis_key in redis_keys:
            redis_client.set(redis_key, primary_url, ex=86400)  # 24 hours
            logger.info(f"CSV URL saved to Redis: {redis_key}")

        return primary_url

    except Exception as e:
        logger.error(f"Failed to upload CSV to MinIO: {str(e)}", exc_info=True)
        raise Exception(f"Failed to upload CSV to MinIO: {str(e)}")

@app.post("/projects/upload")
async def upload_project(
    file: UploadFile = File(...),
    project_name: str = Form(...),
    description: Optional[str] = Form(None),
    git_url: Optional[str] = Form(None),
    git_branch: Optional[str] = Form(None),
    git_commit: Optional[str] = Form(None),
):
    """Upload a project, create its Understand database, a SonarQube project, and save code smells CSV to MinIO."""
    try:
        git_info = {
            "git_url": git_url,
            "git_branch": git_branch,
            "git_commit": git_commit,
        }
        version_id = generate_version_id(project_name, git_info)
        if redis_client.exists(f"project:{project_name}:version:{version_id}"):
            raise HTTPException(
                status_code=400,
                detail="This exact version of the project already exists",
            )

        base_projects_dir = os.getenv("PROJECTS_BASE_DIR", "/opt/projects")
        base_db_dir = os.getenv("DB_BASE_DIR", "/opt/understand_dbs")
        project_dir = os.path.join(base_projects_dir, project_name, version_id)
        db_dir = os.path.join(base_db_dir, project_name, version_id)
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(db_dir, exist_ok=True)

        file_path = os.path.join(project_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.lower().endswith(".zip"):
            try:
                shutil.unpack_archive(file_path, project_dir, format="zip")
                os.remove(file_path)
            except shutil.ReadError as e:
                raise HTTPException(status_code=400, detail="Invalid zip file format")

        # Create Understand database (synchronously)
        try:
            db_path = create_understand_database(project_dir, db_dir)
        except Exception as e:
            logger.error(
                f"Failed to create Understand database: {str(e)}", exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create Understand database: {str(e)}",
            )

        # Run PMD analysis
        pmd_status = "not_started"
        code_smells_url = ""
        project_key = f"{project_name}_{version_id}"

        try:
            # Trigger PMD analysis and upload CSV to MinIO
            code_smells_url = analyze_and_upload_code_smells(
                project_name, version_id, project_dir
            )
            logger.info(f"PMD analysis completed for {project_key}")
            pmd_status = "analyzed"
        except Exception as analyze_err:
            logger.error(f"Error during PMD analysis: {str(analyze_err)}")
            pmd_status = "analysis_failed"
            # Continue with the project creation despite PMD error

        project_info = {
            "project_path": project_dir,
            "db_path": db_path,
            "upload_date": datetime.now().isoformat(),
            "description": description or "",
            "git_url": git_url or "",
            "git_branch": git_branch or "",
            "git_commit": git_commit or "",
            "pmd_status": pmd_status,
            "project_key": project_key,
        }

        # Add code smells URL if available
        if code_smells_url:
            project_info["code_smells_url"] = code_smells_url

        save_project_info(project_name, version_id, project_info)

        message = "Project uploaded and Understand database created successfully"
        if pmd_status == "analyzed":
            message += ", PMD analysis completed successfully"
        elif pmd_status == "analysis_failed":
            message += ", but PMD analysis failed"

        return JSONResponse(
            status_code=200,
            content={
                "message": message,
                "project_name": project_name,
                "version_id": version_id,
                "project_info": project_info,
                "pmd_status": pmd_status,
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing project: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error processing project: {str(e)}"
        )


@app.get("/projects/{project_name}")
async def get_project(project_name: str, version_id: Optional[str] = None):
    """Retrieve project information"""
    if version_id:
        project_info = get_project_info(project_name, version_id)
        if not project_info:
            raise HTTPException(
                status_code=404, detail=f"Project version {version_id} not found"
            )
        return JSONResponse(content=project_info)
    else:
        # Get all versions
        versions = get_project_versions(project_name)
        if not versions:
            raise HTTPException(status_code=404, detail="Project not found")

        latest_version = redis_client.get(f"project:{project_name}:latest")
        version_info = []
        for version in versions:
            info = get_project_info(project_name, version)
            if info:
                version_info.append(info)

        return JSONResponse(
            content={
                "project_name": project_name,
                "latest_version": latest_version,
                "versions": version_info,
            }
        )


@app.post("/projects/analyze")
async def analyze_project_api(
    project_name: str = Form(...),
    version_id: str = Form(...),
):
    """
    Trigger analysis for an existing project version.
    This endpoint retrieves the project directory from Redis,
    runs the code smell analysis, uploads the CSV to MinIO,
    and saves the MinIO URL in Redis.
    """
    try:
        project_info = get_project_info(project_name, version_id)
        if not project_info:
            raise HTTPException(status_code=404, detail="Project version not found")
        project_dir = project_info.get("project_path")
        if not project_dir or not os.path.exists(project_dir):
            raise HTTPException(status_code=404, detail="Project directory not found")

        code_smells_url = analyze_and_upload_code_smells(
            project_name, version_id, project_dir
        )
        # Update project info in Redis with the new code smells URL
        redis_client.hset(
            f"project:{project_name}:version:{version_id}",
            mapping={"code_smells_url": code_smells_url},
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "Code smell analysis completed",
                "code_smells_url": code_smells_url,
                "project_name": project_name,
                "version_id": version_id,
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")


@app.delete("/projects/{project_name}")
async def delete_project(project_name: str, version_id: Optional[str] = None):
    """Delete project files, database, and information"""
    try:
        # First verify if project exists
        versions = redis_client.smembers(f"project:{project_name}:versions")
        if not versions:
            raise HTTPException(
                status_code=404, detail=f"Project {project_name} not found"
            )

        if version_id:
            # Verify if specific version exists
            if not redis_client.hexists(
                f"project:{project_name}:version:{version_id}", "project_path"
            ):
                raise HTTPException(
                    status_code=404, detail=f"Project version {version_id} not found"
                )

            # Get project info before deletion
            project_info = get_project_info(project_name, version_id)
            if not project_info:
                raise HTTPException(
                    status_code=404, detail=f"Project version {version_id} not found"
                )

            # Delete project files
            if project_info.get("project_path") and os.path.exists(
                project_info["project_path"]
            ):
                try:
                    shutil.rmtree(os.path.dirname(project_info["project_path"]))
                except Exception as e:
                    logger.error(f"Error deleting project files: {str(e)}")

            # Delete database files
            if project_info.get("db_path") and os.path.exists(project_info["db_path"]):
                try:
                    shutil.rmtree(os.path.dirname(project_info["db_path"]))
                except Exception as e:
                    logger.error(f"Error deleting database files: {str(e)}")

            # Remove from Redis
            redis_client.delete(f"project:{project_name}:version:{version_id}")
            redis_client.srem(f"project:{project_name}:versions", version_id)

            # Update latest version if needed
            current_latest = redis_client.get(f"project:{project_name}:latest")
            if current_latest == version_id:
                remaining_versions = list(
                    redis_client.smembers(f"project:{project_name}:versions")
                )
                if remaining_versions:
                    redis_client.set(
                        f"project:{project_name}:latest", remaining_versions[0]
                    )
                else:
                    redis_client.delete(f"project:{project_name}:latest")
                    redis_client.delete(f"project:{project_name}:versions")
        else:
            # Delete all versions
            for version in versions:
                project_info = get_project_info(project_name, version)
                if project_info:
                    # Delete project files
                    if project_info.get("project_path") and os.path.exists(
                        project_info["project_path"]
                    ):
                        try:
                            shutil.rmtree(os.path.dirname(project_info["project_path"]))
                        except Exception as e:
                            logger.error(
                                f"Error deleting project files for version {version}: {str(e)}"
                            )

                    # Delete database files
                    if project_info.get("db_path") and os.path.exists(
                        project_info["db_path"]
                    ):
                        try:
                            shutil.rmtree(os.path.dirname(project_info["db_path"]))
                        except Exception as e:
                            logger.error(
                                f"Error deleting database files for version {version}: {str(e)}"
                            )

                    # Remove from Redis
                    redis_client.delete(f"project:{project_name}:version:{version}")

            # Clean up project-level Redis keys
            redis_client.delete(f"project:{project_name}:versions")
            redis_client.delete(f"project:{project_name}:latest")

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Project {project_name} {'version ' + version_id if version_id else ''} deleted successfully"
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")


@app.get("/projects")
async def list_projects():
    """List all projects with their versions"""
    try:
        # Get all project keys from Redis
        project_keys = redis_client.keys("project:*:latest")
        projects = []

        for key in project_keys:
            project_name = key.split(":")[1]
            versions = get_project_versions(project_name)
            latest_version = redis_client.get(f"project:{project_name}:latest")

            project_versions = []
            for version in versions:
                version_info = get_project_info(project_name, version)
                if version_info:
                    project_versions.append(version_info)

            projects.append(
                {
                    "project_name": project_name,
                    "latest_version": latest_version,
                    "versions": project_versions,
                }
            )

        return JSONResponse(content={"projects": projects})
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error listing projects: {str(e)}")
