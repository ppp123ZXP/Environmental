import json
import pandas


# json编码器
class BaseJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        import numpy
        if isinstance(obj, numpy.integer):#整数
            return int(obj)
        elif isinstance(obj, numpy.floating):#浮点数
            return float(obj)
        elif isinstance(obj, numpy.ndarray):#isinstance：判断一个对象是否是一个已知的类型
            return obj.tolist()#数组转化为列表
        else:
            return super(BaseJsonEncoder, self).default(obj)

