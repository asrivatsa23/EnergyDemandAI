"""
EnergyDemandAI - Data Loader Module
====================================
Handles loading, schema validation, and column mapping for Indian electricity demand datasets.
"""

import os
import pandas as pd
import numpy as np
from src.config import (
    SAMPLE_DATA_PATH, TARGET_COLUMN, ALTERNATIVE_TARGET_COLUMNS,
    DATETIME_COLUMNS, STATE_COLUMN, REGION_COLUMN,
    WEATHER_COLUMNS, RENEWABLE_COLUMNS, HOLIDAY_COLUMNS
)

def load_dataset(data_path=None, file_buffer=None):
    """
    Loads dataset from a path or file-like object.
    Identifies datetime and target columns, standardizes naming,
    and returns a clean DataFrame with schema metadata.
    """
    if file_buffer is not None:
        try:
            df = pd.read_csv(file_buffer)
        except Exception as e:
            raise ValueError(f"Could not parse uploaded CSV file: {e}")
    else:
        path_to_use = data_path if data_path and os.path.exists(data_path) else SAMPLE_DATA_PATH
        if not os.path.exists(path_to_use):
            raise FileNotFoundError(f"Dataset not found at {path_to_use}")
        df = pd.read_csv(path_to_use)

    if df.empty:
        raise ValueError("Dataset is empty.")

    # Standardize column mapping
    cols = {col.strip(): col.strip() for col in df.columns}
    
    # 1. Identify Datetime column
    datetime_col = None
    for candidate in DATETIME_COLUMNS:
        for c in df.columns:
            if c.lower() == candidate.lower():
                datetime_col = c
                break
        if datetime_col:
            break

    if datetime_col:
        df[datetime_col] = pd.to_datetime(df[datetime_col], errors="coerce")
        df.rename(columns={datetime_col: "Datetime"}, inplace=True)
    else:
        raise ValueError("Dataset must contain a valid Datetime/Date timestamp column.")

    # 2. Identify Target column
    target_col = None
    for candidate in ALTERNATIVE_TARGET_COLUMNS:
        for c in df.columns:
            if c.lower() == candidate.lower():
                target_col = c
                break
        if target_col:
            break

    if not target_col:
        # Fallback: take the first numeric column that is not Datetime or ID
        numeric_cols = [c for c in df.columns if c != "Datetime" and pd.api.types.is_numeric_dtype(df[c])]
        if numeric_cols:
            target_col = numeric_cols[0]
        else:
            raise ValueError(f"Could not find a target energy demand column (expected one of {ALTERNATIVE_TARGET_COLUMNS}).")

    if target_col != TARGET_COLUMN:
        df.rename(columns={target_col: TARGET_COLUMN}, inplace=True)

    # Convert target column to numeric
    df[TARGET_COLUMN] = pd.to_numeric(df[TARGET_COLUMN], errors="coerce")

    # Metadata check on available optional columns
    metadata = {
        "has_state": STATE_COLUMN in df.columns,
        "has_region": REGION_COLUMN in df.columns,
        "weather_features": [c for c in WEATHER_COLUMNS if c in df.columns],
        "renewable_features": [c for c in RENEWABLE_COLUMNS if c in df.columns],
        "holiday_features": [c for c in HOLIDAY_COLUMNS if c in df.columns],
        "total_rows": len(df)
    }

    return df, metadata
