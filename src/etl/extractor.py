import pandas as pd
import os
from src.config import RAW_DATA_PATH

def load_raw_data():
    orders = pd.read_csv(os.path.join(RAW_DATA_PATH, "orders.csv"))
    returns = pd.read_csv(os.path.join(RAW_DATA_PATH, "returns.csv"))
    products = pd.read_csv(os.path.join(RAW_DATA_PATH, "products.csv"))
    users = pd.read_csv(os.path.join(RAW_DATA_PATH, "users.csv"))
    return orders, returns, products, users
