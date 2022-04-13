#!/bin/sh
set -e

source /venv/bin/activate

#while ! flask
#do
#     echo "Retry..."
#     sleep 1
#done

exec gunicorn --bind 0.0.0.0:5000 --forwarded-allow-ips='*' wsgi:app