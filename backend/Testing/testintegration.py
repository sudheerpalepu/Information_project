from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_jobs_flow():
    response = client.get("/fetch_jobs")

    assert response.status_code == 200

    data = response.json()

    # check structure (adjust based on your API)
    assert data is not None