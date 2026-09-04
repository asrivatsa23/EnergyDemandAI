"""
Unit Tests - Preprocessing & Data Loading Module
"""

import pytest
import pandas as pd
import numpy as np
from src.data_loader import load_dataset
from src.preprocessing import preprocess_data, chronological_split
from src.config import SAMPLE_DATA_PATH, TARGET_COLUMN

def test_load_dataset():
    df, meta = load_dataset(SAMPLE_DATA_PATH)
    assert not df.empty
    assert "Datetime" in df.columns
    assert TARGET_COLUMN in df.columns
    assert meta["total_rows"] > 0

def test_preprocess_data():
    df, _ = load_dataset(SAMPLE_DATA_PATH)
    df_clean = preprocess_data(df)
    assert df_clean["Datetime"].is_monotonic_increasing
    assert df_clean[TARGET_COLUMN].isnull().sum() == 0
    assert (df_clean[TARGET_COLUMN] >= 0).all()

def test_chronological_split():
    df, _ = load_dataset(SAMPLE_DATA_PATH)
    df_clean = preprocess_data(df)
    train_df, val_df, test_df = chronological_split(df_clean, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)
    
    total = len(train_df) + len(val_df) + len(test_df)
    assert total == len(df_clean)
    assert train_df["Datetime"].iloc[-1] < val_df["Datetime"].iloc[0]
    assert val_df["Datetime"].iloc[-1] < test_df["Datetime"].iloc[0]
