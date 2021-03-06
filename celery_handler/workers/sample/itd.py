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
sys.path.append('/code/DJTT/DJTTv2/api/src/apps/')
from celery import Celery
from celery_handler import celeryconfig

worker_name = "itd"
default_routes = celeryconfig.task_routes

task_queue = celeryconfig.worker_queue_mapping.get(worker_name, celeryconfig.task_default_queue)
task_routes = celeryconfig.queue_route_mapping[task_queue]
TASKS = [ "celery_handler.tasks."+task for task in 'itd'.split(',')]
app_itd = Celery('itd', include=TASKS)
app_itd.config_from_object(celeryconfig)
