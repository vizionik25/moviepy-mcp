from fastapi import APIRouter, HTTPException
from ..schemas import CompositeRequest, TextOverlayRequest, ImageOverlayRequest, ResponseModel
from ..video_utils import process_composite_videos, process_text_overlay, process_image_overlay
import os
import asyncio

router = APIRouter(prefix="/compositing", tags=["compositing"])

@router.post("/composite", response_model=ResponseModel)
async def composite_videos(request: CompositeRequest):
    try:
        output_path = process_composite_videos(
            request.video_paths, request.method, request.size, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text-overlay", response_model=ResponseModel)
async def text_overlay(request: TextOverlayRequest):
    try:
        output_path = process_text_overlay(
            request.video_path, request.text, request.fontsize, request.color,
            request.position, request.duration, request.start_time, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image-overlay", response_model=ResponseModel)
async def image_overlay(request: ImageOverlayRequest):
    try:
        output_path = await asyncio.to_thread(
            process_image_overlay,
            request.video_path, request.image_path, request.position, request.scale,
            request.opacity, request.duration, request.start_time, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
