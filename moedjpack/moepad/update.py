# -*- coding: utf-8 -*-
import sys
import datetime
import requests
import json
import time
import calendar
import urllib
import urllib2
import logging
import traceback
from BeautifulSoup import BeautifulSoup

from weibowrapper import WeiboApi, WeiboAuthInfoRedis
from weibo import APIError
from mputils import rs, loggerInit, utcnow, _deletePrefix, logger
from mpconf import MPConf
from mpdefs import *


def getItemCategories(title):
    url = queryCategoryUrl % urllib.quote(title.encode('utf-8'))
    r = requests.get(url)
    rjson = json.loads(r.text)
    pages = rjson['query']['pages']
    key = pages.keys()[0]
    try:
        categories = pages[key]['categories']
    except KeyError:
        # category may not exist
        categories = []

    categories = [c['title'].partition('Category:')[2] for c in categories]
    return categories


def getImage(link):
    try:
        c = urllib2.urlopen(link)
    except:
        return None
    f = c.read()
    c.close()

    soup = BeautifulSoup(f)
    content = soup.find("div", {"id": "bodyContent"})
    img = None
    for tag in content.findAll('img'):
        try:
            if ((int(tag["width"]) < 100) or (int(tag["width"]) > 800)):
                continue
        except:
            continue
        try:
            if ((int(tag["height"]) < 100) or (int(tag["height"]) > 800)):
                continue
        except:
            continue
        img = tag
        break

    result = False
    if img:
        src = str(img["src"])
        if src.startswith("//1-ps.google"):
            src = img["pagespeed_lazy_src"]
        elif src.startswith("//"):
            src = "http:" + src

        image_remote = urllib2.urlopen(src)
        if image_remote.getcode() != 200:
            return None
        image_content = image_remote.read()
        with open("tmp.jpg", 'wb') as fpic:
            fpic.write(image_content)
        result = True
        # resize img ?
    return result


def filterForbiddenItems(that):
    forbiddenKeys = rs.smembers(FORBIDDENS)
    for key in forbiddenKeys:
        if key.decode('utf-8') in that:
            return False

    thatCategories = getItemCategories(that)
    if len(set(forbiddenKeys).intersection(set(thatCategories))):
        return False
    return True


def filterExistedItems(that):
    existedKeys = rs.keys(WIKIITEM_PREFIX+"*")
    existedItems = []
    if existedKeys:
        existedItems = rs.mget(existedKeys)
    verifyingItems = rs.zrange(VERIFYING_SET, 0, -1)
    existedItems += verifyingItems
    for item in existedItems:
        if that == item.decode('utf-8'):
            return False
    return True


def filterRedirectedItems(that):
    url = queryRedirectUrl % that.encode("utf-8")
    r = requests.get(url)
    rjson = json.loads(r.text)
    try:
        logger.info("redirected item: %s" % rjson['query']['redirects'][0]['from'].encode('utf-8'))
        return False
    except KeyError:
        return True


def verifyingKeyExpired(verifyingKey):
    expire_time = rs.zscore(VERIFYING_SET, verifyingKey)
    if not expire_time:
        logger.info("verifyingKey not in verifying keys set")
        return False

    if expire_time < time.time():
        return True
    return False


def autoVerifyExpiredItems():
    verifyingSet = rs.zrange(VERIFYING_SET, 0, -1)
    for verifyingKey in verifyingSet:
        if verifyingKeyExpired(verifyingKey):
            rs.zrem(VERIFYING_SET, verifyingKey)
            rs.set(NEWITEM+verifyingKey, verifyingKey, VERIFIED_EXPIRE)


def item_deleted(that):
    url = queryIfExistUrl % that.encode('utf-8')
    r = requests.get(url)
    rjson = json.loads(r.text)
    try:
        rjson['query']['pages']['-1']['missing']
        return True
    except KeyError:
        return False


def cleanDeletedItemsByPrefix(prefix):
    items = rs.keys(prefix+"*")
    for item in items:
        title = item.partition(prefix)[2]
        if item_deleted(title.decode('utf-8')):
            logger.info('check deleted: %s, %s' % (prefix, title))
            rs.delete(item)


def cleanDeletedItems():
    cleanDeletedItemsByPrefix(NEWITEM)
    cleanDeletedItemsByPrefix(EDITED)


def getItemTobeSend():
    cleanDeletedItems()
    new_items = rs.keys(NEWITEM+"*")
    if new_items:
        return NEWITEM, new_items[0]

    edited_items = rs.keys(EDITED+"*")
    if edited_items:
        return EDITED, edited_items[0]

    return None, None


