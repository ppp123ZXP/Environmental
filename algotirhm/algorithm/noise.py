import pandas as pd
import numpy as np
import math
import json

class NoiseCal(object):

    cacheDict = {}

    def __init__(self, data):
        self.data = data

    def showdata(self):  # 展示数据概况
        return self.data

    # 1、昼间等效声级
    def day_mean(self):
        data = self.data
        dict1 = {}
        data['Y-M-D'] = data['year'].map(str) + '.' + data['mon'].map(str) + '.' + data['day'].map(str)
        data1 = data[(data.hour >= 6) & (data.hour <= 22)]
        for i in data['Y-M-D'].unique():
            data2 = data1[data1['Y-M-D'] == i]
            for j in data2.city:
                data3 = data2[data2.city == j]
                sum1 = 0
                for k in data3.LEQ:
                    a = 10 ** (0.1 * k)
                    sum1 += a
                b = round(10 * math.log10(sum1 / len(data2)), 1)
                dict1.update({i: b})
        self.cacheDict.update({"day_mean":dict1})
        return dict1

    # 2、夜间等效声级
    def night_mean(self):
        data = self.data
        dict1 = {}
        data['Y-M-D'] = data['year'].map(str) + '.' + data['mon'].map(str) + '.' + data['day'].map(str)
        data1 = data[(data.hour < 6) | (data.hour > 22)]
        for i in data['Y-M-D'].unique():
            data2 = data1[data1['Y-M-D'] == i]
            for j in data2.city:
                data3 = data2[data2.city == j]
                sum1 = 0
                for k in data3.LEQ:
                    a = 10 ** (0.1 * k)
                    sum1 += a
                b = round(10 * math.log10(sum1 / len(data2)), 1)
                dict1.update({i: b})
        self.cacheDict.update({"night_mean": dict1})
        return dict1

    # 3、噪声平均水平
    def noise_mean(self):
        sum1 = 0
        for i in self.data['LEQ']:
            sum1 += i
        a = round(sum1 / len(self.data), 1)
        self.cacheDict.update({"noise_mean": a})
        return a

    # 4、百分位等效声级
    def percent(self):
        data = self.data
        dict1 = {}
        for i in data['city'].unique():
            data1 = data[data['city'] == i]
            lst = []
            for j in data1['LEQ']:
                lst.append(j)
            lst.sort()
            min1 = lst[0]
            max1 = lst[-1]
            length = len(lst)
            len10 = math.ceil(0.1 * length) - 1
            len50 = math.ceil(0.5 * length) - 1
            len90 = math.ceil(0.9 * length) - 1
            l10 = lst[len10]
            l50 = lst[len50]
            l90 = lst[len90]
            dict1.update({'min': min1})
            dict1.update({'max': max1})
            dict1.update({'l10': l10})
            dict1.update({'l50': l50})
            dict1.update({'l90': l90})
        return dict1