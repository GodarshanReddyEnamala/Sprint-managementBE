from sqlalchemy import Column, Integer, Date
from database import Base



class Sprint(Base):
    __tablename__="sprint"
    id=Column(Integer,primary_key=True,index=True)
    start_date=Column(Date,nullable=True)
    end_date=Column(Date,nullable=True)