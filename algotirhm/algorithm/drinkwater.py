# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import pandas as pd
import math
import json
import algotirhm.common.standard as std

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
# "ph":"ph值"
# "codmn":"高锰酸钾盐"
# "nh4_n":"氨氮"
# "w_cu":"铜"
# "w_zn":"锌"
# "f":"氟化物"
# "se":"硒"
# "as":"砷"
# "w_hg":"汞"
# "cd":"镉"
# "cr6":"六价铬"
# "w_pb":"铅"
# "cn_total":"氰化物"
# "v_phen":"挥发性酚类"
# "an_saa":"阴离子表面活性剂"
# "s":"硫化物"
# "so4":"硫酸盐"
# "cl":"氯"
# "no3_n":"硝酸盐"
# "w_fe":"铁"
# "w_mn":"锰"
# "trichlo":"三氯甲烷"
# "car-tetr":"四氯化碳"
# "ben":"笨"
# "methyl":"甲苯"
# "dioct":"邻苯二甲酸二（2-乙基巳基）酯"
# "mo":"钼"
# "ni":"镍"
# "ta":"铊"
# "mix":"浑浊度"
# "no2_n":"亚硝酸盐"
# "hard":"硬度"
# "co":"钴"
# "be":"铍"
# "b":"硼"
# "colo_total":"大肠杆菌总数"
# "coloursd":"色度"
# "smells":"嗅和味"
# "visable":"可视度"
# "w_na":"钠"
# "disolvesolid":"固体溶解物"
# "w_al":"铝"
# "bateria_total":"菌群总数"
# "w_i":"碘"
# "alfa":"总α放射性"
# "belta":"总β放射性"

class DrinkWaterCal(object):

    cacheDict = {}

    def __init__(self, data):
        self.data = data

    def showdata(self):  # 展示数据概况
        return self.data

#1.样品数（测点）
    def item_amount(self):
        yps = self.data['stname'].count()  # 样品数
        self.cacheDict.update({"item_amount": yps})
        return yps

# 2.最大值（断面）
    def item_max(self):
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname",
             "stcode", "lycode", "rcode", "rscode", "lscode",
             "sampc", "rsc", "cq", 'year', 'mon', 'day', "time",
             "wd"])
        item_max = data.max()
        self.cacheDict.update({"max": item_max})
        item_max = item_max.to_json()
        item_max = json.loads(item_max)
        return item_max

# 3.最小值（断面）
    def item_min(self):
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname",
             "stcode", "lycode", "rcode", "rscode", "lscode",
             "sampc", "rsc", "cq", 'year', 'mon', 'day', "time",
             "wd"])
        item_min = data.min()
        self.cacheDict.update({"min": item_min})
        item_min = item_min.to_json()
        item_min = json.loads(item_min)
        return item_min

# 12.最大值出现日期（该断面）
    def maxdate(self):
        data = self.data
        data["time1"] = self.data["year"].map(str) + self.data["mon"].map(str) + self.data["day"].map(str)
        data = data.drop(columns=['year', 'mon', 'day'])
        dict = {}
        item_max = self.cacheDict.get("max")
        list = ['wq', 'ph', 'sd', 'chla', 'codmn', 'nh4_n', 'p_total', 'n_total', 'w_cu',
             'w_zn', 'f', 'se', 'as', 'w_hg', 'cd',
             'cr6', 'w_pb', 'cn_total', 'v_phen', 'an_saa',
             's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn',
             'trichlo', 'car-tetr', 'ben', 'methyl', 'dioct', 'mo', 'ni', 'ta', 'mix', 'no2_n', 'hard', 'co', 'be', 'b',
             'colo_total', 'coloursd', 'smells', 'visable', 'w_na', 'disolvesolid', 'w_al',
             'bateria_total', 'w_i', 'alfa', 'belta']
        for i in list:
            time = data[data[i] == item_max[i]]['time1']
            for t in time:
                dict.update({i: t})
        return dict

