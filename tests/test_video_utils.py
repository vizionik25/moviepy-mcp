import os
import pytest
from unittest.mock import patch
from video_gen_service.video_utils import (
    generate_simple_video,
    process_extract_audio,
    process_resize_video,
    process_audio_fade_video,
    process_audio_loop_video,
from unittest.mock import MagicMock, patch
from video_gen_service.video_utils import generate_simple_video, process_audio_loop_video
from video_gen_service.video_utils import process_concatenate_videos

def test_process_concatenate_videos_empty_list():
    """
    Test that process_concatenate_videos raises a ValueError with the correct message
    when provided with an empty list of video paths.
    """
    with pytest.raises(ValueError, match="No video paths provided"):
        process_concatenate_videos([])
from unittest.mock import MagicMock, patch
from moviepy import VideoFileClip

from video_gen_service.video_utils import (
    generate_simple_video,
    process_audio_loop_video,
    process_resize_video,
    process_extract_audio,
    process_audio_fade_video,
    process_color_effect,
    get_unique_output_path,
    process_mirror_video,
    process_time_effect_video,
    process_fade_video
)
    process_fade_video,
    process_fade_video
)

def test_process_audio_loop_video_no_audio(sample_video):
    """
    Test that process_audio_loop_video raises a ValueError with the correct message
    when provided with a video that has no audio track.
    """
    with pytest.raises(ValueError, match="Video has no audio"):
        process_audio_loop_video(sample_video, n=2)

def test_process_audio_loop_video_success(sample_video_with_audio):
    """Test that process_audio_loop_video works correctly with valid input."""
    output = process_audio_loop_video(sample_video_with_audio, n=2)
    assert os.path.exists(output)
    assert os.path.getsize(output) > 0

    # Verify the output has audio
    with VideoFileClip(output) as video:
         assert video.audio is not None

    if os.path.exists(output):
        os.remove(output)

def test_generate_simple_video():
    output = "test_output.mp4"
    try:
        # Use a short duration for speed
        result = generate_simple_video("Test Video", duration=0.5, output_file=output)
        # Fix: compare absolute paths
        assert os.path.abspath(result) == os.path.abspath(output)
        # Use abspath because generate_simple_video returns absolute path
        assert os.path.abspath(result) == os.path.abspath(output)
        assert os.path.abspath(result) == os.path.abspath(output)
        # generate_simple_video returns absolute path, so we check if it ends with our output filename
        # generate_simple_video returns an absolute path, so we check if it ends with our output filename
        # Check if result ends with the output filename, as it returns an absolute path
        assert os.path.basename(result) == output
        assert result == os.path.abspath(output)
        # result is absolute path, output is relative
        assert os.path.abspath(output) == result
        # generate_simple_video returns absolute path
        # result is absolute path, output is relative
        assert result == os.path.abspath(output)
        assert result == os.path.abspath(output)
        # Ensure result ends with the requested output filename (it might be absolute path)
        assert result.endswith(output)
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    finally:
        # Cleanup potentially created file (absolute path or relative)
        if os.path.exists(output):
            os.remove(output)
        # Also try to remove the absolute path version if it's different and exists
        if os.path.exists(os.path.abspath(output)):
             os.remove(os.path.abspath(output))
        # Also try to remove absolute path if returned differently
        abs_output = os.path.abspath(output)
        if os.path.exists(abs_output):
            os.remove(abs_output)
        # Also try to remove absolute path if known/different
        # But 'result' might be out of scope if exception occurred, so rely on 'output'
        # If 'result' is returned, we can try cleaning it too
        pass
        # Cleanup potentially absolute path
        if os.path.exists(output):
            os.remove(output)
        # Check absolute path too just in case
        abs_path = os.path.abspath(output)
        if os.path.exists(abs_path):
            os.remove(abs_path)
        elif os.path.exists(os.path.abspath(output)):
             os.remove(os.path.abspath(output))

