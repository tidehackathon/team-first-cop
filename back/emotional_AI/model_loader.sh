#!/bin/bash

# Download the needed model
python -c "from ModelsOperator import load_models; load_models()"
# turn on bash's job control
export TRANSFORMERS_OFFLINE=1
set -m
gunicorn app:app -b 0.0.0.0:8010 --workers 1 --log-level debug --access-logfile - --timeout 30 --keep-alive 3 -k uvicorn.workers.UvicornWorker