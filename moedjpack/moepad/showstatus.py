# -*- coding: utf-8 -*-
import os
from moedjpack.moepad.mputils import rs
from moedjpack.moepad.mpdefs import *


_dir = os.path.join(os.path.dirname(__file__), os.path.pardir)

logfile = os.path.join(_dir, "MoePad.log")


def showlog():
    os.system("tail -20 %s" % logfile)


def show_verifying():
    verifying_items = rs.zrange(VERIFYING_SET, 0, -1)
    for item in verifying_items:
        print(item)
