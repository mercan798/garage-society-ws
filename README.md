# garage-society-ws


# Garage Society

A terminal-style, real-time WebSocket chat application with a strict **2-user limit**,
designed for secure, minimal, hacker-inspired communication.

Built with **FastAPI + WebSockets**, featuring file uploads and a custom terminal UI.

---

## features

-  Real-time WebSocket chat
-  Maximum **2 concurrent users**
-  File upload support (max 10MB)
-  Persistent callsign (localStorage)
-  Terminal-style dark UI
-  No database, no tracking, no logging
-  Designed to run under a domain endpoint (e.g. `/garage-society`)

---

## Tech Stack

- **Backend:** FastAPI
- **Realtime:** WebSockets
- **Frontend:** Vanilla HTML / CSS / JS
- **Uploads:** FastAPI + StaticFiles
- **Proxy:** Nginx (WebSocket upgrade supported)

---

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