def test_process_audio_loop_video_no_audio(sample_video):
    """
    Test that process_audio_loop_video raises a ValueError with the correct message
    when provided with a video that has no audio track.
    """
    with pytest.raises(ValueError, match="Video has no audio"):
        process_audio_loop_video(sample_video, n=2)

def test_process_extract_audio_no_audio(sample_video):
    """Test that extracting audio from a silent video raises ValueError."""
    with pytest.raises(ValueError, match="Video has no audio"):
        process_extract_audio(sample_video)

def test_process_extract_audio_success(sample_video_with_audio):
    """Test that extracting audio works for video with audio."""
    output = process_extract_audio(sample_video_with_audio)
    try:
        assert os.path.exists(output)
        assert os.path.getsize(output) > 0
    finally:
        if os.path.exists(output):
            os.remove(output)

def test_process_resize_video_invalid_args(sample_video):
    """Test that process_resize_video raises ValueError when no resize parameters are provided."""
    with pytest.raises(ValueError, match="Must provide scale, width, or height"):
        process_resize_video(sample_video)

def test_process_audio_loop_video_no_audio(sample_video):
    """
    Test that process_audio_loop_video raises a ValueError with the correct message
    when provided with a video that has no audio track.
    """
    with pytest.raises(ValueError, match="Video has no audio"):
        process_audio_loop_video(sample_video, n=2)

def test_process_extract_audio_no_audio_mock():
    """Test that extracting audio from a silent video raises ValueError (using mocks)."""
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

def test_process_extract_audio_no_audio_integration(sample_video):
    """Test that extracting audio from a silent video raises ValueError (using real video)."""
    with pytest.raises(ValueError, match="Video has no audio"):
        process_extract_audio(sample_video)

def test_process_extract_audio_success(sample_video_with_audio):
    """Test that extracting audio from a video with audio works correctly."""
    output = process_extract_audio(sample_video_with_audio)
    try:
        assert os.path.exists(output)
        assert output.endswith(".mp3")
        assert os.path.getsize(output) > 0
    finally:
        if os.path.exists(output):
            os.remove(output)

def test_process_extract_audio_no_audio(sample_video):
    """Test that extracting audio from a silent video raises ValueError."""
    # Using sample_video which has no audio track
    with pytest.raises(ValueError, match="Video has no audio"):
        process_extract_audio(sample_video)

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

def test_process_resize_video_invalid_args(sample_video):
    """Test that process_resize_video raises ValueError when no resize parameters are provided."""
    with pytest.raises(ValueError, match="Must provide scale, width, or height"):
        process_resize_video(sample_video)

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

def test_process_audio_loop_video_no_audio(sample_video):
    """
    Test that process_audio_loop_video raises a ValueError with the correct message
    when provided with a video that has no audio track.
    """
    with pytest.raises(ValueError, match="Video has no audio"):
        process_audio_loop_video(sample_video, n=2)

def test_process_color_effect_invalid_type(sample_video):
    """Test that process_color_effect raises ValueError for unknown effect types."""
    with pytest.raises(ValueError, match="Unknown effect type: invalid_effect"):
        process_color_effect(sample_video, "invalid_effect")

def test_process_mirror_video_error_handling(sample_video):
    """Test that process_mirror_video raises ValueError for invalid axis."""
    with pytest.raises(ValueError, match="Axis must be 'x' or 'y'"):
        process_mirror_video(sample_video, axis="z")

def test_process_mirror_video_success(sample_video):
    """Test that process_mirror_video works for valid axis."""
    output_x = process_mirror_video(sample_video, axis="x")
    assert os.path.exists(output_x)
    assert os.path.getsize(output_x) > 0
    if os.path.exists(output_x):
        os.remove(output_x)

    output_y = process_mirror_video(sample_video, axis="y")
    assert os.path.exists(output_y)
    assert os.path.getsize(output_y) > 0
    if os.path.exists(output_y):
        os.remove(output_y)
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
    """Test that process_fade_video raises ValueError for invalid fade types."""
    with pytest.raises(ValueError, match="Fade type must be 'in' or 'out'"):
        process_fade_video(sample_video, fade_type="invalid", duration=1.0)

