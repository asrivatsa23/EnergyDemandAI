"""
EnergyDemandAI - Data Preprocessing Module
===========================================
Pipeline for chronological sorting, deduplication, missing value imputation,
outlier validation, and time-series split creation (train/val/test).
"""

import pandas as pd
import numpy as np
from src.config import TARGET_COLUMN, TRAIN_RATIO, VAL_RATIO, TEST_RATIO

def preprocess_data(df, target_col=TARGET_COLUMN):
    """
    Cleans DataFrame:
    - Sorts chronologically by Datetime
    - Removes duplicate timestamps
    - Forward/backward fills missing numerical values
    - Validates target range
    """
    df = df.copy()

    # Ensure Datetime is set and sorted
    if "Datetime" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        df.sort_values("Datetime", inplace=True)
        df.drop_duplicates(subset=["Datetime"], keep="last", inplace=True)
        df.reset_index(drop=True, inplace=True)

    # Impute missing numeric values using linear interpolation then ffill/bfill
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].interpolate(method="linear").bfill().ffill()

    # Target column range check (non-negative)
    if target_col in df.columns:
        df[target_col] = np.clip(df[target_col], a_min=0, a_max=None)

    return df

def chronological_split(df, train_ratio=TRAIN_RATIO, val_ratio=VAL_RATIO, test_ratio=TEST_RATIO):
    """
    Splits DataFrame strictly chronologically to prevent data leakage.
    Returns (train_df, val_df, test_df)
    """
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_end].copy().reset_index(drop=True)
    val_df = df.iloc[train_end:val_end].copy().reset_index(drop=True)
    test_df = df.iloc[val_end:].copy().reset_index(drop=True)

    return train_df, val_df, test_df