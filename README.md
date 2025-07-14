# CodART - Source Code Automated Refactoring Toolkit

![CodART](docs/figs/codart.png)

## System Architecture Overview

![CodART System Architecture](codart_system_arch.png)

*Overall system architecture showing containerized services*

![CodART Reinforcement Learning Architecture](codart_rl_arch.png)

*Reinforcement learning components and data flow*

![CodART ML Pipeline](codart_ml_pipeline.png)

*Machine learning training pipeline workflow*

## Overview

CodART (Source Code Automated Refactoring Toolkit) is a multi-objective program transformation and optimization engine that combines search-based software engineering (SBSE) with automated refactoring operations to improve Java source code quality. The system now includes a modern web-based interface, containerized deployment, and advanced machine learning capabilities for intelligent code refactoring.

### Key Features

- **Automated Java Refactoring**: Supports 40+ refactoring operations including Extract Class, Move Method, Extract Interface, and more
- **Multi-Objective Optimization**: Uses NSGA-II and NSGA-III algorithms to optimize 8+ quality metrics simultaneously
- **Machine Learning Integration**: Reinforcement learning (PPO) for intelligent refactoring sequence generation
- **Testability Prediction**: Advanced ML models predict code testability using 262+ source code metrics
- **Code Smell Detection**: PMD 7.11.0 integration with custom rulesets for automated quality analysis
- **Web-based UI**: Modern React interface for project management and ML training
- **Containerized Architecture**: Docker-based deployment with microservices
- **Real-time Monitoring**: Task tracking and progress monitoring for long-running operations

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose
- At least 8GB RAM and 4 CPU cores
- SciTools Understand license (for code analysis)

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
BENCHMARK_INDEX=2

# Search Algorithm Settings
POPULATION_SIZE=15
MAX_ITERATIONS=15
PROBLEM=2  # 0: Genetic, 1: NSGA-II, 2: NSGA-III
NUMBER_OBJECTIVES=8

# MinIO Credentials
MINIO_ACCESS_KEY=00jFBl7n9Jn0ex0XL7m1
MINIO_SECRET_KEY=kYfujzkdSGjXKLN9oQhPDIVgRUaZRijvj1yaXmIZ
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application

- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (admin/admin)
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

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

### Key Directories

```
CodART/
├── application/           # FastAPI web service
│   ├── controllers/       # API endpoints
│   ├── services/         # Business logic
│   └── celery_workers/   # Background task handlers
├── codart/               # Core refactoring engine
│   ├── refactorings/     # Refactoring implementations
│   ├── metrics/          # Quality metrics (QMOOD, testability)
│   ├── smells/           # Code smell detection
│   ├── sbse/             # Search-based optimization
│   └── learner/          # Machine learning components
├── ui/                   # React frontend
└── benchmark_projects/   # Test projects
```

## Usage Workflows

### 1. Web Interface Workflow

1. **Project Upload**: Upload Java projects via web interface
2. **Project Analysis**: Generate Understand databases and detect code smells
3. **ML Training Configuration**: Set training parameters and objectives
4. **Training Execution**: Monitor real-time progress and task status
5. **Results Analysis**: Download trained models and analysis reports

### 2. CLI Workflow

```bash
# Direct refactoring execution
python codart/refactoring_cli.py --project-path /path/to/project

# Search-based optimization
python codart/sbse/search_based_refactoring2.py

# Individual refactoring testing
python tests/extract_method/test_1.py
```

### 3. API Integration

```bash
# Upload project
curl -X POST "http://localhost:8000/projects/upload" \
  -F "file=@project.zip" \
  -F "project_name=MyProject"

# Start ML training
curl -X POST "http://localhost:8000/ml-training/train" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "123", "config": {...}}'

# Monitor task
curl "http://localhost:8000/tasks/{task_id}/status"
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
# Core Paths
PROJECT_ROOT_DIR="/opt/projects"
UDB_ROOT_DIR="/opt/understand_dbs"

# SciTools Understand
STILICENSE="/root/.config/SciTools/License.conf"
STIHOME="/app/scitools"

# PMD Configuration
PMD_PATH="/app/pmd/bin/pmd"
PMD_RULESET="/app/pmd/rules/custom.xml"
PMD_CACHE_DIR="/app/pmd/cache"

# Algorithm Configuration
POPULATION_SIZE=15
MAX_ITERATIONS=15
PROBLEM=2  # Algorithm: 0=GA, 1=NSGA-II, 2=NSGA-III
NUMBER_OBJECTIVES=8

# Service URLs
CELERY_BROKER_URL="amqp://guest:guest@rabbitmq:5672//"
CELERY_RESULT_BACKEND="redis://redis:6379/0"
MINIO_ENDPOINT="minio:9000"
```

### Benchmark Projects

The system includes 14 benchmark projects:

- JSON20201115, JFreeChart, Weka, FreeMind
- Commons-codec, JRDF, JMetal, AntApache
- And more...

Configure via `BENCHMARK_INDEX` in config.py.

## Development

### Local Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup SciTools Understand
export PYTHONPATH="/path/to/understand/Python:$PYTHONPATH"
export PATH="/path/to/understand/bin:$PATH"

# Run API server
uvicorn application.main:app --reload

# Run UI development server
cd ui && npm start
```

### Adding New Refactorings

1. Implement refactoring in `codart/refactorings/`
2. Inherit from ANTLR listener/visitor classes
3. Add tests in `tests/` directory
4. Update refactoring registry in `handler.py`

### Testing

```bash
# Run individual refactoring tests
python tests/extract_method/test_1.py

# Test on benchmark projects
python codart/sbse/search_based_refactoring2.py
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