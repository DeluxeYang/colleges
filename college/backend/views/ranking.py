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
    {"url": "#", "name": "搜索榜单", "active": False,
     "drop_down": [
        {"url": "/backend/rankings/search/college/", "name": "按相关院校搜索", "active": False},
     ]},
    {"url": "/backend/ranking/add/", "name": "添加榜单", "active": False},
]


def index(request):
    """

    :return:
    """
    model_fields = ["#", "榜单名  (点击查看该榜单各批次)", "榜单字段", "创建时间", "由excel导入数据", "删除"]
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
    格式化列表
    :return: json
    """
    return_dict = {"data": []}
    i = 1
    for _ranking in ranking:
        return_dict["data"].append([
            '<label>' + str(i) + '<input value="' + str(_ranking.id) +
            '" name="news_checkbox" type="checkbox"/></label>',
            "<a href='/backend/rankings/" + str(_ranking.id) + "/'>" + _ranking.name_cn + "</a>",
            "<a href='/backend/ranking/" + str(_ranking.id) + "/'>查看字段</a>",
            _ranking.create_time.strftime("%Y-%m-%d"),
            "<a href='/backend/ranking/import/" + str(_ranking.id) + "/'>导入数据</a>",
            "<a id='row_" + str(_ranking.id) +
            "' href='javascript:href_ajax(" + str(_ranking.id) + ")'" +
            " onclick=\"return confirm('确认删除" + _ranking.name_cn + "？')\">删除</a>"])
        i += 1
    return return_dict


def retrieve_ranking(request):
    """
    获取所有信息
    :return: json
    """
    _ranking = Table.get_all_tables()
    return_dict = format_ranking(_ranking)  # 格式化院校信息
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
                raise Exception("Add Ranking Failed")
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
    批量删除
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
    删除一所
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


def rankings_index(request, ranking_id=""):
    """

    :return:
    """
    model_fields = ["#", "榜单名", "批次", "创建时间", "删除"]
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[1]["active"] = True
    if ranking_id != "":
        ranking_id += "/"
        if "search_by_college" in request.GET:
            ranking_id += "?search_by_college=true"
    return render_to_response("backend/ranking/list.html", {
        "self": request.user,
        "urls": urls,
        "fields": model_fields,
        "ranking_delete_url": "/backend/rankings/delete/",
        "ranking_batch_delete_url": "/backend/rankings/batch_delete/",
        "get_all_ranking_url": "/backend/rankings/retrieve/"+ranking_id
    }, context_instance=RequestContext(request))


def format_rankings(batches):
    """
    格式化列表
    :return: json
    """
    return_dict = {"data": []}
    i = 1
    for batch in batches:
        return_dict["data"].append([
            '<label>' + str(i) + '<input value="' + str(batch.id) +
            '" name="news_checkbox" type="checkbox"/></label>',
            "<a href='/backend/rankings/content/" + str(batch.id) + "/'>" + str(batch.table.name_cn) + "</a>",
            str(batch.batch.text),
            batch.create_time.strftime("%Y-%m-%d"),
            "<a id='row_" + str(batch.id) +
            "' href='javascript:href_ajax(" + str(batch.id) + ")'" +
            " onclick=\"return confirm('确认删除" + str(batch.table.name_cn)
            + "_" + str(batch.batch.text) + "？')\">删除</a>"])
        i += 1
    return return_dict


def retrieve_rankings(request, ranking_id=""):
    """
    获取所有信息
    :return: json
    """
    if ranking_id == "":
        batches = BatchOfTable.objects.all()
    elif "search_by_college" in request.GET:  # 此时的ranking_id为college id
        relations = BatchAndCollegeRelation.objects.filter(college_id=int(ranking_id))
        batches = []
        for r in relations:
            batches.append(r.batch)
    else:
        _ranking = Table.get_table_by_id(int(ranking_id))
        batches = BatchOfTable.objects.filter(table=_ranking)
    return_dict = format_rankings(batches)  # 格式化院校信息
    return HttpResponse(json.dumps(return_dict))


def batch_delete_ranking_batches(request):
    """
    批量删除
    :return:
    """
    return_dict = {}
    try:
        delete_list = request.POST.getlist("ranking_ids[]")
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


def delete_rankings(request):
    """
    删除一所
    :return:
    """
    return_dict = {}
    try:
        delete_batch = int(request.POST["ranking_id"])
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


def import_ranking(request, ranking_id):
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
            _ranking = Table.get_table_by_id(int(ranking_id))
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
            Table.insert_table(int(ranking_id), fields, args)  # 导入到表
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
    _ranking = Table.get_table_by_id(int(ranking_id))
    _fields = Table.get_fields_by_table_id(int(ranking_id))
    fields = [str(f.name_cn)+"("+str(f.type)+")" for f in _fields]
    urls = copy.deepcopy(SIDEBAR_URL)  # 侧边栏网址
    urls[0]["active"] = True
    return render_to_response("backend/ranking/import.html", {
        "self": request.user,
        "fields": fields,
        "ranking": _ranking,
        "year": year,
        "urls": urls,
        "file_upload_url": "/backend/ranking/import/"+str(ranking_id)+"/",
    }, context_instance=RequestContext(request))


def empty_is_empty_str(content):
    """
    如果excel里为空，则会返回“None”，所以再转换为空
    :param content:
    :return:
    """
    return content if content != "None" else ""


def create_rankings_and_college_relations(excel, batch):
    """
    读取每一行记录，从中提取出学校标识码或者学校名称，建立该榜单与学校的联系
    :param excel:
    :param batch:
    :return:
    """
    wb = excel_loader.load_excel(excel)  # 读取excel
    head = excel_loader.get_excel_head(wb)
    body = excel_loader.get_excel_body_generator(wb)
    cur_code = -1
    cur_name_cn = -1
    if "学校标识码" in head:
        cur_code = head.index("学校标识码")  # 优先记录学校标识码位置
    elif "学校名称" in head:
        cur_name_cn = head.index("学校名称")  # 记录学校名称位置
    for record in body:
        try:
            if cur_code != -1:
                college = College.objects.get(id_code=record[cur_code])
                BatchAndCollegeRelation.objects.create(college=college, batch=batch)
            elif cur_name_cn != -1:
                college = College.objects.get(name_cn=record[cur_name_cn])
                BatchAndCollegeRelation.objects.create(college=college, batch=batch)
        except Exception as e:
            logger.error(str(e))


def rankings_content_index(request, batch_id):
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
        "get_all_ranking_url": "/backend/rankings/content/retrieve/" + str(batch_id) + "/"
    }, context_instance=RequestContext(request))


def format_rankings_content(ranking_id, res):
    """
    格式化列表
    :return: json
    """
    ranking_fields = Table.get_fields_by_table_id(int(ranking_id))
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


def retrieve_rankings_content(request, batch_id):
    """
    获取所有信息
    :return: json
    """
    batch = BatchOfTable.objects.get(id=int(batch_id))  # 获取批次
    fields = ["batch"]
    args = [batch.batch.text.encode('utf-8')]
    res = Table.read_table_content_by_batch(batch.table.name, fields, args)
    return_dict = format_rankings_content(batch.table.id, res)  # 格式化院校信息
    return HttpResponse(json.dumps(return_dict))


def rankings_search_pick(request):
    """
    筛选院校
    :return:
    """
    model_fields = {"many_to_many": []}
    if request.method == "POST":
        return HttpResponseRedirect("/backend/rankings/" + request.POST["college"] + "/?search_by_college=true")
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
