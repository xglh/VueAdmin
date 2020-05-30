#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/29 11:41
# @Author  : liuhui
# @Detail  : 用户鉴权
from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token
from common.request_info import get_authorization_header
from user.models import SysUser

# 用户角色校验
class UserRolePermission(BasePermission):
    # 无权限的显示信息
    message = '接口鉴权失败！'

    # 必须重写 has_permission
    def has_permission(self, request, view):
        result = False
        has_token, token = get_authorization_header(request)
        user_role = None
        perms_map = {}
        if hasattr(view, 'perms_map'):
            perms_map = getattr(view, 'perms_map')

        if len(perms_map) == 0:
            result = True
        else:
            # 根据token获取用户角色
            if has_token:
                try:
                    auth_obj = Token.objects.get(key=token)
                    user = SysUser.objects.get(id=auth_obj.user_id)
                    user_role = user.role_id.role
                except Exception:
                    user_role = None

            req_method = request.method.lower()

            # *优先级低于method key
            key_all_str = '*'
            user_roles_allowed = []
            if key_all_str in perms_map:
                user_roles_allowed = perms_map.get(key_all_str, [])

            if req_method in perms_map:
                user_roles_allowed = perms_map.get(req_method, [])

            if len(user_roles_allowed) > 0 and user_role in user_roles_allowed:
                result = True
            elif len(user_roles_allowed) == 0:
                result = True
        return result
