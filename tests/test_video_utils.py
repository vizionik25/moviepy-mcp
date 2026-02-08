import os
import pytest
from unittest.mock import patch
from video_gen_service.video_utils import generate_simple_video, get_unique_output_path

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
