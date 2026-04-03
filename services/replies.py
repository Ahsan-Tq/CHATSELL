# ============================================================
# CHATSELL — REPLY ENGINE
# This is the brain of Chatsell.
# It handles two things:
# 1. Keyword replies — price, delivery, location etc.
#    These are tied to Noreen's Flowers demo store.
# 2. Order capture flow — multi step conversation that
#    collects product, name and address from the customer.
#
# The order_sessions dictionary tracks where each customer
# is in the order flow using their phone number as the key.
# The flower_catalog is a simple built-in product database.
# When a customer mentions a product we fuzzy match it against
# the catalog so partial names like "pink tulips" still work.
# ============================================================

import os
import httpx
from modules.database import save_order

# Grok API configuration
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

order_sessions = {}

flower_catalog = [
    {"name": "Red Roses Bouquet", "price": "PKR 1,200"},
    {"name": "White Lilies Bunch", "price": "PKR 950"},
    {"name": "Sunflower Arrangement", "price": "PKR 1,500"},
    {"name": "Mixed Seasonal Bouquet", "price": "PKR 1,800"},
    {"name": "Pink Tulips Bunch", "price": "PKR 1,100"},
    {"name": "Lavender Dream Bouquet", "price": "PKR 2,000"},
]


def format_catalog() -> str:
    catalog_text = "*Noreen's Flowers — Our Collection:*\n\n"
    for flower in flower_catalog:
        catalog_text += f"• {flower['name']} — {flower['price']}\n"
    return catalog_text


def match_product(message: str):
    message_lower = message.lower()

    full_match = next(
        (f for f in flower_catalog if f["name"].lower() in message_lower),
        None
    )
    if full_match:
        return full_match

    partial_match = next(
        (
            f for f in flower_catalog
            if any(word in f["name"].lower() for word in message_lower.split() if len(word) > 2)
        ),
        None
    )
    return partial_match


