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

# 1. Moving Averages

merged_df = pd.merge(result_df, stock_df, on='Date', how='outer')
merged_df = merged_df.dropna(subset=['Open', 'Close'])

# Adding new metrics for analyisis

# 1. Moving Averages: The average of a metric over a rolling 30-day window, recalculated for each day.

merged_df['30D_MA_Price'] = merged_df['Close'].rolling(window=30, min_periods=1).mean()
merged_df['30D_MA_Sentiment'] = merged_df['Average_Sentiment'].rolling(window=30, min_periods=1).mean()

# 2. Volume Analysis: Raw number of shares traded daily.
merged_df['30D_MA_Volume'] = merged_df['Volume'].rolling(window=30, min_periods=1).mean()
merged_df['Volume_Ratio'] = merged_df['Volume'] / merged_df['30D_MA_Volume']  # Current vs average volume

# 3. Volatility Metrics: Annualized standard deviation of daily returns over 30 days.
merged_df['Daily_Return'] = merged_df['Close'].pct_change()
merged_df['30D_Volatility'] = merged_df['Daily_Return'].rolling(window=30).std() * np.sqrt(252)

merged_df['7D_MA_Sentiment'] = merged_df['Average_Sentiment'].rolling(window=7, min_periods=1).mean()
# Compare raw vs. smoothed sentiment

# Plot to visualize noise reduction
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.plot(merged_df['Date'], merged_df['Average_Sentiment'], alpha=0.3, label='Raw')
plt.plot(merged_df['Date'], merged_df['30D_MA_Sentiment'], color='red', label='30D MA')
plt.plot(merged_df['Date'], merged_df['7D_MA_Sentiment'], color='blue', label='7D MA')
plt.legend()
plt.show()

print("Merged DataFrame:")
print(merged_df[['Date', 'Close', '30D_MA_Price', 'Average_Sentiment', '30D_MA_Sentiment', 
                'Volume', '30D_MA_Volume', '30D_Volatility']].tail(10))

merged_df.to_csv("data/processed/merged_df.csv", index=False)



# Research
     # 30 Day Moving Average - Stock Price
          # Sentiment Link: Confirms if sentiment trends align with stock price trends.
          # Trading Insights: Filters out noise from daily fluctuations, revealing underlying trends.


     # 30 Day Moving Average - Sentiment
          # Sentiment Link: Identifies sustained mood shifts, not just daily outliers.
          # Trading Insights: Avoids overreacting to daily sentiment spikes, focusing on longer-term trends.


     # Volume Ratio
          # Sentiment Link: High volume with high sentiment may indicate strong market interest.
          # Trading Insights: Validate whether sentiment moves are backed by trading activity.

     # 30 Day Moving Volatility
          # Sentiment Link: Sentiment swings during high volatility may have larger price impacts.
          # Trading Insights: Adjust position sizes during volatile periods.

#"Microsoft's strong Q1 FY2022 earnings release on October 26, 2021, likely fueled the sustained sentiment surge observed in November 2021. Key drivers included:

#Record Financial Performance:

#Revenue grew 22% YoY to $45.3B, with net income up 48% ($20.5B).

#Azure/cloud growth and commercial product demand highlighted execution strength.

#Windows 11 Momentum:

#The October 2021 launch saw rapid adoption, with November sentiment reflecting positive user/developer feedback.

#Forward Guidance:

#Upbeat forecasts for cloud and productivity tools signaled long-term confidence.

#This combination of beat-and-raise earnings + product cycle tailwinds created a bullish sentiment foundation that persisted through November, as seen in the 30D MA’s upward trend."**