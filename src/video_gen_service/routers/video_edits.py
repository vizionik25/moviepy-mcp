from fastapi import APIRouter, HTTPException
from ..schemas import CutRequest, ConcatenateRequest, ResizeRequest, SpeedRequest, ColorEffectRequest, ResponseModel
from ..video_utils import (
    process_cut_video, process_concatenate_videos, process_resize_video,
    process_speed_video, process_color_effect
)
import os

router = APIRouter(prefix="/video-edits", tags=["video-edits"])

@router.post("/cut", response_model=ResponseModel)
async def cut_video(request: CutRequest):
    try:
        output_path = process_cut_video(
            request.video_path, request.start_time, request.end_time, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/concatenate", response_model=ResponseModel)
async def concatenate_videos(request: ConcatenateRequest):
    try:
        output_path = process_concatenate_videos(
            request.video_paths, request.method, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resize", response_model=ResponseModel)
async def resize_video(request: ResizeRequest):
    try:
        output_path = process_resize_video(
            request.video_path, request.width, request.height, request.scale, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/speed", response_model=ResponseModel)
async def speed_video(request: SpeedRequest):
    try:
        output_path = process_speed_video(
            request.video_path, request.factor, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/color-effect", response_model=ResponseModel)
async def color_effect_video(request: ColorEffectRequest):
    try:
        output_path = process_color_effect(
            request.video_path, request.effect_type, request.factor, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
