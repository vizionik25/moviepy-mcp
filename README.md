# MoviePy MCP Video Generation Service

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful video generation and editing service powered by FastAPI, MoviePy, and FastMCP.

## 🎬 Description

This project provides a comprehensive service for programmatically creating and manipulating video and audio content. It exposes a rich set of tools through both a RESTful API (using FastAPI) and a Model-Context-Protocol (MCP) server, making it easy to integrate video editing capabilities into any application or AI agent-based workflow.

Whether you need to generate simple clips, perform complex edits, or composite multiple videos, this service offers a robust and easy-to-use solution.

### ✨ Key Features

*   **Dual-Interface**: Interact via a standard REST API or a flexible MCP server for AI agents.
*   **Rich Editing Suite**: A wide range of tools for video, audio, and compositing tasks.
*   **Extensible**: Built with a modular router-based architecture, making it easy to add new features.
*   **Containerized**: Comes with Docker support for easy deployment and scaling.
*   **Modern Tooling**: Uses `uv` for fast dependency management and `pytest` for robust testing.

## 📖 Table of Contents

*   [Installation](#-installation)
*   [🚀 Quick Start](#-quick-start)
    *   [Running the API Server](#running-the-api-server)
    *   [Running the MCP Server](#running-the-mcp-server)
*   [🛠️ API Documentation](#️-api-documentation)
    *   [Video Generation](#video-generation)
    *   [Video Editing](#video-editing)
    *   [Audio Processing](#audio-processing)
    *   [Compositing](#compositing)
*   [🤖 MCP Tools](#-mcp-tools)
*   [🧪 Development & Testing](#-development--testing)
    *   [Setup](#setup)
    *   [Running Tests](#running-tests)
*   [🐳 Docker Deployment](#-docker-deployment)
*   [📜 License](#-license)

## 📦 Installation

### Prerequisites

*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) (a fast Python package installer)
*   FFmpeg (required by MoviePy for video processing)

```bash
# On Debian/Ubuntu
sudo apt-get update && sudo apt-get install -y ffmpeg

# On macOS (using Homebrew)
brew install ffmpeg
```

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/moviepy-mcp.git
    cd moviepy-mcp
    ```

2.  **Install dependencies using `uv`:**
    This command creates a virtual environment and installs all required packages from `pyproject.toml`.
    ```bash
    uv sync
    ```

## 🚀 Quick Start

You can run the service as a REST API server or as an MCP server.

### Running the API Server

The API server provides standard HTTP endpoints for all video and audio operations.

```bash
uv run uvicorn src.video_gen_service.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be accessible at `http://localhost:8000`. You can explore the interactive API documentation (powered by Swagger UI) at `http://localhost:8000/docs`.

**Example: Generate a video using `curl`**
```bash
curl -X POST "http://localhost:8000/video/generate" \
-H "Content-Type: application/json" \
-d '{"text": "Hello, World!", "duration": 5}'
```

### Running the MCP Server

The MCP server is designed for interaction with AI agents that can consume and use the provided tools.

```bash
uv run python -m src.video_gen_service.mcp_server
```

The server will start and listen for MCP connections over standard I/O by default.

**MCP Transport Modes:**

You can also run the MCP server in different transport modes using environment variables:

*   **HTTP**:
    ```bash
    MCP_TRANSPORT=http PORT=8001 uv run python -m src.video_gen_service.mcp_server
    ```
*   **Server-Sent Events (SSE)**:
    ```bash
    MCP_TRANSPORT=sse PORT=8001 uv run python -m src.video_gen_service.mcp_server
    ```

## 🛠️ API Documentation

The following is a summary of the available API endpoints. For detailed request/response models, please refer to the auto-generated docs at `http://localhost:8000/docs`.

### Video Generation

*   **`POST /video/generate`**: Creates a simple video with text on a background.

### Video Editing

*   **`POST /video-edits/cut`**: Trims a video.
*   **`POST /video-edits/concatenate`**: Joins multiple videos.
*   **`POST /video-edits/resize`**: Resizes a video.
*   **`POST /video-edits/speed`**: Changes the playback speed.
*   **`POST /video-edits/color-effect`**: Applies a color filter.
*   **`POST /video-edits/mirror`**: Mirrors the video horizontally or vertically.
*   **`POST /video-edits/rotate`**: Rotates the video.
*   **`POST /video-edits/crop`**: Crops the video.
*   **`POST /video-edits/margin`**: Adds a margin around the video.
*   **`POST /video-edits/fade`**: Applies fade-in or fade-out.
*   **`POST /video-edits/loop`**: Loops the video content.
*   **`POST /video-edits/time-effect`**: Applies time-based effects like reverse or freeze.

### Audio Processing

*   **`POST /audio/volume`**: Adjusts the volume of a video's audio.
*   **`POST /audio/extract`**: Extracts the audio track from a video.
*   **`POST /audio/fade`**: Fades the audio in or out.
*   **`POST /audio/loop`**: Loops the audio track.

### Compositing

*   **`POST /compositing/composite`**: Stacks or grids multiple videos together.
*   **`POST /compositing/text-overlay`**: Adds a text overlay to a video.
*   **`POST /compositing/image-overlay`**: Adds an image overlay to a video.

## 🤖 MCP Tools

The MCP server exposes a wide range of tools for agentic workflows. Each tool corresponds to one of the API functionalities.

**Example MCP Tools:**

*   `create_video(text: str, duration: float)`
*   `cut_video(video_path: str, start_time: float, end_time: float)`
*   `concatenate_videos(video_paths: List[str])`
*   `resize_video(video_path: str, scale: float)`
*   `text_overlay(video_path: str, text: str)`
*   `adjust_volume(video_path: str, factor: float)`
*   ...and many more!

Refer to `src/video_gen_service/mcp_server.py` for a complete list of available tools and their signatures.

## 🧪 Development & Testing

### Setup

Follow the [Installation](#-installation) steps to set up the development environment. The `dev` dependency group in `pyproject.toml` includes `pytest` and `httpx` for testing.

### Running Tests

To run the full test suite:
```bash
uv run pytest
```

To run tests with code coverage analysis:
```bash
uv run pytest --cov=src
```

## 🐳 Docker Deployment

This project includes a `Dockerfile` and `docker-compose.yml` for easy containerization.

1.  **Build the Docker image:**
    ```bash
    docker-compose build
    ```

2.  **Run the service:**
    This will start the FastAPI server on port 8000.
    ```bash
    docker-compose up
    ```

### ✈️ Fly.io Deployment

The project is configured for deployment on Fly.io.

**Connection Endpoint:**

By default, the `Dockerfile` sets `MCP_TRANSPORT=sse`. When deployed, the MCP server connection endpoint will be:

*   **SSE Endpoint:** `https://<APP_NAME>.fly.dev/sse`
*   **Messages Endpoint:** `https://<APP_NAME>.fly.dev/messages/`

**Using HTTP Transport:**

If you prefer to use stateless HTTP (JSON-RPC over HTTP), you can override the transport environment variable in your `fly.toml` or via the Fly.io CLI.

Set `MCP_TRANSPORT=http` in your configuration. The endpoint will then be:

```
https://<APP_NAME>.fly.dev/mcp
```

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.