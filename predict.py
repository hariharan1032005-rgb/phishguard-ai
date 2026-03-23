import joblib
import os
from feature_extraction import extract_features

# Load model safely
MODEL_FILE = "phishguard_model.pkl"

if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)
else:
    model = None

def predict_url(url):
    if model is None:
        return 0, 0.0, [0,0,0,0,0,0]
    
    try:
        features = extract_features(url)
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1]
        return prediction, probability, features
    except:
        return 0, 0.5, [0,0,0,0,0,0]
