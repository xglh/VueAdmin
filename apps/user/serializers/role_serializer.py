#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 16:03
# @Author  : liuhui
# @Detail  : 序列化

from user.models import SysRole
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class SysRoleCreateSerializer(serializers.ModelSerializer):
    '''
    角色序列化
    '''
    role = serializers.CharField(required=True, min_length=6, max_length=24, validators=[
        # 唯一性校验
        UniqueValidator(
            queryset=SysRole.objects.all(),
            message='角色已存在'
        )])
    role_name = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = SysRole
        fields = ('role', 'role_name')


class SysRoleUpdateSerializer(serializers.ModelSerializer):
    '''
    角色更新序列化
    '''
    role_name = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = SysRole
        fields = ('role_name',)

class SysRoleInfoSerializer(serializers.ModelSerializer):
    '''
    角色信息
    '''
    role = serializers.CharField(max_length=255, required=True)
    role_name = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = SysRole
        fields = ('role', 'role_name')