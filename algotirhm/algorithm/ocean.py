# '漂浮物质':'drifter'
# '色、臭、味':'color'
# '悬浮物质':'wss'
# '大肠杆菌群':'coll_group'
# '粪大肠杆菌群':'colo_org'
#  '病原体':'pathogene'
# '溶解氧': 'do'
# '化学需氧量':'codcr'
# '生化需氧量':'bod5'
# '无机氮': 'n_inorganic'
# '非离子氨':'non-iron_an',
# '活性磷酸盐':'po4',
# '汞':'w_hg'
# '镉':'cd'
# '铅':'w_pb'
# '六价铬':'cr6'
# '总铬‘：'cr'
# '砷'：'as'
# '铜'：'w_cu'
# '锌'：'w_zn'
# '硒'：'se’
# '镍'：'ni'
# '氰化物'：'cn_total'
# '硫化物'：'s'
# '挥发性酚'：'v_phen'
# '石油类'：'oils'
# '六六六'：'hexa'
# '滴滴涕：'ddt
# '马拉硫磷'：'chops'
# '甲基对硫磷'：'chnops'
# '苯并芘'：'benzo'
# '阴离子表面活性剂'：'an_saa',
# '40Co':‘40Co''
# '90Sr':'90Sr',
# '106Rn':'106Rn'
# '134Cs':'134Cs'
# '137Cs':'137Cs'

import pandas as pd
import numpy as np
import math
import json
import algotirhm.common.standard as std

"""
def timeit(func):
    def wap(self):
        import time
        start = time.time()
        func(self)
        end = time.time()
        print('耗费时间：%s' % (end - start))
    return wap
"""


class OceanCal(object):

    cacheDict = {}

    def __init__(self, data):
        self.data = data

    def showdata(self):  # 展示数据概况
        return self.data

# 1、计算样品数
    def item_amount(self):
        yps = self.data['rname'].count()
        self.cacheDict.update({"item_amount": yps})
        return yps

# 2、计算超标样品数
    def item_over_amount(self):
        dict1 = {}
        stdata = std.get_standard('do_cal_hj442')
        k = 0
        for i in self.data['ph']:
            if i < 7.8 or i > 8.5:
                k = k + 1
        dict1.update({'ph': k})
        k1 = 0
        for j in self.data['do']:
            if j <= 5:
                k1 += 1
        dict1.update({'do': k1})
        data1 = self.data.drop(columns=['rsname', 'lsname', 'rname', 'time', 'w_temp', 'do', 'ph'])
        for i, j in data1.items():
            sum1 = 0
            for k in data1[i]:
                if k > stdata[stdata['item'] == i]['II'].values:
                    sum1 += 1
            dict1.update({i: sum1})
        self.cacheDict.update({"item_over_amount": dict1})
        return dict1

    def ph_avg(self):
        # pH值是无量纲指标，所以先要讲pH值转化为H离子浓度再求平均值，然后再转化成pH值的平均值
        sum1 = 0
        ph_avg = 0
        data = self.data['ph']
        data = data.dropna()
        for i in data:
            i = 10 ** (-i)
            sum1 += i
            ph_avg = -math.log10(sum1 / len(data))
        return ph_avg

    # def colo_org_avg(self):
    #     data = self.data['colo_org']
    #     data = data.dropna()
    #     for i in data:
    #         sum = 0
    #         sum += math.log10(i)
    #         colo_org_avg = 10 ** (sum / len(data))
    #     return colo_org_avg

    # 3、平均值
    def item_avg(self):
        item_avg = self.data.mean()
        item_avg["ph"] = OceanCal.ph_avg(self)
        item_avg = item_avg.to_dict()
        item_avg = OceanCal.adjust(self, item_avg)
        return item_avg

    # 4、超标项目
    def excess_item(self):
        stdata = std.get_standard('do_cal_hj442')
        lst = []
        a = OceanCal.item_avg(self)
        if a['ph'] < 7.8 or a['ph'] > 8.5:
            lst.append('ph')
        if a['do'] <= 5:
            lst.append('do')
        data1 = self.data.drop(columns=['rsname', 'lsname', 'rname', 'time', 'w_temp', 'ph', 'do'])
        for i in data1.columns:
            for j in stdata['item']:
                if i == j:
                    if a[i] > stdata[stdata['item'] == i]['II'].values:
                        lst.append(i)
        return lst

