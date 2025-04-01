import joblib
import numpy as np
from sklearn.base import BaseEstimator

# Load the pre-trained vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def score(text: str, model: BaseEstimator, threshold: float) -> tuple[bool, float]:
    """
    Scores the input text using the trained model.

    Parameters:
    - text (str): Input text to be classified
    - model (sklearn.base.BaseEstimator): Trained ML model
    - threshold (float): Decision threshold

    Returns:
    - prediction (bool): 1 if spam, 0 if not spam
    - propensity (float): Probability score from the model
    """
    if not isinstance(text, str) or not isinstance(threshold, (int, float)):
        raise ValueError("Invalid input types.")

    # Ensure threshold is between 0 and 1
    threshold = max(0, min(1, threshold))

    # Transform input using the pre-loaded vectorizer
    text_tfidf = vectorizer.transform([text])  # Convert input text into TF-IDF format
    print(text_tfidf)

    # Get probability score for class 1 (spam)
    prediction_proba = model.predict_proba(text_tfidf)[0, 1]
    print(prediction_proba)

    # Apply threshold to make a classification decision
    prediction = prediction_proba >= threshold

    return bool(prediction), float(prediction_proba)