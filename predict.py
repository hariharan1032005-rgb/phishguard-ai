import joblib
import os
from feature_extraction import extract_features

# 1. Determine the correct model name
# Check if you named your file 'phishguard_model.pkl' or 'model.pkl' 
# and update the line below to match!
MODEL_PATH = "phishguard_model.pkl" 

# Load model safely
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    # This helps you debug if the file is missing in GitHub
    model = None
    print(f"ERROR: {MODEL_PATH} not found!")

def predict_url(url):
    if model is None:
        return 0, 0.0, [0, 0, 0, 0, 0, 0]
        
    try:
        # Extract features using your custom script
        features = extract_features(url)

        # Get prediction (0 for Legitimate, 1 for Phishing)
        prediction = model.predict([features])[0]
        
        # Get the probability of it being phishing (index 1)
        probability = model.predict_proba([features])[0][1]

        return prediction, probability, features

    except Exception as e:
        print(f"Prediction Error: {e}")
        # Return safe defaults if extraction fails
        return 0, 0.0, [0, 0, 0, 0, 0, 0]
