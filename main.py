import os
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

from models import Base, Product
from session import engine, SessionLocal
import random
from ai.ai import BusinessAdvisorAgent

user_histories = {}

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

Base.metadata.create_all(bind=engine)

ai_agent = BusinessAdvisorAgent()


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
    sender = form_dict.get("From")
    user_message = form_dict.get("Body")

    chat_history = user_histories.get(sender, [])

    ai_response, updated_history = ai_agent.handle_query(user_message, chat_history)
    user_histories[sender] = updated_history

    if (
        TWILIO_ACCOUNT_SID
        and TWILIO_AUTH_TOKEN
        and TWILIO_WHATSAPP_NUMBER
        and sender
        and ai_response
    ):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        try:
            message = client.messages.create(
                body=ai_response, from_=TWILIO_WHATSAPP_NUMBER, to=sender
            )
            print(f"Sent message SID: {message.sid}")
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")

    return JSONResponse(
        content={
            "message": "done",
            "body": user_message,
            "ai_response": ai_response,
            "form": form_dict,
            "history": updated_history,
        }
    )


@app.post("/seed")
def seed_products():
    session = SessionLocal()
    product_data = [
        {
            "name": "Apple iPhone 14 Pro",
            "description": "Latest Apple flagship smartphone with advanced camera and display.",
        },
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "Premium Android phone with high-res camera and S Pen support.",
        },
        {
            "name": "Sony WH-1000XM5 Headphones",
            "description": "Industry-leading noise cancelling wireless headphones.",
        },
        {
            "name": "Dell XPS 13 Laptop",
            "description": "Ultra-portable laptop with InfinityEdge display and long battery life.",
        },
        {
            "name": "Apple MacBook Air M2",
            "description": "Lightweight laptop with Apple Silicon for fast performance.",
        },
        {
            "name": "GoPro HERO11 Black",
            "description": "Waterproof action camera with 5.3K video and stabilization.",
        },
        {
            "name": "Nintendo Switch OLED",
            "description": "Versatile gaming console with vibrant OLED display.",
        },
        {
            "name": "Fitbit Charge 5",
            "description": "Advanced fitness tracker with built-in GPS and health metrics.",
        },
        {
            "name": "Canon EOS R10 Camera",
            "description": "Mirrorless camera for creators with fast autofocus.",
        },
        {
            "name": "Bose SoundLink Revolve+",
            "description": "Portable Bluetooth speaker with 360° sound.",
        },
        {
            "name": "Kindle Paperwhite",
            "description": "Waterproof e-reader with high-resolution display.",
        },
        {
            "name": "Logitech MX Master 3S Mouse",
            "description": "Ergonomic wireless mouse for productivity.",
        },
        {
            "name": "Samsung T7 Portable SSD",
            "description": "High-speed external SSD for fast file transfers.",
        },
        {
            "name": "JBL Flip 6 Speaker",
            "description": "Rugged portable speaker with powerful sound.",
        },
        {
            "name": "Apple Watch Series 8",
            "description": "Smartwatch with health sensors and crash detection.",
        },
        {
            "name": "Anker PowerCore 20000",
            "description": "High-capacity portable charger for devices on the go.",
        },
        {
            "name": "Razer BlackWidow V4 Keyboard",
            "description": "Mechanical gaming keyboard with RGB lighting.",
        },
        {
            "name": "Philips Hue Starter Kit",
            "description": "Smart lighting kit with color-changing bulbs.",
        },
        {
            "name": "DJI Mini 3 Pro Drone",
            "description": "Compact drone with 4K camera and obstacle avoidance.",
        },
        {
            "name": "Instant Pot Duo 7-in-1",
            "description": "Multi-use pressure cooker for easy home meals.",
        },
    ]
    products = []
    for data in product_data:
        product = Product(
            name=data["name"],
            description=data["description"],
            price=round(random.uniform(50, 2000), 2),
            stock=random.randint(5, 100),
        )
        products.append(product)
    session.add_all(products)
    session.commit()
    session.close()
    return {"message": "products added."}
