import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load Dataset
df = pd.read_csv("../data/AEP_hourly.csv")

# Convert Datetime
df["Datetime"] = pd.to_datetime(df["Datetime"])

# Set Index
df.set_index("Datetime", inplace=True)

# Sort Data
df.sort_index(inplace=True)

# Time Features
df["Hour"] = df.index.hour
df["Day"] = df.index.day
df["Month"] = df.index.month
df["DayOfWeek"] = df.index.dayofweek

# Lag Features
df["Lag_1"] = df["AEP_MW"].shift(1)
df["Lag_24"] = df["AEP_MW"].shift(24)

# Remove Missing Values
df.dropna(inplace=True)

# Features
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

# Target
y = df["AEP_MW"]

# Time Series Split
split_index = int(len(df) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

# Model
# NOTE: n_estimators/max_depth are intentionally constrained (rather than
# the default unlimited depth) so the saved .pkl file stays a reasonable
# size to ship/commit, while still keeping R2 above 0.99.
model = RandomForestRegressor(
    n_estimators=80,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

# Training
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, predictions)

r2 = r2_score(y_test, predictions)

print("MAE:", round(mae, 2))
print("R2:", round(r2, 4))

# Save Model (compressed to keep the file small)
joblib.dump(model, "../models/random_forest.pkl", compress=3)

print("Model Saved Successfully")