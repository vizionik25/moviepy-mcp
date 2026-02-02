from fastapi.testclient import TestClient
from video_gen_service.main import app
import os
import pytest

client = TestClient(app)

def test_mirror_video(sample_video):
    response = client.post("/video-edits/mirror", json={
        "video_path": sample_video,
        "axis": "x"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

    response = client.post("/video-edits/mirror", json={
        "video_path": sample_video,
        "axis": "y"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

    # Test error
    response = client.post("/video-edits/mirror", json={
        "video_path": sample_video,
        "axis": "z"
    })
    assert response.status_code == 400

def test_rotate_video(sample_video):
    response = client.post("/video-edits/rotate", json={
        "video_path": sample_video,
        "angle": 90
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_crop_video(sample_video):
    response = client.post("/video-edits/crop", json={
        "video_path": sample_video,
        "x1": 0,
        "y1": 0,
        "width": 100,
        "height": 100
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_margin_video(sample_video):
    response = client.post("/video-edits/margin", json={
        "video_path": sample_video,
        "margin": 10,
        "color": [255, 0, 0],
        "opacity": 1.0
    })
    if response.status_code != 200:
        print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_fade_video(sample_video):
    # Fade In
    response = client.post("/video-edits/fade", json={
        "video_path": sample_video,
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
    response = client.post("/video-edits/fade", json={
        "video_path": sample_video,
        "fade_type": "out",
        "duration": 1.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

    # Error
    response = client.post("/video-edits/fade", json={
        "video_path": sample_video,
        "fade_type": "invalid",
        "duration": 1.0
    })
    assert response.status_code == 400

def test_loop_video(sample_video):
    response = client.post("/video-edits/loop", json={
        "video_path": sample_video,
        "n": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_time_effect_video(sample_video):
    # Reverse
    response = client.post("/video-edits/time-effect", json={
        "video_path": sample_video,
        "effect_type": "reverse"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

    # Symmetrize
    response = client.post("/video-edits/time-effect", json={
        "video_path": sample_video,
        "effect_type": "symmetrize"
    })
    assert response.status_code == 200
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

    # Freeze
    response = client.post("/video-edits/time-effect", json={
        "video_path": sample_video,
        "effect_type": "freeze",
        "duration": 1.0
    })
    assert response.status_code == 200
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

    # Freeze Error
    response = client.post("/video-edits/time-effect", json={
        "video_path": sample_video,
        "effect_type": "freeze"
        # Missing duration
    })
    assert response.status_code == 400
