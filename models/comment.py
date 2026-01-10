from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Comment(Base):
    
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    content = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.timezone.utc, nullable=False)

    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)

    # Relationships
    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")

    replies = relationship(
        "Comment",
        backref="parent",
        remote_side=[id]
    )