def get_last_editor_name(item):
    url = queryLastRevisionEditor % item
    r = requests.get(url)
    rjson = json.loads(r.text)
    pages = rjson['query']['pages']
    page = pages[pages.keys()[0]]
    user_name = page['revisions'][0]['user']
    return user_name  # unicode here


def get_weibo_id_by_user_name(user_name):
    url = queryWeiboId % user_name
    r = requests.get(url)

    return "a"


class UpdateItems(object):

    filters = [
        filterForbiddenItems,
        filterExistedItems,
        filterRedirectedItems, ]

    def __init__(self, mins=20):
        super(UpdateItems, self).__init__()
        self.rch = []
        self.lastmins = mins

    def updateRoutine(self):
        try:
            self.fetchNewItemGenerated(self.lastmins)
            self.filter_valid()
            self.storeValidItems()
            autoVerifyExpiredItems()
            cleanDeletedItems()
        except:
            logger.info(traceback.format_exc())

    def fetchNewItemGenerated(self, mins):
        url_t = "http://zh.moegirl.org/api.php?format=json&action=query&list=recentchanges&rcstart=%s&rcend=%s&rcdir=newer&rcnamespace=0&rctoponly&rctype=edit|new"
        rcstart = calendar.timegm((utcnow() - datetime.timedelta(
            minutes=mins)).utctimetuple())
        rcend = calendar.timegm(utcnow().utctimetuple())
        url = url_t % (rcstart, rcend)
        print url
        r = requests.get(url)
        rjson = json.loads(r.text)
        self.rch = rjson['query']['recentchanges']
        self.new_items = [item['title'] for item in self.rch if item['type']
                          == 'new']
        self.edited_items = [item['title'] for item in self.rch if item['type']
                             != 'new']
        msg = '，'.join([item['title'].encode('utf-8') for item in self.rch])
        if msg:
            msg = ('过去%d分钟更新的条目有：' % mins)+msg
        else:
            msg = "过去%d分钟没有条目更新" % mins
        logger.info(msg)

    def filter_valid(self):
        for filterfunc in self.filters:
            self.new_items = filter(filterfunc, self.new_items)
            self.edited_items = filter(filterfunc, self.edited_items)

    def storeValidItems(self):
        for item in self.edited_items:
            itemKey = EDITED + item
            rs.set(EDITED+item, item, EDITED_EXPIRE)
            msg = "插入旧词条更新：%s" % item.encode('utf-8')
            logger.info(msg)

        for item in self.new_items:
            rs.zadd(VERIFYING_SET, item, time.time()+VERIFYING_ZSET_SCORE)
            msg = "插入新创建词条：%s" % item.encode('utf-8')
            logger.info(msg)


class SendItem(object):
    def __init__(self):
        super(SendItem, self).__init__()
        prefix, self.ItemTobeSendKey = getItemTobeSend()
        if not self.ItemTobeSendKey:
            setattr(self, 'ItemTobeSend', None)
            logger.info("No item to be send")
            return None
        self.ItemTobeSend = self.ItemTobeSendKey.partition(prefix)[2]
        self.getWeiboApi()

    def getWeiboApi(self):
        AuthInfo = WeiboAuthInfoRedis("original")
        token = rs.hgetall("WeiboAuth"+"original")
        self.weiboApi = WeiboApi(
            MPConf.SinaAppKey,
            MPConf.SinaAppSecret,
            MPConf.Domain+'/sinacallback',
            token['access_token'],
            token['expires_in'])

    def sendRoutine(self):
        if not self.ItemTobeSend:
            return None
        try:
            self.send()
            self.postsend()
            logger.info("Sending: "+self.ItemTobeSend+" Succ")
        except APIError as e:
            if 'expired_token' in e:
                logger.info("Token已到期，请重新授权")
        except:
            logger.info(traceback.format_exc())

    def send(self):
        weiboTitle = self.ItemTobeSend
        weiboLink = "http://zh.moegirl.org/" + \
                    urllib.quote(weiboTitle)
        last_editor = get_last_editor_name(self.ItemTobeSend)

        self.weiboApi.send(u'［' + weiboTitle.decode('utf-8') + u'］ 本条目最后一次编辑由' + last_editor + u'贡献',
                           weiboLink, getImage(weiboLink))

    def postsend(self):
        key = SENT + self.ItemTobeSend
        rs.set(key, self.ItemTobeSend, SENT_EXPIRE)
        rs.delete(self.ItemTobeSendKey)


def update():
    try:
        mins = int(sys.argv[1])
        updater = UpdateItems(mins)
    except:
        updater = UpdateItems()
    updater.updateRoutine()


def send():
    sender = SendItem()
    sender.sendRoutine()


def deletePrefix():
    for key in sys.argv[1:]:
        _deletePrefix(key)


if __name__ == '__main__':
    update()
    send()
