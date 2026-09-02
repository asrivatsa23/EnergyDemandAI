import matplotlib.pyplot as plt

models = [
    "Linear Regression",
    "Random Forest",
    "XGBoost",
    "LSTM"
]

mae_scores = [
    1822.84,
    1255.65,
    174.53,
    162.59
]

plt.figure(figsize=(10,5))

plt.bar(
    models,
    mae_scores
)

plt.title(
    "Model Comparison (MAE)"
)

plt.xlabel(
    "Models"
)

plt.ylabel(
    "Mean Absolute Error"
)

plt.savefig(
    "../graphs/model_comparison.png"
)

plt.show()

print(
    "Graph Saved Successfully"
)