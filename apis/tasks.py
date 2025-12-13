from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.task import Task
from apis.schemas.task import TaskCreate, TaskUpdate
from apis.ai import send_task_to_gemini

router = APIRouter()




@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):\

    # Find last code
    last_task = db.query(Task).order_by(Task.code.desc()).first()
    new_code = int(last_task.code) + 1 if last_task else 1001


    # Create Task instance with code
    new_task = Task(
        work_type=task.work_type,
        title=task.title,
        work_flow=task.work_flow,
        story_points=task.story_points,
        priority=task.priority,
        user_id=task.user_id,
        parent_task=task.parent_task,
        sprint_id=task.sprint_id,
        project_id=task.project_id,
        description=task.description,
        code=new_code  

    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    

    return {
        "task": new_task
       
    }



# GET TASK BY ID
@router.get("/{id}")
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

# Get all tasks
@router.get("/")
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# UPDATE TASK
@router.put("/{id}")
def update_task(id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


# UPDATE DESCRIPTION
@router.put("/{id}/description")
def update_description(id: int,  db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        description = send_task_to_gemini(db_task.title)
      
    except Exception as e:
        description = {"error": str(e)}

    db_task.description= description

    db.commit()
    db.refresh(db_task)
    return db_task


# DELETE TASK
@router.delete("/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
