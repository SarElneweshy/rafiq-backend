import os
import pickle
import numpy as np
import tensorflow as tf
from django.conf import settings
from keras.preprocessing.sequence import pad_sequences
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'journal_model.keras',)
TOKENIZER_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'tokenizer.pkl')

try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    with open(TOKENIZER_PATH, 'rb') as f:
        tokenizer = pickle.load(f)
except Exception as e:
    print(f"Error Loading ML Files: {e}")
    model = None

DEFAULT_EMOTION = "neutral"

LABEL_MAP = {0: 'Sadness', 1: 'Joy', 2: 'Love', 3: 'Anger', 4: 'Fear', 5: 'Surprise'}

def analyze_emotion(text):
    if not text or not text.strip() or model is None:
        return {}, DEFAULT_EMOTION

    try:

        lang = detect(text)
        if lang != 'en':
            return {}, "Unsupported Language"

        words = text.split()
        chunk_size = 120 
        chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        
        all_chunk_predictions = []

        for chunk in chunks:
            sequence = tokenizer.texts_to_sequences([chunk])

            padded = pad_sequences(sequence, maxlen=150, padding='post', truncating='post')

            prediction = model.predict(padded, verbose=0)[0]
            all_chunk_predictions.append(prediction)

        final_prediction = np.mean(all_chunk_predictions, axis=0)
        
        emotions_dict = {LABEL_MAP[i]: float(final_prediction[i]) for i in range(len(LABEL_MAP))}
        dominant_emotion = LABEL_MAP[np.argmax(final_prediction)]

        return emotions_dict, dominant_emotion

    except LangDetectException:
        return {}, "Unsupported Language"
    except Exception as e:
        print(f"AI Local Analysis Error: {e}")
        return {}, DEFAULT_EMOTION