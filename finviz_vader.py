import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

def scrape_headlines(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')


    # Might have to use this depending on which html class is right:
    news_table = soup.find(id = 'news-table')
    rows = news_table.find_all('div', class_ = "news-link-left")
    headlines = []
    for row in news_table.find_all('div', class_ = "news-link-left"):
      # print(row.text)
      # headline = row.text
      headlines.append(row.text)
    return headlines


ticker = input("Enter a company ticker: ")
headlines = scrape_headlines(ticker)
for headline in headlines:
    print(headline)



def sentiment_analysis(headlines):
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(h)["compound"] for h in headlines]
    return sum(scores) / len(scores)

ticker = input("Enter a company ticker: ")
headlines = scrape_headlines(ticker)
print(headlines)
mean_sentiment = sentiment_analysis(headlines)
print(mean_sentiment)
