# Load the FinBERT model and tokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
print("FinBERT model and tokenizer loaded successfully.")

def get_sentiment_scores(df):
    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    sentiments = sentiment_pipeline(df["cleaned_text"].tolist())
    df["sentiment"] = [s["label"] for s in sentiments]
    df["score"] = [s["score"] for s in sentiments]
    return df