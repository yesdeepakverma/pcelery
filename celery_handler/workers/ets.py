"""
Generated from templates/worker script, make the changes accordingly
"""

__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"

import os, sys

sys.path.append(os.path.join(os.environ['CODE_PATH'], 'api/src/apps/'))

from celery import Celery
from celery_handler import celeryconfig

worker_name = "ets"
default_routes = celeryconfig.task_routes

task_queue = celeryconfig.worker_queue_mapping.get(worker_name, celeryconfig.task_default_queue)
task_routes = celeryconfig.queue_route_mapping[task_queue]
TASKS = [ "celery_handler.tasks."+task for task in 'ets'.split(',')]
app_worker1 = Celery('ets', include=TASKS)
app_worker1.config_from_object(celeryconfig)
