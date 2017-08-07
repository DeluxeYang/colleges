#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import datetime
import traceback

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template.context import RequestContext

from basic.models import News, NewsAndTag, NewsComment, NewsTag

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


def news_classification(obj):
    """
    为添加新闻和修改新闻的页面渲染准备数据
    :return:
    """
    fields_dict = {"char": [], "boolean": [], "many_to_many": [], "text": [],
                   "tag": {"name": "新闻标签", "field": "tag"},
                   "nation": [{"name": "省级",  "field": "province"}, {"name": "市级",  "field": "city"}]}
    for field in News._meta.fields:  # 遍历院校数据库中每个字段
        _field = str(field).split(".")[2]
        temp = {"name": field.verbose_name,  # 字段中文名
                "field": _field,  # 字段英文名  # 某条记录的，该字段的，值
                "value": obj.get(_field, "") if obj.get(_field, "") else ""}
        if type(field).__name__ == "CharField":  # @@@第一类，字符串
            if _field == "college_id_code":
                continue
            fields_dict["char"].append(temp)  # 其他字符串数据到char下
        elif type(field).__name__ == "TextField":  # @@@第2类，布尔数据
            if _field == "abstract":
                fields_dict["text"].append(temp)
            elif _field == "content":
                fields_dict["md"] = temp
        elif type(field).__name__ == "BooleanField":  # @@@第三类，布尔数据
            fields_dict["boolean"].append(temp)
    news_and_tags = NewsAndTag.objects.filter(news_id=int(obj.get("id", 0)))
    checked_tags = {}
    for _tag in news_and_tags:
        checked_tags[_tag.tag.title] = 1
    news_tags = NewsTag.objects.all()
    fields_dict["tag"]["size"] = len(news_tags)
    for tag in news_tags:
        temp = {"title": tag.title, "id": tag.id}
        if tag.title in checked_tags:
            temp["checked"] = 1
        fields_dict["many_to_many"].append(temp)
    return fields_dict


add_news_classification = news_classification({})


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
            "fields": add_news_classification,
            "urls": urls,
            "get_colleges_by_nation_url": "/api/college/by/nation/"
        }, context_instance=RequestContext(request))


@csrf_exempt
def image_upload(request):
    """

    :param request: 
    :return: 
    """
    return_dict = {}
    if request.method == "POST":
        print(request.POST)
        return_dict["success"] = 1
        return_dict["url"] = "/a/"
        return_dict["message"] = ""
    return HttpResponse(json.dumps(return_dict))

