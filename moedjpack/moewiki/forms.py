#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Sai
# @Date:   2014-02-12 23:30:38
# @Email:  email@example.com
# @Last modified by:   Sai
# @Last modified time: 2014-03-02 20:10:33

from django import forms


class MPConfigForm(forms.Form):
    SinaAppKey = forms.CharField(label="Sina App Key:", max_length=100,
                                 required=False)
    SinaAppSecret = forms.CharField(label="Sina App Secret:", max_length=100,
                                    required=False)
    TencentAppKey = forms.CharField(label="Tencent App Key", max_length=100,
                                    required=False)
    TencentAppSecret = forms.CharField(label="Tencent App Secret",
                                       max_length=100, required=False)
    Domain = forms.CharField(label="MoePad程序所在域名 *", max_length=100)
    sameItemInterval = forms.IntegerField(label="同一条目禁止多次发送的间隔(小时) *")


class ForbiddenForm(forms.Form):
    keywords = forms.CharField(
        label="请输入屏蔽词", max_length=400,
        widget=forms.TextInput(attrs=
                               {'data-role': "tagsinput",
                                'placeholder': "输入关键词",
                                }))