def test_process_time_effect_video_success(sample_video):
    """Test successful time effects on video."""

    # Test reverse
    output_reverse = process_time_effect_video(sample_video, "reverse")
    assert os.path.exists(output_reverse)
    assert os.path.getsize(output_reverse) > 0
    os.remove(output_reverse)

    # Test symmetrize
    output_symmetrize = process_time_effect_video(sample_video, "symmetrize")
    assert os.path.exists(output_symmetrize)
    assert os.path.getsize(output_symmetrize) > 0
    os.remove(output_symmetrize)

    # Test freeze
    output_freeze = process_time_effect_video(sample_video, "freeze", duration=1.0)
    assert os.path.exists(output_freeze)
    assert os.path.getsize(output_freeze) > 0
    os.remove(output_freeze)

def test_process_fade_video_invalid_type(sample_video):
    """Test that process_fade_video raises ValueError for invalid fade type."""
    with pytest.raises(ValueError, match="Fade type must be 'in' or 'out'"):
        process_fade_video(sample_video, fade_type="invalid", duration=1.0)

def test_process_audio_fade_video_invalid_type(sample_video_with_audio):
    """
    Test that process_audio_fade_video raises a ValueError for invalid fade types.
    """
    with pytest.raises(ValueError, match="Fade type must be 'in' or 'out'"):
        process_audio_fade_video(sample_video_with_audio, fade_type="invalid", duration=1.0)

def test_process_audio_fade_video_success(sample_video_with_audio):
    """
    Test that process_audio_fade_video works correctly for valid inputs.
    """
    output_in = process_audio_fade_video(sample_video_with_audio, fade_type="in", duration=0.5)
def test_get_unique_output_path_edge_cases():
    suffix = "test"
    with patch('uuid.uuid4') as mock_uuid:
        mock_uuid.return_value.hex = "1234567890abcdef"
        uuid_part = "12345678"

        # 1. Filename without extension
        path = "/path/to/file"
        expected = f"/path/to/file_{suffix}_{uuid_part}"
        assert get_unique_output_path(path, suffix) == expected

        # 2. Filename with multiple dots
        path = "/path/to/archive.tar.gz"
        # os.path.splitext splits at the LAST dot
        # 'archive.tar', '.gz'
        expected = f"/path/to/archive.tar_{suffix}_{uuid_part}.gz"
        assert get_unique_output_path(path, suffix) == expected

        # 3. Path with spaces
        path = "/path/to/my video.mp4"
        expected = f"/path/to/my video_{suffix}_{uuid_part}.mp4"
        assert get_unique_output_path(path, suffix) == expected

        # 4. Suffix with special characters
        suffix_special = "v1.0-beta"
        path = "/video.mp4"
        expected = f"/video_{suffix_special}_{uuid_part}.mp4"
        assert get_unique_output_path(path, suffix_special) == expected

        # 5. ext parameter without leading dot
        path = "/video.mp4"
        ext = "mkv" # intended to be .mkv usually
        # function does: f"{name}_{suffix}_{uuid.hex[:8]}{ext}"
        # so it appends "mkv" directly.
        expected = f"/video_{suffix}_{uuid_part}mkv"
        assert get_unique_output_path(path, suffix, ext=ext) == expected
def test_process_fade_video_success(sample_video):
    """Test that process_fade_video works for valid fade types."""
    # Test fade in
    output_in = process_fade_video(sample_video, fade_type="in", duration=0.5)
    assert os.path.exists(output_in)
    assert os.path.getsize(output_in) > 0
    os.remove(output_in)

    output_out = process_audio_fade_video(sample_video_with_audio, fade_type="out", duration=0.5)
    # Test fade out
    output_out = process_fade_video(sample_video, fade_type="out", duration=0.5)
    assert os.path.exists(output_out)
    assert os.path.getsize(output_out) > 0
    os.remove(output_out)
