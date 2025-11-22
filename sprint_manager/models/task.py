from sqlalchemy import Column, Integer, String, Boolean, Float, Enum, Text, Date
from database import Base



BugType = ('Bug', 'Task', 'Story', 'Review')
WorkflowType = ('Backlog', 'In Progress', 'On Hold', 'Done')
StatusType = ('Blocker', 'Critical', 'Major', 'Minor', 'Trivial')
ActivityType = ('All', 'Comments', 'History', 'Workflow')
DetailsType = (
    'Logwork', 'Sprint', 'Priority', 'EstimatedHours', 'Labels', 'Parent',
    'StartDate', 'EndDate', 'Reporter'
)


class Task(Base):
    __tablename__ = "task"
   # __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)
    available = Column(Boolean, default=True)
    cost = Column(Float)

    code = Column(String, index=True)
    title = Column(String, index=True)

    work_type = Column(Enum(*BugType, name="work_type_enum"), nullable=True)
    work_flow = Column(Enum(*WorkflowType, name="workflow_enum"), nullable=True)
    story_points = Column(Integer, nullable=True)

    status = Column(Enum(*StatusType, name="status_enum"), nullable=True)

    assign = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    sub_task = Column(String, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    activity = Column(Enum(*ActivityType, name="activity_enum"), nullable=True)
    details = Column(Enum(*DetailsType, name="details_enum"), nullable=True)
