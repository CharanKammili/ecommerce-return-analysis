def get_risky_customers(df, threshold=3):
    return df[df['is_returned']].groupby('user_id')['order_id'].count().loc[lambda x: x > threshold]

def get_loyal_customers(df):
    returned_users = df[df['is_returned']]['user_id'].unique()
    return df[~df['user_id'].isin(returned_users)]['user_id'].unique()

def top_spenders(df):
    return df.groupby('user_id')['price'].sum().sort_values(ascending=False).head(10)
