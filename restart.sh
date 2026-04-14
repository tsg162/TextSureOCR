#!/usr/bin/env bash
# TextSureOCR — kill stale processes and re-launch service + tunnel.
# Usage: bash restart.sh
set -euo pipefail

WORK=/workspace/textsure
ENV_FILE="$WORK/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "FATAL: $ENV_FILE not found. Run setup.sh first."
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

PORT="${TEXTSURE_PORT:-5002}"

echo "=== TextSureOCR Restart ==="
echo ""

# ── Kill existing processes ──
echo "--- Stopping existing processes ---"
for pidfile in "$WORK/textsure.pid" "$WORK/tunnel.pid"; do
  if [ -f "$pidfile" ]; then
    PID=$(cat "$pidfile")
    if kill -0 "$PID" 2>/dev/null; then
      echo "  Killing PID $PID ($(basename "$pidfile" .pid))"
      kill "$PID" 2>/dev/null || true
    fi
    rm -f "$pidfile"
  fi
done

# Also kill anything on our port
fuser -k "$PORT/tcp" 2>/dev/null || true
sleep 2

# ── Re-launch via install.sh ──
echo ""
exec bash "$WORK/install.sh"
