# System Design: MoviePy MCP Video Generation Service

## Overview
The Video Generation Service is a modular system designed to provide programmatic video editing capabilities through both RESTful API and MCP (Model Context Protocol).

## Architecture Components

### 1. FastAPI Backend (`src/videoEditor_mcp`)
- **Main Application (`main.py`)**: Entry point for the FastAPI server. Orchestrates routers.
- **Routers (`routers/`)**: Category-specific API endpoints (audio, video, compositing, LLM).
- **Video Utilities (`video_utils.py`)**: Core logic using MoviePy to process media. Handles safety checks and file operations.
- **Schemas (`schemas.py`)**: Pydantic models for request/response validation.

### 2. MCP Server (`mcp_server.py`)
- Built using **FastMCP**.
- Exposes tools that map directly to the `video_utils` functions.
- Allows AI agents to execute video editing tasks autonomously.

### 3. Frontend (`frontend/`)
- **Next.js / React**: Modern UI for user interaction.
- **LiteLLM Integration**: Connects to various LLM providers (local or cloud).
- **MCP Client**: Enables the UI/LLM to communicate with the MCP server tools.

### 4. Storage
- **SAFE_DIR**: A dedicated directory for input/output files to ensure security and prevent arbitrary file system access.

## Data Flow
1. **Request**: User (via Frontend) or AI Agent (via MCP) sends a request with parameters.
2. **Validation**: Pydantic schemas validate the input.
3. **Processing**: `video_utils` invokes MoviePy functions. MoviePy uses FFmpeg for the heavy lifting.
4. **Output**: The processed file is saved to `SAFE_DIR`, and the path is returned to the user.

## Security Considerations
- **Path Validation**: All input/output paths are validated to be within `SAFE_DIR` or `/tmp`.
- **Thread Safety**: Blocking MoviePy calls are offloaded to threads to prevent blocking the async event loop.
