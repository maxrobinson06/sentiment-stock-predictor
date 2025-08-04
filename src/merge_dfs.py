import numpy as np
import pandas as pd

tweet_df = pd.read_csv("data/processed/MSFT_tweets.csv")
stock_df = pd.read_csv(
    'data/raw/MSFT_prices.csv',
    skiprows=3,  # Skip 3 rows to reach actual data
    names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'],
    parse_dates=['Date']
)
tweet_df['Date'] = pd.to_datetime(tweet_df['Date']).dt.tz_localize(None).dt.date
stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.tz_localize(None).dt.date





tweet_df['adjusted_score'] = np.where(
    tweet_df['sentiment'] == 'negative',
    tweet_df['score'] * -1,                # If Negative
    np.where(
        tweet_df['sentiment'] == 'positive',
        tweet_df['score'] * 1,             # If Positive
        tweet_df['score'] * 0              # If Neutral (default)
    )
)

results = []
for day in tweet_df['Date'].unique():
    daily_df = tweet_df[tweet_df['Date'] == day]
    results.append({
        'Date': day,
        'Total_Sentiment': daily_df['adjusted_score'].sum(),
        'Average_Sentiment': daily_df['adjusted_score'].mean(),
        'Total_Tweets': len(daily_df)
    })

# Convert to DataFrame
result_df = pd.DataFrame(results)

merged_df = pd.merge(result_df, stock_df, on='Date', how='outer')
merged_df = merged_df.dropna(subset=['Open', 'Close'])
print("Merged DataFrame:")
print(merged_df.head(10))

merged_df.to_csv("data/processed/merged_df.csv", index=False);