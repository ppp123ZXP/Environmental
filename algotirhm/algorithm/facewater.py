# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import math
import json
import algotirhm.common.standard as std


# PG数据库字段COMMENT
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
# "wss":悬浮物,
# "w_cond":电导率,
# "w_temp":水温,
# "ph":PH值,
# "do":溶解氧,
# "codmn":高锰酸盐指数,
# "codcr":化学需氧量,
# "bod5":生化需氧量,
# "nh4_n":氨氮,
# "p_total":总磷,
# "n_total":总氮,
# "w_cu":铜,
# "w_zn":锌,
# "f":氟化物,
# "se":硒,
# "as":砷,
# "w_hg":汞,
# "cd":镉,
# "cr6":六价铬,
# "w_pb":铅,
# "cn_total":氰化物,
# "v_phen":挥发酚,
# "oils":石油类,
# "an_saa":阴离子表面活性剂,
# "s":硫化物,
# "colo_org":粪大肠菌群,
# "so4":硫酸盐,
# "cl":氯化物,
# "no3_n":硝酸盐,
# "w_fe":铁,
# "w_mn":锰,
# "ni":镍,
# "vel":流速,
# "width":河宽,
# "depth":水深

# json_data = {"stname": "广州市站", "lyname": "珠江", "rname": "顺德水道", "rsname": "乌洲", "lsname": "中",
#              "stcode": 440100, "lycode": "HD020400", "rcode": 1, "rscode": "上", "lscode": "涨",
#              "sampc": 1, "rsc": 1, "cq": 1, "year": 2020, "mon": 1, "day": 6, "time": "15:53:00",
#              "wd": 1, "wq": 1, "wss": 1, "w_cond": 1, "w_temp": 1, "ph": 7.11, "do": 6.34, "codmn": 1.9,
#              "codcr": 8, "bod5": 1.6, "nh4_n": 1, "p_total": 0.05, "n_total": 0, "w_cu": 0.00335,
#              "w_zn": 0.00835, "f": 0.22, "se": 0.00041, "as": 0.00226, "w_hg": 0.000009, "cd": 0.00005,
#              "cr6": 0.004, "w_pb": 0.00014, "cn_total": 0.004, "v_phen": 0.0006, "oils": 0.01, "an_saa": 0.05,
#              "s": 0.005, "colo_org": 29000, "so4": 0, "cl": 0, "no3_n": 0, "w_fe": 0, "w_mn": 0, "ni": 0, "vel": 0,
#              "width": 0, "depth": 0}

class WaterCal(object):
    cacheDict = {}

    def __init__(self, data):
        self.data = data

    def showdata(self):  # 展示数据概况
        return self.data

