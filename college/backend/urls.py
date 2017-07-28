"""college URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from backend.views import index, college


urlpatterns = [
    url(r'^$', index.index),

    url(r'^college/$', college.index),
    url(r'^college/all/$', college.get_all_colleges),
    url(r'^college/search/$', college.get_college_by_name),
    url(r'^college/add/$', college.add_college),
    url(r'^college/import/$', college.import_college),
]