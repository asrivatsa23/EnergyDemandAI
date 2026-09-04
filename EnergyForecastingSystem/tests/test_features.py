"""
Unit Tests - Feature Engineering Module
"""

import pytest
import pandas as pd
from src.data_loader import load_dataset
from src.preprocessing import preprocess_data
from src.feature_engineering import create_features, get_feature_columns
from src.config import SAMPLE_DATA_PATH, TARGET_COLUMN

def test_feature_generation():
    df, _ = load_dataset(SAMPLE_DATA_PATH)
    df_clean = preprocess_data(df)
    df_feat = create_features(df_clean)

    feature_cols = get_feature_columns(df_feat)
    assert "Hour" in feature_cols
    assert "Month" in feature_cols
    assert "Hour_Sin" in feature_cols
    assert "Hour_Cos" in feature_cols
    assert "Lag_1" in feature_cols
    assert "Lag_24" in feature_cols
    assert "Rolling_Mean_24" in feature_cols
    assert TARGET_COLUMN not in feature_cols
