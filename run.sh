#!/usr/bin/env bash

mkdir -p /tmp/prometheus
PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus gunicorn --timeout=120 -b 0.0.0.0:5000 manage:app --workers=10 --worker-class=gevent --worker-connections=200 --no-sendfile