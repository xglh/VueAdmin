#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/29 11:44
# @Author  : liuhui
# @Detail  : request信息
import re
from rest_framework import HTTP_HEADER_ENCODING

# 获取请求头里的token信息
def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    has_token, token = False, ''
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)

    auth_str = str(auth, encoding='utf-8')
    # 解析token
    p = re.compile('Token\s*(\S*)')
    f = p.findall(auth_str)
    if len(f) > 0:
        has_token = True
        token = f[0]
    return has_token, token