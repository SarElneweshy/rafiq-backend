import os
import numpy as np
import joblib

MODEL_PATH = os.path.join('ml_models', 'general_RMmodel.pkl')

try:
    model = joblib.load(MODEL_PATH)
    
except Exception as e:
    print("Error loading general model:", e)
    model = None

DISORDERS = [
    'Anxiety', 'Attention-Deficit/Hyperactivity Disorder (ADHD)', 'Autism Spectrum Disorder (ASD)',
    'Bipolar', 'Eating Disorder', 'Loneliness', 'Major Depressive Disorder (MDD)',
    'Obsessive-Compulsive Disorder (OCD)', 'Persistent Depressive Disorder (PDD)',
    'Post-Traumatic Stress Disorder (PTSD)', 'Psychotic Depression', 'Sleeping Disorder'
]

FEATURES_NAME = [
    'ag+1:629e', 'feeling.nervous', 'panic', 'breathing.rapidly', 'sweating',
    'trouble.in.concentration', 'having.trouble.in.sleeping', 'having.trouble.with.work',
    'hopelessness', 'anger', 'over.react', 'change.in.eating', 'suicidal.thought',
    'feeling.tired', 'close.friend', 'social.media.addiction', 'weight.gain',
    'introvert', 'popping.up.stressful.memory', 'having.nightmares',
    'avoids.people.or.activities', 'feeling.negative', 'trouble.concentrating',
    'blamming.yourself', 'hallucinations', 'repetitive.behaviour',
    'seasonally', 'increased.energy'
]


INFO = {
    "Major Depressive Disorder (MDD)": {
        "title": "You may be experiencing symptoms of Depression",
        "description": "This test suggests that you may have signs of depression. It’s not a diagnosis, but it can help you understand what you’re going through.",
        "suggestions": ["Try journaling", "Do light exercise", "Follow a daily routine"],
        "video": "https://www.youtube.com/watch?v=inpok4MKVLM"
                },
    "Autism Spectrum Disorder (ASD)": {
        "title": "You may be showing signs of Autism Spectrum Disorder",
        "description": "This test suggests that you may have challenges in social communication or interaction patterns. It’s not a diagnosis, but it provides helpful insights.",
        "suggestions": ["Follow structured activities", "Reduce screen time", "Use positive reinforcement"],
        "video": "https://youtu.be/4Talws29mys?si=Ec6dniPHrLkXwwkK"
                },
    "Loneliness": {
        "title": "You may be experiencing symptoms of Loneliness",
        "description": "This test suggests that you may be experiencing social disconnection. It’s not a diagnosis, but it encourages reaching out and finding community support.",
        "suggestions": ["Reach out to old friends", "Join a community", "Volunteer regularly"],
        "video": "https://youtu.be/GckT5n9Ik1s"
                },
    "Bipolar": {
        "title": "You may be experiencing mood fluctuations related to Bipolar",
        "description": "This test suggests that you may experience mood swings between high energy and sadness. It’s not a diagnosis, but it helps track your emotional health.",
        "suggestions": ["Keep a sleep routine", "Track your moods", "Avoid stress triggers"],
        "video": "https://www.youtube.com/watch?v=inpok4MKVLM"
                },
    "Anxiety": {
        "title": "You may be experiencing symptoms of Anxiety",
        "description": "This test suggests that you may have signs of anxiety. It’s not a diagnosis, but it can help you understand what you’re going through.",
        "suggestions": ["Try deep breathing", "Practice mindfulness", "Limit caffeine intake"],
        "video": "https://youtu.be/SNqYG95j_UQ"
                },
    "Post-Traumatic Stress Disorder (PTSD)": {
        "title": "You may be experiencing symptoms of PTSD",
        "description": "This test suggests that you may experience flashbacks, nightmares, or anxiety from past trauma. It’s not a diagnosis, but recognizes your emotional struggles.",
        "suggestions": ["Try grounding techniques", "Seek therapy", "Practice mindfulness"],
        "video": "https://www.youtube.com/watch?v=VDLfVwMSbJ8"
                },
    "Sleeping Disorder": {
        "title": "You may be experiencing symptoms of a Sleeping Disorder",
        "description": "This test suggests that you may have difficulty maintaining sleep quality. It’s not a diagnosis, but helps target areas for sleep hygiene improvement.",
        "suggestions": ["Keep consistent sleep hours", "Avoid screens before bed", "Create a calm bedtime routine"],
        "video": "https://youtu.be/ywTaRqSbQpw"
                },
    "Psychotic Depression": {
        "title": "You may be experiencing symptoms of Psychotic Depression",
        "description": "This test suggests that you may experience depressive thoughts with intense delusional ideas. It’s not a diagnosis, but a sign to monitor your health.",
        "suggestions": ["Seek professional therapy", "Follow a stable routine", "Reduce stress exposure"],
        "video": "https://www.youtube.com/watch?v=qKcRUOWYQ9w"
                },
    "Eating Disorder": {
        "title": "You may be experiencing signs of an Eating Disorder",
        "description": "This test suggests that you may have an unhealthy relationship with food or body image. It’s not a diagnosis, but it can help guide your self-care.",
        "suggestions": ["Eat balanced meals", "Avoid comparison", "Talk to a counselor"],
        "video": "https://www.youtube.com/watch?v=LiUnFJ8P4gM"
                },
    "Attention-Deficit/Hyperactivity Disorder (ADHD)": {
        "title": "You may be experiencing symptoms of ADHD",
        "description": "This test suggests that you may have signs of attention deficit or hyperactivity. It’s not a diagnosis, but it can help you understand your focus patterns.",
        "suggestions": ["Break tasks into parts", "Take short breaks", "Use focus exercises"],
        "video": "https://youtu.be/rTIv5X8Bo1w"
                },
    "Persistent Depressive Disorder (PDD)": {
        "title": "You may be experiencing signs of Persistent Depressive Disorder",
        "description": "This test suggests that you may experience long-term mild depression with low energy. It’s not a diagnosis, but highlights areas for regular care.",
        "suggestions": ["Follow a daily plan", "Set small goals", "Engage in enjoyable activities"],
        "video": "https://www.youtube.com/watch?v=LiUnFJ8P4gM"
                },
    "Obsessive-Compulsive Disorder (OCD)": {
        "title": "You may be experiencing symptoms of OCD",
        "description": "This test suggests that you may experience repetitive thoughts or actions. It’s not a diagnosis, but it helps pinpoint stress patterns.",
        "suggestions": ["Practice CBT techniques", "Avoid seeking reassurance", "Stick to a routine"],
        "video": "https://www.youtube.com/watch?v=pxWOpGm4d7U"
                    
                }
}

def predict_disorder(answers_numeric):
    if model is None:
        return {
            "predicted_disorder": "Unknown",
            "title": "Model not loaded",
            "description": "Please check the model configuration.",
            "suggestions": [],
            "video": ""
        }
    features = np.array([answers_numeric], dtype=float)
    pred_index = model.predict(features)[0]  
    predicted_disorder = DISORDERS[pred_index]
    result = INFO.get(predicted_disorder, {
        "title": f"Results for {predicted_disorder}", 
        "description": "No clear match found.", 
        "suggestions": [], 
        "video": ""})
    return {
        "predicted_disorder": predicted_disorder,
        "title": result["title"],
        "description": result["description"],
        "suggestions": result["suggestions"],
        "video": result["video"]
    }
