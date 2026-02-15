from fastmcp import FastMCP
from .video_utils import (
    generate_simple_video, process_cut_video, process_concatenate_videos,
    process_resize_video, process_speed_video, process_volume_video,
    process_extract_audio, process_composite_videos, process_text_overlay,
    process_image_overlay, process_color_effect, process_mirror_video,
    process_rotate_video, process_crop_video, process_margin_video,
    process_fade_video, process_loop_video, process_time_effect_video,
    process_audio_fade_video, process_audio_loop_video,
    process_accel_decel_video, process_blink_video, process_gamma_correction_video,
    process_painting_video, process_audio_delay_video, process_audio_normalize_video,
    process_detect_scenes, process_save_frame, process_write_gif,
    SAFE_DIR
)
from typing import List, Optional, Tuple, Union
import os

mcp = FastMCP("Video Editor")

@mcp.tool()
def generate_video(text: str, duration: float = 3.0) -> str:
    """Generates a simple video with text on a background."""
    import uuid
    filename = str(SAFE_DIR / f"video_{uuid.uuid4()}.mp4")
    return generate_simple_video(text, duration, filename)

@mcp.tool()
def cut_video(video_path: str, start_time: float, end_time: float, output_path: Optional[str] = None) -> str:
    """Cuts a video between start_time and end_time."""
    return process_cut_video(video_path, start_time, end_time, output_path)

@mcp.tool()
def concatenate_videos(video_paths: List[str], method: str = "compose", output_path: Optional[str] = None) -> str:
    """Concatenates multiple videos together."""
    return process_concatenate_videos(video_paths, method, output_path)

@mcp.tool()
def resize_video(video_path: str, width: Optional[int] = None, height: Optional[int] = None, scale: Optional[float] = None, output_path: Optional[str] = None) -> str:
    """Resizes a video by width, height, or scale."""
    return process_resize_video(video_path, width, height, scale, output_path)

@mcp.tool()
def speed_video(video_path: str, factor: float, output_path: Optional[str] = None) -> str:
    """Changes the speed of a video."""
    return process_speed_video(video_path, factor, output_path)

@mcp.tool()
def volume_video(video_path: str, factor: float, output_path: Optional[str] = None) -> str:
    """Changes the volume of a video."""
    return process_volume_video(video_path, factor, output_path)

@mcp.tool()
def extract_audio(video_path: str, output_path: Optional[str] = None) -> str:
    """Extracts audio from a video file."""
    return process_extract_audio(video_path, output_path)

@mcp.tool()
def composite_videos(video_paths: List[str], method: str = "stack", size: Optional[Tuple[int, int]] = None, output_path: Optional[str] = None) -> str:
    """Composites multiple videos together (stack or grid)."""
    return process_composite_videos(video_paths, method, size, output_path)

@mcp.tool()
def text_overlay(video_path: str, text: str, fontsize: int = 50, color: str = "white", position: str = "center", duration: Optional[float] = None, start_time: float = 0.0, output_path: Optional[str] = None) -> str:
    """Overlays text on a video."""
    # Simplified position for MCP tool
    return process_text_overlay(video_path, text, fontsize, color, position, duration, start_time, output_path)

@mcp.tool()
def image_overlay(video_path: str, image_path: str, position: str = "center", scale: Optional[float] = None, opacity: float = 1.0, duration: Optional[float] = None, start_time: float = 0.0, output_path: Optional[str] = None) -> str:
    """Overlays an image on a video."""
    return process_image_overlay(video_path, image_path, position, scale, opacity, duration, start_time, output_path)

@mcp.tool()
def color_effect(video_path: str, effect_type: str, factor: float = 1.0, output_path: Optional[str] = None) -> str:
    """Applies a color effect (blackwhite, brightness, invert, contrast)."""
    return process_color_effect(video_path, effect_type, factor, output_path)

@mcp.tool()
def mirror_video(video_path: str, axis: str = "x", output_path: Optional[str] = None) -> str:
    """Mirrors a video along the x or y axis."""
    return process_mirror_video(video_path, axis, output_path)

@mcp.tool()
def rotate_video(video_path: str, angle: float, output_path: Optional[str] = None) -> str:
    """Rotates a video by a given angle."""
    return process_rotate_video(video_path, angle, output_path)

