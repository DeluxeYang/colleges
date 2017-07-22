#!/usr/bin/env python
# -*- coding: utf-8 -*-
from basic.utils.logger import logger
from basic.models import News, NewsTag, NewsComment, College
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
