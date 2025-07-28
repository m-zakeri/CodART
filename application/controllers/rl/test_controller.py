from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from torchrl.envs.utils import check_env_specs
from codart.learner.tests.test_reinforcement.environment import (
    RefactoringSequenceEnvironment,
)
import os
import logging
import understand as und
import subprocess

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Update the router configuration
router = APIRouter(
    prefix="/environment",  # Fixed API path to include the full prefix
    tags=["Environment Testing"],
)


@router.post("/test-specs")
async def test_environment_specs(
        udb_path: str = None,
        project_name: str = "",
        version_id: str = "",
        project_path: str = "",
):
    """Test environment specs with timeout protection"""
    import asyncio

    logger.debug(f"Received UDB path: {udb_path}")

    if not udb_path:
        raise HTTPException(status_code=400, detail="UDB path is required")

    udb_path = os.path.normpath(udb_path)
    logger.debug(f"Normalized UDB path: {udb_path}")

    if not os.path.exists(udb_path):
        raise HTTPException(
            status_code=404, detail=f"Database file not found at {udb_path}"
        )

    try:
        # Add timeout to the environment creation
        logger.debug(f"Creating RefactoringSequenceEnvironment with udb_path={udb_path}")

        # Use asyncio.wait_for to add timeout to the environment creation
        env = await asyncio.wait_for(
            asyncio.to_thread(
                RefactoringSequenceEnvironment,
                udb_path=udb_path,
                project_name=project_name,
                version_id=version_id,
                project_path=project_path,
            ),
            timeout=120.0  # 2 minute timeout
        )

        env.to(env.device)
        logger.debug("Checking environment specs")

        # Add timeout to spec checking
        await asyncio.wait_for(
            asyncio.to_thread(check_env_specs, env),
            timeout=30.0  # 30 second timeout
        )

        logger.debug("Environment specs checked successfully")

        # Convert specs to serializable format
        observation_spec = str(env.observation_spec)
        state_spec = str(env.state_spec)
        reward_spec = str(env.reward_spec)

        return JSONResponse({
            "observation_spec": observation_spec,
            "state_spec": state_spec,
            "reward_spec": reward_spec,
        })

    except asyncio.TimeoutError:
        logger.error("Environment testing timed out")
        raise HTTPException(
            status_code=408, detail="Environment testing timed out"
        )
    except Exception as e:
        logger.error(f"Error testing environment: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error testing environment: {str(e)}"
        )