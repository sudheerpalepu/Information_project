import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Read from Render environment variable
DATABASE_URL = os.getenv("postgresql://job_dashboard_db_user:ykbUEwpkoRbkqaK78EptHzaIKRgK2iQq@dpg-d7dq0n3bc2fs73e5nq50-a.oregon-postgres.render.com/job_dashboard_db")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set in environment variables")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()