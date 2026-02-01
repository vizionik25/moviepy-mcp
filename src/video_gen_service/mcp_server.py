from fastmcp import FastMCP
from .video_utils import generate_simple_video
import os

# Create the MCP server
mcp = FastMCP("Video Gen Service")

@mcp.tool()
def create_video(text: str, duration: float = 3.0) -> str:
    """
    Generates a simple video with the given text on a background.
    Returns the path to the generated video file.
    """
    # Sanitize filename
    safe_text = "".join(c for c in text if c.isalnum() or c in (' ', '_', '-')).strip()
    safe_text = safe_text.replace(' ', '_')[:50]

    # Use a temp directory or specific output directory
    output_file = f"video_{safe_text}.mp4"

    try:
        result = generate_simple_video(text, duration, output_file)
        return f"Video generated successfully at: {os.path.abspath(result)}"
    except Exception as e:
        return f"Error generating video: {str(e)}"

if __name__ == "__main__":
    mcp.run()
