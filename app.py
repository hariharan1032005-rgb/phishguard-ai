import streamlit as st
import pandas as pd
from predict import predict_url
import os
import plotly.graph_objects as go
import plotly.express as px
import requests
from urllib.parse import urlparse

# -----------------------------
# UI STYLE & CONFIG
# -----------------------------
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg,#020617,#0f172a,#020617); color:white; }
    h1 { color:#38bdf8; text-align:center; text-shadow:0 0 20px #38bdf8; }
    .stButton>button { background-color:#2563eb; color:white; border-radius:10px; width:100%; }
    .glow-safe { color:#22c55e; font-weight:bold; text-align:center; text-shadow:0 0 10px #22c55e; }
    .glow-danger { color:#ef4444; font-weight:bold; text-align:center; text-shadow:0 0 10px #ef4444; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def get_ip_location(url):
    try:
        domain = urlparse(url).netloc or url.split('/')[0]
        ip_resp = requests.get(f"https://dns.google/resolve?name={domain}").json()
        ip_addr = ip_resp["Answer"][0]["data"]
        data = requests.get(f"http://ip-api.com/json/{ip_addr}").json()
        return data.get("country"), data.get("city")
    except:
        return None, None

# -----------------------------
# DATA PERSISTENCE
# -----------------------------
if not os.path.exists("scan_history.csv"):
    pd.DataFrame(columns=["url","result"]).to_csv("scan_history.csv", index=False)

try:
    with open("blacklist.txt", "r") as f:
        blacklist = f.read().splitlines()
except:
    blacklist = []

# -----------------------------
# MAIN APP
# -----------------------------
st.title("🛡️ PhishGuard AI – Advanced Detection")
url = st.text_input("Enter URL to Scan", placeholder="https://example-site.com")

if url:
    if st.button("Analyze Security"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 1. Prediction Logic
            prediction, probability, features = predict_url(url)
            threat_score = int(probability * 100)
            
            if prediction == 1 or any(b in url for b in blacklist):
                st.error("🚨 PHISHING DETECTED")
                result = "Phishing"
            else:
                st.success("✅ SITE APPEARS LEGITIMATE")
                result = "Legitimate"

            # 2. Score Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=threat_score,
                gauge={'axis':{'range':[0,100]}, 'bar':{'color':"#38bdf8"},
                       'steps':[{'range':[0,40],'color':"green"},{'range':[40,70],'color':"orange"},{'range':[70,100],'color':"red"}]}
            ))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Server Intel")
            country, city = get_ip_location(url)
            if country: st.info(f"📍 Location: {city}, {country}")
            
            st.subheader("Feature Analysis")
            feat_df = pd.DataFrame({
                "Feature": ["Length", "IP", "HTTPS", "Dots", "Hyphens", "Keywords"],
                "Risk": [features[0]/100, features[1], 1-features[2], features[3]/10, features[4]/5, features[5]]
            })
            st.bar_chart(feat_df.set_index("Feature"))

        # 3. Save History
        hist = pd.read_csv("scan_history.csv")
        new_row = pd.DataFrame({"url": [url], "result": [result]})
        pd.concat([hist, new_row]).to_csv("scan_history.csv", index=False)

        # 4. Preview
        st.markdown("---")
        st.subheader("🌐 Site Sandbox Preview")
        st.markdown(f'<iframe src="{url}" width="100%" height="400" style="border:1px solid #38bdf8; border-radius:10px;"></iframe>', unsafe_allow_html=True)

# -----------------------------
# DASHBOARD
# -----------------------------
st.markdown("---")
st.subheader("📊 System Analytics")
if os.path.exists("scan_history.csv"):
    data = pd.read_csv("scan_history.csv")
    if not data.empty:
        c1, c2 = st.columns(2)
        c1.metric("Total Scans", len(data))
        c2.metric("Phishing Blocked", len(data[data["result"]=="Phishing"]))
        st.dataframe(data.tail(5), use_container_width=True)
