#!/usr/bin/env bash
PROJECT_ROOT=$CODE_PATH
WORKDIR=$CODE_PATH/api/src/apps/
VIRTUALENV=$CODE_PATH/venv

source $VIRTUALENV/bin/activate
cd $WORKDIR

echo "Running Celery Worker - ETS-DEV-WORKER"
$VIRTUALENV/bin/celery -A celery_handler.workers.ets worker --loglevel=info -Q ets --hostname=ets_dev@%h

