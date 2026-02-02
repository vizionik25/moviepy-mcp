import os
import tempfile
import uuid
from typing import List, Optional, Tuple, Union
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, clips_array, ImageClip, vfx, afx
from PIL import Image, ImageDraw, ImageFont

def get_unique_output_path(original_path: str, suffix: str, ext: str = None) -> str:
    directory, filename = os.path.split(original_path)
    name, original_ext = os.path.splitext(filename)
    if ext is None:
        ext = original_ext
    return os.path.join(directory, f"{name}_{suffix}_{uuid.uuid4().hex[:8]}{ext}")

def write_video(clip, output_path: str):
    audio_codec = "aac" if clip.audio else None
    clip.write_videofile(output_path, codec="libx264", audio_codec=audio_codec)

def create_text_image(text: str, size: tuple[int, int] = (640, 480), bg_color: str = 'black', text_color: str = 'white', transparent: bool = False, fontsize: int = 40) -> str:
    """
    Creates an image with text using PIL and saves it temporarily.
    Returns the path to the temporary image file.
    """
    mode = 'RGBA' if transparent else 'RGB'
    color = (0, 0, 0, 0) if transparent else bg_color

    img = Image.new(mode, size, color=color)
    d = ImageDraw.Draw(img)

    # Try to load a font, fall back to default
    font = None
    # List of fonts to try (cross-platform attempts)
    fonts_to_try = ["DejaVuSans.ttf", "Arial.ttf", "arial.ttf", "Roboto-Regular.ttf", "FreeSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]

    for font_name in fonts_to_try:
        try:
            font = ImageFont.truetype(font_name, fontsize)
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
        clip.write_videofile(output_file, fps=24, codec='libx264')

        return output_file
    finally:
        # Cleanup
        if img_path and os.path.exists(img_path):
            os.remove(img_path)

def process_cut_video(video_path: str, start_time: float, end_time: float, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "cut")

    with VideoFileClip(video_path) as video:
        new_clip = video.subclipped(start_time, end_time)
        write_video(new_clip, output_path)
    return output_path

def process_concatenate_videos(video_paths: List[str], method: str = "compose", output_path: str = None) -> str:
    clips = []
    try:
        for path in video_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Video file not found: {path}")
            clips.append(VideoFileClip(path))

        if not clips:
             raise ValueError("No video paths provided")

        if output_path is None:
            output_path = get_unique_output_path(video_paths[0], "concat")

        final_clip = concatenate_videoclips(clips, method=method)
        write_video(final_clip, output_path)
        return output_path
    finally:
        for clip in clips:
            clip.close()

def process_resize_video(video_path: str, width: int = None, height: int = None, scale: float = None, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "resized")

    with VideoFileClip(video_path) as video:
        if scale:
            new_clip = video.resized(scale)
        elif width and height:
            new_clip = video.resized(newsize=(width, height))
        elif width:
            new_clip = video.resized(width=width)
        elif height:
            new_clip = video.resized(height=height)
        else:
            raise ValueError("Must provide scale, width, or height")

        write_video(new_clip, output_path)
    return output_path

def process_speed_video(video_path: str, factor: float, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "speed")

    with VideoFileClip(video_path) as video:
        new_clip = video.with_speed_scaled(factor)
        write_video(new_clip, output_path)
    return output_path

def process_volume_video(video_path: str, factor: float, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "volume")

    with VideoFileClip(video_path) as video:
        if not video.audio:
            new_clip = video
        else:
            new_clip = video.with_volume_scaled(factor)
        write_video(new_clip, output_path)
    return output_path

def process_extract_audio(video_path: str, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "audio", ".mp3")

    with VideoFileClip(video_path) as video:
        audio = video.audio
        if not audio:
             raise ValueError("Video has no audio")
        audio.write_audiofile(output_path)
    return output_path

def process_composite_videos(video_paths: List[str], method: str = "stack", size: tuple[int, int] = None, output_path: str = None) -> str:
    clips = []
    try:
        for path in video_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Video file not found: {path}")
            clips.append(VideoFileClip(path))

        if not clips:
             raise ValueError("No video paths provided")

        if method == "stack":
            final_clip = CompositeVideoClip(clips, size=size)
        elif method == "grid":
            final_clip = clips_array([clips])
        else:
            raise ValueError("Invalid method. Use 'stack' or 'grid'")

        if output_path is None:
            output_path = get_unique_output_path(video_paths[0], "composite")

        write_video(final_clip, output_path)
        return output_path
    finally:
        for clip in clips:
            try:
                clip.close()
            except:
                pass

def process_text_overlay(video_path: str, text: str, fontsize: int = 50, color: str = "white", position: Union[str, Tuple[int, int]] = "center", duration: float = None, start_time: float = 0.0, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "text")

    img_path = None
    try:
        with VideoFileClip(video_path) as video:
            # Create transparent image with text
            img = Image.new('RGBA', video.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(img)

            font = None
            fonts_to_try = ["DejaVuSans.ttf", "Arial.ttf", "arial.ttf", "Roboto-Regular.ttf", "FreeSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
            for font_name in fonts_to_try:
                try:
                    font = ImageFont.truetype(font_name, fontsize)
                    break
                except IOError:
                    continue
            if font is None:
                font = ImageFont.load_default()

            bbox = d.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x, y = 0, 0
            if isinstance(position, str):
                if position == 'center':
                    x = (video.w - text_width) / 2
                    y = (video.h - text_height) / 2
                elif position == 'top':
                    x = (video.w - text_width) / 2
                    y = 10
                elif position == 'bottom':
                    x = (video.w - text_width) / 2
                    y = video.h - text_height - 10
            elif isinstance(position, (list, tuple)):
                x, y = position

            d.text((x, y), text, fill=color, font=font)

            fd, img_path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            img.save(img_path)

            txt_clip = ImageClip(img_path).with_duration(duration or video.duration).with_start(start_time)

            final_clip = CompositeVideoClip([video, txt_clip])
            write_video(final_clip, output_path)

        return output_path
    finally:
        if img_path and os.path.exists(img_path):
            os.remove(img_path)

def process_image_overlay(video_path: str, image_path: str, position: Union[str, Tuple[int, int]] = "center", scale: float = None, opacity: float = 1.0, duration: float = None, start_time: float = 0.0, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "img_overlay")

    with VideoFileClip(video_path) as video:
        img_clip = ImageClip(image_path)

        if scale:
            img_clip = img_clip.resized(scale)

        img_clip = img_clip.with_duration(duration or video.duration).with_start(start_time).with_position(position)

        if opacity < 1.0:
            img_clip = img_clip.with_opacity(opacity)

        final_clip = CompositeVideoClip([video, img_clip])
        write_video(final_clip, output_path)

    return output_path

def process_color_effect(video_path: str, effect_type: str, factor: float = 1.0, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, f"fx_{effect_type}")

    with VideoFileClip(video_path) as video:
        if effect_type == "blackwhite":
            new_clip = video.with_effects([vfx.BlackAndWhite()])
        elif effect_type == "brightness":
            new_clip = video.with_effects([vfx.MultiplyColor(factor)])
        elif effect_type == "invert":
            new_clip = video.with_effects([vfx.InvertColors()])
        elif effect_type == "contrast":
            new_clip = video.with_effects([vfx.LumContrast(contrast=factor)])
        else:
            raise ValueError(f"Unknown effect type: {effect_type}")

        write_video(new_clip, output_path)
    return output_path

def process_mirror_video(video_path: str, axis: str = "x", output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, f"mirror_{axis}")

    with VideoFileClip(video_path) as video:
        if axis == "x":
            new_clip = video.with_effects([vfx.MirrorX()])
        elif axis == "y":
            new_clip = video.with_effects([vfx.MirrorY()])
        else:
            raise ValueError("Axis must be 'x' or 'y'")

        write_video(new_clip, output_path)
    return output_path

def process_rotate_video(video_path: str, angle: float, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "rotate")

    with VideoFileClip(video_path) as video:
        new_clip = video.rotated(angle)
        write_video(new_clip, output_path)
    return output_path

def process_crop_video(video_path: str, x1: int = None, y1: int = None, x2: int = None, y2: int = None, width: int = None, height: int = None, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "crop")

    with VideoFileClip(video_path) as video:
        new_clip = video.cropped(x1=x1, y1=y1, x2=x2, y2=y2, width=width, height=height)
        write_video(new_clip, output_path)
    return output_path

def process_margin_video(video_path: str, margin: int, color: tuple[int, int, int] = (0, 0, 0), opacity: float = 1.0, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "margin")

    with VideoFileClip(video_path) as video:
        new_clip = video.with_effects([vfx.Margin(margin_size=margin, color=color, opacity=opacity)])
        write_video(new_clip, output_path)
    return output_path

def process_fade_video(video_path: str, fade_type: str, duration: float, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, f"fade_{fade_type}")

    with VideoFileClip(video_path) as video:
        if fade_type == "in":
            new_clip = video.with_effects([vfx.FadeIn(duration)])
        elif fade_type == "out":
            new_clip = video.with_effects([vfx.FadeOut(duration)])
        else:
            raise ValueError("Fade type must be 'in' or 'out'")
        write_video(new_clip, output_path)
    return output_path

def process_loop_video(video_path: str, n: int = None, duration: float = None, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "loop")

    with VideoFileClip(video_path) as video:
        new_clip = video.with_effects([vfx.Loop(n=n, duration=duration)])
        write_video(new_clip, output_path)
    return output_path

def process_time_effect_video(video_path: str, effect_type: str, duration: float = None, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, f"time_{effect_type}")

    with VideoFileClip(video_path) as video:
        if effect_type == "reverse":
            new_clip = video.with_effects([vfx.TimeMirror()])
        elif effect_type == "symmetrize":
            new_clip = video.with_effects([vfx.TimeSymmetrize()])
        elif effect_type == "freeze":
            if duration is None:
                raise ValueError("Duration required for freeze effect")
            # Freeze at the start
            new_clip = video.with_effects([vfx.Freeze(t=0, freeze_duration=duration)])
        else:
            raise ValueError(f"Unknown time effect: {effect_type}")
        write_video(new_clip, output_path)
    return output_path

def process_audio_fade_video(video_path: str, fade_type: str, duration: float, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, f"audio_fade_{fade_type}")

    with VideoFileClip(video_path) as video:
        if not video.audio:
             raise ValueError("Video has no audio")

        if fade_type == "in":
            new_audio = video.audio.with_effects([afx.AudioFadeIn(duration)])
        elif fade_type == "out":
            new_audio = video.audio.with_effects([afx.AudioFadeOut(duration)])
        else:
            raise ValueError("Fade type must be 'in' or 'out'")

        new_clip = video.with_audio(new_audio)
        write_video(new_clip, output_path)
    return output_path

def process_audio_loop_video(video_path: str, n: int = None, duration: float = None, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    if output_path is None:
        output_path = get_unique_output_path(video_path, "audio_loop")

    with VideoFileClip(video_path) as video:
        if not video.audio:
             raise ValueError("Video has no audio")

        new_audio = video.audio.with_effects([afx.AudioLoop(n_loops=n, duration=duration)])
        new_clip = video.with_audio(new_audio)
        write_video(new_clip, output_path)
    return output_path
