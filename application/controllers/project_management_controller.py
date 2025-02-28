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
import asyncio

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


async def create_understand_database(project_dir: str = None, db_dir: str = None):
    """
    Create understand database for the given project directory.

    Args:
        project_dir (str): The absolute path of project's directory.
        db_dir (str): The absolute directory path to save Understand database

    Returns:
        str: Understand database path
    """
    assert os.path.isdir(
        project_dir
    ), f"Project directory does not exist: {project_dir}"

    db_name = os.path.basename(os.path.normpath(project_dir))
    db_path = os.path.join(db_dir, f"{db_name}")  # Added .udb extension

    if os.path.exists(db_path):
        return db_path

    create_cmd = ["und", "create", "-languages", "java", db_path]
    db_path = db_path + ".und"
    # Second command: Add project files
    add_cmd = [
        "und",
        "add",
        project_dir,
        "-db",
        db_path,
    ]

    # Third command: Analyze the database
    analyze_cmd = ["und", "analyze", "-db", db_path, "-all"]

    commands = [create_cmd, add_cmd, analyze_cmd]

    try:
        for cmd in commands:
            # Using asyncio.create_subprocess_exec for async subprocess execution
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            # Await the process completion
            stdout, stderr = await process.communicate()

            # Convert bytes to string
            stdout_str = stdout.decode("utf-8")
            stderr_str = stderr.decode("utf-8")

            # Check if process was successful
            if process.returncode != 0:
                raise RuntimeError(
                    f"Command failed with return code {process.returncode}: {stderr_str}"
                )

            print(f'Successfully executed: {" ".join(cmd)}')
            print(f"Output: {stdout_str}")

        print("Understand project was created and analyzed successfully!")
        return db_path

    except asyncio.CancelledError:
        # Handle cancellation specifically
        print("Database creation was cancelled")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


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


@app.post("/projects/upload")
async def upload_project(
    file: UploadFile = File(...),
    project_name: str = Form(...),
    description: Optional[str] = Form(None),
    git_url: Optional[str] = Form(None),
    git_branch: Optional[str] = Form(None),
    git_commit: Optional[str] = Form(None),
):
    """Upload a project and create its Understand database"""
    try:
        # Generate version ID based on git information
        git_info = {
            "git_url": git_url,
            "git_branch": git_branch,
            "git_commit": git_commit,
        }
        version_id = generate_version_id(project_name, git_info)

        # Check if this exact version already exists
        if redis_client.exists(f"project:{project_name}:version:{version_id}"):
            raise HTTPException(
                status_code=400,
                detail="This exact version of the project already exists",
            )

        # Base directories for storing projects and databases
        base_projects_dir = os.getenv("PROJECTS_BASE_DIR", "/opt/projects")
        base_db_dir = os.getenv("DB_BASE_DIR", "/opt/understand_dbs")

        # Create version-specific directories
        project_dir = os.path.join(base_projects_dir, project_name, version_id)
        db_dir = os.path.join(base_db_dir, project_name, version_id)

        # Create directories if they don't exist
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(db_dir, exist_ok=True)

        # Save uploaded file
        file_path = os.path.join(project_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract if it's a zip file
        if file.filename.lower().endswith(".zip"):
            try:
                shutil.unpack_archive(file_path, project_dir, format="zip")
                os.remove(file_path)  # Remove the zip file after extraction
            except shutil.ReadError as e:
                raise HTTPException(status_code=400, detail="Invalid zip file format")

        # Create Understand database
        try:
            db_path = await create_understand_database(project_dir, db_dir)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create Understand database: {str(e)}",
            )

        # Save project information to Redis
        project_info = {
            "project_path": project_dir,
            "db_path": db_path,
            "upload_date": datetime.now().isoformat(),
            "description": description or "",
            "git_url": git_url or "",
            "git_branch": git_branch or "",
            "git_commit": git_commit or "",
        }
        save_project_info(project_name, version_id, project_info)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Project uploaded and analyzed successfully",
                "project_name": project_name,
                "version_id": version_id,
                "project_info": project_info,
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
