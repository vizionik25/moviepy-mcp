import os
import pytest
from video_gen_service.video_utils import generate_simple_video, process_fade_video

def test_generate_simple_video():
    output = "test_output.mp4"
    try:
        # Use a short duration for speed
        result = generate_simple_video("Test Video", duration=0.5, output_file=output)
        assert result == output
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    finally:
        if os.path.exists(output):
            os.remove(output)

def test_process_fade_video_invalid_type(sample_video):
    with pytest.raises(ValueError, match="Fade type must be 'in' or 'out'"):
        process_fade_video(sample_video, fade_type="invalid", duration=1.0)
