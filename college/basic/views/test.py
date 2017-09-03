#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import json

from django.http import HttpResponse
from django import forms
from DjangoUeditor.widgets import UEditorWidget

from basic.views import Table
from basic.models import *
from basic.utils.logger import logger


def test1(request):
    return_list = []
    try:
        tables = Table.get_all_tables()
        for t in tables:
            temp_dict = {
                "table_id": t.id,
                "table_name": t.table_name,
                "table_name_cn": t.table_name_cn,
                "create_time": str(t.create_time),
            }
            return_list.append(temp_dict)
    except Exception as e:
        print(e)
    finally:
        return HttpResponse(json.dumps(return_list))


def test2(request):
    return_list = []
    try:
        tables = Table.get_fields_by_table_name(1)
        for t in tables:
            temp_dict = {
                "field_id": t.id,
                "field_name": t.field_name,
                "field_name_cn": t.field_name_cn,
                "field_type": str(t.field_type)
            }
            return_list.append(temp_dict)
    except Exception as e:
        print(e)
    finally:
        return HttpResponse(json.dumps(return_list))


def test3(request):
    result = []
    tables = {
        "table_name": "test",
        "table_name_cn": "啊",
        "table_type": 1
    }
    fields = [{"field_name": "test",
               "field_name_cn": "啊啊",
               "field_type": 1}]
    result = Table.create_table(tables, fields)
    return HttpResponse(json.dumps(result))


def batch(request):
    year = 1800
    for y in range(1900, 2100):
        YearSeasonMonth.objects.create(year=y, type=1)
        for s in range(1, 5):
            YearSeasonMonth.objects.create(year=y, season=s, type=2)
        for m in range(1, 13):
            YearSeasonMonth.objects.create(year=y, month=m, type=3)
    return HttpResponse("")


def test(request):
    from backend.views import college
    start = datetime.datetime.now()

    colleges = College.objects.all()
    res = format_colleges(colleges)
    end = datetime.datetime.now()
    print((end - start))
    return HttpResponse(res)


def format_colleges(colleges):
    """
    获取所有院校信息
    :return: json
    """
    return_dict = {"data": []}
    i = 1
    for college in colleges:
        return_dict["data"].append([
            '<label>' + str(i) + '<input value="' + str(college.id) +
            '" name="college_checkbox" type="checkbox"/></label>',
            college.name_cn,
            college.id_code,
            college.department.name_cn,
            college.area,
            college.province,
            college.city,
            college.edu_level.name_cn,
            college.edu_class.name_cn,
            "是" if college.is_vice_ministry else "",
            "是" if college.is_211 else "",
            "是" if college.is_985 else "",
            "是" if college.is_985_platform else "",
            "是" if college.is_double_first_class else "",
            college.setup_time.strftime("%Y-%m-%d") if college.setup_time else "",
            college.cancel_time.strftime("%Y-%m-%d") if college.cancel_time else "",
            college.note,
            "是" if college.is_cancelled else "",
            college.transfer_to,
            "<a href='/backend/college/modify/" + str(college.id) + "/'>修改</a>",
            "<a id='row_" + str(college.id) +
            "' href='javascript:href_ajax(" + str(college.id) + ")'" +
            " onclick=\"return confirm('确认删除" + college.name_cn + "？')\">删除</a>"])
        i += 1
    return return_dict