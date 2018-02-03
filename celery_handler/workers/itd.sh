#!/usr/bin/env bash
PROJECT_ROOT=$CODE_PATH
WORKDIR=$CODE_PATH/api/src/apps/
VIRTUALENV=$CODE_PATH/venv

source $VIRTUALENV/bin/activate
cd $WORKDIR

echo "Running Celery Worker - worker2"
$VIRTUALENV/bin/celery -A celery_handler.workers.worker2 worker --loglevel=info -Q itd --hostname=worker2@%h
