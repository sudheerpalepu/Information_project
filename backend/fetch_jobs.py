from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
import random
from datetime import datetime
from backend.db import get_db
from backend.models import Job

router = APIRouter()

JOOBLE_API = "b44b7aca-074a-4425-819d-32a3add455d5"
ADZUNA_APP_ID = "95dde1df"
ADZUNA_API_KEY = "d85b9828304c987397ea29b5ff4156ca"

def fetch_single(domain, background, db: Session):
    domain = domain.strip()
    background = background.strip()

    jobs_to_insert = []

    print(f"🔍 Fetching {domain}")

    # -------- JOOBLE --------
    try:
        url = f"https://jooble.org/api/{JOOBLE_API}"
        payload = {"keywords": domain, "location": ""}

        res = requests.post(url, json=payload).json()

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
        for page in range(1, 4):
            try:
                url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_API_KEY}&results_per_page=50&what={domain}"

                res = requests.get(url).json()

                for job in res.get("results", []):
                    title = (job.get("title") or "").lower()

                    if domain.lower() not in title:
                        continue

                    salary = job.get("salary_min")

                    if salary:
                        salary = round(salary / 100000, 2)
                    else:
                        salary = round(random.uniform(3, 15), 2)

                    jobs_to_insert.append({
                        "title": job.get("title"),
                        "company": job.get("company", {}).get("display_name", "Unknown"),
                        "location": job.get("location", {}).get("display_name") or "Remote",
                        "salary": salary
                    })
            except Exception as e:
                print("Adzuna error:", e)

    # -------- INSERT --------
    db.query(Job).filter(
        Job.domain == domain,
        Job.background == background
    ).delete()
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

    print(f"✅ Inserted {len(jobs_to_insert)} jobs for {domain}")


# ✅ NEW API (IMPORTANT)
@router.post("/fetch-domain")
def fetch_domain(payload: dict, db: Session = Depends(get_db)):
    domain = payload.get("domain")
    background = payload.get("background")

    if not domain or not background:
        return {"error": "Domain and background required"}

    fetch_single(domain, background, db)

    return {"message": f"{domain} jobs fetched successfully"}