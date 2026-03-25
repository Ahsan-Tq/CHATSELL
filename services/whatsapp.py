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

async def send_message(to: str, text: str):
    token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")

    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": "text",
        "text": { "body": text }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        print(f"WhatsApp API response: {response.status_code}")

        