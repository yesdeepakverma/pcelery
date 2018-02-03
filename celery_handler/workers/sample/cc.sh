#!/usr/bin/env bash
PROJECT_ROOT=/code/DJTT/DJTTv2
WORKDIR=/code/DJTT/DJTTv2/api/src/apps/
VIRTUALENV=/code/DJTT/DJTTv2/venv

source $VIRTUALENV/bin/activate
cd $WORKDIR

echo "Running Celery Worker - cc"
$VIRTUALENV/bin/celery -A celery_handler.workers.cc worker --loglevel=info -Q cc --hostname=cc@%h
