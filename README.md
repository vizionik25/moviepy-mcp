# Video Gen Service

A FastAPI application using FastMCP and MoviePy to generate videos.

## Requirements

- Python 3.12+
- `uv` package manager

## Installation

```bash
uv sync
```

## Running the Server

```bash
uv run uvicorn video_gen_service.main:app --reload
```

## Running Tests

```bash
uv run pytest
```

To run tests with coverage:

```bash
uv run pytest --cov=src
```

## MCP Server

To run the MCP server:

```bash
uv run python -m video_gen_service.mcp_server
```

## Features

### Video Generation & Editing
- **Create Video**: Generate simple text-on-background videos.
- **Cut**: Trim videos by start and end time.
- **Concatenate**: Join multiple videos together.
- **Resize**: Resize videos by width, height, or scale.
- **Speed**: Adjust playback speed.
- **Mirror**: Mirror video along X or Y axis.
- **Rotate**: Rotate video by degrees.
- **Crop**: Crop video to specific dimensions.
- **Margin**: Add colored margins to video.
- **Fade**: Apply fade-in or fade-out effects.
- **Loop**: Loop video content.
- **Time Effects**: Reverse, symmetrize, or freeze video time.

### Audio Processing
- **Volume**: Adjust audio volume.
- **Extract Audio**: Extract audio track from video.
- **Audio Fade**: Fade audio in or out.
- **Audio Loop**: Loop audio track.

### Compositing
- **Composite**: Stack or grid multiple videos.
- **Text Overlay**: Add text overlays with customizable properties.
- **Image Overlay**: Add image overlays with positioning and opacity.
- **Color Effects**: Apply Black & White, Invert, Brightness, or Contrast effects.

## API Endpoints

### Video Edits (`/video-edits`)
- `POST /cut`
- `POST /concatenate`
- `POST /resize`
- `POST /speed`
- `POST /color-effect`
- `POST /mirror`
- `POST /rotate`
- `POST /crop`
- `POST /margin`
- `POST /fade`
- `POST /loop`
- `POST /time-effect`

### Audio (`/audio`)
- `POST /volume`
- `POST /extract`
- `POST /fade`
- `POST /loop`

### Compositing (`/compositing`)
- `POST /composite`
- `POST /text-overlay`
- `POST /image-overlay`
