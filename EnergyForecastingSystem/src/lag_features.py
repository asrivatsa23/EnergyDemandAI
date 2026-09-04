from src.config import SAMPLE_DATA_PATH
from src.data_loader import load_dataset
from src.feature_engineering import create_features

if __name__ == "__main__":
    df, _ = load_dataset(SAMPLE_DATA_PATH)
    df_feat = create_features(df)
    print("Engineered lag and temporal features successfully.")
    print("Columns:", list(df_feat.columns))