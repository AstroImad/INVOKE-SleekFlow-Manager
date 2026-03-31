import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SLEEKFLOW_BASE_URL", "https://sleekflow-core-app-seas-production.azurewebsites.net")
AUTH_FORMAT = os.getenv("SLEEKFLOW_AUTH_FORMAT", "X-Sleekflow-Api-Key")

def _get_header() -> dict:
    api_key = st.session_state.get("api_key", "")
    fmt = st.session_state.get("auth_format", AUTH_FORMAT)

    auth_header = {
        
    }