import pandas as pd
import numpy as np

# join price data and sentiment data
news_df = pd.read_csv('AAPL-histnews.csv')
price_df = pd.read_csv('/Users/vihar/PythonProjects/stoch_sys3060/saahith-fan-club/data/stock_price_data/AAPL.csv')

news_df['created_at'] = pd.to_datetime(news_df['created_at']).dt.date
price_df['Date'] = pd.to_datetime(price_df['Date']).dt.date

merged_df = pd.merge(news_df, price_df, left_on='created_at', right_on='Date', how='inner')

merged_df = merged_df[['created_at', 'Sentiment_New', 'Close']].rename(columns={'Close': 'Price'})
merged_df.to_csv('AAPL-histnews-merged.csv', index=False)


# read the merged_df and set the index to the "created_at" column
df = pd.read_csv('AAPL-histnews-merged.csv')
df["created_at"] = pd.to_datetime(df["created_at"])
df.set_index("created_at", inplace=True)
print(df.head())