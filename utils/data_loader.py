import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SLEEKFLOW_BASE_URL", "https://sleekflow-core-app-seas-production.azurewebsites.net")
AUTH_FORMAT = os.getenv("SLEEKFLOW_AUTH_FORMAT", "X-Sleekflow-Api-Key")

class APIClient:
    def __init__(self, api_key: str, base_url: str = BASE_URL, auth_format: str = AUTH_FORMAT):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.auth_format = auth_format
        self.header = self._get_header()

# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────
    def _get_header(self) -> dict:
        auth_header = {
            "X-Sleekflow-Api-Key":   {"X-Sleekflow-Api-Key": self.api_key},
            "Authorization: Bearer": {"Authorization": f"Bearer {self.api_key}"},
            "X-API-Key":             {"X-API-Key": self.api_key},
        }.get(self.auth_format, {"X-Sleekflow-Api-Key": self.api_key})

        return {
            **auth_header,
            "Accept":       "application/json",
            "Content-Type": "application/json",
        }

    def api_get(self, path:str, params: dict = None) -> tuple:
        url = f"{self.base_url}{path}"
        try:
            r = requests.get(
                url,
                headers=self._get_header(),
                params=params,
                timeout=15
            )
            r.raise_for_status()
            return r.json(), None

        except requests.exceptions.HTTPError as e:
            return None, f"HTTP {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return None, str(e)

    def api_post(self, path: str, payload: dict) -> tuple:
        url = f"{self.base_url}{path}"
        try:
            r = requests.post(
                url,
                headers=self._get_header(),
                json=payload,
                timeout=15
            )
            r.raise_for_status()
            return r.json(), None
        
        except requests.exceptions.HTTPError as e:
            return None, f"HTTP {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return None, str(e)

# ─────────────────────────────────────────────
# Message Channel API
# ─────────────────────────────────────────────
    @st.cache_data(ttl=600, show_spinner=False)
    def fetch_channels(self) -> tuple:
        """Fetches all connected message channels from SleekFlow."""
        data, err = self.api_get("/api/conversation/channel")

        if err:
            return [], err

        if isinstance(data, list):
            return data, None
            
        for key in ["data", "channels", "items", "result"]:
            if key in data and isinstance(data[key], list):
                return data[key], None
                
        return [], None
    

# ─────────────────────────────────────────────
# Analytics API
# ─────────────────────────────────────────────
    @st.cache_data(ttl=300, show_spinner=False)
    def fetch_analytics(self, start_date: str, end_date: str, channel_id: str = None) -> tuple:
        params = {"startDate": start_date, "endDate": end_date}
        if channel_id:
            params["channelId"] = channel_id
        return self.api_get("/api/analytic", params=params)

# ─────────────────────────────────────────────
# All ConversationAPI
# ─────────────────────────────────────────────
    @st.cache_data(ttl=100, show_spinner=False)
    def fetch_all_conversations(self) -> tuple:
        return self.api_get("/api/conversation/all")

# ─────────────────────────────────────────────
# Conversations Details API
# ─────────────────────────────────────────────
    @st.cache_data(ttl=100, show_spinner=False)
    def fetch_conversation_details(self, conv_id: str) -> tuple:
        return self.api_get(f"/api/conversation/{conv_id}")

# ─────────────────────────────────────────────
# Messages in conversations API
# ─────────────────────────────────────────────
    @st.cache_data(ttl=100, show_spinner=False)
    def fetch_messages(self, conv_id: str) -> tuple:
        return self.api_get(f"/api/conversation/{conv_id}/messages")
