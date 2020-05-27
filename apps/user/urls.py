#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/30 14:13
# @Author  : liuhui
# @Detail  : user路由

from django.urls import path

from user.views.user_login import UserLoginView, UserLogoutView
from user.views.user_account import SysUserCreateView, SysUserInfoView, SysUserUsersView
from user.views.user_role import SysRoleCreateView, SysRoleInfoView, SysRolesView

urlpatterns = [
    # 登录
    path(r'login', UserLoginView.as_view()),
    # 登出
    path(r'logout', UserLogoutView.as_view()),
    # 获取role信息列表
    path('roles', SysRolesView.as_view()),
    # 新增role
    path('role', SysRoleCreateView.as_view()),
    # role接口
    path('role/<str:role>', SysRoleInfoView.as_view()),
    # 获取user信息列表
    path('users', SysUserUsersView.as_view()),
    # 新增user
    path('user', SysUserCreateView.as_view()),
    # user接口
    path('user/<str:userName>', SysUserInfoView.as_view()),
]
