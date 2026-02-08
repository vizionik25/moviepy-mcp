from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Union

class FilePath(BaseModel):
    path: str = Field(..., description="Path to the media file")

class TimeRange(BaseModel):
    start: float = Field(0.0, description="Start time in seconds")
    end: Optional[float] = Field(None, description="End time in seconds")

class ClipRequest(BaseModel):
    video_path: str = Field(..., description="Path to the input video file")
    output_path: Optional[str] = Field(None, description="Path to save the output video")

class CutRequest(ClipRequest):
    start_time: float = Field(..., description="Start time in seconds")
    end_time: float = Field(..., description="End time in seconds")

class ConcatenateRequest(BaseModel):
    video_paths: List[str] = Field(..., description="List of video paths to concatenate")
    output_path: Optional[str] = Field(None, description="Path to save the output video")
    method: str = Field("compose", description="Method to use: 'compose' or 'chain'")

class ResizeRequest(ClipRequest):
    width: Optional[int] = Field(None, description="New width")
    height: Optional[int] = Field(None, description="New height")
    scale: Optional[float] = Field(None, description="Scaling factor (e.g., 0.5 for half size)")

class SpeedRequest(ClipRequest):
    factor: float = Field(..., description="Speed factor (e.g., 2.0 for 2x speed)")

class VolumeRequest(ClipRequest):
    factor: float = Field(..., description="Volume factor (e.g., 0.5 for half volume)")

class AudioExtractRequest(ClipRequest):
    output_audio_path: Optional[str] = Field(None, description="Path to save the extracted audio")

class TextOverlayRequest(ClipRequest):
    text: str = Field(..., description="Text to overlay")
    fontsize: int = Field(50, description="Font size")
    color: str = Field("white", description="Text color")
    position: Union[str, Tuple[int, int]] = Field("center", description="Position: 'center', 'top', 'bottom' or (x, y)")
    duration: Optional[float] = Field(None, description="Duration of the text overlay")
    start_time: float = Field(0.0, description="Start time for the overlay")

class ImageOverlayRequest(ClipRequest):
    image_path: str = Field(..., description="Path to the image to overlay")
    position: Union[str, Tuple[int, int]] = Field("center", description="Position: 'center', 'top', 'bottom' or (x, y)")
    scale: Optional[float] = Field(None, description="Scale of the image")
    opacity: float = Field(1.0, description="Opacity (0.0 to 1.0)")
    duration: Optional[float] = Field(None, description="Duration of the image overlay")
    start_time: float = Field(0.0, description="Start time for the overlay")

class ColorEffectRequest(ClipRequest):
    effect_type: str = Field(..., description="Effect type: 'blackwhite', 'brightness', 'invert', 'contrast'")
    factor: float = Field(1.0, description="Factor for the effect (e.g. brightness multiplier)")

class CompositeRequest(BaseModel):
    video_paths: List[str] = Field(..., description="List of video paths to composite")
    output_path: Optional[str] = Field(None, description="Path to save the output video")
    size: Optional[Tuple[int, int]] = Field(None, description="Size of the final composition")
    method: str = Field("stack", description="Composition method: 'stack' or 'grid'") # simplified

class MirrorRequest(ClipRequest):
    axis: str = Field("x", description="Axis to mirror: 'x' or 'y'")

class RotateRequest(ClipRequest):
    angle: float = Field(..., description="Angle to rotate in degrees")

class CropRequest(ClipRequest):
    x1: Optional[int] = Field(None, description="Top left x coordinate")
    y1: Optional[int] = Field(None, description="Top left y coordinate")
    x2: Optional[int] = Field(None, description="Bottom right x coordinate")
    y2: Optional[int] = Field(None, description="Bottom right y coordinate")
    width: Optional[int] = Field(None, description="Width of the crop")
    height: Optional[int] = Field(None, description="Height of the crop")

class MarginRequest(ClipRequest):
    margin: int = Field(..., description="Margin size")
    color: Tuple[int, int, int] = Field((0, 0, 0), description="Color of the margin (R, G, B)")
    opacity: float = Field(1.0, description="Opacity of the margin")

class FadeRequest(ClipRequest):
    fade_type: str = Field(..., description="Fade type: 'in' or 'out'")
    duration: float = Field(..., description="Duration of the fade in seconds")

class LoopRequest(ClipRequest):
    n: Optional[int] = Field(None, description="Number of times to loop")
    duration: Optional[float] = Field(None, description="Duration to loop for")

class TimeEffectRequest(ClipRequest):
    effect_type: str = Field(..., description="Time effect type: 'reverse', 'symmetrize', 'freeze'")
    duration: Optional[float] = Field(None, description="Duration for 'freeze'")

class AudioFadeRequest(FadeRequest):
    pass

class AudioLoopRequest(LoopRequest):
    pass

class ResponseModel(BaseModel):
    status: str
    output_path: str
    details: Optional[str] = None
