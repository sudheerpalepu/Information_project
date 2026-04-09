from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.db import Base, engine, get_db, SessionLocal
from backend.models import Job
from backend.fetch_jobs import router as fetch_jobs_router, fetch_all

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(fetch_jobs_router)

# AUTO FETCH
@app.on_event("startup")
def startup():
    db = SessionLocal()
    fetch_all(db)
    db.close()

# -------- REQUEST MODELS --------
class PredictRequest(BaseModel):
    domain: str
    background: str

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    salary: float
    domain: str
    background: str

# -------- PREDICT --------
@app.post("/predict")
def predict(payload: PredictRequest, db: Session = Depends(get_db)):
    domain = payload.domain.lower()
    background = payload.background.lower()

    jobs = db.query(Job).all()

    filtered = [
        j for j in jobs
        if domain in j.domain.lower() and background in j.background.lower()
    ]

    companies = {}
    locations = {}
    salaries = []

    for j in filtered:
        companies[j.company] = companies.get(j.company, 0) + 1
        locations[j.location] = locations.get(j.location, 0) + 1
        salaries.append(j.salary)

    return {
        "jobs": [{
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "domain": j.domain,
            "location": j.location,
            "salary": j.salary
        } for j in filtered],
        "total_jobs": len(filtered),
        "total_companies": len(companies),
        "top_companies": sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5],
        "locations": locations,
        "salaries": salaries
    }

# -------- ADD JOB --------
@app.post("/add-job")
def add_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(**job.dict(), source="manual")
    db.add(new_job)
    db.commit()
    return {"message": "Job added"}

# -------- DELETE JOB --------
@app.delete("/delete-job/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"message": "Deleted"}
from fastapi import HTTPException

# 🔐 Hardcoded user (you can change)
USER_DATA = {
    "username": "sudheer",
    "password": "1234"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    if data.username == USER_DATA["username"] and data.password == USER_DATA["password"]:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")