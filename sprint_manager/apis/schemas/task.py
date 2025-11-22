from pydantic import BaseModel
from datetime import date



class TaskCreate(BaseModel):

    name: str
    available: str | None = None
    cost: float | None = None
    code:str
    title:str
    work_type:str 
    work_flow:str
    story_points:int | None = None
    status:str 
    assign:str | None = None
    description:str 
    sub_task:str | None = None
    start_date:date | None = None
    end_date:date   | None = None
    activity :str | None = None
    details:str | None = None



class TaskUpdate(BaseModel):
    name: str
    available: str | None = None
    cost: float | None = None
    code:str    | None = None
    title:str | None = None
    work_type:str | None = None
    work_flow:str   | None = None
    story_points:int | None = None
    status:str | None = None
    assign:str | None = None
    description:str | None = None
    sub_task:str | None = None
    start_date:date | None = None
    end_date:date   | None = None
    activity :str | None = None
    details:str 
