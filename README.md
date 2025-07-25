# CodART - Source Code Automated Refactoring Toolkit

![CodART](docs/figs/codart.png)

Source Code Automated Refactoring Toolkit (CodART) is a refactoring engine with the ability to perform many-objective program transformation and optimization. We have currently focused on automating the [various refactoring operations](https://refactoring.com/catalog/) for Java source codes. A complete list of refactoring supported by CodART can be found at [CodART refactorings list](https://m-zakeri.github.io/CodART/refactorings_list/).

The CodART project is under active development. The current version of CodART works fine on our benchmark projects. To understand how CodART works, read the [CodART white-paper](https://m-zakeri.github.io/CodART). 
Your contributions to the project and your comments in the discussion section would be welcomed. 
Also, feel free to email and ask any question: 
`m-zakeri[at]live[dot]com`.

## System Architecture Overview

![CodART System Architecture](codart_system_arch.png)

*Overall system architecture showing containerized services*

![CodART Reinforcement Learning Architecture](codart_rl_arch.png)

*Reinforcement learning components and data flow*

![CodART ML Pipeline](codart_ml_pipeline.png)

*Machine learning training pipeline workflow*

## Overview

CodART (Source Code Automated Refactoring Toolkit) is a multi-objective program transformation and optimization engine that combines search-based software engineering (SBSE) with automated refactoring operations to improve Java source code quality. The system includes a modern web-based interface, containerized deployment with Docker, reinforcement learning capabilities using PPO algorithms, and advanced machine learning models for testability prediction and intelligent code refactoring.

**Key Innovation**: CodART integrates traditional search-based refactoring with modern reinforcement learning to create an intelligent system that learns optimal refactoring sequences, making it unique in the automated software refactoring domain.

### Key Features

- **Automated Java Refactoring**: Supports 40+ refactoring operations including Extract Class, Move Method, Extract Interface, and more
- **Multi-Objective Optimization**: Uses NSGA-II and NSGA-III algorithms to optimize 8+ QMOOD quality metrics simultaneously
- **Reinforcement Learning**: PPO (Proximal Policy Optimization) algorithm for intelligent refactoring sequence generation
- **Testability Prediction**: Advanced ML models (RandomForest, GradientBoosting, MLP, VotingRegressor) predict code testability using 262+ source code metrics
- **Code Smell Detection**: PMD 7.11.0 integration with custom rulesets for automated quality analysis
- **SciTools Understand Integration**: Professional code analysis engine for parsing and metrics computation
- **Web-based UI**: Modern React interface with real-time progress tracking and project management
- **Containerized Architecture**: Docker-based deployment with microservices including API, UI, MinIO, Redis, RabbitMQ
- **ANTLR4-based Parsing**: Three grammar variants optimized for different parsing performance needs
- **Benchmark Integration**: 14 benchmark projects for testing and validation including JSON, JFreeChart, Weka

## Quick Start with Docker

### Prerequisites

- **Docker and Docker Compose** (Latest versions)
- **System Requirements**: At least 8GB RAM and 4 CPU cores (12GB+ recommended for large projects)
- **SciTools Understand License**: Professional license required for code analysis
  - Academic licenses available for research purposes
  - License activation requires internet connectivity
- **Storage**: Minimum 20GB free disk space for containers and project data

### 1. Clone and Setup

```bash
git clone https://github.com/m-zakeri/CodART.git
cd CodART
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# Project Configuration
PROJECT_ROOT_DIR="/opt/projects"
UDB_ROOT_DIR="/opt/understand_dbs"
BENCHMARK_INDEX=2  # Index from codart/config.py (0-13)

# Search Algorithm Settings
POPULATION_SIZE=15
MAX_ITERATIONS=15
PROBLEM=2  # 0: Simple Genetic, 1: NSGA-II, 2: NSGA-III
NUMBER_OBJECTIVES=8  # QMOOD metrics count
MUTATION_PROBABILITY=0.2
CROSSOVER_PROBABILITY=0.8

# Warm Start Options (Optional)
WARM_START=1  # Enable warm start from previous results
INIT_POP_FILE="/path/to/initial_population.csv"  # Optional
CSV_ROOT_DIR="/path/to/jdeodorant_csv"  # Optional

# MinIO Credentials (Change for production)
MINIO_ACCESS_KEY=00jFBl7n9Jn0ex0XL7m1
MINIO_SECRET_KEY=kYfujzkdSGjXKLN9oQhPDIVgRUaZRijvj1yaXmIZ

# Experimental Settings (Optional)
USE_CPP_BACKEND=0  # Enable C++ parser backend for performance
EXPERIMENTER="Your Name"  # For research tracking
DESCRIPTION="Experiment description"  # For result documentation
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application

- **Web Interface**: http://localhost:3000 (React UI)
- **API Documentation**: http://localhost:8000/docs (FastAPI Swagger)
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **Redis CLI**: `docker exec -it codart_redis_1 redis-cli` (Direct access)

### 5. Initial Setup

```bash
# Verify all services are running
docker-compose ps

# Check SciTools Understand license
docker exec -it codart_api_1 und license

# Upload a test project via web interface or API
curl -X POST "http://localhost:8000/projects/upload" \
  -F "file=@your_project.zip" \
  -F "project_name=TestProject"
```

## Architecture Components

### Core Services

#### API Container (`api`)
- **FastAPI Backend**: RESTful API for all operations
- **Celery Worker**: Handles ML training and analysis tasks
- **SciTools Understand**: Code parsing and analysis engine
- **PMD Integration**: Code smell detection with custom rulesets
- **Combined Architecture**: API and worker run in same container for license sharing

#### User Interface (`ui`)
- **React Frontend**: Modern web interface with real-time updates
- **Project Management**: Upload and manage Java projects
- **ML Training Interface**: Configure and monitor training sessions
- **Task Monitoring**: Real-time progress tracking with localStorage persistence

#### Storage Layer
- **MinIO**: Object storage for models, reports, and temporary files
- **Redis**: Task result backend and caching
- **Docker Volumes**: Persistent data storage

#### Message Queue
- **RabbitMQ**: Async task processing with queues:
  - `ml_training`: Machine learning training tasks
  - `ml_evaluation`: Model evaluation tasks
  - `celery`: General background tasks

### Quality Analysis Components

#### Code Smell Detection (PMD)
- **PMD 7.11.0**: Integrated static analysis tool
- **Custom Rulesets**: Tailored rules for design patterns, complexity, and best practices
- **Automated Detection**: GodClass, LawOfDemeter, CyclomaticComplexity, etc.
- **CSV Reporting**: Structured output for refactoring candidate selection
- **MinIO Storage**: Cloud-based report archival and retrieval

#### Testability Prediction Engine
- **ML Models**: 7 different model types (RandomForest, GradientBoosting, MLP, etc.)
- **Metric Analysis**: 262 comprehensive source code metrics
- **Real-time Prediction**: Integration with refactoring operations
- **Model Variants**: Lightweight (68 metrics), Ultra-light (10 metrics), Design-based
- **Distributed Training**: Celery-based ML pipeline with model versioning

### Project Structure

```
CodART/
├── application/              # FastAPI web service and APIs
│   ├── controllers/          # REST API endpoints
│   │   ├── learning_controller_testability.py
│   │   ├── project_management_controller.py
│   │   ├── rl/              # Reinforcement learning endpoints
│   │   └── reporter/        # Export and download controllers
│   ├── services/            # Business logic services
│   │   ├── minio_training_controller.py
│   │   └── config_integration.py
│   ├── celery_workers/      # Background task processors
│   │   ├── ml_training_task.py
│   │   └── model_prediction_task.py
│   └── main.py             # FastAPI application entry point
├── codart/                  # Core refactoring engine
│   ├── gen/                # ANTLR4-generated parsers
│   │   ├── JavaParserLabeled.py      # Labeled grammar (preferred)
│   │   ├── JavaParserLabeledVisitor.py
│   │   └── JavaParserLabeledListener.py
│   ├── refactorings/       # 40+ refactoring implementations
│   │   ├── extract_class.py, extract_method.py
│   │   ├── move_method.py, move_field.py
│   │   ├── pullup_method.py, pushdown_method.py
│   │   └── handler.py      # Refactoring registry
│   ├── metrics/            # Quality metrics computation
│   │   ├── qmood.py        # QMOOD metrics (8 objectives)
│   │   ├── testability_prediction.py
│   │   └── learner_testability/  # ML models for testability
│   ├── smells/             # Code smell detection
│   │   ├── long_method.py
│   │   └── map_smell_refactoring.py
│   ├── sbse/               # Search-based software engineering
│   │   ├── search_based_refactoring2.py  # Main SBSE engine
│   │   └── simple_genetics.py
│   ├── learner/            # Machine learning components
│   │   ├── genetic.py      # Genetic algorithms
│   │   ├── alpha_zero_MCTS.py  # Monte Carlo Tree Search
│   │   └── sbr_initializer/    # RL environment setup
│   └── utility/            # Common utilities
│       └── setup_understand.py
├── ui/                     # React frontend application
│   ├── src/               # React source code
│   ├── public/            # Static assets
│   ├── Dockerfile         # UI container build
│   └── nginx.conf         # Production web server config
├── benchmark_projects/     # Test projects (14 Java projects)
├── tests/                  # Individual refactoring test cases
├── pmd/                   # PMD 7.11.0 code analysis tool
│   ├── bin/pmd           # PMD executable
│   ├── rules/custom.xml  # Custom rulesets
│   └── lib/              # PMD dependencies
├── scitools/              # SciTools Understand installation
│   ├── bin/              # Understand binaries
│   └── plugins/          # Analysis plugins
├── grammars/              # ANTLR4 grammar files
│   ├── JavaParserLabeled.g4  # Preferred fast grammar
│   ├── JavaParser.g4         # Original fast grammar
│   └── Java9_v2.g4          # Legacy slow grammar
├── docker-compose.yml     # Multi-service orchestration
├── Dockerfile.api         # API container build
├── Dockerfile.base        # Base image with dependencies
└── requirements.txt       # Python dependencies
```

## Usage Workflows

### 1. Web Interface Workflow

1. **Project Upload**: Upload Java projects (ZIP format) via web interface
2. **Understand Database Creation**: Automatic `.und` database generation for code analysis
3. **PMD Code Smell Detection**: Automated smell detection using custom rulesets
4. **ML Training Configuration**: Configure RL training parameters and objectives
5. **Training Execution**: Monitor real-time progress with Celery task tracking
6. **Model Evaluation**: View training metrics and model performance
7. **Results Download**: Export trained models, reports, and refactored code

### 2. CLI Workflow

```bash
# Direct refactoring execution with SciTools Understand
python codart/refactoring_cli.py \
  --udb_path "/path/to/project.und" \
  --file_path "/path/to/SourceClass.java" \
  --source_class "ClassName" \
  --moved_methods "method1,method2" \
  --core 0  # 0=Understand, 1=OpenUnderstand

# Search-based multi-objective optimization
python codart/sbse/search_based_refactoring2.py

# Individual refactoring testing
python tests/extract_method/test_1.py

# Testability prediction
python codart/metrics/testability_prediction.py --project-path /path/to/project

# Code smell detection with PMD
./pmd/bin/pmd check -d /path/to/source -R pmd/rules/custom.xml -f csv
```

### 3. API Integration

```bash
# Upload and analyze project
curl -X POST "http://localhost:8000/projects/upload" \
  -F "file=@project.zip" \
  -F "project_name=MyProject"

# Start ML training with full configuration
curl -X POST "http://localhost:8000/ml-training/train" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "123",
    "config": {
      "population_size": 15,
      "max_iterations": 20,
      "problem_type": 2,
      "objectives": ["ANA", "CAMC", "CIS", "DAM", "DCC", "DSC", "MFA", "MOA"]
    }
  }'

# Monitor training progress
curl "http://localhost:8000/tasks/{task_id}/status"

# Download results
curl "http://localhost:8000/projects/{project_id}/download/models" -o models.zip

# Get testability prediction
curl -X POST "http://localhost:8000/testability/predict" \
  -H "Content-Type: application/json" \
  -d '{"project_path": "/opt/projects/MyProject", "model_type": "voting_regressor"}'
```

## Machine Learning Features

### Testability Prediction Models

CodART implements comprehensive testability prediction using multiple ML approaches:

#### Model Architecture
- **RandomForestRegressor**: Primary ensemble model for robust predictions
- **GradientBoostingRegressor**: High-accuracy gradient-based learning
- **MLPRegressor**: Neural network for complex pattern recognition
- **VotingRegressor**: Ensemble combining top 3 models for optimal accuracy

#### Metric Categories
- **Package Metrics** (59): Module-level design quality indicators
- **Class Lexical Metrics** (17): Code complexity and readability measures
- **Class Ordinary Metrics** (186): Comprehensive structural analysis
- **Total**: 262 source code metrics for comprehensive analysis

#### Model Variants
- **Full Model**: 262 metrics for maximum accuracy
- **Lightweight**: 68 metrics for fast real-time prediction
- **Ultra-light**: 10 most important metrics for instant feedback
- **Design-based**: Graph network analysis using NetworkX

### PMD Code Smell Detection

Integrated PMD 7.11.0 provides automated code quality analysis:

#### Detection Categories
- **Design Issues**: GodClass, LawOfDemeter, CyclomaticComplexity
- **Best Practices**: LooseCoupling, UnusedPrivateMethod
- **Code Style**: UnnecessaryModifier, ProperLogger
- **Complexity**: NPathComplexity, CognitiveComplexity

#### Integration Points
- **Refactoring Guidance**: PMD results guide candidate selection
- **Real-time Analysis**: Automated execution on project upload
- **Cloud Storage**: Results archived in MinIO for persistent access
- **Custom Rules**: Tailored ruleset for refactoring-specific analysis

### Reinforcement Learning Training

The system uses Proximal Policy Optimization (PPO) to learn optimal refactoring sequences:

- **Environment**: `RefactoringSequenceEnvironment` simulates code transformation
- **State**: Current code metrics and smell indicators
- **Actions**: Available refactoring operations
- **Rewards**: Multi-objective improvement in quality metrics
- **Training**: Experience replay with policy and value networks

### Quality Objectives

The system optimizes for 8 design quality objectives:

1. **ANA** (Average Number of Ancestors)
2. **CAMC** (Cohesion Among Methods in Class)
3. **CIS** (Class Interface Size)
4. **DAM** (Data Access Metric)
5. **DCC** (Direct Class Coupling)
6. **DSC** (Design Size in Classes)
7. **MFA** (Measure of Functional Abstraction)
8. **MOA** (Measure of Aggregation)

### Supported Refactorings

**Structural Refactorings:**
- Extract Class, Extract Method, Extract Interface
- Move Method, Move Field, Move Class
- Inline Class, Collapse Hierarchy

**Access Control:**
- Increase/Decrease Field/Method Visibility
- Encapsulate Field

**Inheritance Operations:**
- Pull Up Method/Field/Constructor
- Push Down Method/Field
- Make Class Abstract/Concrete/Final

**Code Quality:**
- Rename Class/Method/Field/Package
- Remove Dead Code
- Replace Conditional with Polymorphism

## Configuration

### Environment Variables

```bash
# Core Paths (Container)
PROJECT_ROOT_DIR="/opt/projects"          # Java projects storage
UDB_ROOT_DIR="/opt/understand_dbs"        # Understand database files
CSV_ROOT_DIR="/opt/csv_reports"           # PMD analysis reports

# SciTools Understand Configuration
STILICENSE="/root/.config/SciTools/License.conf"
STIHOME="/app/scitools"                   # Understand installation
STIDOSUTILDIR="/root/.config/SciTools"    # License directory
UNDERSTAND_API_LICENSE="/root/.local/share/SciTools/Understand/python_api.cfg"

# PMD Configuration
PMD_PATH="/app/pmd/bin/pmd"               # PMD executable
PMD_RULESET="/app/pmd/rules/custom.xml"   # Custom analysis rules
PMD_CACHE_DIR="/app/pmd/cache"            # PMD cache directory

# SBSE Algorithm Configuration
POPULATION_SIZE=15                        # GA population size
MAX_ITERATIONS=15                         # Maximum generations
NGEN=10                                   # Alternative iteration setting
PROBLEM=2                                 # 0=GA, 1=NSGA-II, 2=NSGA-III
NUMBER_OBJECTIVES=8                       # QMOOD metrics count
MUTATION_PROBABILITY=0.2                  # Mutation rate
CROSSOVER_PROBABILITY=0.8                 # Crossover rate
LOWER_BAND=15                            # Lower bound for metrics
UPPER_BAND=50                            # Upper bound for metrics

# Warm Start Configuration
WARM_START=1                             # Enable warm start
INIT_POP_FILE=""                         # Initial population file
RESUME_EXECUTION=""                       # Resume from checkpoint

# Service URLs (Container Network)
CELERY_BROKER_URL="amqp://guest:guest@rabbitmq:5672//"
CELERY_RESULT_BACKEND="redis://redis:6379/0"
MINIO_ENDPOINT="minio:9000"
MINIO_ACCESS_KEY="00jFBl7n9Jn0ex0XL7m1"
MINIO_SECRET_KEY="kYfujzkdSGjXKLN9oQhPDIVgRUaZRijvj1yaXmIZ"

# Performance Options
USE_CPP_BACKEND=0                        # Enable C++ parser (faster)
QT_QPA_PLATFORM="offscreen"              # Headless Qt for Understand

# Research Tracking (Optional)
EXPERIMENTER="Researcher Name"
SCRIPT="search_based_refactoring2.py"
DESCRIPTION="Experiment description"
```

### Benchmark Projects

The system includes 14 benchmark projects (defined in `codart/config.py`):

| Index | Project | Description | Size |
|-------|---------|-------------|------|
| 0 | JSON20201115 | JSON parsing library | Small |
| 1 | JFreeChart | Chart generation library | Large |
| 2 | Weka | Machine learning toolkit | Large |
| 3 | FreeMind | Mind mapping software | Medium |
| 4 | Commons-codec | Apache commons codec | Small |
| 5 | JRDF | RDF framework | Medium |
| 6 | JMetal | Multi-objective optimization | Medium |
| 7 | AntApache | Build automation tool | Large |
| 8-13 | Additional projects | Various Java applications | Varies |

**Configuration**: Set `BENCHMARK_INDEX` (0-13) in `.env` file or `codart/config.py`.

**Project Structure**: Each benchmark includes:
- Source code in standard Maven/Gradle structure
- Pre-generated `.und` database file
- PMD analysis reports (CSV format)
- Initial metrics baseline
- Code smell detection results

## Development

### Local Development Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Setup SciTools Understand (Local Installation)
export PYTHONPATH="/opt/scitools/bin/linux64/Python:$PYTHONPATH"
export PATH="/opt/scitools/bin/linux64:$PATH"
export LD_LIBRARY_PATH="/opt/scitools/bin/linux64:$LD_LIBRARY_PATH"

# Activate Understand license
und -setofflinereplycode YOUR_LICENSE_CODE

# Install PMD (if not using Docker)
wget https://github.com/pmd/pmd/releases/download/pmd_releases%2F7.11.0/pmd-bin-7.11.0.zip
unzip pmd-bin-7.11.0.zip -d /opt/pmd

# Start development services
# Terminal 1: API server
uvicorn application.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Celery worker
celery -A application.celery_workers.ml_training_task worker --loglevel=info

# Terminal 3: UI development server
cd ui && npm install && npm start

# Terminal 4: Redis (if not using Docker)
redis-server

# Terminal 5: RabbitMQ (if not using Docker)
rabbitmq-server
```

### Grammar Development

```bash
# Generate parser from grammar (requires ANTLR4)
cd grammars
antlr4 -Dlanguage=Python3 JavaParserLabeled.g4 -visitor -listener
mv *.py ../codart/gen/

# Test grammar parsing speed
python tests/grammar_speed_tests/test_performance.py
```

### Adding New Refactorings

1. **Create refactoring module** in `codart/refactorings/`:
   ```python
   from codart.gen.JavaParserLabeledListener import JavaParserLabeledListener
   
   class MyRefactoring(JavaParserLabeledListener):
       def __init__(self, source_class, target_info):
           self.source_class = source_class
           # Implementation details
   ```

2. **Inherit from appropriate base class**:
   - `JavaParserLabeledListener` (recommended)
   - `JavaParserLabeledVisitor` (for complex traversals)
   - Import from `codart.gen.JavaLabled` package

3. **Add comprehensive tests** in `tests/` directory:
   ```bash
   tests/my_refactoring/
   ├── test_1.py           # Main test script
   ├── input.java          # Test input code
   ├── expected.java       # Expected output
   └── README.md           # Test documentation
   ```

4. **Register refactoring** in `codart/refactorings/handler.py`:
   ```python
   from .my_refactoring import MyRefactoring
   
   REFACTORING_REGISTRY = {
       'my_refactoring': MyRefactoring,
       # ... other refactorings
   }
   ```

5. **Test on benchmark projects**:
   ```bash
   python codart/sbse/search_based_refactoring2.py
   ```

6. **Update documentation** with refactoring details and examples

### Testing

```bash
# Run individual refactoring tests
python tests/extract_method/test_1.py
python tests/move_method/test_move_method.py
python tests/pullup_method/test_pullup.py

# Test specific refactoring with custom input
python -c "from codart.refactorings.extract_class import ExtractClass; \
           ec = ExtractClass('input.java', 'SourceClass', ['field1', 'method1']); \
           ec.do_refactor()"

# Run all tests in a category
find tests/ -name "test_*.py" -exec python {} \;

# Test on benchmark projects (full SBSE)
python codart/sbse/search_based_refactoring2.py

# Test PMD integration
./pmd/bin/pmd check -d benchmark_projects/JSON20201115/src \
    -R pmd/rules/custom.xml -f csv -r results.csv

# Test Understand integration
python codart/utility/understand_install_test.py

# Test ML components
python codart/metrics/testability_prediction.py --test

# Performance testing
python tests/grammar_speed_tests/benchmark_parsing.py
```

## Troubleshooting

### Common Issues

**SciTools License Error:**
```bash
# Check license status
docker exec -it codart_api_1 und license

# Reactivate license
docker exec -it codart_api_1 /app/activate_license.sh
```

**Memory Issues:**
- Increase container memory limit in docker-compose.yml
- Reduce population size in configuration
- Use smaller benchmark projects for testing

**Build Failures:**
```bash
# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Performance Optimization

- Use fast grammar `JavaParserLabeled.g4` for new development
- Enable C++ backend for faster parsing (optional)
- Configure appropriate population size based on available resources
- Use SSD storage for Docker volumes

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Development Guidelines

- Follow existing code patterns and naming conventions
- Use `JavaParserLabeled.g4` for new refactoring implementations
- Test on individual files before benchmark projects
- Document new refactoring operations
- Follow security best practices

## Citation

If you use CodART in your research, please cite:

```bibtex
@misc{codart2024,
  title={CodART: Source Code Automated Refactoring Toolkit},
  author={Zakeri, Morteza and contributors},
  year={2024},
  url={https://github.com/m-zakeri/CodART}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Official Documentation](https://m-zakeri.github.io/CodART)
- [Refactoring Catalog](https://m-zakeri.github.io/CodART/refactorings_list/)
- [Code Smells Reference](https://m-zakeri.github.io/CodART/code_smells_list/)
- [Benchmark Projects](https://m-zakeri.github.io/CodART/benchmarks/)
- [API Documentation](http://localhost:8000/docs) (when running locally)

## Support

- **Issues**: [GitHub Issues](https://github.com/m-zakeri/CodART/issues)
- **Discussions**: [GitHub Discussions](https://github.com/m-zakeri/CodART/discussions)
- **Email**: m-zakeri[at]live[dot]com

---

*CodART is actively developed at [IUST Reverse Engineering Laboratory](http://reverse.iust.ac.ir/)*