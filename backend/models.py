from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from backend.db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    domain = Column(String)
    background = Column(String)
    salary = Column(Float)
    source = Column(String)
    posted_at = Column(DateTime, default=datetime.utcnow)