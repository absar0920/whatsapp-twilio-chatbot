import os
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})

@app.post("/callback")
async def callback(request: Request, Body: Optional[str] = Form(None)):
    form = await request.form()
    form_dict = dict(form)
    print("Received form:", form_dict)
    sender = form_dict.get("From")
    print("Message body: ", form_dict.get("Body"))

    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_WHATSAPP_NUMBER and sender:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        try:
            message = client.messages.create(
                body="Hello from FastAPI!",
                from_=TWILIO_WHATSAPP_NUMBER,
                to=sender
            )
            print(f"Sent message SID: {message.sid}")
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")

    return JSONResponse(content={"message": "done", "body": Body, "form": form_dict})
