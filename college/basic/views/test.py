#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import json

from django.http import HttpResponse

from basic.views import Table
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
        tables = Table.get_all_fields_of_one_table(1)
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


def test(request):
    result = []
    try:
        tables = {
            "table_name": "test",
            "table_name_cn": "啊"
        }
        fields = [{"field_name": "test",
                   "field_name_cn": "啊啊",
                   "field_type": 2}]
        result = Table.add_table(tables, fields)
    except Exception as e:
        print(e)
        logger.info(str(e))
    finally:
        return HttpResponse(json.dumps(result))