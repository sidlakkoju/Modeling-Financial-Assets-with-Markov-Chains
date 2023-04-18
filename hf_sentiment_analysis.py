# Model Source: https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis?text=Apple+Stock%3A+Santa+Claus+Disappointed%2C+But+What%27s+Next%3F

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from finviz_scraping import finviz_scraper
from datetime import datetime
import tqdm


# Load Model
tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Scrape headlines from finviz for given ticker
scraper = finviz_scraper('tsla')
headlines_df = scraper.get_news()

# Start analyzing headlines from current date
cur_date = f"{datetime.now().month:02}" + "/" + f"{datetime.now().day:02}" + "/" + f"{datetime.now().year:02}"
day_sentiments = {'positive' : 0, 'neutral': 0, 'negative' : 0}

# List where daily sentiments are stored
sentiments = []


# Function which returns most common sentiment for a given day
def get_max_sentiment():
    max_value = max(day_sentiments.values())
    max_keys = [key for key, value in day_sentiments.items() if value == max_value]
    if 'positive' in max_keys and not 'negative' in max_keys:
        max_sentiment = 'positive'
    elif 'negative' in max_keys and not 'positive' in max_keys:
        max_sentiment = 'negative'
    else:
        max_sentiment = 'neutral'
    return max_sentiment



# Iterate through the finviz headlines (past 5 days)
for index, row in headlines_df.iterrows():
    # New Day of Headlines
    if (not row['Date'] == cur_date):
        max_sentiment = get_max_sentiment()
        sentiments.append((cur_date, max_sentiment))
        day_sentiments = {'positive' : 0, 'neutral': 0, 'negative' : 0}
        cur_date = row['Date']
    day_sentiments[classifier(row['News Headline'])[0]['label']] += 1

# Evaluate last day in pandas df
max_sentiment = get_max_sentiment()
sentiments.append((cur_date, max_sentiment))

print(sentiments)