from fastmcp import FastMCP
from video_gen_service.mcp_server import (
    create_video, cut_video, concatenate_videos, resize_video, speed_video,
    adjust_volume, extract_audio, composite_videos, text_overlay, image_overlay,
    color_effect, mirror_video, rotate_video, crop_video, margin_video,
    fade_video, loop_video, time_effect_video, audio_fade, audio_loop
)
import os

def test_mcp_tools(sample_video, sample_video_with_audio, sample_video_2):
    # Test create_video
    res = create_video.fn("MCP Video Test", 1.0)
    assert "Video generated successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test cut
    res = cut_video.fn(sample_video, 0, 1)
    assert "Video cut successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test concatenate
    res = concatenate_videos.fn([sample_video, sample_video_2])
    assert "Videos concatenated successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test resize
    res = resize_video.fn(sample_video, scale=0.5)
    assert "Video resized successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test speed
    res = speed_video.fn(sample_video, factor=2.0)
    assert "Video speed changed successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test volume
    res = adjust_volume.fn(sample_video_with_audio, factor=0.5)
    assert "Volume adjusted successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test extract audio
    res = extract_audio.fn(sample_video_with_audio)
    assert "Audio extracted successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test composite
    res = composite_videos.fn([sample_video, sample_video_2], method="stack")
    assert "Videos composited successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test text overlay
    res = text_overlay.fn(sample_video, "Overlay")
    assert "Text overlay added successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test color effect
    res = color_effect.fn(sample_video, "blackwhite")
    assert "Color effect applied successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test mirror
    res = mirror_video.fn(sample_video, "x")
    assert "Video mirrored successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test rotate
    res = rotate_video.fn(sample_video, 90)
    assert "Video rotated successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test crop
    res = crop_video.fn(sample_video, width=100, height=100)
    assert "Video cropped successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test margin
    res = margin_video.fn(sample_video, 10)
    assert "Margin added successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test fade
    res = fade_video.fn(sample_video, "in", 1.0)
    assert "Video faded successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test loop video
    res = loop_video.fn(sample_video, n=2)
    assert "Video looped successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test time effect
    res = time_effect_video.fn(sample_video, "reverse")
    assert "Time effect applied successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test audio fade
    res = audio_fade.fn(sample_video_with_audio, "in", 1.0)
    assert "Audio faded successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test audio loop
    res = audio_loop.fn(sample_video_with_audio, n=2)
    assert "Audio looped successfully" in res
    path = res.split(": ")[1]
    assert os.path.exists(path)
    os.remove(path)

    # Test error handling
    res = mirror_video.fn("non_existent.mp4")
    assert "Error mirroring video" in res

    res = create_video.fn(None) # Force error
    assert "Error generating video" in res

    res = cut_video.fn("non_existent.mp4", 0, 1)
    assert "Error cutting video" in res

    res = concatenate_videos.fn(["non_existent.mp4"])
    assert "Error concatenating videos" in res

    res = resize_video.fn("non_existent.mp4")
    assert "Error resizing video" in res

    res = speed_video.fn("non_existent.mp4", 2.0)
    assert "Error changing video speed" in res

    res = adjust_volume.fn("non_existent.mp4", 0.5)
    assert "Error adjusting volume" in res

    res = extract_audio.fn("non_existent.mp4")
    assert "Error extracting audio" in res

    res = composite_videos.fn(["non_existent.mp4"])
    assert "Error compositing videos" in res

    res = text_overlay.fn("non_existent.mp4", "text")
    assert "Error adding text overlay" in res

    res = image_overlay.fn("non_existent.mp4", "img")
    assert "Error adding image overlay" in res

    res = color_effect.fn("non_existent.mp4", "invert")
    assert "Error applying color effect" in res

    res = rotate_video.fn("non_existent.mp4", 90)
    assert "Error rotating video" in res

    res = crop_video.fn("non_existent.mp4")
    assert "Error cropping video" in res

    res = margin_video.fn("non_existent.mp4", 10)
    assert "Error adding margin" in res

    res = fade_video.fn("non_existent.mp4", "in", 1)
    assert "Error fading video" in res

    res = loop_video.fn("non_existent.mp4")
    assert "Error looping video" in res

    res = time_effect_video.fn("non_existent.mp4", "reverse")
    assert "Error applying time effect" in res

    res = audio_fade.fn("non_existent.mp4", "in", 1)
    assert "Error fading audio" in res

    res = audio_loop.fn("non_existent.mp4")
    assert "Error looping audio" in res
