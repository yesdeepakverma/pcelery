####This Application house a rest endpoint internal to FTT application

That will allow a way to call celery task which in turn will be processed by celery workers.

- We are going to use RabbitMQ messaging queue.
- All celery application configuration exists in celery_app.py
- All celery tasks are in tasks module

### Monitoring Celery Workers
 - Celery Flower
 - /code/dev/venv/bin/celery flower -A ets worker --loglevel=info -Q ets --hostname=ets_dev@%h --port 5556
 - /code/DJTT/DJTTv2/venv/bin/celery flower -A worker1 worker --loglevel=info -Q ets --hostname=ets_dev@%h --port 5556
 - /code/DJTTv2/venv/bin/celery flower -A ets worker --loglevel=info -Q ets --hostname=ets_uat@%h
 - http://docs.celeryproject.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor
 
### Monitoring RabbitMQ messaging Queue
 - rabbitmqctl command
 - sudo rabbitmq-plugins enable rabbitmq_management
 - http://localhost:15672/
    add in [{rabbit, [{loopback_users, []}]}].  in below config file, create if not already exists.
    /etc/rabbitmq/rabbitmq.config
    
    You should not user default guest/guest user for production use

  -   
   then access using guest/guest
 - http://docs.celeryproject.org/en/latest/userguide/monitoring.html#inspecting-queues


### Managing Celery Workers
 - $ celery multi start 1 -A proj -l info -c4 --pidfile=/var/run/celery/%n.pid
 - $ celery multi restart 1 --pidfile=/var/run/celery/%n.pid
 - http://docs.celeryproject.org/en/latest/userguide/workers.html#variables-in-file-paths

#Other Readme links
 - http://docs.celeryproject.org/en/latest/userguide/monitoring.html#guide-monitoring
 
 