import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join("ml_models", "depression_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print("Error loading depression model:", e)
    model = None


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
  # in ml model #
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

INFO = {
    "Yes": {
        "description": "You may be showing signs of depression.",
        "suggestions": ["Try journaling", 
                "Talk to a mental health professional","Do light exercise", "Follow a daily routine"],
        "video": "https://www.youtube.com/watch?v=qKcRUOWYQ9w"
        
    },
    "No": {
        "description": "Your mind feels calm and balanced. You seem to be in a peaceful mental state. You handle situations calmly and give yourself time to think and breathe. Keep nurturing that balance — it’s your real strength. Maintain your relaxation routine and remember — peace of mind needs care, just like your body.",
        "suggestions": ["Keep up the good work", "Maintain a healthy lifestyle"],
        "video": ""
    }
}

def predict_depression(validated_data: dict):
    """
    validated_data: dict coming from serializer
    """

    if model is None:
        return {
            "depression": "Unknown",
            "description": "Model is not loaded.",
            "suggestions": [],
            "video": ""
        }

    # Arrange answers in the order expected by the model #
    ordered_answers = [validated_data[key] for key in FEATURE_ORDER]

    df = pd.DataFrame([ordered_answers], columns=FEATURES_NAME)

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
