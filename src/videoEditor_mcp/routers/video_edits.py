from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from ..schemas import (
    CutRequest, ConcatenateRequest, ResizeRequest, SpeedRequest, ColorEffectRequest,
    MirrorRequest, RotateRequest, CropRequest, MarginRequest, FadeRequest, LoopRequest, TimeEffectRequest,
    DetectRequest, AccelDecelRequest, BlinkRequest, GammaCorrectionRequest, PaintingRequest,
    DetectScenesRequest, ResponseModel
)
from ..video_utils import (
    process_cut_video, process_concatenate_videos, process_resize_video,
    process_speed_video, process_color_effect,
    process_mirror_video, process_rotate_video, process_crop_video,
    process_margin_video, process_fade_video, process_loop_video, process_time_effect_video,
    process_detect_highlights, process_accel_decel_video, process_blink_video,
    process_gamma_correction_video, process_painting_video, process_detect_scenes
)
import os
import asyncio
from starlette.concurrency import run_in_threadpool

router = APIRouter(prefix="/video-edits", tags=["video-edits"])

@router.post("/detect-scenes", response_model=ResponseModel)
async def detect_scenes_endpoint(request: DetectScenesRequest):
    try:
        cuts = await run_in_threadpool(
            process_detect_scenes,
            request.video_path,
            request.luminosity_threshold
        )
        return ResponseModel(status="success", data=cuts)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/accel-decel", response_model=ResponseModel)
async def accel_decel_video(request: AccelDecelRequest):
    try:
        output_path = await run_in_threadpool(
            process_accel_decel_video,
            request.video_path,
            request.new_duration,
            request.abscissa_fixed,
            request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/blink", response_model=ResponseModel)
async def blink_video(request: BlinkRequest):
    try:
        output_path = await run_in_threadpool(
            process_blink_video,
            request.video_path,
            request.duration_on,
            request.duration_off,
            request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gamma-correction", response_model=ResponseModel)
async def gamma_correction_video(request: GammaCorrectionRequest):
    try:
        output_path = await run_in_threadpool(
            process_gamma_correction_video,
            request.video_path,
            request.gamma,
            request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/painting", response_model=ResponseModel)
async def painting_video(request: PaintingRequest):
    try:
        output_path = await run_in_threadpool(
            process_painting_video,
            request.video_path,
            request.saturation,
            request.black,
            request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect-highlights", response_model=ResponseModel)
async def detect_highlights(request: DetectRequest):
    try:
        output = process_detect_highlights(
            request.video_path, request.threshold, request.output
        )
        return ResponseModel(status="success", output=output)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cut", response_model=ResponseModel)
async def cut_video(request: CutRequest):
    try:
        output_path = process_cut_video(
            request.video_path, request.start_time, request.end_time, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/color-effect", response_model=ResponseModel)
async def color_effect_video(request: ColorEffectRequest):
    try:
        output_path = await run_in_threadpool(
            process_color_effect,
            request.video_path,
            request.effect_type,
            request.factor,
            request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mirror", response_model=ResponseModel)
async def mirror_video(request: MirrorRequest):
    try:
        output_path = process_mirror_video(
            request.video_path, request.axis, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rotate", response_model=ResponseModel)
async def rotate_video(request: RotateRequest):
    try:
        output_path = process_rotate_video(
            request.video_path, request.angle, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/crop", response_model=ResponseModel)
async def crop_video(request: CropRequest):
    try:
        output_path = process_crop_video(
            request.video_path, request.x1, request.y1, request.x2, request.y2, request.width, request.height, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/margin", response_model=ResponseModel)
async def margin_video(request: MarginRequest):
    try:
        output_path = process_margin_video(
            request.video_path, request.margin, request.color, request.opacity, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fade", response_model=ResponseModel)
async def fade_video(request: FadeRequest):
    try:
        output_path = await run_in_threadpool(
            process_fade_video,
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
async def loop_video(request: LoopRequest):
    try:
        output_path = process_loop_video(
            request.video_path, request.n, request.duration, request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/time-effect", response_model=ResponseModel)
async def time_effect_video(request: TimeEffectRequest):
    try:
        output_path = await asyncio.to_thread(
            process_time_effect_video,
            request.video_path,
            request.effect_type,
            request.duration,
            request.output_path
        )
        return ResponseModel(status="success", output_path=output_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
