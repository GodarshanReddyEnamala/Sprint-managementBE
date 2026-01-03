from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean
from database import Base 

class comment(Base):
    __tablename__="comment"

    id=Column(Integer,primary_key=True,index=True)
    Task_id=Column(Integer,ForeignKey("Task.id"),nullable=True)



