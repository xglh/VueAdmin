#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 16:40
# @Author  : liuhui
# @Detail  : 登录&退出view

import logging
import traceback
from rest_framework.views import APIView
from rest_framework import status
import pytz, datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from VueAdmin.base import BaseResponse

# token过期时间
EXPIRE_MINUTES = settings.REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES
logger = logging.getLogger('mylogger')


# token验证
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# 获取token
class UserLoginView(ObtainAuthToken):
    def post(self, request):
        response = BaseResponse()
        response.data = {"token": None}
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
                utc_tz = pytz.timezone('UTC')
                time_now = datetime.datetime.now(tz=utc_tz)
                if not created:
                    # 检查token创建时间,过期则重新创建
                    time_create = token.created
                    # 去掉时区信息
                    if time_create < time_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
                        token.delete()
                        token = Token.objects.create(user=serializer.validated_data['user'])
                        token.created = time_now
                        token.save()
                response.data = {'token': token.key}
            else:
                response.success = False
                err_msg = ""
                try:
                    for error_key in serializer.errors:
                        err_msg += "{}:{}".format(error_key, "".join(serializer.errors[error_key]))
                except Exception:
                    err_msg = "获取token失败"
                response.message = err_msg
        except Exception as e:
            response.set_http_500_response(message=str(e), data=[])
            logger.error(traceback.format_exc())
        return Response(response.to_json())


class UserLogoutView(APIView):

    def post(self, request):
        response = BaseResponse()
        try:
            body = request.data
            try:
                token = body['token']
            except KeyError:
                response.set_error_response(code=400, message='参数校验失败')
            else:
                Token.objects.filter(key=token).delete()
        except Exception as e:
            response.set_http_500_response(message=str(e))
            logger.error(traceback.format_exc())
        return Response(response.to_json())
