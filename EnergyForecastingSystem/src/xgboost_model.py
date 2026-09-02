import pandas as pd
import joblib

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)

#..... Load Dataset

df = pd.read_csv("../data/AEP_hourly.csv")

# Convert Datetime Column
df["Datetime"] = pd.to_datetime(df["Datetime"])

# Set Datetime as Index
df.set_index("Datetime", inplace=True)

# Sort Chronologically
df.sort_index(inplace=True)


#.... Feature Engineering


df["Hour"] = df.index.hour
df["Day"] = df.index.day
df["Month"] = df.index.month
df["DayOfWeek"] = df.index.dayofweek


#.... Lag Features


df["Lag_1"] = df["AEP_MW"].shift(1)

df["Lag_24"] = df["AEP_MW"].shift(24)

# Remove Missing Values
df.dropna(inplace=True)


#.... Input Features and Target


X = df[
    [
        "Hour",
        "Day",
        "Month",
        "DayOfWeek",
        "Lag_1",
        "Lag_24"
    ]
]

y = df["AEP_MW"]

#.... Time Series Split

split_index = int(len(df) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

print("Training Records:", len(X_train))
print("Testing Records:", len(X_test))

print("\nTrain Start:", X_train.index.min())
print("Train End:", X_train.index.max())

print("\nTest Start:", X_test.index.min())
print("Test End:", X_test.index.max())


#.... XGBoost Model


model = XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

# Train Model
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

#.... Evaluation


mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)

print("\nModel Performance")

print("MAE:", round(mae, 2))

print("R2:", round(r2, 4))

#.... Feature Importance

print("\nFeature Importance")

importance = model.feature_importances_

for feature, score in zip(X.columns, importance):
    print(
        feature,
        round(score, 4)
    )

#.... Save Model

joblib.dump(
    model,
    "../models/xgboost.pkl"
)

print("\nXGBoost Model Saved Successfully")