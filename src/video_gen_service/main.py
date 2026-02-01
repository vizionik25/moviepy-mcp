from fastapi import FastAPI
from .routers import video

app = FastAPI(title="Video Generation Service")

app.include_router(video.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Video Generation Service"}
