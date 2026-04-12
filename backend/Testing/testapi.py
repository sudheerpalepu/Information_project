from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_fetch_jobs():
    response = client.get("/fetch_jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), dict) or isinstance(response.json(), list)