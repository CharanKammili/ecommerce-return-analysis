def calculate_return_rate(df):
    total_orders = len(df)
    returned_orders = df['is_returned'].sum()
    return round((returned_orders / total_orders) * 100, 2)

def returns_by_category(df):
    return df[df['is_returned']].groupby('category')['order_id'].count().sort_values(ascending=False)

def returns_by_city(df):
    return df[df['is_returned']].groupby('location')['order_id'].count().sort_values(ascending=False)
