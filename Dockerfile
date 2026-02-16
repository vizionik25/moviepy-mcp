# Combined Dockerfile for VideoEditor-MCP
FROM python:3.12-slim-bookworm

# Install system dependencies (ffmpeg is required for MoviePy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    fonts-dejavu-core \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (needed for frontend)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install backend dependencies first (for better caching)
RUN uv export --no-emit-project --format requirements-txt > requirements.txt && \
    uv pip install --system -r requirements.txt && \
    rm requirements.txt

# Copy frontend dependency files
COPY frontend/package.json frontend/package-lock.json* ./frontend/

# Install frontend dependencies
RUN cd frontend && npm install

# Copy the rest of the application code
COPY . .

# Install the project itself
RUN uv pip install --system --no-deps .

# Build frontend for production
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN cd frontend && npm run build

# Create storage directory for videos
RUN mkdir -p /app/storage

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV VIDEO_STORAGE_DIR=/app/storage
ENV PYTHONPATH=/app/src
ENV NODE_ENV=production

# Expose ports
EXPOSE 8000 3000

# Make start.sh executable
RUN chmod +x start.sh

# Startup command
CMD ["./start.sh", "--prod"]
