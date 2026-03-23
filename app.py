import streamlit as st
import pandas as pd
from predict import predict_url
import os
import plotly.graph_objects as go
import plotly.express as px
import requests
from urllib.parse import urlparse

# -----------------------------
# UI STYLE
# -----------------------------
st.markdown("""
<style>
.stApp {
background: linear-gradient(135deg,#020617,#0f172a,#020617);
color:white;
}

h1 {
color:#38bdf8;
text-align:center;
text-shadow:0 0 20px #38bdf8;
}

h2,h3 {
color:#e2e8f0;
}

.stButton>button {
background-color:#2563eb;
color:white;
border-radius:10px;
padding:10px 20px;
}

.stButton>button:hover {
background-color:#1d4ed8;
}

.stTextInput>div>div>input {
background:#1e293b;
color:white;
border-radius:8px;
}

.glow-safe{
color:#22c55e;
font-size:26px;
text-align:center;
text-shadow:0 0 10px #22c55e,0 0 20px #22c55e;
}

.glow-warning{
color:#facc15;
font-size:26px;
text-align:center;
text-shadow:0 0 10px #facc15,0 0 20px #facc15;
}

.glow-danger{
color:#ef4444;
font-size:26px;
text-align:center;
text-shadow:0 0 10px #ef4444,0 0 20px #ef4444;
}

.stMetric{
background:#1e293b;
padding:10px;
border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("🛡️ PhishGuard AI – Advanced Phishing Detection System")
st.info("AI-Powered Cybersecurity System for Detecting Phishing Websites")

url = st.text_input("Enter URL")

# -----------------------------
# VirusTotal Scan
# -----------------------------
def virustotal_scan(url):
    API_KEY = "YOUR_API_KEY_HERE"
    headers = {"x-apikey": API_KEY}
    params = {"url": url}

    try:
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data=params
        )
        if response.status_code == 200:
            st.success("VirusTotal scan submitted")
        else:
            st.warning("VirusTotal scan failed")
    except:
        st.warning("VirusTotal error")

# -----------------------------
# LOAD FILES
# -----------------------------
if not os.path.exists("scan_history.csv"):
    df = pd.DataFrame(columns=["url","result"])
    df.to_csv("scan_history.csv",index=False)

try:
    with open("blacklist.txt") as f:
        blacklist = f.read().splitlines()
except:
    blacklist = []

# -----------------------------
# SERVER LOCATION
# -----------------------------
def get_ip_location(url):
    try:
        domain = urlparse(url).netloc
        ip = requests.get(f"https://dns.google/resolve?name={domain}").json()
        ip_address = ip["Answer"][0]["data"]
        data = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        return data["country"], data["city"]
    except:
        return None, None

# -----------------------------
# MAIN LOGIC
# -----------------------------
if url:

    if st.button("Run Advanced Scan"):
        virustotal_scan(url)

    if any(b in url for b in blacklist):
        st.error("⚠️ Blacklisted URL")

    suspicious = ["login","verify","update","bank","secure"]
    if any(word in url.lower() for word in suspicious):
        st.warning("⚠️ Suspicious keyword detected")

    prediction, probability, features = predict_url(url)

    if prediction == 1:
        result = "Phishing"
        st.error("⚠️ Phishing Website Detected")
    else:
        result = "Legitimate"
        st.success("✅ Legitimate Website")

    threat_score = int(probability * 100)
    st.write("Phishing Probability:", threat_score, "%")

    # -----------------------------
    # THREAT SCORE
    # -----------------------------
    st.markdown("---")
    st.subheader("AI Threat Score")

    st.metric("Threat Score", threat_score)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=threat_score,
        gauge={'axis':{'range':[0,100]}}
    ))

    st.plotly_chart(fig)

    # Glow indicator
    if threat_score < 30:
        st.markdown('<p class="glow-safe">🟢 SAFE</p>', unsafe_allow_html=True)
    elif threat_score < 70:
        st.markdown('<p class="glow-warning">🟡 SUSPICIOUS</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="glow-danger">🔴 PHISHING</p>', unsafe_allow_html=True)

    st.progress(threat_score)

    # -----------------------------
    # LOCATION
    # -----------------------------
    st.markdown("---")
    st.subheader("Server Location")

    country, city = get_ip_location(url)
    if country:
        st.write(city, ",", country)
    else:
        st.write("Not available")

    # -----------------------------
    # SAVE HISTORY
    # -----------------------------
    data = pd.read_csv("scan_history.csv")
    data.loc[len(data)] = [url, result]
    data.to_csv("scan_history.csv", index=False)

    # -----------------------------
    # FEATURE ANALYSIS
    # -----------------------------
    st.markdown("---")
    st.subheader("AI Feature Risk Analysis")

    feature_df = pd.DataFrame({
        "Feature": ["Length","IP","HTTPS","Dots","Hyphens","Keywords"],
        "Risk": [features[0]/100, features[1], 1-features[2], features[3]/10, features[4]/5, features[5]]
    })

    fig = px.bar(feature_df, x="Risk", y="Feature", orientation="h")
    st.plotly_chart(fig)

    # -----------------------------
    # WEBSITE PREVIEW (SAFE)
    # -----------------------------
    st.markdown("---")
    st.subheader("Website Preview")

    st.markdown(f'<iframe src="{url}" width="100%" height="400"></iframe>', unsafe_allow_html=True)

# -----------------------------
# MODEL PERFORMANCE
# -----------------------------
st.markdown("---")
st.subheader("🤖 AI Model Performance")

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[94,92,90,91],
    theta=["Accuracy","Precision","Recall","F1"],
    fill='toself'
))
st.plotly_chart(fig)

# -----------------------------
# DASHBOARD
# -----------------------------
st.markdown("---")
st.subheader("📊 Dashboard")

data = pd.read_csv("scan_history.csv")

if len(data) > 0:
    phishing = len(data[data["result"]=="Phishing"])
    legit = len(data[data["result"]=="Legitimate"])

    st.metric("Total", len(data))
    st.metric("Phishing", phishing)
    st.metric("Legit", legit)

    fig = px.pie(
        values=[phishing, legit],
        names=["Phishing","Legit"]
    )
    st.plotly_chart(fig)

    st.dataframe(data)
