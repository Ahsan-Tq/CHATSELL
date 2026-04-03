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
from datetime import datetime

order_sessions = {}

flower_catalog = [
    {
        "name": "Red Roses Bouquet",
        "price": "PKR 1,200",
        "aliases": ["red roses", "roses", "rose bouquet"],
    },
    {
        "name": "White Lilies Bunch",
        "price": "PKR 950",
        "aliases": ["white lilies", "lilies", "lily bunch"],
    },
    {
        "name": "Sunflower Arrangement",
        "price": "PKR 1,500",
        "aliases": ["sunflower", "sunflowers", "sunflower arrangement"],
    },
    {
        "name": "Mixed Seasonal Bouquet",
        "price": "PKR 1,800",
        "aliases": ["mixed seasonal", "seasonal bouquet", "mixed bouquet"],
    },
    {
        "name": "Pink Tulips Bunch",
        "price": "PKR 1,100",
        "aliases": ["pink tulips", "tulips", "tulip bunch"],
    },
    {
        "name": "Lavender Dream Bouquet",
        "price": "PKR 2,000",
        "aliases": ["lavender", "lavender dream", "purple bouquet"],
    },
]


def format_catalog() -> str:
    lines = ["*Noreen's Flowers — Our Collection:*", ""]
    for flower in flower_catalog:
        lines.append(f"• {flower['name']} — {flower['price']}")
    return "\n".join(lines)


def match_product(message: str):
    message_lower = message.lower().strip()

    for flower in flower_catalog:
        if flower["name"].lower() in message_lower:
            return flower

    for flower in flower_catalog:
        for alias in flower["aliases"]:
            if alias in message_lower:
                return flower

    words = [word for word in message_lower.split() if len(word) > 2]
    best_match = None
    best_score = 0

    for flower in flower_catalog:
        searchable_text = " ".join([flower["name"].lower()] + flower["aliases"])
        score = sum(1 for word in words if word in searchable_text)
        if score > best_score:
            best_score = score
            best_match = flower

    if best_score >= 1:
        return best_match

    return None


def build_order_id(phone_number: str) -> str:
    phone_suffix = phone_number[-4:] if phone_number else "0000"
    timestamp = datetime.now().strftime("%H%M%S")
    return f"ORD-{phone_suffix}-{timestamp}"


def save_order_to_db(phone_number: str, product: str, customer_name: str, address: str):
    try:
        from modules.database import save_order
        return save_order(
            phone_number=phone_number,
            product=product,
            name=customer_name,
            address=address
        )
    except Exception as e:
        print(f"Save order error: {e}")
        return None


def handle_order_flow(message: str, phone_number: str) -> str:
    session = order_sessions.get(phone_number, {})
    step = session.get("step")
    message_lower = message.lower().strip()

    yes_words = ["yes", "y", "confirm", "correct", "ok", "okay", "haan", "han", "ji"]
    no_words = ["no", "n", "change", "wrong", "nahi", "nah"]

    if step == "choose_product":
        matched = match_product(message)
        if matched:
            session["product"] = matched["name"]
            session["step"] = "confirm_product"
            order_sessions[phone_number] = session
            return (
                f"You'd like to order: *{matched['name']}*\n\n"
                "Reply *YES* to confirm or *NO* to change it."
            )

        return (
            "I could not find that in our catalog.\n\n"
            f"{format_catalog()}\n\n"
            "Please type the bouquet name you'd like to order."
        )

    if step == "confirm_product":
        if any(word in message_lower for word in yes_words):
            session["step"] = "ask_name"
            order_sessions[phone_number] = session
            return "Great. Please send your name for the order."

        if any(word in message_lower for word in no_words):
            session["step"] = "choose_product"
            order_sessions[phone_number] = session
            return (
                f"{format_catalog()}\n\n"
                "Please type the bouquet name you'd like to order."
            )

        matched = match_product(message)
        if matched:
            session["product"] = matched["name"]
            session["step"] = "confirm_product"
            order_sessions[phone_number] = session
            return (
                f"You'd like to order: *{matched['name']}*\n\n"
                "Reply *YES* to confirm or *NO* to change it."
            )

        return "Please reply *YES* to confirm or *NO* to choose another bouquet."

    if step == "ask_name":
        session["customer_name"] = message.strip()
        session["step"] = "ask_address"
        order_sessions[phone_number] = session
        return "Got it. Now please send your delivery address."

    if step == "ask_address":
        session["address"] = message.strip()

        product = session.get("product", "Unknown Product")
        customer_name = session.get("customer_name", "Customer")
        address = session.get("address", "")
        order_id = build_order_id(phone_number)

        save_order_to_db(
            phone_number=phone_number,
            product=product,
            customer_name=customer_name,
            address=address
        )

        order_sessions.pop(phone_number, None)

        return (
            f"Thank you, {customer_name}. Your order for *{product}* has been noted.\n\n"
            f"Order number: *{order_id}*\n"
            "Our team will follow up with you shortly."
        )

    order_sessions.pop(phone_number, None)
    return (
        "Let's start your order again.\n\n"
        f"{format_catalog()}\n\n"
        "Please type the bouquet name you'd like to order."
    )


