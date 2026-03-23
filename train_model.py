<<<<<<< HEAD
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("phishing_dataset.csv")

X = data.drop("label", axis=1)
y = data["label"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "phishguard_model.pkl")

=======
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("phishing_dataset.csv")

X = data.drop("label", axis=1)
y = data["label"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "phishguard_model.pkl")

>>>>>>> 3292d845d44f5701216bdfb571c1a9aa61eb0d04
print("Model trained successfully")