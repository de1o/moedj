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
VERIFYING_EXPIRE = 3600  # 1 hours
VERIFYING_ZSET_SCORE = 1800
VERIFIED_EXPIRE = 24*3600   # 24 hours
EDITED_EXPIRE = 24*3600     # 24 hours
# according to user configuration
SENT_EXPIRE = int(MPConf.sameItemInterval)*3600
queryCategoryUrl = "http://zh.moegirl.org/api.php?format=json&action=query&prop=categories&titles=%s"
queryRedirectUrl = "http://zh.moegirl.org/api.php?format=json&action=query&prop=info&redirects&titles=%s"
queryIfExistUrl = "http://zh.moegirl.org/api.php?format=json&action=query&prop=info&titles=%s"
queryLastRevisionEditor= "http://zh.moegirl.org/api.php?format=json&action=query&prop=revisions&titles=%s"
queryWeiboId = ""
"""
{
query: {
pages: {
19312: {
pageid: 19312,
ns: 0,
title: "NTR",
revisions: [
{
revid: 238336,
parentid: 237162,
user: "肺鱼",
timestamp: "2014-04-20T13:12:26Z",
comment: "/* NTR的人们 */"
}
]
}
}
}
}
"""