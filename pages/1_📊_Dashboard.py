import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

from utils.auth import require_auth
from utils.data_loader import APIClient

api_key = st.session_state.get("api_key", "")

client = APIClient(api_key)

st.set_page_config(
    page_title="Dashboard — SleekFlow",
    page_icon="📊",
    layout="wide",
)

# load_css()
# require_auth()
# render_sidebar()

st.markdown("## 📊 Dashboard")

api_key = st.session_state.api_key

# ─────────────────────────────────────────────
#  STEP 1 — Load channels for the dropdown
# ─────────────────────────────────────────────
with st.spinner("Loading channels..."):
    channels, ch_err = client.fetch_channels(api_key)

channel_option = {"🌐 All Numbers (Account-wide)": None}
for ch in channels:
    