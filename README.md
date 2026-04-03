# SleekFlow Manager — Streamlit App

A dashboard + WhatsApp inbox for SleekFlow API v2.

## Features
- 🔐 Password-protected login
- 📊 Dashboard: KPIs, channel breakdown, team performance, conversation volume chart
- 📥 WhatsApp Inbox: conversation list, message thread, reply from UI

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Change the app password
Open `app.py` and find this line near the top:
```python
APP_PASSWORD = ""
```
Replace with your own password, or move it to Streamlit Secrets (recommended for production).

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Enter your API key
- Open the app in your browser (default: http://localhost:8501)
- Log in with the password
- Paste your SleekFlow API v2 key in the sidebar

## Getting your SleekFlow API Key
1. Log in to SleekFlow
2. Go to **Settings → API / Integrations**
3. Copy your API key


## API Endpoints Used
| Feature | Endpoint |
|---|---|
| Analytics | `GET /api/analytics` |
| Conversations list | `GET /conversation` |
| Messages in thread | `GET /conversation/{id}/message` |
| Send WhatsApp message | `POST /message/send/whatsapp` |
| Contact count | `GET /contact` |
| Team members | `GET /company/member` |
