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
from datetime import datetime
from difflib import get_close_matches

import httpx

from modules.database import save_order

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
    lines = ["*Noreen's Flowers - Our Collection:*", ""]
    for flower in flower_catalog:
        lines.append(f"- {flower['name']} - {flower['price']}")
    return "\n".join(lines)


def get_catalog_names():
    return [flower["name"] for flower in flower_catalog]


def find_similar_products(message: str, limit: int = 2):
    search_pool = []
    alias_to_product = {}

    for flower in flower_catalog:
        search_pool.append(flower["name"].lower())
        alias_to_product[flower["name"].lower()] = flower

        for alias in flower["aliases"]:
            search_pool.append(alias.lower())
            alias_to_product[alias.lower()] = flower

    close = get_close_matches(message.lower().strip(), search_pool, n=limit, cutoff=0.4)

    seen = set()
    results = []

    for item in close:
        product = alias_to_product[item]
        if product["name"] not in seen:
            seen.add(product["name"])
            results.append(product)

    return results


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
        searchable_text = " ".join([flower["name"].lower()] + [a.lower() for a in flower["aliases"]])
        score = sum(1 for word in words if word in searchable_text)
        if score > best_score:
            best_score = score
            best_match = flower

    if best_score >= 1:
        return best_match

    similar = find_similar_products(message_lower, limit=1)
    if similar:
        return similar[0]

    return None


def is_flower_related(message: str) -> bool:
    flower_terms = [
        "flower", "flowers", "bouquet", "bouquets",
        "rose", "roses", "lily", "lilies",
        "sunflower", "sunflowers", "tulip", "tulips",
        "lavender", "seasonal", "bunch", "arrangement"
    ]
    return any(term in message for term in flower_terms)


def is_order_intent(message: str) -> bool:
    strong_order_terms = [
        "order", "buy", "purchase", "book", "place order"
    ]

    soft_order_terms = [
        "want", "need", "send", "chahiye"
    ]

    if any(term in message for term in strong_order_terms):
        return True

    if any(term in message for term in soft_order_terms) and is_flower_related(message):
        return True

    return False


def build_order_id(phone_number: str) -> str:
    phone_suffix = phone_number[-4:] if phone_number else "0000"
    timestamp = datetime.now().strftime("%H%M%S")
    return f"ORD-{phone_suffix}-{timestamp}"


def safe_save_order(phone_number: str, product: str, customer_name: str, address: str):
    try:
        result = save_order(
            phone_number=phone_number,
            product=product,
            name=customer_name,
            address=address
        )
        print("Order saved:", result)
        return result
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
                f"You want *{matched['name']}*.\n\n"
                "Reply *YES* to confirm or *NO* to choose another one."
            )

        similar = find_similar_products(message)
        if similar:
            suggestions = "\n".join([f"- {item['name']} - {item['price']}" for item in similar])
            return (
                "I could not find that exact item.\n\n"
                "Closest available options:\n"
                f"{suggestions}\n\n"
                "Type the product name you want."
            )

        return (
            "That item is not available right now.\n\n"
            f"{format_catalog()}\n\n"
            "Please type the bouquet name you want."
        )

    if step == "confirm_product":
        if any(word == message_lower for word in yes_words) or message_lower in yes_words:
            session["step"] = "ask_name"
            order_sessions[phone_number] = session
            return "Please send your name for the order."

        if any(word == message_lower for word in no_words) or message_lower in no_words:
            session["step"] = "choose_product"
            order_sessions[phone_number] = session
            return (
                f"{format_catalog()}\n\n"
                "Please type the bouquet name you want."
            )

        matched = match_product(message)
        if matched:
            session["product"] = matched["name"]
            session["step"] = "confirm_product"
            order_sessions[phone_number] = session
            return (
                f"You want *{matched['name']}*.\n\n"
                "Reply *YES* to confirm or *NO* to choose another one."
            )

        return "Reply *YES* to confirm or *NO* to choose another bouquet."

    if step == "ask_name":
        session["customer_name"] = message.strip()
        session["step"] = "ask_address"
        order_sessions[phone_number] = session
        return "Now send your delivery address."

    if step == "ask_address":
        session["address"] = message.strip()

        product = session.get("product", "Unknown Product")
        customer_name = session.get("customer_name", "Customer")
        address = session.get("address", "")
        order_id = build_order_id(phone_number)

        safe_save_order(
            phone_number=phone_number,
            product=product,
            customer_name=customer_name,
            address=address
        )

        order_sessions.pop(phone_number, None)

        return (
            f"Thank you, {customer_name}. Your order for *{product}* has been noted.\n\n"
            f"Order number: *{order_id}*\n"
            "Our team will follow up shortly."
        )

    order_sessions.pop(phone_number, None)
    return (
        f"{format_catalog()}\n\n"
        "Please type the bouquet name you want."
    )


async def call_grok(message: str, phone_number: str, context: str = "") -> str:
    grok_api_key = os.getenv("GROK_API_KEY")
    grok_api_url = "https://api.x.ai/v1/chat/completions"

    if not grok_api_key:
        return (
            "We currently offer flowers and bouquets only.\n"
            "Ask for our collection, prices, delivery, or place an order."
        )

    session_context = order_sessions.get(phone_number, {})
    catalog_text = format_catalog()

    system_prompt = f"""
You are a WhatsApp sales assistant for Noreen's Flowers in Pakistan.

Rules:
1. Keep replies short, natural, and human.
2. This store sells flowers and bouquets only.
3. Do not invent products or prices.
4. If customer asks for unrelated items like hoodies, shoes, or electronics, politely say the store only offers flowers.
5. If possible, redirect them to available flower products.
6. If they ask about price, use only the catalog below.
7. If they want to order, guide them toward choosing one catalog item.

Catalog:
{catalog_text}

Delivery:
- Delivery across Pakistan in 4 to 5 working days
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
        async with httpx.AsyncClient(timeout=20.0) as client:
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
                    "temperature": 0.5,
                    "max_tokens": 180,
                },
            )

            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"Grok API error: {e}")
        return (
            "We currently offer flowers and bouquets only.\n"
            "You can ask about our collection, prices, delivery, or place an order."
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
    yes_keywords = ["yes", "haan", "han", "ji", "ok", "okay"]

    matched = match_product(message)

    if any(word in words for word in greet_words) or "assalam" in message_lower:
        return (
            "Assalam o Alaikum. Welcome to *Noreen's Flowers*.\n\n"
            "You can ask about our collection, prices, delivery, or place an order.",
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

    if matched and (is_flower_related(message_lower) or is_order_intent(message_lower) or len(words) <= 4):
        order_sessions[phone_number] = {
            "step": "confirm_product",
            "product": matched["name"],
        }
        return (
            f"You want *{matched['name']}*.\n\n"
            "Reply *YES* to confirm or *NO* to choose another one.",
            False,
        )

    if is_order_intent(message_lower):
        order_sessions[phone_number] = {"step": "choose_product"}
        return (
            f"{format_catalog()}\n\n"
            "Please type the bouquet name you want."
        ), False

    if message_lower in yes_keywords:
        order_sessions[phone_number] = {"step": "choose_product"}
        return (
            f"{format_catalog()}\n\n"
            "Please type the bouquet name you want."
        ), False

    return message, True
