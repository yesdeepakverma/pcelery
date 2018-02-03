"""
All celery configuration, this exists when using Celery without Django.
Just Plain Celery
"""
__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"


import os, sys
from django.core.wsgi import get_wsgi_application
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

environment = os.environ.get('ENVIRONMENT', 'DEV')
setting_file_mapping = {
    'PROD': 'settings_prod',
    'MA_DEV': 'settings_dev',
    'MA_QA': 'settings_qa',
    'UAT': 'settings_uat',
    'DEV': 'settings_dverma'
}
environment_setting = setting_file_mapping.get(environment, 'settings_dverma')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.{}".format(environment_setting))
application = get_wsgi_application()
from django.conf import settings

###################################################################################################
#####CELERY Things##################################################################################

# following is a mapping of
task_queue_mapping = {
    'ptc_count': 'ets'
}
worker_queue_mapping = {
    'worker2': 'ets',
    'worker1': 'itd',
    'worker3': 'cc',
    'ets': 'ets',
    'itd': 'itd',
    'cc': 'cc',
}

queue_route_mapping = {
    'ets': {'celery_handler.tasks.ets.*': {'queue': 'ets'}},
    'itd': {'celery_handler.tasks.itd.*': {'queue': 'itd'}},
    'cc': {'celery_handler.tasks.cc.*': {'queue': 'cc'}},
}

BROKER = settings.BROKER

broker_url = "{PROTOCOL}://{USER}:{PASSWORD}@{HOST}:{PORT}".format(**BROKER)

result_backend = 'amqp://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True

task_default_queue = 'ets'


task_routes = {
    'celery_handler.tasks.ets.*': {'queue': 'ets'},
    'celery_handler.tasks.itd.*': {'queue': 'itd'},
    'celery_handler.tasks.cc.*': {'queue': 'cc'},
}
broker_connection_retry = True  # default
broker_connection_max_retries = 100  # default

task_publish_retry = True  # default
task_publish_retry_policy = {
    'max_retries': 5,  # Maximum number of retries before giving up, in this case the exception that caused the retry to fail will be raised.
    'interval_start': 0,  # Defines the number of seconds (float or integer) to wait between retries
    'interval_step': 0.2,  # On each consecutive retry this number will be added to the retry delay
    'interval_max': 0.2,  # Maximum number of seconds (float or integer) to wait between retries
}
