import tensorflow as tf
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAXLEN = 150

labelMap = {
0:'Sadness',
1:'Joy',
2:'Love',
3:'Anger',
4:'Fear',
5:'Surprise'
}

try:
    model = tf.keras.models.load_model("journal_model.keras")
    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    print("AI MODEL READY")
except Exception as e:
    print(f"CRITICAL ERROR LOADING MODEL: {e}")


def preprocess(text):

    seq = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(
        seq,
        maxlen=MAXLEN,
        padding="post",
        truncating="post"
    )

    return padded


def predict_emotion(text):

    processed = preprocess(text)

    prediction = model.predict(processed)[0]

    emotions = []

    for i,score in enumerate(prediction):

        emotions.append({
            "label": labelMap[i],
            "score": float(score)
        })

    dominant = labelMap[int(np.argmax(prediction))]

    return emotions, dominant