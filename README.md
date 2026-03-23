# 🛡️ PhishGuard AI – Advanced Phishing Detection System

PhishGuard AI is an intelligent cybersecurity tool that uses **Machine Learning** to identify phishing websites in real-time. It analyzes URL structures, checks against blacklists, and provides a "Threat Score" to help users stay safe online.

## 🚀 Features
- **AI-Powered Analysis:** Uses a trained Random Forest model to predict malicious intent.
- **Heuristic Scanning:** Checks for suspicious keywords (e.g., "login", "verify", "secure").
- **Live Server Intel:** Identifies the physical location and IP address of the hosting server.
- **Visual Analytics:** Real-time risk gauges and feature-contribution bar charts.
- **Safe Sandbox:** Preview suspicious sites through a secure iframe without risking infection.

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Python)
- **Machine Learning:** Scikit-Learn, Joblib
- **Data Visualization:** Plotly, Pandas
- **APIs:** Google DNS, IP-API

## 📂 Project Structure
- `app.py`: The main web interface and UI logic.
- `predict.py`: Handles the model loading and prediction logic.
- `feature_extraction.py`: Processes raw URLs into 6 key security features.
- `phishguard_model.pkl`: The pre-trained AI brain.
- `requirements.txt`: Necessary Python libraries for deployment.

## 🔧 Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/PhishGuard-AI.git](https://github.com/YOUR_USERNAME/PhishGuard-AI.git)
   Install dependencies:
   
pip install -r requirements.txt
Run the app:
Bash
streamlit run app.py

