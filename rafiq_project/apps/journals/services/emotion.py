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

LABEL_MAP = {0: 'sadness', 1: 'joy', 2: 'love', 3: 'anger', 4: 'fear', 5: 'surprise'}

def analyze_emotion(text):
    if not text or not text.strip() or model is None:
        return {}, DEFAULT_EMOTION

    try:

        lang = detect(text)
        if lang != 'en':
            return {}, "Unsupported Language"

        sequence = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequence, maxlen=150, padding='post')
        
        prediction = model.predict(padded)[0]
        
        emotions_dict = {LABEL_MAP[i]: float(prediction[i]) for i in range(len(LABEL_MAP))}
        dominant_emotion = LABEL_MAP[np.argmax(prediction)]

        return emotions_dict, dominant_emotion

    except LangDetectException:
        return {}, "Unsupported Language"
    except Exception as e:
        print(f"AI Local Analysis Error: {e}")
        return {}, DEFAULT_EMOTION