import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("csv/whh.csv", usecols=["development index", "ln(population)", "fit_index", "days"])

x = df[["development index", "ln(population)", "days"]]
y = df["fit_index"]

model = sm.OLS(y, x).fit()
print(model.summary())
# y_fitted = model.fittedvalues
