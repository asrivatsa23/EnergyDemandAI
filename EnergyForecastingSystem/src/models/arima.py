"""
ARIMA / SARIMA Statistical Model
=================================
Statistical time-series forecasting model using statsmodels.
"""

import os
import joblib
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

class ARIMAModel:
    def __init__(self, order=(2, 1, 2)):
        self.order = order
        self.fitted_model = None
        self.last_series = None

    def fit(self, y_train):
        """Fit ARIMA model on training time series."""
        # Use last 1000 observations to keep training fast and responsive
        train_series = pd.Series(y_train).tail(1000).values
        model = ARIMA(train_series, order=self.order)
        self.fitted_model = model.fit()
        self.last_series = train_series
        return self

    def predict(self, steps=24):
        """Forecast future steps."""
        if self.fitted_model is None:
            raise ValueError("ARIMA model must be fitted first.")
        forecast = self.fitted_model.forecast(steps=steps)
        return np.array(forecast)

    def predict_instance(self, recent_history, steps=24):
        """Refits or forecasts on a recent time series snippet."""
        try:
            temp_model = ARIMA(recent_history, order=self.order)
            fitted = temp_model.fit()
            return np.array(fitted.forecast(steps=steps))
        except Exception:
            # Fallback naive mean forecast
            mean_val = np.mean(recent_history[-24:])
            return np.full(steps, mean_val)

    def save(self, filepath):
        joblib.dump({"order": self.order, "fitted_model": self.fitted_model, "last_series": self.last_series}, filepath)

    @classmethod
    def load(cls, filepath):
        inst = cls()
        data = joblib.load(filepath)
        inst.order = data.get("order", (2, 1, 2))
        inst.fitted_model = data.get("fitted_model")
        inst.last_series = data.get("last_series")
        return inst
