# "stname":"测站名称",
# "lyname":"流域名称",
# "rname":"河流名称",
# "rsname":"断面名称",
# "lsname":"垂线名称",
# "stcode":测站代码,
# "lycode":"流域代码",
# "rcode":河流代码,
# "rscode":"断面代码",
# "lscode":"垂线代码",
# "sampc":采样点位置,
# "rsc":水期代码,
# "cq":潮期,
# "year":年,
# "mon":月,
# "day":日,
# "time":"采样时间",
# "wd":水位,
# "wq":流量,
# 'color':色
# 'smell':'嗅和味'
# 'td':'浑浊度'
# 'macro':'肉眼可见物'
# 'total_hardness':'总硬度
# 'dissolved_solids':'溶解性总固体'
# 'so4':'硫酸盐'
# 'cn_total':'氰化物'
# 'w_fe':'铁'
# 'w_mn':'锰'
# 'w_cu':'铜'
# 'w_zn':'锌'
# 'mo':'钼'
# 'v_phen':'挥发性酚类'
# 'an_saa' :'阴离子表面活性剂'
# 'cod':'耗氧量'
# 'nh4_n' :'氨氮'
# 's':'硫化物'
# 'na' : '钠'
# 'total_colo' :'总大肠杆菌群'
# 'cfu': '菌落总数'
# 'no2_n': '亚硝酸盐'
# 'no3_n':'硝酸盐'
# 'cn_total':'氰化物'
# 'f':'氟化物'
# 'i':'碘化物'
# 'w_hg':'汞'
# 'as':'砷'
# 'se':'硒'
# 'cd' :'镉'
# 'cr6':'铬（六价）'
# 'w_pb': '铅'
# 'chcl3':'三氯甲烷'
# 'ccl4' :'四氯化碳'
# 'ben': '苯'
# 'toluene' :'甲苯'
# 'total_α': '总α放射性'
# 'total_β': '总β放射性'
# '铍' :"be"
# '硼': "b"
# '锑':"sb"
# '钡':"ba"
# '镍':"ni"
# '钴':"co"
# '钼':"mo"
# '银':"ag"
# '铊':"ti"
# '二氯甲烷':"meth"
# '1,2-二氯乙烷':"sym-dich"
# '1,1,1-三氯乙烷':"111-trich"
# '1,1,2-三氯乙烷':"112-trich"
# '1,2-二氯丙烷':"dich"
# '三溴甲烷':"methy"
# '氯乙烯':"vinyl"
# '1,1-二氯乙烯':"11-vinyl"
# '1,2-二氯乙烯':"12-vinyl"
# '三氯乙烯':"3-trich"
# '四氯乙烯':"4-trich"
# '氯苯':"chloroben"
# '邻二氯苯':"12-dichl"
# '对二氯苯':"14-dichl"
# '三氯苯':"123-dichl"
# '乙苯':"ethyl"
# '二甲苯':"dimeth"
# '苯乙烯':"styrene"
# '2,4-二硝基甲苯': "24-dini"
# '2,6-二硝基甲苯': "aldi"
# '萘':"naph"
# '蒽':"anth"
# '荧蒽':"fluor"
# '苯并荧蒽':"b-benzo"
# '苯并芘':"benzo"
# '多氯联苯':"pcbs"
# '邻苯二甲酸二（2-乙基巳基）酯':"dehp"
# '2,4,6-三氯酚' :"246-tcp"
# '五氯酚':"pcp"
# '六六六':"hexa"
# 'r-六六六':"r-hexa"
# '滴滴涕':"ddt"
# '六氯苯':"hcb"
# '七氯':"hepta"
# '2,4-滴':"24-dichl"
# '克百威':"carb"
# '涕灭威':"aldi"
# '敌敌畏': "ddvp"
# '甲基对硫磷':"chnops"
# '马拉硫磷':"chops"
# '乐果':"dime"
# '毒死蜱': "chlorp"
# '百菌清':"chloro"
# '莠去津':"atra"
# '草甘膦':"glyp"

import pandas as pd
import numpy as np
import math
import algotirhm.common.standard as std
import json

class GroundWaterCal(object):

    cacheDict = {}

    def __init__(self, data):
        self.data = data

    def showdata(self):  # 展示数据概况
        return self.data

    def ph_avg(self):
        # pH值是无量纲指标，所以先要讲pH值转化为H离子浓度再求平均值，然后再转化成pH值的平均值
        sum1 = 0
        ph = 0
        for i in self.data["ph"]:
            i = 10 ** (-i)
            sum1 += i
            ph = -math.log10(sum1 / self.data["rname"].count())
        return ph

    def total_colo_avg(self):
        for i in self.data["total_colo"]:
            sum1 = 0
            sum1 += math.log10(i)
            total_colo_avg = 10 ** (sum1 / self.data["rname"].count())
            return total_colo_avg

