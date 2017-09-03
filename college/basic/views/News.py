#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from basic.models import News, NewsTag, NewsAndTag, NewsComment, NewsAndCollege
from basic.views.College import *


def get_all_news():
    """

    :return:
    """
    return News.objects.all()


def get_news_by_id(news_id):
    """

    :param news_id:
    :return:
    """
    return News.objects.get(id=news_id)


def get_news_by_title(news_title):
    """

    :param news_title:
    :return:
    """
    return News.objects.get(title=news_title)


def get_news_by_id_or_title(param):
    """

    :param param:
    :return:
    """
    if isinstance(param, int):
        _news = get_news_by_id(param)
    elif isinstance(param, str):
        _news = get_news_by_title(param)
    elif isinstance(param, News):
        _news = param
    else:
        raise TypeError("news Type Error")
    return _news


def get_all_news_by_college(college):
    """

    :param college:
    :return:
    """
    _college = get_college_by_id_or_name(college)
    news = News.objects.filter(college=_college)
    return news


def get_all_tags():
    """

    :return:
    """
    return NewsTag.objects.all()


def get_tag_by_id(tag_id):
    """

    :param tag_id:
    :return:
    """
    return NewsTag.objects.get(id=tag_id)


def get_tag_by_title(tag_title):
    """

    :param tag_title:
    :return:
    """
    return NewsTag.objects.get(title=tag_title)


def get_tag_by_id_or_title(tag):
    """

    :param tag:
    :return:
    """
    if isinstance(tag, int):
        _tag = get_tag_by_id(tag)
    elif isinstance(tag, str):
        _tag = get_tag_by_title(tag)
    elif isinstance(tag, NewsTag):
        _tag = tag
    else:
        raise TypeError("tag Type Error")
    return _tag


def get_news_by_tag(tag):
    """

    :param tag:
    :return:
    """
    _tag = get_tag_by_id_or_title(tag)
    news = News.objects.filter(tag=_tag)
    return news


def get_all_comments_of_one_news(news):
    """

    :param news:
    :return:
    """
    news = get_news_by_id_or_title(news)
    comments = NewsComment.objects.filter(news=news)
    return comments


def create_news(news, tags, colleges):
    """

    :param news:
    :param tags: [id,id]
    :param colleges: [id,id]
    :return:
    """
    _news = News.objects.create(
        user=news["user"],
        title=news["title"],
        keywords=news["keywords"],
        abstract=news["abstract"],
        content=news["content"],
        is_published=news["is_published"],
        is_allow_comments=news["is_allow_comments"],
        is_stick_top=news["is_stick_top"],
        is_bold=news["is_bold"])
    for tag in tags:
        NewsAndTag.objects.create(news=_news,
                                  tag=get_tag_by_id(int(tag)))
    for college in colleges:
        NewsAndCollege.objects.create(news=_news,
                                      college=get_college_by_id(int(college)))
    return _news


def update_news(news, tags, colleges):
    """

    :param news:
    :param tags:
    :param colleges:
    :return:
    """
    _news = get_news_by_id_or_title(news["id"])
    _news.user = news["user"]
    _news.title = news["title"]
    _news.keywords = news["keywords"]
    _news.abstract = news["abstract"]
    _news.content = news["content"]
    _news.is_published = news["is_published"]
    _news.is_allow_comments = news["is_allow_comments"]
    _news.is_stick_top = news["is_stick_top"]
    _news.is_bold = news["is_bold"]
    _news.save()
    NewsAndTag.objects.filter(news=_news).delete()
    for tag in tags:
        NewsAndTag.objects.create(news=_news,
                                  tag=get_tag_by_id_or_title(tag))
    NewsAndCollege.objects.filter(news=_news).delete()
    for college in colleges:
        NewsAndCollege.objects.create(news=_news,
                                      college=get_college_by_id_or_name(college))
    return _news


def delete_news(news):
    """

    :param news:
    :return:
    """
    _news = get_news_by_id_or_title(news)
    NewsAndTag.objects.filter(news=_news).delete()
    NewsAndCollege.objects.filter(news=_news).delete()
    _news.delete()
    return _news
