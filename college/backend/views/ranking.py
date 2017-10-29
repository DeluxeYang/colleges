#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import traceback

from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from basic.utils import common
from basic.models import *
from basic.views import Table
from basic.utils import excel_loader
from basic.utils.logger import logger

SIDEBAR_URL = [
    {"url": "/backend/ranking/", "name": "榜单分类列表", "active": False},
    {"url": "/backend/rankings/", "name": "榜单批次列表", "active": False},
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
    return render(request, "backend/list.html", {
        "self": request.user,
        "urls": urls,
        "fields": model_fields,
        "title": "榜单分类列表",
        "delete_url": "/backend/ranking/delete/",
        "batch_delete_url": "/backend/ranking/batch_delete/",
        "get_all_data_url": "/backend/ranking/retrieve/"})


def format_ranking(ranking, page, size):
    """
    格式化列表
    :return: json
    """
    return_dict = {"data": []}
    i = (page - 1) * size + 1
    for _ranking in ranking:
        return_dict["data"].append([
            '<label>' + str(i) + '<input value="' + str(_ranking.id) +
            '" name="_checkbox" type="checkbox"/></label>',
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
    _ranking = Table.get_tables_by_type_id(1)  # 1为榜单
    page = request.GET.get("page", 1)
    size = request.GET.get("size", 200)
    content, num_pages = common.with_paginator(_ranking.order_by("id"), int(page), int(size))
    return_dict = format_ranking(content, int(page), int(size))  # 格式化院校信息
    return_dict["num_pages"] = num_pages
    return JsonResponse(return_dict)


def add_ranking(request):
    """
    添加榜单
    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            _table = {"name_cn": request.POST["table_name_cn"], "type": 1}  # 榜单
            _fields = request.POST.getlist("field_name_cn")
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
    return render(request, "backend/ranking/add.html", {
        "self": request.user,
        "urls": urls})


def get_ranking(request, ranking_id):
    """

    :return:
    """
    ranking = Table.get_table_by_id(int(ranking_id))
    if request.method == "POST":
        print(request.POST)
        try:
            fields = request.POST.getlist("field_name_cn")
            for _field in fields:
                if not Field.objects.filter(table=ranking, name_cn=_field).count():
                    Field.objects.create(table=ranking, name_cn=_field)
                else:
                    messages.info(request, "存在重复字段，已忽略")
            messages.success(request, "添加字段成功")
        except Exception as e:
            logger.error(str(e))
            messages.error(request, "添加字段失败")
    fields = Table.get_fields_by_table_id(int(ranking_id)).order_by("id")
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render(request, "backend/ranking/ranking.html", {
        "self": request.user,
        "ranking": ranking,
        "fields": fields,
        "urls": urls})


def batch_delete_ranking(request):
    """
    批量删除
    :param request:
    :return:
    """
    return_dict = {}
    try:
        delete_list = request.POST.getlist("_ids[]")
        for i in delete_list:
            Table.delete_table(int(i))
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return JsonResponse(return_dict)


def delete_ranking(request):
    """
    删除一所
    :param request:
    :return:
    """
    return_dict = {}
    try:
        Table.delete_table(int(request.POST["_id"]))
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return JsonResponse(return_dict)


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
    return render(request, "backend/list.html", {
        "self": request.user,
        "urls": urls,
        "fields": model_fields,
        "title": "榜单批次列表",
        "delete_url": "/backend/rankings/delete/",
        "batch_delete_url": "/backend/rankings/batch_delete/",
        "get_all_data_url": "/backend/rankings/retrieve/"+ranking_id})


def format_rankings(batches, page, size):
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
        batches = BatchOfTable.objects.filter(table_type=1).order_by("id")
    elif "search_by_college" in request.GET:  # 此时的ranking_id为college id
        relations = RankingAndCollegeRelation.objects.filter(college_id=int(ranking_id))
        batches = []
        no_repeat = {}
        for r in relations:
            if r.ranking.batch.id not in no_repeat:
                no_repeat[r.ranking.batch.id] = 1
                batches.append(r.ranking.batch)
    else:
        _ranking = Table.get_table_by_id(int(ranking_id))
        batches = BatchOfTable.objects.filter(table=_ranking).order_by("id")
    page = request.GET.get("page", 1)
    size = request.GET.get("size", 200)
    content, num_pages = common.with_paginator(batches, int(page), int(size))
    return_dict = format_rankings(content, int(page), int(size))  # 格式化院校信息
    return_dict["num_pages"] = num_pages
    return JsonResponse(return_dict)


def batch_delete_rankings_batches(request):
    """
    批量删除
    :return:
    """
    return_dict = {}
    try:
        delete_list = request.POST.getlist("_ids[]")
        batches = BatchOfTable.objects.filter(id__in=delete_list)
        for _batch in batches:
            Ranking.objects.filter(batch=_batch).delete()
        batches.delete()
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return JsonResponse(return_dict)


def delete_rankings(request):
    """
    删除一所
    :return:
    """
    return_dict = {}
    try:
        delete_batch = int(request.POST["_id"])
        batch = BatchOfTable.objects.get(id=delete_batch)
        Ranking.objects.filter(batch=batch).delete()
        batch.delete()
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return JsonResponse(return_dict)


def import_ranking(request, ranking_id):
    """

    :return:
    """
    if request.method == "POST":
        return_dict = {}
        try:
            _file = request.FILES.get("file_upload")  # 上传的文件
            wb = excel_loader.load_excel(_file)  # 读取excel
            head = excel_loader.get_excel_head(wb)
            body = excel_loader.get_excel_body_generator(wb)
            batch = request.POST["extra"]
            _table = Table.get_table_by_id(int(ranking_id))  # 获取表
            _batch = matching_batch(batch, _table)  # 匹配批次，如果已存在批次，抛出错误
            matching_field(_table, head)  # 如果excel中出现未定义的字段，抛出错误
            # 看字段中是否存在“学校名称”或者“学校标识码”
            if "学校标识码" in head:
                cur = head.index("学校标识码")  # 优先记录学校标识码位置
            elif "学校名称" in head:
                cur = head.index("学校名称")  # 记录学校名称位置
            else:
                cur = -1
            # 分别处理每行数据
            length = len(head)
            for record in body:
                data = {}
                for i in range(length):  # 生成json数据，“字段”：数据
                    data[head[i]] = empty_is_empty_str(record[i])
                ranking = Ranking.objects.create(batch=_batch, data=data)
                if cur != -1:  # 字段中存在“学校名称”或者“学校标识码”，则建立与对应学校之间的关系
                    param = record[cur]  # “学校名称”或者“学校标识码”对应字段
                    try:
                        college = College.objects.get(Q(name_cn=param) | Q(id_code=param))  # 找到该学校
                        RankingAndCollegeRelation.objects.create(college=college, ranking=ranking)  # 建立该字段与学校之间的关系
                    except ObjectDoesNotExist:
                        logger.warning(param+"不存在")
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
            return JsonResponse(return_dict)
    year = YearSeasonMonth.objects.filter(type=1)
    _ranking = Table.get_table_by_id(int(ranking_id))
    _fields = Table.get_fields_by_table_id(int(ranking_id))
    fields = [str(f.name_cn) for f in _fields]
    urls = copy.deepcopy(SIDEBAR_URL)  # 侧边栏网址
    urls[0]["active"] = True
    return render(request, "backend/ranking/import.html", {
        "self": request.user,
        "fields": fields,
        "ranking": _ranking,
        "year": year,
        "urls": urls,
        "file_upload_url": "/backend/ranking/import/"+str(ranking_id)+"/"})


def matching_batch(batch, table):
    """
    匹配批次
    """
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
    # 如果已有该批次，则失败
    if BatchOfTable.objects.filter(batch=_batch, table=table).exists():
        raise IntegrityError(str(table) + str(_batch))
    return BatchOfTable.objects.create(table=table, batch=_batch)


def matching_field(table, head):
    """
    如果excel中有未定义的字段，则抛出错误
    :param table:
    :param head:
    :return:
    """
    _fields = Field.objects.filter(table=table).values_list("name_cn", flat=True)
    for h in head:
        if h not in _fields:
            raise Exception(str(table) + "：字段错误")


def empty_is_empty_str(content):
    """
    如果excel里为空，则会返回“None”，所以再转换为空
    :param content:
    :return:
    """
    return content if content != "None" else ""


def rankings_content_index(request, batch_id):
    """

    :return:
    """
    batch = BatchOfTable.objects.get(id=int(batch_id))
    ranking_fields = Table.get_fields_by_table_id(int(batch.table.id)).order_by("id")
    model_fields = []
    for field in ranking_fields:
        model_fields.append(field.name_cn)
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[1]["active"] = True
    return render(request, "backend/ranking/ranking_content.html", {
        "self": request.user,
        "urls": urls,
        "fields": model_fields,
        "title": str(batch.table.name_cn)+"（批次："+str(batch.batch.text)+"）",
        "get_all_ranking_url": "/backend/rankings/content/retrieve/" + str(batch_id) + "/"})


def retrieve_rankings_content(request, batch_id):
    """
    获取所有信息
    :return: json
    """
    batch = BatchOfTable.objects.get(id=int(batch_id))  # 获取批次
    data = Ranking.objects.filter(batch=batch).values_list("data", flat=True)
    ranking_fields = Field.objects.filter(table=batch.table).order_by("id").values_list("name_cn", flat=True)
    return_dict = {"data": []}
    for _data in data:
        temp = []
        for field in ranking_fields:
            temp.append(_data.get(field, ""))
        return_dict["data"].append(temp)
    return JsonResponse(return_dict)


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
    return render(request, "backend/ranking/pick.html", {
        "self": request.user,
        "fields": model_fields,
        "urls": urls,
        "get_colleges_by_nation_url": "/api/college/by/nation/"})
