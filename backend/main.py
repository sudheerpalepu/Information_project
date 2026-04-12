from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from backend.db import Base, engine, get_db
from backend.models import Job
from backend.fetch_jobs import router as fetch_jobs_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(fetch_jobs_router)


# ---------- JOBS ----------
@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


@app.post("/add-job")
def add_job(job: dict, db: Session = Depends(get_db)):
    new_job = Job(**job, source="manual")
    db.add(new_job)
    db.commit()
    return {"message": "added"}


@app.delete("/delete-job/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404, "Not found")
    db.delete(job)
    db.commit()
    return {"message": "deleted"}


# ---------- LOGIN ----------
@app.post("/login")
def login(data: dict):
    if data["username"] == "sudheer" and data["password"] == "1234":
        return {"message": "success"}
    raise HTTPException(401, "invalid")