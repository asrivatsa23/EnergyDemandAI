"""
EnergyDemandAI - Forecasting Engine
====================================
Generates multi-step ahead forecasts (1h, 6h, 24h, 7d) across individual and ensemble models.
"""

import pandas as pd
import numpy as np
from src.config import TARGET_COLUMN
from src.feature_engineering import create_features, get_feature_columns

def generate_forecast(model_obj, model_type, historical_df, horizon_hours=24, feature_cols=None):
    """
    Generates multi-step ahead demand predictions.
    
    historical_df: DataFrame containing at least lookback hourly records.
    horizon_hours: 1, 6, 24, or 168 (7 days).
    """
    df = historical_df.copy()
    if "Datetime" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        df.sort_values("Datetime", inplace=True)

    last_timestamp = df["Datetime"].iloc[-1]
    last_known_demand = df[TARGET_COLUMN].iloc[-1]

    # Generate future timestamps
    future_timestamps = [last_timestamp + pd.Timedelta(hours=i+1) for i in range(horizon_hours)]
    forecast_results = []

    # Iterative multi-step prediction
    curr_df = df.copy()

    for ts in future_timestamps:
        # Append target row placeholder
        new_row = {
            "Datetime": ts,
            "State": curr_df["State"].iloc[-1] if "State" in curr_df.columns else "Maharashtra",
            "Region": curr_df["Region"].iloc[-1] if "Region" in curr_df.columns else "Western Region",
            TARGET_COLUMN: curr_df[TARGET_COLUMN].iloc[-1], # Placeholder
            "Temperature": 28.0 + 4.0 * np.sin((ts.hour - 8) * np.pi / 12),
            "Humidity": 55.0,
            "Rainfall": 0.0,
            "Solar Generation": float(max(0, 100.0 * np.sin((ts.hour - 6) * np.pi / 12))) if 6 <= ts.hour <= 18 else 0.0,
            "Wind Generation": 40.0,
            "Hydro Generation": 50.0,
            "Holiday": 1 if ts.weekday() == 6 else 0,
            "Festival": "None"
        }
        
        temp_df = pd.concat([curr_df, pd.DataFrame([new_row])], ignore_index=True)
        feat_df = create_features(temp_df, drop_na=False)
        
        target_row = feat_df.iloc[-1:]
        
        if feature_cols is None:
            feature_cols = get_feature_columns(feat_df)

        X_target = target_row[feature_cols].fillna(0)

        # Predict based on model type
        if model_type == "linear_regression":
            # Baseline uses basic calendar features
            basic_cols = ["Hour", "Day", "Month", "DayOfWeek"]
            X_base = target_row[[c for c in basic_cols if c in target_row.columns]].fillna(0)
            pred = float(model_obj.predict(X_base)[0])
        elif model_type in ["random_forest", "xgboost"]:
            pred = float(model_obj.predict(X_target)[0])
        elif model_type == "arima":
            recent_hist = curr_df[TARGET_COLUMN].values
            arima_preds = model_obj.predict_instance(recent_hist, steps=1)
            pred = float(arima_preds[0])
        elif model_type == "lstm":
            # For LSTM sequence input
            if len(X_target) > 0:
                X_seq_window = feat_df[feature_cols].tail(model_obj.time_steps)
                if len(X_seq_window) == model_obj.time_steps:
                    pred = model_obj.predict_sequence(X_seq_window.fillna(0).values)
                else:
                    pred = float(curr_df[TARGET_COLUMN].iloc[-1])
            else:
                pred = float(curr_df[TARGET_COLUMN].iloc[-1])
        else:
            pred = float(curr_df[TARGET_COLUMN].iloc[-1])

        # Clip non-negative
        pred = round(max(0.0, float(pred)), 2)

        # Update placeholder in temp_df and curr_df
        temp_df.loc[temp_df.index[-1], TARGET_COLUMN] = pred
        curr_df = temp_df.copy()

        forecast_results.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": ts.hour,
            "predicted_demand": pred
        })

    return forecast_results
