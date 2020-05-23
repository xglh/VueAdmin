#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/30 14:13
# @Author  : liuhui
# @Detail  : user路由

from django.urls import path

from user.views.user_login import UserLoginView, UserLogoutView
from user.views.user_account import UserSysCreateView, UserSysInfoView, UserSysListView

urlpatterns = [
    # 登录
    path(r'login', UserLoginView.as_view()),
    # 登出
    path(r'logout', UserLogoutView.as_view()),
    # 获取user信息列表
    path('users', UserSysListView.as_view()),
    # 新增user
    path('user', UserSysCreateView.as_view()),
    # user接口
    path('user/<str:userName>', UserSysInfoView.as_view()),
]
