import pytest
import os
from video_gen_service.video_utils import generate_simple_video
import tempfile

@pytest.fixture(scope="session")
def sample_video():
    """Creates a sample video file for testing."""
    # Create a temp file
    fd, temp_path = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)

    # Generate content
    generate_simple_video("Test Video", duration=2.0, output_file=temp_path)

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)

@pytest.fixture(scope="session")
def sample_video_with_audio():
    """Creates a sample video file with audio for testing."""
    import numpy as np
    from moviepy import AudioArrayClip, ImageClip
    from video_gen_service.video_utils import create_text_image

    fd, temp_path = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)

    # Create visual
    img_path = create_text_image("Audio Video")
    clip = ImageClip(img_path).with_duration(2.0)

    # Create audio (stereo sine wave)
    duration = 2.0
    fps = 44100
    t = np.linspace(0, duration, int(fps * duration))
    # 440 Hz sine wave
    audio = np.sin(2 * np.pi * 440 * t)
    stereo_audio = np.stack([audio, audio], axis=1)

    audio_clip = AudioArrayClip(stereo_audio, fps=fps)
    final_clip = clip.with_audio(audio_clip)

    final_clip.write_videofile(temp_path, fps=24, codec='libx264', audio_codec='aac')

    yield temp_path

    if os.path.exists(temp_path):
        os.remove(temp_path)
    if os.path.exists(img_path):
        os.remove(img_path)

@pytest.fixture(scope="session")
def sample_video_2():
    """Creates a second sample video file for testing concatenation."""
    fd, temp_path = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)

    generate_simple_video("Video 2", duration=2.0, output_file=temp_path)

    yield temp_path

    if os.path.exists(temp_path):
        os.remove(temp_path)
