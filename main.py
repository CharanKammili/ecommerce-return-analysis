from src.etl.extractor import load_raw_data
from src.etl.transformer import transform_data
from src.etl.loader import save_transformed_data
from src.analysis.return_analysis import calculate_return_rate, returns_by_category
from src.analysis.customer_segmentation import get_risky_customers
from src.util import log_step

if __name__ == "__main__":
    log_step("Extracting Data")
    orders, returns, products, users = load_raw_data()

    log_step("Transforming Data")
    final_df = transform_data(orders, returns, products, users)

    log_step("Saving Processed Data")
    save_transformed_data(final_df)

    log_step("Analyzing Returns")
    print("Return Rate:", calculate_return_rate(final_df), "%")
    print("Returns by Category:\n", returns_by_category(final_df))

    log_step("Segmenting Customers")
    print("Risky Customers:\n", get_risky_customers(final_df))
