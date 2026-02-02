from fastmcp import FastMCP
from video_utils import (
    generate_simple_video, process_cut_video, process_concatenate_videos,
    process_resize_video, process_speed_video, process_volume_video,
    process_extract_audio, process_composite_videos, process_text_overlay,
    process_color_effect, process_image_overlay
)
import os
from typing import List

# Create the MCP server
mcp = FastMCP("Video Gen Service")

@mcp.tool()
def create_video(text: str, duration: float = 3.0) -> str:
    """
    Generates a simple video with the given text on a background.
    Returns the path to the generated video file.
    """
    safe_text = "".join(c for c in text if c.isalnum() or c in (' ', '_', '-')).strip()
    safe_text = safe_text.replace(' ', '_')[:50]
    output_file = f"video_{safe_text}.mp4"

    try:
        result = generate_simple_video(text, duration, output_file)
        return f"Video generated successfully at: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error generating video: {str(e)}"

@mcp.tool()
def cut_video(video_path: str, start_time: float, end_time: float, output_path: str = None) -> str:
    """Cut a video clip from start_time to end_time."""
    try:
        result = process_cut_video(video_path, start_time, end_time, output_path)
        return f"Video cut successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error cutting video: {str(e)}"

@mcp.tool()
def concatenate_videos(video_paths: List[str], output_path: str = None, method: str = "compose") -> str:
    """Concatenate multiple video files. method can be 'compose' or 'chain'."""
    try:
        result = process_concatenate_videos(video_paths, method, output_path)
        return f"Videos concatenated successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error concatenating videos: {str(e)}"

@mcp.tool()
def resize_video(video_path: str, width: int = None, height: int = None, scale: float = None, output_path: str = None) -> str:
    """Resize video by width, height or scale factor."""
    try:
        result = process_resize_video(video_path, width, height, scale, output_path)
        return f"Video resized successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error resizing video: {str(e)}"

@mcp.tool()
def speed_video(video_path: str, factor: float, output_path: str = None) -> str:
    """Change video speed by a factor (e.g. 2.0 for 2x)."""
    try:
        result = process_speed_video(video_path, factor, output_path)
        return f"Video speed changed successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error changing video speed: {str(e)}"

@mcp.tool()
def adjust_volume(video_path: str, factor: float, output_path: str = None) -> str:
    """Adjust video volume by a factor."""
    try:
        result = process_volume_video(video_path, factor, output_path)
        return f"Volume adjusted successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error adjusting volume: {str(e)}"

@mcp.tool()
def extract_audio(video_path: str, output_path: str = None) -> str:
    """Extract audio from video."""
    try:
        result = process_extract_audio(video_path, output_path)
        return f"Audio extracted successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error extracting audio: {str(e)}"

@mcp.tool()
def composite_videos(video_paths: List[str], method: str = "stack", size: tuple[int, int] = None, output_path: str = None) -> str:
    """Composite videos using 'stack' or 'grid' method."""
    try:
        result = process_composite_videos(video_paths, method, size, output_path)
        return f"Videos composited successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error compositing videos: {str(e)}"

@mcp.tool()
def text_overlay(video_path: str, text: str, fontsize: int = 50, color: str = "white", position: str = "center", duration: float = None, start_time: float = 0.0, output_path: str = None) -> str:
    """Overlay text on video."""
    try:
        result = process_text_overlay(
            video_path, text, fontsize, color, position, duration, start_time, output_path
        )
        return f"Text overlay added successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error adding text overlay: {str(e)}"

@mcp.tool()
def image_overlay(video_path: str, image_path: str, position: str = "center", scale: float = None, opacity: float = 1.0, duration: float = None, start_time: float = 0.0, output_path: str = None) -> str:
    """Overlay image on video."""
    try:
        result = process_image_overlay(
            video_path, image_path, position, scale, opacity, duration, start_time, output_path
        )
        return f"Image overlay added successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error adding image overlay: {str(e)}"

@mcp.tool()
def color_effect(video_path: str, effect_type: str, factor: float = 1.0, output_path: str = None) -> str:
    """Apply color effect to video. effect_type: 'blackwhite', 'brightness', 'invert', 'contrast'."""
    try:
        result = process_color_effect(video_path, effect_type, factor, output_path)
        return f"Color effect applied successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error applying color effect: {str(e)}"

if __name__ == "__main__":
    mcp.run()