# 4.平均值
    def pH_avg(self):
        # pH值是无量纲指标，所以先要讲pH值转化为H离子浓度再求平均值，然后再转化成pH值的平均值
        for i in self.data['ph']:
            sum = 0
            i = 10 ** (-i)
            sum += i
            pH_avg = -math.log10(sum / DrinkWaterCal.item_amount(self))
            return pH_avg

    def item_avg(self):
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname",
             "stcode", "lycode", "rcode", "rscode", "lscode",
             "sampc", "rsc", "cq", "time",
             "wd"])
        item_avg = data.mean()
        item_avg['ph'] = DrinkWaterCal.pH_avg(self)
        self.cacheDict.update({"avg": item_avg})
        item_avg = item_avg.to_dict()
        item_avg = DrinkWaterCal.adjust(self, item_avg)
        return item_avg

#获取补充项目标准限制
    def get_restrict(self):
        df = pd.DataFrame({'item': ['codmn', 'nh4_n', 'w_cu', 'w_zn', 'f', 'se', 'as',
                                    'w_hg', 'cd', 'cr6', 'w_pb', 'cn_total', 'v_phen', 'an_saa',
                                    's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn', "trichlo", "car-tetr",
                                    "ben", "methyl", "dioct", "mo", "ni", "ta", "mix", "no2_n", "hard", "co", "be", "b",
                                    "colo_total", "coloursd", "smells", "visable", "w_na", "disolvesolid", "w_al",
                                    "bateria_total", "w_i", "alfa", "belta"],
                      'restrict': [1, 0.5, 250, 1.0, 1.0, 0.01, 0.01, 0.001, 0.005, 0.05, 0.01, 0.05, 0.002, 0.3, 0.02,
                                   250, 250, 10, 0.3, 0.1, 0.06, 0.002, 0.01, 0.7, 0.008, 0.07, 0.02, 0.0001, 1, 0.1,
                                   450, 1.0, 0.002, 0.5, 1, 15, 1, 1, 20, 200, 0.2, 100, 0.1, 0.5, 1]})
        return df

#7.水质类别（断面）
    def water_level(self):
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname",
             "stcode", "lycode", "rcode", "rscode", "lscode",
             "sampc", "rsc", "cq", "time",
             "wd"])

        item_avg = self.cacheDict.get("avg")
        dict = {}
        stdata = std.get_standard('do_cal_gb5749')
        if 6 < float(item_avg['ph']) < 9:
            dict.update({'ph': "I类"})
        else:
            dict.update({'ph': "劣V类"})
        for i in stdata['item']:
            if float(item_avg[i]) <= float(stdata[stdata['item'] == i]['I']):
                dict.update({i: "I类"})
            elif float(stdata[stdata['item'] == i]['II']) >= float(item_avg[i]) > float(stdata[stdata['item'] == i]['I']):
                dict.update({i: "II类"})
            elif float(stdata[stdata['item'] == i]['III']) >= float(item_avg[i]) > float(stdata[stdata['item'] == i]['II']):
                dict.update({i: "III类"})
            elif float(stdata[stdata['item'] == i]['IV']) >= float(item_avg[i]) > float(stdata[stdata['item'] == i]['III']):
                dict.update({i: "IV类"})
            elif float(item_avg[i]) == float(stdata[stdata['item'] == i]['V']):
                dict.update({i: "V类"})
            elif float(item_avg[i]) > float(stdata[stdata['item'] == i]['V']):
                dict.update({i: "劣V类"})

            rsdata = DrinkWaterCal.get_restrict(self)
            for j in rsdata['item']:
                if float(item_avg[j]) > float(rsdata[rsdata['item'] == j]['restrict']):
                    dict.update({j: "劣V类"})
                else:
                    dict.update({j: "I类"})
        self.cacheDict.update({"water_level": dict})
        return dict

#20.总水质类别
    def allwaterlevel(self):
        dict = {}
        lst = []
        ww = self.cacheDict.get("water_level")
        for k,v in ww.items():
            if v == "劣V类":
                lst.append(6)
            elif v == "V类":
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
        if lst[0] == 6:
            w = "劣V类"
        elif lst[0] == 5:
            w = "V类"
        elif lst[0] == 4:
            w = "IV类"
        elif lst[0] == 3:
            w = "III类"
        elif lst[0] == 2:
            w = "II类"
        elif lst[0] == 1:
            w = "I类"
        self.cacheDict.update({"allwaterlevel": w})
        return w

