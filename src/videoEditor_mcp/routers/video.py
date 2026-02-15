from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..video_utils import generate_simple_video, SAFE_DIR, process_save_frame, process_write_gif
from ..schemas import SaveFrameRequest, WriteGifRequest, ResponseModel, VideoRequest, VideoResponse
import os
import uuid
import asyncio

router = APIRouter(prefix="/video", tags=["video"])

@router.post("/save-frame", response_model=ResponseModel)
async def save_frame(request: SaveFrameRequest):
    try:
        output_path = await asyncio.to_thread(
            process_save_frame, request.video_path, request.t, request.output_image_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/write-gif", response_model=ResponseModel)
async def write_gif(request: WriteGifRequest):
    try:
        output_path = await asyncio.to_thread(
            process_write_gif, request.video_path, request.fps, request.program, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate", response_model=VideoResponse)
async def generate_video_endpoint(request: VideoRequest):
    try:
        # Create a unique filename in SAFE_DIR
        filename = str(SAFE_DIR / f"video_{uuid.uuid4()}.mp4")
        # In a real app, manage temp files or upload to storage
        result = generate_simple_video(request.text, request.duration, filename)
        return VideoResponse(status="success", file_path=os.path.abspath(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
