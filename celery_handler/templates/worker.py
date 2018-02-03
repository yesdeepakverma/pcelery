"""
This template is used to generate a worker module for passed in worker name
and Tasks

This script should be passed with 3 arguments
1. module_name: the name of the worker module, the worker module will be saved as with .py extension
2. tasks: comma separated list of tasks to be executed by worker unlined.

Celery app will be created with same module_name with _app prefixed
"""

__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"


import os
import sys

PROJECT_ROOT = "/code/DJTT/DJTTv2"
WORKERS_PATH = PROJECT_ROOT+'/api/src/apps/celery_handler/workers/'
VENV = PROJECT_ROOT+"/venv"
CELERY_APP_PATH = PROJECT_ROOT+"/api/src/apps/"



WORKER_TEMPLATE = '''
"""
Generated from templates/worker script, make the changes accordingly
"""
import os, sys
sys.path.append('{celery_app_path}')
from celery import Celery
from celery_handler import celeryconfig

worker_name = "{module_name}"
default_routes = celeryconfig.task_routes

task_queue = celeryconfig.worker_queue_mapping.get(worker_name, celeryconfig.task_default_queue)
task_routes = celeryconfig.queue_route_mapping[task_queue]
TASKS = [ "celery_handler.tasks."+task for task in '{tasks}'.split(',')]
{app_name} = Celery('{module_name}', include=TASKS)
{app_name}.config_from_object(celeryconfig)
'''

WORKER_BASH_TEMPLATE = """#!/usr/bin/env bash
PROJECT_ROOT={PROJECT_ROOT}
WORKDIR={celery_app_path}
VIRTUALENV={venv}

source $VIRTUALENV/bin/activate
cd $WORKDIR

echo "Running Celery Worker - {module_name}"
$VIRTUALENV/bin/celery -A celery_handler.workers.{module_name} worker --loglevel=info -Q {queue} --hostname={module_name}@%h
"""


def build_worker(module_name, tasks):
    """

    :param module_name: Worker module name to be passed as first(main) argument to celery.Celery
    :param tasks: Task list to associate with it, tasks should be separated by comma(,) and should be importable
                    i.e. they should be absolute import or relative import if the django app is in system path
    :return: creates a {module_name}.py file for the worker and also a .sh file for the same
    """
    worker_file_path = os.path.join(WORKERS_PATH, module_name+'.py')
    worker_bash_path = os.path.join(WORKERS_PATH, module_name+'.sh')
    app_name = "app_"+module_name
    if os.path.exists(worker_file_path):
        print("Worker {} already exists".format(worker_file_path))
    else:
        with open(worker_file_path, 'w') as wfp:
            worker = WORKER_TEMPLATE.format(module_name=module_name,
                                            tasks=tasks,
                                            app_name=app_name,
                                            celery_app_path=CELERY_APP_PATH
                                            )
            wfp.write(worker)

    if os.path.exists(worker_bash_path):
        print("Worker bash {} script already exists".format(worker_bash_path))
    else:
        with open(worker_bash_path, 'w') as wbp:
            worker_bash = WORKER_BASH_TEMPLATE.format(PROJECT_ROOT=PROJECT_ROOT,
                                                      celery_app_path=CELERY_APP_PATH,
                                                      module_name=module_name,
                                                      venv=VENV,
                                                      queue=tasks
                                                      )
            wbp.write(worker_bash)


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 3:
        print("Please pass module_name tasks and app_name")
        sys.exit(0)
    script, module_name, tasks, *others = argv  # just absorb all arguments
    build_worker(module_name=module_name, tasks=tasks)
