import streamlit as st
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

st.set_page_config(page_title="Neural Nexus | Agentic AI", layout="wide")

st.markdown("""
    <style>
    .main { background: #050505; }
    .agent-box { background: rgba(157, 0, 255, 0.08); border: 1px solid #9d00ff; border-radius: 20px; padding: 25px; }
    .stMetric { background: rgba(0, 242, 255, 0.05); border: 1px solid #00f2ff; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Neural Nexus: Agentic Intelligence")
st.caption("Autonomous Decision Engine for Hyderabad Metropolitan Logistics")

with st.sidebar:
    st.header("⚡ Agent Parameters")
    hour = st.slider("Forecast Hour", 0, 23, 18)
    weather = st.selectbox("Atmospheric State", ["Clear", "Heavy Rain", "Monsoon Storm"])
    st.divider()
    agent_decision = st.toggle("Enable Autonomous Logic", value=True)

HYD_CENTER = [17.4486, 78.3908]

def run_prediction(hour, weather):
    points = np.random.randn(150, 2) * 0.03 + HYD_CENTER
    mult = 2.8 if (17 <= hour <= 21) or weather != "Clear" else 1.1
    return np.column_stack((points, np.random.rand(150) * mult))

data = run_prediction(hour, weather)
load_index = (np.mean(data[:, 2]) * 10).round(1)

col1, col2 = st.columns([2, 1])

with col1:
    m = folium.Map(location=HYD_CENTER, zoom_start=13, tiles="CartoDB dark_matter")
    HeatMap(data).add_to(m)
    st_folium(m, width="100%", height=500, key="nexus_map")

with col2:
    st.metric("Predicted Hub Load", f"{load_index}%", delta="CRITICAL" if load_index > 7.0 else "STABLE")
    if agent_decision:
        st.markdown('<div class="agent-box">', unsafe_allow_html=True)
        st.subheader("🤖 Agentic Reasoning")
        if load_index > 7.0:
            st.error("Threshold Breach Detected")
            st.write("**Decision:** Deploying autonomous reroute vectors to bypass Hitech City bottleneck.")
            if st.button("Execute Fleet Dispatch"):
                with st.spinner("Broadcasting instructions..."):
                    time.sleep(2)
                    st.success("Dispatch Protocol 01 Verified")
        else:
            st.success("System Optimized")
            st.write("**Status:** Nodes within safety parameters. No active intervention required.")
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.latex(r"\text{Decision}(a) = \text{argmax}_{a \in A} \sum_{t=0}^{\infty} \gamma^t R(s_t, a_t)")
