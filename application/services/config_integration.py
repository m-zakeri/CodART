# config_integration.py - Fixed configuration system that integrates with your existing setup

import os
import configparser
import redis
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class IntegratedConfigManager:
    """
    Integrated configuration manager that works with your existing setup:
    - Reads from INI configuration files (config.ini)
    - Uses your Redis infrastructure
    - Integrates with Docker environment variables
    """

    def __init__(self):
        self.redis_client = self._setup_redis()
        self.config_parser = configparser.ConfigParser()
        self._load_configurations()

    def _setup_redis(self):
        """Setup Redis connection using your existing configuration"""
        return redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True,
        )

    def _load_configurations(self):
        """Load configuration from multiple sources"""
        # Load only INI configuration files - skip Python files
        config_paths = [
            "config.ini",  # Root config
            "/app/config.ini",  # Docker container config
            os.path.expanduser("~/.codart/config.ini"),  # User config
        ]

        for path in config_paths:
            if os.path.exists(path):
                try:
                    # Only read INI files with ConfigParser
                    if path.endswith('.ini'):
                        self.config_parser.read(path)
                        logger.info(f"Loaded configuration from {path}")
                    else:
                        logger.debug(f"Skipping non-INI file: {path}")
                except Exception as e:
                    logger.warning(f"Failed to load config from {path}: {e}")

    def get_training_config(self) -> Dict[str, Any]:
        """Get training configuration from your existing setup"""
        try:
            return {
                'frames_per_batch': self.config_parser.getint("TRAINING", "frames_per_batch", fallback=6000),
                'n_iters': self.config_parser.getint("TRAINING", "n_iters", fallback=10),
                'num_epochs': self.config_parser.getint("TRAINING", "num_epochs", fallback=30),
                'minibatch_size': self.config_parser.getint("TRAINING", "minibatch_size", fallback=400),
                'learning_rate': self.config_parser.getfloat("TRAINING", "learning_rate", fallback=0.0003),
                'max_grad_norm': self.config_parser.getfloat("TRAINING", "max_grad_norm", fallback=1.0),
                'max_steps': self.config_parser.getint("TRAINING", "max_steps", fallback=100),
                'torch_manual_seed': self.config_parser.getint("TRAINING", "torch_manual_seed", fallback=0),
                'save_interval': 100,  # Add missing intervals
                'evaluation_interval': 50,
            }
        except Exception as e:
            logger.error(f"Error loading training config: {e}")
            return self._get_fallback_training_config()

    def get_ppo_config(self) -> Dict[str, Any]:
        """Get PPO configuration"""
        try:
            return {
                'clip_epsilon': self.config_parser.getfloat("PPO", "clip_epsilon", fallback=0.2),
                'gamma': self.config_parser.getfloat("PPO", "gamma", fallback=0.99),
                'lambda': self.config_parser.getfloat("PPO", "lambda", fallback=0.9),
                'entropy_eps': self.config_parser.getfloat("PPO", "entropy_eps", fallback=0.0001),
                'depth': self.config_parser.getint("PPO", "depth", fallback=2),
                'num_cells': self.config_parser.getint("PPO", "num_cells", fallback=256),
                'share_parameters_critic': self.config_parser.getboolean("PPO", "share_parameters_critic",
                                                                         fallback=True),
            }
        except Exception as e:
            logger.error(f"Error loading PPO config: {e}")
            return self._get_fallback_ppo_config()

    def get_environment_config(self, project_name: str = None) -> Dict[str, Any]:
        """Get environment configuration using your existing Config section"""
        try:
            # Use your existing [Config] section structure
            base_config = {
                'project_name': project_name or self.config_parser.get("Config", "PROJECT_NAME", fallback="JSON"),
                'udb_path': self._resolve_udb_path(),
                'n_obj': self.config_parser.getint("Config", "OBJECTIVE", fallback=8),
                'lower_band': self.config_parser.getint("Config", "LOWER_BAND", fallback=10),
                'upper_bound': self.config_parser.getint("Config", "UPPER_BAND", fallback=50),
                'population_size': self.config_parser.getint("Config", "POPULATION_SIZE", fallback=100),
                'version_id': "v1.0",
                'project_path': self._resolve_project_path(),
                'evaluate_in_parallel': self.config_parser.getboolean("Config", "evaluate_in_parallel", fallback=True),
                'verbose_design_metrics': self.config_parser.getboolean("Config", "verbose_design_metrics",
                                                                        fallback=True),
            }

            # Override with environment variables if present
            env_overrides = {
                'project_name': 'CODART_PROJECT_NAME',
                'udb_path': 'CODART_UDB_PATH',
                'project_path': 'CODART_PROJECT_PATH',
            }

            for key, env_var in env_overrides.items():
                if env_var in os.environ:
                    base_config[key] = os.environ[env_var]

            return base_config

        except Exception as e:
            logger.error(f"Error loading environment config: {e}")
            return self._get_fallback_environment_config(project_name)

    def _resolve_udb_path(self) -> str:
        """Resolve UDB path from your configuration"""
        try:
            # Try to get from Config section
            db_address = self.config_parser.get("Config", "db_address", fallback="/app/jflex")
            db_name = self.config_parser.get("Config", "db_name", fallback="jflex.udb")
            return os.path.join(db_address, db_name)
        except Exception as e:
            print(e)
            return "/app/jflex/jflex.udb"

    def _resolve_project_path(self) -> str:
        """Resolve project path from your configuration"""
        try:
            return self.config_parser.get("Config", "repo_address", fallback="/app/jflex")
        except Exception as e:
            print(e)
            return "/app/jflex"

    def get_minio_config(self) -> Dict[str, Any]:
        """Get MinIO configuration using your Docker environment"""
        return {
            'endpoint': os.getenv('MINIO_ENDPOINT', 'minio:9000'),
            'access_key': os.getenv('MINIO_ACCESS_KEY', '00jFBl7n9Jn0ex0XL7m1'),
            'secret_key': os.getenv('MINIO_SECRET_KEY', 'kYfujzkdSGjXKLN9oQhPDIVgRUaZRijvj1yaXmIZ'),
            'secure': False,
            'results_bucket': 'ml-models',
            'metrics_bucket': os.getenv('MINIO_CODESMELLS_BUCKET', 'code-smells'),
        }

    def get_redis_project_configs(self) -> Dict[str, Any]:
        """Get project configurations stored in Redis"""
        try:
            # Get all project keys
            project_keys = self.redis_client.keys("project:*:latest")
            projects = {}

            for key in project_keys:
                project_name = key.split(":")[1]
                latest_version = self.redis_client.get(f"project:{project_name}:latest")

                if latest_version:
                    project_info = self.redis_client.hgetall(f"project:{project_name}:version:{latest_version}")
                    if project_info:
                        projects[project_name] = {
                            'project_name': project_name,
                            'version_id': latest_version,
                            'udb_path': project_info.get('db_path', ''),
                            'project_path': project_info.get('project_path', ''),
                            'description': project_info.get('description', ''),
                            'upload_date': project_info.get('upload_date', ''),
                        }

            return projects

        except Exception as e:
            logger.error(f"Error getting Redis project configs: {e}")
            return {}

    def get_project_specific_config(self, project_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific project from Redis"""
        try:
            latest_version = self.redis_client.get(f"project:{project_name}:latest")
            if not latest_version:
                return None

            project_info = self.redis_client.hgetall(f"project:{project_name}:version:{latest_version}")
            if not project_info:
                return None

            # Create complete config for this project
            env_config = self.get_environment_config(project_name)
            env_config.update({
                'project_name': project_name,
                'version_id': latest_version,
                'udb_path': project_info.get('db_path', env_config['udb_path']),
                'project_path': project_info.get('project_path', env_config['project_path']),
            })

            return {
                'env_config': env_config,
                'minio_config': self.get_minio_config(),
                'training_config': self.get_training_config(),
                'ppo_config': self.get_ppo_config(),
                'project_metadata': {
                    'description': project_info.get('description', ''),
                    'upload_date': project_info.get('upload_date', ''),
                    'git_url': project_info.get('git_url', ''),
                    'git_branch': project_info.get('git_branch', ''),
                    'git_commit': project_info.get('git_commit', ''),
                }
            }

        except Exception as e:
            logger.error(f"Error getting project specific config: {e}")
            return None

    def get_refactoring_config(self) -> Dict[str, Any]:
        """Get refactoring configuration"""
        try:
            refactoring_types = self.config_parser.get("REFACTORING", "types",
                                                       fallback="extract_class,move_method,pull_up_method,push_down_method,extract_method")
            return {
                'types': [t.strip() for t in refactoring_types.split(',')],
                'relations': {
                    'god_class_path': self.config_parser.get("RELATIONS", "GOD_CLASS_PATH", fallback=""),
                    'feature_envy_path': self.config_parser.get("RELATIONS", "FEATURE_ENVY_PATH", fallback=""),
                    'long_method_path': self.config_parser.get("RELATIONS", "LONG_METHOD_PATH", fallback=""),
                }
            }
        except Exception as e:
            logger.error(f"Error loading refactoring config: {e}")
            return {'types': ['extract_class', 'move_method', 'pull_up_method', 'push_down_method', 'extract_method']}

    def get_understand_config(self) -> Dict[str, Any]:
        """Get Understand configuration"""
        try:
            return {
                'sys_path_object': self.config_parser.get("UNDERSTAND", "sys_path_object",
                                                          fallback="/app/scitools/bin/linux64/Python"),
                'sys_path_index': self.config_parser.getint("UNDERSTAND", "sys_path_index", fallback=0),
                'os_environs_key': self.config_parser.get("UNDERSTAND", "os_environs_key", fallback="LD_LIBRARY_PATH"),
                'os_environs_value': self.config_parser.get("UNDERSTAND", "os_environs_value",
                                                            fallback="/app/scitools/bin/linux64/Python"),
            }
        except Exception as e:
            logger.error(f"Error loading understand config: {e}")
            return {}

    def _get_fallback_training_config(self) -> Dict[str, Any]:
        """Fallback training configuration"""
        return {
            'frames_per_batch': 6000,
            'n_iters': 10,
            'num_epochs': 30,
            'minibatch_size': 400,
            'learning_rate': 0.0003,
            'max_grad_norm': 1.0,
            'max_steps': 100,
            'torch_manual_seed': 0,
            'save_interval': 100,
            'evaluation_interval': 50,
        }

    def _get_fallback_ppo_config(self) -> Dict[str, Any]:
        """Fallback PPO configuration"""
        return {
            'clip_epsilon': 0.2,
            'gamma': 0.99,
            'lambda': 0.9,
            'entropy_eps': 0.0001,
            'depth': 2,
            'num_cells': 256,
            'share_parameters_critic': True,
        }

    def _get_fallback_environment_config(self, project_name: str = None) -> Dict[str, Any]:
        """Fallback environment configuration"""
        return {
            'project_name': project_name or "JSON",
            'udb_path': "/app/jflex/jflex.udb",
            'n_obj': 8,
            'lower_band': 10,
            'upper_bound': 50,
            'population_size': 100,
            'version_id': "v1.0",
            'project_path': "/app/jflex",
            'evaluate_in_parallel': True,
            'verbose_design_metrics': True,
        }


# Global config manager instance
_config_manager = None


def get_integrated_config_manager() -> IntegratedConfigManager:
    """Get global integrated config manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = IntegratedConfigManager()
    return _config_manager