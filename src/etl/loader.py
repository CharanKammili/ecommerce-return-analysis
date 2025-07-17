import os
from src.config import PROCESSED_DATA_PATH

def save_transformed_data(df, filename='final_dataset.csv'):
    output_path = os.path.join(PROCESSED_DATA_PATH, filename)
    df.to_csv(output_path, index=False)
