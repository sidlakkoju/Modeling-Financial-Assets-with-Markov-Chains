### CREDIT: https://gist.github.com/shashankvemuri/b791e316efa18c8707fb912f69760b09 ###


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from datetime import datetime


pd.set_option('display.max_colwidth', 25)

class finviz_scraper() :
    def __init__(self, ticker):
        self.month_dict = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06', 'Jul' : '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12'}
        self.symbol = ticker
        url = ("http://finviz.com/quote.ashx?t=" + self.symbol.lower())
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        self.html = soup(webpage, "html.parser")

    def get_news(self):
        try:
            # Find news table
            self.news = pd.read_html(str(self.html), attrs = {'class': 'fullview-news-outer'})[0]

            # Add Headers
            self.news.columns = ['Time', 'News Headline']
            
            day = f"{datetime.now().day:02}"
            month = f"{datetime.now().month:02}"
            year = f"{datetime.now().year:02}"
            century = year[0:2]
            dates = []
            for index, row in self.news.iterrows():
                if (row['Time'][0:3] in self.month_dict):
                    
                    month = self.month_dict[row['Time'][0:3]]
                    day = row['Time'][4:6]
                    year = century + row['Time'][7:9]

                dates.append(month + '/' + day + '/' + year)

            self.news['Dates'] = dates
            return self.news

        except Exception as e:
            return e

    def get_insider(self):
        try:
            # Find insider table
            self.insider = pd.read_html(str(self.html), attrs = {'class': 'body-table'})[0]
            
            # Clean up insider dataframe
            self.insider = self.insider.iloc[1:]
            self.insider.columns = ['Trader', 'Relationship', 'Date', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']
            self.insider = self.insider[['Date', 'Trader', 'Relationship', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']]
            self.insider = self.insider.set_index('Date')
            return self.insider

        except Exception as e:
            return e


if __name__ == "__main__":
    scraper = finviz_scraper('tsla')
    print(scraper.get_news())
    print(scraper.get_insider())