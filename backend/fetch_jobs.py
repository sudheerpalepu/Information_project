from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests, random
from datetime import datetime
from backend.db import get_db
from backend.models import Job

router = APIRouter()

JOOBLE_API = "b44b7aca-074a-4425-819d-32a3add455d5"
ADZUNA_APP_ID = "95dde1df"
ADZUNA_API_KEY = "d85b9828304c987397ea29b5ff4156ca"

def fetch_single(domain, background, db: Session):

    jobs_to_insert = []

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
    except:
        pass

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
            except:
                pass

    db.query(Job).filter(Job.domain == domain, Job.background == background).delete()
    db.commit()

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
def fetch_domain(payload: dict, db: Session = Depends(get_db)):
    fetch_single(payload["domain"], payload["background"], db)
    return {"message": "fetched"}