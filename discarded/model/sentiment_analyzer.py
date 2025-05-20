from transformers import pipeline

# Load FinBERT for financial sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

def analyze_sentiment(news_list):
    """
    Analyze the sentiment of a list of news headlines/texts.
    Returns: 'positive', 'neutral', or 'negative'
    """
    if not news_list:
        return 'neutral'
    combined = " ".join(news_list)
    result = sentiment_pipeline(combined)[0]
    return result['label'].lower()  # 'positive', 'neutral', 'negative'

def sentiment_score(news_list):
    """
    Returns a sentiment score: +1 for positive, 0 for neutral, -1 for negative.
    """
    sentiment = analyze_sentiment(news_list)
    if sentiment == 'positive':
        return 1
    elif sentiment == 'negative':
        return -1
    return 0
