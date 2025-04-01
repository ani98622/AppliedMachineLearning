from flask import Flask, request, jsonify
import joblib

# Load the trained model and vectorizer
model = joblib.load("Support_Vector_Machine.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score_text():
    data = request.get_json()
    text = data.get("text", "")

    if not isinstance(text, str) or text.strip() == "":
        return jsonify({"error": "Invalid input. Please provide a valid text."}), 400

    # Transform text using the vectorizer
    text_vectorized = vectorizer.transform([text])

    # Get probability score
    prediction_proba = model.predict_proba(text_vectorized)[0, 1]
    
    # Apply threshold (0.5 by default)
    threshold = 0.5
    prediction = int(prediction_proba >= threshold)

    return jsonify({"prediction": prediction, "propensity": prediction_proba})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
