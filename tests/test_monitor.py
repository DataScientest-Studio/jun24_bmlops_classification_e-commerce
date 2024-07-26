import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../FastAPI"))
)

from monitor import app  # Adjust based on the actual location of `app`

client = TestClient(app)


def test_monitor():
    response = client.get("/api/monitor")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "model_performance" in response.json()
