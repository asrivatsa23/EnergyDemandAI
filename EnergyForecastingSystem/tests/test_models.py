"""
Unit Tests - Forecasting Models Module
"""

import pytest
import numpy as np
import pandas as pd
from src.models.linear_regression import LinearRegressionModel
from src.models.random_forest import RandomForestModel
from src.models.xgboost import XGBoostModel

def test_linear_regression():
    X = pd.DataFrame({"Hour": [1, 2, 3, 4], "Day": [10, 10, 10, 10], "Month": [5, 5, 5, 5], "DayOfWeek": [0, 0, 0, 0]})
    y = pd.Series([100.0, 110.0, 120.0, 130.0])
    
    lr = LinearRegressionModel()
    lr.fit(X, y)
    preds = lr.predict(X)
    assert len(preds) == 4

def test_random_forest():
    X = pd.DataFrame({
        "Hour": np.random.randint(0, 24, 50),
        "Lag_1": np.random.uniform(100, 200, 50),
        "Lag_24": np.random.uniform(100, 200, 50)
    })
    y = pd.Series(np.random.uniform(100, 200, 50))

    rf = RandomForestModel(n_estimators=10)
    rf.fit(X, y)
    preds = rf.predict(X)
    assert len(preds) == 50

def test_xgboost():
    X = pd.DataFrame({
        "Hour": np.random.randint(0, 24, 50),
        "Lag_1": np.random.uniform(100, 200, 50),
        "Lag_24": np.random.uniform(100, 200, 50)
    })
    y = pd.Series(np.random.uniform(100, 200, 50))

    xgb = XGBoostModel(n_estimators=10)
    xgb.fit(X, y)
    preds = xgb.predict(X)
    assert len(preds) == 50
