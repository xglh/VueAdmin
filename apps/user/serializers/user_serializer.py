#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 16:03
# @Author  : liuhui
# @Detail  : 序列化

from user.models import SysUser, role_choice
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


class SysUserCreateSerializer(serializers.ModelSerializer):
    '''
    用户生成序列化
    '''
    username = serializers.CharField(required=True, validators=[
        # 唯一性校验
        UniqueValidator(
            queryset=SysUser.objects.all(),
            message='username已存在'
        )])
    password = serializers.CharField(required=True, min_length=6, max_length=24)
    email = serializers.CharField(max_length=255, default='', allow_blank=True, required=False)
    phone = serializers.CharField(max_length=255, default='', allow_blank=True, required=False)
    avatar = serializers.CharField(max_length=255, default='', allow_blank=True, required=False)
    nick_name = serializers.CharField(max_length=255, default='', allow_blank=True, required=False)
    role = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = SysUser
        fields = ('username', 'password', 'email', 'phone', 'avatar', 'nick_name', 'role')

    def validate_password(self, password):
        return make_password(password)

    def validate_role(self, role):
        role_allowed_list = [x[0] for x in role_choice]
        print(role, role_allowed_list)
        if role not in role_allowed_list:
            raise serializers.ValidationError('role只能为:{}'.format(','.join(role_allowed_list)))
        return role


class SysUserUpdateSerializer(serializers.ModelSerializer):
    '''
    用户更新序列化
    '''
    password = serializers.CharField(min_length=6, max_length=24, required=False)
    email = serializers.CharField(max_length=255, allow_blank=True, required=False)
    phone = serializers.CharField(max_length=255, allow_blank=True, required=False)
    avatar = serializers.CharField(max_length=255, allow_blank=True, required=False)
    nick_name = serializers.CharField(max_length=255, allow_blank=True, required=False)
    role = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = SysUser
        fields = ('password', 'email', 'phone', 'role', 'avatar', 'nick_name', 'role')

    def validate_password(self, password):
        if password:
            password = make_password(password)
        return password

    def validate_role(self, role):
        role_allowed_list = [x[0] for x in role_choice]
        if role and role not in role_allowed_list:
            raise serializers.ValidationError('role只能为:{}'.format(','.join(role_allowed_list)))
        return role


class SysUserInfoSerializer(serializers.ModelSerializer):
    '''
    用户信息序列化
    '''
    username = serializers.CharField(max_length=255, allow_blank=True, required=False)
    role = serializers.CharField(max_length=255, allow_blank=True, required=False)
    email = serializers.CharField(max_length=255, allow_blank=True, required=False)
    phone = serializers.CharField(max_length=255, allow_blank=True, required=False)
    avatar = serializers.CharField(max_length=255, allow_blank=True, required=False)
    nick_name = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = SysUser
        fields = ('username', 'role', 'email', 'phone', 'role', 'avatar', 'nick_name')
