from flask import Blueprint, jsonify, request
import json
import pandas as pd
from algotirhm.algorithm import airW
from algotirhm.algorithm import acidrain
from algotirhm.common.http_util import response_ok
from algotirhm.common.http_util import response_error

air_cal_api = Blueprint('air_cal_api', __name__)


@air_cal_api.route("/do_cal_hj633", methods=["POST"])
def do_cal_hj633():
    req_data = request.get_data()
    if req_data is None:
        return response_error('请求参数为空')
    # 传入的参数为bytes类型，需要转化成json,再用json.loads（）方法，将json数据转化成python对象数据，即dict
    req_data = json.loads(req_data)
    # 将dict数据类型转为DataFrame对象，方便指标计算
    df = pd.DataFrame.from_dict(req_data, orient='index').T
    data = df['data'].values.tolist()
    air_data = pd.DataFrame(data, columns=['rname', 'city', 'so2', 'no2', 'co', 'o3', 'pm25', 'pm10', 'year', 'mon',
                                           'day', 'hour'])
    air_cal =airW.AirCal(air_data)
    result_data = { 'pollute_fzs': air_cal.pollute_fzs(),
                    'aqi': air_cal.aqi(),
                    'first_pollute': air_cal.first_pollute(),
                    'aqi_quality': air_cal.aqi_quality(),
                    'aqi_level': air_cal.aqi_level(),
                    'single_index': air_cal.single_index(),
                    'max_quality_index': air_cal.max_quality_index(),
                    'sum_quality_index': air_cal.sum_quality_index(),
                    'beyond_pollute': air_cal.beyond_pollute(),
                    'hazard_multiple': air_cal.hazard_multiple(),
                    'point_hour_mean': air_cal.point_hour_mean(),
                    'point_o3_8h': air_cal.point_o3_8h(),
                    'point_day_mean': air_cal.point_day_mean(),
                    #'point_quarter_mean': air_cal.point_quarter_mean(),
                    'point_year_mean': air_cal.point_year_mean(),
                    'city_hour_mean': air_cal.city_hour_mean(),
                    'city_day_mean': air_cal.city_day_mean(),
                    'city_year_mean': air_cal.city_year_mean(),
                    'city_year_percent': air_cal.city_year_percent(),
                    'non-exceed_percent_hour': air_cal.non_exceed_percent_hour(),
                    'non_exceed_percent_day': air_cal.non_exceed_percent_day(),
                    'spearman': air_cal.speraman()
                   }

    # 对参数进行操作
    return response_ok(result_data)



acidrain_cal_api = Blueprint('acidrain_cal_api', __name__)
# 计算HJ442-2008评价标准
@acidrain_cal_api.route("/do_cal_qx372", methods=["POST"])
def do_cal_qx372():
    req_data = request.get_data()
    if req_data is None:
        return response_error('请求参数为空')
    # 传入的参数为bytes类型，需要转化成json,再用json.loads（）方法，将json数据转化成python对象数据，即dict
    req_data = json.loads(req_data)
    # 将dict数据类型转为DataFrame对象，方便指标计算
    df = pd.DataFrame.from_dict(req_data, orient='index').T
    data = df['data'].values.tolist()
    acidrain_data = pd.DataFrame(data,
                              columns=["序号", "测点编号", "测点名称", "所属行政区", "降雨类型", "降水量", "ph值", "是否酸雨", "创建时间"])
    # acidrain_data["time"] = acidrain_data["year"].map(str) + '.' + acidrain_data["mon"].map(str) + '.'\
    #     + acidrain_data["day"].map(str) + '.' + acidrain_data["time"].map(str)
    # acidrain_data.drop(['year', 'month', 'day','time'], axis=1, inplace=True)

    acidrain_cal = acidrain.AirCal(acidrain_data)

    result_data = {'itemAmount': acidrain_cal.item_amount(),
                   'AvgPh': acidrain_cal.pH_avg(),
                   'AcidRain': acidrain_cal.acid_rain(),
                   'GradeOfAcidRain': acidrain_cal.grade_of_acid_rain(),
                   'AcidRainArea': acidrain_cal.acid_rain_area(),
                   'AcidRainAreaLevel': acidrain_cal.acid_rain_area_level(),
                   'FrequencyOfAcidRain': acidrain_cal.frequency_of_acid_rain(),
                   'FrequencyOfAcidRainLevel': acidrain_cal.frequency_of_acid_rain_level(),
                   }

    # 对参数进行操作
    return response_ok(result_data)