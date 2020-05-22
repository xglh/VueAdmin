# coding:utf-8
# 基类
# json序列化与反序列化基类
from rest_framework.pagination import PageNumberPagination


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
