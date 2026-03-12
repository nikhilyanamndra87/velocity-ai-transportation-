import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from math import radians, cos, sin, asin, sqrt
import time
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Velocity AI Enterprise", layout="wide")

# YOUR ACTUAL FIREBASE URL
FIREBASE_URL = "https://velocity-ai-b3d5d-default-rtdb.firebaseio.com/drivers.json"
CITY_HUB = (17.4486, 78.3908) # Hitech City, Hyderabad
GEOFENCE_RADIUS = 5.0 # Kilometers

# --- 2. MATHEMATICAL ENGINE ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 
    dLat, dLon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dLat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2)**2
    return 2 * R * asin(sqrt(a))

def fetch_data():
    try:
        r = requests.get(FIREBASE_URL, timeout=5)
        return r.json() if r.status_code == 200 else {}
    except: return {}

# --- 3. UI STYLING ---
st.markdown("""
    <style>
    .main { background: #000; color: #fff; }
    .stMetric { background: #0a0a0a; border: 1px solid #333; padding: 15px; border-radius: 12px; }
    .alert-card { background: #ff4b4b22; border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px; color: #ff4b4b; margin-bottom: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MAIN APPLICATION ---
st.title("🚖 Velocity AI: Enterprise Fleet Command")
st.caption(f"Connected to: {FIREBASE_URL}")

fleet_data = fetch_data()

tab1, tab2, tab3 = st.tabs(["🌐 Live Geo-Tracking", "📊 Business Intelligence", "🛠️ Raw Data Logs"])

with tab1:
    col_map, col_alerts = st.columns([3, 1])
    
    with col_map:
        # Map Setup
        m = folium.Map(location=CITY_HUB, zoom_start=13, tiles="CartoDB dark_matter")
        # Draw Geofence
        folium.Circle(CITY_HUB, radius=GEOFENCE_RADIUS*1000, color="cyan", fill=True, opacity=0.1).add_to(m)
        
        active_alerts = []
        if fleet_data:
            for d_id, info in fleet_data.items():
                lat, lon = info.get('lat'), info.get('lon')
                if lat and lon:
                    dist = haversine(CITY_HUB[0], CITY_HUB[1], lat, lon)
                    is_sos = info.get('sos', False)
                    is_outside = dist > GEOFENCE_RADIUS
                    
                    color = 'red' if (is_sos or is_outside) else 'blue'
                    icon = 'exclamation-triangle' if is_sos else 'car'
                    
                    if is_sos: active_alerts.append(f"🚨 SOS: {d_id} needs help!")
                    if is_outside: active_alerts.append(f"⚠️ BREACH: {d_id} is outside zone!")

                    folium.Marker(
                        [lat, lon], 
                        icon=folium.Icon(color=color, icon=icon, prefix="fa"),
                        tooltip=f"Driver: {d_id}"
                    ).add_to(m)
        st_folium(m, width="100%", height=600)

    with col_alerts:
        st.subheader("Safety Monitor")
        if active_alerts:
            for a in active_alerts:
                st.markdown(f'<div class="alert-card">{a}</div>', unsafe_allow_html=True)
        else:
            st.success("Fleet Secure (Inside Zone)")

with tab2:
    st.subheader("Revenue & Surge Analytics")
    surge = st.slider("AI Surge Factor", 1.0, 4.0, 1.2)
    if fleet_data:
        stats = []
        for d_id, info in fleet_data.items():
            dist_km = haversine(CITY_HUB[0], CITY_HUB[1], info.get('lat',0), info.get('lon',0))
            rev = (60 + (dist_km * 18)) * surge
            stats.append({"Driver": d_id, "Profit": rev * 0.7})
        
        df = pd.DataFrame(stats)
        st.plotly_chart(px.bar(df, x="Driver", y="Profit", color="Profit", template="plotly_dark"))

with tab3:
    st.subheader("Database Pulse")
    st.write(fleet_data)

# Real-time refresh (Every 4 seconds)
time.sleep(4)
st.rerun()
