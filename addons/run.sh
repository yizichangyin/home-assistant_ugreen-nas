#!/bin/bash

set -e

CONFIG_FILE="/app/config.json"

if [[ -z "$UGREEN_NAS_API_SCHEME" ]]; then
  echo "config.json"
  export UGREEN_NAS_API_SCHEME=$(jq -r '.options.UGREEN_NAS_API_SCHEME' "$CONFIG_FILE")
  export UGREEN_NAS_API_IP=$(jq -r '.options.UGREEN_NAS_API_IP' "$CONFIG_FILE")
  export UGREEN_NAS_API_PORT=$(jq -r '.options.UGREEN_NAS_API_PORT' "$CONFIG_FILE")
  export UGREEN_NAS_API_VERIFY_SSL=$(jq -r '.options.UGREEN_NAS_API_VERIFY_SSL' "$CONFIG_FILE")
else
  echo "docker-compose"
fi

echo "UGREEN_NAS_API_SCHEME: $UGREEN_NAS_API_SCHEME"
echo "UGREEN_NAS_API_IP: $UGREEN_NAS_API_IP"
echo "UGREEN_NAS_API_PORT: $UGREEN_NAS_API_PORT"
echo "UGREEN_NAS_API_VERIFY_SSL: $UGREEN_NAS_API_VERIFY_SSL"

exec uvicorn main:app --host 0.0.0.0 --port 4115