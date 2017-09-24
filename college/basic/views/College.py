#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from basic.utils import common
from basic.models import College


def get_all_colleges():
    """

    :return:
    """
    return College.objects.all()


def get_college_by_id(college_id):
    """

    :param college_id:
    :return:
    """
    return College.objects.get(id=college_id)


def get_college_by_name(name_cn):
    """

    :param name_cn:
    :return:
    """
    return College.objects.get(name_cn__contains=name_cn)


def get_college_by_id_or_name(college):
    """

    :param college:
    :return:
    """
    if isinstance(college, int):
        _college = get_college_by_id(college)
    elif isinstance(college, str):
        _college = get_college_by_name(college)
    elif isinstance(college, College):
        _college = college
    else:
        raise TypeError("college Type Error")
    return _college


def get_colleges_id_name_by_nation(nation_code):
    """
    根据nation_code获取院校id和名称
    :return:
    """
    return_list = []
    colleges = College.objects.filter(nation_code__startswith=nation_code)
    for college in colleges:
        return_list.append({"id": college.id, "name_cn": college.name_cn})
    return return_list


def format_colleges_for_api(colleges):
    """
    获取所有院校信息
    :return: json
    """
    return_list = []
    i = 1
    for college in colleges:
        return_list.append({
            "i": str(i),
            "college_name_cn": college.name_cn,
            "college_id_code": college.id_code,
            "college_department": college.department.name_cn,
            "college_area": college.area,
            "college_province": college.province,
            "college_city": college.city,
            "college_edu_level": college.edu_level.name_cn,
            "college_edu_class": college.edu_class.name_cn,
            "college_is_vm": college.is_vice_ministry,
            "college_is_211": college.is_211,
            "college_is_985": college.is_985,
            "college_is_985p": college.is_985_platform,
            "college_is_dfc": college.is_double_first_class,
            "college_setup_time": college.setup_time.strftime("%Y-%m-%d") if college.setup_time else "",
            "college_cancel_time": college.cancel_time.strftime("%Y-%m-%d") if college.cancel_time else "",
            "college_note": college.note,
            "college_is_cancelled": college.is_cancelled,
            "college_transfer_to": college.transfer_to})
        i += 1
    return return_list


def get_all_colleges_with_paginator(page, size):
    """
    返回可以分页的所有院校信息
    :param page:  第几页
    :param size:  每页多少条
    :return:
    """
    colleges = College.objects.all()
    paginator = Paginator(colleges, size)  # colleges分页器
    try:
        content = paginator.page(page)
    except PageNotAnInteger:  # If page is not an integer, deliver first page.
        content = paginator.page(1)
    except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
        content = paginator.page(paginator.num_pages)
    return content, paginator.num_pages
