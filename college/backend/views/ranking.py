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
    {"url": "/backend/ranking/", "name": "榜单分类列表", "active": False},
    {"url": "/backend/rankings/", "name": "榜单详细列表", "active": False},
    {"url": "/backend/ranking/add/", "name": "添加榜单", "active": False},
]


def index(request):
    """

    :return:
    """
    model_fields = ["#", "榜单名", "创建时间", "删除"]
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render_to_response("backend/ranking/list.html", {
        "self": request.user,
        "urls": urls,
        "fields": model_fields,
        "ranking_delete_url": "/backend/ranking/delete/",
        "ranking_batch_delete_url": "/backend/ranking/batch_delete/",
        "get_all_ranking_url": "/backend/ranking/retrieve/"
    }, context_instance=RequestContext(request))


def format_ranking(ranking):
    """
    格式化新闻列表
    :return: json
    """
    return_dict = {"data": []}
    i = 1
    for _ranking in ranking:
        return_dict["data"].append([
            '<label>' + str(i) + '<input value="' + str(_ranking.id) +
            '" name="news_checkbox" type="checkbox"/></label>',
            "<a href='/backend/ranking/" + str(_ranking.id) + "/'>" + _ranking.name_cn + "</a>",
            _ranking.create_time.strftime("%Y-%m-%d"),
            "<a id='row_" + str(_ranking.id) +
            "' href='javascript:href_ajax(" + str(_ranking.id) + ")'" +
            " onclick=\"return confirm('确认删除" + _ranking.name_cn + "？')\">删除</a>"])
        i += 1
    return return_dict


def retrieve_ranking(request):
    """
    获取所有院校信息
    :return: json
    """
    _ranking = Table.get_all_tables()
    return_dict = format_ranking(_ranking)  # 格式化院校信息
    logger.info("数据库访问次数: "+str(len(connection.queries)))
    return HttpResponse(json.dumps(return_dict))


def add_ranking(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            _table = {"table_name_cn": request.POST["table_name_cn"],
                      "table_type": 1}  # 榜单
            i = 0
            _fields = []
            field_types = request.POST.getlist("field_type")
            field_names_cn = request.POST.getlist("field_name_cn")
            while i < len(field_types):
                _fields.append({"field_type": int(field_types[i]),
                                "field_name_cn": field_names_cn[i]})
                i += 1
            table_id = Table.create_table(_table, _fields)
            if table_id:
                return HttpResponseRedirect("/backend/ranking/"+str(table_id)+"/")
            else:
                raise Exception("添加榜单失败")
        except Exception as e:
            logger.error(str(e))
            messages.error(request, "添加榜单失败")
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    field_types = TypeOfField.objects.all()
    return render_to_response("backend/ranking/add.html", {
        "self": request.user,
        "field_types": field_types,
        "urls": urls,
    }, context_instance=RequestContext(request))


def get_ranking(request, ranking_id):
    """

    :return:
    """
    ranking = Table.get_table_by_id(int(ranking_id))
    fields = Table.get_fields_by_table_id(int(ranking_id))
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render_to_response("backend/ranking/ranking.html", {
        "self": request.user,
        "ranking": ranking,
        "fields": fields,
        "urls": urls,
    }, context_instance=RequestContext(request))


def batch_delete_ranking(request):
    """
    批量删除院校
    :param request:
    :return:
    """
    return_dict = {}
    try:
        delete_list = request.POST.getlist("ranking_ids[]")
        for i in delete_list:
            Table.drop_table(int(i))
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return HttpResponse(json.dumps(return_dict))


def delete_ranking(request):
    """
    删除一所院校
    :param request:
    :return:
    """
    return_dict = {}
    try:
        Table.drop_table(int(request.POST["ranking_id"]))
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return HttpResponse(json.dumps(return_dict))