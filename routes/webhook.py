# ============================================================
# CHATSELL — WEBHOOK ROUTE
# This file is the entry point for all WhatsApp messages.
# When a customer sends a message, Meta sends it here first.
# We extract the message text and phone number from the data
# then pass it to the reply engine to figure out what to send back.
# ============================================================

import os
from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse
from services.replies import get_reply
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

        reply = get_reply(message_text)
        await send_message(from_number, reply)

    except Exception as e:
        print(f"Error: {e}")

    return {"status": "received"}