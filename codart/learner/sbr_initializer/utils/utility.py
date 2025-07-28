import random
import json
import os
from abc import abstractmethod, ABCMeta
import logging
import sys
from configparser import ConfigParser
from datetime import datetime


# Enhanced logging setup for debugging TensorDictModule issues
def setup_logging():
    """Setup comprehensive logging for debugging"""
    # Create logs directory if it doesn't exist
    log_dir = "/app/logs"
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except:
            log_dir = "."  # Fallback to current directory

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Console handler with simple format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # Debug file handler with detailed format
    debug_file = os.path.join(log_dir, f"debug_{datetime.now().strftime('%Y%m%d')}.log")
    debug_handler = logging.FileHandler(debug_file, mode='a')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(detailed_formatter)
    logger.addHandler(debug_handler)

    # Error file handler
    error_file = os.path.join(log_dir, f"error_{datetime.now().strftime('%Y%m%d')}.log")
    error_handler = logging.FileHandler(error_file, mode='a')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)

    # TensorDict/TorchRL specific debugging
    tensordict_logger = logging.getLogger('tensordict')
    tensordict_logger.setLevel(logging.DEBUG)

    torchrl_logger = logging.getLogger('torchrl')
    torchrl_logger.setLevel(logging.DEBUG)

    return logger


# Setup logging
logger = setup_logging()

# Configuration setup with better error handling
config = ConfigParser()

# Extended config paths
config_paths = [
    "config.ini",  # Current directory
    "/app/config.ini",  # Docker container
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "config.ini"),  # Relative to this file
    os.path.join(os.path.dirname(__file__), "..", "..", "config.ini"),  # Two levels up
    os.path.join(os.path.dirname(__file__), "..", "config.ini"),  # One level up
    os.path.join(os.path.dirname(__file__), "config.ini"),  # Same directory
]

config_loaded = False
for config_path in config_paths:
    if os.path.exists(config_path):
        try:
            config.read(config_path)
            config_loaded = True
            logger.info(f"Successfully loaded config from {config_path}")
            break
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")

if not config_loaded:
    logger.warning("No config.ini file found, creating default configuration")

    # Create default configuration
    config.add_section('TRAINING')
    config.set('TRAINING', 'frames_per_batch', '100')
    config.set('TRAINING', 'n_iters', '10')
    config.set('TRAINING', 'num_epochs', '4')
    config.set('TRAINING', 'minibatch_size', '25')
    config.set('TRAINING', 'learning_rate', '3e-4')
    config.set('TRAINING', 'max_grad_norm', '1.0')
    config.set('TRAINING', 'max_steps', '50')
    config.set('TRAINING', 'torch_manual_seed', '42')

    config.add_section('PPO')
    config.set('PPO', 'clip_epsilon', '0.2')
    config.set('PPO', 'gamma', '0.99')
    config.set('PPO', 'lambda', '0.95')
    config.set('PPO', 'entropy_eps', '0.01')
    config.set('PPO', 'depth', '2')
    config.set('PPO', 'num_cells', '256')
    config.set('PPO', 'scenario_name', 'navigation')
    config.set('PPO', 'n_agents', '1')
    config.set('PPO', 'continuous_actions', 'True')
    config.set('PPO', 'centralised', 'False')
    config.set('PPO', 'share_parameters_critic', 'True')

    config.add_section('ENVIRONMENT')
    config.set('ENVIRONMENT', 'udb_path', '/opt/understand_dbs/json/e9e396ad/e9e396ad.und')
    config.set('ENVIRONMENT', 'n_obj', '8')
    config.set('ENVIRONMENT', 'lower_band', '1')
    config.set('ENVIRONMENT', 'upper_bound', '50')
    config.set('ENVIRONMENT', 'population_size', '100')
    config.set('ENVIRONMENT', 'project_name', 'json')
    config.set('ENVIRONMENT', 'version_id', 'e9e396ad')
    config.set('ENVIRONMENT', 'project_path', '/opt/projects/json/e9e396ad')

    config.add_section('MINIO')
    config.set('MINIO', 'endpoint', 'minio:9000')
    config.set('MINIO', 'access_key', 'minioadmin')
    config.set('MINIO', 'secret_key', 'minioadmin')
    config.set('MINIO', 'secure', 'False')
    config.set('MINIO', 'results_bucket', 'ml-models')


def get_config_value(section, key, fallback=None, value_type=str):
    """Safely get configuration values with fallbacks and proper error handling"""
    try:
        if value_type == int:
            return config.getint(section, key)
        elif value_type == float:
            return config.getfloat(section, key)
        elif value_type == bool:
            return config.getboolean(section, key)
        else:
            return config.get(section, key)
    except Exception as e:
        logger.warning(f"Config error for [{section}] {key}: {e}. Using fallback: {fallback}")
        return fallback


def log_tensor_info(tensor, name="tensor"):
    """Helper function to log tensor information for debugging"""
    if hasattr(tensor, 'shape'):
        logger.debug(f"{name} - shape: {tensor.shape}, dtype: {tensor.dtype}, device: {tensor.device}")
        if hasattr(tensor, 'requires_grad'):
            logger.debug(f"{name} - requires_grad: {tensor.requires_grad}")
    else:
        logger.debug(f"{name} - not a tensor: {type(tensor)}")


