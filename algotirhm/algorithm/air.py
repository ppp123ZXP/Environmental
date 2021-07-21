import pandas as pd
import numpy as np
import algotirhm.common.standard as std
import json
import math


# 计算污染物的分指数：
# 1.1、计算SO2的分指数：
class AirCal(object):
    cacheDict = {}

    def __init__(self, data):
        self.data = data

    def showdata(self):  # 展示数据概况
        return self.data
#so2分指数计算?

    def airAvg(self):  # 计算大气污染物的平均值
        data1 = self.data.drop(columns=["year", "mon", "day", "hour"])
        data = data1.mean()
        self.cacheDict.update({"airAvg": data})
        item_avg = data.to_dict()
        return item_avg

    def pollute_fzs(self):
        dict1 = {}
        stdata = std.get_standard('do_cal_hj633')
        so2 = stdata[stdata['item'] == 'so2_fzs']
        avg = AirCal.airAvg(self)
        if float(avg["so2"]) <= float(so2['I']):
            so2_index = math.ceil((50 - 0) / (so2['I'] - 0) * (avg["so2"] - 0) + 0)
            dict1.update({'so2': so2_index})
        elif float(so2['I']) < float(avg["so2"]) <= float(so2['II']):
            so2_index = math.ceil((100 - 50) / (float(so2['II']) - float(so2['I'])) * (float(avg["so2"]) - 50) + 50)
            dict1.update({'so2': so2_index})
        elif float(so2['II']) < float(avg["so2"]) <= float(so2['III']):
            so2_index = math.ceil(
                (150 - 100) / (float(so2['III']) - float(so2['II'])) * (float(avg["so2"]) - 150) + 100)
            dict1.update({'so2': so2_index})
        elif float(so2['III']) < float(avg["so2"]) <= float(so2['IV']):
            so2_index = math.ceil(
                (200 - 150) / (float(so2['IV']) - float(so2['III'])) * (float(avg["so2"]) - 475) + 150)
            dict1.update({'so2': so2_index})
        elif float(so2['IV']) < float(avg["so2"]) <= float(so2['V']):
            so2_index = math.ceil((300 - 200) / (float(so2['V']) - float(so2['IV'])) * (float(avg["so2"]) - 800) + 200)
            dict1.update({'so2': so2_index})
        elif float(so2['V']) < float(avg["so2"]) <= float(so2['VI']):
            so2_index = math.ceil((400 - 300) / (float(so2['VI']) - float(so2['V'])) * (float(avg["so2"]) - 1600) + 300)
            dict1.update({'so2': so2_index})
        else:
            so2_index = math.ceil(
                (500 - 400) / (float(so2['VII']) - float(so2['VI'])) * (float(avg["so2"]) - 2100) + 400)
            dict1.update({'so2': so2_index})

        no2 = stdata[stdata['item'] == 'no2_fzs']
        if float(avg["no2"]) <= float(no2['I']):
            no2_index = math.ceil((50 - 0) / (float(no2['I']) - 0) * (float(avg["no2"]) - 0) + 0)
            dict1.update({'no2': no2_index})
        elif float(no2['I']) < float(avg["no2"]) <= float(no2['II']):
            no2_index = math.ceil((100 - 50) / (float(no2['II']) - float(no2['I'])) * (float(avg["no2"]) - 40) + 50)
            dict1.update({'no2': no2_index})
        elif float(no2['II']) < float(avg["no2"]) <= float(no2['III']):
            no2_index = math.ceil((150 - 100) / (float(no2['III']) - float(no2['II'])) * (float(avg["no2"]) - 80) + 100)
            dict1.update({'no2': no2_index})
        elif float(no2['III']) < float(avg["no2"]) <= float(no2['IV']):
            no2_index = math.ceil(
                (200 - 150) / (float(no2['IV']) - float(no2['III'])) * (float(avg["no2"]) - 180) + 150)
            dict1.update({'no2': no2_index})
        elif float(no2['IV']) < float(avg["no2"]) <= float(no2['V']):
            no2_index = math.ceil((300 - 200) / (float(no2['V']) - float(no2['IV'])) * (float(avg["no2"]) - 280) + 200)
            dict1.update({'no2': no2_index})
        elif float(no2['V']) < float(avg["no2"]) <= float(no2['VI']):
            no2_index = math.ceil((400 - 300) / (float(no2['VI']) - float(no2['V'])) * (float(avg["no2"]) - 565) + 300)
            dict1.update({'no2': no2_index})
        else:
            no2_index = math.ceil(
                (500 - 400) / (float(no2['VII']) - float(no2['VI'])) * (float(avg["no2"]) - 750) + 400)
            dict1.update({'no2': no2_index})

        if float(avg["o3"]) < 800:
            o3 = stdata[stdata['item'] == 'o3_fzs']
            if float(avg["o3"]) <= float(o3['I']):
                o3_index = math.ceil((50 - 0) / (float(o3['I']) - 0) * (float(avg["o3"]) - 0) + 0)
                dict1.update({'o3': o3_index})
            elif float(o3['I']) < float(avg["o3"]) <= float(o3['II']):
                o3_index = math.ceil(((100 - 50) / (float(o3['II']) - float(o3['I'])) * (float(avg["o3"]) - 160) + 50))
                dict1.update({'o3': o3_index})
            elif float(o3['II']) < float(avg["o3"]) <= float(o3['III']):
                o3_index = math.ceil(
                    (150 - 100) / (float(o3['III']) - float(o3['II'])) * (float(avg["o3"]) - 200) + 100)
                dict1.update({'o3': o3_index})
            elif float(o3['III']) < float(avg["o3"]) <= float(o3['IV']):
                o3_index = math.ceil(
                    (200 - 150) / (float(o3['IV']) - float(o3['III'])) * (float(avg["o3"]) - 300) + 150)
                dict1.update({'o3': o3_index})
            elif o3['IV'] < float(avg["o3"]) <= float(o3['V']):
                o3_index = math.ceil((300 - 200) / (float(o3['V']) - float(o3['IV'])) * (float(avg["o3"]) - 400) + 200)
                dict1.update({'o3': o3_index})
        else:
            dict1.update({'o3': 0})

        co = stdata[stdata['item'] == 'co_fzs']
        if float(avg["co"]) <= float(co['I']):
            co_index = math.ceil((50 - 0) / (float(co['I']) - 0) * (float(avg["co"]) - 0) + 0)
            dict1.update({'co': co_index})
        elif float(co['I']) < float(avg["co"]) <= float(co['II']):
            co_index = math.ceil((100 - 50) / (float(co['II']) - float(co['I'])) * (float(avg["co"]) - 2) + 50)
            dict1.update({'co': co_index})
        elif float(co['II']) < float(avg["co"]) <= float(co['III']):
            co_index = math.ceil((150 - 100) / (float(co['III']) - float(co['II'])) * (float(avg["co"]) - 4) + 100)
            dict1.update({'co': co_index})
        elif float(co['III']) < float(avg["co"]) <= float(co['IV']):
            co_index = math.ceil((200 - 150) / (float(co['IV']) - float(co['III'])) * (float(avg["co"]) - 14) + 150)
            dict1.update({'co': co_index})
        elif float(co['IV']) < float(avg["co"]) <= float(co['V']):
            co_index = math.ceil((300 - 200) / (float(co['V']) - float(co['IV'])) * (float(avg["co"]) - 24) + 200)
            dict1.update({'co': co_index})
        elif float(co['V']) < float(avg["co"]) <= float(co['VI']):
            co_index = math.ceil((400 - 300) / (float(co['VI']) - float(co['V'])) * (float(avg["co"]) - 36) + 300)
            dict1.update({'co': co_index})
        else:
            co_index = math.ceil((500 - 400) / (float(co['VII']) - float(co['VI'])) * (float(avg["co"]) - 48) + 400)
            dict1.update({'co': co_index})

        pm25 = stdata[stdata['item'] == 'pm25_fzs']
        if float(avg["pm25"]) <= float(pm25['I']):
            pm25_index = math.ceil((50 - 0) / (float(pm25['I']) - 0) * (float(avg["pm25"]) - 0) + 0)
            dict1.update({'pm25': pm25_index})
        elif float(pm25['I']) < float(avg["pm25"]) <= float(pm25['II']):
            pm25_index = math.ceil((100 - 50) / (float(pm25['II']) - float(pm25['I'])) * (float(avg["pm25"]) - 35) + 50)
            dict1.update({'pm25': pm25_index})
        elif float(pm25['II']) < float(avg["pm25"]) <= float(pm25['III']):
            pm25_index = math.ceil(
                (150 - 100) / (float(pm25['III']) - float(pm25['II'])) * (float(avg["pm25"]) - 75) + 100)
            dict1.update({'pm25': pm25_index})
        elif float(pm25['III']) < float(avg["pm25"]) <= float(pm25['IV']):
            pm25_index = math.ceil(
                (200 - 150) / (float(pm25['IV']) - float(pm25['III'])) * (float(avg["pm25"]) - 115) + 150)
            dict1.update({'pm25': pm25_index})
        elif float(pm25['IV']) < float(avg["pm25"]) <= float(pm25['V']):
            pm25_index = math.ceil(
                (300 - 200) / (float(pm25['V']) - float(pm25['IV'])) * (float(avg["pm25"]) - 150) + 200)
            dict1.update({'pm25': pm25_index})
        elif float(pm25['V']) < float(avg["pm25"]) <= float(pm25['VI']):
            pm25_index = math.ceil(
                (400 - 300) / (float(pm25['VI']) - float(pm25['V'])) * (float(avg["pm25"]) - 250) + 300)
            dict1.update({'pm25': pm25_index})
        else:
            pm25_index = math.ceil(
                (500 - 400) / (float(pm25['VII']) - float(pm25['VI'])) * (float(avg["pm25"]) - 350) + 400)
            dict1.update({'pm25': pm25_index})

        pm10 = stdata[stdata['item'] == 'pm10_fzs']
        if float(avg["pm10"]) <= float(pm10['I']):
            pm10_index = math.ceil((50 - 0) / (float(pm10['I']) - 0) * (float(avg["pm10"]) - 0) + 0)
            dict1.update({'pm10': pm10_index})
        elif float(pm10['I']) < float(avg["pm10"]) <= float(pm10['II']):
            pm10_index = math.ceil((100 - 50) / (float(pm10['II']) - float(pm10['I'])) * (float(avg["pm10"]) - 50) + 50)
            dict1.update({'pm10': pm10_index})
        elif float(pm10['II']) < float(avg["pm10"]) <= float(pm10['III']):
            pm10_index = math.ceil(
                (150 - 100) / (float(pm10['III']) - float(pm10['II'])) * (float(avg["pm10"]) - 150) + 100)
            dict1.update({'pm10': pm10_index})
        elif float(pm10['III']) < float(avg["pm10"]) <= float(pm10['IV']):
            pm10_index = math.ceil(
                (200 - 150) / (float(pm10['IV']) - float(pm10['III'])) * (float(avg["pm10"]) - 250) + 150)
            dict1.update({'pm10': pm10_index})
        elif float(pm10['IV']) < float(avg["pm10"]) <= float(pm10['V']):
            pm10_index = math.ceil(
                (300 - 200) / (float(pm10['V']) - float(pm10['IV'])) * (float(avg["pm10"]) - 350) + 200)
            dict1.update({'pm10': pm10_index})
        elif float(pm10['V']) < float(avg["pm10"]) <= float(pm10['VI']):
            pm10_index = math.ceil(
                (400 - 300) / (float(pm10['VI']) - float(pm10['V'])) * (float(avg["pm10"]) - 420) + 300)
            dict1.update({'pm10': pm10_index})
        else:
            pm10_index = math.ceil(
                (500 - 400) / (float(pm10['VII']) - float(pm10['VI'])) * (float(avg["pm10"]) - 500) + 400)
            dict1.update({'pm10': pm10_index})
        self.cacheDict.update({"pollute_fzs": dict1})
        return dict1

    # 2、求空气质量指数
    def aqi(self):
        list = []
        a = self.cacheDict.get("pollute_fzs")
        for k, v in a.items():
            list.append(v)
        list.sort()
        b = list[-1]
        self.cacheDict.update({"aqi": b})
        return b

    # 3、计算首要污染物,：AQI>50时
    def first_pollute(self):
        a = self.cacheDict.get("aqi")
        temp = self.cacheDict.get("pollute_fzs")
        lst1 = []
        if a > 50:
            for i, j in temp.items():
                if j == a:
                    lst1.append(i)
        self.cacheDict.update({"first_pollute": lst1})
        return lst1

    # 4、计算AQI对应的等级
    def aqi_quality(self):
        v = self.cacheDict.get("aqi")
        if v <= 50:
            return '一级'
        elif v <= 100:
            return '二级'
        elif v <= 150:
            return '三级'
        elif v <= 200:
            return '四级'
        elif v <= 300:
            return '五级'
        elif v > 300:
            return '六级'

    # 4、计算AQI对应的空气质量类别
    def aqi_level(self):
        v = self.cacheDict.get("aqi")
        if v <= 50:
            return '优'
        elif v <= 100:
            return '良'
        elif v <= 150:
            return '轻度污染'
        elif v <= 200:
            return '中度污染'
        elif v <= 300:
            return '重度污染'
        elif v > 300:
            return '严重污染'

    # 5、单项指数：年污染物浓度均值和二级浓度限值的值和24小时百分位数与百分位数的二级限制比较的最大值（24小时的so2和no2的98分位，pm10和pm25、co的95分位）
    def single_index(self):
        data = self.data
        # 先求年度均值
        data1 = data.groupby(['rname', 'year']).mean()[['so2', 'no2', 'pm10', 'pm25']]
        data1['so2'] = round(data1['so2'] / 60, 2)
        data1['pm25'] = round(data1['pm25'] / 35, 2)
        data1['no2'] = round(data1['no2'] / 40, 2)
        data1['pm10'] = round(data1['pm10'] / 70, 2)
        list = []
        list1 = []
        for i in data1.index:
            list.append(i[0])
            list1.append(i[1])
        data1['rname1'] = list
        data1['year1'] = list1
        data1['rname-year'] = data1['rname1'].map(str) + '.' + data1['year1'].map(str)
        data1.index = data1['rname-year']
        data1.drop(columns=['rname1', 'year1'], inplace=True)
        # 再求年平均24小时百分位数:先求除了臭氧的其他污染物，再求臭氧8小时
        data2 = data.groupby(['rname', 'year', 'mon', 'day']).mean()[['so2', 'no2', 'pm10', 'pm25', 'co']]
        lst = []
        lst1 = []
        lst2 = []
        lst3 = []
        for i in data2.index:
            lst.append(i[0])
            lst1.append(i[1])
            lst2.append(i[2])
            lst3.append(i[3])
        data2['rname1'] = lst
        data2['year1'] = lst1
        data2['mon1'] = lst2
        data2['day1'] = lst3
        data2['rname-Y-M-D'] = data2['rname1'].map(str) + '-' + data2['year1'].map(str) + '-' + data2['mon1'].map(
            str) + '-' + data2['day1'].map(str)
        data2.index = data2['rname-Y-M-D']
        data2['rname-year'] = data2['rname1'].map(str) + '.' + data2['year1'].map(str)
        data2.drop(columns=['rname1', 'year1', 'mon1', 'day1', 'rname-Y-M-D'], inplace=True)

        # 接着求臭氧的8小时最大值
        data3 = self.data
        data3['time'] = pd.to_datetime(data3['hour'])
        data3['time'] = data3['time'].apply(lambda x: x.hour + 1)
        data3['rname-Y-M-D'] = data3['rname'].map(str) + '-' + data3['year'].map(str) + '-' + data3['mon'].map(str) \
                               + '-' + data3['day'].map(str)
        # 求O3的8小时:求出8-24时的滑动平均值大小
        df = pd.DataFrame()
        for i in data['rname-Y-M-D'].unique():
            data5 = data[data['rname-Y-M-D'] == i]
            df1 = pd.DataFrame()
            for j in range(8, 25):
                data3 = data5[(data5['time'] <= j) & (data5['time'] >= j - 7)]
                df1.loc[i, j] = data3['o3'].mean()
            df = pd.concat([df, df1])
        lst = []
        # 判断小时数是否超过14
        for k in df.index:
            data4 = df.loc[k].dropna()
            lst1 = []
            for v in data4:
                lst1.append(v)
            if len(lst1) < 14:
                lst.append(1000000)  # 8小时小于14的先变为1000000，后面把当天的最大8小时值变为np.nan
            else:
                lst.append(0)
        df['amount'] = lst
        df['o3_8h'] = df.max(axis=1)  # 每行的最大值
        df = df.replace(1000000, np.nan)
        # print(data2) # 除了臭氧的
        data2 = pd.concat([df['o3_8h'], data2], axis=1)  # 合并臭氧和其他污染物
        # print(df)    # o3的
        # print(data2)  # 除了臭氧的
        df1 = pd.DataFrame()
        for i in data2['rname-year'].unique():
            df = data2[data2['rname-year'] == i]
            percent_98 = round(len(df) * 0.98) - 1
            percent_95 = round(len(df) * 0.95) - 1
            percent_90 = round(len(df) * 0.90) - 1
            so2 = df.sort_values(by=['so2'])  # 按照so2从小到大排序
            so2_98 = so2.iloc[percent_98]['so2']  # 找到so2在98%分位的数字
            no2 = df.sort_values(by=['no2'])
            no2_98 = no2.iloc[percent_98]['no2']
            co = df.sort_values(by=['co'])
            co_95 = co.iloc[percent_95]['co']
            o3 = df.sort_values(by=['o3_8h'])
            o3_90 = o3.iloc[percent_90]['co']
            pm25 = df.sort_values(by=['pm25'])
            pm25_95 = pm25.iloc[percent_95]['pm25']
            pm10 = df.sort_values(by=['pm10'])
            pm10_95 = pm10.iloc[percent_95]['pm10']
            df1.loc[i, 'so2'] = so2_98  # 装进DataFrame里面
            df1.loc[i, 'no2'] = no2_98
            df1.loc[i, 'co'] = co_95
            df1.loc[i, 'pm25'] = pm25_95
            df1.loc[i, 'pm10'] = pm10_95
            df1.loc[i, 'o3_8h'] = o3_90
        df1['so2'] = round(df1['so2'] / 150, 2)
        df1['no2'] = round(df1['no2'] / 80, 2)
        df1['co'] = round(df1['so2'] / 4, 2)
        df1['pm10'] = round(df1['so2'] / 150, 2)
        df1['pm25'] = round(df1['so2'] / 75, 2)
        df1['o3_8h'] = round(df1['o3_8h'] / 160, 2)
        df1['rname-year'] = df1.index
        # 比较两者的大小,先联合data1和df1
        data3 = pd.concat([data1, df1]).replace(np.nan, 0)
        data4 = data3.groupby('rname-year').max()
        dict1 = {}
        data4 = data4.to_json()
        data4 = json.loads(data4)
        for i, j in data4.items():
            for k, v in j.items():
                dict1.update({i: round(v, 2)})
        self.cacheDict.update({"single_index": dict1})
        return dict1

    # 5、最大质量指数
    def max_quality_index(self):
        list = []
        a = self.cacheDict.get("single_index")
        for k, v in a.items():
            v = float(v)
            list.append(v)
        list.sort()
        b = list[-1]
        self.cacheDict.update({"max_quality_index": b})
        return b

    # 6、综合质量指数
    def sum_quality_index(self):
        a = self.cacheDict.get("single_index")
        sum1 = 0
        for i, j in a.items():
            sum1 += j
        sum1 = round(sum1, 2)
        self.cacheDict.update({"sum_quality_index": sum1})
        return sum1

    # 7、计算超标污染物，分指数大于100
    def beyond_pollute(self):
        a = self.cacheDict.get("pollute_fzs")
        lst = []
        for i, j in a.items():
            if j > 100:
                lst.append(i)
        self.cacheDict.update({"beyond_pollute": lst})
        return lst

    # 8、超标倍数
    def hazard_multiple(self):
        data1 = self.data
        data1['so2'] = round(data1['so2'] / 60, 1)
        data1['no2'] = round(data1['no2'] / 40, 1)
        data1['co'] = round(data1['co'] / 4, 1)
        data1['o3'] = round(data1['o3'] / 160, 1)
        data1['pm10'] = round(data1['pm10'] / 70, 1)
        data1['pm25'] = round(data1['pm25'] / 35, 1)
        data1 = data1[['so2', 'no2', 'co', 'o3', 'pm10', 'pm25']]
        self.cacheDict.update({"hazrad_multiple": data1})
        data1 = data1.to_json()
        data1 = json.loads(data1)
        return data1

    # 9、点位小时评价污染物平均值
    def point_hour_mean(self):
        df = pd.DataFrame()
        data = self.data
        data['hour'] = pd.to_datetime(data['hour'])
        data['hour'] = data['hour'].apply(lambda x: x.hour + 1)
        for i in ['so2', 'co', 'no2', 'o3', 'pm10', 'pm25']:
            data1 = data[[i, 'rname', 'year', 'mon', 'day', 'hour']].groupby(
                ['year', 'mon', 'day', 'hour', 'rname']).mean()
            df = pd.concat([df, data1], axis=1)
        lst4 = []
        for i in df.index:
            lst4.append(i[3])
        df['hour'] = lst4
        for i in ['so2', 'pm10', 'pm25', 'no2', 'o3']:
            df[i] = np.round(df[i], 0)
        df['co'] = np.round(df[i], 1)
        self.cacheDict.update({"point_hour_mean": df})
        df = df.to_json()
        df = json.loads(df)
        return df

    # 10、点位臭氧最大8小时平均
    def point_o3_8h(self):
        data = self.data
        data['time'] = pd.to_datetime(data['hour'])
        data['time'] = data['time'].apply(lambda x: x.hour + 1)
        data['rname-Y-M-D'] = data['rname'].map(str) + '-' + data['year'].map(str) + '-' + data['mon'].map(str) \
                              + '-' + data['day'].map(str)
        # 求O3的8小时:求出8-24时的滑动平均值大小
        df = pd.DataFrame()
        for i in data['rname-Y-M-D'].unique():
            data2 = data[data['rname-Y-M-D'] == i]
            df1 = pd.DataFrame()
            for j in range(8, 25):
                data3 = data2[(data2['time'] <= j) & (data2['time'] >= j - 7)]
                if len(data3) == 8:
                    df1.loc[i, j] = data3['o3'].mean()
                else:
                    df1.loc[i, j] = np.nan
            df = pd.concat([df, df1])
        lst = []
        # 判断小时数是否超过14
        for k in df.index:
            data4 = df.loc[k].dropna()
            lst1 = []
            for v in data4:
                lst1.append(v)
            if len(lst1) < 14:
                lst.append(1000000)  # 8小时小于14的先变为1000000，后面把当天的最大8小时值变为np.nan
            else:
                lst.append(0)
        df['amount'] = lst
        df['o3_8h'] = df.max(axis=1)  # 每行的最大值
        df = df.replace(1000000, np.nan)
        self.cacheDict.update({"point_o3_8h": df})
        data = df['o3_8h'].to_json()
        data = json.loads(data)
        return data

    # 10、点位日评价污染物平均值
    def point_day_mean(self):
        data = self.data
        data['time'] = pd.to_datetime(data['hour'])
        data['hour'] = data['time'].apply(lambda x: x.hour + 1)
        data1 = data.groupby(['rname', 'year', 'mon', 'day', 'hour']).mean()[['so2', 'no2', 'co', 'pm10', 'pm25', 'o3']]
        rname = []
        year = []
        mon = []
        day = []
        for i in data1.index:
            rname.append(i[0])
            year.append(i[1])
            mon.append(i[2])
            day.append(i[3])
        data1['rname1'] = rname
        data1['year1'] = year
        data1['mon1'] = mon
        data1['day1'] = day
        data1 = data1.groupby(['rname1', 'year1', 'mon1', 'day1']).mean()
        year1 = []
        mon1 = []
        rname1 = []
        for i in data1.index:
            rname1.append(i[0])
            year1.append(i[1])
            mon1.append(i[2])
        data1['year'] = year1
        data1['mon'] = mon1
        data1['rname'] = rname1
        for i in ['so2', 'pm10', 'pm25', 'no2', 'o3']:
            data1[i] = np.round(data1[i], 0)
        data1['co'] = np.round(data1[i], 1)
        self.cacheDict.update({"point_day_mean": data1})
        data1 = data1.to_json()
        data1 = json.loads(data1)
        return data1

    # 11、点位年度污染物平均值
    def point_year_mean(self):
        df = self.data.groupby(['rname', 'year', 'mon', 'day']).mean()[['so2', 'no2', 'pm10', 'pm25', 'o3', 'co']]
        rname = []
        year = []
        for i in df.index:
            rname.append(i[0])
            year.append(i[1])
        df['year1'] = year
        df['rname1'] = rname
        df1 = df.groupby(['rname1', 'year1']).mean()
        for i in ['so2', 'pm10', 'pm25', 'no2', 'o3']:
            df1[i] = np.round(df1[i], 0)
        df1['co'] = np.round(df1[i], 1)
        self.cacheDict.update({"point_year_mean": df1})
        df1 = df1.to_json()
        df1 = json.loads(df1)
        return df1

    # 9、城市小时评价污染物平均值
    def city_hour_mean(self):
        df = pd.DataFrame()
        data = self.data
        data['hour'] = pd.to_datetime(data['hour'])
        data['hour'] = data['hour'].apply(lambda x: x.hour + 1)
        for i in ['so2', 'co', 'no2', 'o3', 'pm10', 'pm25']:
            data1 = data[[i, 'city', 'year', 'mon', 'day', 'hour']].groupby(
                ['year', 'mon', 'day', 'hour', 'city']).mean()
            df = pd.concat([df, data1], axis=1)
        lst4 = []
        for i in df.index:
            lst4.append(i[3])
        df['hour'] = lst4
        for i in ['so2', 'pm10', 'pm25', 'no2', 'o3']:
            df[i] = np.round(df[i], 0)
        df['co'] = np.round(df[i], 1)
        self.cacheDict.update({"city_hour_mean": df})
        df = df.to_json()
        df = json.loads(df)
        return df

    # 10、城市日评价污染物平均值
    def city_day_mean(self):
        data = self.data
        data['time'] = pd.to_datetime(data['hour'])
        data['time'] = data['time'].apply(lambda x: x.hour + 1)
        data['city-Y-M-D'] = data['city'].map(str) + '-' + data['year'].map(str) + '-' + data['mon'].map(str) \
                             + '-' + data['day'].map(str)
        data1 = data.groupby(['city-Y-M-D']).mean()[['so2', 'no2', 'co', 'pm10', 'pm25']]
        # 求O3的8小时:求出8-24时的滑动平均值大小
        df = pd.DataFrame()
        for i in data['city-Y-M-D'].unique():
            data2 = data[data['city-Y-M-D'] == i]
            df1 = pd.DataFrame()
            for j in range(8, 25):
                data3 = data2[(data2['time'] <= j) & (data2['time'] >= j - 7)]
                if len(data3) == 8:
                    df1.loc[i, j] = data3['o3'].mean()
                else:
                    df1.loc[i, j] = np.nan
            df = pd.concat([df, df1])
        lst = []
        # 判断小时数是否超过14
        for k in df.index:
            data4 = df.loc[k].dropna()
            lst1 = []
            for v in data4:
                lst1.append(v)
            if len(lst1) < 14:
                lst.append(1000000)  # 8小时数量小于14的先变为1000000，后面把当天的最大8小时值变为np.nan
            else:
                lst.append(0)  # 8小时的数量超过14的变为0，这样不会影响到取臭氧日最大值
        df['amount'] = lst
        df['o3_8h'] = df.max(axis=1)  # 每行的最大值
        df = df.replace(1000000, np.nan)
        # 合并O3最大8小时平均和其他污染物的日平均值
        df = pd.concat([df[['o3_8h']], data1], axis=1)
        for i in ['so2', 'pm10', 'pm25', 'no2', 'o3_8h']:
            df[i] = np.round(df[i], 0)
        df['co'] = np.round(df['co'], 1)
        self.cacheDict.update({"city_day_mean": df})
        data = df.to_json()
        data = json.loads(data)
        return data

    # 11、城市年度污染物平均值:先比较日平均值的每个月天数
    def city_year_mean(self):
        df = self.data.groupby(['city', 'year', 'mon', 'day']).mean()[['so2', 'no2', 'pm10', 'pm25', 'o3', 'co']]
        rname = []
        year = []
        for i in df.index:
            rname.append(i[0])
            year.append(i[1])
        df['year1'] = year
        df['city1'] = rname
        df1 = df.groupby(['city1', 'year1']).mean()
        city1 = []
        year1 = []
        for i in df1.index:
            city1.append(i[0])
            year1.append(i[1])
        df1['year2'] = year1
        df1['city2'] = city1
        df1.index = df1.year2
        df1 = df1.drop(columns=['city2', 'year2'])
        for i in ['so2', 'pm10', 'pm25', 'no2', 'o3']:
            df1[i] = np.round(df1[i], 0)
        df1['co'] = np.round(df1[i], 1)
        self.cacheDict.update({"city_year_mean": df1})
        df1 = df1.to_json()
        df1 = json.loads(df1)
        return df1

    # 12、日历年内百分位数求解:看每个月和每年的天数，不符合规定天数的为空值，设置为-100000，合并年月规定天数未一个DataFrame
    # 求每年规定的百分位数，然后将百分位数与年月的DataFrame合并，空值设为-1000000，合并两个DataFrame求平均值
    def city_year_percent(self):
        data = pd.DataFrame()
        for i in ['so2', 'co', 'pm10', 'pm25', 'no2', 'o3']:
            data1 = self.data[[i, 'year', 'mon', 'city']].groupby(['year', 'mon', 'city']).count()
            data = pd.concat([data, data1], axis=1)
        year = []
        mon = []
        city = []
        for i in data.index:
            year.append(i[0])
            mon.append(i[1])
            city.append(i[2])
        data['year'] = year
        data['mon'] = mon
        data['city'] = city
        # 下面计算每个月天数小于25和27的情况
        data2 = data[data.mon == 2][['so2', 'no2', 'co', 'pm10', 'pm25', 'o3']]
        data2 = data2[data2 >= 25]
        data3 = data[data.mon != 2][['so2', 'no2', 'co', 'pm10', 'pm25', 'o3']]
        data3 = data3[data3 >= 27]
        df = pd.concat([data2, data3])  # 每个月份小于25或27的都变为np.nan
        # 下面提取data7的年月
        year1 = []
        mon1 = []
        city1 = []
        for i in df.index:
            year1.append(i[0])
            mon1.append(i[1])
            city1.append(i[2])
        df['year1'] = year1
        df['mon1'] = mon1
        df['city1'] = city1
        df.index = df.index.droplevel()  # 去掉列名
        df = df.sort_values(['year1', 'mon1', 'city1']).replace(np.nan, -1000000)  # 排序后将空值转为-100000，方便后面计算转化
        df = df.groupby(['city1', 'year1']).mean()  # 求出每年的平均值
        df = df[df > 0][['so2', 'no2', 'pm10', 'pm25', 'co', 'o3']]  # 将小于0的转为空值，空值代表天数不合要求
        # 接下来就每年小于324天的
        df1 = self.data[['so2', 'co', 'pm10', 'pm25', 'no2', 'o3', 'year', 'city']].groupby(['city', 'year']).count()
        df1 = df1[df1 >= 324]
        df2 = pd.concat([df, df1])  # 合并年月的DataFrame
        df2 = df2.replace(np.nan, -10000000)
        city2 = []
        year2 = []
        for i in df2.index:
            city2.append(i[0])
            year2.append(i[1])
        df2['year'] = year2
        df2['city'] = city2
        df3 = df2.groupby(['city', 'year']).mean()
        df3 = df3[df3 > 0]
        year3 = []
        city3 = []
        for i in df3.index:
            city3.append(i[0])
            year3.append(i[1])
        df3['city'] = city3
        df3['year'] = year3
        df3['city-year'] = df3['city'].map(str) + '.' + df3['year'].map(str)
        df3.drop(columns=['city', 'year'], inplace=True)
        # 下面求日平均值:先求pm10、pm2.5、co、so2、no2的，再求o3的日最大8小时平均值
        # 先求除了o3的平均值
        data4 = self.data.groupby(['city', 'year', 'mon', 'day']).mean()
        city3 = []
        year3 = []
        for i in data4.index:
            city3.append(i[0])
            year3.append(i[1])
        data4['year1'] = year3
        data4['city1'] = city3
        data4['city-year'] = data4['city1'].map(str) + '.' + data4['year1'].map(str)
        data4.drop(columns=['year1', 'city1'], inplace=True)
        data4.index = data4['city-year']
        # 求o3的日最大8小时
        data5 = self.data
        data5['time'] = pd.to_datetime(data5['hour'])
        data5['time'] = data5['time'].apply(lambda x: x.hour + 1)
        data5['city-Y-M-D'] = data5['city'].map(str) + '-' + data5['year'].map(str) + '-' + data5['mon'].map(str) \
                              + '-' + data5['day'].map(str)
        df6 = pd.DataFrame()
        for i in data5['city-Y-M-D'].unique():
            data2 = data5[data5['city-Y-M-D'] == i]
            df7 = pd.DataFrame()
            for j in range(8, 25):
                data3 = data2[(data2['time'] <= j) & (data2['time'] >= j - 7)]
                if len(data3) == 8:
                    df7.loc[i, j] = data3['o3'].mean()
                else:
                    df7.loc[i, j] = np.nan
            df6 = pd.concat([df6, df7])
        lst = []
        # 判断小时数是否超过14
        for k in df6.index:
            data7 = df6.loc[k].dropna()
            lst1 = []
            for v in data7:
                lst1.append(v)
            if len(lst1) < 14:
                lst.append(1000000)  # 8小时小于14的先变为1000000，后面把当天的最大8小时值变为np.nan
            else:
                lst.append(0)
        df6['amount'] = lst
        df6['o3_8h'] = df6.max(axis=1)  # 每行的最大值
        df6 = df6.replace(1000000, np.nan)
        city4 = []
        year4 = []
        # print(df6)
        for i in df6.index:
            if i[2] == '-':
                city4.append(i[0:2])
                year4.append(i[3:7])
            elif i[3] == '-':
                city4.append(i[0:3])
                year4.append(i[4:8])
            elif i[4] == '-':
                city4.append(i[0:4])
                year4.append(i[5:9])
        df6['year1'] = year4
        df6['city1'] = city4
        df6['city-year'] = df6['city1'].map(str) + '.' + df6['year1'].map(str)
        df6.index = df6['city-year']
        # 合并各污染物的平均
        df6 = df6.reset_index(drop=True)
        data4 = data4.reset_index(drop=True)
        data4 = pd.concat([df6['o3_8h'], data4], axis=1)
        data4.index = range(len(data4))
        # 求各污染物在各地的年百分位数
        df4 = pd.DataFrame()
        for i in data4['city-year'].unique():
            data5 = data4[data4['city-year'] == i]
            percent_98 = round(len(data5) * 0.98) - 1  # 98分位的位置
            percent_95 = round(len(data5) * 0.95) - 1  # 95分位的位置
            percent_90 = round(len(data5) * 0.90) - 1  # 90分位的位置
            so2 = data5.sort_values(by=['so2'])  # 按照so2从小到大排序
            so2_98 = so2.iloc[percent_98]['so2']  # 找到so2在98%分位的数字
            no2 = data5.sort_values(by=['no2'])
            no2_98 = no2.iloc[percent_98]['no2']
            co = data5.sort_values(by=['co'])
            co_95 = co.iloc[percent_95]['co']
            pm25 = data5.sort_values(by=['pm25'])
            pm25_95 = pm25.iloc[percent_95]['pm25']
            pm10 = data5.sort_values(by=['pm10'])
            pm10_95 = pm10.iloc[percent_95]['pm10']
            o3_90 = data5.sort_values(by=['o3_8h'])
            o3_90 = o3_90.iloc[percent_90]['o3_8h']
            df4.loc[i, 'so2'] = so2_98  # 装进DataFrame里面
            df4.loc[i, 'no2'] = no2_98
            df4.loc[i, 'co'] = co_95
            df4.loc[i, 'pm25'] = pm25_95
            df4.loc[i, 'pm10'] = pm10_95
            df4.loc[i, 'o3'] = o3_90
        df4['city-year'] = df4.index
        df5 = pd.concat([df3, df4]).replace(np.nan, -10000000)
        df5 = df5.groupby(['city-year']).min()
        df5 = df5[df5 > 0]
        for i in ['so2', 'pm10', 'pm25', 'no2', 'o3']:
            df5[i] = np.round(df5[i], 0)
        df5['co'] = np.round(df5[i], 1)
        lst = []
        for i in df5.index:
            lst.append(i[-4:])
        df5.index = lst
        self.cacheDict.update({"city_year_percent": df5})
        df5 = df5.to_json()
        df5 = json.loads(df5)
        return df5

    # 13、小时达标率
    def non_exceed_percent_hour(self):
        data = self.data
        data['time'] = pd.to_datetime(data['hour'])
        data['time'] = data['time'].apply(lambda x: x.hour + 1)
        data1 = data.groupby(['rname', 'year', 'mon', 'day', 'time']).mean()
        # 求各污染物达标的情况
        data1_so2 = data1['so2']
        data1_so2 = data1_so2[data1_so2 <= 60]
        data1_no2 = data1['no2']
        data1_no2 = data1_no2[data1_no2 <= 40]
        data1_pm25 = data1['pm25']
        data1_pm25 = data1_pm25[data1_pm25 <= 35]
        data1_pm10 = data1['pm10']
        data1_pm10 = data1_pm10[data1_pm10 <= 35]
        data1_co = data1['co']
        data1_co = data1_co[data1_co <= 4]
        data1_o3 = data1['o3']
        data1_o3 = data1_o3[data1_o3 <= 4]
        data2 = pd.concat([data1_so2, data1_co, data1_no2, data1_o3, data1_pm10, data1_pm25], axis=1)
        # 求每天的时刻数
        rname = []
        year = []
        mon = []
        day = []
        for i in data2.index:
            rname.append(i[0])
            year.append(i[1])
            mon.append(i[2])
            day.append(i[3])
        data2['rname1'] = rname
        data2['year1'] = year
        data2['mon1'] = mon
        data2['day1'] = day
        # 计算每天达标的监测数量
        data3 = data2.groupby(['rname1', 'year1', 'mon1', 'day1']).count()
        # 计算每天的监测数量
        data4 = data.groupby(['rname', 'year', 'mon', 'day']).count()[['so2', 'no2', 'pm10', 'pm25', 'co', 'o3']]
        # 求达标率
        df = pd.DataFrame(index=data4.index)
        for i in data4.index:
            for j in data4.columns:
                df.loc[i, j] = data3.loc[i, j] / data4.loc[i, j]
        df = df.applymap(lambda x: '%.1f%%' % (x * 100))
        rname1 = []
        year1 = []
        mon1 = []
        day1 = []
        # 转换下index
        for i in df.index:
            rname1.append(i[0])
            year1.append(i[1])
            mon1.append(i[2])
            day1.append(i[3])
        df['rname1'] = rname1
        df['year1'] = year1
        df['mon1'] = mon1
        df['day1'] = day1
        df['time'] = df['rname1'].map(str) + '.' + df['year1'].map(str) + '.' + df['mon1'].map(str) \
                     + '.' + df['day1'].map(str)
        df.set_index(["time"], inplace=True)
        df = df.drop(columns=['rname1', 'mon1', 'year1', 'day1'])
        self.cacheDict.update({"non_exceed_percent_hour": df})
        df = df.to_json()
        df = json.loads(df)
        return df

    # 14、日达标率
    def non_exceed_percent_day(self):
        data = self.data
        data1 = data.groupby(['rname', 'year', 'mon', 'day']).mean()
        # 求各污染物达标的情况
        data1_so2 = data1['so2']
        data1_so2 = data1_so2[data1_so2 <= 60]
        data1_no2 = data1['no2']
        data1_no2 = data1_no2[data1_no2 <= 40]
        data1_pm25 = data1['pm25']
        data1_pm25 = data1_pm25[data1_pm25 <= 35]
        data1_pm10 = data1['pm10']
        data1_pm10 = data1_pm10[data1_pm10 <= 35]
        data1_co = data1['co']
        data1_co = data1_co[data1_co <= 4]
        data1_o3 = data1['o3']
        data1_o3 = data1_o3[data1_o3 <= 4]
        data2 = pd.concat([data1_so2, data1_co, data1_no2, data1_o3, data1_pm10, data1_pm25], axis=1)
        # 求每年的天数
        rname = []
        year = []
        for i in data2.index:
            rname.append(i[0])
            year.append(i[1])
        data2['rname1'] = rname
        data2['year1'] = year
        # 计算每年达标的监测数量
        data3 = data2.groupby(['rname1', 'year1']).count()
        # 计算每年的监测数量
        data4 = data.groupby(['rname', 'year']).count()[['so2', 'no2', 'pm10', 'pm25', 'co', 'o3']]
        # 求达标率
        df = pd.DataFrame(index=data4.index)
        for i in data4.index:
            for j in data4.columns:
                df.loc[i, j] = data3.loc[i, j] / data4.loc[i, j]
        rname1 = []
        year1 = []
        # 转换下index
        for i in df.index:
            rname1.append(i[0])
            year1.append(i[1])
        df['rname1'] = rname1
        df['year1'] = year1
        df['time'] = df['rname1'].map(str) + '.' + df['year1'].map(str)
        df.set_index(["time"], inplace=True)
        df = df.drop(columns=['rname1', 'year1'])
        df = df.applymap(lambda x: '%.1f%%' % (x * 100))
        self.cacheDict.update({"non_exceed_percent_day": df})
        df = df.to_json()
        df = json.loads(df)
        return df

    # 15、斯皮尔曼相关系数
    def speraman(self):
        dict1 = {}
        data = self.data[['so2', 'no2', 'co', 'pm25', 'pm10', 'o3', 'year', 'mon']]
        lst = []
        lst1 = []
        for i in data.year.unique():
            lst.append(i)
        for i in data.mon.unique():
            lst1.append(i)

        # 年为周期判断
        if len(lst) > 4:
            for i in ['so2', 'no2', 'co', 'pm25', 'pm10', 'o3', 'year']:
                data[i] = data[i].rank(method="min")  # 排名
            for i in ['so2', 'no2', 'co', 'pm25', 'pm10', 'o3']:
                sum1 = 0
                for j in range(len(data)):
                    a = (data.loc[j][i] - data.loc[j]['year']) * (data.loc[j][i] - data.loc[j]['year'])
                    sum1 += a
                rs = round(1 - 6 / (len(lst) * (len(lst) ** 2 - 1)) * sum1, 2)
                dict1.update({i: rs})

        # 月为周期
        elif len(lst1) > 4:
            for i in ['so2', 'no2', 'co', 'pm25', 'pm10', 'o3', 'mon']:
                data[i] = data[i].rank(method="min")
            for i in ['so2', 'no2', 'co', 'pm25', 'pm10', 'o3']:
                sum1 = 0
                for j in range(len(data)):
                    a = (data.loc[j][i] - data.loc[j]['mon']) * (data.loc[j][i] - data.loc[j]['mon'])
                    sum1 += a
                rs = round(1 - 6 / (len(lst1) * (len(lst1) ** 2 - 1)) * sum1, 2)
                dict1.update({i: rs})
        else:
            dict1.update({'spearman': []})
        return dict1
