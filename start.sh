#!/bin/bash
set -e

# Mandatory argument: --prod or --dev
if [[ "$1" != "--prod" && "$1" != "--dev" ]]; then
    echo "Error: Mandatory argument --prod or --dev is required."
    echo "Usage: $0 [--prod|--dev]"
    exit 1
fi

MODE=$1

# Ensure we are in the project root
cd "$(dirname "$0")"

# Set PYTHONPATH to include the src directory
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

echo "🚀 Starting FastAPI App..."
# Start FastAPI in background
uv run python -m videoEditor_mcp.main &
BACKEND_PID=$!

# Health check
echo "⏳ Waiting for FastAPI to be healthy (http://localhost:8000/)..."
MAX_RETRIES=60
RETRY_COUNT=0
until curl -s http://localhost:8000/ > /dev/null; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -gt $MAX_RETRIES ]; then
      echo "❌ Error: FastAPI failed to start after $MAX_RETRIES seconds."
      kill $BACKEND_PID
      exit 1
    fi
    sleep 1
done
echo "✅ FastAPI is healthy!"

echo "🚀 Starting MCP Server..."
# Start MCP Server in background
uv run python -m videoEditor_mcp.mcp_server &
MCP_PID=$!

echo "🚀 Starting Frontend in $MODE mode..."
cd frontend

# Install dependencies if node_modules doesn't exist (helpful for first-time local run)
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

if [[ "$MODE" == "--dev" ]]; then
    npm run dev
else
    # In production mode, we assume the app is already built or we build it now
    if [ ! -d ".next" ]; then
        echo "🏗️ Building frontend for production..."
        npm run build
    fi
    npm start
fi

# Cleanup on exit
trap "kill $BACKEND_PID $MCP_PID" EXIT
wait
