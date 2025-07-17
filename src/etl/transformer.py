def transform_data(orders, returns, products, users):
    orders['is_returned'] = orders['order_id'].isin(returns['order_id'])
    merged = orders.merge(products, on='product_id', how='left') \
                   .merge(users, on='user_id', how='left')
    return merged
