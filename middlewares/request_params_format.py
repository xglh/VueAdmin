#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 17:03
# @Author  : liuhui
# @Detail  : 请求参数处理中间件
from django.utils.deprecation import MiddlewareMixin
import json

from VueAdmin.utils import underline_dict, camel_dict


class FormatReqParamsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 处理api接口
        if request.path.startswith('/api'):
            if request.GET:
                request_data = underline_dict(request.GET)
                request.GET = request_data
            if request.body:
                req_body = json.loads(request.body.decode('utf-8'))
                request_data = underline_dict(req_body)
                request._body = json.dumps(request_data).encode('utf-8')

    def process_response(self, request, response):
        # 处理api接口
        if request.path.startswith('/api') and response.status_code == 200:
            try:
                response_data = camel_dict(response.data)
                response.data = response_data
                response._is_rendered = False
                response.render()
            except Exception as e:
                print(e)
        return response
