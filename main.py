import streamlit as st
import random
import time
import requests

# --- CONFIGURATION & NASA API ---
NASA_EXOPLANET_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+top+1+pl_name,pl_bmassj,pl_teff+from+pscomppars+where+pl_bmassj+is+not+null+and+pl_teff+is+not+null+order+by+random()"

# --- SESSION STATE ---
if 'inventory' not in st.session_state: st.session_state.inventory = {}
if 'credits' not in st.session_state: st.session_state.credits = 0
if 'ship_level' not in st.session_state: st.session_state.ship_level = 1
if 'location' not in st.session_state: st.session_state.location = "Earth"
if 'exoplanet' not in st.session_state: st.session_state.exoplanet = None



st.set_page_config(page_title="Cosmopolitan", page_icon="🚀", layout="wide")
st.title("🚀 Cosmopolitan")
st.write("Welcome to Cosmopolitan, the interstellar trading game! Explore the galaxy, trade resources, and upgrade your ship to become the ultimate space trader.")

tab1, tab2, tab3 = st.tabs(["🌌 Explore", "🍳 Cook","📦 Cargo"])

with st.sidebar:
    st.header("Ship Status")
    st.write(f"Level: {st.session_state.ship_level}")
    st.write(f"Credits: {st.session_state.credits}")
    cost = st.session_state.ship_level * 100
    if st.button(f"Upgrade Ship ({cost} credits)"):
        if st.session_state.credits >= cost:
            st.session_state.credits -= cost
            st.session_state.ship_level += 1
            st.success("Ship upgraded!")
            st.rerun()
        else:
            st.error("Not enough credits to upgrade!")