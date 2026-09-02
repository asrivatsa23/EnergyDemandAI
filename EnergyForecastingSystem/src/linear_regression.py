import pandas as pd
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# =========================
# Load Dataset
# =========================

df = pd.read_csv("../data/AEP_hourly.csv")

df["Datetime"] = pd.to_datetime(df["Datetime"])

df.set_index("Datetime", inplace=True)

df.sort_index(inplace=True)

# =========================
# Feature Engineering
# =========================
# NOTE: Linear Regression only uses time-of-day features (no lag values),
# so it serves as the simplest baseline model.

df["Hour"] = df.index.hour
df["Day"] = df.index.day
df["Month"] = df.index.month
df["DayOfWeek"] = df.index.dayofweek

X = df[["Hour", "Day", "Month", "DayOfWeek"]]

y = df["AEP_MW"]

# =========================
# Time Series Split
# =========================
# A chronological split (rather than a random shuffle) is used so this
# model is evaluated the same way as Random Forest / XGBoost / LSTM:
# trained on the past, tested on the future.

split_index = int(len(X) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

# =========================
# Train Model
# =========================

model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

# =========================
# Evaluation
# =========================

mae = mean_absolute_error(y_test, predictions)

r2 = r2_score(y_test, predictions)

print("\nActual vs Predicted")

for i in range(5):
    print(
        "Actual:", y_test.iloc[i],
        "Predicted:", round(predictions[i], 2)
    )

print("\nModel Performance")
print("Mean Absolute Error:", round(mae, 2))
print("R2 Score:", round(r2, 4))

# =========================
# Save Model
# =========================

joblib.dump(model, "../models/linear_regression.pkl")

print("\nLinear Regression Model Saved Successfully")