#24.定类项目
    def decideitem(self):
        lst = []
        temp = self.cacheDict.get("water_level")
        temp1 = self.cacheDict.get("allwaterlevel")
        for k,v in temp.items():
            if v == temp1:
                lst.append(k)
        self.cacheDict.update({"decideitem": lst})
        return lst

    #水质类别占比
    def waterradio(self):
        amount = 50
        dict = {}
        Isum = 0
        IIsum = 0
        IIIsum = 0
        IVsum = 0
        Vsum = 0
        temp = self.cacheDict.get("water_level")
        for i in temp.values():
            if i == "I类":
                Isum += 1
                Iradio = (Isum/amount)*100
                dict.update({"I类比例": str(round(Iradio, 2))+'%'})
            elif i == "II类":
                IIsum += 1
                IIradio = (IIsum/amount)*100
                dict.update({"II类比例": str(round(IIradio, 2))+'%'})
            elif i == "III类":
                IIIsum += 1
                IIIradio = (IIIsum/amount)*100
                dict.update({"III类比例": str(round(IIIradio, 2))+'%'})
            elif i == "IV类":
                IVsum += 1
                IVradio = (IVsum/amount)*100
                dict.update({"IV类比例": str(round(IVradio, 2))+'%'})
            elif i == "V类" or "劣V类":
                Vsum += 1
                Vradio = (Vsum/amount)*100
                dict.update({"V类比例": str(round(Vradio, 2))+'%'})
        self.cacheDict.update({"waterradio": dict})
        return dict

#33/44.断面水质状况（类别 污染状况 颜色）
    def water_status(self):
        dict = {}
        temp = self.cacheDict.get("allwaterlevel")
        if temp == "I类":
            dict.update({"status": "优"})
            dict.update({"colour": "蓝色"})
        elif temp == "II类":
            dict.update({"status": "优"})
            dict.update({"colour": "蓝色"})
        elif temp == "III类":
            dict.update({"status": "良好"})
            dict.update({"colour": "绿色"})
        elif temp == "IV类":
            dict.update({"status": "轻度污染"})
            dict.update({"colour": "黄色"})
        elif temp == "V类":
            dict.update({"status": "中度污染"})
            dict.update({"colour": "橙色"})
        elif temp == "劣V类":
            dict.update({"status": "重度污染"})
            dict.update({"colour": "红色"})
        return dict

#11.主要污染物
    def mainpollute(self):
        list = []
        temp = self.cacheDict.get("water_level")
        for k, v in temp.items():
            if v == "劣V类":
                list.append(k)
            if v == "V类":
                list.append(k)
            if v == "IV类":
                list.append(k)

        return list[0:3]

#5.超标样品数
    def hazard_amount(self):
        dict = {}
        stdata = std.get_standard('do_cal_gb5749')
        self.data1 = self.data.drop(columns=["year", "mon", "day",
                                             "stname", "lyname", "rname", "rsname", "lsname",
                                             "stcode", "lycode", "rcode", "rscode", "lscode",
                                             "sampc", "rsc", "cq", "time", "wd"])
        sum = 0
        for i, j in self.data1.items():
            if i != 'ph':
                for k in self.data1[i]:
                    if float(k) > stdata[stdata['item'] == i]['III'].values:
                        sum += 1
                dict.update({i: sum})

        k = 0
        for i in self.data1['ph']:
            if i < 6 or i > 9:
                k = k + 1
                dict.update({'ph': k})
        self.cacheDict.update({"hazard_amount": dict})
        return dict


    def hazardpoint(self):
        stdata = std.get_standard("do_cal_gb5749")
        data1 = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname", "stcode", "lycode", "rcode",
                            "rscode", "lscode", "sampc", "rsc", "cq", "year", "mon", "day", "time", "wd",
                            "wq"])
        sum = 0

        for i in range(0, len(data1)):
            for j in list(data1):
                if j != "ph" or j != "do":
                    if data1.iloc[i][j] > stdata[stdata["item"] == j]["III"].values:
                        sum += 1
                        break

        for i in data1["ph"]:
            if i < 6 or i > 9:
                sum += 1

        for i in data1["do"]:
            if i < 5:
                sum += 1
        self.cacheDict.update({"hazardpoint": sum})
        return sum

