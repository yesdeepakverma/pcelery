__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"

import logging

from django.conf import settings
from django.views import View

from kombu.exceptions import OperationalError

from core.constants import *
from core.common.utils import get_utc, json_response, send_email

from celery_handler.utils import get_task_queue
from celery_handler.tasks import ETS, CC, ITD
from celery_handler.celeryconfig import task_publish_retry_policy


from common.models import Task_Report

api_logger = logging.getLogger("api")
error_logger = logging.getLogger("error")
celery_failed = logging.getLogger("celery_failed")


queue_task_mapping = {
    'ets': ETS,
    'cc': CC,
    'itd': ITD
}


class TaskHandler(View):
    def post(self, request, *args, **kwargs):
        """
        Single Endpoint to handle all celery related Task rest calls
        This View takes 3 arguments
        :param data_key: comma separated data_key to update
        :param user_instance: comma separated user_instance
        :param client_instance: client_instance, all user instance should of of this group
        """

        data_key = request.POST.get('data_key')
        user_instance = request.POST.get('user_instance')
        client_instance = request.POST.get('client_instance')
        task_queue = ''
        if not (data_key and user_instance and client_instance):
            code = CELERY_NOT_ENOUGH_ARGUMENTS
        else:
            for user in user_instance.split(','):
                for d_key in data_key.split(','):
                    task_queue = get_task_queue(d_key)
                    kwargs = {'client_instance': client_instance,
                              'user_instance': user,
                              'data_key': d_key}
                    try:
                        queue_task_mapping.get(task_queue, ETS)().apply_async(kwargs=kwargs,
                                                                            queue=task_queue,
                                                                            retry=True,
                                                                            retry_policy=task_publish_retry_policy)
                        code = CELERY_TASKS_ADDED
                    except Exception as ex:
                        # If Rabbit MQ is down
                        self.update_task_report(d_key, task_args='', task_kwargs=kwargs)
                        email_body = "{} - {}".format(kwargs, ex)
                        send_email(settings.ERROR_MAIL_TO, email_body=email_body, email_subject="[CRITICAL][CELERY-TASK-NOT-CREATED]-Rabbit MQ is down? Celery tasks not created !")
                        code = CELERY_ERROR_INSERTING_TASK

        return json_response({'code': code, 'task_queue': task_queue})

    def update_task_report(self, data_key, **kwargs):
        """
        Insert task details in Task_Report Table
        :param data_key: data_key of the task
        :param kwrags:
        :return:
        """
        task_args = str(kwargs.get('task_args', ''))
        task_kwargs = str(kwargs.get('task_kwargs', ''))
        treport = Task_Report(task_name=data_key,
                              task_state="NOT-CREATED",
                              task_args=task_args,
                              task_kwargs=task_kwargs,
                              task_received=str(get_utc()))
        treport.save()
