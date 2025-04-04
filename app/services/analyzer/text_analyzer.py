from app.services.sentiment.analyzer import detect_sentiment
from app.services.highlighter.matcher import check_highlight


def analyze_text(text: str, highlight: str):
    sentiment = detect_sentiment(text)
    highlight_found, count = check_highlight(text, highlight)

    return {
        "sentiment": sentiment,
        "highlight_found": highlight_found,
        "highlight_count": count
    }
