from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class IssueModel(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    status = Column(String, default="open")
    created_at = Column(DateTime, server_default=func.now())