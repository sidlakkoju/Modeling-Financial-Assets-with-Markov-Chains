from alpaca.tradeapi.rest import REST

# authentication and connection details
API_KEY = 'PKQ89N6MBAFGWQ44DDGX'
API_SECRET = '8qvyZ2pTScgnIl86Tn6VQJU3qb8KMT3RLzl4gzYJ'
BASE_URL =  'https://paper-api.alpaca.markets'  # Use 'https://api.alpaca.markets' for live trading
TICKER = 'TSLA'

start_date = '2013-01-01T00:00:00Z'
end_date = '2023-01-01T00:00:00Z'

# Initialize the Alpaca API for trading
tradeapi = REST(API_KEY, API_SECRET, base_url=BASE_URL)

# Get the historical price data for the stock
barset = tradeapi.get_barset(TICKER, '1D', start=start_date, end=end_date).df

# Initialize the Alpaca API for news
news_client = RESTClient(base_url='https://data.alpaca.markets',
                         api_version='v1beta1',
                         api_key=API_KEY, 
                         secret_key=API_SECRET,)

news_endpoint = '/news'
parameters = {'start':start_date,
              'end':end_date,
              'symbols':TICKER,
}

news = news_client.get(news_endpoint, parameters,)
next_page_token = news.get('next_page_token')

df = pd.DataFrame.from_dict(news['news'])

# Convert the 'published_utc' to date only and set it as the index
df['published_utc'] = pd.to_datetime(df['published_utc']).dt.date
df.set_index('published_utc', inplace=True)

while next_page_token:
    parameters['page_token'] = next_page_token
    news = news_client.get(news_endpoint, parameters,)
    next_page_token = news.get('next_page_token')
    temp_df = pd.DataFrame.from_dict(news['news'])
    temp_df['published_utc'] = pd.to_datetime(temp_df['published_utc']).dt.date
    temp_df.set_index('published_utc', inplace=True)
    df = pd.concat([df, temp_df], ignore_index=False)

# Merge the news and price dataframes
df = df.join(barset[TICKER]['close'], how='left')

df.to_csv(f'{TICKER}-histnews.csv', index=False)