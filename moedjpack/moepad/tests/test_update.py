#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: delo
# @Date:   2014-02-17 23:12:19
# @Email:  deloeating@gmail.com
# @Last modified by:   Sai
# @Last modified time: 2014-03-02 15:36:07
import time


import moedjpack.moepad.update as update
from moedjpack.moepad.mputils import rs, logger, _deletePrefix
from moedjpack.moepad.mpdefs import *


def test_getItemCategories():
    possible_categories = ['R-18', 'R18']
    real_categories = update.getItemCategories(u'Ahe颜')
    assert len(set(possible_categories).intersection(set(real_categories)))

    real_categories = update.getItemCategories(u'神原骏河')
    logger.info(str(type(real_categories[0])))
    assert u"物语系列" in real_categories


def test_filterForbiddenItems():
    rs.sadd(FORBIDDENS, u"神原骏河".encode('utf-8'))
    rs.sadd(FORBIDDENS, u"R18".encode('utf-8'))
    rs.sadd(FORBIDDENS, u"R-18".encode('utf-8'))

    assert not update.filterForbiddenItems(u"Ahe颜")
    assert not update.filterForbiddenItems(u'援助交际')
    assert not update.filterForbiddenItems(u"神原骏河")
    assert update.filterForbiddenItems(u"猫物语")

    rs.srem(FORBIDDENS, u"神原骏河".encode('utf-8'))
    rs.srem(FORBIDDENS, u"R18".encode('utf-8'))
    rs.srem(FORBIDDENS, u"R-18".encode('utf-8'))


def test_filterRedirectedItems():
    assert not update.filterRedirectedItems(u"百合(消歧义)")
    assert update.filterRedirectedItems(u"NTR")


def test_filterExistedItems():
    _deletePrefix(NEWITEM)
    _deletePrefix(EDITED)
    rs.delete(VERIFYING_SET)


    rs.set(NEWITEM+"newitem", "newitem")
    rs.set(EDITED+"edited", "edited")
    rs.zadd(VERIFYING_SET, "verifying", 1)

    assert not update.filterExistedItems("newitem")
    assert not update.filterExistedItems("edited")
    assert not update.filterExistedItems("verifying")
    assert update.filterExistedItems("shouldnotexisted")

    rs.delete(NEWITEM+"newitem")
    rs.delete(EDITED+"edited")
    rs.zrem(VERIFYING_SET, "verifying")


def test_autoVerifyExpiredItems():
    curtime = time.time()
    expired_time = curtime
    future_time = curtime + 120

    rs.zadd(VERIFYING_SET, "expired", curtime)
    rs.zadd(VERIFYING_SET, "future_item", future_time)

    assert rs.zscore(VERIFYING_SET, "expired") == curtime

    update.autoVerifyExpiredItems()

    assert not rs.zscore(VERIFYING_SET, "expired")
    assert rs.zscore(VERIFYING_SET, "future_item") == future_time
    assert rs.get(NEWITEM+"expired") == "expired"

    rs.zrem(VERIFYING_SET, "future_item")
    rs.delete(NEWITEM+"expired")


def test_verifyingKeyExpired():
    expired_time = time.time()
    future_time = expired_time + 120
    assert not update.verifyingKeyExpired("shouldnotexisted")

    rs.zadd(VERIFYING_SET, "expired", expired_time)
    rs.zadd(VERIFYING_SET, "future_item", future_time)

    assert update.verifyingKeyExpired("expired")
    assert not update.verifyingKeyExpired("future_item")

    rs.zrem(VERIFYING_SET, "expired")
    rs.zrem(VERIFYING_SET, "future_item")


def test_getItemTobeSend():
    # 0. test no item exist in either side
    _deletePrefix(EDITED)
    _deletePrefix(NEWITEM)
    result = update.getItemTobeSend()
    assert not (result[1])

    # 1. test when new items not exist, edited item exist
    rs.set(EDITED+"百合", "百合")
    rs.set(EDITED+"佐天泪子", "佐天泪子")
    assert update.getItemTobeSend()[1] in [EDITED+"百合", EDITED+"佐天泪子"]

    # 2. test when new items exist but is deleted
    rs.set(NEWITEM+"newitem1", "newitem1")
    rs.set(NEWITEM+"newitem2", "newitem2")
    assert update.getItemTobeSend()[1] in [EDITED+"佐天泪子", EDITED+"百合"]

    # 3. test when new items existed and existed in mb web pages
    rs.set(NEWITEM+"NTR", "NTR")
    rs.set(NEWITEM+"百合", "百合")
    assert update.getItemTobeSend()[1] in [NEWITEM+"NTR", NEWITEM+"百合"]

    _deletePrefix(EDITED)
    _deletePrefix(NEWITEM)


def test_item_deleted():
    assert update.item_deleted("gjlsjirjl")
    assert not update.item_deleted("NTR")


def test_cleanDeletedNewItems():
    rs.set(NEWITEM+"NotExisted", "fjslfs")
    rs.set(NEWITEM+"NTR", "BTR")
    rs.set(NEWITEM+"百合", "百合")

    update.cleanDeletedItemsByPrefix(NEWITEM)

    assert rs.get(NEWITEM+"NTR")
    assert rs.get(NEWITEM+"百合")
    assert not rs.get(NEWITEM+"NotExisted")

    _deletePrefix(NEWITEM)


def test_cleanDeletedEditedItems():
    rs.set(EDITED+"NotExisted", "fjslfs")
    rs.set(EDITED+"NTR", "BTR")
    rs.set(EDITED+"百合", "百合")

    update.cleanDeletedItemsByPrefix(EDITED)

    assert rs.get(EDITED+"NTR")
    assert rs.get(EDITED+"百合")
    assert not rs.get(EDITED+"NotExisted")


def test_get_last_editor_name():
    assert u"Wyjroshan" == update.get_last_editor_name("义妹")