def log_tensordict_info(tensordict, name="tensordict"):
    """Helper function to log TensorDict information for debugging"""
    if hasattr(tensordict, 'keys'):
        logger.debug(f"{name} - keys: {list(tensordict.keys())}")
        logger.debug(f"{name} - batch_size: {getattr(tensordict, 'batch_size', 'unknown')}")
        for key, value in tensordict.items():
            log_tensor_info(value, f"{name}[{key}]")
    else:
        logger.debug(f"{name} - not a TensorDict: {type(tensordict)}")


def debug_model_forward(model, input_data, model_name="model"):
    """Debug helper for model forward passes"""
    logger.debug(f"=== Debugging {model_name} forward pass ===")
    try:
        logger.debug(f"Input type: {type(input_data)}")
        if hasattr(input_data, 'keys'):
            log_tensordict_info(input_data, "input")

        output = model(input_data)

        logger.debug(f"Output type: {type(output)}")
        if hasattr(output, 'keys'):
            log_tensordict_info(output, "output")

        logger.debug(f"=== {model_name} forward pass completed successfully ===")
        return output

    except Exception as e:
        logger.error(f"=== {model_name} forward pass FAILED ===")
        logger.error(f"Error: {e}", exc_info=True)
        raise


def handle_index_error(func):
    """Decorator to handle index errors gracefully"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as e:
            logger.warning(f"Index error in {func.__name__}: {e}")
            return None, None, None
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            return None, None, None

    return wrapper


class DynamicAbstractMetaInitializeRefactoringMethods(ABCMeta):
    """Metaclass for dynamic method creation"""

    def create_not_implemented_method(self, method_name):
        def not_implemented_method(self):
            raise NotImplementedError(f"Method {method_name} not implemented.")

        return not_implemented_method

    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)

        if "refactoring_types" in namespace:
            for refactoring in namespace["refactoring_types"]:
                method_name = f"init_{refactoring.strip()}"
                setattr(
                    new_class,
                    method_name,
                    abstractmethod(cls.create_not_implemented_method(method_name)),
                )
                method_name = f"load_{refactoring.strip()}_candidates"
                setattr(
                    new_class,
                    method_name,
                    abstractmethod(cls.create_not_implemented_method(method_name)),
                )

        return new_class


class Utils(object):
    """Utility class with enhanced logging and debugging"""

    def __init__(self, logger, population, initializers, project_name="", version_id="", project_dir: str = ""):
        self.logger = logger
        self.population = population
        self.initializers = initializers
        self.project_name = project_name
        self.version_id = version_id
        self.project_dir = project_dir

        # Log initialization
        self.logger.debug(f"Utils initialized - project: {project_name}, version: {version_id}")
        self.logger.debug(f"Population size: {len(population) if population else 0}")
        self.logger.debug(f"Initializers count: {len(initializers) if initializers else 0}")

    @handle_index_error
    def select_random(self):
        """Select random initializer with enhanced error handling"""
        if not self.initializers:
            self.logger.error("No initializers available for selection")
            return None, None, None

        try:
            initializer = random.choice(self.initializers)
            self.logger.debug(f"Randomly selected initializer: {initializer}")

            if not isinstance(initializer, (list, tuple)) or len(initializer) != 3:
                self.logger.error(f"Invalid initializer structure: {initializer}")
                return None, None, None

            main_function, params, name = initializer

            if not (callable(main_function) and isinstance(params, dict) and isinstance(name, str)):
                self.logger.error(f"Invalid initializer components - function: {callable(main_function)}, "
                                  f"params: {isinstance(params, dict)}, name: {isinstance(name, str)}")
                return None, None, None

            self.logger.debug(f"Successfully selected refactoring: {name}")
            return main_function, params, name

        except Exception as e:
            self.logger.error(f"Error selecting random initializer: {e}", exc_info=True)
            return None, None, None

    def dump_population(self, path=None):
        """Dump population with better error handling"""
        if self.population is None or len(self.population) == 0:
            self.logger.warning("No population to dump")
            return

        try:
            population_trimmed = []
            for i, chromosome in enumerate(self.population):
                try:
                    chromosome_new = []
                    for j, gene_ in enumerate(chromosome):
                        if len(gene_) >= 3:
                            chromosome_new.append((gene_[2], gene_[1]))
                        else:
                            self.logger.warning(f"Invalid gene structure at chromosome {i}, gene {j}: {gene_}")
                    population_trimmed.append(chromosome_new)
                except Exception as e:
                    self.logger.error(f"Error processing chromosome {i}: {e}")

            if path is None:
                path = f"population_{self.project_name}_{self.version_id}.json"

            with open(path, mode="w", encoding="utf-8") as fp:
                json.dump(population_trimmed, fp, indent=4)

            self.logger.info(f"Population saved to {path}")

        except Exception as e:
            self.logger.error(f"Error dumping population: {e}", exc_info=True)

    def get_move_method_location(self, row):
        """Parse move method location with error handling"""
        try:
            class_info, method_info = row.split("::")
            class_info = class_info.split(".")
            source_package = ".".join(class_info[:-1])
            source_class = class_info[-1]
            method_name = method_info.split("(")[0]

            self.logger.debug(f"Parsed method location - package: {source_package}, "
                              f"class: {source_class}, method: {method_name}")

            return source_package, source_class, method_name

        except Exception as e:
            self.logger.error(f"Error parsing method location '{row}': {e}")
            return None, None, None


# Log the successful setup
logger.info("Enhanced utility module loaded with debugging capabilities")
if config_loaded:
    logger.info("Configuration loaded successfully")
else:
    logger.warning("Using default configuration - consider creating config.ini")