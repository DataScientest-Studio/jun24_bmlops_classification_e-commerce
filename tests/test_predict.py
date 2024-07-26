import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../FastAPI"))
)

from predict import app  # Adjust based on the actual location of `app`

client = TestClient(app)


def test_prediction():
    response = client.post(
        "/api/predict",
        json={"product_description": "A sample product", "image_path": "path/to/image"},
    )
    assert response.status_code == 200
    assert "category" in response.json()
