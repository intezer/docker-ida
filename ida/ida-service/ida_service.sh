#!/usr/bin/env bash
CORES=${1:-8}
gunicorn -w $CORES -b 0.0.0.0:4000 flask_service:app