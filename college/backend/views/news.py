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

from basic.utils.logger import logger
from basic.models import News, NewsAndTag, NewsComment, NewsTag, NewsAndCollege
from basic.views.News import get_news_by_id, create_news, update_news

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
                   "tag": {"name": "新闻标签", "field": "tag"}, "college": [],
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
        elif type(field).__name__ == "BooleanField":  # @@@第三类，布尔数据
            print(_field, temp["value"])
            temp["value"] = "checked" if temp["value"] else ""
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
    news_and_colleges = NewsAndCollege.objects.filter(news_id=int(obj.get("id", 0)))
    for nac in news_and_colleges:
        fields_dict["college"].append({"name_cn": nac.college.name_cn, "id": nac.college.id})
    fields_dict["md_doc"] = obj.get("md_doc", "") if obj.get("md_doc", "") else ""
    return fields_dict


add_news_classification = news_classification({})


def add_news(request):
    """
    
    :param request: 
    :return: 
    """
    if request.method == "POST":
        try:
            news = {"user": request.user,
                    "title": request.POST["title"],
                    "keywords": request.POST["keywords"],
                    "abstract": request.POST["abstract"],
                    "md_doc": request.POST["test-editormd-markdown-doc"],
                    "html_code": request.POST["test-editormd-html-code"],
                    "is_published": True if "is_published" in request.POST else False,
                    "is_allow_comments": True if "is_allow_comments" in request.POST else False,
                    "is_stick_top": True if "is_stick_top" in request.POST else False,
                    "is_bold": True if "is_bold" in request.POST else False}
            colleges = request.POST["colleges"].split(",") if request.POST["colleges"] != '' else []
            tags = request.POST["tags"].split(",") if request.POST["tags"] != '' else []
            _news = create_news(news, tags, colleges)
            messages.success(request, "添加新闻成功")
            return HttpResponseRedirect("/backend/news/modify/"+str(_news.id)+"/")
        except Exception as e:
            logger.error(str(e))
            messages.error(request, "添加新闻失败")
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    return render_to_response("backend/news/add.html", {
            "self": request.user,
            "fields": add_news_classification,
            "urls": urls,
            "get_colleges_by_nation_url": "/api/college/by/nation/",
            "news_image_upload_url": "/api/news/image_upload/"
        }, context_instance=RequestContext(request))


def modify_news(request, news_id):
    """

    :return:
    """
    news = get_news_by_id(news_id)
    if request.method == "POST":
        try:
            news = {"user": request.user,
                    "title": request.POST["title"],
                    "keywords": request.POST["keywords"],
                    "abstract": request.POST["abstract"],
                    "md_doc": request.POST["test-editormd-markdown-doc"],
                    "html_code": request.POST["test-editormd-html-code"],
                    "is_published": True if "is_published" in request.POST else False,
                    "is_allow_comments": True if "is_allow_comments" in request.POST else False,
                    "is_stick_top": True if "is_stick_top" in request.POST else False,
                    "is_bold": True if "is_bold" in request.POST else False}
            colleges = request.POST["colleges"].split(",") if request.POST["colleges"] != '' else []
            tags = request.POST["tags"].split(",") if request.POST["tags"] != '' else []
            update_news(news, tags, colleges)
            messages.success(request, "修改新闻成功")
        except Exception as e:
            logger.error(str(e))
            messages.error(request, "修改新闻失败")
    modify_news_classification = news_classification(news.__dict__)
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    return render_to_response("backend/news/modify.html", {
        "self": request.user,
        "fields": modify_news_classification,
        "urls": urls,
        "get_colleges_by_nation_url": "/api/college/by/nation/",
        "news_image_upload_url": "/api/news/image_upload/"
    }, context_instance=RequestContext(request))
