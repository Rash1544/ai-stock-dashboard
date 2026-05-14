import feedparser

positive_words = [
    "gain",
    "growth",
    "profit",
    "surge",
    "strong",
    "bullish",
    "up"
]

negative_words = [
    "loss",
    "drop",
    "fall",
    "bearish",
    "down",
    "weak",
    "crash"
]

def analyze_news_sentiment(stock_symbol):

    try:

        url = (
            f"https://news.google.com/rss/search?"
            f"q={stock_symbol}+stock"
        )

        feed = feedparser.parse(url)

        headlines = []

        sentiment_score = 0

        for entry in feed.entries[:5]:

            title = entry.title

            headlines.append(title)

            title_lower = title.lower()

            for word in positive_words:

                if word in title_lower:
                    sentiment_score += 1

            for word in negative_words:

                if word in title_lower:
                    sentiment_score -= 1

        # Final Sentiment
        if sentiment_score > 2:
            sentiment = "Positive"

        elif sentiment_score < -2:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "score": sentiment_score,
            "headlines": headlines
        }

    except Exception as e:

        return {
            "sentiment": "Unknown",
            "score": 0,
            "headlines": [str(e)]
        }