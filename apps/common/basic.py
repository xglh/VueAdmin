#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 14:24
# @Author  : liuhui
# @Detail  :
import math
from django.core.paginator import Page, EmptyPage
from django.db import models
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_edit_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class JsonSerializer:

    def to_json(self):
        jsonData = {}
        for name, value in vars(self).items():
            if not name.startswith("_"):
                jsonData[name] = value
        return jsonData

    def get_from_json(self, jsonData):
        if jsonData is not None:
            for name, value in vars(self).items():
                if jsonData.get(name) is not None:
                    setattr(self, name, jsonData.get(name))
        return self

    def get_field_name(self):
        field_list = []
        for name, value in vars(self).items():
            if not name.startswith("_"):
                field_list.append(name)
        return field_list


# 响应基类
class BaseResponse(JsonSerializer):

    def __init__(self):
        self.code = 200
        self.success = True
        self.message = "success"
        self.data = {}

    def set_error_response(self, code=-100, message='error', data={}):
        self.code = code
        self.message = message
        self.success = False
        self.data = data

    def set_http_500_response(self, message='error', data={}):
        self.code = 500
        self.message = message
        self.success = False
        self.data = data


class MyPageNumberPagination(PageNumberPagination):
    # 默认page数
    page_size = 20
    # 指定size参数
    page_size_query_param = 'size'
    # 执行page参数
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        try:
            self.page = paginator.page(page_number)
        except EmptyPage:
            # 构造空page
            self.page = Page([], 0, paginator)

        self.request = request
        return list(self.page)


class BaseModelViewSet(ModelViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = BaseResponse()
        response.data = serializer.data
        return Response(response.to_json())

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = BaseResponse()
        response.data = serializer.data
        return Response(response.to_json())

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        response = BaseResponse()
        response.data = serializer.data
        return Response(response.to_json())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = BaseResponse()
        return Response(response.to_json())

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        response = BaseResponse()
        response.data = {
            'total': queryset.count(),
            'rows': serializer.data
        }
        return Response(response.to_json())
