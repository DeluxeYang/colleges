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
from backend.views import index, college, news, ranking


urlpatterns = [
    url(r'^$', index.index),
    # college
    url(r'^college/$', college.index),
    url(r'^college/search/(?P<param>[a-zA-Z0-9_]+)/$', college.index),
    url(r'^college/search/(?P<param>[a-zA-Z0-9_]+)/(?P<digit>[0-9]+)/$', college.index),

    url(r'^college/retrieve/$', college.retrieve_colleges),
    url(r'^college/retrieve/(?P<param>[a-zA-Z0-9_]+)/$', college.retrieve_colleges),
    url(r'^college/pick/(?P<param>[a-zA-Z0-9_]+)/$', college.college_search_pick),
    url(r'^college/retrieve/(?P<param>[a-zA-Z0-9_]+)/(?P<digit>[0-9]+)/$', college.retrieve_colleges),

    url(r'^college/add/$', college.add_college),
    url(r'^college/modify/(?P<college_id>[0-9]+)/$', college.modify_college),
    url(r'^college/delete/$', college.delete_college),
    url(r'^college/batch_delete/$', college.batch_delete_college),
    url(r'^college/import/$', college.import_college),
    url(r'^college/clean/$', college.clean_college),
    # news
    url(r'^news/$', news.index),
    url(r'^news/search/(?P<param>[a-zA-Z0-9_]+)/$', news.index),
    url(r'^news/search/(?P<param>[a-zA-Z0-9_]+)/(?P<digit>[0-9]+)/$', news.index),

    url(r'^news/retrieve/$', news.retrieve_news),
    url(r'^news/retrieve/(?P<param>[a-zA-Z0-9_]+)/$', news.retrieve_news),
    url(r'^news/retrieve/(?P<param>[a-zA-Z0-9_]+)/(?P<digit>[0-9]+)/$', news.retrieve_news),

    url(r'^news/pick/(?P<param>[a-zA-Z0-9_]+)/$', news.news_search_pick),

    url(r'^news/(?P<news_id>[0-9]+)/$', news.get_news),
    url(r'^news/add/$', news.add_news),
    url(r'^news/modify/(?P<news_id>[0-9]+)/$', news.modify_news),
    url(r'^news/delete/$', news.delete_news),
    url(r'^news/batch_delete/$', news.batch_delete_news),
    # ranking
    url(r'^ranking/$', ranking.index),
    url(r'^ranking/retrieve/$', ranking.retrieve_ranking),
    url(r'^ranking/(?P<ranking_id>[0-9]+)/$', ranking.get_ranking),

    url(r'^ranking/import/(?P<ranking_id>[0-9]+)/$', ranking.import_ranking),

    url(r'^ranking/add/$', ranking.add_ranking),
    url(r'^ranking/delete/$', ranking.delete_ranking),
    url(r'^ranking/batch_delete/$', ranking.batch_delete_ranking),

    url(r'^rankings/$', ranking.rankings_index),
    url(r'^rankings/retrieve/$', ranking.retrieve_rankings),
    url(r'^rankings/(?P<ranking_id>[0-9]+)/$', ranking.rankings_index),
    url(r'^rankings/retrieve/(?P<ranking_id>[0-9]+)/$', ranking.retrieve_rankings),
    url(r'^rankings/delete/$', ranking.delete_rankings),
    url(r'^rankings/batch_delete/$', ranking.batch_delete_ranking_batches),

    url(r'^rankings/content/(?P<batch_id>[0-9]+)/$', ranking.rankings_content_index),
    url(r'^rankings/content/retrieve/(?P<batch_id>[0-9]+)/$', ranking.retrieve_rankings_content),
    url(r'^rankings/search/college/$', ranking.rankings_search_pick),
]
