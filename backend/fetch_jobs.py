from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests, random
from datetime import datetime
from backend.db import get_db
from backend.models import Job
from pydantic import BaseModel

class FetchDomainRequest(BaseModel):
    domain: str
    background: str

router = APIRouter()

JOOBLE_API = "7c3d4eae-538c-48a7-af32-b57f3a3ad6d6"
ADZUNA_APP_ID = "db6dc542"
ADZUNA_API_KEY = "55a0e032e19564961dedb66c1b5a6f73"

def fetch_single(domain, background, db: Session):

    if not domain or not background:
        raise HTTPException(status_code=400, detail="Domain and background required")

    jobs_to_insert = []

    # -------- JOOBLE --------
    try:
        url = f"https://jooble.org/api/{JOOBLE_API}"
        res = requests.post(url, json={"keywords": domain}).json()

        for job in res.get("jobs", []):
            title = (job.get("title") or "").lower()

            if domain.lower() not in title:
                continue

            jobs_to_insert.append({
                "title": job.get("title"),
                "company": job.get("company") or "Unknown",
                "location": job.get("location") or "Remote",
                "salary": round(random.uniform(3, 12), 2)
            })
    except Exception as e:
        print("Jooble error:", e)

    # -------- ADZUNA --------
    for country in ["us", "gb", "in"]:
        for page in range(1, 2):
            try:
                url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
                params = {
                    "app_id": ADZUNA_APP_ID,
                    "app_key": ADZUNA_API_KEY,
                    "what": domain,
                    "results_per_page": 20
                }

                res = requests.get(url, params=params).json()

                for job in res.get("results", []):
                    title = (job.get("title") or "").lower()

                    # ✅ FIXED CONDITION
                    if domain.lower() not in title:
                        continue

                    salary = job.get("salary_min")
                    salary = round(salary / 100000, 2) if salary else round(random.uniform(3, 10), 2)

                    jobs_to_insert.append({
                        "title": job.get("title"),
                        "company": job.get("company", {}).get("display_name", "Unknown"),
                        "location": job.get("location", {}).get("display_name", "Remote"),
                        "salary": salary
                    })
            except Exception as e:
                print("Adzuna error:", e)

    # -------- CLEAN OLD DATA --------
    db.query(Job).filter(
        Job.domain == domain,
        Job.background == background
    ).delete()
    db.commit()

    # -------- INSERT --------
    for j in jobs_to_insert:
        db.add(Job(
            title=j["title"],
            company=j["company"],
            location=j["location"],
            domain=domain,
            background=background,
            salary=j["salary"],
            source="api",
            posted_at=datetime.utcnow()
        ))

    db.commit()


@router.post("/fetch-domain")
def fetch_domain(payload: FetchDomainRequest, db: Session = Depends(get_db)):
    fetch_single(payload.domain, payload.background, db)
    return {"message": "fetched successfully"}