#6.超标率 25.达标率
    def hazard_radio(self):
        dict = {}
        temp = self.cacheDict.get("hazardpoint")
        temp1 = self.cacheDict.get("item_amount")
        radio = temp/(temp1)
        rcradio = 1-radio
        radio = round(radio, 2)*100
        rcradio = round(rcradio, 2)*100
        radio = str(radio)+'%'
        rcradio = str(rcradio)+'%'
        dict.update({"超标率": radio})
        dict.update({"达标率": rcradio})
        self.cacheDict.update({"hazard_radio": dict})
        return dict

    # 22.超标项目
    def overItem(self):
        lst = []
        temp = self.cacheDict.get("water_level")
        for k, v in temp.items():
            if v == "劣V类":
                lst.append(k)
            elif v == "V类":
                lst.append(k)
            elif v == "IV类":
                lst.append(k)
            else:
                continue
        self.cacheDict.update({"overItem": lst})
        return lst

   #  42.超标倍数
    def hazard_multiple(self):
        lst = []
        temp = self.cacheDict.get("overItem")
        temp1 = self.cacheDict.get("avg")
        stdata = std.get_standard("do_cal_gb5749")
        for i in temp:
            multiple = temp1[i] / stdata[stdata["item"] == i]["III"]
            for k,v in multiple.items():
                multiple = round(v,2)
                multi = i + "(" + str(multiple) + ")"
                lst.append(multi)
        return lst

#10.最大超标倍数
    def max_hazerd_multiple(self):
        stdata = std.get_standard('do_cal_gb5749')
        dict = {}
        dict2 = {}
        item_max = self.cacheDict.get("max")
        temp = self.cacheDict.get("water_level")
        for k, v in temp.items():
            if v == "IV类" or "V类" or "劣V类":
                maxmultiple = (item_max[k]/stdata[stdata['item'] == k]['III'])-1
                for m in maxmultiple:
                    dict.update({k: m})
        for k,v in dict.items():
            if v > 0:
                v = round(v, 3)
                dict2.update({k: v})
        self.cacheDict.update({"max_hazard_multiple": dict2})
        return dict2

# 11.平均超标倍数
    def hazard_multiavg(self):
        dict = {}
        stdata = std.get_standard('do_cal_gb5749')
        temp = self.cacheDict.get("overItem")
        temp1 = self.cacheDict.get("polluteIndex")
        for i in temp:
            a = temp1[i]/(stdata[stdata['item'] == i]['III'])
            dict.update({i: a})
        self.cacheDict.update({"hazard_multiavg": dict})
        return dict

#15/16.污染指数
    def polluteIndex(self):
        dict = {}
        dict2 = {}
        rsdata = DrinkWaterCal.get_restrict(self)
        if DrinkWaterCal.pH_avg(self) > 7.5:
            ph_pollute = (DrinkWaterCal.item_avg(self)['ph'] - 7.5) / 1.5
            dict.update({'ph': ph_pollute})
        else:
            ph_pollute = ((DrinkWaterCal.item_avg(self)['ph'] - 7.5) / (-1.5))
            dict.update({'ph': ph_pollute})

        stdata = std.get_standard('do_cal_gb5749')

        temp = self.cacheDict.get("avg")
        for i in stdata['item']:
            if float(temp[i]) <= float(stdata[stdata['item'] == i]['I']):
                xpollute = (temp[i]) / (stdata[stdata['item'] == i]['I'])
                for x in xpollute:
                    dict.update({i: x})

            elif float(stdata[stdata['item'] == i]['II']) >= float(temp[i]) > float(stdata[stdata['item'] == i]['I']):
                xpollute = (temp[i]) / (stdata[stdata['item'] == i]['II'])
                for x in xpollute:
                    dict.update({i: x})

            elif float(stdata[stdata['item'] == i]['III']) >= float(temp[i]) > float(stdata[stdata['item'] == i]['II']):
                xpollute = (temp[i]) / (stdata[stdata['item'] == i]['III'])
                for x in xpollute:
                    dict.update({i: x})

            elif float(stdata[stdata['item'] == i]['IV']) >= float(temp[i]) > float(stdata[stdata['item'] == i]['III']):
                xpollute = (temp[i]) / (stdata[stdata['item'] == i]['IV'])
                for x in xpollute:
                    dict.update({i: x})

            elif float(temp[i]) >= float(stdata[stdata['item'] == i]['I']):
                xpollute = (temp[i]) / (stdata[stdata['item'] == i]['V'])
                for x in xpollute:
                    dict.update({i: x})

        for i in self.data['rname']:
            if "湖" in i:
                for j in rsdata['item']:
                    hpollute = (temp[j])/(rsdata[rsdata['item'] == j]['restrict'])
                    for h in hpollute:
                        dict.update({j: h})

        for k, v in dict.items():
            v = round(v, 3)
            dict2.update({k: v})
        self.cacheDict.update({"polluteIndex": dict2})
        return dict2

    def polluteIndexRank(self):
        temp = self.cacheDict.get("polluteIndex")
        dict = sorted(temp.items(), key=lambda d: d[1], reverse=True)
        self.cacheDict.update({"polluteIndexRank": dict})
        return dict

