# coding:utf-8
# 基类
# json序列化与反序列化基类
import math
from django.db import models
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from VueAdmin.basic import CassResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import exception_handler
from django.conf import settings


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    create_timestamp = models.DateTimeField(null=True)
    last_edit_timestamp = models.DateTimeField(null=True)

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


# 自定义异常返回数据结构
def rest_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['code'] = response.status_code
        response.data['success'] = False
        response.data['message'] = response.data['detail']
        response.data['data'] = {}
        # 去掉detail信息
        response.data.pop('detail')
    return response


def xops_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        msg = '失败' if response.status_code >= 400 else '成功'
        notification_response = dict()
        notification_response['code'] = response.status_code
        notification_response['message'] = msg
        notification_response['detail'] = response.data
        response.data = notification_response
    return response


class CommonPagination(PageNumberPagination):
    """
    分页设置
    """
    page_size = 100
    page_size_query_param = 'size'

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
        except:
            self.page = paginator.page(math.ceil(paginator.count / page_size))
        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


class RbacPermission(BasePermission):
    """
    自定义权限
    """

    @classmethod
    def get_permission_from_role(self, request):
        try:
            perms = request.user.roles.values(
                'permissions__method',
            ).distinct()
            return [p['permissions__method'] for p in perms]
        except AttributeError:
            return None

    def has_permission(self, request, view):
        perms = self.get_permission_from_role(request)
        if perms:
            if 'admin' in perms:
                return True
            elif not hasattr(view, 'perms_map'):
                return True
            else:
                perms_map = view.perms_map
                _method = request._request.method.lower()
                for i in perms_map:
                    for method, alias in i.items():
                        if (_method == method or method == '*') and alias in perms:
                            return True


class ObjPermission(BasePermission):
    """
    密码管理对象级权限控制
    """

    def has_object_permission(self, request, view, obj):
        perms = RbacPermission.get_permission_from_role(request)
        if 'admin' in perms:
            return True
        elif request.user.id == obj.uid_id:
            return True


class TreeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)


class TreeAPIView(ListAPIView):
    """
    自定义树结构View
    """
    serializer_class = TreeSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        tree_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                else:
                    tree_data.append(tree_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return CassResponse(results)