# 1、平均值
    def item_avg(self):
        data = self.data
        data = data.dropna(axis=1)
        item_avg = data.mean()
        item_avg["ph"] = GroundWaterCal.ph_avg(self)
        item_avg["total_colo"] = GroundWaterCal.total_colo_avg(self)
        item_avg = GroundWaterCal.adjust(self, item_avg)
        self.cacheDict.update({"avg": item_avg})
        return item_avg

# 2、水质类别
    def water_level(self):
        dict1 = {}
        stdata = std.get_standard('do_cal_gb14848')
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'smell')].index)
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'macro')].index)
        item_avg = self.cacheDict.get("avg")
        for i in stdata["item"]:
            if float(item_avg[i]) <= float(stdata[stdata['item'] == i]['I'].values):
                dict1.update({i: "I类"})
            elif float(item_avg[i]) <= float(stdata[stdata['item'] == i]['II'].values):
                dict1.update({i: "II类"})
            elif float(item_avg[i]) <= float(stdata[stdata['item'] == i]['III'].values):
                dict1.update({i: "III类"})
            elif float(item_avg[i]) <= float(stdata[stdata['item'] == i]['IV'].values):
                dict1.update({i: "IV类"})
            else:
                dict1.update({i: "V类"})
        if 'total_α' in item_avg:
            if item_avg['total_α'] > 0.5:
                dict1.update({'total_α': 'IV类'})
        if 'total_β' in item_avg:
            if item_avg['total_β'] > 0.1:
                dict1.update({'total_β': 'IV类'})
        if 6.5 <= item_avg['ph'] <= 8.5:
            dict1.update({'ph': 'I类'})
        elif 5.5 <= item_avg['ph'] < 6.5 or 8.5 < item_avg['ph'] <= 9.0:
            dict1.update({'ph': 'IV类'})
        else:
            dict1.update({'ph': 'V类'})
        if 'smell' in item_avg:
            if item_avg['smell'] == 0:
                dict1.update({'smell': 'I类'})
            else:
                dict1.update({'smell': 'V类'})
        if 'macro' in item_avg:
            if item_avg['macro'] == 0:
                dict1.update({'macro': 'I类'})
            else:
                dict1.update({'macro': 'V类'})
        self.cacheDict.update({"water_level": dict1})
        return dict1

# 3、 断面水质类别
    def all_water_level(self):
        lst = []
        temp = self.cacheDict.get("water_level")
        for k,v in temp.items():
            if v == "V类":
                lst.append(5)
            elif v == "IV类":
                lst.append(4)
            elif v == "III类":
                lst.append(3)
            elif v == "II类":
                lst.append(2)
            elif v == "I类":
                lst.append(1)
        lst.sort(reverse=True)
        if lst[0] == 5:
            all = "V类"
        elif lst[0] == 4:
            all = "IV类"
        elif lst[0] == 3:
            all = "III类"
        elif lst[0] == 2:
            all = "II类"
        elif lst[0] == 1:
            all = "I类"
        self.cacheDict.update({"allwaterlevel": all})
        return all

# 4、得分
    def score(self):
        dict1 = {}
        stdata = std.get_standard('do_cal_gb14848')
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'smell')].index)
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'macro')].index)
        item_avg = self.cacheDict.get("avg")
        for i in item_avg:
            if item_avg[i] <= stdata[stdata['item'] == i]['I'].values:
                dict1.update({i: 0})
            elif item_avg[i] <= stdata[stdata['item'] == i]['II'].values:
                dict1.update({i: 1})
            elif item_avg[i] <= stdata[stdata['item'] == i]['III'].values:
                dict1.update({i: 3})
            elif item_avg[i] <= stdata[stdata['item'] == i]['IV'].values:
                dict1.update({i: 6})
            else:
                dict1.update({i: 10})
        if 'total_α' in item_avg:
            if item_avg['total_α'] > 0.5:
                dict1.update({'total_α': 6})
        if 'total_β' in item_avg:
            if item_avg['total_β'] > 0.5:
                dict1.update({'total_β': 6})
        if 6.5 <= item_avg['ph'] <= 8.5:
            dict1.update({'ph': 0})
        elif 5.5 <= item_avg['ph'] < 6.5 or 8.5 < item_avg['ph'] <= 9.0:
            dict1.update({'ph': 6})
        else:
            dict1.update({'ph': 10})
        if 'smell' in item_avg:
            if item_avg['smell'] == 0:
                dict1.update({'smell': 0})
            else:
                dict1.update({'smell': 10})
        if 'macro' in item_avg:
            if item_avg['macro'] == 0:
                dict1.update({'macro': 0})
            else:
                dict1.update({'macro': 10})
        self.cacheDict.update({"score": dict1})
        return dict1

