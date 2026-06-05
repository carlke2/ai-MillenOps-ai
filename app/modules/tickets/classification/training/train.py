import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

DATA_PATH = "app/modules/tickets/classification/training/datasets/tickets.csv"
MODEL_PATH = "app/modules/tickets/classification/models/ticket_classifier.joblib"


def combine_text(row):
    return f"""
    title: {row.get('title', '')}
    description: {row.get('description', '')}
    room: {row.get('roomName', '')}
    department: {row.get('department', '')}
    bookingLinked: {row.get('bookingLinked', '')}
    """


def main():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["finalCategory"])

    if len(df) < 20:
        print("Not enough real training data yet. Use baseline-rules-v1 for now.")
        print(f"Current sample size: {len(df)}")
        return

    df["text"] = df.apply(combine_text, axis=1)

    X = df["text"]
    y = df["finalCategory"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y if y.nunique() > 1 else None
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=5000
        )),
        ("classifier", LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ))
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Classification Report:")
    print(classification_report(y_test, predictions))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
