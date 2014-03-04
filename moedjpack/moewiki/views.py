# -*- coding: utf-8 -*-
import feedparser
import datetime
import logging
import redis
import json

from django.http import HttpResponse, Http404
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm

from forms import MPConfigForm, ForbiddenForm
from moedjpack.moepad.mputils import rs
from moedjpack.moepad.mpdefs import *

log = logging.getLogger('moepad')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # new user created
            return HttpResponseRedirect("/accounts/login/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html",
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def index(request):
    if request.method == 'POST':
        form = MPConfigForm(request.POST)
        if form.is_valid():
            rs.hmset("MoePadConf", request.POST)
        return render(request, "index.html", {"form": form})
    else:
        data = rs.hgetall("MoePadConf")
        form = MPConfigForm(initial=data)
        return render(request, "index.html", {"form": form})


@login_required
def forbidden_proc(request):
    if request.method == 'POST':
        forbidden_keywords = request.POST['keywords'].split(',')
        forbidden_keywords = set(forbidden_keywords).remove("")
        for keyword in forbidden_keywords:
            rs.sadd(FORBIDDENS, keyword)
    form = ForbiddenForm()
    forbidden_keywords = rs.smembers(FORBIDDENS)
    return render(request, "forbidden.html",
                  {"form": form, "forbiddens": forbidden_keywords})


@csrf_exempt
@login_required
def forbidden_item(request, item):
    if request.method == "DELETE":
        try:
            rs.srem(FORBIDDENS, item)
            status = 'ok'
        except:
            status = 'error'
    else:
        status = 'not implement'
    return HttpResponse(json.dumps({"status": status}),
                        content_type="application/json")


# def verify(request):
#     if request.method == 'POST':
#         print request.POST
#         for key in request.POST.keys():
#             if 'on' in request.POST[key]:
#                 RecentUpdateItems.objects.filter(title=key).update(
#                     itemState=RecentUpdateItems.VERIFIED)

#         return generateUnverifiedPage(request)
#     else:
#         return generateUnverifiedPage(request)


# def generateUnverifiedPage(request):
#     unverified_items_rec = RecentUpdateItems.objects.filter(
#         itemState=RecentUpdateItems.VERIFYING_NEW)
#     unverified_items = [rec.title.encode('utf-8')
#                         for rec in unverified_items_rec]
#     c = RequestContext(request, {"unverified_items": unverified_items})
#     return render_to_response('verify.html', c)
