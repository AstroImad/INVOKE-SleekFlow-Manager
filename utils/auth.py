import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

_BASE_URL = os.getenv("SLEEKFLOW_BASE_URL", "https://sleekflow-core-app-seas-production.azurewebsites.net")
_APP_PASSWORD      = os.getenv("APP_PASSWORD", "")
_API_KEY       = os.getenv("SLEEKFLOW_API_KEY", "")
_AUTH_FORMAT   = os.getenv("SLEEKFLOW_AUTH_FORMAT", "")

# ─────────────────────────────────────────────
#  SESSION STATE & AUTH FUNCTIONS
# ─────────────────────────────────────────────

def init_session():
    """Initializes the default session state variables on first load."""
    defaults = {
        "authenticated": False,
        "api_key": _API_KEY,
        "base_url": _BASE_URL,
        "auth_format": _AUTH_FORMAT,
        "page": "Dashboard",
        "selected_conv_id": None,
        "selected_conv_name": "",
    }
    
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

def check_auth() -> bool:
    """Checks if the user is currently logged in."""
    return st.session_state.get("authenticated", False)

def require_auth():
    """Stops the page from loading if the user is not logged in."""
    init_session()
    if not check_auth():
        st.warning("Please log in first.")
        st.stop()  # This halts Streamlit from rendering the rest of the page