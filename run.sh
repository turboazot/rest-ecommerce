#!/usr/bin/env bash

mkdir -p /tmp/prometheus
PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus gunicorn --timeout=120 -b 0.0.0.0:5000 --log-level DEBUG --log-file=gunicorn.log manage:app --access-logfile=access.log --error-logfile=error.log --workers=3