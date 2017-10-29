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

from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status

from basic.models import College as College_model, Nation, Department, EduLevel, EduClass, Area
from basic.views import College
from basic.utils.logger import logger


from api.serializer import college


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


class CollegeList(generics.ListAPIView):
    """

    """
    queryset = College_model.objects.all()
    serializer_class = college.CollegeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class CollegeDetail(generics.RetrieveAPIView):
    """
    College详细信息
    """
    queryset = College_model.objects.all()
    serializer_class = college.CollegeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
