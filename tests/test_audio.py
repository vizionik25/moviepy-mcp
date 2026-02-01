from fastapi.testclient import TestClient
from video_gen_service.main import app
import os

client = TestClient(app)

def test_volume_adjust(sample_video_with_audio):
    response = client.post("/audio/volume", json={
        "video_path": sample_video_with_audio,
        "factor": 0.5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_extract_audio(sample_video_with_audio):
    response = client.post("/audio/extract", json={
        "video_path": sample_video_with_audio
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_extract_audio_no_audio(sample_video):
    response = client.post("/audio/extract", json={
        "video_path": sample_video
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Video has no audio"
