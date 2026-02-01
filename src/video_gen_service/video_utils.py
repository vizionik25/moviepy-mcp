import os
import tempfile
from pathlib import Path
from moviepy import ImageClip
from PIL import Image, ImageDraw, ImageFont

def create_text_image(text: str, size: tuple[int, int] = (640, 480), bg_color: str = 'black', text_color: str = 'white') -> str:
    """
    Creates an image with text using PIL and saves it temporarily.
    Returns the path to the temporary image file.
    """
    img = Image.new('RGB', size, color=bg_color)
    d = ImageDraw.Draw(img)

    # Try to load a font, fall back to default
    font = None
    # List of fonts to try (cross-platform attempts)
    fonts_to_try = ["DejaVuSans.ttf", "Arial.ttf", "arial.ttf", "Roboto-Regular.ttf", "FreeSans.ttf"]

    for font_name in fonts_to_try:
        try:
            font = ImageFont.truetype(font_name, 40)
            break
        except IOError:
            continue

    if font is None:
        # Fallback to default (very small)
        font = ImageFont.load_default()

    # Get text bounding box to center it
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2

    d.text((x, y), text, fill=text_color, font=font)

    # Create a temp file
    fd, temp_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)

    img.save(temp_path)
    return temp_path

def generate_simple_video(text: str, duration: float = 3.0, output_file: str = "output.mp4") -> str:
    """
    Generates a simple video with text on a background.
    """
    img_path = None
    try:
        # Create image with text
        img_path = create_text_image(text)

        # Create clip from image
        clip = ImageClip(img_path).with_duration(duration)

        # Write video file
        # codec='libx264' is standard for mp4
        clip.write_videofile(output_file, fps=24, codec='libx264')

        return output_file
    finally:
        # Cleanup
        if img_path and os.path.exists(img_path):
            os.remove(img_path)
