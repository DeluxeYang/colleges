#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import datetime
import traceback

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
    {"url": "/backend/college/search/", "name": "搜索院校", "active": False,
     "drop_down": [
        {"url": "/backend/college/search/by_class/", "name": "按类别搜索院校",
         "drop_down": [
            {"url": "/backend/college/search/by_nation/", "name": "3"},
            {"url": "/backend/college/search/by_nation/", "name": "3"},
         ]},
        {"url": "/backend/college/search/by_nation/", "name": "按地域搜索院校"},
        {"url": "/backend/college/search/by_nation/", "name": "按搜索院校"},
     ]},
    {"url": "/backend/college/add/", "name": "添加院校", "active": False},
    {"url": "/backend/college/import/", "name": "批量导入院校", "active": False},
]


def index(request):
    """

    :param request:
    :return:
    """
    model_fields = ["#", "院校名称", "标识码", "主管部门", "省", "市", "层次",
                    "类别", "副部级", "211", "985", "985平台", "双一流",
                    "成立时间", "注销时间", "备注", "已撤销", "合并后", "修改", "删除"]
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render_to_response("backend/college/list.html",
                              {
                                  "self": request.user,
                                  "fields": model_fields,
                                  "urls": urls,
                                  "get_all_college_url": "/backend/college/all/"
                              },
                              context_instance=RequestContext(request))


def get_all_colleges(request):
    """
    获取所有院校信息
    :param request:
    :return: json
    """
    colleges = College.get_all_colleges()
    return_dict = {"data": []}
    i = 1
    for college in colleges:
        return_dict["data"].append([
            i,
            college.name_cn,
            college.id_code,
            college.department.name_cn,
            college.province,
            college.city,
            college.edu_level.name_cn,
            college.edu_class.name_cn,
            "是" if college.is_vice_ministry else "",
            "是" if college.is_211 else "",
            "是" if college.is_985 else "",
            "是" if college.is_985_platform else "",
            "是" if college.is_double_first_class else "",
            college.setup_time.strftime("%Y-%m-%d") if college.setup_time else "",
            college.cancel_time.strftime("%Y-%m-%d") if college.cancel_time else "",
            college.note,
            "是" if college.is_cancelled else "",
            college.transfer_to,
            "<a href='/backend/college/modify/" + str(college.id) + "/'>修改</a>",
            "<a href='/backend/college/delete/" + str(college.id) + "/'" +
            " onclick=\"return confirm('确认删除" + college.name_cn + "？')\">删除</a>"
        ])
        i += 1
    return HttpResponse(json.dumps(return_dict))


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


def college_classification():
    """

    :return:
    """
    fields_dict = {"char": [], "boolean": [], "foreign_key": [], "nation": [], "time": []}
    for field in College_model._meta.fields:
        temp = {"name": field.verbose_name, "field": str(field).split(".")[2]}
        if type(field).__name__ == "CharField":
            if temp["field"] == "area" or temp["field"] == "nation_code":
                continue
            elif temp["field"] == "province" or temp["field"] == "city":
                fields_dict["nation"].append(temp)
            else:
                fields_dict["char"].append(temp)
        elif type(field).__name__ == "DateField":
            fields_dict["time"].append(temp)
        elif type(field).__name__ == "BooleanField":
            fields_dict["boolean"].append(temp)
        elif type(field).__name__ == "ForeignKey":
            if temp["field"] == "department":
                temp["field"] = Department.objects.all().order_by("name_cn")
            elif temp["field"] == "edu_level":
                temp["field"] = EduLevel.objects.all().order_by("name_cn")
            elif temp["field"] == "edu_class":
                temp["field"] = EduClass.objects.all().order_by("name_cn")
            fields_dict["foreign_key"].append(temp)
    return fields_dict


def add_college(request):
    """
    添加一所院校
    :param request:
    :return:
    """
    fields_dict = college_classification()
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    return render_to_response("backend/college/add.html",
                              {
                                  "self": request.user,
                                  "fields": fields_dict,
                                  "urls": urls
                              },
                              context_instance=RequestContext(request))