#18.综合污染指数
    def comprepollute(self):
        sum = 0
        temp = self.cacheDict.get("polluteIndex")
        for k, v in temp.items():
            sum += v
        self.cacheDict.update({"comprepollute": sum})
        return sum

#19.平均污染指数
    def comprepolluteavg(self):
        amount = 28
        temp = self.cacheDict.get("comprepollute")
        avg = temp/amount
        self.cacheDict.update({"comprepolluteavg": avg})
        return avg

#8/9.分担率
    def share(self):
        dict = {}
        temp = self.cacheDict.get("polluteIndex")
        temp1 = self.cacheDict.get("comprepollute")
        for k,v in temp.items():
            shareIndex = v / float(temp1)
            shareIndex = round(shareIndex*100, 2)
            shareIndex = str(shareIndex)+"%"
            dict.update({k: shareIndex})
        self.cacheDict.update({"share": dict})
        return dict

#17.单项指数
    def singleIndex(self):
        dict = {}
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname",
             "stcode", "lycode", "rcode", "rscode", "lscode",
             "sampc", "rsc", "cq", "time",
             "wd"])
        item_avg = self.cacheDict.get("avg")
        stdata = std.get_standard('do_cal_gb5749')
        # dict.update({"n_total": 0})
        if 6 < item_avg['ph'] < 9:
            dict.update({"ph": 0})
        else:
            dict.update({"ph": 100})
        dict.update({'p_total': 0})
        dict.update({'n_total': 0})

        for i in stdata['item']:

            if float(item_avg[i]) <= float(stdata[stdata['item'] == i]['I']):
                single_index = ((item_avg[i])-0)/((stdata[stdata['item'] == i]['I']-0)*20)
                for s in single_index:
                    dict.update({i: s})

            elif float(stdata[stdata['item'] == i]['II']) <= float(item_avg[i]) < float(stdata[stdata['item'] == i]['I']):
                single_index = (item_avg[i]-stdata[stdata['item'] == i]['I'])/((stdata[stdata['item'] == i]['II'] - stdata[stdata['item']==i]['I'])*20)+20
                for s in single_index:
                    dict.update({i: s})

            elif float(stdata[stdata['item'] == i]['III']) <= float(item_avg[i]) < float(stdata[stdata['item'] == i]['II']):
                single_index = (item_avg[i] - stdata[stdata['item'] == i]['II']) /((stdata[stdata['item'] == i]['III'] - stdata[stdata['item'] == i]['II']) * 20)+40
                for s in single_index:
                    dict.update({i: s})

            elif float(stdata[stdata['item'] == i]['IV']) <= float(item_avg[i]) < float(stdata[stdata['item'] == i]['III']):
                single_index = (item_avg[i] - stdata[stdata['item'] == i]['III']) / ((stdata[stdata['item'] == i]['IV'] - stdata[stdata['item'] == i]['III']) * 20)+60
                for s in single_index:
                    dict.update({i: s})

            elif float(item_avg[i]) > float(stdata[stdata['item'] == i]['V']):
                dict.update({i: 900})

            elif float(item_avg[i]) == float(stdata[stdata['item'] == i]['V']):
                dict.update({i: 100})


            for i in DrinkWaterCal.get_restrict(self)['item']:
                single_index = (item_avg[i]/250)*60
                dict.update({i: single_index})

        dict2 = DrinkWaterCal.adjust(self, dict)
        self.cacheDict.update({"singleIndex": dict2})
        return dict2

    def singleIndexRank(self):
        ds = self.cacheDict.get("singleIndex")
        dict = sorted(ds.items(), key=lambda d: d[1], reverse=True)
        self.cacheDict.update({"singleIndexRank": dict})
        return dict

    #29/30/31.分类指数123
    def level_index(self):
        dict1 = {}
        dict2 = {}
        dict3 = {}
        list1 = ['se', 'as', 'w_hg', 'cd', 'cr6', 'w_pb', 'cn_total']
        list2 = ['ph', 'codmn', 'nh4_n', 'colo_total']
        list3 = ['w_cu', 'w_zn', 'f', 'v_phen', 'an_saa', 's', 'so4', 'cl',
                            'no3_n', 'w_fe', 'w_mn']
        temp = self.cacheDict.get("singleIndex")

        for i in list1:
            dict1.update({i: temp[i]})
        for i in list2:
            dict2.update({i: temp[i]})
        for i in list3:
            dict3.update({i: temp[i]})

        return dict1, dict2, dict3

