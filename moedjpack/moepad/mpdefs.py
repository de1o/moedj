#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mpconf import MPConf

WIKIITEM_PREFIX = 'WikiItem:'
NEWITEM = WIKIITEM_PREFIX+"New:"
EDITED = WIKIITEM_PREFIX+'Edited:'
SENT = WIKIITEM_PREFIX+'Sent:'
VERIFYING_SET = 'VerifyingSet'
FORBIDDENS = "ForbiddenItems"
# the real expire time set in redis key should be a bit longer
# than the score (which represent items' expiry time) in zset, so the
# verifying items can be moved to verified item list before it's infomation
# disappeared by lifetime expired
VERIFYING_EXPIRE = 2*3600  # 2 hours
VERIFYING_ZSET_SCORE = 3600
VERIFIED_EXPIRE = 24*3600   # 24 hours
EDITED_EXPIRE = 24*3600     # 24 hours
# according to user configuration
SENT_EXPIRE = int(MPConf.sameItemInterval)*3600
queryCategoryUrl = "http://zh.moegirl.org/api.php?format=json&action=query&prop=categories&titles=%s"
queryRedirectUrl = "http://zh.moegirl.org/api.php?format=json&action=query&prop=info&redirects&titles=%s"
queryIfExistUrl = "http://zh.moegirl.org/api.php?format=json&action=query&prop=info&titles=%s"