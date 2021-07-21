import json
from algotirhm.common.jsonencoder import BaseJsonEncoder


# 响应json
def response_json(data, status=200):
    return json.dumps(data, ensure_ascii=False, cls=BaseJsonEncoder), status, {"Content-Type": "application/json"}
#ensure_ascii=False：列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False


# 正确响应
def response_ok(data):
    return response_json({'status': '200', 'message': '处理成功', 'data': data}, 200)


# 错误响应
def response_error(message):
    return response_json({'status': 500, 'message': message}, 200)

