import pandas as pd

df = pd.read_csv("../data/AEP_hourly.csv")

# Convert to datetime
df["Datetime"] = pd.to_datetime(df["Datetime"])

print(df.head())

print("\nData Types:")
print(df.dtypes)

# Set Datetime as Index
df.set_index("Datetime", inplace=True)

print(df.head())

print("\nIndex Type:")
print(type(df.index))