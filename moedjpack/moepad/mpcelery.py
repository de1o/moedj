# -*- coding: utf-8 -*-
from celery import Celery
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'send-every-20-mins-in-day': {
        'task': 'moedjpack.moepad.mptask.send',
        'schedule': crontab(hour='0-15,22-0', minute='10,30,50'),
        'args': None,
    },
    'send-once-an-hour-in-night': {
        'task': 'moedjpack.moepad.mptask.send',
        'schedule': crontab(hour='16-22', minute='10'),
        'args': None,
    },
    'update-every-20-mins': {
        'task': 'moedjpack.moepad.mptask.updateitem',
        'schedule': crontab(minute='*'),
        'args': None,
    },
    # 'test': {
    #     'task': 'moedjpack.moepad.mptask.justtest',
    #     'schedule': crontab(hour='0-15,22-0', minute='*'),
    #     'args': None,
    # },
    # 'nighttest': {
    #     'task': 'moedjpack.moepad.mptask.nighttest',
    #     'schedule': crontab(hour='16-22', minute='*/2'),
    #     'args': None,
    # },
}

CELERY_TIMEZONE = 'UTC'

app = Celery('moedjpack.moepad', broker='redis://localhost/1',
             include=['moedjpack.moepad.mptask'])
app.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE, CELERY_TIMEZONE=CELERY_TIMEZONE)


if __name__ == '__main__':
    app.start()
