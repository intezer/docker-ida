#!/usr/bin/env bash
if [ -z "${1+x}" ]; then
    CORES=8
else
    CORES=${1}
fi
gunicorn -w $CORES -b 0.0.0.0:4000 flask_service:app