from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import video, video_edits, audio, compositing
from .mcp_server import mcp
from fastmcp.server.http import create_streamable_http_app

mcp_app = create_streamable_http_app(server=mcp, streamable_http_path="/mcp")

app = FastAPI(title="Video Generation Service", lifespan=mcp_app.lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev/mcp
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount MCP server
app.mount("/mcp", mcp_app)

app.include_router(video.router)
app.include_router(video_edits.router)
app.include_router(audio.router)
app.include_router(compositing.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Video Generation Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.videoEditor_mcp.main:app", host="0.0.0.0", port=8000, reload=True)
