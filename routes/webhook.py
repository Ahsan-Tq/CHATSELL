# ============================================================
# CHATSELL — WEBHOOK ROUTE
# Entry point for all incoming WhatsApp messages.
# Extracts the message text and phone number then passes
# both to the reply engine. Phone number is important because
# it lets us track where each customer is in the order flow.
# ============================================================

@router.post("/webhook")
async def receive_message(request: Request):
    try:
        data = await request.json()
        print("Incoming webhook data:", data)

        changes = data["entry"][0]["changes"][0]["value"]

        if "messages" not in changes:
            return {"status": "ignored"}

        message = changes["messages"][0]
        from_number = message.get("from")
        message_type = message.get("type")

        if message_type != "text":
            print(f"Ignored non-text message: {message_type}")
            return {"status": "ignored - non-text"}

        message_text = message.get("text", {}).get("body", "").lower().strip()

        if not message_text:
            return {"status": "ignored - empty text"}

        print(f"Message from {from_number}: {message_text}")

        reply, use_grok = get_reply(message_text, from_number)

        if use_grok:
            try:
                reply = await call_grok(message_text, from_number)
            except Exception as e:
                print(f"Grok error: {e}")
                reply = "Thank you for reaching out to Noreen's Flowers! You can ask about our collection, prices, delivery or place an order."

        await send_message(from_number, reply)
        return {"status": "received"}

    except Exception as e:
        print(f"Error in webhook: {e}")
        return {"status": "error", "detail": str(e)}

