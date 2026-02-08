from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from ..schemas import VolumeRequest, AudioExtractRequest, AudioFadeRequest, AudioLoopRequest, ResponseModel
from ..video_utils import process_volume_video, process_extract_audio, process_audio_fade_video, process_audio_loop_video
import os

router = APIRouter(prefix="/audio", tags=["audio"])

@router.post("/volume", response_model=ResponseModel)
async def adjust_volume(request: VolumeRequest):
    try:
        output_path = process_volume_video(
            request.video_path, request.factor, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract", response_model=ResponseModel)
async def extract_audio(request: AudioExtractRequest):
    try:
        output_path = process_extract_audio(
            request.video_path, request.output_audio_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fade", response_model=ResponseModel)
async def fade_audio(request: AudioFadeRequest):
    try:
        output_path = await run_in_threadpool(
            process_audio_fade_video,
            request.video_path,
            request.fade_type,
            request.duration,
            request.output_path,
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/loop", response_model=ResponseModel)
async def loop_audio(request: AudioLoopRequest):
    try:
        output_path = process_audio_loop_video(
            request.video_path, request.n, request.duration, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
