"""
XGBoost Model
=============
Gradient Boosted decision tree regressor for time-series forecasting.
"""

import joblib
from xgboost import XGBRegressor

class XGBoostModel:
    def __init__(self, n_estimators=150, max_depth=6, learning_rate=0.05, random_state=42):
        self.model = XGBRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            n_jobs=-1
        )

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
