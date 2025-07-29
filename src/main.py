from data_loader import load_tweet_data, load_stock_data
from tweet_cleaner import clean_tweet_df
from get_sentiment_scores import get_sentiment_scores

df = load_tweet_data();
df_msft = df[df['Stock Name'] == 'MSFT'];
cleaned_df = clean_tweet_df(df_msft);

df = get_sentiment_scores(cleaned_df);
df.to_csv("data/processed/MSFT_tweets.csv", index=False);
