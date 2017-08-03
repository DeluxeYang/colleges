#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import datetime
import traceback

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template.context import RequestContext

SIDEBAR_URL = [
    {"url": "/backend/news/", "name": "新闻列表", "active": False},
    {"url": "#", "name": "搜索新闻", "active": False,
     "drop_down": [
        {"url": "/backend/news/pick/tag/", "name": "按 标签 筛选新闻"},
        {"url": "/backend/news/pick/college/", "name": "按 院校 筛选新闻"},
     ]},
    {"url": "/backend/news/add/", "name": "添加新闻", "active": False},
]


def index(request):
    """

    :param request: 
    :return: 
    """
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render_to_response("backend/base.html", {
        "self": request.user,
        "urls": urls
        }, context_instance=RequestContext(request))


def add_news(request):
    """
    
    :param request: 
    :return: 
    """
    if request.method == "POST":
        print(request.POST)
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    return render_to_response("backend/news/add.html", {
        "self": request.user,
        "urls": urls
        }, context_instance=RequestContext(request))


def image_upload(request):
    """

    :param request: 
    :return: 
    """
    if request.method == "POST":
        print(request.POST)
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    return render_to_response("backend/news/add.html", {
        "self": request.user,
        "urls": urls
    }, context_instance=RequestContext(request))
