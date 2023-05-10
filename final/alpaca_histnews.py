from alpaca.common.rest import RESTClient
import pandas as pd





# authentication and connection details
API_KEY = 'PKQ89N6MBAFGWQ44DDGX'
API_SECRET = '8qvyZ2pTScgnIl86Tn6VQJU3qb8KMT3RLzl4gzYJ'
BASE_URL =  'https://paper-api.alpaca.markets'  # Use 'https://api.alpaca.markets' for live trading
TICKER = 'TSLA'

start_date = '2013-01-01T00:00:00Z'
end_date = '2023-01-01T00:00:00Z'

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

while next_page_token:
    parameters['page_token'] = next_page_token
    news = news_client.get(news_endpoint, parameters,)
    next_page_token = news.get('next_page_token')
    df = pd.concat([df, pd.DataFrame.from_dict(news['news'])], ignore_index=True)
    if not next_page_token:
        break

df.to_csv(f'{TICKER}-histnews.csv', index=False)