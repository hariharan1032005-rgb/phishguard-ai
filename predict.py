import joblib
from feature_extraction import extract_features

model = joblib.load("phishguard_model.pkl")

def predict_url(url):

    features = extract_features(url)

    prediction = model.predict([features])[0]

    probability = model.predict_proba([features])[0][1]

    return prediction, probability, features