# 5、综合评价分值
    def comp_score(self):
        df = self.cacheDict.get("score")
        a = 0
        c = 0
        for i in df.keys():
            b = df[i]
            c = c + b
            if b > a:
                a = b
        data = round(np.sqrt((a ** 2 + (c / len(df.keys())) ** 2) / 2), 2)
        self.cacheDict.update({"comp_score": data})
        return data

# 6、地下水水质
    def quality(self):
        a = self.cacheDict.get("comp_score")
        if a <= 0.8:
            waterq = '优良'
        elif a <= 2.5:
            waterq = '良好'
        elif a <= 4.25:
            waterq = '较好'
        elif a <= 7.5:
            waterq = '较差'
        else:
            waterq = '极差'
        self.cacheDict.update({"quality":waterq})
        return waterq

# ph污染指数
    def ph_pollute(self):
        temp = self.cacheDict.get("avg")
        ph_pollute = abs(temp['ph'] - 7.5) / 1.5
        self.cacheDict.update({"ph_pollute": ph_pollute})
        return ph_pollute

# 7、综合污染指数
    def comp_pollute_index(self):
        stdata = std.get_standard('do_cal_gb14848')
        sum1 = 0
        item_avg = self.cacheDict.get("avg")
        temp = self.cacheDict.get("ph_pollute")
        for i in stdata["item"]:
            if i != 'ph' and i != 'macro' and i != 'smell':
                poll = item_avg[i] / float(stdata[stdata['item'] == i]['III'].values)
                sum1 += poll
        ph = abs(item_avg[i] - 7.5) / 1.5
        sum1 += ph
        sum1 = round(sum1, 2)
        self.cacheDict.update({"com_pollute_index": sum1})
        return sum1

# 8、超标项目
    def over_item(self):
        stdata = std.get_standard('do_cal_gb14848')
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'smell')].index)
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'macro')].index)
        lst = []
        item_avg = self.cacheDict.get("avg")
        for i in item_avg:
            if item_avg[i] > stdata[stdata['item'] == i]['III'].values:
                lst.append(i)
        if 'total_α' in item_avg:
            if item_avg['total_α'] > 0.5:
                lst.append('total_α')
        if 'total_β' in item_avg:
            if item_avg['total_β'] > 0.1:
                lst.append('total_β')
        if item_avg['ph'] < 6.5 or item_avg['ph'] > 8.5:
            lst.append('ph')
        if 'smell' in item_avg:
            if item_avg['smell'] > 0:
                lst.append('smell')
        if 'macro' in item_avg:
            if item_avg['macro'] > 0:
                lst.append('macro')
        lst = list(set(lst))
        self.cacheDict.update({"over_item": lst})
        return lst

# 9、评价指标超标率
    def index_over_rate(self):
        stdata = std.get_standard('do_cal_gb14848')
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'smell')].index)
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'macro')].index)
        sum1 = 0
        data = self.data
        for i in stdata['item']:
            if data[i].values[0] >= stdata[stdata['item'] == i]['III'].values[0]:
                sum1 += 1
        if sum1 > 0:
            return 1
        else:
            return 0

# 10、评价达标率(平均值）
    def non_exceed_rate(self):
        stdata = std.get_standard('do_cal_gb14848')
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'smell')].index)
        stdata = stdata.drop(index=stdata.loc[(stdata['item'] == 'macro')].index)
        sum1 = 0
        item_avg = self.cacheDict.get("avg")
        for i in item_avg:
            if item_avg[i] <= stdata[stdata['item'] == i]['III'].values:
                sum1 += 1
        if 6.5 <= item_avg['ph'] <= 8.5:
            sum1 += 1
        if 'smell' in item_avg:
            if item_avg['smell'] == 0:
                sum1 += 1
        if 'macro' in item_avg:
            if item_avg['macro'] == 0:
                sum1 += 1
        amount = len(item_avg)
        rate = round(sum1 / amount, 2)
        self.cacheDict.update({"non_exceed_rate": rate})
        return rate

    # 14、 超标倍数
    def hazard_multiple(self):
        stdata = std.get_standard('do_cal_gb14848')
        dict1 = {}
        dict2 = {}
        a = self.cacheDict.get("over_item")
        b = self.cacheDict.get("avg")
        for i in a:
            maxmultiple = (b[i] - stdata[stdata['item'] == i]['III']) / stdata[stdata['item'] == i]['III'].values
            for x in maxmultiple:
                dict1.update({i: round(x, 2)})
        self.cacheDict.update({"hazard_multiple": dict1})
        return dict1

