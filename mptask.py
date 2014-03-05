# -*- coding: utf-8 -*-
# from celery.schedules import crontab

# CELERYBEAT_SCHEDULE = {
#     # Executes every Monday morning at 7:30 A.M
#     'add-every-monday-morning': {
#         'task': 'tasks.add',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16),
#     },
# }

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'tesks.add',
        'schedule': timedelta(seconds=2),
        'args': (16, 16)
    },
}

CELERY_TIMEZONE = 'UTC'
