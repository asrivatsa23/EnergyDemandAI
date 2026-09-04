"""
EnergyDemandAI - Anomaly Detection Module
=========================================
Identifies unusual electricity demand spikes, drops, and unexpected forecasting residuals
using Isolation Forest and Z-Score statistical thresholding.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from src.config import TARGET_COLUMN

def detect_anomalies(df, target_col=TARGET_COLUMN, contamination=0.03):
    """
    Detects demand anomalies in historical time-series DataFrame.
    Returns DataFrame with anomaly flags, scores, and anomaly classification.
    """
    df = df.copy()
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame.")

    # 1. Isolation Forest Anomaly Detection
    iso = IsolationForest(contamination=contamination, random_state=42)
    series_vals = df[target_col].values.reshape(-1, 1)
    df["iso_anomaly_flag"] = iso.fit_predict(series_vals)
    df["iso_anomaly"] = df["iso_anomaly_flag"].apply(lambda x: 1 if x == -1 else 0)

    # 2. Statistical Z-score Thresholding (Z > 3 or Z < -3)
    mean_val = df[target_col].mean()
    std_val = df[target_col].std()
    
    df["z_score"] = (df[target_col] - mean_val) / (std_val if std_val > 0 else 1.0)
    df["z_anomaly"] = df["z_score"].apply(lambda x: 1 if abs(x) > 2.8 else 0)

    # Combined anomaly condition
    df["is_anomaly"] = ((df["iso_anomaly"] == 1) | (df["z_anomaly"] == 1)).astype(int)

    # Anomaly Type Classification
    def classify_anomaly(row):
        if row["is_anomaly"] == 1:
            if row["z_score"] > 2.0:
                return "Unusual Demand Spike"
            elif row["z_score"] < -2.0:
                return "Unusual Demand Drop"
            else:
                return "Structural Demand Anomaly"
        return "Normal"

    df["anomaly_type"] = df.apply(classify_anomaly, axis=1)

    # Format list of detected anomalies
    anomalies_df = df[df["is_anomaly"] == 1]
    anomalies_list = []

    for idx, row in anomalies_df.iterrows():
        anomalies_list.append({
            "index": int(idx),
            "timestamp": str(row["Datetime"]) if "Datetime" in row else str(idx),
            "demand": float(round(row[target_col], 2)),
            "z_score": float(round(row["z_score"], 2)),
            "type": row["anomaly_type"],
            "severity": "High" if abs(row["z_score"]) > 3.5 else "Medium"
        })

    return {
        "total_anomalies": len(anomalies_list),
        "anomaly_rate_percent": round(len(anomalies_list) / len(df) * 100.0, 2),
        "anomalies": anomalies_list
    }