async def call_grok(message: str, phone_number: str, context: str = "") -> str:
    """
    Call Grok API to handle out-of-flow messages.
    Context includes customer history and catalog info.
    """
    if not GROK_API_KEY:
        return (
            "Thank you for reaching out to Noreen's Flowers.\n\n"
            "You can ask about our collection, prices, delivery or place an order.\n\n"
            "How can we help?"
        )

    system_prompt = f"""You are a WhatsApp customer service bot for Noreen's Flowers, a flower shop in Pakistan.

IMPORTANT RULES:
1. Keep responses short (2-3 sentences max for WhatsApp)
2. Always be friendly and professional
3. Suggest relevant flowers from our catalog when possible
4. If customer asks about products NOT in catalog, politely decline and suggest alternatives
5. Encourage orders by showing catalog when relevant
6. Do NOT generate prices - only use catalog prices
7. Speak Urdu-friendly English (use "Assalam o Alaikum", "Inshallah", etc when appropriate)

OUR CATALOG:
{format_catalog()}

DELIVERY INFO:
- Delivery: 4-5 working days across Pakistan
- Cash on Delivery available
- Free gift wrapping

Customer Message: {message}
Previous Context: {context}

Respond naturally as if you're a helpful flower shop assistant. Keep it conversational."""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GROK_API_URL,
                headers={
                    "Authorization": f"Bearer {GROK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                timeout=10.0
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return format_catalog() + "\nHow can we help?"

    except Exception as e:
        print(f"Grok API error: {e}")
        return format_catalog() + "\nHow can we help?"


def handle_order_flow(message: str, phone_number: str) -> str:
    session = order_sessions[phone_number]
    step = session["step"]
    message_clean = message.strip()
    message_lower = message_clean.lower()

    if step == 1:
        matched = match_product(message_clean)
        if matched:
            order_sessions[phone_number]["product_raw"] = matched["name"]
            order_sessions[phone_number]["step"] = 2
            return (
                f"You'd like to order: *{matched['name']}*\n\n"
                f"Is this correct? Reply *YES* to confirm or *NO* to change it."
            )
        else:
            return (
                "Sorry, we don't have that item. Here's what we offer:\n\n"
                + format_catalog()
                + "\nWhich bouquet would you like?"
            )

    elif step == 2:
        yes_keywords = ["yes", "haan", "ha", "haa", "ji", "ji haan", "yep", "yup", "yeah", "sure", "bilkul"]

        if message_lower in yes_keywords:
            product_raw = order_sessions[phone_number]["product_raw"]
            matched = match_product(product_raw)

            if not matched:
                order_sessions[phone_number]["step"] = 1
                return (
                    "Sorry, we couldn't find that in our collection. Please choose from below:\n\n"
                    + format_catalog()
                    + "\nPlease type the bouquet name:"
                )

            order_sessions[phone_number]["product"] = matched["name"]
            order_sessions[phone_number]["step"] = 3
            return f"Perfect! *{matched['name']}* it is.\n\nHow many would you like to order?"

        else:
            order_sessions[phone_number]["step"] = 1
            return (
                "No problem! Please type the name of the bouquet you'd like:\n\n"
                + format_catalog()
            )

    elif step == 3:
        if not message_clean.isdigit() or int(message_clean) <= 0:
            return "Please enter a valid quantity, for example: 1, 2, or 3."

        order_sessions[phone_number]["quantity"] = int(message_clean)
        order_sessions[phone_number]["step"] = 4
        return "Got it. What's your full name?"

    elif step == 4:
        order_sessions[phone_number]["name"] = message_clean
        order_sessions[phone_number]["step"] = 5
        return f"Got it, {message_clean}! What's your delivery address?"

    elif step == 5:
        order_sessions[phone_number]["address"] = message_clean

        product = order_sessions[phone_number]["product"]
        quantity = order_sessions[phone_number]["quantity"]
        name = order_sessions[phone_number]["name"]
        address = message_clean

        order_sessions.pop(phone_number)

        save_order(phone_number, product, quantity, name, address)

        return (
            f"Order Confirmed!\n\n"
            f"Bouquet: {product}\n"
            f"Quantity: {quantity}\n"
            f"Name: {name}\n"
            f"Address: {address}\n\n"
            f"Your flowers will be delivered in 4-5 working days.\n"
            f"Our team will contact you shortly. Thank you for choosing Noreen's Flowers!"
        )

    return "Something went wrong. Type 'order' to start again."


def get_reply(message: str, phone_number: str) -> tuple[str, bool]:
    """
    Returns (reply_text, is_async)
    is_async = True means this reply needs async execution (Grok call)
    """

    message = message.strip()

    # ORDER FLOW
    if phone_number in order_sessions:
        return (handle_order_flow(message, phone_number), False)

    # FIRST MESSAGE GREETING
    greet_keywords = ["hi", "hello", "hii", "helo", "aoa", "assalam", "salam", "hey"]
    if any(word in message.lower() for word in greet_keywords):
        return (
            "Assalam o Alaikum! Welcome to *Noreen's Flowers* \n\n"
            "We deliver fresh flowers across Pakistan.\n\n"
            "You can ask about our collection, prices, delivery or place an order.\n\n"
            "How can I help you today?",
            False
        )

    # KEYWORD DETECTION
    price_keywords = ["price", "cost", "kitna", "rate", "pricing", "how much", "charges", "daam", "qeemat", "collection", "products", "flowers", "kya hai", "menu"]
    delivery_keywords = ["delivery", "deliver", "shipping", "ship", "courier", "time", "kab", "kitne din", "days"]
    available_keywords = ["available", "stock", "in stock", "hai", "do you have", "milega", "milegi"]
    location_keywords = ["location", "address", "where", "kahan", "pickup", "store", "shop"]
    order_keywords = ["order", "buy", "purchase", "want", "chahiye", "lena", "order karna", "leni hai", "booking"]
    yes_keywords = ["yes", "haan", "ha", "haa", "ji", "ji haan", "yep", "yup", "yeah", "sure", "bilkul"]

    message_lower = message.lower()

    if any(word in message_lower for word in price_keywords):
        return (
            format_catalog()
            + "\nAll bouquets are freshly prepared on order. Which one would you like?",
            False
        )

    if any(word in message_lower for word in delivery_keywords):
        return (
            "We deliver all across Pakistan \n\n"
            "• Delivery time: 4-5 working days\n"
            "• Cash on delivery available\n"
            "• Free gift wrapping on all orders\n\n"
            "Want to place an order?",
            False
        )

    if any(word in message_lower for word in available_keywords):
        return (
            "Yes, all our flowers are available and freshly prepared on order!\n\n"
            + format_catalog()
            + "\nWhich bouquet would you like?",
            False
        )

    if any(word in message_lower for word in location_keywords):
        return (
            "We are an online flower shop \n\n"
            "We deliver fresh flowers right to your doorstep across all of Pakistan.\n"
            "No need to visit — just order and we'll handle the rest!",
            False
        )

    if any(word in message_lower for word in order_keywords):
        matched = match_product(message)
        if matched:
            order_sessions[phone_number] = {"step": 2, "product_raw": matched["name"]}
            return (
                f"You'd like to order: *{matched['name']}*\n\n"
                f"Is this correct? Reply *YES* to confirm or *NO* to change it.",
                False
            )
        else:
            order_sessions[phone_number] = {"step": 1}
            return (
                "Let's place your order!\n\n"
                + format_catalog()
                + "\nPlease type the name of the bouquet you'd like to order:",
                False
            )

    if any(word in message_lower for word in yes_keywords):
        order_sessions[phone_number] = {"step": 1}
        return (
            "Let's place your order!\n\n"
            + format_catalog()
            + "\nPlease type the name of the bouquet you'd like to order:",
            False
        )

    matched = match_product(message)
    if matched:
        order_sessions[phone_number] = {"step": 2, "product_raw": matched["name"]}
        return (
            f"You'd like to order: *{matched['name']}*\n\n"
            f"Is this correct? Reply *YES* to confirm or *NO* to change it.",
            False
        )

    # OUT OF FLOW: USE GROK
    return (message, True)
