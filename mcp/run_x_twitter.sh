#!/bin/bash
# X/Twitter MCP stdio wrapper for Hermes
# Sources credentials from fabiabox_marketing .env and maps to expected names

set -e

ENV_FILE="/home/ansen/projects/fabiabox_marketing/.env"
if [[ -f "$ENV_FILE" ]]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs -d '\n' 2>/dev/null || true)
fi

# Map credentials to x-twitter-mcp-server expected names
export X_APP_KEY="${CONSUMER_KEY:-${X_API_KEY:-}}"
export X_APP_SECRET="${CONSUMER_KEY_SECRET:-${X_API_SECRET:-}}"
export X_ACCESS_TOKEN="${X_ACCESS_TOKEN:-}"
export X_ACCESS_SECRET="${X_ACCESS_TOKEN_SECRET:-}"

exec npx -y x-twitter-mcp-server
