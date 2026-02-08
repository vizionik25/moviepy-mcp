from fastapi.testclient import TestClient
from video_gen_service.main import app
import os
import pytest

client = TestClient(app)

def test_audio_fade(sample_video_with_audio):
    # Fade In
    response = client.post("/audio/fade", json={
        "video_path": sample_video_with_audio,
        "fade_type": "in",
        "duration": 1.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

    # Fade Out
    response = client.post("/audio/fade", json={
        "video_path": sample_video_with_audio,
        "fade_type": "out",
        "duration": 1.0
    })
    assert response.status_code == 200
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_audio_fade_no_audio(sample_video):
    response = client.post("/audio/fade", json={
        "video_path": sample_video,
        "fade_type": "in",
        "duration": 1.0
    })
    assert response.status_code == 400

def test_audio_loop(sample_video_with_audio):
    response = client.post("/audio/loop", json={
        "video_path": sample_video_with_audio,
        "n": 2
    })
    if response.status_code != 200:
        print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_audio_loop_no_audio(sample_video):
    response = client.post("/audio/loop", json={
        "video_path": sample_video,
        "n": 2
    })
    assert response.status_code == 400
