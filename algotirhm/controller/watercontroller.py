from flask import Blueprint, jsonify, request
import json
import pandas as pd
from algotirhm.algorithm import facewaterW, oceanW
from algotirhm.algorithm import groundwaterW
from algotirhm.algorithm import drinkwaterW
from algotirhm.common.http_util import response_ok
from algotirhm.common.http_util import response_error

facewater_cal_api = Blueprint('facewater_cal_api', __name__)


def to_json(data, orient='split'):#不维护列标签的顺序
    data.to_json(orient=orient, force_ascii=False)

# 计算3838评价标准
@facewater_cal_api.route("/do_cal_gb3838", methods=["POST"])#创建一个新的资源
def do_cal_gb3838():
    req_data = request.get_data()#获取数据
    if req_data is None:
        return response_error('请求参数为空')
    # 传入的参数为bytes类型，需要转化成json,再用json.loads（）方法，将json数据转化成python对象数据，即dict
    req_data = json.loads(req_data)
    # 将dict数据类型转为DataFrame对象，方便指标计算
    df = pd.DataFrame.from_dict(req_data, orient='index').T#转置
    data = df['data'].values.tolist()
    water_data = pd.DataFrame(data,
                    columns=['stname', 'lyname', 'rname', 'rsname', 'lsname', 'stcode', 'lycode', 'rcode',
                            'rscode', 'lscode', 'sampc', 'rsc', 'cq', 'year', 'mon', 'day', 'time', 'wd',
                            'wq', 'wss', 'w_cond', 'w_temp', 'ph', 'do', 'sd', 'chla', 'codmn', 'codcr', 'bod5', 'nh4_n',
                            'p_total', 'n_total', 'w_cu', 'w_zn', 'f', 'se', 'as', 'w_hg', 'cd', 'cr6',
                            'w_pb', 'cn_total', 'v_phen', 'oils', 'an_saa', 's', 'colo_org', 'so4', 'cl',
                            'no3_n', 'w_fe', 'w_mn', 'ni', 'vel', 'width', 'depth'])
    water_cal = facewaterW.WaterCal(water_data)

    result_data = { 'itemAmount': water_cal.item_amount(),
                    'itemMax': water_cal.item_max(),
                    'itemMin': water_cal.item_min(),
                    'maxdate': water_cal.maxdate(),
                    'itemAvg': water_cal.item_avg(),
                    'waterLevel': water_cal.water_level(),
                    'allwaterLevel': water_cal.allwaterlevel(),
                    'waterLevelnodo': water_cal.water_level_no_do(),
                    'allwaterLevelnodo': water_cal.allwaterlevel_no_do(),
                    'decideItem': water_cal.decideitem(),
                    'waterRadio': water_cal.waterradio(),
                    'waterStaus': water_cal.waterstatus(),
                    'mainpollute': water_cal.mainpollute(),
                    'hazardAmount': water_cal.hazard_amount(),
                    'hazardpoint': water_cal.hazardpoint(),
                    'hazardRadio': water_cal.hazard_radio(),
                    'overItem': water_cal.overItem(),
                    'hazardMutiple': water_cal.hazard_multiple(),
                    'maxpolluteMultiple': water_cal.max_hazard_multiple(),
                    'compreMultipleAvg': water_cal.comprepolluteavg(),
                    'polluteIndex': water_cal.polluteIndex(),
                    'ComprePollute': water_cal.comprepollute(),
                    'polluteIndexavg': water_cal.comprepolluteavg(),
                    'ShareRadio': water_cal.share(),
                    'singleIndex': water_cal.singleIndex(),
                    'waterQuantity': water_cal.waterquantity(),
                    'reachWaterQuantity': water_cal.reachwaterquantity(),
                    'levelIndex': water_cal.level_index(),
                    'originIndex': water_cal.origin_index(),
                    'NutriIndex': water_cal.Nutri_index(),
                    'NutriLevel': water_cal.hk_NutriLevel(),
                    'spearmanIndex': water_cal.spearman()
                   }
    
    # 对参数进行操作
    return response_ok(result_data)


