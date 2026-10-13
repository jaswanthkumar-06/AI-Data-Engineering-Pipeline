import re


POSITIVE_WORDS = {
    "excellent",
    "amazing",
    "great",
    "good",
    "delicious",
    "fresh",
    "fast",
    "enjoyed",
    "love",
    "perfect",
    "tasty",
    "friendly",
    "wonderful",
    "awesome",
    "quick",
}

NEGATIVE_WORDS = {
    "cold",
    "late",
    "poor",
    "bad",
    "terrible",
    "slow",
    "worst",
    "unhappy",
    "disappointed",
    "rude",
    "awful",
    "expensive",
    "delay",
    "missing",
    "wrong",
}


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def analyze_sentiment(text):
    cleaned_text = clean_text(text)
    words = set(cleaned_text.split())

    positive_count = len(words.intersection(POSITIVE_WORDS))
    negative_count = len(words.intersection(NEGATIVE_WORDS))

    score = positive_count - negative_count

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, score