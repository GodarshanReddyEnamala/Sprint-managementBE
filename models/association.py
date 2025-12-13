from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

user_projects = Table(
    "user_projects",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True)
)
