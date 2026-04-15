#!/usr/bin/env bash
# TextSureOCR — install deps, start service, start tunnel.
# Called by setup.sh or directly for reinstalls.
set -euo pipefail

WORK=/workspace/textsure
ENV_FILE="$WORK/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "FATAL: $ENV_FILE not found. Run setup.sh first."
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

TUNNEL_TOKEN="${TEXTSURE_TUNNEL_TOKEN:-}"
AUTH_TOKEN="${TEXTSURE_AUTH_TOKEN:-}"
PORT="${TEXTSURE_PORT:-5002}"

# Vast.ai sets $CONTAINER_ID for every container; persist it so /health can expose it.
VAST_INSTANCE_ID="${TEXTSURE_VAST_INSTANCE_ID:-${CONTAINER_ID:-}}"
if [ -n "$VAST_INSTANCE_ID" ] && ! grep -q '^TEXTSURE_VAST_INSTANCE_ID=' "$ENV_FILE"; then
  echo "TEXTSURE_VAST_INSTANCE_ID=$VAST_INSTANCE_ID" >> "$ENV_FILE"
fi

echo "=== TextSureOCR Install ==="
echo ""

# ── Kill anything on our port ──
echo "--- Cleaning up port $PORT ---"
fuser -k "$PORT/tcp" 2>/dev/null || true
sleep 1

# ── Check environment ──
echo "--- Environment ---"
python3 --version
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader 2>/dev/null || echo "  (no GPU detected)"
echo ""

# ── Install Python dependencies ──
echo "--- Installing Python dependencies ---"
pip install --quiet fastapi uvicorn transformers accelerate requests
python3 -c "import torch; print(f'torch {torch.__version__} cuda={torch.cuda.is_available()}')" 2>/dev/null \
  || pip install --quiet torch
echo "Dependencies installed."
echo ""

# ── Install cloudflared ──
echo "--- Installing cloudflared ---"
if ! command -v cloudflared &>/dev/null; then
  curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o /usr/local/bin/cloudflared
  chmod +x /usr/local/bin/cloudflared
  echo "  cloudflared installed: $(cloudflared --version)"
else
  echo "  cloudflared already installed: $(cloudflared --version)"
fi
echo ""

# ── Start TextSureOCR service ──
echo "--- Starting TextSureOCR on port $PORT ---"
cd "$WORK"

export TEXTSURE_PORT="$PORT"
export TEXTSURE_AUTH_TOKEN="$AUTH_TOKEN"
export TEXTSURE_VAST_INSTANCE_ID="$VAST_INSTANCE_ID"

nohup python3 app.py > "$WORK/textsure.log" 2>&1 &
SERVICE_PID=$!
echo "$SERVICE_PID" > "$WORK/textsure.pid"
echo "  Service PID: $SERVICE_PID"

# ── Wait for model load + health ──
echo "  Waiting for model load + health..."
for i in $(seq 1 60); do
  sleep 5
  if ! kill -0 "$SERVICE_PID" 2>/dev/null; then
    echo "FATAL: service died. Check $WORK/textsure.log"
    tail -20 "$WORK/textsure.log" 2>/dev/null || true
    exit 1
  fi
  HEALTH=$(curl -s "http://localhost:$PORT/health" 2>/dev/null || true)
  if echo "$HEALTH" | grep -q '"model_loaded":true' 2>/dev/null; then
    echo "  Health OK: $HEALTH"
    break
  fi
  echo "    attempt $i/60 ..."
done

# Verify health one more time
HEALTH=$(curl -s "http://localhost:$PORT/health" 2>/dev/null || true)
if ! echo "$HEALTH" | grep -q '"model_loaded":true' 2>/dev/null; then
  echo "FATAL: service not healthy after 5 minutes."
  tail -20 "$WORK/textsure.log" 2>/dev/null || true
  exit 1
fi
echo ""

# ── Run test battery ──
echo "=== Running test battery ==="
echo ""
python3 "$WORK/tests.py" "http://localhost:$PORT" || true
echo ""
echo "=== Test battery complete ==="
echo ""

# ── Start Cloudflare tunnel ──
if [ -n "$TUNNEL_TOKEN" ]; then
  echo "--- Starting Cloudflare tunnel ---"
  nohup cloudflared tunnel run --token "$TUNNEL_TOKEN" > "$WORK/tunnel.log" 2>&1 &
  TUNNEL_PID=$!
  echo "$TUNNEL_PID" > "$WORK/tunnel.pid"
  echo "  Tunnel PID: $TUNNEL_PID"
  sleep 3
  if kill -0 "$TUNNEL_PID" 2>/dev/null; then
    echo "  Tunnel running."
  else
    echo "WARNING: tunnel process died. Check $WORK/tunnel.log"
    tail -10 "$WORK/tunnel.log" 2>/dev/null || true
  fi
else
  echo "--- Skipping tunnel (no TEXTSURE_TUNNEL_TOKEN) ---"
fi

echo ""
echo "=== TextSureOCR ready ==="
echo "  Service: http://localhost:$PORT"
echo "  Logs:    $WORK/textsure.log"
echo "  Tunnel:  $WORK/tunnel.log"
echo "  PIDs:    textsure=$(cat "$WORK/textsure.pid") tunnel=$(cat "$WORK/tunnel.pid" 2>/dev/null || echo 'none')"
