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

## MCP Server

To run the MCP server:

```bash
uv run python -m video_gen_service.mcp_server
```
