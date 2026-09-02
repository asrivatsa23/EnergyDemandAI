import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("../data/AEP_hourly.csv")

df["Datetime"] = pd.to_datetime(df["Datetime"])

df.set_index("Datetime", inplace=True)

df["Hour"] = df.index.hour
df["Day"] = df.index.day
df["Month"] = df.index.month
df["DayOfWeek"] = df.index.dayofweek

X = df[["Hour", "Day", "Month", "DayOfWeek"]]

y = df["AEP_MW"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Records:", len(X_train))

print("Testing Records:", len(X_test))