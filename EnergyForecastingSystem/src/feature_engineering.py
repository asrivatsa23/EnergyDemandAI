"""
EnergyDemandAI - Feature Engineering Module
============================================
Generates temporal, cyclic, lag, rolling, weather, and renewable features
for time-series electricity demand forecasting models.
"""

import numpy as np
import pandas as pd
from src.config import TARGET_COLUMN, WEATHER_COLUMNS, RENEWABLE_COLUMNS, HOLIDAY_COLUMNS

def create_features(df, target_col=TARGET_COLUMN, include_lags=True, drop_na=True):
    """
    Applies comprehensive feature engineering pipeline on a preprocessed DataFrame.
    """
    df = df.copy()

    if "Datetime" not in df.columns:
        raise ValueError("DataFrame must contain a 'Datetime' column for feature engineering.")

    dt = df["Datetime"].dt

    # 1. Calendar & Time Features
    df["Hour"] = dt.hour
    df["Day"] = dt.day
    df["DayOfWeek"] = dt.dayofweek
    df["DayOfMonth"] = dt.day
    df["WeekOfYear"] = dt.isocalendar().week.astype(int)
    df["Month"] = dt.month
    df["Quarter"] = dt.quarter
    df["IsWeekend"] = df["DayOfWeek"].apply(lambda x: 1 if x >= 5 else 0)

    # 2. Cyclic Features (Sin/Cos Transformations)
    df["Hour_Sin"] = np.sin(2 * np.pi * df["Hour"] / 24.0)
    df["Hour_Cos"] = np.cos(2 * np.pi * df["Hour"] / 24.0)
    df["Month_Sin"] = np.sin(2 * np.pi * df["Month"] / 12.0)
    df["Month_Cos"] = np.cos(2 * np.pi * df["Month"] / 12.0)
    df["DayOfWeek_Sin"] = np.sin(2 * np.pi * df["DayOfWeek"] / 7.0)
    df["DayOfWeek_Cos"] = np.cos(2 * np.pi * df["DayOfWeek"] / 7.0)

    # 3. Lag Features
    if include_lags and target_col in df.columns:
        lag_periods = [1, 2, 3, 6, 12, 24, 48, 72, 168]
        for lag in lag_periods:
            df[f"Lag_{lag}"] = df[target_col].shift(lag)

        # 4. Rolling Statistical Features
        rolling_windows = [3, 6, 12, 24, 168]
        for window in rolling_windows:
            df[f"Rolling_Mean_{window}"] = df[target_col].shift(1).rolling(window=window).mean()
        
        df["Rolling_Std_24"] = df[target_col].shift(1).rolling(window=24).std()
        df["Rolling_Min_24"] = df[target_col].shift(1).rolling(window=24).min()
        df["Rolling_Max_24"] = df[target_col].shift(1).rolling(window=24).max()

    # 5. Weather & Renewable Features Interaction (if available)
    for col in WEATHER_COLUMNS + RENEWABLE_COLUMNS + HOLIDAY_COLUMNS:
        if col not in df.columns:
            # Fill with 0 or mean if missing in custom upload
            if col in RENEWABLE_COLUMNS:
                df[col] = 0.0
            elif col in WEATHER_COLUMNS:
                df[col] = 28.0 if col == "Temperature" else (50.0 if col == "Humidity" else 0.0)
            elif col in HOLIDAY_COLUMNS:
                df[col] = 0

    if "Festival" in df.columns:
        df["Festival"] = df["Festival"].fillna("None")

    if drop_na:
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)

    return df

def get_feature_columns(df):
    """
    Returns list of feature column names excluding Datetime, State, Region, Target, etc.
    """
    exclude_cols = [
        "Datetime", "State", "Region", "Festival", TARGET_COLUMN, "AEP_MW", "Energy Available (MU)",
        "Peak Demand (MW)", "Peak Met (MW)"
    ]
    return [col for col in df.columns if col not in exclude_cols]