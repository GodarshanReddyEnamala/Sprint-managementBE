from sqlalchemy import Column, Integer, String, Table, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

from models.association import user_projects

class Project(Base):
    __tablename__="project"
    
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True)
    users = relationship("User", secondary=user_projects, back_populates="projects")