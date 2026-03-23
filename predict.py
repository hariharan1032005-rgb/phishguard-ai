<<<<<<< HEAD
import joblib
from feature_extraction import extract_features

model = joblib.load("phishguard_model.pkl")

def predict_url(url):

    features = extract_features(url)

    prediction = model.predict([features])[0]

    probability = model.predict_proba([features])[0][1]

    return prediction, probability, features
=======
import joblib
from feature_extraction import extract_features

# Load model
model = joblib.load("model.pkl")   # 🔥 make sure file name matches

def predict_url(url):
    try:
        features = extract_features(url)

        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1]

        return prediction, probability, features

    except Exception as e:
        return 0, 0.0, [0,0,0,0,0,0]
>>>>>>> 3292d845d44f5701216bdfb571c1a9aa61eb0d04
