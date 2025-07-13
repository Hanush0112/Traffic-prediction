# app.py

import streamlit as st
from maps_api import get_alternate_routes
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

st.set_page_config(page_title="Smart Traffic Redirector", page_icon="🚦")
st.title("🚦 Smart Traffic Redirector")

st.markdown("""
This app simulates a traffic congestion detection system.
If congestion is detected, it fetches alternate routes using Google Maps.
""")

# User Inputs
origin = st.text_input("📍 Enter Origin Location", "Chennai Central, India")
destination = st.text_input("🏁 Enter Destination Location", "Velachery, Chennai")

# Simulate model output (in actual project, get this from your CV detection)
congestion_status = st.selectbox("🚦 Is Traffic Congested?", ["No", "Yes"])

if st.button("Check & Suggest Route"):
    if not origin or not destination:
        st.warning("Please provide both origin and destination.")
    else:
        if congestion_status == "Yes":
            st.warning("⚠️ Congestion detected! Fetching alternate routes...")
            with st.spinner("Contacting Google Maps..."):
                try:
                    routes = get_alternate_routes(origin, destination, API_KEY)
                    st.success(f"Found {len(routes)} alternate route(s):")

                    for i, route in enumerate(routes, start=1):
                        st.subheader(f"Route {i}: {route['summary']}")
                        st.markdown(f"**Distance**: {route['distance']}")
                        st.markdown(f"**Estimated Time**: {route['duration']}")
                        with st.expander("📋 Step-by-step Directions"):
                            for step, dist in route["steps"]:
                                st.markdown(f"- {step} ({dist})")

                except Exception as e:
                    st.error(f"Failed to fetch routes: {e}")
        else:
            st.success("✅ No congestion detected. Continue on the same route.")
