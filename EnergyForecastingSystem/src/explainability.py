"""
EnergyDemandAI - Explainable AI (XAI) Module
=============================================
Provides SHAP and LIME model explanations with feature attributions,
contribution directions, and natural language decision insights.
"""

import numpy as np
import pandas as pd
import shap
from lime.lime_tabular import LimeTabularExplainer

def explain_tree_model(model, X_sample, feature_names):
    """
    Computes SHAP feature importance for Tree-based models (Random Forest, XGBoost).
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    
    if isinstance(shap_values, list):
        shap_values = shap_values[0]

    # Calculate average absolute SHAP value across samples
    mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
    
    # Feature attributions for the last instance
    latest_shap = shap_values[-1] if len(shap_values) > 0 else mean_abs_shap
    latest_x = X_sample.iloc[-1] if isinstance(X_sample, pd.DataFrame) else X_sample[-1]

    feature_importances = []
    for i, name in enumerate(feature_names):
        val = float(latest_shap[i])
        feature_importances.append({
            "feature": name,
            "value": float(latest_x[name]) if isinstance(latest_x, (pd.Series, dict)) else float(latest_x[i]),
            "importance": round(abs(val), 4),
            "contribution": round(val, 4),
            "direction": "positive" if val >= 0 else "negative"
        })

    # Sort by absolute importance
    feature_importances.sort(key=lambda x: x["importance"], reverse=True)
    
    # Base value
    base_val = explainer.expected_value
    if isinstance(base_val, (list, np.ndarray)):
        base_val = float(np.array(base_val).flatten()[0])
    else:
        base_val = float(base_val)

    # Generate natural language summary
    top_pos = [f['feature'] for f in feature_importances if f['direction'] == 'positive'][:2]
    top_neg = [f['feature'] for f in feature_importances if f['direction'] == 'negative'][:2]

    explanation_summary = (
        f"Demand forecast is primarily driven upward by {', '.join(top_pos) if top_pos else 'seasonal peak trends'}, "
        f"while being moderated down by {', '.join(top_neg) if top_neg else 'base load factors'}."
    )

    return {
        "base_value": round(base_val, 2),
        "features": feature_importances,
        "summary": explanation_summary
    }

def explain_linear_model(model, X_sample, feature_names):
    """
    Computes SHAP explanations for Linear Regression.
    """
    explainer = shap.LinearExplainer(model, X_sample)
    shap_values = explainer.shap_values(X_sample)
    
    latest_shap = shap_values[-1]
    latest_x = X_sample.iloc[-1]

    feature_importances = []
    for i, name in enumerate(feature_names):
        val = float(latest_shap[i])
        feature_importances.append({
            "feature": name,
            "value": float(latest_x[name]),
            "importance": round(abs(val), 4),
            "contribution": round(val, 4),
            "direction": "positive" if val >= 0 else "negative"
        })

    feature_importances.sort(key=lambda x: x["importance"], reverse=True)
    base_val = float(np.mean(model.predict(X_sample)))

    return {
        "base_value": round(base_val, 2),
        "features": feature_importances,
        "summary": "Linear model attribution based on temporal calendar coefficients."
    }

def explain_with_lime(model_predict_func, X_train, instance_x, feature_names):
    """
    Generates LIME local instance explanation.
    """
    try:
        explainer = LimeTabularExplainer(
            training_data=np.array(X_train),
            feature_names=feature_names,
            mode='regression'
        )
        exp = explainer.explain_instance(
            data_row=np.array(instance_x),
            predict_fn=model_predict_func,
            num_features=5
        )
        
        lime_list = []
        for feat, weight in exp.as_list():
            lime_list.append({
                "rule": feat,
                "weight": round(float(weight), 4),
                "direction": "positive" if weight >= 0 else "negative"
            })
        return lime_list
    except Exception as e:
        return [{"rule": "LIME explanation fallback", "weight": 0.0, "direction": "neutral"}]
