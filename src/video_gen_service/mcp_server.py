from fastmcp import FastMCP
from video_gen_service.video_utils import (
    generate_simple_video, process_cut_video, process_concatenate_videos,
    process_resize_video, process_speed_video, process_volume_video,
    process_extract_audio, process_composite_videos, process_text_overlay,
    process_color_effect, process_image_overlay,
    process_mirror_video, process_rotate_video, process_crop_video,
    process_margin_video, process_fade_video, process_loop_video,
    process_time_effect_video, process_audio_fade_video, process_audio_loop_video,
    detect_highlights
)
import os
from typing import List

# Create the MCP server
mcp = FastMCP("Video Gen Service")

@mcp.tool()
def detect_highlights(video_path: str, Threshold: float = 5.0) ->  str:
    """
    Analyzes moments within a video file where Hightened motion activity occurs.
    Which is the Industry Standard for detecting High Virality Potential Moments
    within video files. This tool only creates an output of a listing of start &
    end timestamps. Therefore you must use the output  as the input data for another
    tool such as the cut_video tool.
    """
    try:
        clips = dict[0:10]
        output = clips
        result = process_detect_highlights(video_path, Threshold)
        return f"{output}"
    except Exception as e:
        return f"Error generating viral moments list: {str(e)}"

@mcp.tool()
def create_video(text: str, duration: float = 3.0) -> str:
    """
    Generates a simple video with the given text on a background.
    Returns the path to the generated video file.
    """
    try:
        safe_text = "".join(c for c in text if c.isalnum() or c in (' ', '_', '-')).strip()
        safe_text = safe_text.replace(' ', '_')[:50]
        output_file = f"video_{safe_text}.mp4"

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

@mcp.tool()
def mirror_video(video_path: str, axis: str = "x", output_path: str = None) -> str:
    """Mirror video along axis 'x' or 'y'."""
    try:
        result = process_mirror_video(video_path, axis, output_path)
        return f"Video mirrored successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error mirroring video: {str(e)}"

@mcp.tool()
def rotate_video(video_path: str, angle: float, output_path: str = None) -> str:
    """Rotate video by angle."""
    try:
        result = process_rotate_video(video_path, angle, output_path)
        return f"Video rotated successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error rotating video: {str(e)}"

@mcp.tool()
def crop_video(video_path: str, x1: int = None, y1: int = None, x2: int = None, y2: int = None, width: int = None, height: int = None, output_path: str = None) -> str:
    """Crop video."""
    try:
        result = process_crop_video(video_path, x1, y1, x2, y2, width, height, output_path)
        return f"Video cropped successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error cropping video: {str(e)}"

@mcp.tool()
def margin_video(video_path: str, margin: int, color: tuple[int, int, int] = (0, 0, 0), opacity: float = 1.0, output_path: str = None) -> str:
    """Add margin to video."""
    try:
        result = process_margin_video(video_path, margin, color, opacity, output_path)
        return f"Margin added successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error adding margin: {str(e)}"

@mcp.tool()
def fade_video(video_path: str, fade_type: str, duration: float, output_path: str = None) -> str:
    """Fade video 'in' or 'out'."""
    try:
        result = process_fade_video(video_path, fade_type, duration, output_path)
        return f"Video faded successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error fading video: {str(e)}"

@mcp.tool()
def loop_video(video_path: str, n: int = None, duration: float = None, output_path: str = None) -> str:
    """Loop video."""
    try:
        result = process_loop_video(video_path, n, duration, output_path)
        return f"Video looped successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error looping video: {str(e)}"

@mcp.tool()
def time_effect_video(video_path: str, effect_type: str, duration: float = None, output_path: str = None) -> str:
    """Apply time effect: 'reverse', 'symmetrize', 'freeze'."""
    try:
        result = process_time_effect_video(video_path, effect_type, duration, output_path)
        return f"Time effect applied successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error applying time effect: {str(e)}"

@mcp.tool()
def audio_fade(video_path: str, fade_type: str, duration: float, output_path: str = None) -> str:
    """Fade audio 'in' or 'out'."""
    try:
        result = process_audio_fade_video(video_path, fade_type, duration, output_path)
        return f"Audio faded successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error fading audio: {str(e)}"

@mcp.tool()
def audio_loop(video_path: str, n: int = None, duration: float = None, output_path: str = None) -> str:
    """Loop audio."""
    try:
        result = process_audio_loop_video(video_path, n, duration, output_path)
        return f"Audio looped successfully: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error looping audio: {str(e)}"

if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        mcp.run(transport="sse", host=host, port=port)
    elif transport == "http":
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run()
