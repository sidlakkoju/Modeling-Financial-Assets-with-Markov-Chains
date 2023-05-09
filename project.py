from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from finviz_scraping import finviz_scraper
from datetime import datetime
from tqdm import tqdm
import csv

# tokenizer = AutoTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")
# model = AutoModelForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")
device = torch.device("mps")

tokenizer = AutoTokenizer.from_pretrained("soleimanian/financial-roberta-large-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("soleimanian/financial-roberta-large-sentiment")
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

csv_file_name = 'AAPL-histnews.csv'
with open(csv_file_name) as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

# Add new column
header = rows[0]
header.append('Sentiment_New')
for i in tqdm(range(1, len(rows))):
    rows[i].append(classifier(rows[i][3])[0]['label'])

# Write to new file
with open(csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(rows)