# 5、主要污染项目
    def main_pollute(self):
        lst = []
        lst1 = []
        dict1 = {}
        a = OceanCal.excess_multiple(self)
        for i, j in a.items():
            lst.append(i)
            lst1.append(j)
        df = pd.DataFrame(index=lst)
        df['values'] = lst1
        df = df.sort_values(by='values', ascending=False)
        lst2 = df.index.tolist()
        if len(lst2) > 3:
            dict1.update({"主要污染项目": [lst2[0], lst2[1], lst2[2]]})
        elif len(lst2) > 0:
            dict1.update({'主要污染项目': lst2})
        elif len(lst2) == 0:
            dict1.update({"主要污染项目": '不存在'})
        return lst2

# 6、超标率
    def excess_rate(self):
        dict1 = {}
        b = OceanCal.item_over_amount(self)
        for i, j in b.items():
            if i != 'no2_n' and i != 'nh4_n' and i != 'no3_n':
                data = self.data[i]
                data = data.dropna()
                dict1.update({i: j/len(data)})
        dict1 = OceanCal.adjust(self, dict1)
        return dict1

# 7、超标倍数
    def excess_multiple(self):
        dict1 = {}
        stdata = std.get_standard('do_cal_hj442')
        b = OceanCal.item_avg(self)
        for i, j in b.items():
            a = stdata[stdata['item'] == i]['II'].values
            if i != "ph" and i != "w_temp" and i != "do":
                if j > a:
                    b = j / a - 1
                    for x in b:
                        dict1.update({i: x})
        dict1 = OceanCal.adjust(self, dict1)
        return dict1

# 8、水质类别
    def water_level(self):
        stdata = std.get_standard('do_cal_hj442')
        df = pd.DataFrame(index=self.data['time'])
        for i in self.data.columns:
            for k in stdata['item']:
                if i == k:
                    lst = []
                    data = self.data[i]
                    data = data.dropna()
                    a = stdata[stdata['item'] == i]
                    for j in data:
                        if j <= a['I'].values:
                            lst.append("I类")
                        elif j <= a['II'].values:
                            lst.append("II类")
                        elif j <= a['III'].values:
                            lst.append("III类")
                        elif j <= a['IV'].values:
                            lst.append("IV类")
                        elif j > a['IV'].values:
                            lst.append("IIIII类")
                    df[i] = lst
        lst1 = []
        data1 = self.data['ph']
        data1 = data1.dropna()
        for k in data1:
            if 7.8 <= k <= 8.5:
                lst1.append("I类")
            elif 6.8 <= k <= 8.5:
                lst1.append("III类")
            else:
                lst1.append('IIIII类')
        df['ph'] = lst1
        lst2 = []
        for i in self.data['time']:
            data = self.data[self.data['time'] == i]
            data = data.dropna()
            if data['do'].values > 6:
                lst2.append("I类")
            elif data['do'].values > 5:
                lst2.append("II类")
            elif data['do'].values > 4:
                lst2.append("III类")
            elif data['do'].values >= 3:
                lst2.append("IV类")
            elif data['do'].values < 3:
                lst2.append("IIIII类")
        dict1 = {}
        df['do'] = lst2
        for i in df.index:
            lst3 = []
            for j in df.loc[i]:
                lst3.append(j)
                lst3.sort()
                if lst3[0] == 'IIIII类':
                    dict1.update({i: '劣IV类'})
                else:
                    dict1.update({i: lst3[0]})
        return dict1

# 9、水质级别
    def water_grade(self):
        dict1 = {}
        a = OceanCal.water_level(self)
        for i, j in a.items():
            if j == "I类":
                dict1.update({i: "优"})
            elif j == "II类":
                dict1.update({i: "良好"})
            elif j == "III类":
                dict1.update({i: "一般"})
            elif j == "IV类":
                dict1.update({i: "差"})
            elif j == "劣IV类":
                dict1.update({i: "极差"})
        return dict1

