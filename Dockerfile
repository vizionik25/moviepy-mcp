# Use uv base image which has uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install system dependencies required for moviepy, imageio, and caddy healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    curl \
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

# Install Caddy
COPY --from=caddy:2 /usr/bin/caddy /usr/bin/caddy

# Copy Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# Copy start script
COPY start.sh ./
RUN chmod +x start.sh

# Set environment variables
ENV MCP_TRANSPORT=sse
ENV HOST=0.0.0.0
ENV PORT=8000
ENV DOMAIN_NAME=localhost
ENV VIDEO_STORAGE_DIR=/app/storage

# Create storage directory
RUN mkdir -p /app/storage

# Expose ports
EXPOSE 80 443 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/healthz || exit 1

# Command to run the start script
CMD ["./start.sh"]
