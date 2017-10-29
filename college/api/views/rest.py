from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status

from basic.models import College

from api.serializer import college


@api_view(('GET',))
def api_root(request, _format=None):
    """
    无登录，无注册
    """
    return Response({
        'college': reverse('college-list', request=request, format=_format),
        'college_by_nation': reverse('college-by-nation', request=request, format=_format),
    })