# 10、海水类别比例
    def water_level_percent(self):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        sum5 = 0
        b = OceanCal.water_level(self)
        for i, j in b.items():
            if j == 'I类':
                sum1 += 1
            elif j == 'II类':
                sum2 += 1
            elif j == 'III类':
                sum3 += 1
            elif j == 'IV类':
                sum4 += 1
            elif j == '劣IV类':
                sum5 += 1
        a = len(self.data['rname'])
        sum1 = round(sum1 / a, 3)
        sum2 = round(sum2 / a, 3)
        sum3 = round(sum3 / a, 3)
        sum4 = round(sum4 / a, 3)
        sum5 = round(sum5 / a, 3)
        df = pd.DataFrame(index=['I类', 'II类', 'III类', 'IV类', '劣IV类'])
        df['percent'] = [sum1, sum2, sum3, sum4, sum5]
        df = df.sort_values(by='percent', ascending=False)
        pollute = df.to_json()
        pollute = json.loads(pollute)
        return pollute

# 11、主要水质类别
    def main_water_level(self):
        lst = []
        lst1 = []
        lst2 = []
        # 使用两次items()是因为a是DataFrame
        a = OceanCal.water_level_percent(self)
        for i, j in a.items():
            for v, k in j.items():
                lst.append(k)
                lst1.append(v)
        if lst[0] > 0.5:
            return lst[0]
        elif lst[0] + lst[1] > 0.7:
            return lst1[0], lst1[1]
        else:
            return lst2

# 12、污染物指数
    def pollu_index(self):
        df = pd.DataFrame(index=self.data.time)
        stdata = std.get_standard('do_cal_hj442')
        for j in stdata['item']:
            for k in self.data.columns:
                if j == k:
                    lst = []
                    data = self.data[j]
                    a = stdata[stdata['item'] == j]
                    for v in data:
                        if v < a['I'].values:
                            b = v / a['I'].values
                            for x in b:
                                lst.append(x)
                        elif v < a['II'].values:
                            b = v / a['I'].values
                            for x in b:
                                lst.append(x)
                        elif v < a['III'].values:
                            b = v / a['I'].values
                            for x in b:
                                lst.append(x)
                        else:
                            b = v / a['I'].values
                            for x in b:
                                lst.append(x)
                    df[j] = lst
        lst1 = []
        for k in self.data['ph']:
            if 7.8 < k < 8.5:
                a = abs(k - 0.5 * (8.5 + 7.8)) / (0.5 * (8.5 - 7.8))
                lst1.append(a)
            else:
                a = abs(k - 0.5 * (8.8 + 6.8)) / (0.5 * (8.8 - 6.8))
                lst1.append(a)
        df['ph'] = lst1
        lst2 = []
        for i in self.data['time']:
            data = self.data[self.data['time'] == i]
            do = 468 / (31.6 + data['w_temp'].values)
            if data['do'].values > 6:
                a = abs(do - data['do'].values) / (do - 6)
                for j in a:
                    lst2.append(j)
            elif data['do'].values > 5:
                a = abs(do - data['do'].values) / (do - 5)
                for j in a:
                    lst2.append(j)
            elif data['do'].values > 4:
                a = abs(do - data['do'].values) / (do - 4)
                for j in a:
                    lst2.append(j)
            elif data['do'].values >= 3:
                a = abs(do - data['do'].values) / (do - 3)
                for j in a:
                    lst2.append(j)
            else:
                a = 10 - 9 * do / 3
                for j in a:
                    lst2.append(j)
        df['do'] = lst2
        for i in ['drifter', 'color-smell', 'pathogene', 'n_inorganic', 'cr', 'oil', 'an_saa', '40Co']:
            for j in df.columns:
                if i == j:
                    df[i] = df[i].apply(lambda x: round(x, 2))
        for i in ['colo_org', "coll_group", 'w_temp', 'do', 'codcr', 'bod5', '90Sr']:
            for j in df.columns:
                if i == j:
                    df[i] = df[i].apply(lambda x: round(x, 0))
        for i in ['ph', '106Rn', '134Cs', '137Cs']:
            for j in df.columns:
                if i == j:
                    df[i] = df[i].apply(lambda x: round(x, 1))
        for i in ['non-iron_an', 'po4', 'cd', 'w_pb', 'cr6', 'as', 'w_cu', 'w_zn', 'se', 'ni', 'cn_total', 'v_phen', 'hexa']:
            for j in df.columns:
                if i == j:
                    df[i] = df[i].apply(lambda x: round(x, 3))
        for i in ['w_hg', 'ddt']:
            for j in df.columns:
                if i == j:
                    df[i] = df[i].apply(lambda x: round(x, 5))
        pollute_index = df.to_json()
        pollute_index = json.loads(pollute_index)
        return pollute_index

