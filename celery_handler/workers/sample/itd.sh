#!/usr/bin/env bash
PROJECT_ROOT=/code/DJTT/FTTv2
WORKDIR=/code/DJTT/DJTTv2/api/src/apps/
VIRTUALENV=/code/DJTT/DJTTv2/venv

source $VIRTUALENV/bin/activate
cd $WORKDIR

echo "Running Celery Worker - itd"
$VIRTUALENV/bin/celery -A celery_handler.workers.itd worker --loglevel=info -Q itd --hostname=itd@%h
