#!/usr/bin/env bash
set -e
APP_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$APP_DIR/romaneio_express-v2.py" "$@"
