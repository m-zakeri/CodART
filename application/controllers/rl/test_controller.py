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
async def test_environment_specs(udb_path: str = None):
    """
    Test and return the environment specifications including observation, state, and reward specs

    Args:
        udb_path (str): Path to the UDB file
    """
    logger.debug(f"Received UDB path: {udb_path}")

    if not udb_path:
        raise HTTPException(status_code=400, detail="UDB path is required")

    # Normalize path
    udb_path = os.path.normpath(udb_path)
    logger.debug(f"Normalized UDB path: {udb_path}")

    # Verify the file exists
    if not os.path.exists(udb_path):
        raise HTTPException(
            status_code=404, detail=f"Database file not found at {udb_path}"
        )

    # Check file permissions
    try:
        with open(udb_path, "rb") as f:
            # Just check if we can open it
            pass
        logger.debug(f"File permissions check passed for {udb_path}")
    except PermissionError:
        raise HTTPException(
            status_code=403, detail=f"Permission denied when accessing {udb_path}"
        )
    except Exception as e:
        logger.error(f"Error checking file permissions: {str(e)}")

    try:
        logger.debug(
            f"Creating RefactoringSequenceEnvironment with udb_path={udb_path}"
        )
        env = RefactoringSequenceEnvironment(udb_path=udb_path)
        env.to(env.device)
        logger.debug("Checking environment specs")
        check_env_specs(env)
        logger.debug("Environment specs checked successfully")

        # Convert specs to serializable format
        observation_spec = str(env.observation_spec)
        state_spec = str(env.state_spec)
        reward_spec = str(env.reward_spec)

        return JSONResponse(
            {
                "observation_spec": observation_spec,
                "state_spec": state_spec,
                "reward_spec": reward_spec,
            }
        )
    except Exception as e:
        logger.error(f"Error testing environment: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error testing environment: {str(e)}"
        )