@mcp.tool()
def crop_video(video_path: str, x1: Optional[int] = None, y1: Optional[int] = None, x2: Optional[int] = None, y2: Optional[int] = None, width: Optional[int] = None, height: Optional[int] = None, output_path: Optional[str] = None) -> str:
    """Crops a video."""
    return process_crop_video(video_path, x1, y1, x2, y2, width, height, output_path)

@mcp.tool()
def margin_video(video_path: str, margin: int, color: Tuple[int, int, int] = (0, 0, 0), opacity: float = 1.0, output_path: Optional[str] = None) -> str:
    """Adds a margin to a video."""
    return process_margin_video(video_path, margin, color, opacity, output_path)

@mcp.tool()
def fade_video(video_path: str, fade_type: str, duration: float, output_path: Optional[str] = None) -> str:
    """Adds a fade-in or fade-out effect to a video."""
    return process_fade_video(video_path, fade_type, duration, output_path)

@mcp.tool()
def loop_video(video_path: str, n: Optional[int] = None, duration: Optional[float] = None, output_path: Optional[str] = None) -> str:
    """Loops a video n times or for a specific duration."""
    return process_loop_video(video_path, n, duration, output_path)

@mcp.tool()
def time_effect(video_path: str, effect_type: str, duration: Optional[float] = None, output_path: Optional[str] = None) -> str:
    """Applies a time effect (reverse, symmetrize, freeze)."""
    return process_time_effect_video(video_path, effect_type, duration, output_path)

@mcp.tool()
def audio_fade(video_path: str, fade_type: str, duration: float, output_path: Optional[str] = None) -> str:
    """Adds a fade-in or fade-out effect to the audio of a video."""
    return process_audio_fade_video(video_path, fade_type, duration, output_path)

@mcp.tool()
def audio_loop(video_path: str, n: Optional[int] = None, duration: Optional[float] = None, output_path: Optional[str] = None) -> str:
    """Loops the audio of a video."""
    return process_audio_loop_video(video_path, n, duration, output_path)

@mcp.tool()
def accel_decel(video_path: str, new_duration: Optional[float] = None, abscissa_fixed: float = 0.5, output_path: Optional[str] = None) -> str:
    """Applies acceleration/deceleration effect."""
    return process_accel_decel_video(video_path, new_duration, abscissa_fixed, output_path)

@mcp.tool()
def blink(video_path: str, duration_on: float, duration_off: float, output_path: Optional[str] = None) -> str:
    """Makes the video blink."""
    return process_blink_video(video_path, duration_on, duration_off, output_path)

@mcp.tool()
def gamma_correction(video_path: str, gamma: float, output_path: Optional[str] = None) -> str:
    """Applies gamma correction."""
    return process_gamma_correction_video(video_path, gamma, output_path)

@mcp.tool()
def painting_effect(video_path: str, saturation: float = 1.4, black: float = 0.006, output_path: Optional[str] = None) -> str:
    """Applies a painting-like effect."""
    return process_painting_video(video_path, saturation, black, output_path)

@mcp.tool()
def audio_delay(video_path: str, offset: float, output_path: Optional[str] = None) -> str:
    """Adds a delay to the audio."""
    return process_audio_delay_video(video_path, offset, output_path)

@mcp.tool()
def audio_normalize(video_path: str, output_path: Optional[str] = None) -> str:
    """Normalizes the audio volume."""
    return process_audio_normalize_video(video_path, output_path)

@mcp.tool()
def detect_scenes(video_path: str, luminosity_threshold: float = 10.0) -> List[Tuple[float, float]]:
    """Detects scenes in a video based on luminosity changes."""
    return process_detect_scenes(video_path, luminosity_threshold)

@mcp.tool()
def save_frame(video_path: str, t: float, output_path: Optional[str] = None) -> str:
    """Saves a single frame from the video at time t."""
    return process_save_frame(video_path, t, output_path)

@mcp.tool()
def write_gif(video_path: str, fps: Optional[int] = None, program: str = "imageio", output_path: Optional[str] = None) -> str:
    """Converts a video to a GIF."""
    return process_write_gif(video_path, fps, program, output_path)

if __name__ == "__main__":
    mcp.run()
