# ============================================================
# CHATSELL — WEBHOOK ROUTE
# Entry point for all incoming WhatsApp messages.
# Extracts the message text and phone number then passes
# both to the reply engine. Phone number is important because
# it lets us track where each customer is in the order flow.
# ============================================================

import os
from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse
from services.replies import get_reply, call_grok
from services.whatsapp import send_message

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    verify_token = os.getenv("VERIFY_TOKEN")
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return PlainTextResponse(content=hub_challenge)
    return PlainTextResponse(content="Verification failed", status_code=403)

@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    try:
        changes = data["entry"][0]["changes"][0]["value"]

        if "messages" not in changes:
            return {"status": "ignored"}

        message = changes["messages"][0]
        from_number = message["from"]
        message_text = message["text"]["body"].lower().strip()

        print(f"Message from {from_number}: {message_text}")

        reply, use_grok = get_reply(message_text, from_number)
        
        if use_grok:
            try:
                reply = await call_grok(message_text, from_number)
            except Exception as e:
                print(f"Grok error: {e}")
                reply = "Thank you for reaching out to Noreen's Flowers! You can ask about our collection, prices, delivery or place an order."
        
        await send_message(from_number, reply)

    except Exception as e:
        print(f"Error: {e}")

    return {"status": "received"}
