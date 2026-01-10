from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.project import Project
from apis.schemas.project import AssignUsers, ProjectCreate, ProjectUpdate
from models.user import User

router = APIRouter()


# CREATE PROJECT
@router.post("/")
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    # 1. Fetch existing User objects from the DB using the IDs provided
    # project_data.users is a list of ints like [1, 2, 3]
    users_to_add = db.query(User).filter(User.id.in_(project_data.users)).all()

    # 2. Create the Project instance
    new_project = Project(title=project_data.title)

    # 3. Establish the relationship
    # This automatically creates entries in the 'user_projects' table
    new_project.users = users_to_add

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project



# Get all projects
@router.get("/user/{user_id}")
def get_projects_by_user(user_id: int, db: Session = Depends(get_db), ):
    return db.query(Project).join(Project.users).filter(User.id == user_id).all()


# GET PROJECT
@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


# UPDATE PROJECT
@router.put("/{project_id}")
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


# DELETE PROJECT
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}


@router.post("/add-users/{project_id}")
def add_users_to_project(project_id: int, data: AssignUsers, db: Session = Depends(get_db)):

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    users = db.query(User).filter(User.id.in_(data.user_ids)).all()
    if not users:
        raise HTTPException(status_code=404, detail="No valid users found") 
    for user in users:
        if user not in project.users:
            project.users.append(user)

    db.commit()
    return {"message": "Projects added to user"}