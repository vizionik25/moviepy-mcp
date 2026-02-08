import os
import pytest
from unittest.mock import MagicMock, patch
from video_gen_service.video_utils import generate_simple_video, process_extract_audio
from video_gen_service.video_utils import generate_simple_video, process_audio_fade_video
from video_gen_service.video_utils import generate_simple_video, process_color_effect
from unittest.mock import patch
from video_gen_service.video_utils import generate_simple_video, get_unique_output_path
from video_gen_service.video_utils import generate_simple_video, process_mirror_video
from video_gen_service.video_utils import generate_simple_video, process_time_effect_video
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

def test_process_extract_audio_no_audio():
    """Test that extracting audio from a silent video raises ValueError."""
    # Mock os.path.exists to avoid needing a real file
    # We patch it specifically in the video_utils module
    with patch("video_gen_service.video_utils.os.path.exists", return_value=True):
        # Mock VideoFileClip to simulate a video with no audio track
        with patch("video_gen_service.video_utils.VideoFileClip") as MockVideoFileClip:
            mock_clip = MagicMock()
            mock_clip.audio = None
            # Configure context manager
            MockVideoFileClip.return_value.__enter__.return_value = mock_clip

            with pytest.raises(ValueError, match="Video has no audio"):
                process_extract_audio("dummy_video.mp4")
def test_process_audio_fade_video_no_audio(sample_video):
    """
    Test that process_audio_fade_video raises a ValueError when the input video has no audio.
    """
    with pytest.raises(ValueError, match="Video has no audio"):
        process_audio_fade_video(sample_video, fade_type="in", duration=1.0)
def test_process_color_effect_invalid_type(sample_video):
    """Test that process_color_effect raises ValueError for unknown effect types."""
    with pytest.raises(ValueError, match="Unknown effect type: invalid_effect"):
        process_color_effect(sample_video, "invalid_effect")
def test_get_unique_output_path():
    # Test basic functionality with default extension
    original_path = "/path/to/video.mp4"
    suffix = "test"
    output = get_unique_output_path(original_path, suffix)

    assert output.startswith("/path/to/video_test_")
    assert output.endswith(".mp4")
    assert len(output) > len("/path/to/video_test_.mp4")  # Should include UUID part

    # Test with custom extension
    output_custom = get_unique_output_path(original_path, suffix, ext=".mov")
    assert output_custom.startswith("/path/to/video_test_")
    assert output_custom.endswith(".mov")

    # Test file without extension
    no_ext_path = "/path/to/video"
    output_no_ext = get_unique_output_path(no_ext_path, suffix)
    assert output_no_ext.startswith("/path/to/video_test_")
    # It should look something like /path/to/video_test_<uuid>
    assert "." not in os.path.basename(output_no_ext).split("_")[-1]

    # Test uniqueness
    output1 = get_unique_output_path(original_path, suffix)
    output2 = get_unique_output_path(original_path, suffix)
    assert output1 != output2

    # Test without directory
    filename = "video.mp4"
    output_local = get_unique_output_path(filename, suffix)
    assert output_local.startswith("video_test_")
    assert output_local.endswith(".mp4")
    assert "/" not in output_local

    # Mock UUID for deterministic output check
    with patch('uuid.uuid4') as mock_uuid:
        # Configure mock to return an object with .hex attribute
        mock_uuid.return_value.hex = "1234567890abcdef"

        # Test default extension
        output_mocked = get_unique_output_path(original_path, suffix)
        expected = "/path/to/video_test_12345678.mp4"
        assert output_mocked == expected

        # Test explicit extension
        output_mocked_ext = get_unique_output_path(original_path, suffix, ext=".avi")
        expected_ext = "/path/to/video_test_12345678.avi"
        assert output_mocked_ext == expected_ext
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
def test_process_time_effect_video_error_handling(sample_video):
    """Test error handling for process_time_effect_video."""

    # Test unknown effect type
    with pytest.raises(ValueError, match="Unknown time effect: invalid_effect"):
        process_time_effect_video(sample_video, "invalid_effect")

    # Test freeze effect without duration
    with pytest.raises(ValueError, match="Duration required for freeze effect"):
        process_time_effect_video(sample_video, "freeze", duration=None)
def test_process_fade_video_invalid_type(sample_video):
    with pytest.raises(ValueError, match="Fade type must be 'in' or 'out'"):
        process_fade_video(sample_video, fade_type="invalid", duration=1.0)
