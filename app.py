import streamlit as st
import os
from dotenv import load_dotenv

from utils.auth import init_session, check_auth
from utils.ui_components import load_css

load_dotenv()  # Reads your .env file automatically

# ─────────────────────────────────────────────
#  Load Password
# ─────────────────────────────────────────────
_APP_PASSWORD = os.getenv("APP_PASSWORD", "sleekflow2024")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SleekFlow Manager",
    page_icon="💬✅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help or Report an Issue': 'imadduddin@invokeisdata.com',
    }
)

load_css()
init_session()

if check_auth():
    st.switch_page("pages/dashboard.py")

# ─────────────────────────────────────────────
#  CUSTOM CSS for Login box HTML  (light, clean, professional)
# ─────────────────────────────────────────────
st.markdown("""
<div class="login-box">
    <div style="font-size:3rem;">💬</div>
    <div style="font-size:1.5rem; font-weight:700;">SleekFlow Manager</div>
    <div style="font-size:0.85rem; color:#6b7280;">
        Sign in to access your dashboard & inbox
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Password input and sign-in button
# ─────────────────────────────────────────────
password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter app password",
    label_visibility="collapsed",
)

if st.button("Sign In →", type="primary", use_container_width=True):
    if password == _APP_PASSWORD:
        st.session_state.authenticated = True
        st.switch_page("pages/dashboard.py")
    else:
        st.error("Incorrect password. Please try again.") 

# ─────────────────────────────────────────────
#  Footer note
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:1rem;
    font-size:0.75rem; color:#9ca3af;">
    API key is loaded from your <code>.env</code> file
</div>
""", unsafe_allow_html=True)