import pandas as pd

def load_tweet_data(path ="data/raw/stock_tweets.csv") -> pd.DataFrame:
    """
    Load tweet data from a CSV file.

    Args:
        path (str): The file path to the CSV containing tweet data.

    Returns:
        pd.DataFrame: A DataFrame containing the tweet data.
    """
    return pd.read_csv(path)

def load_stock_data(path ="data/raw/MSFT_prices.csv") -> pd.DataFrame:
    """
    Load stock price data from a CSV file.

    Args:
        path (str): The file path to the CSV containing stock price data.

    Returns:
        pd.DataFrame: A DataFrame containing the stock price data.
    """
    return pd.read_csv(path)

if __name__ == "__main__":
    # Example usage
    tweets = load_tweet_data()
    stocks = load_stock_data()
    
    print("Tweets Data:")
    print(tweets.head())
    
    print("\nStock Prices Data:")
    print(stocks.head())