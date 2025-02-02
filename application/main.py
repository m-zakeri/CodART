from fastapi import FastAPI
from application.controllers import learning_controller_testability, task_controller, project_management_controller

app = FastAPI()

# Include routers
app.include_router(learning_controller_testability.app, prefix="/api/v1/learning")
app.include_router(project_management_controller.app, prefix="/api/v1/projects")
app.include_router(task_controller.router, prefix="/tasks")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)