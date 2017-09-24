#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import datetime
import traceback

from django.db import connection
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from basic.models import College as College_model, Nation, Department, EduLevel, EduClass, Area
from basic.views import College
from basic.utils import excel_loader
from basic.utils.logger import logger


def get_colleges_by_nation(request):
    """

    :param request:
    :return:
    """
    return_dict = {"data": [], "message": "success"}
    province = request.POST.get("province", "")
    city = request.POST.get("city", "")
    if province[:2] != city[:2]:
        city = ""
    if city != "":
        return_dict["data"] = College.get_colleges_id_name_by_nation(city[:4])
    elif province != "":
        return_dict["data"] = College.get_colleges_id_name_by_nation(province[:2])
    else:
        return_dict["message"] = "error"
    return HttpResponse(json.dumps(return_dict))


def get_all_colleges(request):
    """

    :param request:
    :return:
    """
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 20))
    colleges, num_pages = College.get_all_colleges_with_paginator(page, size)
    return_dict = {"page": colleges.number, "size": size,
                   "num_pages": num_pages, "type": "colleges", "length": len(colleges),
                   "data": College.format_colleges_for_api(colleges)}
    return JsonResponse(return_dict)
