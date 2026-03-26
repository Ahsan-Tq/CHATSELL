# ============================================================
# CHATSELL — REPLY ENGINE
# This is the brain of Chatsell.
# It handles two things:
# 1. Simple keyword replies — price, delivery, location etc.
# 2. Order capture flow — a multi step conversation that
#    collects product, name and address from the customer.
# 
# The order_sessions dictionary is how we remember where
# each customer is in the order flow. Each customer has
# their own phone number as a key so multiple customers
# can order at the same time without mixing up their data.
# ============================================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.database import save_order

order_sessions = {}

def get_reply(message: str, phone_number: str) -> str:

    # ── ORDER FLOW ──
    # If this customer is already in the middle of ordering
    # we skip keyword detection and continue their order flow
    if phone_number in order_sessions:
        return handle_order_flow(message, phone_number)

    # ── KEYWORD DETECTION ──
    price_keywords = ["price", "cost", "kitna", "rate", "pricing", "how much", "charges"]
    delivery_keywords = ["delivery", "deliver", "shipping", "ship", "courier", "time", "kab"]
    available_keywords = ["available", "stock", "in stock", "available?", "hai", "do you have"]
    location_keywords = ["location", "address", "where", "kahan", "pickup", "store"]
    order_keywords = ["order", "buy", "purchase", "want", "chahiye", "lena", "order karna"]

    if any(word in message for word in price_keywords):
        return "Hi! Our prices vary by product. Please tell us which item you're interested in and we'll share the exact price. 😊"

    if any(word in message for word in delivery_keywords):
        return "We deliver all across Pakistan! Delivery takes 2-3 working days. Cash on delivery is available. 🚚"

    if any(word in message for word in available_keywords):
        return "Yes we're open and taking orders! Tell us what you're looking for and we'll check availability for you. ✅"

    if any(word in message for word in location_keywords):
        return "We're an online store operating across Pakistan. No physical store — but we deliver right to your door! 📦"
    
    if any(word in message for word in order_keywords):
        order_sessions[phone_number] = {"step": 1}
        return "Great! Let's place your order. 🛍️\n\nPlease type only the product name you want to order:"

    return "Assalam o Alaikum! Thanks for reaching out. How can we help you today? 😊"


def handle_order_flow(message: str, phone_number: str) -> str:
    session = order_sessions[phone_number]
    step = session["step"]

    if step == 1:
        # Save what they said and ask them to confirm
        order_sessions[phone_number]["product_raw"] = message
        order_sessions[phone_number]["step"] = 2
        return (
            f"You want to order: *{message}*\n\n"
            f"Is this correct? Reply *YES* to confirm or *NO* to change it."
        )

    elif step == 2:
        if message.lower() in ["yes", "haan", "ha", "haa", "ji", "ji haan"]:
            # Confirmed — move to name
            order_sessions[phone_number]["product"] = order_sessions[phone_number]["product_raw"]
            order_sessions[phone_number]["step"] = 3
            return "Great! What's your full name?"
        else:
            # They said no — ask again cleanly
            order_sessions[phone_number]["step"] = 1
            return "No problem! Please type only the product name you want to order:"

    elif step == 3:
        order_sessions[phone_number]["name"] = message
        order_sessions[phone_number]["step"] = 4
        return f"Got it, {message}! 😊\n\nWhat's your delivery address?"

    elif step == 4:
        order_sessions[phone_number]["address"] = message

        product = order_sessions[phone_number]["product"]
        name = order_sessions[phone_number]["name"]
        address = message

        order_sessions.pop(phone_number)
        save_order(phone_number, product, name, address)

        return (
            f"✅ *Order Confirmed!*\n\n"
            f"📦 Product: {product}\n"
            f"👤 Name: {name}\n"
            f"📍 Address: {address}\n\n"
            f"We'll deliver within 2-3 working days. "
            f"Our team will contact you shortly. Thank you! 🙏"
        )

    return "Something went wrong. Type 'order' to start again."