async def call_grok(message: str, phone_number: str, context: str = "") -> str:
    grok_api_key = os.getenv("GROK_API_KEY")
    grok_api_url = "https://api.x.ai/v1/chat/completions"

    if not grok_api_key:
        return (
            "Thank you for reaching out to Noreen's Flowers.\n\n"
            "You can ask about our collection, prices, delivery or place an order."
        )

    session_context = order_sessions.get(phone_number, {})
    catalog_text = format_catalog()

    system_prompt = f"""
You are a WhatsApp customer support assistant for Noreen's Flowers in Pakistan.

Rules:
1. Keep replies short and natural for WhatsApp.
2. Be helpful and professional.
3. Use only the catalog prices provided below.
4. If a product is not available, politely say so and suggest the closest available product.
5. Do not invent products or prices.
6. If the customer wants to order, guide them toward choosing one item from the catalog.

Catalog:
{catalog_text}

Delivery details:
- Delivery in 4 to 5 working days across Pakistan
- Cash on Delivery available
- Free gift wrapping

Customer phone:
{phone_number}

Session context:
{session_context}

Extra context:
{context}
""".strip()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                grok_api_url,
                headers={
                    "Authorization": f"Bearer {grok_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "grok-beta",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 150,
                },
            )

            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"Grok API error: {e}")
        return (
            "Sorry, I could not process that properly.\n\n"
            "You can ask about our collection, prices, delivery or place an order."
        )


def get_reply(message: str, phone_number: str) -> tuple[str, bool]:
    message_lower = message.lower().strip()
    words = message_lower.split()

    if phone_number in order_sessions:
        return handle_order_flow(message, phone_number), False

    greet_words = ["hi", "hello", "hey", "aoa", "salam", "hii", "helo"]
    price_keywords = [
        "price", "cost", "how much", "rate", "pricing", "daam", "qeemat",
        "catalog", "catalogue", "menu", "collection", "products", "flowers"
    ]
    delivery_keywords = [
        "delivery", "deliver", "shipping", "ship", "courier", "time",
        "days", "kab", "kitne din"
    ]
    order_keywords = [
        "order", "buy", "purchase", "book", "chahiye", "want", "need", "send"
    ]
    yes_keywords = ["yes", "haan", "han", "ji", "ok", "okay"]

    if any(word in words for word in greet_words) or "assalam" in message_lower:
        return (
            "Assalam o Alaikum. Welcome to *Noreen's Flowers*.\n\n"
            "You can ask about our collection, prices, delivery or place an order.",
            False,
        )

    if any(keyword in message_lower for keyword in price_keywords):
        return format_catalog(), False

    if any(keyword in message_lower for keyword in delivery_keywords):
        return (
            "We deliver across Pakistan in 4 to 5 working days.\n"
            "Cash on Delivery is available, and gift wrapping is free.",
            False,
        )

    if any(keyword in message_lower for keyword in order_keywords):
        matched = match_product(message)
        if matched:
            order_sessions[phone_number] = {
                "step": "confirm_product",
                "product": matched["name"],
            }
            return (
                f"You'd like to order: *{matched['name']}*\n\n"
                "Reply *YES* to confirm or *NO* to change it.",
                False,
            )

        order_sessions[phone_number] = {"step": "choose_product"}
        return (
            f"{format_catalog()}\n\n"
            "Please type the bouquet name you'd like to order."
        ), False

    if message_lower in yes_keywords:
        order_sessions[phone_number] = {"step": "choose_product"}
        return (
            f"{format_catalog()}\n\n"
            "Please type the bouquet name you'd like to order."
        ), False

    matched = match_product(message)
    if matched:
        order_sessions[phone_number] = {
            "step": "confirm_product",
            "product": matched["name"],
        }
        return (
            f"You'd like to order: *{matched['name']}*\n\n"
            "Reply *YES* to confirm or *NO* to change it.",
            False,
        )

    return message, True
