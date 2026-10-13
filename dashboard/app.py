
import os
import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

st.set_page_config(
    page_title="AI Food Delivery Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("AI Food Delivery Analytics")
st.caption("Python • scikit-learn • PostgreSQL • dbt • Streamlit")

DATA_FILE = "data/raw/reviews.csv"

@st.cache_data
def load_reviews(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

reviews = load_reviews(DATA_FILE)

if reviews.empty:
    st.error(f"No review data found at {DATA_FILE}. Check your project folder.")
    st.stop()

# Adapt common review-column names
text_candidates = ["review_text", "review", "comment", "text"]
label_candidates = ["sentiment", "sentiment_label", "label"]

text_col = next((c for c in text_candidates if c in reviews.columns), None)
label_col = next((c for c in label_candidates if c in reviews.columns), None)

if not text_col:
    st.error(f"Could not identify review text. Available columns: {list(reviews.columns)}")
    st.stop()

reviews[text_col] = reviews[text_col].fillna("").astype(str)
reviews = reviews[reviews[text_col].str.strip().ne("")].copy()

st.sidebar.header("Dashboard Filters")

if label_col:
    reviews[label_col] = reviews[label_col].fillna("Unknown").astype(str)
    selected_labels = st.sidebar.multiselect(
        "Sentiment",
        sorted(reviews[label_col].unique()),
        default=sorted(reviews[label_col].unique()),
    )
    filtered = reviews[reviews[label_col].isin(selected_labels)].copy()
else:
    filtered = reviews.copy()

col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews", f"{len(filtered):,}")
col2.metric("Unique Review Texts", f"{filtered[text_col].nunique():,}")
col3.metric("Available Columns", len(reviews.columns))

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Review Data Preview")
    st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)

with right:
    st.subheader("Sentiment Distribution")
    if label_col:
        counts = filtered[label_col].value_counts().rename_axis("Sentiment").reset_index(name="Reviews")
        fig = px.pie(counts, names="Sentiment", values="Reviews", hole=0.45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sentiment-label column found. Use the ML training section below.")

st.divider()
st.header("Machine Learning: Sentiment Classification")

if not label_col:
    st.warning(
        "The reviews CSV has no sentiment label column. "
        "Train the classifier using a dataset with known sentiment labels."
    )
else:
    model_data = reviews[
        reviews[text_col].str.strip().ne("")
        & reviews[label_col].notna()
    ].copy()

    if model_data[label_col].nunique() < 2:
        st.warning("At least two sentiment classes are required for classification.")
    elif model_data[label_col].value_counts().min() < 2:
        st.warning("Each class needs at least two examples for a stratified split.")
    else:
        if st.button("Train and evaluate scikit-learn model", type="primary"):
            with st.spinner("Training TF-IDF + Logistic Regression..."):
                X_train, X_test, y_train, y_test = train_test_split(
                    model_data[text_col],
                    model_data[label_col],
                    test_size=0.2,
                    random_state=42,
                    stratify=model_data[label_col],
                )

                model = Pipeline([
                    ("tfidf", TfidfVectorizer(
                        max_features=10000,
                        ngram_range=(1, 2),
                        stop_words="english",
                    )),
                    ("classifier", LogisticRegression(
                        max_iter=1000,
                        class_weight="balanced",
                    )),
                ])

                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)

            st.metric("Holdout Accuracy", f"{accuracy:.1%}")
            report = classification_report(
                y_test,
                predictions,
                output_dict=True,
                zero_division=0,
            )
            st.subheader("Classification Report")
            st.dataframe(
                pd.DataFrame(report).transpose().round(3),
                use_container_width=True,
            )

            st.session_state["sentiment_model"] = model

        st.subheader("Try a Review")
        review_input = st.text_area(
            "Enter review text",
            placeholder="Food arrived quickly and tasted excellent...",
        )

        if st.button("Predict sentiment"):
            model = st.session_state.get("sentiment_model")
            if model is None:
                st.warning("Train the model first.")
            elif not review_input.strip():
                st.warning("Enter some review text.")
            else:
                prediction = model.predict([review_input])[0]
                st.success(f"Predicted sentiment: {prediction}")

st.divider()
st.subheader("Dataset Quality Checks")

quality = pd.DataFrame({
    "Check": [
        "Total rows",
        "Duplicate rows",
        "Missing values",
        "Empty review texts",
    ],
    "Result": [
        len(reviews),
        int(reviews.duplicated().sum()),
        int(reviews.isna().sum().sum()),
        int(reviews[text_col].str.strip().eq("").sum()),
    ],
})

st.dataframe(quality, use_container_width=True, hide_index=True)
st.download_button(
    "Download filtered reviews",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_reviews.csv",
    mime="text/csv",
)
