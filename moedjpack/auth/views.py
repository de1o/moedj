# -*- coding: utf-8 -*-
import logging
import redis
import pickle

from django.http import HttpResponse
from django.shortcuts import *
from django.contrib.auth.decorators import login_required

from moedjpack import qqweibo

from moedjpack.moepad.mpconf import MPConf
from moedjpack.moepad.weibowrapper import WeiboAuthInfoRedis
from moedjpack.moepad import weibo
from moedjpack.moepad.mputils import rs

log = logging.getLogger('moepad')

SinaAppKey = MPConf.SinaAppKey
SinaAppSecret = MPConf.SinaAppSecret
MoePadSite = MPConf.Domain
OriWeiboAuth = WeiboAuthInfoRedis("original")
RtWeiboAuth = WeiboAuthInfoRedis("retweet")
TencentAppKey = MPConf.TencentAppKey
TencentAppSecret = MPConf.TencentAppSecret

def authSina(code):
    client = weibo.APIClient(SinaAppKey, SinaAppSecret,
                             MoePadSite+"/sinacallback")
    r = client.request_access_token(code)
    client.set_access_token(r.access_token, r.expires_in)
    ruid = client.account.get_uid.get()
    #can get user type when callback from sina
    #so save the type in memcache, as long as
    #only on account get oauthed at a time, this works
    current_user_type = rs.get("current_user_type")
    print current_user_type
    if current_user_type == "original":
        WeiboAuthObj = OriWeiboAuth
    elif current_user_type == "retweet":
        WeiboAuthObj = RtWeiboAuth
    else:
        log.error("invalid callback user type autSina")
        raise Exception
    WeiboAuthObj.set(
        access_token=r.access_token,
        expires_in=r.expires_in,
        user_type=current_user_type, uid=ruid.uid)
    WeiboAuthObj.save()
    return r.access_token, r.expires_in


def authSinaUrl():
    client = weibo.APIClient(
        SinaAppKey, SinaAppSecret, MoePadSite+"/sinacallback")
    return client.get_authorize_url()


def authTencentUrl():
    auth = qqweibo.OAuthHandler(TencentAppKey, TencentAppSecret, callback=MoePadSite+"/tencentcallback")
    url = auth.get_authorization_url()
    f = open('tx_rt', 'wb')
    f.write(pickle.dumps(auth.request_token))
    f.close()
    return url


@login_required
def sinacallback(request):
    code = request.GET['code']
    access_token, expires_in = authSina(code)
    c = {"information": "授权信息已保存"}
    return render_to_response("info.html", c)


@login_required
def re_auth_sina(request):
    WeiboAuthObj.clean()
    return redirect(authSinaUrl())


@login_required
def re_auth_tencent(requset):
    try:
        WeiboAuth.objects.filter(source='tencent').delete()
    except:
        pass
    return redirect(authTencentUrl())


def tencentcallback(request):
    verifier = request.GET['oauth_verifier']
    auth = qqweibo.OAuthHandler(TencentAppKey, TencentAppSecret, callback=MoePadSite+"/tencentcallback")

    f = open('tx_rt', 'rb')
    auth.request_token = pickle.loads(f.read())
    f.close()
    access_token = auth.get_access_token(verifier)
    tencent_data = {
        "access_token": access_token.key,
        "secret": access_token.secret,
        "expires_in": 13000000
    }
    tencent_key = "TencentOauth"
    rs.hmset(tencent_key, tencent_data)
    rs.expire(tencent_key, tencent_data['expires_in'])

    return HttpResponse("auth info saved")


@login_required
def clean_auth(request):
    rs.delete('WeiboAuthoriginal')
    return render_to_response("info.html",
                              {'information': '授权信息已清除'})


def getWeiboAuthedApi(source, user_type):
    if user_type == "original":
        weiboData = OriWeiboAuth
    elif user_type == "retweet":
        weiboData = RtWeiboAuth
    else:
        log.error("invalid user type getWeiboAuthedApi")
        raise e

    if source == 'sina':
        client = weibo.APIClient(
            SinaAppKey, SinaAppSecret, MoePadSite+"/sinacallback")
        client.set_access_token(weiboData.access_token, weiboData.expires_in)

        return client


@login_required
def loginSina(request, user_type):
    rs.set("current_user_type", user_type)
    return redirect(authSinaUrl())


@login_required
def loginTencent(request):
    return redirect(authTencentUrl())
