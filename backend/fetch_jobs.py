from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
import random
from datetime import datetime
from backend.db import get_db
from backend.models import Job

router = APIRouter()

JOOBLE_API = "b44b7aca-074a-4425-819d-32a3add455d5"
ADZUNA_APP_ID = "db6dc542"
ADZUNA_API_KEY = "55a0e032e19564961dedb66c1b5a6f73"

DOMAIN_MAP = {
    "Computer Science": ["Data Science", "AIML", "Web Development", "Cybersecurity"],
    "Mechanical": ["Automobile", "Design", "Manufacturing"],
    "Finance": ["Accounting", "Investment Banking"],
    "Marketing": ["Digital Marketing", "Brand Management"]
}

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

            # ✅ FIX: STRICT FILTER
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

    # -------- ADZUNA MULTI COUNTRY + PAGINATION --------
    for country in ["us", "gb", "in"]:
        for page in range(1, 4):
            try:
                url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_API_KEY}&results_per_page=50&what={domain}"

                res = requests.get(url).json()

                for job in res.get("results", []):
                    title = (job.get("title") or "").lower()

                    # ✅ FIX: STRICT FILTER
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
    count = 0
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
        count += 1

    db.commit()

    print(f"✅ Inserted {count} jobs for {domain}")


@router.post("/fetch-all")
def fetch_all(db: Session = Depends(get_db)):

    # CLEAR OLD DATA
    db.query(Job).delete()
    db.commit()

    for bg, domains in DOMAIN_MAP.items():
        for d in domains:
            fetch_single(d, bg, db)

    return {"message": "All jobs inserted successfully"}