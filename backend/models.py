from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"   # Must match your DB table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    background = Column(String, nullable=True)
    salary = Column(Float, nullable=True)
    source = Column(String, nullable=True)
    posted_at = Column(DateTime, default=datetime.utcnow)