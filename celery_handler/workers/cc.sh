#!/usr/bin/env bash
CODE_PATH=/code/DJTTv2
PROJECT_ROOT=$CODE_PATH
WORKDIR=$CODE_PATH/api/src/apps/
VIRTUALENV=$CODE_PATH/venv

export CODE_PATH=$CODE_PATH
export DB_USER=**
export DB_PASSWORD=****
source $VIRTUALENV/bin/activate
cd $WORKDIR

echo "Running Celery Worker - CC-QA-WORKER"
$VIRTUALENV/bin/celery -A celery_handler.workers.cc worker --loglevel=info -Q cc --hostname=cc_uat@%h