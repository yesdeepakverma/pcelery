"""
Celery Endpoint Module urls
"""
from django.conf.urls import url, include
from .views import TaskHandler

urlpatterns = [
            url(r'^task_handler/$', TaskHandler.as_view(), name="task_handler"),
]
