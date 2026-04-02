# ============================================================
# CHATSELL — MAIN SERVER FILE
# This is the entry point of the entire Chatsell backend.
# When you start the server this is the first file that runs.
# It creates the FastAPI app, connects all the routes (webhook, orders),
# and starts listening for incoming requests.
# Think of this as the front door of the building —
# every request that comes in passes through here first.
# ============================================================

import os
import asyncio
import httpx
from fastapi import FastAPI, Request
from services.replies import get_reply, call_grok

app = FastAPI()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# DEBUG: Print credentials on startup
print("=" * 50)
print("DEBUG: Environment Variables Check")
print(f"WHATSAPP_TOKEN: {'SET' if WHATSAPP_TOKEN else 'MISSING'}")
print(f"PHONE_NUMBER_ID: {PHONE_NUMBER_ID if PHONE_NUMBER_ID else 'MISSING'}")
print("=" * 50)

async def send_message(phone_number: str, message: str):
    """Send message via WhatsApp API"""
    url = f"https://graph.instagram.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # DEBUG: Print request details
    print(f"DEBUG API Call:")
    print(f"  URL: {url}")
    print(f"  Phone: {phone_number}")
    print(f"  Token: {WHATSAPP_TOKEN[:20] if WHATSAPP_TOKEN else 'MISSING'}...")
    print(f"  Payload: {payload}")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        print(f"WhatsApp API response: {response.status_code}")
        if response.status_code != 200:
            print(f"Response body: {response.text}")
        return response

@app.post("/webhook")
async def webhook(request: Request):
    """Receive messages from WhatsApp"""
    data = await request.json()
    
    messages = data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("messages", [])
    
    if not messages:
        return {"status": "ok"}
    
    message_data = messages[0]
    phone_number = message_data.get("from")
    message_text = message_data.get("text", {}).get("body", "").strip()
    
    if not message_text:
        return {"status": "ok"}
    
    print(f"Message from {phone_number}: {message_text}")
    
    reply_text, is_async = get_reply(message_text, phone_number)
    
    if is_async:
        try:
            reply_text = await call_grok(message_text, phone_number)
        except Exception as e:
            print(f"Grok error: {e}")
            reply_text = (
                "Thank you for reaching out to Noreen's Flowers!\n\n"
                "You can ask about our collection, prices, delivery or place an order."
            )
    
    await send_message(phone_number, reply_text)
    
    return {"status": "ok", "message_sent": reply_text}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """WhatsApp webhook verification"""
    verify_token = "your_verify_token"
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == verify_token:
        return int(challenge)
    
    return {"status": "forbidden"}, 403
