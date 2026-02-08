import os
import pytest
import tempfile
from unittest.mock import MagicMock, patch
from moviepy import VideoFileClip
from video_gen_service.video_utils import (
    generate_simple_video,
    process_extract_audio,
    process_resize_video,
    process_audio_fade_video,
    process_audio_loop_video,
    process_concatenate_videos,
    process_color_effect,
    get_unique_output_path,
    process_mirror_video,
    process_time_effect_video,
    process_fade_video
)

def test_process_concatenate_videos_empty_list():
    """
    Test that process_concatenate_videos raises a ValueError with the correct message
    when provided with an empty list of video paths.
    """
    with pytest.raises(ValueError, match="No video paths provided"):
        process_concatenate_videos([])

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
    try:
        assert os.path.exists(output)
        assert os.path.getsize(output) > 0

        # Verify the output has audio
        with VideoFileClip(output) as video:
             assert video.audio is not None
    finally:
        if os.path.exists(output):
            os.remove(output)

def test_generate_simple_video():
    output = os.path.join(tempfile.gettempdir(), "test_output.mp4")
    try:
        # Use a short duration for speed
        result = generate_simple_video("Test Video", duration=0.5, output_file=output)
        # generate_simple_video returns absolute path
        assert result == os.path.abspath(output)
        assert os.path.exists(result)
        assert os.path.getsize(result) > 0
    finally:
        if os.path.exists(output):
            os.remove(output)
        abs_output = os.path.abspath(output)
        if os.path.exists(abs_output) and abs_output != output:
            os.remove(abs_output)

def test_process_extract_audio_no_audio(sample_video):
    """Test that extracting audio from a silent video raises ValueError."""
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

def test_process_resize_video_invalid_args(sample_video):
    """Test that process_resize_video raises ValueError when no resize parameters are provided."""
    with pytest.raises(ValueError, match="Must provide scale, width, or height"):
        process_resize_video(sample_video)

def test_process_extract_audio_no_audio_mock():
    """Test that extracting audio from a silent video raises ValueError (using mocks)."""
    with patch("video_gen_service.video_utils.os.path.exists", return_value=True):
        with patch("video_gen_service.video_utils.VideoFileClip") as MockVideoFileClip:
            mock_clip = MagicMock()
            mock_clip.audio = None
            MockVideoFileClip.return_value.__enter__.return_value = mock_clip

            with pytest.raises(ValueError, match="Video has no audio"):
                process_extract_audio(os.path.join(tempfile.gettempdir(), "dummy_video.mp4"))

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
    assert os.path.exists(output_in)
    assert os.path.getsize(output_in) > 0
    os.remove(output_in)

    output_out = process_audio_fade_video(sample_video_with_audio, fade_type="out", duration=0.5)
    assert os.path.exists(output_out)
    assert os.path.getsize(output_out) > 0
    os.remove(output_out)

def test_process_fade_video_success(sample_video):
    """Test that process_fade_video works for valid fade types."""
    output_in = process_fade_video(sample_video, fade_type="in", duration=0.5)
    assert os.path.exists(output_in)
    assert os.path.getsize(output_in) > 0
    os.remove(output_in)

    output_out = process_fade_video(sample_video, fade_type="out", duration=0.5)
    assert os.path.exists(output_out)
    assert os.path.getsize(output_out) > 0
    os.remove(output_out)

def test_get_unique_output_path():
    original_path = "/path/to/video.mp4"
    suffix = "test"
    output = get_unique_output_path(original_path, suffix)

    assert "/video_test_" in output
    assert output.endswith(".mp4")

    output_custom = get_unique_output_path(original_path, suffix, ext=".mov")
    assert output_custom.endswith(".mov")

    no_ext_path = "/path/to/video"
    output_no_ext = get_unique_output_path(no_ext_path, suffix)
    assert "/video_test_" in output_no_ext

    output1 = get_unique_output_path(original_path, suffix)
    output2 = get_unique_output_path(original_path, suffix)
    assert output1 != output2

    filename = "video.mp4"
    output_local = get_unique_output_path(filename, suffix)
    assert "video_test_" in output_local
    assert output_local.endswith(".mp4")

    with patch('uuid.uuid4') as mock_uuid:
        mock_uuid.return_value.hex = "1234567890abcdef"
        output_mocked = get_unique_output_path(original_path, suffix)
        expected = "/path/to/video_test_12345678.mp4"
        assert output_mocked == expected

def test_get_unique_output_path_edge_cases():
    suffix = "test"
    with patch('uuid.uuid4') as mock_uuid:
        mock_uuid.return_value.hex = "1234567890abcdef"
        uuid_part = "12345678"

        path = "/path/to/file"
        expected = f"/path/to/file_{suffix}_{uuid_part}"
        assert get_unique_output_path(path, suffix) == expected

        path = "/path/to/archive.tar.gz"
        expected = f"/path/to/archive.tar_{suffix}_{uuid_part}.gz"
        assert get_unique_output_path(path, suffix) == expected

        path = "/path/to/my video.mp4"
        expected = f"/path/to/my video_{suffix}_{uuid_part}.mp4"
        assert get_unique_output_path(path, suffix) == expected

        path = "/video.mp4"
        ext = "mkv"
        expected = f"/video_{suffix}_{uuid_part}mkv"
        assert get_unique_output_path(path, suffix, ext=ext) == expected

def test_process_mirror_video_error_handling(sample_video):
    with pytest.raises(ValueError, match="Axis must be 'x' or 'y'"):
        process_mirror_video(sample_video, axis="z")

def test_process_mirror_video_success(sample_video):
    output_x = process_mirror_video(sample_video, axis="x")
    try:
        assert os.path.exists(output_x)
        assert os.path.getsize(output_x) > 0
    finally:
        if os.path.exists(output_x):
            os.remove(output_x)

    output_y = process_mirror_video(sample_video, axis="y")
    try:
        assert os.path.exists(output_y)
        assert os.path.getsize(output_y) > 0
    finally:
        if os.path.exists(output_y):
            os.remove(output_y)

def test_process_time_effect_video_error_handling(sample_video):
    with pytest.raises(ValueError, match="Unknown time effect: invalid_effect"):
        process_time_effect_video(sample_video, "invalid_effect")

    with pytest.raises(ValueError, match="Duration required for freeze effect"):
        process_time_effect_video(sample_video, "freeze", duration=None)

def test_process_time_effect_video_success(sample_video):
    output_reverse = process_time_effect_video(sample_video, "reverse")
    try:
        assert os.path.exists(output_reverse)
        assert os.path.getsize(output_reverse) > 0
    finally:
        if os.path.exists(output_reverse):
            os.remove(output_reverse)

    output_symmetrize = process_time_effect_video(sample_video, "symmetrize")
    try:
        assert os.path.exists(output_symmetrize)
        assert os.path.getsize(output_symmetrize) > 0
    finally:
        if os.path.exists(output_symmetrize):
            os.remove(output_symmetrize)

    output_freeze = process_time_effect_video(sample_video, "freeze", duration=1.0)
    try:
        assert os.path.exists(output_freeze)
        assert os.path.getsize(output_freeze) > 0
    finally:
        if os.path.exists(output_freeze):
            os.remove(output_freeze)
