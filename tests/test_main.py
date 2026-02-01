from fastapi.testclient import TestClient
from video_gen_service.main import app
import os

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Video Generation Service"}

def test_generate_video_endpoint():
    # Use short duration to speed up test
    payload = {"text": "API Test", "duration": 0.5}
    response = client.post("/video/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "file_path" in data

    file_path = data["file_path"]
    assert os.path.exists(file_path)

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)
