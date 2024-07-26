import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../FastAPI"))
)

from data_ingest import app  # Adjust based on the actual location of `app`

client = TestClient(app)


def test_data_ingestion():
    response = client.post(
        "/api/data-ingest",
        json={
            "product_id": "123",
            "description": "A sample product",
            "image_path": "path/to/image",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
