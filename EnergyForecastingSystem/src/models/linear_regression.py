"""
Linear Regression Baseline Model
================================
Baseline model for electricity demand forecasting using time and engineered features.
"""

import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return self

    def predict(self, X):
        return self.model.predict(X)

    def save(self, filepath):
        joblib.dump(self.model, filepath)

    @classmethod
    def load(cls, filepath):
        inst = cls()
        inst.model = joblib.load(filepath)
        return inst
