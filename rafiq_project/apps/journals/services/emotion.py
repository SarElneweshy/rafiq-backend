import requests
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
DetectorFactory.seed = 0

AI_URL = "http://emotion_model:5000/predict"

DEFAULT_EMOTION = "neutral"


def analyze_emotion(text):

    if not text.strip():
        return [], DEFAULT_EMOTION

    try:
        lang = detect(text)
        if lang != 'en':
            return [], "Unsupported Language"
        res = requests.post(
            AI_URL,
            json={"text": text},
            timeout=10
        )

        if res.status_code != 200:
            return [], DEFAULT_EMOTION

        data = res.json()
        return data["emotions"], data["dominant_emotion"]

    except LangDetectException:
        return [], "Unsupported Language"
    except Exception as e:
        print("AI ERROR:", e)
        return [], DEFAULT_EMOTION