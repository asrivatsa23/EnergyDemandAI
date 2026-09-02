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
Backend Setup
# Navigate to the system directory
cd EnergyForecastingSystem

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API server / app
python src/app.py
Frontend Setup
# Navigate to frontend directory
cd EnergyForecastingSystem/frontend
📊 Models & Evaluation
The system processes hourly load datasets to evaluate model accuracy across standard metrics:

RMSE (Root Mean Squared Error)

MAE (Mean Absolute Error)

R² Score (Coefficient of Determination)

Model outputs and comparison charts are stored automatically in /graphs and /results.
# Install dependencies
npm install

# Start development server
npm run dev
