import os
import pandas as pd
from src.config import RESULTS_DIR

if __name__ == "__main__":
    csv_path = os.path.join(RESULTS_DIR, "model_comparison.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(df.to_string(index=False))
    else:
        print("No evaluation results found. Please run: python -m src.train")