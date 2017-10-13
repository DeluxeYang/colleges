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
from basic.utils import common
from basic.utils import excel_loader
from basic.utils.logger import logger
from backend.views.ranking import empty_is_empty_str, create_rankings_and_college_relations

SIDEBAR_URL = [
    {"url": "/backend/professor/", "name": "人才榜单分类列表", "active": False},
    {"url": "/backend/professors/", "name": "人才榜单批次列表", "active": False},
    {"url": "#", "name": "搜索人才榜单", "active": False,
     "drop_down": [
        {"url": "/backend/professors/search/college/", "name": "按相关院校搜索", "active": False},
     ]},
    {"url": "/backend/professor/add/", "name": "添加人才榜单", "active": False},
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


def format_professor(data, page, size):
    """
    格式化列表
    :return: json
    """
    return_dict = {"data": []}
    i = (page - 1) * size + 1
    for _data in data:
        return_dict["data"].append([
            '<label>' + str(i) + '<input value="' + str(_data.id) +
            '" name="_checkbox" type="checkbox"/></label>',
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
    page = request.GET.get("page", 1)
    size = request.GET.get("size", 200)
    content, num_pages = common.with_paginator(_professor, int(page), int(size))
    return_dict = format_professor(content, int(page), int(size))  # 格式化院校信息
    return_dict["num_pages"] = num_pages
    return HttpResponse(json.dumps(return_dict))


def add_professor_ranking(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            _table = {"table_name_cn": request.POST["table_name_cn"],
                      "table_type": 2}  # 人才榜单
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
                return HttpResponseRedirect("/backend/professor/"+str(table_id)+"/")
            else:
                raise Exception("Add Professor Ranking Failed")
        except Exception as e:
            logger.error(str(e))
            messages.error(request, "添加榜单失败")
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[3]["active"] = True
    field_types = TypeOfField.objects.all()
    return render_to_response("backend/ranking/add.html", {
        "self": request.user,
        "field_types": field_types,
        "urls": urls,
        "title": "人才"
    }, context_instance=RequestContext(request))


def get_professor_ranking(request, professor_id):
    """

    :return:
    """
    ranking = Table.get_table_by_id(int(professor_id))
    fields = Table.get_fields_by_table_id(int(professor_id))
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render_to_response("backend/ranking/ranking.html", {
        "self": request.user,
        "ranking": ranking,
        "fields": fields,
        "urls": urls,
    }, context_instance=RequestContext(request))


def batch_delete_professor_ranking(request):
    """
    批量删除
    :param request:
    :return:
    """
    return_dict = {}
    try:
        delete_list = request.POST.getlist("_ids[]")
        for i in delete_list:
            Table.drop_table(int(i))
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return HttpResponse(json.dumps(return_dict))


def delete_professor_ranking(request):
    """
    删除一所
    :param request:
    :return:
    """
    return_dict = {}
    try:
        Table.drop_table(int(request.POST["_id"]))
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return HttpResponse(json.dumps(return_dict))


def professors_index(request, professor_id=""):
    """

    :return:
    """
    model_fields = ["#", "人才榜单名", "批次", "创建时间", "删除"]
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[1]["active"] = True
    if professor_id != "":
        professor_id += "/"
        if "search_by_college" in request.GET:
            professor_id += "?search_by_college=true"
    return render_to_response("backend/list.html", {
        "self": request.user,
        "urls": urls,
        "fields": model_fields,
        "title": "人才榜单批次列表",
        "delete_url": "/backend/professors/delete/",
        "batch_delete_url": "/backend/professors/batch_delete/",
        "get_all_data_url": "/backend/professors/retrieve/"+professor_id
    }, context_instance=RequestContext(request))


def format_professors(batches, page, size):
    """
    格式化列表
    :return: json
    """
    return_dict = {"data": []}
    i = (page - 1) * size + 1
    for batch in batches:
        return_dict["data"].append([
            '<label>' + str(i) + '<input value="' + str(batch.id) +
            '" name="_checkbox" type="checkbox"/></label>',
            "<a href='/backend/professors/content/" + str(batch.id) + "/'>" + str(batch.table.name_cn) + "</a>",
            str(batch.batch.text),
            batch.create_time.strftime("%Y-%m-%d"),
            "<a id='row_" + str(batch.id) +
            "' href='javascript:href_ajax(" + str(batch.id) + ")'" +
            " onclick=\"return confirm('确认删除" + str(batch.table.name_cn)
            + "_" + str(batch.batch.text) + "？')\">删除</a>"])
        i += 1
    return return_dict


def retrieve_professors(request, professor_id=""):
    """
    获取所有信息
    :return: json
    """
    if professor_id == "":
        batches = BatchOfTable.objects.filter(type=2)
    elif "search_by_college" in request.GET:  # 此时的professor_id为college id
        relations = BatchAndCollegeRelation.objects.filter(type=2).filter(college_id=int(professor_id))
        batches = []
        no_repeat = {}
        for r in relations:
            if r.batch.id not in no_repeat:
                no_repeat[r.batch.id] = 1
                batches.append(r.batch)
    else:
        _professor = Table.get_table_by_id(int(professor_id))
        batches = BatchOfTable.objects.filter(table=_professor)
    page = request.GET.get("page", 1)
    size = request.GET.get("size", 200)
    content, num_pages = common.with_paginator(batches, int(page), int(size))
    return_dict = format_professors(content, int(page), int(size))  # 格式化院校信息
    return_dict["num_pages"] = num_pages
    return HttpResponse(json.dumps(return_dict))


def batch_delete_professors(request):
    """
    批量删除
    :return:
    """
    return_dict = {}
    try:
        delete_list = request.POST.getlist("_ids[]")
        batches = BatchOfTable.objects.filter(id__in=delete_list)
        _fields = ["batch"]
        _args = []
        last_table_name = batches[0].table.name
        for _batch in batches:
            _args.append((_batch.batch.text.encode('utf-8'), ))  # 批次入list
            table_name = _batch.table.name  # 该记录的榜单名
            if table_name != last_table_name:  # 如果与上一个榜单名不同，则提交一次
                Table.table_record_delete(last_table_name, _fields, _args)  # 把之前的提交了
                last_table_name = table_name  # 更新上一次榜单名
                _args = []  # 批次重置
        Table.table_record_delete(last_table_name, _fields, _args)
        batches.delete()
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return HttpResponse(json.dumps(return_dict))


def delete_professors(request):
    """
    删除一所
    :return:
    """
    return_dict = {}
    try:
        delete_batch = int(request.POST["_id"])
        batch = BatchOfTable.objects.get(id=delete_batch)
        _args = [(batch.batch.text.encode('utf-8',))]
        _fields = ["batch"]
        Table.table_record_delete(batch.table.name, _fields, _args)
        batch.delete()
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return HttpResponse(json.dumps(return_dict))


def import_professor(request, professor_id):
    """

    :return:
    """
    if request.method == "POST":
        return_dict = {}
        try:
            _file = request.FILES.get("file_upload")  # 上传的文件
            wb = excel_loader.load_excel(_file)  # 读取excel
            body = excel_loader.get_excel_body_generator(wb)
            batch = request.POST["extra"]
            # 先匹配批次
            if batch == "0":
                _batch = YearSeasonMonth.objects.get(type=0)
            else:
                temp_batch = batch.split("-")
                year = temp_batch[1]
                if temp_batch[0] == "2":
                    _batch = YearSeasonMonth.objects.get(year=int(year), season=int(temp_batch[2]), type=2)
                elif temp_batch[0] == "3":
                    _batch = YearSeasonMonth.objects.get(year=int(year), month=int(temp_batch[2]), type=3)
                else:
                    _batch = YearSeasonMonth.objects.get(year=int(year), type=1)
            _ranking = Table.get_table_by_id(int(professor_id))
            # 如果已有该批次，则失败
            if BatchOfTable.objects.filter(batch=_batch, table=_ranking).exists():
                raise IntegrityError(str(_ranking)+str(_batch))
            args = []
            # 分别处理每行数据
            for record in body:
                temp_list = [_batch.text.encode('utf-8')]
                for r in record:
                    r = empty_is_empty_str(r)
                    temp_list.append(r.encode('utf-8'))
                args.append(tuple(temp_list))
            fields = ["batch"]  # 在field中首先添加一个"batch"，其余的fields由下面这个函数添加
            Table.insert_table(int(professor_id), fields, args)  # 导入到表
            batch = BatchOfTable.objects.create(batch=_batch,  # 导入成功，才添加batch
                                                table=_ranking,
                                                name_cn=str(_ranking.name_cn) + "_" + str(_batch.text))
            create_rankings_and_college_relations(_file, batch)  # 建立榜单与学校的关系
            return_dict["success"] = "success"
        except IndexError as e:
            logger.error(str(e))
            return_dict["error"] = "请选择批次"
        except IntegrityError as e:  # 仅处理重复添加错误
            logger.error(str(e))
            return_dict["error"] = "批次重复"
        except Exception as e:
            logger.error(str(e))
            logger.error(traceback.format_exc())
            return_dict["error"] = "出现错误，请检查文件及内容格式"
        finally:
            return HttpResponse(json.dumps(return_dict))
    year = YearSeasonMonth.objects.filter(type=1)
    _ranking = Table.get_table_by_id(int(professor_id))
    _fields = Table.get_fields_by_table_id(int(professor_id))
    fields = [str(f.name_cn)+"("+str(f.type)+")" for f in _fields]
    urls = copy.deepcopy(SIDEBAR_URL)  # 侧边栏网址
    urls[0]["active"] = True
    return render_to_response("backend/ranking/import.html", {
        "self": request.user,
        "fields": fields,
        "ranking": _ranking,
        "year": year,
        "urls": urls,
        "file_upload_url": "/backend/professor/import/"+str(professor_id)+"/",
    }, context_instance=RequestContext(request))


def professors_content_index(request, batch_id):
    """

    :return:
    """
    batch = BatchOfTable.objects.get(id=int(batch_id))
    ranking_fields = Table.get_fields_by_table_id(int(batch.table.id))
    model_fields = ["#"]
    for field in ranking_fields:
        model_fields.append(field.name_cn)
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[1]["active"] = True
    return render_to_response("backend/ranking/ranking_content.html", {
        "self": request.user,
        "urls": urls,
        "fields": model_fields,
        "title": str(batch.table.name_cn)+"（批次："+str(batch.batch.text)+"）",
        "get_all_ranking_url": "/backend/professors/content/retrieve/" + str(batch_id) + "/"
    }, context_instance=RequestContext(request))


def format_professors_content(professor_id, res):
    """
    格式化列表
    :return: json
    """
    ranking_fields = Table.get_fields_by_table_id(int(professor_id))
    _fields = []
    for filed in ranking_fields:
        _fields.append(filed.name)
    return_dict = {"data": []}
    i = 1
    for r in res:
        temp = ['<label>' + str(i) + '</label>']
        for f in _fields:
            temp.append(r[f])
        return_dict["data"].append(temp)
        i += 1
    return return_dict


def retrieve_professors_content(request, batch_id):
    """
    获取所有信息
    :return: json
    """
    batch = BatchOfTable.objects.get(id=int(batch_id))  # 获取批次
    fields = ["batch"]
    args = [batch.batch.text.encode('utf-8')]
    res = Table.read_table_content_by_batch(batch.table.name, fields, args)
    return_dict = format_professors_content(batch.table.id, res)  # 格式化院校信息
    return HttpResponse(json.dumps(return_dict))


def professors_search_pick(request):
    """
    筛选院校
    :return:
    """
    model_fields = {"many_to_many": []}
    if request.method == "POST":
        return HttpResponseRedirect("/backend/professors/" + request.POST["college"] + "/?search_by_college=true")
    model_fields["nation"] = [{"name": "所在地（省级）", "field": "province"},
                              {"name": "所在地（市级）", "field": "city"}]
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    return render_to_response("backend/ranking/pick.html",
                              {
                                  "self": request.user,
                                  "fields": model_fields,
                                  "urls": urls,
                                  "get_colleges_by_nation_url": "/api/college/by/nation/",
                              },
                              context_instance=RequestContext(request))
