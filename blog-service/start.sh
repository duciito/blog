#!/bin/sh
celery -A config multi start worker1 -l info\
    --pidfile="$HOME/run/celery/%n.pid" \
    --logfile="$HOME/log/celery/%n%I.log"
python manage.py runserver 0.0.0.0:8000
