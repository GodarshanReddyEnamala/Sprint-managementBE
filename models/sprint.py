from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from database import Base
from datetime import datetime,timezone



class Sprint(Base):

    __tablename__="sprint"
    
    id=Column(Integer,primary_key=True,index=True)
    start_date= Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    end_date= Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    status = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)