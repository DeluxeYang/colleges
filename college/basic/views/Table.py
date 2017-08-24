#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import time
import random
import string

from django.db import IntegrityError
from django.db.models import Q

from basic.utils.logger import logger
from basic.utils import mysql_base_api
from basic.models import *


def get_all_table_types():
    """
    获取所有【表类型】
    :return:
    """
    return TypeOfTable.objects.all()


def get_table_type_by_id(_id):
    """
    按【ID】获取【表类型】
    :return:
    """
    return TypeOfTable.objects.get(id=_id)


def get_table_type_by_name(name_cn):
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
    if isinstance(param, int):
        table_type = get_table_type_by_id(param)
    elif isinstance(param, str):
        table_type = get_table_type_by_name(param)
    else:
        raise TypeError("Not a id or name")
    return table_type


def get_all_tables():
    """
    返回所有【表】
    :return:
    """
    return Table.objects.all()


def get_table_by_id(_id):
    """

    :param _id:
    :return:
    """
    return Table.objects.get(id=_id)


def get_table_by_name(_name):
    """

    :param _name:
    :return:
    """
    return Table.objects.get(Q(name=_name) | Q(name_cn=_name))


def get_table_by_id_or_name(param):
    """

    :param param:
    :return:
    """
    if isinstance(param, int):
        table = get_table_by_id(param)
    elif isinstance(param, str):
        table = get_table_by_name(param)
    else:
        raise TypeError("Not a id or name")
    return table


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


def get_fields_by_table_name(_name):
    """
    按【表名】返回一个【表】所有【字段】
    :param _name:
    :return:
    """
    table = get_table_by_name(_name)
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
    if isinstance(param, int):
        field_type = get_field_type_by_id(param)
    elif isinstance(param, str):
        field_type = get_field_type_by_name(param)
    else:
        raise TypeError("Not a id or name")
    return field_type


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


def get_random_name(temp_dict=None):
    while True:
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if not isinstance(temp_dict, dict):  # 如果参数为空，则返回带有时间戳的随机字符串
            return salt + "_" + str(int(time.time()))
        if salt not in temp_dict:  # 如果参数不为空，则为字典，判断salt是否重复
            temp_dict[salt] = 1
            return salt


def create_table(table, fields):
    """
    添加【表】及【表的字段】
    :param table: {table_name_cn,table_type}
    :param fields: [{field_name_cn,field_type}
    :return:
    """
    result = False
    try:
        _table = Table.objects.create(  # 先建立表
            name="ranking_" + get_random_name(),
            name_cn=table["table_name_cn"],
            type=get_table_type_by_id_or_name(table["table_type"]))  # 表类型的数据可以为名称也可以为ID，外键：TypeOfTable
        sql = "CREATE TABLE " + _table.name + "(" \
              + "id int(10) unsigned NOT NULL AUTO_INCREMENT," \
              + "batch varchar(255),"
        temp_dict = {}
        for field in fields:
            _type = get_field_type_by_name_or_id(field["field_type"])  # 字段类型数据可以为名称也可以为ID
            _field = Field.objects.create(
                name="field_" + get_random_name(temp_dict),
                name_cn=field["field_name_cn"],
                type=_type,  # 外键：TypeOfField
                table=_table)  # 外键：Table
            sql += _field.name + " " + _type.name
            sql += "(%s)," % _type.size if _type.size else ","  # 如果没有size，则没有括号
        sql += "PRIMARY KEY (id));"  # SQL尾
        logger.info(sql)  # 输出SQL
        db = mysql_base_api.MYSQL_CONFIG  # 连接mysql数据库
        conn, cursor = mysql_base_api.sql_init(db['HOST'], db['USER'], db['PASSWORD'], db['NAME'], int(db['PORT']))
        res = mysql_base_api.sql_execute(conn, cursor, sql, None)  # 执行SQL语句
        mysql_base_api.sql_close(conn, cursor)  # 关闭mysql连接
        if res != ():
            raise Exception(res)
        result = _table.id
    except IntegrityError as e:  # 仅处理重复添加错误
        logger.error(str(e))
    finally:
        return result


def drop_table(table):
    """
    删除【表】及【表的字段】
    :param table: table_name or table_name_cn or table_type
    :return:
    """
    result = False
    try:
        _table = get_table_by_id_or_name(table)
        try:
            tables_list = [_table.name]
            db = mysql_base_api.MYSQL_CONFIG  # 连接mysql数据库
            conn, cursor = mysql_base_api.sql_init(db['HOST'], db['USER'], db['PASSWORD'], db['NAME'], int(db['PORT']))
            mysql_base_api.drop_tables(cursor, tables_list)
            mysql_base_api.sql_close(conn, cursor)  # 关闭mysql连接
        except Exception as e:
            logger.error(str(e))
        get_fields_by_table_id(_table.id).delete()
        _table.delete()
        result = True
    except Exception as e:  # 仅处理重复添加错误
        logger.error(str(e))
    finally:
        return result
