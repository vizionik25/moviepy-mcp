from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import video, video_edits, audio, compositing

app = FastAPI(title="Video Generation Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router)
app.include_router(video_edits.router)
app.include_router(audio.router)
app.include_router(compositing.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Video Generation Service"}
