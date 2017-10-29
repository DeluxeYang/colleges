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
from django.conf.urls import url, include
from api.views import college, news, rest
from rest_framework.urlpatterns import format_suffix_patterns
# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', rest.api_root),
    url(r'^college/$', college.CollegeList.as_view(), name='college-list'),
    url(r'^college/(?P<pk>[0-9]+)/$', college.CollegeDetail.as_view(), name='college-detail'),
    # url(r'^college/by/$', college.CollegesByNation.as_view(), name='college-by'),
])

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^college/by/nation/$', college.get_colleges_by_nation),

    url(r'^news/image_upload/$', news.image_upload),
]
