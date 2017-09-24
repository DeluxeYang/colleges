#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import datetime
import traceback

from django.db import connection
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from basic.models import *
from basic.views import Table
from basic.utils import excel_loader
from basic.utils.logger import logger

SIDEBAR_URL = [
    {"url": "/backend/ranking/", "name": "人才榜单分类列表", "active": False},
    {"url": "/backend/rankings/", "name": "人才榜单批次列表", "active": False},
    {"url": "#", "name": "搜索人才榜单", "active": False,
     "drop_down": [
        {"url": "/backend/rankings/search/college/", "name": "按相关院校搜索", "active": False},
     ]},
    {"url": "/backend/ranking/add/", "name": "添加人才榜单", "active": False},
]


def index(request):
    """

    :return:
    """
    model_fields = ["#", "人才榜单名  (点击查看该榜单各批次)", "榜单字段", "创建时间", "由excel导入数据", "删除"]
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render_to_response("backend/list.html", {
        "self": request.user,
        "urls": urls,
        "fields": model_fields,
        "title": "人才榜单分类列表",
        "delete_url": "/backend/professor/delete/",
        "batch_delete_url": "/backend/professor/batch_delete/",
        "get_all_data_url": "/backend/professor/retrieve/"
    }, context_instance=RequestContext(request))


def format_professor(data):
    """
    格式化列表
    :return: json
    """
    return_dict = {"data": []}
    i = 1
    for _data in data:
        return_dict["data"].append([
            '<label>' + str(i) + '<input value="' + str(_data.id) +
            '" name="news_checkbox" type="checkbox"/></label>',
            "<a href='/backend/professors/" + str(_data.id) + "/'>" + _data.name_cn + "</a>",
            "<a href='/backend/professor/" + str(_data.id) + "/'>查看字段</a>",
            _data.create_time.strftime("%Y-%m-%d"),
            "<a href='/backend/professor/import/" + str(_data.id) + "/'>导入数据</a>",
            "<a id='row_" + str(_data.id) +
            "' href='javascript:href_ajax(" + str(_data.id) + ")'" +
            " onclick=\"return confirm('确认删除" + _data.name_cn + "？')\">删除</a>"])
        i += 1
    return return_dict


def retrieve_professor(request):
    """
    获取所有信息
    :return: json
    """
    _professor = Table.get_tables_by_type_id(2)
    return_dict = format_professor(_professor)  # 格式化信息
    return HttpResponse(json.dumps(return_dict))
