#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import datetime
import traceback

from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
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
                                  "file_delete_url": "/backend/college/delete/",
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
            "<a id='row_" + str(college.id) +
            "' href='javascript:href_ajax(" + str(college.id) + ")'" +
            " onclick=\"return confirm('确认删除" + college.name_cn + "？')\">删除</a>"])
        i += 1
    return HttpResponse(json.dumps(return_dict))


def get_college_by_name(request):
    """

    :param request:
    :return:
    """
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[1]["active"] = True
    return render_to_response("backend/base.html",
                              {
                                  "self": request.user,
                                  "urls": urls
                              },
                              context_instance=RequestContext(request))


def college_classification(obj):
    """

    :return:
    """
    fields_dict = {"char": [], "boolean": [], "foreign_key": [], "nation": [], "time": []}
    for field in College_model._meta.fields:
        _field = str(field).split(".")[2]
        temp = {"name": field.verbose_name,
                "field": _field,
                "value": obj.get(_field, "")}
        if type(field).__name__ == "CharField":
            temp["value"] = temp["value"] if temp["value"] else ""
            if temp["field"] == "area" or temp["field"] == "nation_code":
                continue
            elif temp["field"] == "province" or temp["field"] == "city":
                fields_dict["nation"].append(temp)
            else:
                fields_dict["char"].append(temp)
        elif type(field).__name__ == "DateField":
            temp["value"] = temp["value"].strftime("%Y-%m-%d") if temp["value"] else ""
            fields_dict["time"].append(temp)
        elif type(field).__name__ == "BooleanField":
            temp["value"] = "checked" if temp["value"] else ""
            fields_dict["boolean"].append(temp)
        elif type(field).__name__ == "ForeignKey":
            if temp["field"] == "department":
                if _field+"_id" in obj:
                    temp["value"] = Department.objects.get(id=obj[_field+"_id"])
                    temp["fields"] = Department.objects.exclude(id=obj[_field+"_id"])
                else:
                    temp["fields"] = Department.objects.all().order_by("name_cn")
            elif temp["field"] == "edu_level":
                if _field+"_id" in obj:
                    temp["value"] = EduLevel.objects.get(id=obj[_field+"_id"])
                    temp["fields"] = EduLevel.objects.exclude(id=obj[_field+"_id"])
                else:
                    temp["fields"] = EduLevel.objects.all().order_by("name_cn")
            elif temp["field"] == "edu_class":
                if _field+"_id" in obj:
                    temp["value"] = EduClass.objects.get(id=obj[_field+"_id"])
                    temp["fields"] = EduClass.objects.exclude(id=obj[_field+"_id"])
                else:
                    temp["fields"] = EduClass.objects.all().order_by("name_cn")
            fields_dict["foreign_key"].append(temp)
    return fields_dict


def add_college(request):
    """
    添加一所院校
    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            nation = Nation.objects.get(code=request.POST["city"])
            college = College_model.objects.create(
                name_cn=request.POST["name_cn"],
                id_code=request.POST["id_code"],
                department=Department.objects.get(id=int(request.POST["department"])),
                edu_level=EduLevel.objects.get(id=int(request.POST["edu_level"])),
                edu_class=EduClass.objects.get(id=int(request.POST["edu_class"])),
                city=nation.city,
                province=Nation.objects.get(id=nation.parent).province,
                is_vice_ministry=True if "is_vice_ministry" in request.POST else False,
                is_211=True if "is_211" in request.POST else False,
                is_985=True if "is_985" in request.POST else False,
                is_985_platform=True if "is_985_platform" in request.POST else False,
                is_double_first_class=True if "is_double_first_class" in request.POST else False,
                is_cancelled=True if "is_cancelled" in request.POST else False,
                setup_time=get_date_from_post(request.POST.get("setup_time", "")),
                cancel_time=get_date_from_post(request.POST.get("cancel_time", "")),
                note=request.POST.get("note", ""),
                transfer_to=request.POST.get("transfer_to", ""))
            messages.success(request, "添加成功")
            return HttpResponseRedirect("/backend/college/modify/" + str(college.id) + "/")
        except IntegrityError as e:  # 处理重复添加错误
            logger.error(str(e))
            logger.error(traceback.format_exc())
            messages.error(request, "添加失败，院校名称或识别码重复添加")
        except Exception as e:
            logger.error(str(e))
            logger.error(traceback.format_exc())
            messages.error(request, "添加失败，请检查添加的数据")
    fields_dict = college_classification(obj={})
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[2]["active"] = True
    return render_to_response("backend/college/add.html", {
            "self": request.user,
            "fields": fields_dict,
            "urls": urls
        }, context_instance=RequestContext(request))


def modify_college(request, college_id):
    """

    :param request:
    :param college_id:
    :return:
    """
    college = College_model.objects.get(id=college_id)
    if request.method == "POST":
        try:
            nation = Nation.objects.get(code=request.POST["city"])
            college.name_cn = request.POST["name_cn"]
            college.id_code = request.POST["id_code"]
            college.department = Department.objects.get(id=int(request.POST["department"]))
            college.edu_level = EduLevel.objects.get(id=int(request.POST["edu_level"]))
            college.edu_class = EduClass.objects.get(id=int(request.POST["edu_class"]))
            college.city = nation.city
            college.province = Nation.objects.get(id=nation.parent).province
            college.is_vice_ministry = True if "is_vice_ministry" in request.POST else False
            college.is_211 = True if "is_211" in request.POST else False
            college.is_985 = True if "is_985" in request.POST else False
            college.is_985_platform = True if "is_985_platform" in request.POST else False
            college.is_double_first_class = True if "is_double_first_class" in request.POST else False
            college.is_cancelled = True if "is_cancelled" in request.POST else False
            college.setup_time = get_date_from_post(request.POST.get("setup_time", ""))
            college.cancel_time = get_date_from_post(request.POST.get("cancel_time", ""))
            college.note = request.POST.get("note", "")
            college.transfer_to = request.POST.get("transfer_to", "")
            college.save()
            messages.success(request, "修改成功")
        except IntegrityError as e:  # 处理重复添加错误
            logger.error(str(e))
            logger.error(traceback.format_exc())
            messages.error(request, "添加失败，院校名称或识别码重复添加")
        except Exception as e:
            logger.error(str(e))
            logger.error(traceback.format_exc())
            messages.error(request, "添加失败，请检查添加的数据")
    fields_dict = college_classification(college.__dict__)
    urls = copy.deepcopy(SIDEBAR_URL)
    urls[0]["active"] = True
    return render_to_response("backend/college/modify.html", {
            "self": request.user,
            "fields": fields_dict,
            "urls": urls
        }, context_instance=RequestContext(request))


def delete_college(request):
    """

    :param request:
    :return:
    """
    return_dict = {}
    try:
        College_model.objects.get(id=int(request.POST["college_id"])).delete()
        return_dict["success"] = "删除成功"
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        return_dict["error"] = "删除失败"
    return HttpResponse(json.dumps(return_dict))


def get_date_from_post(content):
    if content != "":
        return datetime.datetime.strptime(content, "%Y-%m-%d")
    else:
        return None


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


def get_date_from_excel(text):
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
                    setup_time=get_date_from_excel(record[temp_dict[model_fields[15]]]),
                    cancel_time=get_date_from_excel(record[temp_dict[model_fields[16]]]),
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