drinkwater_cal_api = Blueprint('drinkwater_cal_api', __name__)

#'三氯甲烷', '四氯化碳', '三溴甲烷', '二氯甲烷', '1,2-二氯乙烷', '环氧氯丙烷', '氯乙烯',
# '1,1-二氯乙烯', '1,2-二氯乙烯', '三氯乙烯', '四氯乙烯', '氯丁二烯', '六氯丁二烯', '苯乙烯',
# '甲醛', '乙醛', '丙烯醛', '三氯乙醛', '苯', '甲苯', '乙苯', '二甲苯', '异丙苯', '氯苯', '1,2-二氯苯',
# '1,4-二氯苯', '三氯苯', '四氯苯', '六氯苯', '硝基苯', '二硝基苯', '2,4-二硝基甲苯', '2,4,6-三硝基甲苯',
# '硝基氯苯', '2,4-二硝基氯苯', '2,4-二氯苯酚', '2,4,6-三氯苯酚', '五氯酚', '苯胺', '联苯胺', '丙烯酰胺',
# '丙烯腈', '邻苯二甲酸二丁酯', '邻苯二甲酸二（2-乙基己基）酯', '水合肼', '四乙基铅', '吡啶', '松节油', '苦味酸',
# '丁基黄原酸', '活性氧', '滴滴涕', '林丹', '环氧七氯', '对硫磷', '甲基对硫磷', '马拉硫磷', '乐果', '敌敌畏',
# '敌百虫', '内吸磷', '百菌清', '甲萘威', '溴氰菊酯(阿特拉津)', '阿特拉津', '苯并花', '甲基苯', '多氯联苯', '微囊藻毒素-LR',
# '黄磷', '钼', '钴', '铍', '硼', '锑', '镍', '钡', '钒', '钛', '铊'，'硫酸盐', '氯化物','硝酸盐','铁','锰'
# 计算gb5749评价标准
@drinkwater_cal_api.route("/do_cal_gb5749", methods=["POST"])
def do_cal_gb5749():
    req_data = request.get_data()
    if req_data is None:
        return response_error('请求参数为空')
    # 传入的参数为bytes类型，需要转化成json,再用json.loads（）方法，将json数据转化成python对象数据，即dict
    req_data = json.loads(req_data)
    # 将dict数据类型转为DataFrame对象，方便指标计算
    df = pd.DataFrame.from_dict(req_data, orient='index').T
    data = df['data'].values.tolist()
    drinkwater_data = pd.DataFrame(data,
    columns=['stname', 'lyname', 'rname', 'rsname', 'lsname',
             'stcode', 'lycode', 'rcode', 'rscode', 'lscode',
             'sampc', 'rsc', 'cq', 'year', 'mon', 'day', 'time',
             'wd', 'wq', 'ph', 'sd', 'chla', 'codmn', 'nh4_n', 'p_total', 'n_total', 'w_cu',
             'w_zn', 'f', 'se', 'as', 'w_hg', 'cd',
             'cr6', 'w_pb', 'cn_total', 'v_phen', 'an_saa',
             's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn',
             'trichlo', 'car-tetr', 'ben', 'methyl', 'dioct', 'mo', 'ni', 'ta', 'mix', 'no2_n', 'hard', 'co', 'be', 'b',
             'colo_total', 'coloursd', 'smells', 'visable', 'w_na', 'disolvesolid', 'w_al',
             'bateria_total', 'w_i', 'alfa', 'belta'
    ])

    drinkwater_data.fillna(drinkwater_data.mean())

    drinkwater_cal = drinkwaterW.DrinkWaterCal(drinkwater_data)
    result_data = { 'itemAmount': drinkwater_cal.item_amount(),
                    'itemMax': drinkwater_cal.item_max(),
                    'itemMin': drinkwater_cal.item_min(),
                    'maxdate': drinkwater_cal.maxdate(),
                    'itemAvg': drinkwater_cal.item_avg(),
                    'waterLevel': drinkwater_cal.water_level(),
                    'allwaterLevel': drinkwater_cal.allwaterlevel(),
                    'waterRadio': drinkwater_cal.waterradio(),
                    'waterStaus': drinkwater_cal.water_status(),
                    'mainpollute': drinkwater_cal.mainpollute(),
                    'hazardAmount': drinkwater_cal.hazard_amount(),
                    # 'hazardpoint': drinkwater_cal.hazardpoint(),
                    # 'hazardRadio': drinkwater_cal.hazard_radio(),
                    'overItem': drinkwater_cal.overItem(),
                    'hazardMutiple': drinkwater_cal.hazard_multiple(),
                    'polluteIndex': drinkwater_cal.polluteIndex(),
                    'ComprePollute': drinkwater_cal.comprepollute(),
                    'polluteIndexavg': drinkwater_cal.comprepolluteavg(),
                    'ShareRadio': drinkwater_cal.share(),
                    'singleIndex': drinkwater_cal.singleIndex(),
                    'waterQuantity': drinkwater_cal.waterquantity(),
                    # 'reachWaterQuantity': drinkwater_cal.reachwaterquantity(),
                    'levelIndex': drinkwater_cal.level_index(),
                    'originIndex': drinkwater_cal.origin_index(),
                    'NutriIndex': drinkwater_cal.Nutri_index(),
                    'NutriLevel': drinkwater_cal.hk_NutriLevel(),
                    'spearmanIndex': drinkwater_cal.spearman()
                   }

    # 对参数进行操作
    return response_ok(result_data)


