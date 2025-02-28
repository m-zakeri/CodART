from fastapi import FastAPI
from application.controllers import (
    learning_controller_testability,
    task_controller,
    project_management_controller,
)
from application.controllers.reporter import (
    export_metric_contoller,
    download_files_controller,
)
from application.controllers.rl import test_controller

app = FastAPI()

# Include routers
app.include_router(learning_controller_testability.app, prefix="/api/v1/learning")
app.include_router(project_management_controller.app, prefix="/api/v1/projects")
app.include_router(export_metric_contoller.app, prefix="/api/v1/exporter")
app.include_router(task_controller.router, prefix="/api/v1/tasks")
app.include_router(download_files_controller.router, prefix="/api/v1/downloads")
app.include_router(test_controller.router, prefix="/api/v1/reinforcement")
