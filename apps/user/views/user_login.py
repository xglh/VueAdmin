#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 16:40
# @Author  : liuhui
# @Detail  : 登录&退出view

import logging
import jwt
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from VueAdmin.settings import SECRET_KEY
from common.basic import BaseResponse
from django.contrib.auth import authenticate, logout
from rest_framework_jwt.settings import api_settings

logger = logging.getLogger()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserAuthView(APIView):
    """
    用户认证获取token
    """
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        response = BaseResponse()
        if user:
            payload = jwt_payload_handler(user)
            response.data = {
                'user_id': user.id,
                'username': user.username,
                'token': jwt.encode(payload, SECRET_KEY)
            }
        else:
            response.set_error_response(code=401, message='用户名或密码错误！')
        return Response(response.to_json())


class UserLogoutView(APIView):

    def put(self, request):
        response = BaseResponse()
        logout(request)
        return Response(response.to_json())
