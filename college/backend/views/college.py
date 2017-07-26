#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json

from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from basic.models import College as College_model, Nation, Department, EduLevel, EduClass
from basic.views import College
from basic.utils import excel_loader
from basic.utils.logger import logger

SIDEBAR_URL = [
    {"url": "/backend/college/", "name": "院校信息", "active": False},
    {"url": "/backend/college/search/", "name": "搜索院校", "active": False},
    {"url": "/backend/college/add/", "name": "添加院校", "active": False},
    {"url": "/backend/college/import/", "name": "批量导入院校", "active": False},
]


def get_all_colleges(request):
    """

    :param request:
    :return:
    """
    colleges = College.get_all_colleges()
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render_to_response("backend/base.html",
                              {
                                  "self": request.user,
                                  "colleges": colleges,
                                  "urls": urls
                              },
                              context_instance=RequestContext(request))


def get_college_by_name(request):
    """

    :param request:
    :return:
    """
    college = request.POST.get("college_name", "")
    # college = College.get_college_by_name(college_name_cn)
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[1]["active"] = True
    return render_to_response("backend/base.html",
                              {
                                  "self": request.user,
                                  "colleges": college,
                                  "urls": urls
                              },
                              context_instance=RequestContext(request))


def add_college(request):
    """

    :param request:
    :return:
    """
    college = request.POST.get("college_name", "")
    # college = College.get_college_by_name(college_name_cn)
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    return render_to_response("backend/base.html",
                              {
                                  "self": request.user,
                                  "colleges": college,
                                  "urls": urls
                              },
                              context_instance=RequestContext(request))


def get_obj_or_insert_obj(obj, query):
    result = None
    try:
        result = obj.objects.get(name_cn=query)
    except ObjectDoesNotExist:
        result = obj.objects.create(name_cn=query)
    finally:
        return result


def empty_is_false(content):
    return True if len(content.strip()) != 0 else False


def get_nation_code(city):
    nation_code = ""
    try:
        if len(city.strip()) == 0:
            raise Exception()
        nation_code = Nation.objects.get(
            Q(city=city, province="") | Q(district=city, province="", city="")).code
    except ObjectDoesNotExist:
        logger.error(city + ": 不存在")
    except Exception as e:
        logger.error(str(e) + ": " + city)
    finally:
        return nation_code


def import_college(request):
    """

    :param request:
    :return:
    """
    model_fields = [x.verbose_name for x in College_model._meta.fields]
    if request.method == "POST":
        _file = request.FILES.get("file_upload")
        wb = excel_loader.load_excel(_file)
        head = excel_loader.get_excel_head(wb)
        body = excel_loader.get_excel_body(wb)
        temp_dict = {}
        for f in model_fields[1:]:
            if f in head:
                temp_dict[f] = head.index(f)
        for record in body:
            College_model.objects.create(
                name_cn=record[temp_dict[model_fields[1]]],
                id_code=record[temp_dict[model_fields[2]]],
                department=get_obj_or_insert_obj(Department, record[temp_dict[model_fields[3]]]),
                area=record[temp_dict[model_fields[4]]],
                province=record[temp_dict[model_fields[5]]],
                city=record[temp_dict[model_fields[6]]],
                nation_code=get_nation_code(record[temp_dict[model_fields[6]]]),
                edu_level=get_obj_or_insert_obj(EduLevel, record[temp_dict[model_fields[8]]]),
                edu_class=get_obj_or_insert_obj(EduClass, record[temp_dict[model_fields[9]]]),
                is_vice_ministry=empty_is_false(record[temp_dict[model_fields[10]]]),
                is_211=empty_is_false(record[temp_dict[model_fields[11]]]),
                is_985=empty_is_false(record[temp_dict[model_fields[12]]]),
                is_985_platform=empty_is_false(record[temp_dict[model_fields[13]]]),
                is_double_first_class=empty_is_false(record[temp_dict[model_fields[14]]]),
                setup_time=record[temp_dict[model_fields[15]]],
                cancel_time=record[temp_dict[model_fields[16]]],
                note=record[temp_dict[model_fields[17]]],
                is_cancelled=empty_is_false(record[temp_dict[model_fields[18]]]),
                transfer_to=record[temp_dict[model_fields[19]]],
            )
        return HttpResponse(json.dumps({"success": "success"}))
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[3]["active"] = True
    return render_to_response("backend/college/college_import.html",
                              {
                                  "self": request.user,
                                  "fields": model_fields[1:7] + model_fields[8:],
                                  "urls": urls,
                                  "file_upload_url": "/backend/college/import/"
                              },
                              context_instance=RequestContext(request))
