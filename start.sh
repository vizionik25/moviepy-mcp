#!/bin/bash

# Function to handle signals
cleanup() {
    echo "Received termination signal, shutting down..."
    [ -n "$APP_PID" ] && kill -SIGTERM "$APP_PID" 2>/dev/null
    [ -n "$CADDY_PID" ] && kill -SIGTERM "$CADDY_PID" 2>/dev/null
    wait
    exit 0
}

# Trap signals
trap cleanup SIGTERM SIGINT

# Start the application in the background
echo "Starting application..."
uv run python -m video_gen_service.mcp_server &
APP_PID=$!

# Start Caddy in the background
echo "Starting Caddy..."
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile &
CADDY_PID=$!

# Wait for any process to exit
# wait -n waits for the next background job to finish
wait -n

# If we get here, one process exited unexpectedly.
# We should kill the other and exit.
echo "One process exited unexpectedly. Shutting down..."
[ -n "$APP_PID" ] && kill -SIGTERM "$APP_PID" 2>/dev/null
[ -n "$CADDY_PID" ] && kill -SIGTERM "$CADDY_PID" 2>/dev/null
wait
exit 1
