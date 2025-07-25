#!/usr/bin/env python3
"""
CodART System Architecture Diagram
Generates diagrams showing the application infrastructure and RL learning components
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.network import ALB
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.programming.framework import React, Fastapi
from diagrams.programming.language import Python, Java
from diagrams.onprem.analytics import Spark
from diagrams.onprem.monitoring import Grafana
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Rack
from diagrams.onprem.database import Postgresql
from diagrams.generic.network import Firewall

# Create the main system architecture diagram
with Diagram("CodART System Architecture", show=False, filename="codart_system_arch", direction="TB"):
    
    # User Interface Layer
    with Cluster("User Interface"):
        users = Users("Users")
        ui = React("React UI\n(Port 3000)")
    
    # API Gateway Layer  
    with Cluster("API Gateway"):
        nginx = ALB("Nginx Proxy\n(Port 80)")
        api = Fastapi("FastAPI Server\n(Port 8000)")
    
    # Application Services Layer
    with Cluster("Application Services"):
        with Cluster("API Container (Privileged)"):
            celery_worker = Python("Celery Worker\n(ML Training)")
            api_server = Server("API Server\n(uvicorn)")
            scitools = Java("SciTools Understand\n(Code Analysis)")
            pmd = Java("PMD 7.11.0\n(Code Smell Detection)")
            
        with Cluster("External License"):
            licensing = Firewall("SciTools License\n(licensing.scitools.com)")
    
    # Quality Analysis Layer
    with Cluster("Quality Analysis"):
        testability_models = Spark("Testability ML Models\n(7 Model Types)")
        pmd_rules = Storage("PMD Custom Rules\n(XML Configuration)")
        smell_reports = Storage("Code Smell Reports\n(CSV Format)")
    
    # Message Queue & Cache Layer
    with Cluster("Message & Cache Layer"):
        rabbitmq = Rabbitmq("Rabbitmq\n(Message Broker)")
        redis = Redis("Redis\n(Result Backend)")
    
    # Storage Layer
    with Cluster("Storage Layer"):
        minio = S3("MinIO\n(Object Storage)")
        volumes = Storage("Docker Volumes\n(Persistent Data)")
    
    # Docker Infrastructure Layer
    with Cluster("Docker Infrastructure"):
        with Cluster("Networks"):
            internal_net = Storage("Internal Network\n(Bridge)")
            default_net = Storage("Default Network\n(Bridge)")
        
        with Cluster("Persistent Volumes"):
            vol_projects = Storage("Projects Volume\n(/opt/projects)")
            vol_und_dbs = Storage("UDB Volume\n(/opt/understand_dbs)")
            vol_csv_pmd = Storage("CSV Reports\n(/opt/csv_reports)")
            vol_scitools = Storage("SciTools Config\n(/root/.config)")
    
    # Data Flow Connections
    users >> ui >> nginx >> api
    nginx >> ui
    api >> api_server
    api_server >> celery_worker
    celery_worker >> rabbitmq
    celery_worker >> redis
    celery_worker >> scitools
    celery_worker >> pmd
    celery_worker >> minio
    api_server >> vol_projects
    api_server >> vol_und_dbs
    scitools >> licensing
    
    # Quality Analysis Flows
    pmd >> pmd_rules
    pmd >> smell_reports >> minio
    celery_worker >> testability_models
    testability_models >> minio

# Create the Reinforcement Learning Architecture diagram
with Diagram("CodART Reinforcement Learning Architecture", show=False, filename="codart_rl_arch", direction="TB"):
    
    # Input Data Layer
    with Cluster("Input Data Sources"):
        projects = Storage("Java Projects\n(/opt/projects)")
        understand_db = Postgresql("Understand DB\n(.und files)")
        code_smells = Storage("PMD Code Smells\n(CSV Reports)")
        testability_data = Storage("Testability Dataset\n(262 Metrics)")
    
    # Environment Layer
    with Cluster("RL Environment"):
        env = Rack("RefactoringSequenceEnvironment")
        transforms = Server("Transforms\n(Normalization)")
        
        with Cluster("Environment Components"):
            smell_init = Python("SmellInitialization\n(PMD Integration)")
            refactor_mgr = Python("RefactoringManager\n(Apply Operations)")
            metrics = Python("QualityMetrics\n(QMOOD, Testability)")
            testability_pred = Spark("Testability Predictor\n(ML Models)")
    
    # Agent & Training Layer
    with Cluster("RL Agent & Training"):
        with Cluster("Neural Networks"):
            policy_net = Spark("Policy Network\n(Actor)")
            value_net = Spark("Value Network\n(Critic)")
        
        with Cluster("Training Components"):
            trainer = Python("RefactoringTrainer\n(PPO Algorithm)")
            collector = Python("Data Collector\n(Experience)")
            replay_buffer = Redis("Replay Buffer\n(Experience Storage)")
    
    # Optimization & Objectives
    with Cluster("Multi-Objective Optimization"):
        objectives = Server("8 Design Objectives\n(ANA, CAMC, CIS, etc.)")
        reward_calc = Python("Reward Calculator\n(Multi-objective)")
    
    # Results & Monitoring
    with Cluster("Results & Monitoring"):
        model_storage = S3("Model Checkpoints\n(MinIO)")
        training_metrics = Storage("Training Metrics\n(CSV)")
        evaluation = Grafana("Evaluation Results\n(Performance)")
    
    # Data Flow for RL Training
    projects >> understand_db >> smell_init
    code_smells >> smell_init
    testability_data >> testability_pred
    smell_init >> env
    env >> transforms >> trainer
    
    trainer >> collector >> replay_buffer
    trainer >> policy_net
    trainer >> value_net
    
    refactor_mgr >> metrics >> objectives
    testability_pred >> objectives
    objectives >> reward_calc >> env
    
    trainer >> model_storage
    trainer >> training_metrics
    trainer >> evaluation

# Create the detailed ML Training Pipeline diagram
with Diagram("ML Training Pipeline Flow", show=False, filename="codart_ml_pipeline", direction="LR"):
    
    # API Request Flow
    with Cluster("API Request"):
        api_request = Users("API Call\n/ml-training/train")
        task_queue = Rabbitmq("Celery Task Queue\nml_training")
    
    # Training Initialization
    with Cluster("Training Setup"):
        config_validation = Server("Config Validation")
        env_creation = Python("Environment Creation")
        trainer_init = Python("Trainer Initialization")
    
    # Training Loop
    with Cluster("Training Loop"):
        with Cluster("PPO Training Steps"):
            data_collection = Python("1. Data Collection\n(Experience Gathering)")
            advantage_calc = Python("2. Advantage Calculation\n(GAE)")
            policy_update = Python("3. Policy Update\n(PPO Loss)")
            value_update = Python("4. Value Update\n(MSE Loss)")
    
    # Environment Interaction
    with Cluster("Environment Interaction"):
        action_generation = Python("Action Generation\n(Policy Network)")
        refactoring_exec = Java("Refactoring Execution\n(SciTools)")
        reward_computation = Python("Reward Computation\n(Multi-objective)")
        state_update = Python("State Update\n(Metrics)")
    
    # Monitoring & Storage
    with Cluster("Monitoring & Persistence"):
        progress_tracking = Grafana("Progress Tracking\n(Celery Updates)")
        checkpoint_save = S3("Checkpoint Saving\n(MinIO)")
        metrics_logging = Storage("Metrics Logging\n(CSV)")
    
    # Pipeline Flow
    api_request >> task_queue >> config_validation
    config_validation >> env_creation >> trainer_init
    
    trainer_init >> data_collection
    data_collection >> advantage_calc >> policy_update >> value_update
    
    data_collection >> action_generation >> refactoring_exec
    refactoring_exec >> reward_computation >> state_update
    state_update >> data_collection
    
    policy_update >> progress_tracking
    value_update >> checkpoint_save
    trainer_init >> metrics_logging

print("✅ Architecture diagrams generated successfully!")
print("📊 Generated files:")
print("   - codart_system_arch.png - Overall system architecture")
print("   - codart_rl_arch.png - Reinforcement learning components")  
print("   - codart_ml_pipeline.png - ML training pipeline flow")