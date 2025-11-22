from pydantic import BaseModel

class SprintCreate(BaseModel):
    name: str
    start_date: str
    end_date: str

class SprintUpdate(BaseModel):
    name: str | None = None
    start_date: str | None = None
    end_date: str | None = None
