#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Sai
# @Date:   2014-02-12 23:13:59
# @Email:  email@example.com
# @Last modified by:   Sai
# @Last modified time: 2014-03-02 16:54:32
# 🎵 ミライナイト
import redis
import logging
import logging.handlers
import pytz
import os
import os.path as p
import logging.config
from datetime import datetime
from moedjpack.moedj.settings import LOGGING

rs = redis.Redis("localhost", db=1)
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('moepad')


def sub_dict(somedict, somekeys, default=None):
    return dict([(k, somedict.get(k, default)) for k in somekeys])


def loggerInit(logfile):
    logger = logging.getLogger(logfile)
    logger.setLevel(logging.DEBUG)
    try:
        fh = logging.handlers.RotatingFileHandler(
            logfile, maxBytes=10*1024*1024, backupCount=2)
    except IOError:
        os.makedirs(p.dirname(logfile))
        fh = logging.handlers.RotatingFileHandler(
            logfile, maxBytes=10*1024*1024, backupCount=2)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def utcnow():
    tz = pytz.timezone('UTC')
    return datetime.now(tz)


def _deletePrefix(key):
    keys_with_prefix = rs.keys(key+"*")
    for key_with_prefix in keys_with_prefix:
        rs.delete(key_with_prefix)


def create_default_db():
    cmd = "mpserver syncdb --noinput"
    os.system(cmd)
    print("---------------------------------------")
    print("input password for user moepad[default]")
    cmd = 'mpserver createsuperuser --username=moepad --email=deloeating@gmail.com'
    os.system(cmd)
