#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 16:39
# @Author  : liuhui
# @Detail  :

import logging
from common.basic import BaseModelViewSet, MyPageNumberPagination, BaseResponse
from rest_framework.response import Response
from common.custom import UserRolePermission
from user.models import SysRole
from user.serializers.role_serializer import SysRoleSerializer, SysRoleCreateSerializer, SysRoleUpdateSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView

logger = logging.getLogger()


class UserRoleViewSet(BaseModelViewSet):
    """
    UserAccount增删改查
    """
    perms_map = {
        '*': ['admin']
    }
    queryset = SysRole.objects.all().order_by('id')
    serializer_class = SysRoleSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('role', 'role_name')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (UserRolePermission,)

    # 根据action定义
    def get_serializer_class(self):
        serializer_class = SysRoleSerializer
        # 新建用户
        if self.action == 'create':
            serializer_class = SysRoleCreateSerializer
        # 更新用户信息
        elif self.action == 'update':
            serializer_class = SysRoleUpdateSerializer
        return serializer_class


class UserRoleListDataApiView(APIView):
    '''
    获取所有角色
    '''
    perms_map = {
        '*': ['admin']
    }
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (UserRolePermission,)

    def get(self, request):
        response = BaseResponse()
        sysRole_qs = SysRole.objects.all().order_by('id')
        sysRole_serializer = SysRoleSerializer(sysRole_qs, many=True)

        response.data = sysRole_serializer.data
        return Response(response.to_json())


class UserRolesDeleteApiView(APIView):
    '''
    批量删除角色
    '''
    perms_map = {
        '*': ['admin']
    }
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (UserRolePermission,)

    def delete(self, request):
        response = BaseResponse()
        role_ids = request.data
        if type(role_ids) != list:
            response.set_error_response(code=400, message='参数校验失败')
        else:
            SysRole.objects.filter(id__in=role_ids).delete()
        return Response(response.to_json())
