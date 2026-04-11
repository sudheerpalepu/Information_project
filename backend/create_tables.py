# backend/create_tables.py
from backend.db import engine, Base
from backend.models import Company, Domain, Job

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")