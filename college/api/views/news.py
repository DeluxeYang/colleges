#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import traceback

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from basic.models import NewsImage
from basic.utils.logger import logger
from college.settings import MEDIA_URL


@csrf_exempt
def image_upload(request):
    """

    :param request:
    :return:
    """
    return_dict = {"message": "error", "success": 0}
    try:
        if request.method == "POST":
            if "editormd-image-file" in request.FILES:
                news_image = NewsImage.objects.create(image=request.FILES["editormd-image-file"])
                return_dict = {"message": "success", "success": 1, "url": MEDIA_URL + str(news_image.image)}
    except Exception as e:
        logger.error(str(e))
    return HttpResponse(json.dumps(return_dict))