# 11、主要污染物
    def main_pollute(self):
        lst1 = []
        lst2 = []
        lst3 = []
        a = self.cacheDict.get("over_item")
        b = self.cacheDict.get("hazard_multiple")
        if len(a) == 0:
            return lst1
        else:
            for i in a:
                lst1.append(i)
                lst2.append(GroundWaterCal.hazard_multiple(self)[i])
            df = pd.DataFrame(index=lst1)
            df['value'] = lst2
            df = df.sort_values(by='value', ascending=False)
            if len(df) > 3:
                df = df.iloc[0:3]
                for v1 in df.index:
                    lst3.append(v1)
            else:
                for v2 in df.index:
                    lst3.append(v2)
            self.cacheDict.update({"main_pollute": lst3})
            return lst3

# 12、评价是否达标
    def meet_standard(self):
        if self.cacheDict.get("non_exceed_rate") == 1:
            a = '达标'
        else:
            a = '不达标'
        self.cacheDict.update({"meet_standard": a})
        return a

# 13、定类项目:决定水质类别的污染物
    def decide_item(self):
        dict2 = self.cacheDict.get("water_level")
        lst = []
        a = self.cacheDict.get("all_water_level")
        for key, values in dict2.items():
            if values == a:
                lst.append(key)
        self.cacheDict.update({"decide_item": lst})
        return lst

    # 数据的精度
    def adjust(self, dict):
        dict1 = {}
        self.dict = dict
        for k, v in self.dict.items():
            if k == "color":  # 色度
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "smell":  # 嗅和味
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "ph":  # pH
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "td":  # 浑浊度
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "macro":  # 肉眼可见物
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "total_hardness":  # 总硬度
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "dissolved_solids":  # 可溶性固体
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "so4":  # 硫酸盐
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "cl":  # 氯化物
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "w_fe":  # 铁
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "w_mn":  # 锰
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_cu":  # 铜
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_zn":  # 锌
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "al":  # 铝
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "v_phen":  # 挥发酚
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "an_saa":  # 阴离子表面活性剂
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "codmn":  # 耗氧量
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "nh4_n":  # 氨氮
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "s":  # 硫化物
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "na":  # 钠
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "total_colo":  # 总大肠杆菌
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "cfu":  # 菌落总数
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "no2_n":  # 亚硝酸盐
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "no3_n":  # 硝酸盐
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "cn_total":  # 氰化物
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "f":  # 氟化物
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "i":  # 碘化物
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_hg":  # 汞
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "as":  # 砷
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "se":  # 硒
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "cd":  # 镉
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "cr6":  # 铬
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "w_pb":  # 铅
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "chcl3":  # 三氯甲烷
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "ccl4":  # 四氯化碳
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "ben":  # 苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "toluene":  # 甲苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "total_α":  # 总α放射性
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "total_β":  # 总β放射性
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "be":  # 铍
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "b":  # 硼
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "sb":  # 锑
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "ba":  # 钡
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "ni":  # 镍
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "co":  # 钴
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "mo":  # 钼
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "ag":  # 银
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "ti":  # 铊
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "meth":  # 二氯甲烷
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "sym-dich":  # 1,2-二氯乙烷
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "111-trich":  # 1,1,1-三氯乙烷
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "112-trich":  # 1,1,2-三氯乙烷
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "dich":  # 1,2-二氯丙烷
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "methy":  # 三溴甲烷
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "vinyl":  # 氯乙烯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "11-vinyl":  # 1,1-二氯乙烯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "12-vinyl":  # 1,2-二氯乙烯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "3-trich":  # 三氯乙烯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "4-trich":  # 四氯乙烯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "chloroben":  # 氯苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "12-dichl":  # 邻二氯苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "14-dichl":  # 对二氯苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "123-dichl":  # 三氯苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "ethyl":  # 乙苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "dimeth":  # 二甲苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "styrene":  # 苯乙烯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "24-dini":  # 2,4-二硝基苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "26-dini":  # 2,6-二硝基苯
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "naph":  # 萘
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "anth":  # 蒽
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "fluor":  # 荧蒽
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "b-benzo":  # 苯并荧蒽
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "benzo":  # 苯并芘
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "pcbs":  # 多氯联苯
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "dehp":  # 邻苯二甲酸二（2-乙基己基）酯
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "246-tcp":  # 246-三氯酚
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "pcp":  # 五氯酚
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "hexa":  # 六六六
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "r-hexa":  # γ-六六六
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "ddt":  # 滴滴涕
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "hcb":  # 六氯酚
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "hepta":  # 七氯
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "24-dichl":  # 2,4-滴
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "carb":  # 克百威
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "aldi":  # 涕灭威
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "ddvp":  # 敌敌畏
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "chnops":  # 甲基对硫磷
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "chops":  # 马拉硫磷
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "dime":  # 乐果
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "chlorp":  # 毒死蜱
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "chloro":  # 百菌清
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "atra":  # 莠去津
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "glyp":  # 草甘膦
                v = round(v, 1)
                dict1.update({k: v})
        return dict1
