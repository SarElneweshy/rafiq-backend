from flask import Flask, request, jsonify
from model_utils import predict_emotion

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if "text" not in data:
        return jsonify({"error":"text required"}),400

    text = data["text"]
    try:
        emotions, dominant = predict_emotion(text)
        return jsonify({
            "emotions": emotions,
            "dominant_emotion": dominant
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)