#32.水源地分类指数
    def origin_index(self):
        dict = {}
        lst1 = []
        lst2 = []
        lst3 = []
        list1 = ['se', 'as', 'w_hg', 'cd', 'cr6', 'w_pb', 'cn_total']
        list2 = ['ph', 'codmn', 'nh4_n']
        list3 = ['p_total', 'n_total', 'w_cu', 'w_zn', 'f', 'v_phen', 'an_saa', 's', 'so4', 'cl',
                            'no3_n', 'w_fe', 'w_mn']
        temp = self.cacheDict.get("singleIndex")
        for i in list1:
            origin1 = temp[i]
            lst1.append(origin1)
            lst1.sort(reverse=True)
            dict.update({"分类指数1": lst1[0]})
        for i in list2:
            origin2 = temp[i]
            lst2.append(origin2)
            lst2.sort(reverse=True)
            dict.update({"分类指数2": lst2[0]})
        for i in list3:
            origin3 = temp[i]
            lst3.append(origin3)
            lst3.sort(reverse=True)
            dict.update({"分类指数3": lst3[0]})
        return dict

    def waterquantity(self):
        sum = 0
        for i in self.data['wq']:
            sum += i
        self.cacheDict.update({"waterquantity": sum})
        return sum

    def reachwaterquantity(self):
        stdata = std.get_standard('do_cal_gb3838')
        self.data1 = self.data.drop(
            columns=['stname', 'lyname', 'rname', 'rsname', 'lsname', 'stcode', 'lycode', 'rcode',
                     'rscode', 'lscode', 'sampc', 'rsc', 'cq', 'year', 'mon', 'day', 'time', 'wd',
                     ])
        sum = 0
        temp = self.cacheDict.get("waterquantity")
        for i in self.data1.index:
            data1 = self.data1.loc[i]
            for k, v in data1.items():
                lst = 0
                if k != 'w_temp' and k != 'ph' and k != 'do':

                    if float(data1.loc[k]) > stdata[stdata['item'] == k]['III'].values:
                        lst += 1
                if lst > 0:
                    sum += data1["wq"]
        sum1 = temp - sum
        return sum1

    # 37.综合富营养化指数
    def Nutri_index(self):
        global tli_sd, tli_codmn, tli_tn, tli_tp, tli_chla
        tp_value = self.data['p_total']
        tn_value = self.data['n_total']
        sd_value = self.data['sd']
        codmn_value = self.data['codmn']
        chla_value = self.data['chla']

        for i in self.data['rname']:
            if '河' in i:
                return "河流无富营养化指数"
            elif '湖' in i:
                for i in chla_value:
                    if i > 0:
                        tli_chla = 10 * (2.5 + 1.086 * math.log(i))
                    for i in tp_value:
                        if i > 0:
                            tli_tp = 10 * (9.436 + 1.624 * math.log(i))
                for i in tn_value:
                    if i > 0:
                        tli_tn = 10 * (5.453 + 1.694 * math.log(i))
                for i in sd_value:
                    if i > 0:
                        tli_sd = 10 * (5.118 - 1.94 * math.log(i))
                for i in codmn_value:
                    if i > 0:
                        tli_codmn = 10 * (0.109 + 2.661 * math.log(i))

                Nutri_std = pd.DataFrame({
                    "item": ['Chla', 'TP', 'TN', 'SD', 'CODMn'],
                    "value": [1, 0.84, 0.82, -0.83, 0.83],
                    "value^2": [1, 0.7056, 0.6726, 0.6889, 0.6889],
                    "TLI": [tli_chla, tli_tp, tli_tn, tli_sd, tli_codmn]
                })

                Nutri_std_sum = Nutri_std['value^2'].sum()

                for i in Nutri_std['TLI']:
                    Wj = i / Nutri_std_sum
                    for j in Nutri_std['TLI']:
                        Nutri_index = j / Wj
                        return Nutri_index

    # 38.湖库营养等级分类
    def hk_NutriLevel(self):
        for i in self.data['rname']:
            if '河' in i:
                return "河流无营养等级分类"
            elif '湖' in i:
                if DrinkWaterCal.Nutri_index(self) < 30:
                    return '贫营养'
                elif 30 <= DrinkWaterCal.Nutri_index(self) <= 50:
                    return '中营养'
                elif 50 < DrinkWaterCal.Nutri_index(self) <= 60:
                    return '轻度富营养'
                elif 60 < DrinkWaterCal.Nutri_index(self) <= 70:
                    return '中度富营养'
                else:
                    return '重度富营养'

