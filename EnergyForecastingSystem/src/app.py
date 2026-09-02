"""
Energy Forecasting System - Backend API
========================================
Flask REST API powering the React dashboard.

Key features:
- CSV upload is the ONLY way to submit data for a prediction
  (there is no manual 24-field entry form).
- The dashboard can choose which trained model to use at request time:
  LSTM, Random Forest, XGBoost, or Linear Regression.
- Every prediction is returned together with a SHAP-based explanation,
  using the explainer best suited to that model type.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from tensorflow.keras.models import load_model

import pandas as pd
import numpy as np
import joblib
import shap
import io
import os
import random

# ======================================================
# Paths
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "AEP_hourly.csv")
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

TIME_STEPS = 24
TARGET_COLUMN = "AEP_MW"

LAG_FEATURES = ["Hour", "Day", "Month", "DayOfWeek", "Lag_1", "Lag_24"]
BASIC_FEATURES = ["Hour", "Day", "Month", "DayOfWeek"]

# ======================================================
# Flask Application
# ======================================================

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

# ======================================================
# Load Dataset (once, at startup)
# ======================================================

df = pd.read_csv(DATA_PATH)
df["Datetime"] = pd.to_datetime(df["Datetime"])
df.sort_values("Datetime", inplace=True)
df.reset_index(drop=True, inplace=True)

energy_values = df[TARGET_COLUMN].tolist()

random.seed(42)

# ======================================================
# Feature engineering (shared by RF / XGBoost / Linear Regression)
# ======================================================


def _engineer_features(target_ts, values):
    """
    Given the timestamp being predicted (target_ts) and the chronological
    24-hour window of raw MW values leading up to it, return a dict with
    all engineered features used by the tree/linear models.
    """
    return {
        "Hour": target_ts.hour,
        "Day": target_ts.day,
        "Month": target_ts.month,
        "DayOfWeek": target_ts.dayofweek,
        "Lag_1": values[-1],       # value one hour before the target
        "Lag_24": values[0],       # value 24 hours before the target
    }


def _dataset_feature_sample(columns, n=100):
    """Random real feature rows sampled from the historical dataset,
    used as SHAP background data."""
    d = df.copy()
    d["Hour"] = d["Datetime"].dt.hour
    d["Day"] = d["Datetime"].dt.day
    d["Month"] = d["Datetime"].dt.month
    d["DayOfWeek"] = d["Datetime"].dt.dayofweek
    d["Lag_1"] = d[TARGET_COLUMN].shift(1)
    d["Lag_24"] = d[TARGET_COLUMN].shift(24)
    d = d.dropna()
    sample = d[columns].sample(n=n, random_state=42)
    return sample


# ======================================================
# LSTM Model
# ======================================================

lstm_model = load_model(os.path.join(MODELS_DIR, "lstm_model.keras"))
lstm_scaler = joblib.load(os.path.join(MODELS_DIR, "lstm_scaler.pkl"))


def _lstm_predict_raw(sequences_mw: np.ndarray) -> np.ndarray:
    sequences_mw = np.asarray(sequences_mw, dtype=float)
    n_samples = sequences_mw.shape[0]

    flat = sequences_mw.reshape(-1, 1)
    scaled_flat = lstm_scaler.transform(flat)
    scaled = scaled_flat.reshape(n_samples, TIME_STEPS, 1)

    preds_scaled = lstm_model.predict(scaled, verbose=0)
    preds = lstm_scaler.inverse_transform(preds_scaled)

    return preds.flatten()


def _lstm_predict(values, timestamps, target_ts):
    prediction = float(_lstm_predict_raw(np.array(values).reshape(1, -1))[0])
    return prediction


def _build_lstm_background(n_windows: int = 30) -> np.ndarray:
    windows = []
    max_start = len(energy_values) - TIME_STEPS - 1
    starts = random.sample(range(0, max_start), n_windows)
    for start in starts:
        windows.append(energy_values[start:start + TIME_STEPS])
    return np.array(windows)


LSTM_BACKGROUND = _build_lstm_background()
LSTM_EXPLAINER = shap.KernelExplainer(_lstm_predict_raw, LSTM_BACKGROUND)


def _lstm_explain(values, timestamps, target_ts, nsamples=100):
    instance = np.array(values, dtype=float).reshape(1, TIME_STEPS)
    sv = LSTM_EXPLAINER.shap_values(instance, nsamples=nsamples, silent=True)

    if isinstance(sv, list):
        sv = sv[0]
    sv = np.array(sv).reshape(-1).tolist()

    base_value = LSTM_EXPLAINER.expected_value
    if isinstance(base_value, (list, np.ndarray)):
        base_value = float(np.array(base_value).flatten()[0])
    else:
        base_value = float(base_value)

    labels = timestamps if timestamps else [
        f"t-{TIME_STEPS - i}" for i in range(TIME_STEPS)
    ]

    return base_value, sv, labels


# ======================================================
# Random Forest / XGBoost (lag-feature tree models)
# ======================================================

rf_model = joblib.load(os.path.join(MODELS_DIR, "random_forest.pkl"))
xgb_model = joblib.load(os.path.join(MODELS_DIR, "xgboost.pkl"))

RF_EXPLAINER = shap.TreeExplainer(rf_model)
XGB_EXPLAINER = shap.TreeExplainer(xgb_model)


def _make_tree_predict(model):
    def _predict(values, timestamps, target_ts):
        features = _engineer_features(target_ts, values)
        X = pd.DataFrame([features])[LAG_FEATURES]
        return float(model.predict(X)[0])
    return _predict


def _make_tree_explain(explainer):
    def _explain(values, timestamps, target_ts):
        features = _engineer_features(target_ts, values)
        X = pd.DataFrame([features])[LAG_FEATURES]

        sv = explainer.shap_values(X)
        sv = np.array(sv).reshape(-1).tolist()

        base_value = explainer.expected_value
        if isinstance(base_value, (list, np.ndarray)):
            base_value = float(np.array(base_value).flatten()[0])
        else:
            base_value = float(base_value)

        return base_value, sv, LAG_FEATURES
    return _explain


# ======================================================
# Linear Regression (basic time features only)
# ======================================================

lr_model = joblib.load(os.path.join(MODELS_DIR, "linear_regression.pkl"))
LR_BACKGROUND = _dataset_feature_sample(BASIC_FEATURES, n=100)
LR_EXPLAINER = shap.LinearExplainer(lr_model, LR_BACKGROUND)


def _lr_predict(values, timestamps, target_ts):
    features = _engineer_features(target_ts, values)
    X = pd.DataFrame([features])[BASIC_FEATURES]
    return float(lr_model.predict(X)[0])


def _lr_explain(values, timestamps, target_ts):
    features = _engineer_features(target_ts, values)
    X = pd.DataFrame([features])[BASIC_FEATURES]

    sv = LR_EXPLAINER.shap_values(X)
    sv = np.array(sv).reshape(-1).tolist()

    base_value = LR_EXPLAINER.expected_value
    if isinstance(base_value, (list, np.ndarray)):
        base_value = float(np.array(base_value).flatten()[0])
    else:
        base_value = float(base_value)

    return base_value, sv, BASIC_FEATURES


# ======================================================
# Model Registry
# ======================================================
# Every model exposes the same interface so /api/predict can treat
# them interchangeably:
#   predict(values, timestamps, target_ts) -> float
#   explain(values, timestamps, target_ts) -> (base_value, shap_values, labels)

MODEL_REGISTRY = {
    "lstm": {
        "name": "LSTM",
        "description": "Sequence model trained on the raw previous 24 hourly readings.",
        "requires_datetime": False,
        "mae": 162.59,
        "r2": 0.9924,
        "predict": _lstm_predict,
        "explain": _lstm_explain,
    },
    "random_forest": {
        "name": "Random Forest",
        "description": "Ensemble of decision trees using time-of-day and lag features.",
        "requires_datetime": True,
        "mae": 182.34,
        "r2": 0.9902,
        "predict": _make_tree_predict(rf_model),
        "explain": _make_tree_explain(RF_EXPLAINER),
    },
    "xgboost": {
        "name": "XGBoost",
        "description": "Gradient-boosted trees using time-of-day and lag features.",
        "requires_datetime": True,
        "mae": 174.53,
        "r2": 0.9912,
        "predict": _make_tree_predict(xgb_model),
        "explain": _make_tree_explain(XGB_EXPLAINER),
    },
    "linear_regression": {
        "name": "Linear Regression",
        "description": "Baseline model using only time-of-day features (no lag).",
        "requires_datetime": True,
        "mae": 2011.59,
        "r2": 0.0506,
        "predict": _lr_predict,
        "explain": _lr_explain,
    },
}

DEFAULT_MODEL_ID = "lstm"

# ======================================================
# Helpers
# ======================================================


def get_random_sample():
    start = random.randint(0, len(energy_values) - TIME_STEPS - 1)
    return energy_values[start:start + TIME_STEPS]


def parse_uploaded_csv(file_storage):
    """
    Validates and parses an uploaded CSV file.
    Returns (values, timestamps_or_None) for the most recent
    TIME_STEPS rows, or raises ValueError with a user-facing message.
    """
    filename = file_storage.filename or ""

    if not filename.lower().endswith(".csv"):
        raise ValueError("Only .csv files are supported.")

    try:
        raw_bytes = file_storage.read()
        text_stream = io.StringIO(raw_bytes.decode("utf-8-sig"))
        data = pd.read_csv(text_stream)
    except Exception:
        raise ValueError("The file could not be read as a valid CSV.")

    if data.empty:
        raise ValueError("The uploaded CSV is empty.")

    column_map = {c.lower(): c for c in data.columns}
    target_col = column_map.get(TARGET_COLUMN.lower())

    if target_col is None:
        raise ValueError(
            f"The CSV must contain a '{TARGET_COLUMN}' column with hourly "
            f"energy consumption values (found columns: "
            f"{', '.join(data.columns)})."
        )

    datetime_col = None
    for candidate in data.columns:
        if candidate.lower() in ("datetime", "date", "timestamp"):
            datetime_col = candidate
            break

    if datetime_col is not None:
        try:
            data[datetime_col] = pd.to_datetime(data[datetime_col])
            data = data.sort_values(datetime_col)
        except Exception:
            datetime_col = None

    values = pd.to_numeric(data[target_col], errors="coerce")

    if values.isna().any():
        raise ValueError(
            f"The '{target_col}' column must contain only numeric values."
        )

    if len(values) < TIME_STEPS:
        raise ValueError(
            f"The CSV must contain at least {TIME_STEPS} rows of hourly "
            f"data (found {len(values)})."
        )

    tail = data.tail(TIME_STEPS)
    value_list = pd.to_numeric(tail[target_col]).tolist()

    timestamps = None
    if datetime_col is not None:
        timestamps = tail[datetime_col].astype(str).tolist()

    return value_list, timestamps


def resolve_target_timestamp(timestamps):
    """The model predicts the hour right after the last uploaded row."""
    if not timestamps:
        return None
    last_ts = pd.to_datetime(timestamps[-1])
    return last_ts + pd.Timedelta(hours=1)


# ======================================================
# Routes
# ======================================================

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/models")
def models():
    return jsonify({
        "default": DEFAULT_MODEL_ID,
        "models": [
            {
                "id": model_id,
                "name": info["name"],
                "description": info["description"],
                "mae": info["mae"],
                "r2": info["r2"],
                "requires_datetime": info["requires_datetime"],
            }
            for model_id, info in MODEL_REGISTRY.items()
        ],
    })


@app.route("/api/metrics")
def metrics():
    model_id = request.args.get("model", DEFAULT_MODEL_ID)
    info = MODEL_REGISTRY.get(model_id, MODEL_REGISTRY[DEFAULT_MODEL_ID])
    return jsonify({
        "model_name": info["name"],
        "mae": info["mae"],
        "r2": info["r2"],
    })


@app.route("/api/sample-csv")
def sample_csv():
    start = random.randint(0, len(df) - TIME_STEPS - 1)
    sample_df = df.iloc[start:start + TIME_STEPS][["Datetime", TARGET_COLUMN]]

    buffer = io.BytesIO()
    sample_df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name="sample_energy_data.csv",
    )


@app.route("/api/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "No file was uploaded. Please attach a CSV file.",
        }), 400

    file_storage = request.files["file"]

    if file_storage.filename == "":
        return jsonify({
            "success": False,
            "error": "No file was selected.",
        }), 400

    model_id = request.form.get("model", DEFAULT_MODEL_ID)
    model_info = MODEL_REGISTRY.get(model_id)

    if model_info is None:
        return jsonify({
            "success": False,
            "error": f"Unknown model '{model_id}'. Valid options: "
                     f"{', '.join(MODEL_REGISTRY.keys())}.",
        }), 400

    try:
        values, timestamps = parse_uploaded_csv(file_storage)
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred while parsing the CSV.",
        }), 400

    if model_info["requires_datetime"] and timestamps is None:
        return jsonify({
            "success": False,
            "error": (
                f"The {model_info['name']} model needs to know the "
                f"timestamp of each reading. Please include a "
                f"'Datetime' (or 'Date'/'Timestamp') column in your CSV, "
                f"or switch to the LSTM model, which only needs the raw "
                f"24-hour value sequence."
            ),
        }), 400

    target_ts = resolve_target_timestamp(timestamps)

    try:
        prediction = round(model_info["predict"](values, timestamps, target_ts), 2)
    except Exception as exc:
        return jsonify({
            "success": False,
            "error": f"Prediction failed: {exc}",
        }), 500

    try:
        base_value, shap_values, labels = model_info["explain"](
            values, timestamps, target_ts
        )
    except Exception as exc:
        return jsonify({
            "success": False,
            "error": f"Prediction succeeded but the SHAP explanation "
                     f"failed: {exc}",
        }), 500

    return jsonify({
        "success": True,
        "model_id": model_id,
        "model_name": model_info["name"],
        "mae": model_info["mae"],
        "r2": model_info["r2"],
        "input_values": [float(v) for v in values],
        "timestamps": timestamps,
        "target_timestamp": str(target_ts) if target_ts is not None else None,
        "prediction": prediction,
        "shap": {
            "base_value": round(base_value, 2),
            "values": [round(v, 2) for v in shap_values],
            "labels": labels,
        },
    })


@app.route("/api/sample")
def sample():
    sample_values = get_random_sample()
    return jsonify({"values": sample_values})


# ======================================================
# Run
# ======================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
