from fastapi.testclient import TestClient
from video_gen_service.main import app
import os

client = TestClient(app)

def test_cut_video(sample_video):
    response = client.post("/video-edits/cut", json={
        "video_path": sample_video,
        "start_time": 0.0,
        "end_time": 1.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    # Clean up
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_concatenate_videos(sample_video, sample_video_2):
    response = client.post("/video-edits/concatenate", json={
        "video_paths": [sample_video, sample_video_2],
        "method": "compose"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_resize_video(sample_video):
    response = client.post("/video-edits/resize", json={
        "video_path": sample_video,
        "scale": 0.5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_speed_video(sample_video):
    response = client.post("/video-edits/speed", json={
        "video_path": sample_video,
        "factor": 2.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_color_effect_video(sample_video):
    # Test black and white
    response = client.post("/video-edits/color-effect", json={
        "video_path": sample_video,
        "effect_type": "blackwhite"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

    # Test invert
    response = client.post("/video-edits/color-effect", json={
        "video_path": sample_video,
        "effect_type": "invert"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])
