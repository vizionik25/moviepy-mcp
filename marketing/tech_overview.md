# Technical Overview: VideoEditor-MCP

## 1. Introduction
VideoEditor-MCP is a specialized backend service designed to provide programmatic video editing capabilities through modern protocols. It leverages the robust MoviePy (v2.2.x) library, exposing its functionality via a high-performance FastAPI server and a FastMCP server.

## 2. Architecture
The system is built on a modular architecture that prioritizes performance and ease of integration:

- **Core Engine:** MoviePy v2.2.x provides the underlying video processing logic.
- **API Layer:** FastAPI handles RESTful requests, providing structured endpoints for video, audio, and compositing tasks.
- **Agentic Layer:** FastMCP exposes MoviePy tools to AI agents using the Model Context Protocol, allowing for natural language command of video editing tasks.
- **Frontend:** A Next.js/React application serves as a management console and MCP client interface.
- **Dependency Management:** Utilizes `uv` for fast, reproducible builds.

## 3. Core Capabilities

### Video Editing & Effects
- **Standard Edits:** Trimming (cut), resizing, speed adjustment, rotation, and cropping.
- **Visual Effects:** Color filters, mirroring, fading (in/out), and looping.
- **Advanced Effects:** 
    - **Chroma Key:** High-quality background removal.
    - **Scene Detection:** Automatic identification of shot changes.
    - **Artistic Filters:** Painting, Kaleidoscope, and Gamma Correction.
    - **Time Manipulation:** Reverse, freeze frames, and acceleration/deceleration.

### Compositing & Audio
- **Multi-Track Compositing:** Stacking videos vertically/horizontally or creating complex grids.
- **Overlays:** Dynamic text and image (watermark) overlays with precise positioning.
- **Audio Management:** Volume normalization, fading, and track extraction.

## 4. Integration & Deployment
- **REST API:** Fully documented with OpenAPI (Swagger), making it compatible with any modern language.
- **MCP Server:** Plug-and-play support for AI agents (Claude Desktop, Cursor, etc.).
- **Dockerized:** Simple deployment using `docker-compose`.
- **Environment:** Requires Python 3.12+ and FFmpeg.

## 5. Use Cases
- **AI Content Pipelines:** Programmatic generation of social media snippets.
- **Automated Video Summarization:** Using scene detection and LLMs to create highlights.
- **Cloud-Based Editing Tools:** Scalable backend for visual web editors.
