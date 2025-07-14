from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from application.controllers import (
    learning_controller_testability,
    task_controller,
    project_management_controller,
)
from application.controllers.reporter import (
    export_metric_contoller,
    download_files_controller,
)
from application.controllers.rl import test_controller, rl_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(learning_controller_testability.app, prefix="/api/v1/learning")
app.include_router(project_management_controller.app, prefix="/api/v1")
app.include_router(export_metric_contoller.app, prefix="/api/v1/exporter")
app.include_router(task_controller.router, prefix="/api/v1/tasks")
app.include_router(download_files_controller.router, prefix="/api/v1/download")

app.include_router(test_controller.router, prefix="/api/v1/reinforcement")
app.include_router(rl_controller.router, prefix="/api/v1/rl-handler")