def get_obj_or_insert_obj(obj, query):
    """
    获取一个model对象，如果不存在则创建
    :param obj:
    :param query:
    :return:
    """
    result = None
    try:
        result = obj.objects.get(name_cn=query)
    except ObjectDoesNotExist:
        result = obj.objects.create(name_cn=query)
    finally:
        return result


def empty_is_false(content):
    """
    如果读取到的内容为’None‘，则为False
    :param content:
    :return:
    """
    return True if content != "None" else False


def empty_is_empty(content):
    """
    如果excel里为空，则会返回“None”，所以再转换为空
    :param content:
    :return:
    """
    return content if content != "None" else None


def get_nation_code(city):
    """
    根据城市名获取行政区划代码
    :param city:
    :return:
    """
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


def get_date(text):
    """
    获取日期
    :param text:
    :return:
    """
    text = text.split(" ")[0]
    if not empty_is_empty(text):
        return None
    else:
        return datetime.datetime.strptime(text, "%Y-%m-%d")


def import_college(request):
    """
    从excel导入院校信息
    :param request:
    :return:
    """
    model_fields = [x.verbose_name for x in College_model._meta.fields]  # 读取数据库中院校表的字段别名
    if request.method == "POST":
        return_dict = {}
        try:
            _file = request.FILES.get("file_upload")  # 上传的文件
            wb = excel_loader.load_excel(_file)  # 读取excel
            head = excel_loader.get_excel_head(wb)
            body = excel_loader.get_excel_body_generator(wb)
            temp_dict = {}
            for f in model_fields[1:]:
                if f in head:
                    temp_dict[f] = head.index(f)  # 找到数据库字段对应在excel的位置
            for record in body:
                College_model.objects.create(  # 创建记录
                    name_cn=empty_is_empty(record[temp_dict[model_fields[1]]]),
                    id_code=empty_is_empty(record[temp_dict[model_fields[2]]]),
                    department=get_obj_or_insert_obj(Department, empty_is_empty(record[temp_dict[model_fields[3]]])),
                    area=empty_is_empty(record[temp_dict[model_fields[4]]]),
                    province=empty_is_empty(record[temp_dict[model_fields[5]]]),
                    city=empty_is_empty(record[temp_dict[model_fields[6]]]),
                    nation_code=get_nation_code(record[temp_dict[model_fields[6]]]),
                    edu_level=get_obj_or_insert_obj(EduLevel, empty_is_empty(record[temp_dict[model_fields[8]]])),
                    edu_class=get_obj_or_insert_obj(EduClass, empty_is_empty(record[temp_dict[model_fields[9]]])),
                    is_vice_ministry=empty_is_false(record[temp_dict[model_fields[10]]]),
                    is_211=empty_is_false(record[temp_dict[model_fields[11]]]),
                    is_985=empty_is_false(record[temp_dict[model_fields[12]]]),
                    is_985_platform=empty_is_false(record[temp_dict[model_fields[13]]]),
                    is_double_first_class=empty_is_false(record[temp_dict[model_fields[14]]]),
                    setup_time=get_date(record[temp_dict[model_fields[15]]]),
                    cancel_time=get_date(record[temp_dict[model_fields[16]]]),
                    note=empty_is_empty(record[temp_dict[model_fields[17]]]),
                    is_cancelled=empty_is_false(record[temp_dict[model_fields[18]]]),
                    transfer_to=empty_is_empty(record[temp_dict[model_fields[19]]]),
                )
            return_dict["success"] = "success"
        except Exception as e:
            logger.error(str(e))
            logger.error(traceback.format_exc())
            return_dict["error"] = "出现错误，请检查文件及内容格式"
        finally:
            return HttpResponse(json.dumps(return_dict))
    urls = copy.deepcopy(SIDEBAR_URL)  # 侧边栏网址
    urls[3]["active"] = True
    return render_to_response("backend/college/import.html",
                              {
                                  "self": request.user,
                                  "fields": model_fields[1:7] + model_fields[8:],
                                  "urls": urls,
                                  "file_upload_url": "/backend/college/import/"
                              },
                              context_instance=RequestContext(request))
