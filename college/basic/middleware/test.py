import time
from importlib import import_module

from django.conf import settings
from django.contrib.sessions.backends.base import UpdateError
from django.core.exceptions import SuspiciousOperation
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import cookie_date


class Test1(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        # engine = import_module(settings.SESSION_ENGINE)
        # self.SessionStore = engine.SessionStore
        # super().__init__()

    def process_request(self, request):
        print(request.COOKIES)
        print(request.__dict__)
        print("request 1")
        # request.session = self.SessionStore(session_key)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("process_view 1")

    def process_response(self, request, response):
        print("response 1")
        return response

class Test2(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        # engine = import_module(settings.SESSION_ENGINE)
        # self.SessionStore = engine.SessionStore
        # super().__init__()

    def process_request(self, request):
        print(request.COOKIES)
        print(request.session.__dict__)
        print("request 2")
        # request.session = self.SessionStore(session_key)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("process_view 2")

    def process_response(self, request, response):
        print("response 2")
        return response

class Test3(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        # engine = import_module(settings.SESSION_ENGINE)
        # self.SessionStore = engine.SessionStore
        # super().__init__()

    def process_request(self, request):
        print(request.session.__dict__)
        print("request 3")
        # request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
        print("response 3")
        return response