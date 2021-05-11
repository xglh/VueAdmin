#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 16:39
# @Author  : liuhui
# @Detail  :

import logging
from common.basic import BaseModelViewSet, MyPageNumberPagination
from common.custom import UserRolePermission
from user.models import SysUser
from user.serializers.user_serializer import SysUserCreateSerializer, SysUserUpdateSerializer, SysUserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

logger = logging.getLogger()


class UserAccountViewSet(BaseModelViewSet):
    """
    UserAccount增删改查
    """
    perms_map = {
        # action: 角色列表； *代表所有
        '*': ['admin'],
        'retrieve': ['*'],
        'update': ['*'],

    }
    queryset = SysUser.objects.all().order_by('id')
    serializer_class = SysUserSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'nick_name')
    ordering_fields = ('id', 'username')
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (UserRolePermission,)

    # 根据action定义
    def get_serializer_class(self):
        serializer_class = SysUserSerializer
        # 新建用户
        if self.action == 'create':
            serializer_class = SysUserCreateSerializer
        # 更新用户信息
        elif self.action == 'update':
            serializer_class = SysUserUpdateSerializer
        return serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.GET
        role_id = params.get('role_id')
        if role_id:
            queryset = queryset.filter(role_id=int(role_id))
        return queryset
