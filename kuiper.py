from numpy import copy, sort, amax, arange, exp, sqrt, abs, floor, searchsorted
import matplotlib.pyplot as plt
import pandas as pd


def countFrequnce(confirmAdd):
    """
    统计首位数字出现的频数

    输入: 新冠新增/确诊/死亡等数据列表
    返回：统计首位数字出现频数的字典
    """
    seq = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
    counterDic = dict.fromkeys(seq, 0)

    for i in map(str, confirmAdd):
        if i[0] == "1":
            counterDic["1"] += 1
        elif i[0] == "2":
            counterDic["2"] += 1
        elif i[0] == "3":
            counterDic["3"] += 1
        elif i[0] == "4":
            counterDic["4"] += 1
        elif i[0] == "5":
            counterDic["5"] += 1
        elif i[0] == "6":
            counterDic["6"] += 1
        elif i[0] == "7":
            counterDic["7"] += 1
        elif i[0] == "8":
            counterDic["8"] += 1
        elif i[0] == "9":
            counterDic["9"] += 1

    return counterDic


def sumOfList(lst, size):
    """
    计算列表中元素的和

    输入: 数据列表
    返回：列表中元素的和
    """
    if size == 0:
        return 0
    else:
        return lst[size - 1] + sumOfList(lst, size - 1)


def benfordKuiper(confirmAdd):
    """
    利用kuiper检验, 检验新冠数据是否服从benford分布

    输入: 新冠新增/确诊/死亡等数据列表
    返回: kuiper检验统计量V
    """
    # 统计首位数字出现的频数
    counterDic = countFrequnce(confirmAdd)
    # benford分布的概率分布函数
    benfordDistribute = [0.301, 0.177, 0.133, 0.106, 0.089, 0.077, 0.068, 0.061, 0.056]
    benfordCDF = [0.301, 0.477, 0.602, 0.699, 0.778, 0.845, 0.903, 0.954, 1]
    # 取出首位数字出现的频数
    frequency = list(counterDic.values())
    # 样本总数
    n = sumOfList(frequency, len(frequency))
    # 累积频数
    cumulativeFrequency = [
        frequency[0],
        sum(frequency[0:2]),
        sum(frequency[0:3]),
        sum(frequency[0:4]),
        sum(frequency[0:5]),
        sum(frequency[0:6]),
        sum(frequency[0:7]),
        sum(frequency[0:8]),
        sum(frequency[0:9]),
    ]
    # 累积频率
    cumulativeFrequency = [i / n for i in cumulativeFrequency]
    # 保留三位小数
    cumulativeFrequency = [round(i, 3) for i in cumulativeFrequency]
    # 频率
    frequency = [i / n for i in frequency]
    # 求H_d - P_d
    v1 = [i - j for i, j in zip(cumulativeFrequency, benfordCDF)]
    v2 = [i - j for i, j in zip(benfordCDF, cumulativeFrequency)]
    # 画理论分布与实际分布的CDF, 蓝色为实际分布, 红色为理论分布
    # paint(
    #     list(counterDic.keys()),
    #     frequency,
    #     benfordDistribute,
    #     "leading digit",
    #     "CDF",
    #     "Demo",
    # )
    # 求D^+
    D_plus = max(v1)
    # 求D^-
    D_minus = max(v2)
    # 求V
    V = (D_plus + D_minus) * (sqrt(n) + 0.155 + 0.24 / sqrt(n))

    return V


# 绘制折线图
def paint(x, y, y2, x_label, y_label, title):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.bar(x, y)
    plt.plot(x, y2, "ro")
    plt.show()


# d = pd.read_csv("csv/国内疫情时间序列.csv", usecols=["confirmedIncr", "deadIncr", "dateId"])
# confirmAdd = d["confirmedIncr"].values.tolist()
# print(benfordKuiper(confirmAdd))
# chn2 = pd.read_csv("csv/国内疫情时间序列.csv", usecols=["confirmedIncr", "dateId"])
# # chn2["dateID"] = pd.to_datetime(chn2["dateID"])
# print(chn2)
# CHNconfirmAdd2 = chn2["confirmedIncr"].values.tolist()
# print(CHNconfirmAdd2)
# print(benfordKuiper(CHNconfirmAdd2))

def D_static(confirmAdd):
    counterDic = countFrequnce(confirmAdd)
    # benford分布的概率分布函数
    benfordDistribute = [0.301, 0.177, 0.133, 0.106, 0.089, 0.077, 0.068, 0.061, 0.056]
    benfordCDF = [0.301, 0.477, 0.602, 0.699, 0.778, 0.845, 0.903, 0.954, 1]
    # 取出首位数字出现的频数
    frequency = list(counterDic.values())
    n = sumOfList(frequency, len(frequency))
    Frequency = [(i / n ) for i in frequency]

    # 样本总数
    sum=0
    for i in range(8):
        sum+=(Frequency[i]-benfordDistribute[i])**2
        return sqrt(sum)