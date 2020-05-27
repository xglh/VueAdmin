#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 16:39
# @Author  : liuhui
# @Detail  :

import logging
import traceback
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers.role_serializer import SysRoleCreateSerializer, SysRoleUpdateSerializer, SysRoleInfoSerializer
from user.models import SysRole
from VueAdmin.base import BaseResponse, MyPageNumberPagination

logger = logging.getLogger('mylogger')


# 创建角色
class SysRoleCreateView(APIView):

    def post(self, request):
        response = BaseResponse()
        try:
            serializer = SysRoleCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                response.set_error_response(code=400, message=serializer.errors)
        except Exception as e:
            response.set_http_500_response(message=str(e))
            logger.error(traceback.format_exc())
        return Response(response.to_json())


class SysRoleInfoView(APIView):

    # 获取角色信息
    def get(self, request, role):
        response = BaseResponse()
        try:
            try:
                user_qs = SysRole.objects.get(role=role)
            except SysRole.DoesNotExist:
                response.set_error_response(code=404, message='用户不存在')
            else:
                serializer = SysRoleInfoSerializer(user_qs)
                response.data = serializer.data
        except Exception as e:
            response.set_http_500_response(message=str(e))
            logger.error(traceback.format_exc())
        return Response(response.to_json())

    # 修改用户信息
    def put(self, request, role):
        response = BaseResponse()
        try:
            try:
                user_qs = SysRole.objects.get(role=role)
            except SysRole.DoesNotExist:
                response.set_error_response(code=500, message='用户不存在')
            else:

                serializer = SysRoleUpdateSerializer(data=request.data, instance=user_qs)
                if serializer.is_valid():
                    serializer.save()
                else:
                    response.set_error_response(code=500, message=serializer.errors)
        except Exception as e:
            response.set_http_500_response(message=str(e))
            logger.error(traceback.format_exc())
        return Response(response.to_json())

    # 删除用户
    def delete(self, request, role):
        response = BaseResponse()
        try:
            try:
                user_qs = SysRole.objects.get(role=role)
            except SysRole.DoesNotExist:
                response.set_error_response(code=500, message='用户不存在')
            else:
                user_qs.delete()
        except Exception as e:
            response.set_http_500_response(message=str(e))
            logger.error(traceback.format_exc())
        return Response(response.to_json())


class SysRolesView(APIView):

    # 获取角色信息列表
    def get(self, request):
        response = BaseResponse()
        try:

            user_qs = SysRole.objects.all().order_by('id')
            data_list, total = [], user_qs.count()
            try:
                page = MyPageNumberPagination()
                pages_query_set = page.paginate_queryset(queryset=user_qs, request=request, view=self)
                serializer = SysRoleInfoSerializer(instance=pages_query_set, many=True)
                data_list = serializer.data
            except NotFound:
                data_list = []
            response.data = {
                'total': total,
                'rows': data_list
            }
        except Exception as e:
            response.set_http_500_response(message=str(e))
            logger.error(traceback.format_exc())

        return Response(response.to_json())

    # 批量删除角色
    def delete(self, request):
        response = BaseResponse()
        try:
            body = request.data
            try:
                assert type(body) == list
            except Exception:
                response.set_error_response(400,message='参数类型错误')
            else:
                SysRole.objects.filter(role__in=body).delete()
        except Exception as e:
            response.set_http_500_response(message=str(e))
            logger.error(traceback.format_exc())

        return Response(response.to_json())