# 13、无机氮
    def inorganic_n(self):
        dict1 = {}
        for i in self.data['time']:
            data = self.data[self.data['time'] == i]
            sum1 = (data['no3_n'].values + data['no2_n'].values + data["nh4_n"].values) * 14 * 0.001
            for x in sum1:
                dict1.update({i: x})
        return dict1

# 14、非离子氨
    def non_iron_an(self):
        dict1 = {}
        for i in self.data['time']:
            data = self.data[self.data['time'] == i]
            pk = 9.245 + 0.002949 * data['san'].values + 0.0324 * (298 - data['w_temp'].values)
            f = 100 / (10 ** (pk - 1) + 1)
            nh3 = 14 * 0.00001 * data['nh4_n'].values * f
            for x in nh3:
                dict1.update({i: x})
        return dict1

# 15、计算富营养化系数
    def nutri_index(self):
        dict1 = {}
        for i in self.data['time']:
            data = self.data[self.data['time'] == i]
            df = np.array(data['codcr']) * np.array(data['n_inorganic']) * np.array(data['po4'])
            df = df / 4500 * 10 ** 6
            for x in df:
                dict1.update({i: round(x, 2)})
        return dict1

# 16、水质富营养等级
    def nutri_grade(self):
        dict1 = {}
        a = OceanCal.nutri_index(self)
        for i, j in a.items():
            if j < 1:
                dict1.update({i: "贫营养"})
            elif j < 2.0:
                dict1.update({i: "轻度富营养"})
            elif j < 5:
                dict1.update({i: "中度富营养"})
            elif j < 15:
                dict1.update({i: "重度营养"})
            elif j > 5:
                dict1.update({i: "严重富营养"})
        return dict1

# 17、监测站沉积物质量类别:共八种沉积物，筛选出来原始数据有的污染物后，求出原始数据污染物对应的污染物级别，求出所在监测站的水质类别
    def sediment_level(self):
        dict1 = {}
        t = ['w_hg', 'cd', 'w_pb', 'w_zn', 'w_cu', 'as', 'organic_c', 'oils']
        lst = []
        stdata = std.get_standard('do_cal_hj442')
        for i in self.data.columns:
            for j in t:
                if i == j:
                    lst.append(i)
        df = pd.DataFrame(index=self.data['time'])
        for j in lst:
            lst1 = []
            for i in self.data['time']:
                data = self.data[self.data['time'] == i][j].values
                if data <= stdata[stdata['item'] == j]['I'].values:
                    lst1.append('I类')
                elif data <= stdata[stdata['item'] == j]['II'].values:
                    lst1.append('II类')
                elif data <= stdata[stdata['item'] == j]['III'].values:
                    lst1.append('III类')
                elif data <= stdata[stdata['item'] == j]['IV'].values:
                    lst1.append('IV类')
                elif data > stdata[stdata['item'] == j]['IV'].values:
                    lst1.append('劣IV类')
            df[j] = lst1
        for i in df.index:
            lst3 = []
            for j in df.loc[i]:
                lst3.append(j)
                lst3.sort()
            dict1.update({i: lst3[-1]})
        return dict1

# 18、监测站质量类别
    def sediment_levelpercent(self):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        sum5 = 0
        dict1 = {}
        a = OceanCal.sediment_level(self)
        for i, j in a.items():
            if j == 'I类':
                sum1 += 1
            elif j == 'II类':
                sum2 += 1
            elif j == 'III类':
                sum3 += 1
            elif j == 'IV类':
                sum4 += 1
            elif j == '劣IV类':
                sum5 += 1
        sum0 = sum1 + sum2 + sum3 + sum4 + sum5
        dict1.update({'I类': round(sum1/sum0, 3)})
        dict1.update({'II类': round(sum2 / sum0, 3)})
        dict1.update({'III类': round(sum3 / sum0, 3)})
        dict1.update({'IV类': round(sum4 / sum0, 3)})
        dict1.update({'劣IV类': round(sum5 / sum0, 3)})
        return dict1


# 19、沉积物质量类别
    def sediment_quality(self):
        dict1 = {}
        a = OceanCal.sediment_level(self)
        for i, j in a.items():
            if j == 'I类':
                dict1.update({i: '优良'})
            elif j == "II类":
                dict1.update({i: "一般"})
            elif j == "III类":
                dict1.update({i: "差"})
            elif j == "IV类" or i == "劣IV类":
                dict1.update({i: "极差"})
        return dict1

