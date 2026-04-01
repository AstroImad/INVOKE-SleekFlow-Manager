import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SLEEKFLOW_BASE_URL", "https://sleekflow-core-app-seas-production.azurewebsites.net")
AUTH_FORMAT = os.getenv("SLEEKFLOW_AUTH_FORMAT", "X-Sleekflow-Api-Key")


# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────

def _get_header() -> dict:
    api_key = st.session_state.get("api_key", "")
    fmt = st.session_state.get("auth_format", AUTH_FORMAT)

    auth_header = {
        "X-Sleekflow-Api-Key":   {"X-Sleekflow-Api-Key": api_key},
        "Authorization: Bearer": {"Authorization": f"Bearer {api_key}"},
        "X-API-Key":             {"X-API-Key": api_key},
    }.get(fmt, {"X-Sleekflow-Api-Key": api_key})

    return {
        **auth_header,
        "Accept":       "application/json",
        "Content-Type": "application/json",
    }

def _get_base() -> str:
    return st.session_state.get("base_url", BASE_URL).rstrip("/")


def api_get(path:str, params: dict = None) -> tuple:
    url = f"{_get_base()}{path}"
    try:
        r = requests.get(
            url,
            headers=_get_header(),
            params=params,
            timeout=15
        )
        r.raise_for_status()
        return r.json(), None

    except requests.exceptions.HTTPError:
        return None, f"HTTP {r.status_code} - {r.text}"
    except Exception as e:
        return None, str(e)

def api_post(path: str, payload: dict) -> tuple:
    url = f"{_get_base()}{path}"
    try:
        r = requests.post(
            url,
            header=_get_header(),
            json=payload,
            timeout=15
        )
        r.raise_for_status()
        return r.json(), None
    
    except requests.exeptions.HTTPError:
        return None, f"HTTP {r.status_code} - {r.text}"
    except Exception as e:
        return None, str(e)