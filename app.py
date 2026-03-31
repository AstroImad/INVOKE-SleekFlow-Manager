import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

load_dotenv()  # Reads your .env file automatically


# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SleekFlow Manager",
    page_icon="💬✅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  API CONFIG
# ─────────────────────────────────────────────
DEFAULT_BASE_URL = os.getenv("SLEEKFLOW_BASE_URL", "https://sleekflow-core-app-seas-production.azurewebsites.net")
APP_PASSWORD      = os.getenv("APP_PASSWORD", "")
ENV_API_KEY       = os.getenv("SLEEKFLOW_API_KEY", "")
ENV_AUTH_FORMAT   = os.getenv("SLEEKFLOW_AUTH_FORMAT", "")

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for key, default in {
    "authenticated": False,
    "api_key": ENV_API_KEY,
    "base_url": DEFAULT_BASE_URL,
    "auth_format": ENV_AUTH_FORMAT,
    "page": "Dashboard",
    "selected_conv_id": None,
    "selected_conv_name": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default
