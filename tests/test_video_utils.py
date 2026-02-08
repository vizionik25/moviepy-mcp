import os
import pytest
from video_gen_service.video_utils import generate_simple_video, process_resize_video

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

def test_process_resize_video_invalid_args(sample_video):
    """Test that process_resize_video raises ValueError when no resize parameters are provided."""
    with pytest.raises(ValueError, match="Must provide scale, width, or height"):
        process_resize_video(sample_video)
