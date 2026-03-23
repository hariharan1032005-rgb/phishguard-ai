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
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️")

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
.glow-safe {
    color:#22c55e;
    font-size:26px;
    text-align:center;
    text-shadow:0 0 10px #22c55e;
}
.glow-warning {
    color:#facc15;
    font-size:26px;
    text-align:center;
    text-shadow:0 0 10px #facc15;
}
.glow-danger {
    color:#ef4444;
    font-size:26px;
    text-align:center;
    text-shadow:0 0 10px #ef4444;
}
.stMetric {
    background:#1e293b;
    padding:10px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# FUNCTIONS
# -----------------------------
def virustotal_scan(url):
    API_KEY = "YOUR_API_KEY_HERE"
    headers = {"x-apikey": API_KEY}
    params = {"url": url}
    try:
        response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=params)
        if response.status_code == 200:
            st.success("VirusTotal scan submitted")
        else:
            st.warning("VirusTotal scan failed (Check API Key)")
    except:
        st.warning("VirusTotal connection error")

def get_ip_location(url):
    try:
        domain = urlparse(url).netloc
        if not domain:
            domain = url.split('/')[0]
        ip_resp = requests.get(f"https://dns.google/resolve?name={domain}").json()
        ip_address = ip_resp["Answer"][0]["data"]
        data = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        return data.get("country"), data.get("city")
    except:
        return None, None

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
# TITLE & INPUT
# -----------------------------
st.title("🛡️ PhishGuard AI")
st.info("AI-Powered Cybersecurity System for Detecting Phishing Websites")

url = st.text_input("Enter URL (e.g., https://example.com)")

# -----------------------------
# MAIN LOGIC
# -----------------------------
if url:
    if st.button("Run Advanced Scan"):
        virustotal_scan(url)

        if any(b in url for b in blacklist):
            st.error("⚠️ Blacklisted URL Detected!")

        suspicious = ["login","verify","update","bank","secure"]
        if any(word in url.lower() for word in suspicious):
            st.warning("⚠️ Suspicious keyword detected in URL")

        # Get Prediction
        try:
            prediction, probability, features = predict_url(url)
            
            if prediction == 1:
                result = "Phishing"
                st.error("⚠️ Phishing Website Detected")
            else:
                result = "Legitimate"
                st.success("✅ Legitimate Website")

            threat_score = int(probability * 100)
            st.write(f"Phishing Probability: {threat_score}%")

            # Score Gauge
            st.markdown("---")
            st.subheader("AI Threat Score")
            st.metric("Threat Score", f"{threat_score}/100")
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=threat_score,
                gauge={'axis':{'range':[0,100]},
                       'bar': {'color': "darkblue"},
                       'steps' : [
                           {'range': [0, 30], 'color': "green"},
                           {'range': [30, 70], 'color': "yellow"},
                           {'range': [70, 100], 'color': "red"}]}
            ))
            st.plotly_chart(fig)

            # Visual Indicator
            if threat_score < 30:
                st.markdown('<p class="glow-safe">🟢 SAFE</p>', unsafe_allow_html=True)
            elif threat_score < 70:
                st.markdown('<p class="glow-warning">🟡 SUSPICIOUS</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="glow-danger">🔴 PHISHING</p>', unsafe_allow_html=True)

            st.progress(threat_score)

            # Location info
            st.markdown("---")
            st.subheader("Server Location")
            country, city = get_ip_location(url)
            if country:
                st.write(f"📍 {city}, {country}")
            else:
                st.write("Location data unavailable")

            # Save to history
            hist_df = pd.read_csv("scan_history.csv")
            new_entry = pd.DataFrame({"url": [url], "result": [result]})
            hist_df = pd.concat([hist_df, new_entry], ignore_index=True)
            hist_df.to_csv("scan_history.csv", index=False)

            # Feature Risk Chart
            st.markdown("---")
            st.subheader("AI Feature Risk Analysis")
            feature_df = pd.DataFrame({
                "Feature": ["Length","IP","HTTPS","Dots","Hyphens","Keywords"],
                "Risk": [features[0]/100, features[1], 1-features[2], features[3]/10, features[4]/5, features[5]]
            })
            fig_bar = px.bar(feature_df, x="Risk", y="Feature", orientation="h", color="Risk", color_continuous_scale="RdYlGn_r")
            st.plotly_chart(fig_bar)

            # Preview
            st.markdown("---")
            st.subheader("Website Preview")
            st.markdown(f'<iframe src="{url}" width="100%" height="400"></iframe>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error during prediction: {e}")

# -----------------------------
# PERFORMANCE & DASHBOARD
# -----------------------------
st.markdown("---")
st.subheader("🤖 AI Model Performance")
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=[94,92,90,91],
    theta=["Accuracy","Precision","Recall","F1"],
    fill='toself'
))
st.plotly_chart(fig_radar)

st.markdown("---")
st.subheader("📊 Scan Analytics")
if os.path.exists("scan_history.csv"):
    data = pd.read_csv("scan_history.csv")
    if not data.empty:
        p_count = len(data[data["result"]=="Phishing"])
        l_count = len(data[data["result"]=="Legitimate"])
        
        c1, c2 = st.columns(2)
        c1.metric("Total Scans", len(data))
        c2.pie = px.pie(values=[p_count, l_count], names=["Phishing","Legit"], color_discrete_sequence=["red","green"])
        st.plotly_chart(c2.pie)
        
        st.dataframe(data.tail(10))
