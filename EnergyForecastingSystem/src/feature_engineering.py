import pandas as pd

df = pd.read_csv("../data/AEP_hourly.csv")

df["Datetime"] = pd.to_datetime(df["Datetime"])

df.set_index("Datetime", inplace=True)

# Feature Engineering
df["Hour"] = df.index.hour

df["Day"] = df.index.day

df["Month"] = df.index.month

df["DayOfWeek"] = df.index.dayofweek

print(df.head())

print(df.describe())