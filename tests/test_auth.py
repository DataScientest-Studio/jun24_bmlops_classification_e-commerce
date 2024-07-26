import sys
import os
from fastapi.testclient import TestClient

# Add the FastAPI directory to the system path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../FastAPI"))
)

from main import app  # Adjust this import based on where `app` is defined

client = TestClient(app)


def test_authentication():
    response = client.post("/api/auth", json={"username": "user", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
