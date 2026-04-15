#!/usr/bin/env bash
# TextSureOCR — one-liner bootstrap for fresh Vast.ai instances.
#
# Usage:
#   bash <(curl -sL https://raw.githubusercontent.com/tsg162/TextSureOCR/main/setup.sh) <tunnel-token> [auth-token]
#
# Or, if already cloned:
#   bash setup.sh <tunnel-token> [auth-token]
set -euo pipefail

TUNNEL_TOKEN="${1:-}"
AUTH_TOKEN="${2:-}"
WORK=/workspace/textsure
REPO_URL="https://github.com/tsg162/TextSureOCR.git"

if [ -z "$TUNNEL_TOKEN" ]; then
  echo "Usage: bash setup.sh <tunnel-token> [auth-token]"
  echo "  tunnel-token  Cloudflare tunnel token (required)"
  echo "  auth-token    Bearer token for /v1/* endpoints (optional)"
  exit 1
fi

echo "=== TextSureOCR Bootstrap ==="
echo ""

# ── Clone or update repo ──
if [ -d "$WORK/.git" ]; then
  echo "--- Updating existing repo ---"
  cd "$WORK"
  git pull --ff-only
else
  echo "--- Cloning repo ---"
  git clone "$REPO_URL" "$WORK"
  cd "$WORK"
fi

# ── Write .env ──
echo "--- Writing .env ---"
cat > "$WORK/.env" <<EOF
TEXTSURE_TUNNEL_TOKEN=$TUNNEL_TOKEN
TEXTSURE_AUTH_TOKEN=$AUTH_TOKEN
TEXTSURE_PORT=5002
EOF
echo "  .env written (auth=$([ -n "$AUTH_TOKEN" ] && echo 'enabled' || echo 'disabled'))"

# ── Hand off to install.sh ──
echo ""
exec bash "$WORK/install.sh"
