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
    {"url": "/backend/college/", "name": "院校信息", "active": False},
    {"url": "#", "name": "搜索院校", "active": False,
     "drop_down": [
        {"url": "#", "name": "按 地域 筛选院校",
         "drop_down": [
            {"url": "/backend/college/pick/area/", "name": "按 片区 筛选院校"},
            {"url": "/backend/college/pick/nation/", "name": "按 省市 筛选院校"},
         ]},
        {"url": "#", "name": "按 类型 筛选院校",
         "drop_down": [
             {"url": "/backend/college/pick/department/", "name": "按 主管部门 筛选院校"},
             {"url": "/backend/college/pick/level/", "name": "按 办学层次 筛选院校"},
             {"url": "/backend/college/pick/class/", "name": "按 办学类别 筛选院校"},
         ]},
        {"url": "#", "name": "按 类别 筛选院校", "drop_down": [
             {"url": "/backend/college/search/211/", "name": "211工程院校"},
             {"url": "/backend/college/search/985/", "name": "985工程院校"},
             {"url": "/backend/college/search/985p/", "name": "985平台院校"},
             {"url": "/backend/college/search/vice_ministry/", "name": "副部级院校"},
             {"url": "/backend/college/search/double_first/", "name": "双一流院校"},
             {"url": "/backend/college/search/cancelled/", "name": "已取消院校"},
         ]},
     ]},
    {"url": "/backend/college/add/", "name": "添加院校", "active": False},
    {"url": "/backend/college/import/", "name": "批量导入院校", "active": False},
]


def add_news(request):
    """
    
    :param request: 
    :return: 
    """
    urls = copy.deepcopy(SIDEBAR_URL)
    return render_to_response("backend/base.html", {
        "self": request.user,
        "urls": urls
        }, context_instance=RequestContext(request))
