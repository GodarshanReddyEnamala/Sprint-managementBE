from fastapi import FastAPI
from database import Base, engine
from models import task, project, user, sprint  # imports all models
from apis.task import router as task_router
from apis.project import router as project_router
from apis.user import router as user_router
from apis.sprint import router as sprint_router


app = FastAPI(
    title="Sprint Manager API",
    version="1.0.0",
)

# Create PostgreSQL tables
Base.metadata.create_all(bind=engine)


# Include API Routes
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(sprint_router, prefix="/sprints", tags=["Sprints"])
