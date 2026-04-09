from pydantic import BaseModel
from typing import Optional


# -----------------------------
# Job CRUD
# -----------------------------
class JobCreate(BaseModel):
    title: str
    company: str
    domain: str
    background: str
    location: Optional[str] = None
    salary: Optional[float] = None


# -----------------------------
# Predict request
# -----------------------------
class PredictRequest(BaseModel):
    domain: str