# Twilio Webhook Setup for Nexus IVR

To connect Twilio to your FastAPI backend:

1. **Expose your local FastAPI server to the internet** (for Twilio to reach it):
   - Use [ngrok](https://ngrok.com/) or similar:
     ```sh
     ngrok http 8000
     ```
   - Note the HTTPS forwarding URL (e.g., `https://xxxx.ngrok.io`).

2. **Configure Twilio Voice Webhook:**
   - In your Twilio Console, go to your phone number settings.
   - Set the Voice webhook (for incoming calls) to:
     ```
     https://xxxx.ngrok.io/ivr/answer
     ```
   - Use HTTP POST method.

3. **Test the flow:**
   - Call your Twilio number. You should hear the IVR greeting and be able to record a question.

---

**Endpoints:**
- `/ivr/answer` — Handles incoming calls (Twilio webhook)
- `/ivr/handle-recording` — Handles the recording after the beep

**Note:**
- Make sure your FastAPI server is running and accessible via the ngrok URL whenever you want to test with Twilio.
- You can extend `/ivr/handle-recording` to process the recording, transcribe, and answer questions automatically.
