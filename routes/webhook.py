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
    hub_mode: str = Query(default=None, alias="hub.mode"),
    hub_challenge: str = Query(default=None, alias="hub.challenge"),
    hub_verify_token: str = Query(default=None, alias="hub.verify_token"),
):
    verify_token = os.getenv("VERIFY_TOKEN")

    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return PlainTextResponse(content=hub_challenge or "")

    return PlainTextResponse(content="Verification failed", status_code=403)


@router.post("/webhook")
async def receive_message(request: Request):
    try:
        data = await request.json()
        print("Incoming webhook data:", data)

        entry = data.get("entry", [])
        if not entry:
            return {"status": "ignored - no entry"}

        changes = entry[0].get("changes", [])
        if not changes:
            return {"status": "ignored - no changes"}

        value = changes[0].get("value", {})
        messages = value.get("messages", [])
        if not messages:
            return {"status": "ignored - no messages"}

        message_obj = messages[0]
        from_number = message_obj.get("from")
        message_type = message_obj.get("type")

        if not from_number:
            return {"status": "ignored - no sender"}

        if message_type != "text":
            print(f"Ignored non-text message: {message_type}")
            return {"status": f"ignored - {message_type}"}

        message_text = message_obj.get("text", {}).get("body", "").strip()

        if not message_text:
            return {"status": "ignored - empty text"}

        print(f"Message from {from_number}: {message_text}")

        reply, use_grok = get_reply(message_text, from_number)

        if use_grok:
            try:
                reply = await call_grok(message_text, from_number)
            except Exception as e:
                print(f"Grok error: {e}")
                reply = (
                    "Thank you for reaching out to Noreen's Flowers. "
                    "You can ask about our collection, prices, delivery or place an order."
                )

        await send_message(from_number, reply)
        return {"status": "received"}

    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "detail": str(e)}