groundwater_cal_api = Blueprint("groundwater_cal_api", __name__)
# 计算14848评价标准


@groundwater_cal_api.route("/do_cal_gb14848", methods=["POST"])
def do_cal_gb14848():
    req_data = request.get_data()
    if req_data is None:
        return response_error("请求参数为空")
    # 传入的参数为bytes类型，需要转化成json,再用json.loads（）方法，将json数据转化成python对象数据，即dict
    req_data = json.loads(req_data)
    # 将dict数据类型转为DataFrame对象，方便指标计算
    df = pd.DataFrame.from_dict(req_data, orient="index").T
    data = df["data"].values.tolist()
    groundwater_data = pd.DataFrame(data,
                                    columns=['rname', 'lsname', 'rsname', 'ph', 'year', 'mon', 'day', 'time', 'codmn',
                                             'nh4_n', 'w_cu', 'w_zn', 'f', 'se', 'as', 'w_hg', 'cd', 'cr6', 'w_pb',
                                             'cn_total', 'v_phen', 'an_saa', 's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn',
                                             'chcl3', 'ccl4', 'methy', 'meth', 'sym-dich', 'vinyl', '11-vinyl',
                                             '12-vinyl', '3-trich', '4-trich', 'styrene', 'ben', 'toluene', 'ethyl',
                                             'dimeth', 'chloroben', '12-dichl', '14-dichl', '123-dichl', 'hcb',
                                             '24-dini', '246-tcp', 'pcp', 'dehp', 'ddt', 'r-hexa', 'chnops', 'chops',
                                             'dime', 'ddvp', 'chloro', 'mo', 'sb', 'ni', 'ti',
                                             'td', 'no2_n', 'total_hardness', 'dich', 'benzo', 'atra', 'co',
                                             'be', 'b', 'ba', 'total_colo', 'pcbs', 'color', 'smell',
                                             'macro', 'na', '111-trich', 'naph', 'b-benzo', 'chlorp', 'hexa',
                                             'carb', 'dissolved_solids', 'al', 'cfu', 'i', 'total_α',  'total_β',
                                             'ag', '112-trich', 'anth', 'fluor', 'glyp', '26-dini', 'aldi',
                                             'hepta', '24-dichl'])
    groundwater_data["time"] = groundwater_data["year"].map(str) + '.' + groundwater_data["mon"].map(str) + '.' \
        + groundwater_data["day"].map(str)
    groundwater_data.drop(['year', 'mon', 'day'], axis=1, inplace=True)
    groundwater_cal = groundwaterW.GroundWaterCal(groundwater_data)
    result_data = {"item_avg": groundwater_cal.item_avg(),
                   'item_waterLevel': groundwater_cal.water_level(),
                   'all_water_level': groundwater_cal.all_water_level(),
                   'water_score': groundwater_cal.score(),
                   'com_score': groundwater_cal.comp_score(),
                   'item_quality': groundwater_cal.quality(),
                   'pollute_index': groundwater_cal.comp_pollute_index(),
                   # 'over_item': groundwater_cal.over_item(),
                   # 'index_over_rate': groundwater_cal.index_over_rate(),
                   # 'non_exceed__rate': groundwater_cal.non_exceed_rate(),
                   # 'main_pollute': groundwater_cal.main_pollute(),
                   # 'meet_stand': groundwater_cal.meet_standard(),
                   # 'decide_item': groundwater_cal.decide_item(),
                   # 'hazard_multiple': groundwater_cal.hazard_multiple(),
                   }

    # 对参数进行操作
    return response_ok(result_data)


