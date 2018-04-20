"""
# middleware for dispatch url
"""
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from basic.utils.response import BIZ_CODE
from django.utils.deprecation import MiddlewareMixin


# 判断用户是否登陆的中间件
class QtsAuthentication(MiddlewareMixin):
    """ class in middleware to dispatch url in different situations """
    @staticmethod
    def process_request(request):
        if 'api' in request.path:
            # 如果当前用户没有登录,则只能访问登录和注册的接口,api/login/和api/register
            if str(request.user) == "AnonymousUser":
                # 未登录用户只能访问登录和注册接口,否则返回未登录{code:101, msg:未登录}
                if request.path != '/api/login/' and request.path != '/api/register/' and \
                                request.path != '/api/globalscore/':
                    ret = BIZ_CODE['UN_LOGIN']
                    return HttpResponse(json.dumps(ret))
        elif 'backend' in request.path:
            if not request.user.is_authenticated:
                return HttpResponseRedirect('/admin/login/?next=%s' % request.path)
            elif not request.user.is_staff:
                messages.error(request, "不是管理员无法访问后台系统")
                return HttpResponseRedirect('/')
