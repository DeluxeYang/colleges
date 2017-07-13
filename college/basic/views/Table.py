#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import datetime

from elasticsearch import Elasticsearch

from django.db import IntegrityError

from college.settings import es_address
from basic.utils.logger import logger
from basic.models import Tables, Types, DateOfTable, Fields

es = Elasticsearch(es_address)


def get_all_tables():
    """
    返回所有表信息
    :return:
    """
    return Tables.objects.all()


def get_all_fields_of_one_table(table_id):
    """
    返回一个表所有字段
    :param table_id:
    :return:
    """
    return Fields.objects.filter(table_id=table_id)


def add_table(table, fields):
    """

    :param table: {table_name,table_name_cn}
    :param fields: [{field_name,field_name_cn,field_type}
    :return:

CREATE TABLE `mapping_session` (
  `mapping_session_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `old_db_name` varchar(80) NOT NULL DEFAULT '',
  `new_db_name` varchar(80) NOT NULL DEFAULT '',
  `old_release` varchar(5) NOT NULL DEFAULT '',
  `new_release` varchar(5) NOT NULL DEFAULT '',
  `old_assembly` varchar(20) NOT NULL DEFAULT '',
  `new_assembly` varchar(20) NOT NULL DEFAULT '',
  `created` datetime NOT NULL,
  PRIMARY KEY (`mapping_session_id`)
) ENGINE=MyISAM AUTO_INCREMENT=392 DEFAULT CHARSET=latin1;
    """
    try:
        table = Tables.objects.create(
            table_name=table["table_name"],
            table_name_cn=table["table_name_cn"],
            create_time=datetime.datetime.now())
        for field in fields:
            Fields.objects.create(
                field_name=field["field_name"],
                field_name_cn=field["field_name_cn"],
                field_type_id=int(field["field_type"]),
                table=table)
    except IntegrityError as e:
        # print(e)
        logger.info(str(e))
    return "success"
