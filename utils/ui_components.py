"""
utils/ui_components.py
─────────────────────────────────────────────────────────────
Reusable UI building blocks used across pages.

Why here?
- Pages stay clean — they call render_kpi_card() instead of
  pasting raw HTML everywhere.
- Changing a design only requires editing one place.
"""

import streamlit as st
import os


# ── CSS loader ────────────────────────────────────────────
def load_css() -> None:
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ── KPI Card ─────────────────────────────────────────────
def render_kpi_card(col, label: str, value: str, icon: str = "") -> None:
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{icon} {label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Section header ────────────────────────────────────────
def render_section_header(title: str) -> None:
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


# ── Message bubble ────────────────────────────────────────
def render_message_bubble(text: str, is_outbound: bool, sender: str = "", timestamp: str = "") -> None:
    if is_outbound:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; margin:6px 0;">
            <div>
                <div style="background:#6366f1; color:white; padding:10px 14px;
                    border-radius:16px 16px 4px 16px; max-width:65%;
                    font-size:0.85rem; line-height:1.45; word-wrap:break-word;
                    display:inline-block;">{text}</div>
                <div style="font-size:0.68rem; color:#9ca3af;
                    text-align:right; margin-top:2px;">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; margin:6px 0;">
            <div>
                <div style="font-size:0.72rem; color:#6b7280; margin-bottom:2px;">{sender}</div>
                <div style="background:#f3f4f6; color:#111827; padding:10px 14px;
                    border-radius:16px 16px 16px 4px; max-width:65%;
                    font-size:0.85rem; line-height:1.45; word-wrap:break-word;
                    display:inline-block;">{text}</div>
                <div style="font-size:0.68rem; color:#9ca3af; margin-top:2px;">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Conversation list item ────────────────────────────────
def render_conversation_item(name: str, preview: str, timestamp: str,
                              status: str, unread: int) -> None:
    status_colours = {
        "open":     ("🟡", "#fef3c7", "#92400e"),
        "active":   ("🟢", "#d1fae5", "#065f46"),
        "closed":   ("⚫", "#f3f4f6", "#374151"),
        "resolved": ("✅", "#d1fae5", "#065f46"),
        "pending":  ("🔵", "#dbeafe", "#1d4ed8"),
    }
    dot, bg, fg = status_colours.get(status.lower(), ("⚪", "#f3f4f6", "#374151"))
    badge = (
        f'<span style="background:#ef4444;color:#fff;border-radius:999px;'
        f'font-size:0.65rem;padding:1px 7px;margin-left:6px;">{unread}</span>'
        if unread else ""
    )

    st.markdown(f"""
    <div class="conv-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="conv-name">📱 {name}{badge}</span>
            <span style="font-size:0.72rem; color:#9ca3af;">{timestamp}</span>
        </div>
        <div class="conv-preview">{preview[:55]}{"…" if len(preview) > 55 else ""}</div>
        <div style="margin-top:4px;">
            <span style="background:{bg}; color:{fg}; border-radius:999px;
                font-size:0.68rem; font-weight:600; padding:2px 8px;">{dot} {status.capitalize()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Duration parser ───────────────────────────────────────
def parse_duration(hms: str) -> str:
    try:
        if not hms or hms == "00:00:00":
            return "—"
        h, m, s = [int(x) for x in hms.split(":")]
        total_min = h * 60 + m + s / 60
        return f"{total_min:.0f} min" if total_min < 60 else f"{total_min/60:.1f} hr"
    except Exception:
        return hms


# ── Timestamp formatter ───────────────────────────────────
def format_timestamp(ts) -> str:
    from datetime import datetime, timedelta
    if not ts:
        return ""
    try:
        if isinstance(ts, (int, float)):
            ts = ts / 1000 if ts > 1e10 else ts
            dt = datetime.fromtimestamp(ts)
        else:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00")).replace(tzinfo=None)
        now = datetime.now()
        if dt.date() == now.date():
            return dt.strftime("%H:%M")
        elif dt.date() == (now - timedelta(days=1)).date():
            return "Yesterday"
        return dt.strftime("%d %b")
    except Exception:
        return str(ts)[:10]


# ── Sidebar renderer ──────────────────────────────────────
def render_sidebar() -> None:
    from utils.auth import logout

    with st.sidebar:
        st.markdown("### 💬 SleekFlow Manager")
        st.divider()

        if st.session_state.get("api_key"):
            st.success("🔑 API Key loaded", icon="✅")
        else:
            st.error("🔑 API Key missing — check your .env file")

        st.divider()

        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪 Sign Out", use_container_width=True):
            logout()
            st.rerun()