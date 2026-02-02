# Use uv base image which has uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install system dependencies required for moviepy and imageio
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies (only libs first to cache)
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src/ src/

# Install the project itself
RUN uv sync --frozen

# Set environment variables
ENV MCP_TRANSPORT=http
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose port
EXPOSE 8000

# Command to run the MCP server
CMD ["uv", "run", "python", "-m", "video_gen_service.mcp_server"]
