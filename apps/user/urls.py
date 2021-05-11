#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/30 14:13
# @Author  : liuhui
# @Detail  : user路由

from django.urls import path, include
from rest_framework import routers
from user.views.user_login import UserAuthView, UserLogoutView

from user.views.user_role import UserRoleViewSet, UserRoleListDataApiView, UserRolesDeleteApiView
from user.views.user_account import UserAccountViewSet

router = routers.SimpleRouter()
router.register(r"roles", UserRoleViewSet, base_name="roles")
router.register(r"users", UserAccountViewSet, base_name="users")

urlpatterns = [
    # 登录
    path(r'login/', UserAuthView.as_view()),
    # 登出
    path(r'logout/', UserLogoutView.as_view()),
    # 获取所有角色
    path(r'roles/all/', UserRoleListDataApiView.as_view()),
    # 批量删除角色
    path(r'roles/del/', UserRolesDeleteApiView.as_view()),
    # 获取user信息列表
    path(r"", include(router.urls)),
]
