from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..video_utils import generate_simple_video
import os
import uuid

router = APIRouter(prefix="/video", tags=["video"])

class VideoRequest(BaseModel):
    text: str
    duration: float = 3.0

class VideoResponse(BaseModel):
    status: str
    file_path: str

@router.post("/generate", response_model=VideoResponse)
async def generate_video_endpoint(request: VideoRequest):
    try:
        # Create a unique filename
        filename = f"video_{uuid.uuid4()}.mp4"
        # In a real app, manage temp files or upload to storage
        result = generate_simple_video(request.text, request.duration, filename)
        return VideoResponse(status="success", file_path=os.path.abspath(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
