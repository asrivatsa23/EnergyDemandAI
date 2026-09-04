"""
Multivariate LSTM Model
=======================
Deep learning sequence model supporting multivariate time-series input
for electricity demand forecasting.
"""

import os
import joblib
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import StandardScaler

class LSTMModel:
    def __init__(self, time_steps=24, n_features=1):
        self.time_steps = time_steps
        self.n_features = n_features
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.model = None

    def _build_model(self, input_shape):
        model = Sequential([
            LSTM(64, activation='relu', input_shape=input_shape, return_sequences=True),
            Dropout(0.2),
            LSTM(32, activation='relu'),
            Dropout(0.2),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def create_sequences(self, X_data, y_data):
        X_seq, y_seq = [], []
        for i in range(len(X_data) - self.time_steps):
            X_seq.append(X_data[i:i + self.time_steps])
            y_seq.append(y_data[i + self.time_steps])
        return np.array(X_seq), np.array(y_seq)

    def fit(self, X_train, y_train, epochs=10, batch_size=32):
        # Scale features and target
        X_scaled = self.scaler_X.fit_transform(X_train)
        y_scaled = self.scaler_y.fit_transform(y_train.values.reshape(-1, 1))

        self.n_features = X_scaled.shape[1]
        X_seq, y_seq = self.create_sequences(X_scaled, y_scaled)

        self.model = self._build_model((self.time_steps, self.n_features))
        self.model.fit(X_seq, y_seq, epochs=epochs, batch_size=batch_size, verbose=0)
        return self

    def predict(self, X):
        X_scaled = self.scaler_X.transform(X)
        X_seq, _ = self.create_sequences(X_scaled, np.zeros((len(X_scaled), 1)))
        if len(X_seq) == 0:
            return np.array([])
        preds_scaled = self.model.predict(X_seq, verbose=0)
        return self.scaler_y.inverse_transform(preds_scaled).flatten()

    def predict_sequence(self, sequence_window):
        """
        Given raw 24-step sequence window (24 x n_features), predict next step.
        """
        seq_scaled = self.scaler_X.transform(sequence_window)
        seq_reshaped = np.expand_dims(seq_scaled, axis=0)
        pred_scaled = self.model.predict(seq_reshaped, verbose=0)
        return float(self.scaler_y.inverse_transform(pred_scaled)[0, 0])

    def save(self, model_path, scalers_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        self.model.save(model_path)
        joblib.dump({"scaler_X": self.scaler_X, "scaler_y": self.scaler_y, "time_steps": self.time_steps}, scalers_path)

    @classmethod
    def load(cls, model_path, scalers_path):
        inst = cls()
        inst.model = load_model(model_path)
        scalers = joblib.load(scalers_path)
        inst.scaler_X = scalers["scaler_X"]
        inst.scaler_y = scalers["scaler_y"]
        inst.time_steps = scalers.get("time_steps", 24)
        return inst
