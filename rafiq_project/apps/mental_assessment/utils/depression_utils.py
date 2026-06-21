import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join("ml_models", "depression_model.pkl")
SCALER_PATH = os.path.join("ml_models", "scaler.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print("Error loading depression model:", e)
    model = None

try:
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print("Error loading scaler:", e)
    scaler = None

FEATURE_ORDER = [
    "gender",
    "age",
    "work_pressure",
    "job_satisfaction",
    "sleep_duration",
    "dietary_habits",
    "suicidal_thoughts",
    "work_hours",
    "financial_stress",
    "family_history"
]

FEATURES_NAME = [
    "Gender",
    "Age",
    "Work Pressure",
    "Job Satisfaction",
    "Sleep Duration",
    "Dietary Habits",
    "Have you ever had suicidal thoughts ?",
    "Work Hours",
    "Financial Stress",
    "Family History of Mental Illness"
]

NUMERIC_COLS = ['Age', 'Work Pressure', 'Job Satisfaction', 'Work Hours', 'Financial Stress']

INFO = {
    "Yes": {
        "title": "Your Mind Needs Extra Care Right Now",
        "subtitle": "Your results indicate signs of depression",
        "description": "You may be experiencing persistent sadness, low energy, or a loss of interest in activities you once enjoyed.",
        "bottom_text": "Remember, seeking help is a sign of strength. Taking one small step today can make a positive difference in your journey toward feeling better.",

    },
    "No": {
        "title": "Your Mind Feels Calm and Balanced",
        "subtitle": "You seem to be in a peaceful mental state",
        "description": "You handle situations calmly and give yourself time to think and breathe. Keep nurturing that balance — it’s your real strength.",
        "bottom_text": "Maintain your relaxation routine and remember – peace of mind needs care, just like your body.",
    }
}

def predict_depression(validated_data: dict):
    if model is None or scaler is None:
        return {
            "depression": "Unknown",
            "title": "Model error", 
            "subtitle": "Configuration",          
            "description": "Model or scaler is not loaded.",
            "bottom_text": ""
        }

    ordered_answers = [validated_data[key] for key in FEATURE_ORDER]
    df = pd.DataFrame([ordered_answers], columns=FEATURES_NAME)

    try:
        df[NUMERIC_COLS] = scaler.transform(df[NUMERIC_COLS])
        pred_num = model.predict(df)[0]
    except Exception as e:
        return {
            "depression": "Unknown",
            "title": "Prediction Error",
            "subtitle": "Error occurs during inference", "description": f"Prediction error: {e}",
            "bottom_text": ""
        }

    pred_label = "Yes" if pred_num == 1 else "No"
    target_info = INFO[pred_label]

    return {
        "depression": pred_label,
        "title": target_info["title"],
        "subtitle": target_info["subtitle"],
        "description": target_info["description"],
        "bottom_text": target_info["bottom_text"],
    }
