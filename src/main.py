from data_loader import load_tweet_data, load_stock_data
from tweet_cleaner import clean_tweet_df

df = load_tweet_data();
df_msft = df[df['Stock Name'] == 'MSFT'];
cleaned_df = clean_tweet_df(df_msft);

cleaned_df.to_csv("data/processed/MSFT_tweets.csv", index=False)
print("Cleaned Tweets Data:")
print(cleaned_df)