from src.config import SAMPLE_DATA_PATH
from src.data_loader import load_dataset
from src.preprocessing import preprocess_data

if __name__ == "__main__":
    df, meta = load_dataset(SAMPLE_DATA_PATH)
    df_clean = preprocess_data(df)
    print("Preprocessed Indian Electricity Dataset successfully.")
    print("Shape:", df_clean.shape)