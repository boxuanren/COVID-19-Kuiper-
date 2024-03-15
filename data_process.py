import pandas as pd
import kuiper
import numpy as np


# 加载csv文件
df = pd.read_csv("csv/owid-covid-data.csv", usecols=["location", "date","new_cases"])
# 将新增为空的数据设为0，转换数据类型
df.dropna(inplace=True)
df["new_cases"] = df["new_cases"].astype(int)
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")



# 取得国家
country = df.drop_duplicates(subset=["location"])
countries = country["location"].values.tolist()

lst = []
for i in countries:
    temp = df.loc[df["location"] == i]
    temp["MA"] = temp.iloc[:, 3].rolling(window=30).mean()
    cutoff = temp[temp["MA"] == temp["MA"].max()]
    cutoff = [cutoff["date"].values][0][0]
    temp = temp[(temp["date"] <= cutoff)]
    days = (temp["new_cases"] != 0).sum()
    tempConfirmAdd = temp["new_cases"].values.tolist()
    d = kuiper.benfordKuiper(tempConfirmAdd)
    statistic = [i, d, days, cutoff]
    lst.append(statistic)

statistics = pd.DataFrame(lst, columns=["Country Name", "fit_index", "days", "cutoffday"])
statistics.to_csv("csv/statistics.csv", float_format="%.3f")

df1 = pd.read_csv("csv/statistics.csv", usecols=["Country Name", "fit_index", "days"])
df2 = pd.read_csv("data_set/p_datasets/whh.csv",usecols=["Country Name", "development index", "ln(population)"],)

df3 = pd.merge(df2, df1, on="Country Name")
df3.to_csv("csv/full_data.csv")
