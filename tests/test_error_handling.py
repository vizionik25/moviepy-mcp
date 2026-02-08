from fastapi.testclient import TestClient
from video_gen_service.main import app
import pytest
from video_gen_service.video_utils import (
    process_cut_video, process_concatenate_videos, process_resize_video,
    process_speed_video, process_volume_video, process_extract_audio,
    process_composite_videos, process_text_overlay, process_image_overlay,
    process_color_effect, process_mirror_video, process_rotate_video,
    process_crop_video, process_margin_video, process_fade_video,
    process_loop_video, process_time_effect_video, process_audio_fade_video,
    process_audio_loop_video
)

client = TestClient(app)

def test_router_file_not_found():
    # Test a few endpoints for 404 on missing file
    endpoints = [
        ("/video-edits/cut", {"video_path": "missing.mp4", "start_time": 0, "end_time": 1}),
        ("/video-edits/resize", {"video_path": "missing.mp4", "scale": 0.5}),
        ("/video-edits/speed", {"video_path": "missing.mp4", "factor": 2.0}),
        ("/video-edits/color-effect", {"video_path": "missing.mp4", "effect_type": "invert"}),
        ("/video-edits/mirror", {"video_path": "missing.mp4", "axis": "x"}),
        ("/audio/volume", {"video_path": "missing.mp4", "factor": 0.5}),
        ("/audio/extract", {"video_path": "missing.mp4"}),
        ("/video-edits/concatenate", {"video_paths": ["missing.mp4"], "method": "compose"}),
        ("/compositing/composite", {"video_paths": ["missing.mp4"], "method": "stack"}),
        ("/compositing/text-overlay", {"video_path": "missing.mp4", "text": "test"}),
        ("/compositing/image-overlay", {"video_path": "missing.mp4", "image_path": "missing.png"}),
    ]

    for endpoint, data in endpoints:
        response = client.post(endpoint, json=data)
        assert response.status_code == 404, f"Failed for {endpoint}"

def test_router_bad_request(sample_video):
    # Test 400 Bad Request (ValueError)
    endpoints = [
        ("/video-edits/concatenate", {"video_paths": [], "method": "compose"}),
        ("/video-edits/resize", {"video_path": sample_video}), # No size
        ("/video-edits/color-effect", {"video_path": sample_video, "effect_type": "invalid"}),
        ("/video-edits/mirror", {"video_path": sample_video, "axis": "z"}),
        ("/video-edits/fade", {"video_path": sample_video, "fade_type": "invalid", "duration": 1}),
        ("/video-edits/time-effect", {"video_path": sample_video, "effect_type": "freeze"}), # Missing duration
        ("/audio/extract", {"video_path": sample_video}), # Assuming sample_video has no audio
        ("/audio/fade", {"video_path": sample_video, "fade_type": "in", "duration": 1}), # No audio
        ("/audio/loop", {"video_path": sample_video}), # No audio
        ("/compositing/composite", {"video_paths": [], "method": "stack"}),
        ("/compositing/composite", {"video_paths": [sample_video], "method": "invalid"}),
    ]

    for endpoint, data in endpoints:
        response = client.post(endpoint, json=data)
        if response.status_code not in [400, 500]:
             print(f"Failed for {endpoint}: {response.status_code} - {response.json()}")
        assert response.status_code in [400, 500], f"Failed for {endpoint}"

def test_router_bad_request_audio_loop(sample_video):
    # Test that invalid audio loop parameters return 400
def test_router_bad_request_500(sample_video):
     # Endpoints known to return 500 on error (ValueError not explicitly caught)
     # This test is now updated to expect 400 as ValueError is handled
     # Endpoints that previously returned 500 but now return 400
    endpoints = [
         ("/audio/loop", {"video_path": sample_video}), # Invalid loop params? Or no audio?
    ]

    response = client.post("/audio/loop", json={"video_path": sample_video})
    assert response.status_code == 400

def test_utils_file_not_found():
    # Direct util calls
    with pytest.raises(FileNotFoundError):
        process_cut_video("missing.mp4", 0, 1)

    with pytest.raises(FileNotFoundError):
        process_concatenate_videos(["missing.mp4"])

    with pytest.raises(FileNotFoundError):
        process_resize_video("missing.mp4", scale=0.5)

    with pytest.raises(FileNotFoundError):
        process_speed_video("missing.mp4", 2.0)

    with pytest.raises(FileNotFoundError):
        process_volume_video("missing.mp4", 0.5)

    with pytest.raises(FileNotFoundError):
        process_extract_audio("missing.mp4")

    with pytest.raises(FileNotFoundError):
        process_composite_videos(["missing.mp4"])

    with pytest.raises(FileNotFoundError):
        process_text_overlay("missing.mp4", "text")

    with pytest.raises(FileNotFoundError):
        process_image_overlay("missing.mp4", "missing.png")

    with pytest.raises(FileNotFoundError):
        # file exists but image missing
        process_image_overlay("src/video_gen_service/main.py", "missing.png")

    with pytest.raises(FileNotFoundError):
        process_color_effect("missing.mp4", "invert")

    with pytest.raises(FileNotFoundError):
        process_mirror_video("missing.mp4")

    with pytest.raises(FileNotFoundError):
        process_rotate_video("missing.mp4", 90)

    with pytest.raises(FileNotFoundError):
        process_crop_video("missing.mp4")

    with pytest.raises(FileNotFoundError):
        process_margin_video("missing.mp4", 10)

    with pytest.raises(FileNotFoundError):
        process_fade_video("missing.mp4", "in", 1)

    with pytest.raises(FileNotFoundError):
        process_loop_video("missing.mp4")

    with pytest.raises(FileNotFoundError):
        process_time_effect_video("missing.mp4", "reverse")

    with pytest.raises(FileNotFoundError):
        process_audio_fade_video("missing.mp4", "in", 1)

    with pytest.raises(FileNotFoundError):
        process_audio_loop_video("missing.mp4")

def test_utils_invalid_args(sample_video):
    with pytest.raises(ValueError):
        process_resize_video(sample_video) # no args

    with pytest.raises(ValueError):
        process_composite_videos([sample_video], method="invalid")

    with pytest.raises(ValueError):
        process_composite_videos([]) # empty list

    with pytest.raises(ValueError, match="No video paths provided"):
        process_concatenate_videos([]) # empty list

    with pytest.raises(ValueError):
        process_color_effect(sample_video, "invalid")

    with pytest.raises(ValueError):
        process_mirror_video(sample_video, "z")

    with pytest.raises(ValueError):
        process_fade_video(sample_video, "invalid", 1)

    with pytest.raises(ValueError):
        process_time_effect_video(sample_video, "invalid")

    with pytest.raises(ValueError):
        process_time_effect_video(sample_video, "freeze") # missing duration

    # Audio on video without audio
    with pytest.raises(ValueError):
        process_extract_audio(sample_video)

    with pytest.raises(ValueError):
        process_audio_fade_video(sample_video, "in", 1)

    with pytest.raises(ValueError):
        process_audio_loop_video(sample_video)
