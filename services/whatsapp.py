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


async def send_message(to: str, message: str):
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")

    if not whatsapp_token:
        raise ValueError("WHATSAPP_TOKEN is missing in .env")

    if not phone_number_id:
        raise ValueError("PHONE_NUMBER_ID is missing in .env")

    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        print("WhatsApp status:", response.status_code)
        print("WhatsApp response:", response.text)
        response.raise_for_status()
        return response.json()
