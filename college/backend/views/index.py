#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required


def index(request):
    """

    :param request:
    :return:
    """
    if not request.user.is_staff:
        return HttpResponseRedirect("/")
    else:
        return render_to_response("backend/base.html",
                                  {"self": request.user},
                                  context_instance=RequestContext(request))

