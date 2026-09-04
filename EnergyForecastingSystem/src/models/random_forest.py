"""
Random Forest Model
===================
Multivariate decision tree ensemble for energy demand forecasting.
"""

import joblib
from sklearn.ensemble import RandomForestRegressor

class RandomForestModel:
    def __init__(self, n_estimators=100, max_depth=15, random_state=42):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
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
