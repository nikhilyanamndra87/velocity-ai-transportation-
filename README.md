# 🚖 Velocity AI: Enterprise Fleet Command

Velocity AI is a production-ready, real-time ecosystem designed to manage large-scale cab fleets. It bridges the gap between hardware telemetry (mobile GPS) and autonomous business logic (Agentic AI).

## 🌟 Key Features
- **Real-Time GPS Tracking:** Sub-second latency syncing between mobile hardware and the cloud dashboard using **Firebase NoSQL**.
- **Agentic Geofencing:** Implements the **Haversine Formula** to monitor vehicle boundaries in Hyderabad (Hitech City), triggering automated security alerts for zone breaches.
- **SOS Emergency Protocol:** A dedicated safety-interrupt layer that provides immediate visual and logging overrides on the admin console during driver emergencies.
- **Dynamic Surge Analytics:** An interactive BI module that simulates market demand and calculates net profit margins based on vehicle fuel efficiency and surge multipliers.

## 🏗️ Architecture
The system utilizes a two-tier cloud architecture:
1. **Edge Layer (Driver):** A lightweight HTML5/JavaScript application accessing the phone's GPS hardware via the W3C Geolocation API.
2. **Cloud Brain (Admin):** A Python-powered Streamlit dashboard hosted in the cloud, performing real-time data orchestration and geospatial analysis.

## 🛠️ Technical Stack
- **Languages:** Python (Backend), JavaScript (Edge Tracking), CSS3 (UI Styling).
- **Database:** Firebase Realtime Database (Live NoSQL).
- **Maps:** Folium & Leaflet.js with Dark-Matter tiles.
- **Data Science:** Pandas, NumPy, Plotly Express.

## 🚀 Deployment Guide
1. **Admin Dashboard:** Deploy `app.py` to **Streamlit Cloud**.
2. **Driver App:** Host `driver.html` on **GitHub Pages** (HTTPS is required for GPS access).
3. **Connectivity:** Update the Firebase URL in both files to point to your Realtime Database instance.

---
**Developed by Nikhil Yanamandra** *Engineering the future of Intelligent Transportation Systems.*