# 1.样品数（测点）
    def item_amount(self):
        yps = self.data["stname"].count()  # 样品数
        self.cacheDict.update({"item_amount": yps})
        return yps

    # 2.最大值（断面）
    def item_max(self):
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname", "stcode", "lycode", "rcode",
                                       "rscode", "lscode", "sampc", "rsc", "cq", "year", "mon", "day", "time", "wd",
                                       "wq", "wss", "w_cond"])
        item_max = data.max()
        item_max["do"] = data.min()["do"]
        self.cacheDict.update({"max": item_max})
        item_max = item_max.to_json()
        item_max = json.loads(item_max)
        return item_max

    # 3.最小值（断面）
    def item_min(self):
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname", "stcode", "lycode", "rcode",
                                       "rscode", "lscode", "sampc", "rsc", "cq", "year", "mon", "day", "time", "wd",
                                       "wq", "wss", "w_cond"])
        item_min = data.min()
        item_min["do"] = data.max()["do"]
        self.cacheDict.update({"min": item_min})
        item_min = item_min.to_json()
        item_min = json.loads(item_min)
        return item_min

    # 12.最大值出现日期（该断面）
    def maxdate(self):
        data = self.data
        data["time1"] = self.data["year"].map(str) + self.data["mon"].map(str) + self.data["day"].map(str)
        data = data.drop(columns=["year", "mon", "day"])
        dict = {}
        temp = self.cacheDict.get("max")
        list = ["w_temp", "ph", "do", "sd", "chla", "codmn", "codcr", "bod5", "nh4_n",
                "p_total", "n_total", "w_cu", "w_zn", "f", "se", "as", "w_hg", "cd", "cr6",
                "w_pb", "cn_total", "v_phen", "oils", "an_saa", "s", "colo_org", "so4", "cl",
                "no3_n", "w_fe", "w_mn", "ni", "vel", "width", "depth"]
        for i in list:
            time1 = data[data[i] == temp[i]]["time1"]
            time2 = data[data[i] == temp[i]]["time"]
            for t in time1:
                for j in time2:
                    x = t + " " + j
                    dict.update({i: x})
        return dict

    # 4.平均值
    def pH_avg(self):
        # pH值是无量纲指标，所以先要讲pH值转化为H离子浓度再求平均值，然后再转化成pH值的平均值
        for i in self.data["ph"]:
            sum = 0
            i = 10 ** (-i)
            sum += i
            temp = self.cacheDict.get("item_amount")
            pH_avg = -math.log10(sum / temp)
            return pH_avg

    def colo_org_avg(self):
        for i in self.data["colo_org"]:
            sum = 0
            sum += math.log10(i)
            temp = self.cacheDict.get("item_amount")
            colo_org_avg = 10 ** (sum / temp)
            return colo_org_avg

    def item_avg(self):
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname", "stcode", "lycode", "rcode",
                                       "rscode", "lscode", "sampc", "rsc", "cq", "year", "mon", "day", "time", "wd",
                                       "wq", "wss", "w_cond"])
        item_avg = data.mean()
        item_avg["ph"] = WaterCal.pH_avg(self)
        item_avg["colo_org"] = WaterCal.colo_org_avg(self)
        self.cacheDict.update({"avg": item_avg})
        item_avg = item_avg.to_dict()
        item_avg = WaterCal.adjust(self, item_avg)
        return item_avg

    # 获取补充项目标准限制
    def get_restrict(self):
        df = pd.DataFrame({"item": ["so4", "cl", "no3_n", "w_fe", "w_mn"],
                           "restrict": [250, 250, 10, 0.3, 0.1]})
        return df

    # 7.水质类别（断面）
    def water_level(self):
        temp = self.cacheDict.get("avg")
        dict = {}
        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")

        if 6 < float(temp["ph"]) < 9:
            dict.update({"ph": "I类"})
        else:
            dict.update({"ph": "劣V类"})

        if float(temp["do"]) >= float(stdata[stdata["item"] == "do"]["I"]):
            dict.update({"do": "I类"})
        elif float(stdata[stdata["item"] == "do"]["II"]) <= float(temp["do"]) < float(
                stdata[stdata["item"] == "do"]["I"]):
            dict.update({"do": "II类"})
        elif float(stdata[stdata["item"] == "do"]["III"]) <= float(temp["do"]) < float(
                stdata[stdata["item"] == "do"]["II"]):
            dict.update({"do": "III类"})
        elif float(stdata[stdata["item"] == "do"]["IV"]) <= float(temp["do"]) < float(
                stdata[stdata["item"] == "do"]["III"]):
            dict.update({"do": "IV类"})
        elif float(temp["do"]) == float(stdata[stdata["item"] == "do"]["V"]):
            dict.update({"do": "V类"})
        elif float(temp["do"]) > float(stdata[stdata["item"] == "do"]["V"]):
            dict.update({"do": "劣V类"})

        stdata = stdata.drop(index=(stdata.loc[(stdata["item"] == "do")].index))

        for i in stdata["item"]:
            if float(temp[i]) <= float(stdata[stdata["item"] == i]["I"]):
                dict.update({i: "I类"})
            elif float(stdata[stdata["item"] == i]["II"]) >= float(temp[i]) > float(stdata[stdata["item"] == i]["I"]):
                dict.update({i: "II类"})
            elif float(stdata[stdata["item"] == i]["III"]) >= float(temp[i]) > float(stdata[stdata["item"] == i]["II"]):
                dict.update({i: "III类"})
            elif float(stdata[stdata["item"] == i]["IV"]) >= float(temp[i]) > float(stdata[stdata["item"] == i]["III"]):
                dict.update({i: "IV类"})
            elif float(temp[i]) == float(stdata[stdata["item"] == i]["V"]):
                dict.update({i: "V类"})
            elif float(temp[i]) > float(stdata[stdata["item"] == i]["V"]):
                dict.update({i: "劣V类"})
            rsdata = WaterCal.get_restrict(self)
            for j in rsdata["item"]:
                if float(temp[j]) > float(rsdata[rsdata["item"] == j]["restrict"]):
                    dict.update({j: "劣V类"})
                else:
                    dict.update({j: "I类"})
        self.cacheDict.update({"water_level": dict})
        return dict

    # 20.总水质类别
    def allwaterlevel(self):
        lst = []
        temp = self.cacheDict.get("water_level")
        for k, v in temp.items():
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
            all = "劣V类"
        elif lst[0] == 5:
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


    # 7.水质类别（断面）
    def water_level_no_do(self):
        temp = self.cacheDict.get("avg")
        dict = {}
        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")

        if 6 < float(temp["ph"]) < 9:
            dict.update({"ph": "I类"})
        else:
            dict.update({"ph": "劣V类"})

        stdata = stdata.drop(index=(stdata.loc[(stdata["item"] == "do")].index))

        for i in stdata["item"]:
            if float(temp[i]) <= float(stdata[stdata["item"] == i]["I"]):
                dict.update({i: "I类"})
            elif float(stdata[stdata["item"] == i]["II"]) >= float(temp[i]) > float(stdata[stdata["item"] == i]["I"]):
                dict.update({i: "II类"})
            elif float(stdata[stdata["item"] == i]["III"]) >= float(temp[i]) > float(stdata[stdata["item"] == i]["II"]):
                dict.update({i: "III类"})
            elif float(stdata[stdata["item"] == i]["IV"]) >= float(temp[i]) > float(stdata[stdata["item"] == i]["III"]):
                dict.update({i: "IV类"})
            elif float(temp[i]) == float(stdata[stdata["item"] == i]["V"]):
                dict.update({i: "V类"})
            elif float(temp[i]) > float(stdata[stdata["item"] == i]["V"]):
                dict.update({i: "劣V类"})
            rsdata = WaterCal.get_restrict(self)
            for j in rsdata["item"]:
                if float(temp[j]) > float(rsdata[rsdata["item"] == j]["restrict"]):
                    dict.update({j: "劣V类"})
                else:
                    dict.update({j: "I类"})
        self.cacheDict.update({"water_level_no_do": dict})
        return dict

    # 20.总水质类别
    def allwaterlevel_no_do(self):
        lst = []
        temp = self.cacheDict.get("water_level_no_do")
        for k, v in temp.items():
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
            all = "劣V类"
        elif lst[0] == 5:
            all = "V类"
        elif lst[0] == 4:
            all = "IV类"
        elif lst[0] == 3:
            all = "III类"
        elif lst[0] == 2:
            all = "II类"
        elif lst[0] == 1:
            all = "I类"
        self.cacheDict.update({"allwaterlevel_no_do": all})
        return all

    # 24.定类项目
    def decideitem(self):
        lst = []
        temp = self.cacheDict.get("water_level")
        temp1 = self.cacheDict.get("allwaterlevel")
        for k, v in temp.items():
            if v == temp1:
                lst.append(k)
        self.cacheDict.update({"decideitem": lst})
        return lst

    # 水质类别占比
    def waterradio(self):
        amount = 28
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
                Iradio = (Isum / amount) * 100
                dict.update({"I类比例": str(round(Iradio, 2)) + "%"})
            elif i == "II类":
                IIsum += 1
                IIradio = (IIsum / amount) * 100
                dict.update({"II类比例": str(round(IIradio, 2)) + "%"})
            elif i == "III类":
                IIIsum += 1
                IIIradio = (IIIsum / amount) * 100
                dict.update({"III类比例": str(round(IIIradio, 2)) + "%"})
            elif i == "IV类":
                IVsum += 1
                IVradio = (IVsum / amount) * 100
                dict.update({"IV类比例": str(round(IVradio, 2)) + "%"})
            elif i == "V类" or "劣V类":
                Vsum += 1
                Vradio = (Vsum / amount) * 100

                dict.update({"V类比例": str(round(Vradio, 2)) + "%"})
        self.cacheDict.update({"waterradio": dict})
        return dict

    # 33/44.断面水质状况（类别 污染状况 颜色）
    def waterstatus(self):
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
        self.cacheDict.update({"waterstatus": dict})
        return dict

    # 15/16.污染指数
    def polluteIndex(self):
        dict = {}
        dict2 = {}
        rsdata = WaterCal.get_restrict(self)
        temp = self.cacheDict.get("avg")
        if WaterCal.pH_avg(self) > 7.5:
            ph_pollute = (temp["ph"] - 7.5) / 1.5
            dict.update({"ph": ph_pollute})
        else:
            ph_pollute = ((temp["ph"] - 7.5) / (-1.5))
            dict.update({"ph": ph_pollute})
        temp1 = self.cacheDict.get("max")
        # 计算溶解氧的污染指数
        fulloxy_value = 2 + (temp1["w_temp"] - temp["do"]) * (7 - 2)
        if fulloxy_value > 7.5:
            if fulloxy_value - 7.5 > 0 and fulloxy_value > temp["do"]:
                oxy_pollute = (fulloxy_value - temp["do"]) / (fulloxy_value - 7.5)
                dict.update({"do": oxy_pollute})
            elif fulloxy_value - 7.5 > 0 and fulloxy_value <= temp["do"]:
                oxy_pollute = 0
                dict.update({"do": oxy_pollute})
        elif 6 <= fulloxy_value <= 7.5:
            if fulloxy_value - 6 > 0 and fulloxy_value > temp["do"]:
                oxy_pollute = (fulloxy_value - temp["do"]) / (fulloxy_value - 6)
                dict.update({"do": oxy_pollute})
            elif fulloxy_value - 6 > 0 and fulloxy_value <= temp["do"]:
                oxy_pollute = 0
                dict.update({"do": oxy_pollute})

        elif 5 <= fulloxy_value <= 6:
            if fulloxy_value - 5 > 0 and fulloxy_value > temp["do"]:
                oxy_pollute = (fulloxy_value - temp["do"]) / (fulloxy_value - 5)
                dict.update({"do": oxy_pollute})
            elif fulloxy_value - 5 > 0 and fulloxy_value <= temp["do"]:
                oxy_pollute = 0
                dict.update({"do": oxy_pollute})

        elif 3 <= fulloxy_value <= 5:
            if fulloxy_value - 3 > 0 and fulloxy_value > temp["do"]:
                oxy_pollute = (fulloxy_value - temp["do"]) / (fulloxy_value - 3)
                dict.update({"do": oxy_pollute})
            elif fulloxy_value - 3 > 0 and fulloxy_value <= temp["do"]:
                oxy_pollute = 0
                dict.update({"do": oxy_pollute})


        elif fulloxy_value - 2 != 0:  # 不等于

            if fulloxy_value - 2 > 0 and fulloxy_value > temp["do"]:

                oxy_pollute = (fulloxy_value - temp["do"]) / (fulloxy_value - 2)

                dict.update({"do": oxy_pollute})

            elif fulloxy_value - 2 > 0 and fulloxy_value == temp["do"]:

                oxy_pollute = 0

                dict.update({"do": oxy_pollute})

        for i in self.data["rname"]:
            if "水" in i:
                tp_pollute = temp["p_total"] / 0.05
                dict.update({"p_total": tp_pollute})
            elif "湖" in i:
                tp_pollute = temp["p_total"] / 0.02
                dict.update({"p_total": tp_pollute})

        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")

        stdata = stdata.drop(index=(stdata.loc[(stdata["item"] == "do")].index))
        stdata = stdata.drop(index=(stdata.loc[(stdata["item"] == "p_total")].index))

        for i in stdata["item"]:
            if float(temp[i]) <= float(stdata[stdata["item"] == i]["I"]):
                xpollute = (temp[i]) / (stdata[stdata["item"] == i]["I"])
                for x in xpollute:
                    dict.update({i: x})

            elif float(stdata[stdata["item"] == i]["II"]) >= float(temp[i]) > float(
                    stdata[stdata["item"] == i]["I"]):
                xpollute = (temp[i]) / (stdata[stdata["item"] == i]["II"])
                for x in xpollute:
                    dict.update({i: x})

            elif float(stdata[stdata["item"] == i]["III"]) >= float(temp[i]) > float(
                    stdata[stdata["item"] == i]["II"]):
                xpollute = (temp[i]) / (stdata[stdata["item"] == i]["III"])
                for x in xpollute:
                    dict.update({i: x})

            elif float(stdata[stdata["item"] == i]["IV"]) >= float(temp[i]) > float(
                    stdata[stdata["item"] == i]["III"]):
                xpollute = (temp[i]) / (stdata[stdata["item"] == i]["IV"])
                for x in xpollute:
                    dict.update({i: x})

            elif float(temp[i]) >= float(stdata[stdata["item"] == i]["I"]):
                xpollute = (temp[i]) / (stdata[stdata["item"] == i]["V"])
                for x in xpollute:
                    dict.update({i: x})

        for i in self.data["rname"]:
            if "湖" in i:
                for j in rsdata["item"]:
                    hpollute = (temp[j]) / (rsdata[rsdata["item"] == j]["restrict"])
                    for h in hpollute:
                        dict.update({j: h})

        for k, v in dict.items():
            v = round(v, 3)
            dict2.update({k: v})
        # dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)
        self.cacheDict.update({"polluteIndex": dict2})
        return dict2

        # 11.主要污染物
    def mainpollute(self):
        lst = []
        temp1 = WaterCal.overItem(self)
        list1 = ["ni", "w_mn", "w_fe", "cn_total", "w_pb", "cr6", "cd", "w_hg", "w_zn", "w_cu"]  # 重金属
        a = [x for x in temp1 if x in list1]  # 两个列表中都存在
        if len(a) >= 3:
            return a[0:3]
        elif len(a) == 2:
            lst.append(a[0:2])
            for j in a:
                del temp1[j]
            lst.append(temp1[0])
        elif len(a) == 1:
            lst.append(a[0])
            for j in a:
                del temp1[j]
            lst.append(temp1[0:2])
        return lst

    # 5.超标样品数
    def hazard_amount(self):
        dict = {}
        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")
        data1 = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname", "stcode", "lycode", "rcode",
                                        "rscode", "lscode", "sampc", "rsc", "cq", "year", "mon", "day", "time", "wd",
                                        "wq", "wss", "w_cond", "w_temp"])

        for i, j in data1.items():
            sum = 0
            if i != "ph" or i != "do":
                for k in data1[i]:
                    if float(k) > stdata[stdata["item"] == i]["III"].values:
                        sum += 1
                dict.update({i: sum})

        k = 0
        for i in data1["ph"]:
            if i < 6 or i > 9:
                k = k + 1
                dict.update({"ph": k})

        for i in data1["do"]:
            if i < 5:
                k = k + 1
        dict.update({"do": k})
        self.cacheDict.update({"hazard_amount": dict})
        return dict

    def hazardpoint(self):
        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")
        self.data1 = self.data.drop(
            columns=["stname", "lyname", "rname", "rsname", "lsname", "stcode", "lycode", "rcode",
                     "rscode", "lscode", "sampc", "rsc", "cq", "year", "mon", "day", "time", "wd",
                     "wq", "wss", "w_cond"])
        sum = 0
        for i in self.data1.index:
            if i != "w_temp" or i != "ph" or i != "do":
                data1 = self.data1.loc[i]
                for j in data1.index:
                    if data1.loc[j] > stdata[stdata["item"] == j]["III"].values:
                        sum += 1
                        break

        for i in self.data1["ph"]:
            if i < 6 or i > 9:
                sum += 1

        for i in self.data1["do"]:
            if i < 5:
                sum += 1
        self.cacheDict.update({"hazardpoint": sum})
        return sum

    # 6.超标率 25.达标率
    def hazard_radio(self):
        dict = {}
        temp = self.cacheDict.get("hazardpoint")
        radio = temp / (self.cacheDict.get("item_amount") * 32)
        rcradio = 1 - radio
        radio = round(radio, 2) * 100
        rcradio = round(rcradio, 2) * 100
        radio = str(radio) + "%"
        rcradio = str(rcradio) + "%"
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
        self.cacheDict.update({"overItem": lst})
        return lst

    # 42.超标倍数
    def hazard_multiple(self):
        lst = []
        temp = self.cacheDict.get("overItem")
        if len(temp) == 0:
            return lst
        else:
            for i in self.data["rname"]:
                if "湖" in i:
                    stdata = std.get_standard("do_cal_gb3838r")
                else:
                    stdata = std.get_standard("do_cal_gb3838l")
            lst = []
            temp1 = self.cacheDict.get("avg")
            for i in stdata["item"]:
                if float(temp1[i]) - float(stdata[stdata["item"] == i]["III"]) > 0:
                    multiple = (float(temp1[i]) - float(stdata[stdata["item"] == i]["III"])) / float(
                        stdata[stdata["item"] == i]["III"])
                    multiple = round(multiple, 2)
                else:
                    continue
                multi = i + "(" + str(multiple) + ")"
                lst.append(multi)
            self.cacheDict.update({"hazardmultiple": lst})
            return lst

    # 10.最大超标倍数
    def max_hazard_multiple(self):
        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")
        dict = {}
        dict2 = {}
        temp = self.cacheDict.get("max")
        temp1 = self.cacheDict.get("water_level")
        for k, v in temp1.items():
            if v == "IV类" or "V类" or "劣V类":
                maxmultiple = (temp[k] / stdata[stdata["item"] == k]["III"]) - 1
                for m in maxmultiple:
                    dict.update({k: m})
        for k, v in dict.items():
            if v > 0:
                v = round(v, 3)
                dict2.update({k: v})
        self.cacheDict.update({"max_hazard_multiple": dict2})
        return dict2

    # 11.平均超标倍数
    def hazard_multiavg(self):
        dict = {}
        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")
        temp = self.cacheDict.get("overItem")
        temp1 = self.cacheDict.get("polluteIndex")
        for i in temp:
            a = temp1 / (stdata[stdata["item"] == i]["III"])
            dict.update({i: a})
        self.cacheDict.update({"hazard_multiavg": sum})
        return dict

    # 18.综合污染指数
    def comprepollute(self):
        sum = 0
        temp = WaterCal.polluteIndex(self)
        wp = temp
        for k, v in wp.items():
            sum += v
        sum = round(sum, 2)
        self.cacheDict.update({"comprepollute": sum})
        return sum

    # 19.平均污染指数
    def comprepolluteavg(self):
        temp = WaterCal.comprepollute(self)
        for i in self.data["rname"]:
            if "河" in i:
                amount = 23
                avg = temp / amount
                avg = round(avg, 2)
                return avg
        for i in self.data["rname"]:
            if "湖" in i:
                amount = 28
                avg = temp / amount
                avg = round(avg, 2)
                return avg

    # 8/9.分担率
    def share(self):
        dict = {}
        temp = self.cacheDict.get("polluteIndex")
        wp = temp
        temp1 = self.cacheDict.get("comprepollute")
        wc = temp1
        for k, v in wp.items():
            shareIndex = v / float(wc)
            shareIndex = round(shareIndex * 100, 2)
            shareIndex = str(shareIndex) + "%"
            dict.update({k: shareIndex})
        self.cacheDict.update({"share": dict})
        return dict

    # 17.单项指数
    def singleIndex(self):
        dict = {}
        data = self.data.drop(columns=["stname", "lyname", "rname", "rsname", "lsname", "stcode", "lycode", "rcode",
                                       "rscode", "lscode", "sampc", "rsc", "cq", "year", "mon", "day", "time", "wd",
                                       "wq", "wss", "w_cond"])
        temp = self.cacheDict.get("avg")
        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")
        for i in stdata["item"]:

            if float(temp[i]) <= float(stdata[stdata["item"] == i]["I"]):
                single_index = ((temp[i]) - 0) / ((stdata[stdata["item"] == i]["I"] - 0) * 20)
                for s in single_index:
                    dict.update({i: s})

            elif float(stdata[stdata["item"] == i]["II"]) <= float(temp[i]) < float(stdata[stdata["item"] == i]["I"]):
                single_index = (temp[i] - stdata[stdata["item"] == i]["I"]) / (
                            (stdata[stdata["item"] == i]["II"] - stdata[stdata["item"] == i]["I"]) * 20) + 20
                for s in single_index:
                    dict.update({i: s})

            elif float(stdata[stdata["item"] == i]["III"]) <= float(temp[i]) < float(stdata[stdata["item"] == i]["II"]):
                single_index = (temp[i] - stdata[stdata["item"] == i]["II"]) / (
                            (stdata[stdata["item"] == i]["III"] - stdata[stdata["item"] == i]["II"]) * 20) + 40
                for s in single_index:
                    dict.update({i: s})

            elif float(stdata[stdata["item"] == i]["IV"]) <= float(temp[i]) < float(stdata[stdata["item"] == i]["III"]):
                single_index = (temp[i] - stdata[stdata["item"] == i]["III"]) / (
                            (stdata[stdata["item"] == i]["IV"] - stdata[stdata["item"] == i]["III"]) * 20) + 60
                for s in single_index:
                    dict.update({i: s})

            elif float(temp[i]) > float(stdata[stdata["item"] == i]["V"]):
                dict.update({i: 900})

            elif float(temp[i]) == float(stdata[stdata["item"] == i]["V"]):
                dict.update({i: 100})


            else:
                dict.update({i: 0})

        for i in self.data["rname"]:
            if "湖" in i:
                if 6 < temp["ph"] < 9:
                    dict.update({"ph": 0})

                else:
                    dict.update({"ph": 100})

                single_index = (temp["so4"] / 250) * 60
                dict.update({"so4": single_index})

                single_index = (temp["cl"] / 250) * 60
                dict.update({"cl": single_index})

                single_index = (temp["no3_n"] / 10) * 60
                dict.update({"no3_n": single_index})

                single_index = (temp["w_fe"] / 0.3) * 60
                dict.update({"w_fe": single_index})

                single_index = (temp["w_mn"] / 0.1) * 60
                dict.update({"w_mn": single_index})

                # dict.update({"n_total": 0})

        dict = WaterCal.adjust(self, dict)
        self.cacheDict.update({"singleIndex": dict})
        return dict

    def singleIndexRank(self):
        temp = self.cacheDict.get("singleIndex")
        dict = sorted(temp.items(), key=lambda d: d[1], reverse=True)
        return dict

    # 取水总量
    def waterquantity(self):
        sum = 0
        for i in self.data["wq"]:
            sum += i
        self.cacheDict.update({"waterquantity": dict})
        return sum

    # 达标水量
    def reachwaterquantity(self):
        temp = WaterCal.waterquantity(self)
        for i in self.data["rname"]:
            if "湖" in i:
                stdata = std.get_standard("do_cal_gb3838r")
            else:
                stdata = std.get_standard("do_cal_gb3838l")
        self.data1 = self.data.drop(
            columns=["stname", "lyname", "rname", "rsname", "lsname", "stcode", "lycode", "rcode",
                     "rscode", "lscode", "sampc", "rsc", "cq", "year", "mon", "day", "time", "wd",
                     ])
        sum = 0
        for i in self.data1.index:
            data1 = self.data1.loc[i]
            for k, v in data1.items():
                lst = 0
                if k != "w_temp" and k != "ph" and k != "do":

                    if float(data1.loc[k]) > stdata[stdata["item"] == k]["III"].values:
                        lst += 1
                if lst > 0:
                    sum += data1["wq"]
        sum1 = temp - sum
        return sum1

    # 29/30/31.分类指数123
    def level_index(self):
        dict1 = {}
        dict2 = {}
        dict3 = {}
        list1 = ["se", "as", "w_hg", "cd", "cr6", "w_pb", "cn_total"]
        list2 = ["ph", "do", "codmn", "bod5", "nh4_n", "colo_org"]
        list3 = ["p_total", "n_total", "w_cu", "w_zn", "f", "v_phen", "oils", "an_saa", "s", "colo_org", "so4", "cl",
                 "no3_n", "w_fe", "w_mn"]
        temp = self.cacheDict.get("singleIndex")
        for i in self.data["rname"]:
            if "湖" in i:
                for i in list1:
                    dict1.update({i: temp[i]})
                for i in list2:
                    dict2.update({i: temp[i]})
                for i in list3:
                    dict3.update({i: temp[i]})
                return dict1, dict2, dict3
            else:
                return "无分类指数"

    # 32.水源地分类指数
    def origin_index(self):
        dict = {}
        lst1 = []
        lst2 = []
        lst3 = []
        list1 = ["se", "as", "w_hg", "cd", "cr6", "w_pb", "cn_total"]
        list2 = ["ph", "do", "codmn", "bod5", "nh4_n", "colo_org"]
        list3 = ["p_total", "n_total", "w_cu", "w_zn", "f", "v_phen", "oils", "an_saa", "s", "colo_org", "so4", "cl",
                 "no3_n", "w_fe", "w_mn"]
        temp = self.cacheDict.get("singleIndex")
        for i in self.data["rname"]:
            if "湖" in i:
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

    # 37.综合富营养化指数
    def Nutri_index(self):
        global tli_sd, tli_codmn, tli_tn, tli_tp, tli_chla
        tp_value = self.data["p_total"]
        tn_value = self.data["n_total"]
        sd_value = self.data["sd"]
        codmn_value = self.data["codmn"]
        chla_value = self.data["chla"]

        for i in self.data["rname"]:
            if "湖" in i:
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
                    "item": ["Chla", "TP", "TN", "SD", "CODMn"],
                    "value": [1, 0.84, 0.82, -0.83, 0.83],
                    "value^2": [1, 0.7056, 0.6726, 0.6889, 0.6889],
                    "TLI": [tli_chla, tli_tp, tli_tn, tli_sd, tli_codmn]
                })

                Nutri_std_sum = Nutri_std["value^2"].sum()

                for i in Nutri_std["value^2"]:
                    Wj = i / Nutri_std_sum
                    for j in Nutri_std["TLI"]:
                        Nutri_index = j * Wj
                        return Nutri_index

    # 38.湖库营养等级分类
    def hk_NutriLevel(self):
        for i in self.data["rname"]:
            if "湖" in i:
                if WaterCal.Nutri_index(self) < 30:
                    return "贫营养"
                elif 30 <= WaterCal.Nutri_index(self) <= 50:
                    return "中营养"
                elif 50 < WaterCal.Nutri_index(self) <= 60:
                    return "轻度富营养"
                elif 60 < WaterCal.Nutri_index(self) <= 70:
                    return "中度富营养"
                else:
                    return "重度富营养"

    # 评价指标计算数据精度标准化方法
    def adjust(self, dict):
        dict1 = {}
        self.dict = dict
        for k, v in self.dict.items():
            if k == "do":  # 溶解氧
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_temp":  # 温度
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "ph":  # ph值
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "codmn":  # 高锰酸盐
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "codcr":
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "bod5":  # 氨氮
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "nh4_n":  # 氨氮
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "p_total":  # 总磷
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "n_total":  # 总氮
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_cu":  # 铜
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_zn":  # 锌
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "f":  # 氟化物
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "se":  # 硒
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "as":  # 砷
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_hg":  # 汞
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "cd":  # 镉
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "cr6":  # 六价铬
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_pb":  # 铅
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "cn_total":  # 氰化物
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "v_phen":  # 挥发酚
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "an_saa":  # 阴离子表面活性剂
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "oils":  # 石油类
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "s":  # 硫化物
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "colo_org":  # 粪大肠杆菌群
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "so4":  # 硫酸盐
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "cl":  # 氯化物
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "no3_n":  # 硝酸盐
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "w_fe":  # 铁
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "w_mn":  # 锰
                v = round(v, 1)
                dict1.update({k: v})
        return dict1

    def spearman(self):
        dict1 = {}
        data = self.data[["w_temp", "ph", "do", "sd", "chla", "codmn", "codcr", "bod5", "nh4_n",
                          "p_total", "n_total", "w_cu", "w_zn", "f", "se", "as", "w_hg", "cd", "cr6",
                          "w_pb", "cn_total", "v_phen", "oils", "an_saa", "s", "colo_org", "so4", "cl",
                          "no3_n", "w_fe", "w_mn", "ni", "vel", "width", "depth", "year", "mon"]]
        lst = []
        lst1 = []
        for i in data.year.unique():
            lst.append(i)
        for i in data.mon.unique():
            lst1.append(i)
        # 年为周期判断
        if len(lst) > 4:
            for i in ["w_temp", "ph", "do", "sd", "chla", "codmn", "codcr", "bod5", "nh4_n",
                      "p_total", "n_total", "w_cu", "w_zn", "f", "se", "as", "w_hg", "cd", "cr6",
                      "w_pb", "cn_total", "v_phen", "oils", "an_saa", "s", "colo_org", "so4", "cl",
                      "no3_n", "w_fe", "w_mn", "ni", "vel", "width", "depth", "year"]:
                data[i] = data[i].rank(method="min")  # 排名
            for i in ["w_temp", "ph", "do", "sd", "chla", "codmn", "codcr", "bod5", "nh4_n",
                      "p_total", "n_total", "w_cu", "w_zn", "f", "se", "as", "w_hg", "cd", "cr6",
                      "w_pb", "cn_total", "v_phen", "oils", "an_saa", "s", "colo_org", "so4", "cl",
                      "no3_n", "w_fe", "w_mn", "ni", "vel", "width", "depth"]:
                sum1 = 0
                for j in range(len(data)):
                    a = (data.loc[j][i] - data.loc[j]["year"]) * (data.loc[j][i] - data.loc[j]["year"])
                    sum1 += a
                rs = round(1 - 6 / (len(lst) * (len(lst) ** 2 - 1)) * sum1, 2)
                dict1.update({i: rs})
        # 月为周期
        elif len(lst1) > 1:
            for i in ["w_temp", "ph", "do", "sd", "chla", "codmn", "codcr", "bod5", "nh4_n",
                      "p_total", "n_total", "w_cu", "w_zn", "f", "se", "as", "w_hg", "cd", "cr6",
                      "w_pb", "cn_total", "v_phen", "oils", "an_saa", "s", "colo_org", "so4", "cl",
                      "no3_n", "w_fe", "w_mn", "ni", "vel", "width", "depth", "mon"]:
                data[i] = data[i].rank(method="min")
            for i in ["w_temp", "ph", "do", "sd", "chla", "codmn", "codcr", "bod5", "nh4_n",
                      "p_total", "n_total", "w_cu", "w_zn", "f", "se", "as", "w_hg", "cd", "cr6",
                      "w_pb", "cn_total", "v_phen", "oils", "an_saa", "s", "colo_org", "so4", "cl",
                      "no3_n", "w_fe", "w_mn", "ni", "vel", "width", "depth"]:
                sum1 = 0
                for j in range(len(data)):
                    a = (data.loc[j][i] - data.loc[j]["mon"]) * (data.loc[j][i] - data.loc[j]["mon"])
                    sum1 += a
                rs = round(1 - 6 / (len(lst1) * (len(lst1) ** 2 - 1)) * sum1, 2)
                dict1.update({i: rs})
        else:
            dict1.update({"spearman": "不存在"})
        return dict1