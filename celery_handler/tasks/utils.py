__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"


import os, sys

sys.path.append('/code/FTT/FTTv2/api/src/apps/')
from .base import TaskMaster
from celery.exceptions import MaxRetriesExceededError


class EMAIL(TaskMaster):
    def run(self, email_to, email_body, email_from="ftt_celery@financial-tracking.com", email_subject="CELERY-NOTIFICATION"):
        """
        Insert in email_outbox the asynchronous way
        :param email_to:
        :param email_body:
        :param email_from:
        :param email_subject:
        :return:
        """
        self.email(email_to, email_body, email_from=email_from, email_subject=email_subject)