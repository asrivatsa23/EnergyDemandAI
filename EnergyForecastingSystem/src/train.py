"""
EnergyDemandAI - Pipeline & Model Training Script
=================================================
Executes end-to-end dataset loading, preprocessing, feature engineering,
model training (LR, RF, XGB, ARIMA, LSTM, Hybrid Ensemble), evaluation,
and serializes artifacts into models/ and results/.
"""

import os
import time
import joblib
import pandas as pd
import numpy as np

from src.config import (
    MODELS_DIR, SAMPLE_DATA_PATH, TARGET_COLUMN, TIME_STEPS
)
from src.data_loader import load_dataset
from src.preprocessing import preprocess_data, chronological_split
from src.feature_engineering import create_features, get_feature_columns
from src.models.linear_regression import LinearRegressionModel
from src.models.random_forest import RandomForestModel
from src.models.xgboost import XGBoostModel
from src.models.arima import ARIMAModel
from src.models.lstm import LSTMModel
from src.ensemble import HybridEnsembleModel
from src.evaluate import evaluate_models

def train_pipeline():
    print("=" * 60)
    print("EnergyDemandAI Pipeline & Model Training")
    print("=" * 60)

    # 1. Load Data
    df, meta = load_dataset(SAMPLE_DATA_PATH)
    print(f"Loaded dataset with {len(df)} rows. Target: '{TARGET_COLUMN}'")

    # 2. Preprocess
    df_clean = preprocess_data(df)

    # 3. Feature Engineering
    df_feat = create_features(df_clean)
    feature_cols = get_feature_columns(df_feat)
    print(f"Generated {len(feature_cols)} engineered features.")

    # Save feature names for inference
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(feature_cols, os.path.join(MODELS_DIR, "feature_columns.pkl"))

    # 4. Chronological Split
    train_df, val_df, test_df = chronological_split(df_feat)
    print(f"Data split - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

    X_train, y_train = train_df[feature_cols], train_df[TARGET_COLUMN]
    X_val, y_val = val_df[feature_cols], val_df[TARGET_COLUMN]
    X_test, y_test = test_df[feature_cols], test_df[TARGET_COLUMN]

    train_times = {}
    predict_times = {}
    test_preds = {}
    val_preds = {}

    # --- 1. Linear Regression Baseline ---
    print("\nTraining Linear Regression Baseline...")
    lr_cols = [c for c in ["Hour", "Day", "Month", "DayOfWeek"] if c in feature_cols]
    t0 = time.time()
    lr = LinearRegressionModel()
    lr.fit(X_train[lr_cols], y_train)
    train_times["Linear Regression"] = time.time() - t0

    t0 = time.time()
    test_preds["Linear Regression"] = lr.predict(X_test[lr_cols])
    predict_times["Linear Regression"] = time.time() - t0
    val_preds["Linear Regression"] = lr.predict(X_val[lr_cols])
    lr.save(os.path.join(MODELS_DIR, "linear_regression.pkl"))

    # --- 2. Random Forest ---
    print("Training Random Forest Regressor...")
    t0 = time.time()
    rf = RandomForestModel(n_estimators=100, max_depth=15)
    rf.fit(X_train, y_train)
    train_times["Random Forest"] = time.time() - t0

    t0 = time.time()
    test_preds["Random Forest"] = rf.predict(X_test)
    predict_times["Random Forest"] = time.time() - t0
    val_preds["Random Forest"] = rf.predict(X_val)
    rf.save(os.path.join(MODELS_DIR, "random_forest.pkl"))

    # --- 3. XGBoost ---
    print("Training XGBoost Regressor...")
    t0 = time.time()
    xgb = XGBoostModel(n_estimators=150, max_depth=6, learning_rate=0.05)
    xgb.fit(X_train, y_train)
    train_times["XGBoost"] = time.time() - t0

    t0 = time.time()
    test_preds["XGBoost"] = xgb.predict(X_test)
    predict_times["XGBoost"] = time.time() - t0
    val_preds["XGBoost"] = xgb.predict(X_val)
    xgb.save(os.path.join(MODELS_DIR, "xgboost.pkl"))

    # --- 4. ARIMA ---
    print("Fitting ARIMA Statistical Model...")
    t0 = time.time()
    arima = ARIMAModel(order=(2, 1, 2))
    arima.fit(y_train)
    train_times["ARIMA"] = time.time() - t0

    t0 = time.time()
    # Generate rolling forecast on test set
    arima_test_preds = arima.predict_instance(y_train.values, steps=len(y_test))
    predict_times["ARIMA"] = time.time() - t0
    test_preds["ARIMA"] = arima_test_preds
    val_preds["ARIMA"] = arima.predict_instance(y_train.values, steps=len(y_val))
    arima.save(os.path.join(MODELS_DIR, "arima.pkl"))

    # --- 5. Multivariate LSTM ---
    print("Training Multivariate LSTM Deep Learning Model...")
    t0 = time.time()
    lstm = LSTMModel(time_steps=TIME_STEPS, n_features=len(feature_cols))
    lstm.fit(X_train, y_train, epochs=8, batch_size=32)
    train_times["Multivariate LSTM"] = time.time() - t0

    t0 = time.time()
    lstm_test_pred = lstm.predict(X_test)
    # Align test predictions due to lookback sequence padding
    if len(lstm_test_pred) < len(y_test):
        pad_len = len(y_test) - len(lstm_test_pred)
        lstm_test_pred = np.pad(lstm_test_pred, (pad_len, 0), mode='edge')
    test_preds["Multivariate LSTM"] = lstm_test_pred
    predict_times["Multivariate LSTM"] = time.time() - t0

    lstm_val_pred = lstm.predict(X_val)
    if len(lstm_val_pred) < len(y_val):
        lstm_val_pred = np.pad(lstm_val_pred, (len(y_val) - len(lstm_val_pred), 0), mode='edge')
    val_preds["Multivariate LSTM"] = lstm_val_pred

    lstm.save(
        os.path.join(MODELS_DIR, "lstm_model.keras"),
        os.path.join(MODELS_DIR, "lstm_scaler.pkl")
    )

    # --- 6. Hybrid Ensemble ---
    print("Constructing Hybrid Ensemble Model...")
    ensemble = HybridEnsembleModel()
    weights = ensemble.fit_weights(val_preds, y_val)
    print("Ensemble Weights:", {k: round(v, 4) for k, v in weights.items()})

    t0 = time.time()
    test_preds["Hybrid Ensemble"] = ensemble.predict(test_preds)
    predict_times["Hybrid Ensemble"] = time.time() - t0
    train_times["Hybrid Ensemble"] = sum(train_times.values())

    joblib.dump(weights, os.path.join(MODELS_DIR, "ensemble_weights.pkl"))

    # 5. Evaluate all models
    print("\nEvaluating all models on chronological test set...")
    metrics_df = evaluate_models(y_test, test_preds, train_times, predict_times)
    print("\n" + metrics_df.to_string(index=False))
    print("\nPipeline and training completed successfully!")

if __name__ == "__main__":
    train_pipeline()
