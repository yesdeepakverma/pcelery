"""
This base class implementation for celery tasks
This should be extended by any tasks created for data point

Each salary task should have a worker associated with it
"""

__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"


import logging
import logging.config

from celery.task import Task
from django.conf import settings
from common.models import Task_Report
from core.common.utils import get_utc, send_email

from celery.app.base import Celery
from celery_handler import celeryconfig

from kombu.utils.uuid import uuid


class TaskMaster(Task):
    """
    Define some setup and TearDown function for Celery Task
    """
    def __init__(self):
        self.failed_logger = logging.getLogger('celery_failed')
        self.retried_logger = logging.getLogger('celery_retried')
        self.success_logger = logging.getLogger('celery_success')

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self.retried_logger.info((exc, task_id, args, kwargs, einfo))
        if settings.ENVIRONMENT != 'PROD':
            self.send_email(settings.CELERY_EMAILS_TO, "Task Failed with following details"+str((exc, task_id, args, kwargs, einfo)), email_subject="TASK RETRIED")

        super(TaskMaster, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_success(self, retval, task_id, args, kwargs):
        self.success_logger.debug((task_id, retval, args, kwargs))
        super(TaskMaster, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.failed_logger.debug((exc, task_id, args, kwargs, einfo))
        self.insert_task_report(task_id, task_args=args, task_kwargs=kwargs, task_state="FAILURE", task_exception=exc, task_traceback=einfo)

        self.send_email(email_to=settings.CELERY_EMAILS_TO,
                        email_body="Task Failed with following details {}".format((exc, task_id, args, kwargs, einfo)),
                        email_subject='[CELERY-CRITICAL] - TASK FAILED')
        super(TaskMaster, self).on_failure(exc, task_id, args, kwargs, einfo)


    def apply_async123(self, args=None, kwargs=None, task_id=None, producer=None,
                    link=None, link_error=None, shadow=None, **options):

        app = Celery('FTT_Tasker', set_as_current=True, loader='default')
        app.config_from_object(celeryconfig)
        if app.conf.task_always_eager:
            return self.apply(args, kwargs, task_id=task_id or uuid(),
                              link=link, link_error=link_error, **options)
        # add 'self' if this is a "task_method".
        if self.__self__ is not None:
            args = args if isinstance(args, tuple) else tuple(args or ())
            args = (self.__self__,) + args
            shadow = shadow or self.shadow_name(args, kwargs, options)

        preopts = self._get_exec_options()
        options = dict(preopts, **options) if options else preopts
        return app.send_task(
            self.name, args, kwargs, task_id=task_id, producer=producer,
            link=link, link_error=link_error, result_cls=self.AsyncResult,
            shadow=shadow, task_type=self,
            **options
        )

    def update_state(self, task_id=None, state=None, meta=None):
        super(TaskMaster, self).update_state(task_id, state, meta)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        super(TaskMaster, self).after_return(status, retval, task_id, args, kwargs, einfo)

    def send_email(self, email_to, email_body, email_from=settings.EMAIL_FROM, email_subject="[CRITICAL]-CELERY-NOTIFICATION"):
        """
        Send email
        :param email_to: email recipient list
        :param email_body:
        :param email_from:
        :param email_subject:
        :return: None
        """
        send_email(email_to=email_to, email_body=email_body, email_from=email_from, email_subject=email_subject)

    def run(self, client_instance, user_instance, data_key, **kwargs):
        """
        Must pass user_instance and data_key as keyword arguments
        :param user_instance:
        :param data_key:
        :param kwargs: extensible function definition
        :return: this works asychrocously as we do not need to keep track of what returned form here
        """
        task_func_name = 'update_'+data_key.lower()
        # task_func_name = 'set_'+data_key.lower()
        task_func = getattr(self, task_func_name)
        try:
            return task_func(client_instance=client_instance, user_instance=user_instance, data_key=data_key, **kwargs)
        except Exception as ex:
            self.retry(countdown=2, exc=ex)

    def update_count(self, client_instance, user_instance, data_key, **kwargs):
        """
        This function takes a data_key and inserts counts for the specified user
        This will call a procedure which in turn will update the count in de-normalised table
        :return: None
        """
        from django.db import connection
        cursor = connection.cursor()
        cursor.callproc("pace_master.dbo.uspMasterDashboardCountSet", (data_key, user_instance, client_instance))
        cursor.close()

    def insert_task_report(self, task_id, task_args="", task_kwargs="", task_state="FAILURE", task_exception='', task_traceback=''):
        """
        update task state in Task_Report Table
        :param task_id: task id
        :param task_args: task positional argument
        :param task_kwargs: task keyword arguments
        :param task_state: task state
        :param task_exception: exception detail if any
        :param task_traceback: detailed exception detail if any
        :return:
        """
        treport = Task_Report(task_id=task_id,
                              task_name=self.name,
                              task_args=str(task_args),
                              task_kwargs=str(task_kwargs),
                              task_state=task_state,
                              task_exception=task_exception,
                              task_timestamp=str(get_utc()),
                              task_traceback=task_traceback,
                              task_eta=self.request.eta,
                              task_parent_id=self.request.parent_id,
                              task_root_id=self.request.root_id)
        treport.save()
