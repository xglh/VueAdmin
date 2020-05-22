#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 10:36
# @Author  : liuhui
# @Detail  :
import os
import sys
import django
import datetime

current_path = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
project_dir = '{}/../'.format(current_dir)
sys.path.append(project_dir)

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VueAdmin.settings")
django.setup()

from user.models import SysUser
from django.contrib.auth.hashers import make_password,check_password

# 创建系统角色

admin_user = SysUser.objects.create(username='admin', password=make_password('admin2020'),
                                    role='admin')
admin_user = SysUser.objects.get(username='admin')
print(check_password('admin2020',admin_user.password))