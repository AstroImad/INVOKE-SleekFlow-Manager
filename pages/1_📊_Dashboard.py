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

channel_options = {"🌐 All Numbers (Account-wide)": None}

for ch in channels:
    # Notice how everything below is pushed in by 4 spaces!
    if not isinstance(ch, dict):
        continue
    
    cid  = (ch.get("id") or ch.get("channelId") or
            ch.get("phoneNumberId") or ch.get("_id"))
    
    name = (ch.get("name") or ch.get("channelName") or
            ch.get("displayName") or ch.get("phoneNumber") or
            ch.get("identifier") or str(cid))
    
    ctype = str(ch.get("type") or ch.get("channelType") or "")
    icon  = "📱" if "whatsapp" in ctype.lower() else "💬"
    
    if cid:
        channel_options[f"{icon} {name}"] = cid