# Nexus IVR Backend (FastAPI)

This is the backend for the Nexus IVR application, built with FastAPI (Python). It will handle:
- Automated call answering (via Twilio integration)
- Question handling and FAQ logic
- Admin endpoints for call logs and FAQ management

## Setup

1. Create a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install fastapi uvicorn twilio
   ```
3. Run the server:
   ```sh
   uvicorn main:app --reload
   ```

## Endpoints (to be implemented)
- `/ivr/answer` — Twilio webhook for answering calls
- `/ivr/faq` — Endpoint for managing FAQs
- `/ivr/logs` — Endpoint for retrieving call logs
