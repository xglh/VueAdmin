from rest_framework.views import exception_handler

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
