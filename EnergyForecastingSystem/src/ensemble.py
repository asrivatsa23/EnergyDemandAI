"""
EnergyDemandAI - Hybrid Ensemble Module
=======================================
Combines predictions from statistical, machine learning, and deep learning models
using validation-error inverse weighting strategy.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

class HybridEnsembleModel:
    def __init__(self, models_dict=None, weights=None):
        """
        models_dict: dict of {model_id: trained_model_instance}
        weights: dict of {model_id: weight_float}
        """
        self.models = models_dict or {}
        self.weights = weights or {}

    def fit_weights(self, val_predictions_dict, y_val):
        """
        Calculates ensemble weights based on Inverse Mean Absolute Error (MAE) on validation data.
        Better performing models get higher weights.
        """
        inverse_maes = {}
        total_inv_mae = 0.0

        for model_id, preds in val_predictions_dict.items():
            mae = mean_absolute_error(y_val, preds)
            # Avoid division by zero
            inv_mae = 1.0 / max(mae, 1e-5)
            inverse_maes[model_id] = inv_mae
            total_inv_mae += inv_mae

        # Normalize weights
        self.weights = {m_id: inv_mae / total_inv_mae for m_id, inv_mae in inverse_maes.items()}
        return self.weights

    def predict(self, predictions_dict):
        """
        Computes weighted average prediction across models.
        predictions_dict: {model_id: np.array of predictions}
        """
        first_key = list(predictions_dict.keys())[0]
        n_samples = len(predictions_dict[first_key])
        ensemble_pred = np.zeros(n_samples)

        # Sum available weights
        active_weight_sum = sum(self.weights.get(m_id, 0.0) for m_id in predictions_dict.keys())
        if active_weight_sum == 0:
            active_weight_sum = 1.0

        for model_id, preds in predictions_dict.items():
            w = self.weights.get(model_id, 1.0 / len(predictions_dict)) / active_weight_sum
            ensemble_pred += w * np.array(preds)

        return ensemble_pred
