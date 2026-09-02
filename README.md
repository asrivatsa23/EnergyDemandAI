# ⚡ EnergyDemandAI - Hourly Energy Consumption Forecasting System

An end-to-end Machine Learning and Deep Learning system for forecasting hourly energy demand. Includes an interactive web frontend to run model predictions, compare performance metrics, and view SHAP explainability analyses.

---

## 📌 Features

* **Multiple Forecasting Models**: Evaluates Linear Regression, Random Forest, XGBoost, and LSTM (Long Short-Term Memory) neural networks.
* **Feature Engineering**: Built-in temporal feature extraction and configurable lag features.
* **Interactive Frontend**: Modern React + Vite interface to select models, adjust parameters, upload custom CSVs, and view charts.
* **Model Explainability**: SHAP (SHapley Additive exPlanations) visual outputs for interpreting predictions.
* **Metrics Comparison**: Automated comparison tables evaluating RMSE, MAE, and R² scores.

---

## 🛠️ Project Structure

```text
EnergyForecastingSystem/
├── data/                 # Raw datasets (e.g., AEP_hourly.csv)
├── frontend/             # React + Vite web user interface
├── graphs/               # Generated evaluation plots and visualizations
├── models/               # Saved trained model artifacts
├── results/              # Comparative CSV outputs (e.g., model_comparison.csv)
├── screenshots/          # Application preview images
└── src/                  # Core Python modules & ML pipelines
    ├── app.py            # API Server / Main app entrypoint
    ├── feature_engineering.py
    ├── lag_features.py
    ├── linear_regression.py
    ├── lstm_model.py
    ├── random_forest_model.py
    ├── xgboost_model.py
    └── model_comparison.py
