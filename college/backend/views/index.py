#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template.context import RequestContext


def index(request):
    """

    :param request:
    :return:
    """
    directions = [
        {"url": "/index/", "name": "首页", "active": True},
    ]
    return render_to_response("backend/base.html",
                              {"self": request.user,
                               "urls": directions},
                              context_instance=RequestContext(request))
