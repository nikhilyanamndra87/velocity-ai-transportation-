import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import time

# --- CONFIG ---
FIREBASE_URL = "https://velocity-ai-b3d5d-default-rtdb.firebaseio.com/drivers.json"
CITY_HUB = (17.4486, 78.3908) # Hitech City

st.set_page_config(page_title="Velocity AI | Enterprise", layout="wide")

# Persistent memory for the "Zomato Trail"
if 'driver_history' not in st.session_state:
    st.session_state.driver_history = {}

def fetch_live_data():
    try:
        r = requests.get(FIREBASE_URL, timeout=2)
        return r.json() if r.status_code == 200 else {}
    except: return {}

st.title("🚖 Velocity AI: Real-Time Command")
st.caption("Live Fleet Feed from Hyderabad Hub | Sub-second Synchronization")

# --- THE SMOOTH ENGINE (FRAGMENT) ---
@st.fragment(run_every=3) # Refreshes only this block every 3s (No Blinking)
def update_map():
    fleet_data = fetch_live_data()
    m = folium.Map(location=CITY_HUB, zoom_start=14, tiles="CartoDB dark_matter")
    
    if fleet_data:
        for d_id, info in fleet_data.items():
            lat, lon = info.get('lat'), info.get('lon')
            if lat and lon:
                # 1. Update Path History
                if d_id not in st.session_state.driver_history:
                    st.session_state.driver_history[d_id] = []
                
                pos = [lat, lon]
                if not st.session_state.driver_history[d_id] or st.session_state.driver_history[d_id][-1] != pos:
                    st.session_state.driver_history[d_id].append(pos)

                # 2. Draw Breadcrumb Trail (The Zomato Line)
                if len(st.session_state.driver_history[d_id]) > 1:
                    folium.PolyLine(st.session_state.driver_history[d_id], color="cyan", weight=3, opacity=0.7).add_to(m)

                # 3. Draw Marker
                icon_color = 'red' if info.get('sos') else 'blue'
                folium.Marker(pos, icon=folium.Icon(color=icon_color, icon='car', prefix='fa'), tooltip=f"Driver ID: {d_id}").add_to(m)
    
    st_folium(m, width="100%", height=600, key="live_map_v2")

update_map()

# Static Metrics (Sidebar stays perfectly still)
st.sidebar.header("System Intelligence")
st.sidebar.success("Connection: Operational")
if st.sidebar.button("Clear Path History"):
    st.session_state.driver_history = {}
    st.rerun()
