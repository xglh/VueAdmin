#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/27 15:25
# @Author  : liuhui
# @Detail  :
import django.utils.timezone as timezone
from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_edit_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True