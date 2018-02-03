__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"


import os, sys

sys.path.append('/code/FTT/FTTv2/api/src/apps/')
from celery_handler.tasks.base import TaskMaster
from celery.exceptions import MaxRetriesExceededError


class ETS(TaskMaster):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("Calling subclass on_failure")
        super(ETS, self).on_failure(exc, task_id, args, kwargs, einfo)

    def __getattr__(self, item):
        """
        If task function is not found
        :param item:
        :return:
        """
        if item.startswith("update_"):
            return self.update_count
        else:
            raise AttributeError(item)

