import csv
import numpy as np
import pandas as pd
# combine data from 4 files
r1 = pd.read_csv("data_set/o_datasets/UHC.csv", usecols=["Country Name", "2017"])  # 文件1
r2 = pd.read_csv("data_set/o_datasets/HE_GDP.csv", usecols=["Country Name", "2018"])  # 文件2
r3 = pd.read_csv("data_set/o_datasets/GDP_per_capita.csv", usecols=["Country Name", "2019"])
r4 = pd.read_csv("data_set/o_datasets/Population_data.csv",usecols=["Country Name", "Populaition(2021)"])


r5 = pd.merge(r1, r2, on="Country Name")
r6 = pd.merge(r5, r3, on="Country Name")
r7 = pd.merge(r6, r4, on="Country Name")
df = r7.dropna(axis = 0, how = 'any')
df.to_csv("data_set/p_datasets/combined.csv",float_format="%.3f")


def cal_rank(rows,row,num):
    if np.double(row) < np.double(num[0.25]):
        rows.append(0)
    elif np.double(row) < np.double(num[0.5]):
        rows.append(1)
    elif np.double(row) < np.double(num[0.75]):
        rows.append(2)
    else:
        rows.append(3)
  # 文件1

uhc = df["2017"].quantile([0.25, 0.5, 0.75])
he_gdp = df["2018"].quantile([0.25, 0.5, 0.75])
gdp_per = df["2019"].quantile([0.25, 0.5, 0.75])

input_file = "data_set/p_datasets/combined.csv"
output_file = "data_set/p_datasets/whh.csv"

with open(input_file, "r", newline="") as csv_in_file:
    with open(output_file, "w", newline="") as csv_out_file:
        filereader = csv.reader(
            csv_in_file,
        )
        filewriter = csv.writer(csv_out_file)
        header = next(filereader)
        head = [
            "",
            "Country Name",
            "UHC",
            "HE_GDP",
            "GDP_per_captia",
            "Population",
            "UHC_rank",
            "HE_GDP_rank",
            "GDP_per_captia1_rank",
            "development index",
            "ln(population)",
        ]
        filewriter.writerow(head)
        for row_list in filereader:
            cal_rank(row_list, row_list[2], uhc)
            cal_rank(row_list, row_list[3], he_gdp)
            cal_rank(row_list, row_list[4], gdp_per)
            row_list.append(row_list[6] + row_list[7] + row_list[8])
            l = round(np.log(float(row_list[5]) / 100000), 4)
            # print(l)
            row_list.append(l)

            filewriter.writerow(row_list)
