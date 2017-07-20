#!/usr/bin/env python
# -*- coding: utf-8 -*-
from basic.views.Table import create_table
# from basic.utils.logger import logger
# from basic.utils import mysql_base_api
from basic.models import *


def create_ranking(table, fields):
    """
    创建【榜单】的数据表
    :param table: {"table_name": *, "table_name_cn": *}
    :param fields: [{field_name,field_name_cn,field_type}, ...] 默认在list头添加batch字段
    :return:
    """
    table["table_type"] = 1  # 表类型为1，为榜单
    _fields = [{"field_name": "batch", "field_name_cn": "批次", "field_type": 1}] + fields  # 默认字段1，int，存BatchOfTable的ID
    return create_table(table, _fields)


def add_batch_of_ranking(table_id, batch_id):
    """
    向【榜单】中添加一个批次的数据
    :param table_id: 表id
    :param batch_id: batch_id
    :return:
    """
    batch = YearSeasonMonth.objects.get(id=batch_id)
    table = Table.objects.get(id=table_id)
    batch_of_table = BatchOfTable.objects.create(
        table=table, batch=batch, name_cn=str(table.name_cn)+"_"+str(batch.text))
    return batch_of_table


def import_excel_to_ranking(table_id, batch_id, excel_file):
    """

    :param table_id:
    :param batch_id:
    :param excel_file:
    :return:
    """
    batch_of_table = BatchOfTable.objects.get(table_id=table_id, batch_id=batch_id)
    batch = batch_of_table.id
    fields = Table.objects.get(id=table_id)
