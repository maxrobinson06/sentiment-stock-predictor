import re
import pandas as pd


def clean_tweet_text(text: str) -> str:
    """
    Clean the tweet text by removing URLs, mentions, hashtags, and special characters.

    Args:
        text (str): The raw tweet text.

    Returns:
        str: The cleaned tweet text.
    """
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'#', '', text)  # Remove hashtags
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters
    text = text.strip()  # Remove leading/trailing whitespace
    return text

def clean_tweet_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the tweet DataFrame by applying text cleaning to the 'Tweet' column.

    Args:
        df (pd.DataFrame): The DataFrame containing tweet data.

    Returns:
        pd.DataFrame: The cleaned DataFrame with a 'cleaned_text' column.
    """
    df = df.copy()


    df['cleaned_text'] = df['Tweet'].apply(clean_tweet_text)
    return df
