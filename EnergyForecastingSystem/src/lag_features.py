import pandas as pd

df = pd.read_csv("../data/AEP_hourly.csv")

df["Datetime"] = pd.to_datetime(df["Datetime"])

df.set_index("Datetime", inplace=True)

# Time Features
df["Hour"] = df.index.hour
df["Day"] = df.index.day
df["Month"] = df.index.month
df["DayOfWeek"] = df.index.dayofweek

# Lag Features
df["Lag_1"] = df["AEP_MW"].shift(1)

df["Lag_24"] = df["AEP_MW"].shift(24)

print(df.head(30))