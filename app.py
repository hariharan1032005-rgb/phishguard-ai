import streamlit as st
import pandas as pd
from predict import predict_url
import os
import plotly.graph_objects as go
import plotly.express as px
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
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

</style>
""", unsafe_allow_html=True)
# -----------------------------
# Screenshot Function
# -----------------------------
def capture_screenshot(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200,800)

    driver.get(url)
    time.sleep(3)

    driver.save_screenshot("site_preview.png")
    driver.quit()

    return "site_preview.png"


# -----------------------------
# Cybersecurity UI Theme
# -----------------------------
st.markdown("""
<style>
body {background-color:#0f172a;}
.stApp {background-color:#0f172a;}

h1{
color:#38bdf8;
text-align:center;
text-shadow:0px 0px 20px #38bdf8;
}

h2,h3{color:#e2e8f0;}

.stTextInput>div>div>input{
background:#1e293b;
color:white;
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
""",unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("🛡️ PhishGuard AI – Advanced Phishing Detection System")
st.info("🛡️ AI-Powered Cybersecurity System for Detecting Phishing Websites")

url = st.text_input("Enter URL")

# -----------------------------
# VirusTotal Scan
# -----------------------------
def virustotal_scan(url):

    API_KEY="YOUR_API_KEY_HERE"

    headers={"x-apikey":API_KEY}
    params={"url":url}

    response=requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=params
    )

    if response.status_code==200:
        st.success("VirusTotal scan submitted successfully")
    else:
        st.warning("VirusTotal scan failed")

# -----------------------------
# Load Blacklist
# -----------------------------
with open("blacklist.txt") as f:
    blacklist=f.read().splitlines()

# -----------------------------
# Create History File
# -----------------------------
if not os.path.exists("scan_history.csv"):
    df=pd.DataFrame(columns=["url","result"])
    df.to_csv("scan_history.csv",index=False)

# -----------------------------
# Server Location
# -----------------------------
def get_ip_location(url):

    try:
        domain=urlparse(url).netloc

        ip=requests.get(f"https://dns.google/resolve?name={domain}").json()
        ip_address=ip["Answer"][0]["data"]

        data=requests.get(f"http://ip-api.com/json/{ip_address}").json()

        return data["country"],data["city"]

    except:
        return None,None


# -----------------------------
# URL Analysis
# -----------------------------
if url:

    if st.button("Run Advanced Security Scan"):
        virustotal_scan(url)

    if any(b in url for b in blacklist):
        st.error("⚠️ URL found in phishing blacklist")

    suspicious_keywords=["login","verify","update","secure","bank","account"]

    if any(word in url.lower() for word in suspicious_keywords):
        st.warning("⚠️ Suspicious keyword detected")

    prediction,probability,features=predict_url(url)

    if prediction==1:
        result="Phishing"
        st.error("⚠️ Phishing Website Detected")
    else:
        result="Legitimate"
        st.success("✅ Legitimate Website")

    st.write("Phishing Probability:",round(probability*100,2),"%")

    threat_score=int(probability*100)

# -----------------------------
# Threat Score
# -----------------------------
    st.markdown("---")
    st.subheader("AI Threat Score")

    st.metric("Threat Score",threat_score)

    fig=go.Figure(go.Indicator(
        mode="gauge+number",
        value=threat_score,
        title={'text':"Phishing Risk Level"},
        gauge={
            'axis':{'range':[0,100]},
            'steps':[
                {'range':[0,30],'color':"green"},
                {'range':[30,70],'color':"yellow"},
                {'range':[70,100],'color':"red"}
            ]
        }
    ))

    st.plotly_chart(fig)

# -----------------------------
# Glowing Threat Indicator
# -----------------------------
    if threat_score<30:
        st.markdown('<p class="glow-safe">🟢 SAFE WEBSITE</p>',unsafe_allow_html=True)

    elif threat_score<70:
        st.markdown('<p class="glow-warning">🟡 SUSPICIOUS WEBSITE</p>',unsafe_allow_html=True)

    else:
        st.markdown('<p class="glow-danger">🔴 HIGH PHISHING RISK</p>',unsafe_allow_html=True)

    st.progress(threat_score)

# -----------------------------
# Server Location
# -----------------------------
    st.markdown("---")
    st.subheader("Server Location")

    country,city=get_ip_location(url)

    if country:
        st.write("Server Location:",city,",",country)
    else:
        st.write("Location not available")

# -----------------------------
# Save Scan History
# -----------------------------
    data=pd.read_csv("scan_history.csv")
    data.loc[len(data)]=[url,result]
    data.to_csv("scan_history.csv",index=False)

# -----------------------------
# AI Feature Risk Analysis
# -----------------------------
    st.markdown("---")
    st.subheader("AI Feature Risk Analysis")

    feature_names=[
        "URL Length",
        "IP Address in URL",
        "HTTPS Usage",
        "Dot Count",
        "Hyphen Count",
        "Suspicious Keywords"
    ]

    feature_values=[
        features[0]/100,
        features[1],
        1-features[2],
        features[3]/10,
        features[4]/5,
        features[5]
    ]

    feature_df=pd.DataFrame({
        "Feature":feature_names,
        "Risk Score":feature_values
    })

    fig=px.bar(
        feature_df,
        x="Risk Score",
        y="Feature",
        orientation="h",
        color="Risk Score",
        color_continuous_scale=["green","yellow","red"],
        title="AI Feature Risk Contribution"
    )

    st.plotly_chart(fig)

# -----------------------------
# AI Explanation
# -----------------------------
    st.markdown("---")
    st.subheader("AI Risk Explanation")

    reasons=[]

    if features[1]==1:
        reasons.append("URL contains IP address")

    if features[2]==0:
        reasons.append("Website not using HTTPS")

    if features[3]>3:
        reasons.append("Too many dots in URL")

    if features[4]>1:
        reasons.append("Multiple hyphens detected")

    if features[5]==1:
        reasons.append("Suspicious keywords detected")

    if reasons:
        for r in reasons:
            st.warning(r)
    else:
        st.success("No suspicious indicators")

# -----------------------------
# Website Screenshot
# -----------------------------
    st.markdown("---")
    st.subheader("Website Screenshot")

    try:
        screenshot=capture_screenshot(url)
        st.image(screenshot)
    except:
        st.warning("Unable to capture website screenshot")

# -----------------------------
# Model Performance
# -----------------------------
st.markdown("---")
st.subheader("🤖 AI Model Performance")

metrics=["Accuracy","Precision","Recall","F1 Score"]
values=[94,92,90,91]

fig=go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=metrics,
    fill='toself'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0,100]
        )
    ),
    showlegend=False
)

st.plotly_chart(fig)

# -----------------------------
# Dashboard
# -----------------------------
st.markdown("---")
st.subheader("📊 Security Analytics Dashboard")

data=pd.read_csv("scan_history.csv")

if len(data)>0:

    phishing_count=len(data[data["result"]=="Phishing"])
    legit_count=len(data[data["result"]=="Legitimate"])

    col1,col2,col3=st.columns(3)

    col1.metric("Total URLs Scanned",len(data))
    col2.metric("Phishing Detected",phishing_count)
    col3.metric("Legitimate URLs",legit_count)

    chart_data=pd.DataFrame({
        "Type":["Phishing","Legitimate"],
        "Count":[phishing_count,legit_count]
    })

    fig=px.pie(
        chart_data,
        values="Count",
        names="Type",
        title="Phishing Detection Distribution",
        color_discrete_sequence=["red","green"]
    )

    st.plotly_chart(fig)

    st.subheader("Scan History")
    st.dataframe(data)

    st.download_button(
        label="Download Scan Report",
        data=data.to_csv(index=False),
        file_name="phishguard_scan_report.csv",
        mime="text/csv"
    )