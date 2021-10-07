#!/usr/bin/env bash

mkdir -p /tmp/prometheus
PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus gunicorn --timeout=120 -b 0.0.0.0:5000 --log-file=gunicorn.log manage:app --access-logfile - --workers=3