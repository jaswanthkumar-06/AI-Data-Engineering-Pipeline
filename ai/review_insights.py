import os
import pandas as pd

from sentiment_analysis import analyze_sentiment


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "reviews.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "review_sentiment.csv"
)


def main():

    print("Loading reviews...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Reviews loaded: {len(df)}")

    results = df["review_text"].apply(analyze_sentiment)

    df["sentiment"] = results.apply(lambda x: x[0])
    df["sentiment_score"] = results.apply(lambda x: x[1])

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Sentiment analysis completed.")
    print(f"Output saved to: {OUTPUT_FILE}")

    print("\nSentiment distribution:")
    print(df["sentiment"].value_counts())


if __name__ == "__main__":
    main()