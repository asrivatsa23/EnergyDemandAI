import pandas as pd
from src.config import SAMPLE_DATA_PATH
from src.data_loader import load_dataset

df, meta = load_dataset(SAMPLE_DATA_PATH)

print(df.head())
print("\nShape:", df.shape)
print("\nColumns:", df.columns)
print("\nMissing Values:")
print(df.isnull().sum())
print("\nMetadata:", meta)