"""
EnergyDemandAI - Evaluation Module
===================================
Evaluates model predictions using MAE, RMSE, MAPE (zero-safe), and R2.
Generates metrics table and visualization comparison graphs.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from src.config import RESULTS_DIR, GRAPHS_DIR

def calculate_mape(y_true, y_pred):
    """Calculates zero-safe Mean Absolute Percentage Error (MAPE)."""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    # Avoid zero division
    mask = y_true != 0
    if not np.any(mask):
        return 0.0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100.0)

def evaluate_models(y_true, predictions_dict, train_times=None, predict_times=None):
    """
    Evaluates all model predictions against ground truth y_true.
    Returns metrics DataFrame and saves results/model_comparison.csv.
    """
    metrics = []
    train_times = train_times or {}
    predict_times = predict_times or {}

    for model_name, y_pred in predictions_dict.items():
        mae = float(mean_absolute_error(y_true, y_pred))
        rmse = float(root_mean_squared_error(y_true, y_pred))
        mape = calculate_mape(y_true, y_pred)
        r2 = float(r2_score(y_true, y_pred))

        metrics.append({
            "Model": model_name,
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "MAPE (%)": round(mape, 2),
            "R2": round(r2, 4),
            "Training Time (s)": round(train_times.get(model_name, 0.0), 3),
            "Prediction Time (s)": round(predict_times.get(model_name, 0.0), 3)
        })

    metrics_df = pd.DataFrame(metrics)
    
    # Save CSV artifact
    os.makedirs(RESULTS_DIR, exist_ok=True)
    csv_path = os.path.join(RESULTS_DIR, "model_comparison.csv")
    metrics_df.to_csv(csv_path, index=False)
    print(f"Saved evaluation metrics to: {csv_path}")

    # Generate comparison graph
    generate_comparison_chart(metrics_df)

    return metrics_df

def generate_comparison_chart(metrics_df):
    """Generates comparison bar chart and saves to graphs/."""
    os.makedirs(GRAPHS_DIR, exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # MAE Chart
    axes[0].bar(metrics_df["Model"], metrics_df["MAE"], color="#3b82f6")
    axes[0].set_title("Model MAE Comparison (Lower is Better)")
    axes[0].set_ylabel("MAE (MU)")
    axes[0].tick_params(axis='x', rotation=30)
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # R2 Chart
    axes[1].bar(metrics_df["Model"], metrics_df["R2"], color="#10b981")
    axes[1].set_title("Model R² Comparison (Higher is Better)")
    axes[1].set_ylabel("R² Score")
    axes[1].set_ylim(-0.1, 1.05)
    axes[1].tick_params(axis='x', rotation=30)
    axes[1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    chart_path = os.path.join(GRAPHS_DIR, "model_comparison.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Saved model comparison chart to: {chart_path}")
