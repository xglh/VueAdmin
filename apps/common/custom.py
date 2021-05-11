# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/30 22:19
# @Author  : liuhui
# @Detail  :

from rest_framework.permissions import BasePermission
from rest_framework.views import exception_handler


# 用户角色校验
class UserRolePermission(BasePermission):
    '''
    retrieve: 用户详情
    create: 创建用户
    update: 更新用户信息
    destroy: 删除用户
    list: 获取用户列表
    '''
    # 无权限的显示信息
    message = '无接口访问权限！'

    # 必须重写 has_permission
    def has_permission(self, request, view):
        result = False
        perms_map = {}
        if hasattr(view, 'perms_map'):
            perms_map = getattr(view, 'perms_map')
        if len(perms_map) == 0:
            result = True
        else:
            # 根据token获取用户角色
            user = request.user
            user_role = user.role_id.role

            # ModelViewSet 通过action判断
            if hasattr(view, 'action'):
                target_perm_key = view.action
            # APIView 通过请求方法判断
            else:
                target_perm_key = request.method.lower()
            key_all_str = '*'
            user_roles_allowed = []
            if key_all_str in perms_map:
                user_roles_allowed = perms_map.get(key_all_str, [])
                # 判断具有*权限的角色
                if user_role in user_roles_allowed:
                    result = True
                else:
                    if target_perm_key in perms_map:
                        user_roles_allowed = perms_map.get(target_perm_key, [])
                        if key_all_str in user_roles_allowed or user_role in user_roles_allowed:
                            result = True
        return result


# 自定义异常返回数据结构
def rest_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        msg = '失败' if response.status_code >= 400 else '成功'
        notification_response = dict()
        notification_response['code'] = response.status_code
        notification_response['message'] = msg
        notification_response['success'] = False
        notification_response['data'] = response.data
        response.data = notification_response
        response.status_code = 200
    return response
