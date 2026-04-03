# ============================================================
# CHATSELL — WHATSAPP SERVICE
# This file handles sending messages back to customers.
# When the reply engine decides what to say, this file
# actually sends it through the WhatsApp API.
# It takes the customer's phone number and the reply text
# and fires it off to Meta's servers.
# ============================================================

import os
import httpx

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


async def send_message(to: str, message: str):
    if not WHATSAPP_TOKEN:
        raise ValueError("WHATSAPP_TOKEN is missing in .env")

    if not PHONE_NUMBER_ID:
        raise ValueError("PHONE_NUMBER_ID is missing in .env")

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        print("WhatsApp status:", response.status_code)
        print("WhatsApp response:", response.text)
        response.raise_for_status()
