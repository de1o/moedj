#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: delo
# @Date:   2014-02-18 00:12:46
# @Email:  deloeating@gmail.com
# @Last modified by:   delo
# @Last modified time: 2014-02-19 23:44:23
import weibo
from mputils import sub_dict, rs


class WeiboApi(object):

    def __init__(self, appkey, appsecret, callback, token, expires_in):
        super(WeiboApi, self).__init__()
        self.client = weibo.APIClient(appkey, appsecret, callback)
        self.client.set_access_token(token, expires_in)

    def send(self, text, url, img=None):
        short_link = self.client.short_url__shorten(url_long=url)
        shortUrl = short_link["urls"][0]["url_short"]
        text = ' '.join([text, shortUrl])

        if img:
            with open('tmp.jpg', 'rb') as fpic:
                r = self.client.statuses.upload.post(status=text, pic=fpic)
        else:
            r = self.client.statuses.update.post(status=text)


class WeiboAuthInfo(object):
    def __init__(self, user_type):
        super(WeiboAuthInfo, self).__init__()
        args = locals()
        args.pop("self")
        for key in args.keys():
            setattr(self, key, args[key])

    def set(self, access_token, expires_in, user_type, uid):
        args = locals()
        args.pop("self")
        for key in args.keys():
            setattr(self, key, args[key])

    def load():
        pass

    def save(self):
        pass

    def clean(self):
        pass


class WeiboAuthInfoRedis(WeiboAuthInfo):
    def __init__(self, user_type):
        super(WeiboAuthInfoRedis, self).__init__(user_type)
        self.mckey = "WeiboAuth" + user_type

    def load(self):
        args = rs.get(self.mckey)
        if args:
            for key in args.keys():
                setattr(self, key, args[key])

    def save(self):
        print self.__dict__
        confs = sub_dict(self.__dict__,
                         ['uid', 'access_token', 'expires_in', 'user_type'])
        rs.hmset(self.mckey, confs)
        rs.expire(self.mckey, confs['expires_in'])

    def clean(self):
        rs.hdel(self.mckey)
