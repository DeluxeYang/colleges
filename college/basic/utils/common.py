#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def with_paginator(data, page, size):
    paginator = Paginator(data, size)  # colleges分页器
    try:
        content = paginator.page(page)
    except PageNotAnInteger:  # If page is not an integer, deliver first page.
        content = paginator.page(1)
    except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
        content = []
    return content, paginator.num_pages
