from flask import Blueprint, jsonify, request
import json
import pandas as pd
from algotirhm.algorithm import noiseW
from algotirhm.common.http_util import response_ok
from algotirhm.common.http_util import response_error

noise_cal_api = Blueprint('noise_cal_api', __name__)


@noise_cal_api.route("/do_cal_hj640", methods=["POST"])
def do_cal_hj640():
    req_data = request.get_data()
    if req_data is None:
        return response_error('请求参数为空')
    # 传入的参数为bytes类型，需要转化成json,再用json.loads（）方法，将json数据转化成python对象数据，即dict
    req_data = json.loads(req_data)
    # 将dict数据类型转为DataFrame对象，方便指标计算
    df = pd.DataFrame.from_dict(req_data, orient='index').T
    data = df['data'].values.tolist()
    noise_data = pd.DataFrame(data,
                    columns=['city', 'LEQ', 'year', 'mon', 'day', 'hour', 'min'])

    noise_cal = noiseW.NoiseCal(noise_data)

    result_data = { "day_mean": noise_cal.day_mean(),
                    "night_mean": noise_cal.night_mean(),
                    'noise_mean': noise_cal.noise_mean(),
                    'percent': noise_cal.percent(),
                   }

    # 对参数进行操作
    return response_ok(result_data)