#!/usr/bin/env python
# -*- coding: utf-8 -*-

BIZ_CODE = {
    'SUCCESS': {'code': '200', 'message': '操作成功'},
    'ERROR': {'code': '201', 'message': '操作失败'},

    'UN_LOGIN': {'code': '101', 'message': '未登录'},
    'PARAM_INVALID': {'code': '102', 'message': '参数错误'},
    'OPERATE_DATABASE_ERROR': {'code': '103', 'message': '操作数据库失败'},
    'IMG_UPLOAD_ERROR': {'code': '104', 'message': '图片上传失败'},
    'OPERATING_FAILED': {'code': '105', 'message': '操作失败'},
    'WRONG_CONNECT': {'code': '106', 'message': '访问方式出错'},

    'USER_LOGIN_FAIL': {'code': '201', 'message': '用户名或密码错误'},
    'USER_REMAIN': {'code': '202', 'message': '用户已存在'},
    'USER_LOGON': {'code': '203', 'message': '用户已登录'},
    'USER_INACTIVE': {'code': '204', 'message': '用户已被本系统禁用'},
    'WRONG_PASS': {'code': '205', 'message': '当前旧密码错误'},
    'USER_NOT_EXIST': {'code': '206', 'message': '不能修改其他用户密码'},
    'USER_NOT_LOGIN': {'code': '207', 'message': '用户未登录'},

    'OPTION_ALREADY_HANDLED': {'code': '202', 'message': '已经操作成功'}
}


# global return code
class Response:
    """
    @:param
        code for response status
        message for response message
        result for handling result from views/v1/[function].py
    """
    code = ''
    message = ''
    result = {}

    def __init__(self):
        self.code = BIZ_CODE['SUCCESS']['code']
        self.message = BIZ_CODE['SUCCESS']['message']
        self.result = {}

    def set_code(self, state):
        """
        :param state:
        :return:
        """
        self.code = BIZ_CODE[state]['code']
        self.message = BIZ_CODE[state]['message']

    def add_data(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        self.result[key] = value