import os
import pytest
from video_gen_service.video_utils import generate_simple_video, process_mirror_video

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

def test_process_mirror_video_error_handling(sample_video):
    """Test that process_mirror_video raises ValueError for invalid axis."""
    with pytest.raises(ValueError, match="Axis must be 'x' or 'y'"):
        process_mirror_video(sample_video, axis="z")

def test_process_mirror_video_success(sample_video):
    """Test that process_mirror_video works for valid axis."""
    output_x = process_mirror_video(sample_video, axis="x")
    assert os.path.exists(output_x)
    assert os.path.getsize(output_x) > 0
    os.remove(output_x)

    output_y = process_mirror_video(sample_video, axis="y")
    assert os.path.exists(output_y)
    assert os.path.getsize(output_y) > 0
    os.remove(output_y)
