from textblob import TextBlob


def detect_sentiment(text: str) -> str:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.4:
        return "Positivo"
    elif 0.1 < polarity <= 0.4:
        return "Neutro Positivo"
    elif -0.1 <= polarity <= 0.1:
        return "Neutro"
    elif -0.4 <= polarity < -0.1:
        return "Neutro Negativo"
    else:
        return "Negativo"
