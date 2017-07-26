#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.models import User

from basic.utils.response import Response
from basic.utils.logger import logger


class UserForm(forms.Form):
    username = forms.CharField(label='用户名：', max_length=100)
    password = forms.CharField(label='密码：', widget=forms.PasswordInput())


# 登录
def login(request):
    response = Response()
    if request.user.is_authenticated():
        response.set_code('USER_LOGON')  # 用户已经登录
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)  # 检验用户名密码是否存在auth_user表中
        if user is not None:
            if user.is_active:
                user_login(request, user)  # 登录用户
                logger.info("username login : " + username)
            else:
                response.set_code('USER_INACTIVE')
        else:
            response.set_code('USER_LOGIN_FAIL')  # 用户名或者密码错误
    else:
        response.set_code('WRONG_CONNECT')
    return response.__dict__


# 注册
def register(request):
    response = Response()
    if request.method == 'POST':
        form = UserForm(data=request.POST)  # 将数据存储在form类对象中
        if form.is_valid():  # 检验数据是否为空
            username = request.POST.get('username')  # 取出用户名数据
            password = request.POST.get('password')  # 取出密码数据
            # 首先判断用户是否已存在
            filter_result = User.objects.filter(username=username)
            if filter_result.first() == ("" or None):  # 若不存在该用户，则添加用户名密码到数据库的auth_user表中
                # 这里三个参数是固定的，必须是用户名、邮箱、密码，且顺序不能改变
                new_user = User.objects.create_user(username, "", password)
                new_user.save()
                request.session['username'] = username  # 把用户存储在session中
            else:
                response.set_code('USER_REMAIN')
        else:
            response.set_code('PARAM_INVALID')
    else:
        response.set_code('WRONG_CONNECT')
    return response.__dict__


# 修改密码
def modify_password(request):
    response = Response()
    if request.method == 'POST':
        username = request.session.get('username')
        old_password = request.POST.get('password')
        new_password = request.POST.get('newpassword')
        try:  # 首先要校验用户名是否存在
            u = User.objects.get(username__exact=username)
            res = u.check_password(old_password)  # 校验密码是否正确
            if res:
                u.set_password(new_password)  # 设置新密码
                u.save()  # 保存新密码
            else:
                response.set_code('WRONG_PASS')
        except Exception as e:
            logger.error(e)
            response.set_code('WRONG_PASS')
        return response.__dict__


# 退出登录
def logout(request):
    response = Response()
    user_logout(request)  # 用户退出登录
    return response.__dict__
