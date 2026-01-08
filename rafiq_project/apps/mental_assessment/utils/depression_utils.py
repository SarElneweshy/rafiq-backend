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
        "description": "You may be showing signs of depression.",
        "suggestions": ["Try journaling", "Talk to a mental health professional",
                        "Do light exercise", "Follow a daily routine"],
        "video": "https://www.youtube.com/watch?v=qKcRUOWYQ9w"
    },
    "No": {
        "description": "Your mind feels calm and balanced. Keep nurturing that balance — it’s your real strength.",
        "suggestions": ["Keep up the good work", "Maintain a healthy lifestyle"],
        "video": ""
    }
}

def predict_depression(validated_data: dict):
    if model is None or scaler is None:
        return {
            "depression": "Unknown",
            "description": "Model or scaler is not loaded.",
            "suggestions": [],
            "video": ""
        }

    ordered_answers = [validated_data[key] for key in FEATURE_ORDER]
    df = pd.DataFrame([ordered_answers], columns=FEATURES_NAME)

    df[NUMERIC_COLS] = scaler.transform(df[NUMERIC_COLS])

    try:
        pred_num = model.predict(df)[0]
    except Exception as e:
        return {
            "depression": "Unknown",
            "description": f"Prediction error: {e}",
            "suggestions": [],
            "video": ""
        }

    pred_label = "Yes" if pred_num == 1 else "No"

    return {
        "depression": pred_label,
        "description": INFO[pred_label]["description"],
        "suggestions": INFO[pred_label]["suggestions"],
        "video": INFO[pred_label]["video"]
    }