#评价指标计算数据精度标准化方法
    def adjust(self, dict):
        dict1 = {}
        self.dict = dict
        for k, v in self.dict.items():
            if k == "wq": #取水量
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "ph":#ph值
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "sd":#透明度
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "chla":#叶绿色a
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "codmn":#高锰酸盐
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "nh4_n":#氨氮
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "p_total":#总磷
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "n_total":#总氮
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_cu":#铜
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_zn":#锌
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "f":#氟化物
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "se":#硒
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "as":#砷
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "w_hg":#汞
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "cd":#镉
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "cr6":#六价铬
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "w_pb":#铅
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "cn_total":#氰化物
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "v_phen":#挥发酚
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "an_saa":#阴离子表面活性剂
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "s":#硫化物
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "so4":#硫酸盐
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "cl":#氯化物
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "no3_n":#硝酸盐
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_fe":#铁
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "w_mn":#锰
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "trichlo":#三氯甲烷
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "car-tetr":#四氯化碳
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "ben":#苯
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "methyl":#甲苯
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "dioct":#邻苯二甲酸二脂
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "mo":#钼
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "ni":#镍
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "ta":#铊
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "mix":#浊度
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "no2_n":#亚硝酸盐
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "hard":#硬度
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "co":#钴
                v = round(v, 6)
                dict1.update({k: v})
            elif k == "be":#铍
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "b":#硼
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "ba":#钡
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "colo_total":#大肠杆菌总数
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "coloursd":#色度
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "smells":#嗅和味
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "visable":#可见度
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_na":#钠
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "disolvesolid":#可溶性固体
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_al":#铝
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "bateria_total":#菌落总数
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_i":#碘化物
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "alfa":#α射线
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "belta":#β射线
                v = round(v, 2)
                dict1.update({k: v})
        return dict1

    def spearman(self):
        dict1 = {}
        data = self.data[[
             'wd', 'wq', 'ph', 'sd', 'chla', 'codmn', 'nh4_n', 'p_total', 'n_total', 'w_cu',
             'w_zn', 'f', 'se', 'as', 'w_hg', 'cd',
             'cr6', 'w_pb', 'cn_total', 'v_phen', 'an_saa',
             's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn',
             'trichlo', 'car-tetr', 'ben', 'methyl', 'dioct', 'mo', 'ni', 'ta', 'mix', 'no2_n', 'hard', 'co', 'be', 'b',
             'colo_total', 'coloursd', 'smells', 'visable', 'w_na', 'disolvesolid', 'w_al',
             'bateria_total', 'w_i', 'alfa', 'belta', 'year', 'mon']]
        lst = []
        lst1 = []
        for i in data.year.unique():
            lst.append(i)
        for i in data.mon.unique():
            lst1.append(i)
        # 年为周期判断
        if len(lst) > 4:
            for i in ['year',
             'wd', 'wq', 'ph', 'sd', 'chla', 'codmn', 'nh4_n', 'p_total', 'n_total', 'w_cu',
             'w_zn', 'f', 'se', 'as', 'w_hg', 'cd',
             'cr6', 'w_pb', 'cn_total', 'v_phen', 'an_saa',
             's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn',
             'trichlo', 'car-tetr', 'ben', 'methyl', 'dioct', 'mo', 'ni', 'ta', 'mix', 'no2_n', 'hard', 'co', 'be', 'b',
             'colo_total', 'coloursd', 'smells', 'visable', 'w_na', 'disolvesolid', 'w_al',
             'bateria_total', 'w_i', 'alfa', 'belta']:
                data[i] = data[i].rank(method="min")  # 排名
            for i in [
             'wd', 'wq', 'ph', 'sd', 'chla', 'codmn', 'nh4_n', 'p_total', 'n_total', 'w_cu',
             'w_zn', 'f', 'se', 'as', 'w_hg', 'cd',
             'cr6', 'w_pb', 'cn_total', 'v_phen', 'an_saa',
             's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn',
             'trichlo', 'car-tetr', 'ben', 'methyl', 'dioct', 'mo', 'ni', 'ta', 'mix', 'no2_n', 'hard', 'co', 'be', 'b',
             'colo_total', 'coloursd', 'smells', 'visable', 'w_na', 'disolvesolid', 'w_al',
             'bateria_total', 'w_i', 'alfa', 'belta']:
                sum1 = 0
                for j in range(len(data)):
                    a = (data.loc[j][i] - data.loc[j]['year']) * (data.loc[j][i] - data.loc[j]['year'])
                    sum1 += a
                rs = round(1 - 6 / (len(lst) * (len(lst) ** 2 - 1)) * sum1, 2)
                dict1.update({i: rs})
        # 月为周期
        elif len(lst1) > 1:
            for i in ['mon',
             'wd', 'wq', 'ph', 'sd', 'chla', 'codmn', 'nh4_n', 'p_total', 'n_total', 'w_cu',
             'w_zn', 'f', 'se', 'as', 'w_hg', 'cd',
             'cr6', 'w_pb', 'cn_total', 'v_phen', 'an_saa',
             's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn',
             'trichlo', 'car-tetr', 'ben', 'methyl', 'dioct', 'mo', 'ni', 'ta', 'mix', 'no2_n', 'hard', 'co', 'be', 'b',
             'colo_total', 'coloursd', 'smells', 'visable', 'w_na', 'disolvesolid', 'w_al',
             'bateria_total', 'w_i', 'alfa', 'belta']:
                data[i] = data[i].rank(method="min")
            for i in [
             'wd', 'wq', 'ph', 'sd', 'chla', 'codmn', 'nh4_n', 'p_total', 'n_total', 'w_cu',
             'w_zn', 'f', 'se', 'as', 'w_hg', 'cd',
             'cr6', 'w_pb', 'cn_total', 'v_phen', 'an_saa',
             's', 'so4', 'cl', 'no3_n', 'w_fe', 'w_mn',
             'trichlo', 'car-tetr', 'ben', 'methyl', 'dioct', 'mo', 'ni', 'ta', 'mix', 'no2_n', 'hard', 'co', 'be', 'b',
             'colo_total', 'coloursd', 'smells', 'visable', 'w_na', 'disolvesolid', 'w_al',
             'bateria_total', 'w_i', 'alfa', 'belta']:
                sum1 = 0
                for j in range(len(data)):
                    a = (data.loc[j][i] - data.loc[j]['mon']) * (data.loc[j][i] - data.loc[j]['mon'])
                    sum1 += a
                rs = round(1 - 6 / (len(lst1) * (len(lst1) ** 2 - 1)) * sum1, 2)
                dict1.update({i: rs})
        else:
            dict1.update({'spearman': '不存在'})
        return dict1