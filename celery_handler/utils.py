__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"

from celery_handler import celeryconfig


def get_task_queue(task_name):
    """
    Return Target queue based on task_name
    Task name is data_key form the application
    :param task_name: data_key name
    :return: rabbitmq name
    """
    task_queue = celeryconfig.task_queue_mapping.get(task_name)
    if not task_queue:
        module_name = task_name.lower().split('_')[0]
        task_queue = celeryconfig.worker_queue_mapping.get(module_name)
    return task_queue or celeryconfig.task_default_queue
