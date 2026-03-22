from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Allow CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV
df = pd.read_csv("jobs.csv")
df.columns = df.columns.str.strip()  # Remove any extra spaces

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/predict")
def predict(data: dict):
    background = data.get("background")
    domain = data.get("domain")
    
    # Filter dataframe
    filtered = df[(df['Background'] == background) & (df['Domain'] == domain)]
    
    jobs = len(filtered)
    salary = f"{filtered['Salary'].min()} - {filtered['Salary'].max()}" if jobs > 0 else "N/A"
    companies = filtered['Company'].tolist() if jobs > 0 else []

    return {
        "jobs": jobs,
        "salary": salary,
        "companies": companies
    }