#!/bin/bash
# X/Twitter OAuth 2.0 MCP stdio wrapper for Hermes

set -e

ENV_FILE="/home/ansen/projects/fabiaweb_marketing/config/.env"
if [[ -f "$ENV_FILE" ]]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs -d '\n' 2>/dev/null || true)
fi

exec python3 /home/ansen/projects/fabiaweb_marketing/mcp/x_oauth2_server.py
