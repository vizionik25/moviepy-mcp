from fastapi import FastAPI
from .routers import video, video_edits, audio, compositing

app = FastAPI(title="Video Generation Service")

app.include_router(video.router)
app.include_router(video_edits.router)
app.include_router(audio.router)
app.include_router(compositing.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Video Generation Service"}
