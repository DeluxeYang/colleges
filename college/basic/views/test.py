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
    from basic.utils import mysql_base_api
    db = mysql_base_api.MYSQL_CONFIG  # 连接mysql数据库
    conn, cursor = mysql_base_api.sql_init(db['HOST'], db['USER'], db['PASSWORD'], db['NAME'], int(db['PORT']))
    sql = mysql_base_api.build_insertsql("ranking_DwBptz0j_1503994945", {"A": "a", "B": "b"})
    mysql_base_api.sql_execute(conn, cursor, sql, ("a", "b"))
    mysql_base_api.sql_close(conn, cursor)  # 关闭mysql连接
