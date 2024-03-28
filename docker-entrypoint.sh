#!/bin/bash
set -e

source /app/.venv/bin/activate

exec gunicorn --bind 0.0.0.0:5000 --forwarded-allow-ips='*' wsgi:app