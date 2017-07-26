#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
