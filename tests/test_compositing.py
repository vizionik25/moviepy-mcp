from fastapi.testclient import TestClient
from video_gen_service.main import app
from video_gen_service.video_utils import create_text_image
import os
import tempfile

client = TestClient(app)

def test_composite_videos_stack(sample_video, sample_video_2):
    response = client.post("/compositing/composite", json={
        "video_paths": [sample_video, sample_video_2],
        "method": "stack"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_composite_videos_grid(sample_video, sample_video_2):
    response = client.post("/compositing/composite", json={
        "video_paths": [sample_video, sample_video_2],
        "method": "grid"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_text_overlay(sample_video):
    response = client.post("/compositing/text-overlay", json={
        "video_path": sample_video,
        "text": "Overlay Test",
        "fontsize": 40,
        "color": "red",
        "position": "center",
        "start_time": 0.5,
        "duration": 1.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert os.path.exists(data["output_path"])
    if os.path.exists(data["output_path"]):
        os.remove(data["output_path"])

def test_image_overlay(sample_video):
    # Create a temp image
    img_path = create_text_image("Img", size=(100, 100), bg_color="blue")

    try:
        response = client.post("/compositing/image-overlay", json={
            "video_path": sample_video,
            "image_path": img_path,
            "position": "center",
            "scale": 0.5,
            "opacity": 0.8,
            "start_time": 0.5,
            "duration": 1.0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert os.path.exists(data["output_path"])
        if os.path.exists(data["output_path"]):
            os.remove(data["output_path"])
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)