ocean_cal_api = Blueprint('ocean_cal_api', __name__)


# 计算HJ442-2008评价标准
@ocean_cal_api.route("/do_cal_hj442", methods=["POST"])
def do_cal_hj442():
    req_data = request.get_data()
    if req_data is None:
        return response_error('请求参数为空')
    # 传入的参数为bytes类型，需要转化成json,再用json.loads（）方法，将json数据转化成python对象数据，即dict
    req_data = json.loads(req_data)
    # 将dict数据类型转为DataFrame对象，方便指标计算
    df = pd.DataFrame.from_dict(req_data, orient='index').T
    data = df['data'].values.tolist()
    ocean_data = pd.DataFrame(data,
                              columns=["rname", "rsname", "lsname", "year", "mon", "day", "time", "w_temp", "ph",
                                       "do", "codcr", "nh4_n", "w_cu", "w_zn", "as", "w_hg", "cd",
                                       "w_pb", "oils", "no3_n", "wss", "san", "no2_n", "po4", "n_inorganic"])
    ocean_data["time"] = ocean_data["year"].map(str) + '.' + ocean_data["mon"].map(str) + '.'\
        + ocean_data["day"].map(str)
    ocean_data.drop(['year', 'mon', 'day'], axis=1, inplace=True)

    ocean_cal = oceanW.OceanCal(ocean_data)

    result_data = {'itemAmount': ocean_cal.item_amount(),
                   'itemOver_amount': ocean_cal.item_over_amount(),
                   'iteamAvg': ocean_cal.item_avg(),
                   'excessItem': ocean_cal.excess_item(),
                   'mainpollute': ocean_cal.main_pollute(),
                   'itemExcess_rate': ocean_cal.excess_rate(),
                   'itemExcess_multiple': ocean_cal.excess_multiple(),
                   "itemWater_level": ocean_cal.water_level(),
                   "itemWaterpercent": ocean_cal.water_level_percent(),
                   "itemMainWaterpercent": ocean_cal.main_water_level(),
                   "water_grade": ocean_cal.water_grade(),
                   'itemPollu_index': ocean_cal.pollu_index(),
                   "inorganicN": ocean_cal.inorganic_n(),
                   "nonIron_an": ocean_cal.non_iron_an(),
                   'itemNutri_index': ocean_cal.nutri_index(),
                   'itemNutri_grade': ocean_cal.nutri_grade(),
                   'itemSedimentLevel': ocean_cal.sediment_level(),
                   'itemSedimentLevelPercent': ocean_cal.sediment_levelpercent(),
                   'itemSedimentQuality': ocean_cal.sediment_quality(),
                   "itemMainSedimentLevel": ocean_cal.main_sediment_percent(),
                   'comp_pollu_index': ocean_cal.comp_pollute_index()
                   }

    # 对参数进行操作
    return response_ok(result_data)




