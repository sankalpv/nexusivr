from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.voice_response import VoiceResponse
from typing import List, Dict
import uuid
import os
import openai
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
faqs: List[Dict] = [
    {"id": str(uuid.uuid4()), "question": "What are your hours?", "answer": "We are open 9am to 5pm, Monday to Friday."},
    {"id": str(uuid.uuid4()), "question": "Where are you located?", "answer": "We are located at 123 Main St."}
]
logs: List[Dict] = []

# Set your OpenAI API key as an environment variable: OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

async def ai_answer(question: str) -> str:
    if not openai.api_key:
        return "AI answering is not configured."
    # Use FAQ matching first
    for faq in faqs:
        if faq["question"].lower() in question.lower():
            return faq["answer"]
    # Fallback to OpenAI
    try:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an IVR assistant. Answer concisely."},
                {"role": "user", "content": question}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"AI error: {e}"

@app.post("/ivr/answer", response_class=PlainTextResponse)
async def answer_call(request: Request):
    """
    Webhook endpoint for Twilio to answer incoming calls.
    Responds with TwiML instructions.
    """
    response = VoiceResponse()
    response.say("Welcome to the Nexus IVR. Please ask your question after the beep.")
    response.record(maxLength=30, action="/ivr/handle-recording", method="POST")
    return str(response)

@app.post("/ivr/handle-recording", response_class=PlainTextResponse)
async def handle_recording(request: Request):
    """
    Handles the recording and responds with a placeholder answer.
    """
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    caller = form.get("From")
    transcription = form.get("TranscriptionText")
    log_entry = {
        "id": str(uuid.uuid4()),
        "caller": caller,
        "recording_url": recording_url,
        "transcription": transcription
    }
    logs.append(log_entry)
    response = VoiceResponse()
    answer = ""
    if transcription:
        answer = await ai_answer(transcription)
        response.say(answer)
    else:
        response.say("Thank you. Your question has been received. Goodbye.")
    response.hangup()
    return str(response)

@app.get("/ivr/faq")
async def get_faq():
    """
    Retrieve all FAQs.
    """
    return {"faqs": faqs}

@app.post("/ivr/faq")
async def add_faq(question: str = Form(...), answer: str = Form(...)):
    """
    Add a new FAQ.
    """
    faq = {"id": str(uuid.uuid4()), "question": question, "answer": answer}
    faqs.append(faq)
    return {"success": True, "faq": faq}

@app.delete("/ivr/faq/{faq_id}")
async def delete_faq(faq_id: str):
    """
    Delete an FAQ by ID.
    """
    global faqs
    faqs = [f for f in faqs if f["id"] != faq_id]
    return {"success": True}

@app.get("/ivr/logs")
async def get_logs():
    """
    Retrieve call logs.
    """
    return {"logs": logs}

@app.delete("/ivr/logs/{log_id}")
async def delete_log(log_id: str):
    """
    Delete a log entry by ID.
    """
    global logs
    logs = [l for l in logs if l["id"] != log_id]
    return {"success": True}
