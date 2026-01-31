from pydantic import BaseModel, Field
from datetime import datetime, timezone


class SprintCreate(BaseModel):
    
    start_date: datetime = datetime.now(timezone.utc)
    end_date: datetime = datetime.now(timezone.utc)
    project_id: int
    status: bool = False


class SprintUpdate(BaseModel):
    start_date: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_date: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))
    project_id: int
    status: bool = False
