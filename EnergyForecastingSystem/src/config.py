"""
EnergyDemandAI - Configuration Settings
========================================
Centralized configuration parameters for data paths, features,
model hyperparameters, time-series splits, and Indian energy grid metadata.
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
SAMPLE_DATA_DIR = os.path.join(DATA_DIR, "sample")

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
GRAPHS_DIR = os.path.join(PROJECT_ROOT, "graphs")

# Default Sample Indian Dataset Path
SAMPLE_DATA_PATH = os.path.join(SAMPLE_DATA_DIR, "indian_electricity_sample.csv")

# Ensure required directories exist
for path in [
    RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATA_DIR,
    MODELS_DIR, RESULTS_DIR, GRAPHS_DIR
]:
    os.makedirs(path, exist_ok=True)

# Time Series Settings
TIME_STEPS = 24  # historical hours lookback
FORECAST_HORIZON_DEFAULT = 24  # hours ahead
RANDOM_STATE = 42

# Train / Validation / Test Chronological Split Ratios
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Core Target and Schema Definitions
TARGET_COLUMN = "Energy Required (MU)"
ALTERNATIVE_TARGET_COLUMNS = ["Energy Required (MU)", "Demand (MW)", "Peak Demand (MW)", "AEP_MW"]

DATETIME_COLUMNS = ["Datetime", "Date", "Timestamp", "datetime", "date", "timestamp"]
STATE_COLUMN = "State"
REGION_COLUMN = "Region"

# Weather & Renewable Features
WEATHER_COLUMNS = ["Temperature", "Humidity", "Rainfall"]
RENEWABLE_COLUMNS = ["Solar Generation", "Wind Generation", "Hydro Generation"]
HOLIDAY_COLUMNS = ["Holiday", "Festival"]

# Indian Power Grid Regions & States Mapping
INDIAN_REGIONS_STATES = {
    "Northern Region": ["Delhi", "Punjab", "Haryana", "Rajasthan", "Uttar Pradesh", "Himachal Pradesh", "Uttarakhand"],
    "Western Region": ["Maharashtra", "Gujarat", "Madhya Pradesh", "Chhattisgarh", "Goa"],
    "Southern Region": ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Telangana", "Kerala"],
    "Eastern Region": ["West Bengal", "Odisha", "Bihar", "Jharkhand"],
    "North-Eastern Region": ["Assam", "Meghalaya", "Tripura", "Nagaland", "Manipur"]
}

# Registered Models List
AVAILABLE_MODELS = [
    {"id": "linear_regression", "name": "Linear Regression", "type": "baseline"},
    {"id": "random_forest", "name": "Random Forest Regressor", "type": "tree"},
    {"id": "xgboost", "name": "XGBoost Regressor", "type": "tree"},
    {"id": "arima", "name": "ARIMA / SARIMA", "type": "statistical"},
    {"id": "lstm", "name": "Multivariate LSTM", "type": "deep_learning"},
    {"id": "hybrid_ensemble", "name": "Hybrid Ensemble", "type": "ensemble"}
]
