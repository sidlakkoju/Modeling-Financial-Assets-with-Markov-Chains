# For 3x3 matrix of just sentiments x sentiments:
import pandas as pd
import numpy as np

df = pd.read_csv('AAPL-histnews.csv')

df["created_at"] = pd.to_datetime(df["created_at"])

df = df.sort_values(by="created_at")

sentiment_values = df["Sentiment_New"].unique()
num_sentiments = len(sentiment_values)
# should be 3x3 matrix
transition_matrix = np.zeros((num_sentiments, num_sentiments))

for i in range(1, len(df)):
    prev_sentiment = df.iloc[i-1]["Sentiment_New"]
    curr_sentiment = df.iloc[i]["Sentiment_New"]

    row_idx = np.where(sentiment_values == prev_sentiment)[0][0]
    col_idx = np.where(sentiment_values == curr_sentiment)[0][0]

    transition_matrix[row_idx][col_idx] += 1

row_sums = transition_matrix.sum(axis=1, keepdims=True)
transition_matrix = transition_matrix / row_sums

transition_df = pd.DataFrame(transition_matrix, columns=sentiment_values, index=sentiment_values)

# print(transition_matrix)
print(transition_df)