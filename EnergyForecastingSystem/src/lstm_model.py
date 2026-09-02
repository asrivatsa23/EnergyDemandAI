import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# =========================
# Load Dataset
# =========================

df = pd.read_csv("../data/AEP_hourly.csv")

df["Datetime"] = pd.to_datetime(df["Datetime"])

df.set_index("Datetime", inplace=True)

df.sort_index(inplace=True)

# =========================
# Select Target Column
# =========================

data = df[["AEP_MW"]]

# =========================
# Scale Data
# =========================

scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(data)

# =========================
# Create Sequences
# =========================

X = []
y = []

time_steps = 24

for i in range(time_steps, len(scaled_data)):

    X.append(
        scaled_data[i-time_steps:i]
    )

    y.append(
        scaled_data[i]
    )

X = np.array(X)

y = np.array(y)

print("X Shape:", X.shape)

print("y Shape:", y.shape)

# =========================
# Train Test Split
# =========================

split_index = int(len(X) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# =========================
# Build LSTM Model
# =========================

model = Sequential()

model.add(
    LSTM(
        units=50,
        input_shape=(
            X_train.shape[1],
            X_train.shape[2]
        )
    )
)

model.add(
    Dense(1)
)

# =========================
# Compile Model
# =========================

model.compile(
    optimizer="adam",
    loss="mse"
)

# =========================
# Train Model
# =========================

history = model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_data=(
        X_test,
        y_test
    ),
    verbose=1
)

# =========================
# Predictions
# =========================

predictions = model.predict(X_test)

# =========================
# Reverse Scaling
# =========================

predictions = scaler.inverse_transform(
    predictions
)

y_test_actual = scaler.inverse_transform(
    y_test
)

# =========================
# Evaluation
# =========================

mae = mean_absolute_error(
    y_test_actual,
    predictions
)

r2 = r2_score(
    y_test_actual,
    predictions
)

print("\nModel Performance")

print("MAE:", round(mae, 2))

print("R2:", round(r2, 4))

# Generate a plot to visualize the actual vs predicted values for the first 200 samples

plt.figure(figsize=(12,6))

plt.plot(
    y_test_actual[:200],
    label="Actual"
)

plt.plot(
    predictions[:200],
    label="Predicted"
)

plt.title(
    "LSTM Energy Forecasting"
)

plt.xlabel(
    "Time"
)

plt.ylabel(
    "Energy Consumption (MW)"
)

plt.legend()

plt.savefig(
    "../graphs/lstm_predictions.png"
)

plt.show()

# =========================
# Save Model
# =========================

# model.save(
#     "../models/lstm_model.h5"
# )

model.save(
    "../models/lstm_model.keras"
)

joblib.dump(
    scaler,
    "../models/lstm_scaler.pkl"
)

print("\nLSTM Model Saved Successfully")