#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import datetime

# from elasticsearch import Elasticsearch

from django.db import IntegrityError
from django.db.models import Q

from basic.utils.logger import logger
from basic.models import *


def get_all_table_types():
    """
    获取所有【表类型】
    :return:
    """
    return TypeOfTable.objects.all()


def get_table_types_by_id(_id):
    """
    按【ID】获取【表类型】
    :return:
    """
    return TypeOfTable.objects.get(id=_id)


def get_table_types_by_name(name_cn):
    """
    按【名称】获取【表类型】
    :return:
    """
    return TypeOfTable.objects.get(name_cn=name_cn)


def get_table_type_by_id_or_name(param):
    """

    :param param:
    :return:
    """
    return TypeOfTable.objects.get(Q(id=param) | Q(name_cn=param))


def get_all_tables():
    """
    返回所有【表】
    :return:
    """
    return Table.objects.all()


def get_tables_by_type_id(type_id):
    """
    按【表类型ID】获取【表】
    :return:
    """
    type_of_table = TypeOfTable.objects.get(id=type_id)
    return Table.objects.filter(type=type_of_table)


def get_tables_by_type_name(name):
    """
    按【表类型名】获取【表】
    :return:
    """
    type_of_table = TypeOfTable.objects.get(name_cn=name)
    return Table.objects.filter(type=type_of_table)


def get_fields_by_table_name(table_name):
    """
    按【表名】返回一个【表】所有【字段】
    :param table_name:
    :return:
    """
    table = Table.objects.get(Q(name=table_name) | Q(name_cn=table_name))
    return Field.objects.filter(table=table)


def get_fields_by_table_id(table_id):
    """
    按【表ID】返回一个【表】所有【字段】
    :param table_id:
    :return:
    """
    return Field.objects.filter(table_id=table_id)


def get_all_field_types():
    """
    返回所有【字段类型】
    :return:
    """
    return TypeOfField.objects.all()


def get_field_type_by_id(_id):
    """
    按【ID】返回所有【字段类型】
    :return:
    """
    return TypeOfField.objects.get(id=_id)


def get_field_type_by_name(name):
    """
    按【名称】返回所有【字段类型】
    :return:
    """
    return TypeOfField.objects.get(name=name)


def get_field_type_by_name_or_id(param):
    """
    按【名称】返回所有【字段类型】
    :return:
    """
    return TypeOfField.objects.get(Q(id=param) | Q(name=param))


def get_field_types_size():
    """
    返回【字段类型】的预定义【size】
    :return: {varchar：30}
    """
    field_types_size = {}
    field_types = get_all_field_types()
    for field_type in field_types:
        field_types_size[field_type.name] = field_type.size
    return field_types_size


def add_table(table, fields):
    """
    添加表及表的字段
    :param table: {table_name,table_name_cn,table_type}
    :param fields: [{field_name,field_name_cn,field_type}
    :return:
    """
    try:
        _table = Table.objects.create(  # 先建立表
            name=table["table_name"],
            name_cn=table["table_name_cn"],
            type=get_table_type_by_id_or_name(table["table_type"]))  # 表类型的数据可以为名称也可以为ID，外键：TypeOfTable
        sql = "CREATE TABLE " + table["table_name"] + "(" \
              + "id int(10) unsigned NOT NULL AUTO_INCREMENT,"  # SQL头
        for field in fields:
            _type = get_field_type_by_name_or_id(field["field_type"])  # 字段类型数据可以为名称也可以为ID
            Field.objects.create(
                name=field["field_name"],
                name_cn=field["field_name_cn"],
                type=_type,  # 外键：TypeOfField
                table=_table)  # 外键：Table
            sql += field["field_name"] + " " + _type.name
            sql += "(%s)," % _type.size if _type.size else ","  # 如果没有size，则没有括号
        sql += "PRIMARY KEY (id));"  # SQL尾
        logger.info(sql)  # 输出SQL
    except IntegrityError as e:
        logger.info(str(e))
    return "success"
