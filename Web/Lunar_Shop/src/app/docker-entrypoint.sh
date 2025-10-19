#!/bin/bash
set -euo pipefail

WORKERS=${WORKERS:-1}
WORKER_CLASS=${WORKER_CLASS:-gevent}
WORKER_TEMP_DIR=${WORKER_TEMP_DIR:-/dev/shm}
SECRET_KEY=${SECRET_KEY:-}

echo "Starting Challenge"
exec uv run gunicorn 'app:create_app()' \
  --bind '0.0.0.0:8000' \
  --workers "$WORKERS" \
  --worker-tmp-dir "$WORKER_TEMP_DIR" \
  --worker-class "$WORKER_CLASS" \
  --log-level critical \
  --access-logfile /dev/null \
  --error-logfile /dev/null