# 20、主要沉积物质量类别
    def main_sediment_percent(self):
        lst1 = []
        lst = []
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        b = OceanCal.sediment_quality(self)
        for i, j in b.items():
            if j == 'I类':
                sum1 += 1
            elif j == 'II类':
                sum2 += 1
            elif j == 'III类':
                sum3 += 1
            elif j == '劣III类':
                sum4 += 1
        a = len(self.data['rname'])
        sum1 = round(sum1 / a, 3)
        sum2 = round(sum2 / a, 3)
        sum3 = round(sum3 / a, 3)
        sum4 = round(sum4 / a, 3)
        df = pd.DataFrame(index=['I类', 'II类', 'III类', '劣III类'])
        df['percent'] = [sum1, sum2, sum3, sum4]
        df = df.sort_values(by='percent', ascending=False)
        for i in df['percent']:
            lst.append(i)
        if lst[0] > 0.5:
            return df.index[0]
        elif lst[0] + lst[1] > 0.7:
            return df.index[0], df.index[1]
        else:
            return lst1

# 21、综合污染指数
    def comp_pollute_index(self):
        stdata = std.get_standard('do_cal_hj442')
        dict1 = {}
        dict2 = {}
        k = OceanCal.item_avg(self)
        for i1, j1 in k.items():
            for i2 in stdata['item']:
                if i1 == i2:
                    a = k[i1] / stdata[stdata['item'] == i1]['II'].values
                    for x in a:
                        dict1.update({i1: x})
        a = abs(k["ph"] - 7.5)/1.5
        dict1.update({'ph': a})
        b = k['do']
        do_max = 3 + (max(self.data['w_temp'])-b) * (6 - 3)
        if do_max > 5 and b < do_max:
            pollute_index = (do_max - b)/(do_max - 5)
        elif 5 < do_max <= b:
            pollute_index = 0
        else:
            pollute_index = np.nan
        dict1.update({'do': pollute_index})
        sum1 = 0
        for i, j in dict1.items():
            sum1 += j
        a = round(sum1, 2)
        return a

    # 数据精度
    def adjust(self, dict):
        dict1 = {}
        self.dict = dict
        for k, v in self.dict.items():
            if k == "drifter":  # 漂浮物
                v = round(v, 2)
                dict1.update({k: v})
            elif k == 'w_temp':  # 水温
                v = round(v, 1)
                dict1.update({k: v})
            elif k == 'ph':  # ph
                v = round(v, 1)
                dict1.update({k: v})
            elif k == 'color-smell':  # 色、臭和味
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "wss":  # 悬浮物
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "coll_group":  # 大肠杆菌群
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "colo_org":  # 粪大肠杆菌
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "pathogene":  # 病原体
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "do":  # 溶解氧
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "codcr":  # 化学需氧量
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "bod5":  # 生化需氧量
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "n_inorganic":  # 无机氮
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "non-iron_an":  # 无机氮
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "po4":  # 磷酸盐
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "w_hg":  # 汞
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "cd":  # 镉
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "w_pb":  # 铅
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "cr6":  # 六价铬
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "cr":  # 铬
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "as":  # 砷
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "w_cu":  # 铜
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "w_zn":  # 锌
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "se":  # 硒
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "ni":  # 镍
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "cn_total":  # 氰化物
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "s":  # 硫化物
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "v_phen":  # 挥发酚
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "oils":  # 石油类
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "hexa":  # 六六六
                v = round(v, 3)
                dict1.update({k: v})
            elif k == "ddt":  # 滴滴涕
                v = round(v, 5)
                dict1.update({k: v})
            elif k == "chops":  # 马拉硫磷
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "chnops":  # 甲基对硫磷
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "benzo":  # 苯并芘
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "an_saa":  # 阴离子表面活性剂
                v = round(v, 2)
                dict1.update({k: v})
            elif k == "40Co":  # 钴40
                v = round(v, 4)
                dict1.update({k: v})
            elif k == "90Sr":  # 锶90
                v = round(v, 0)
                dict1.update({k: v})
            elif k == "106Rn":  # 氡106
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "134Cs":  # 铯134
                v = round(v, 1)
                dict1.update({k: v})
            elif k == "137Cs":  # 铯137
                v = round(v, 1)
                dict1.update({k: v})
        return dict1
