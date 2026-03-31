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
# ============================================================

from modules.database import save_order

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

def get_reply(message: str, phone_number: str) -> str:

    # ── ORDER FLOW ──
    if phone_number in order_sessions:
        return handle_order_flow(message, phone_number)

    # ── FIRST MESSAGE GREETING ──
    greet_keywords = ["hi", "hello", "hii", "helo", "aoa", "assalam", "salam", "hey"]
    if any(word in message for word in greet_keywords):
        return (
            "Assalam o Alaikum! Welcome to *Noreen's Flowers*.\n\n"
            "We deliver fresh flowers across Pakistan.\n\n"
            "You can ask about:\n"
            "• Our flower collection & prices\n"
            "• Delivery info\n"
            "• Place an order\n\n"
            "How can I help you today?"
        )

    # ── KEYWORD DETECTION ──
    price_keywords = ["price", "cost", "kitna", "rate", "pricing", "how much", "charges", "daam", "qeemat", "collection", "products", "flowers", "kya hai", "menu"]
    delivery_keywords = ["delivery", "deliver", "shipping", "ship", "courier", "time", "kab", "kitne din", "days"]
    available_keywords = ["available", "stock", "in stock", "hai", "do you have", "milega", "milegi"]
    location_keywords = ["location", "address", "where", "kahan", "pickup", "store", "shop"]
    order_keywords = ["order", "buy", "purchase", "want", "chahiye", "lena", "order karna", "leni hai", "booking"]
    yes_keywords = ["yes", "haan", "ha", "haa", "ji", "ji haan", "yep", "yup", "yeah", "sure", "bilkul"]

    if any(word in message for word in price_keywords):
        return (
            format_catalog() +
            "\nAll bouquets are freshly prepared on order.\n"
            "Which one would you like to order?"
        )

    if any(word in message for word in delivery_keywords):
        return (
            "We deliver all across Pakistan.\n\n"
            "Delivery time: 4-5 working days\n"
            "Cash on delivery available\n"
            "Free gift wrapping on all orders\n\n"
            "Want to place an order?"
        )

    if any(word in message for word in available_keywords):
        return (
            "Yes, all our flowers are available and freshly prepared on order.\n\n"
            + format_catalog() +
            "\nWhich bouquet would you like?"
        )

    if any(word in message for word in location_keywords):
        return (
            "We are an online flower shop.\n\n"
            "We deliver fresh flowers right to your doorstep across all of Pakistan.\n"
            "No need to visit — just order and we'll handle the rest."
        )

    if any(word in message for word in order_keywords):
        order_sessions[phone_number] = {"step": 1}
        return (
            "Let's place your order.\n\n"
            + format_catalog() +
            "\nPlease type the name of the bouquet you'd like to order:"
        )

    if any(word in message for word in yes_keywords):
        order_sessions[phone_number] = {"step": 1}
        return (
            "Let's place your order.\n\n"
            + format_catalog() +
            "\nPlease type the name of the bouquet you'd like to order:"
        )

    return (
        "Thank you for reaching out to *Noreen's Flowers*.\n\n"
        "You can ask us about:\n"
        "• Prices & collection\n"
        "• Delivery info\n"
        "• Place an order\n\n"
        "How can we help you?"
    )


def handle_order_flow(message: str, phone_number: str) -> str:
    session = order_sessions[phone_number]
    step = session["step"]

    if step == 1:
        order_sessions[phone_number]["product_raw"] = message
        order_sessions[phone_number]["step"] = 2
        return (
            f"You'd like to order: *{message}*\n\n"
            f"Is this correct? Reply *YES* to confirm or *NO* to change it."
        )

    elif step == 2:
        if message.lower() in ["yes", "haan", "ha", "haa", "ji", "ji haan", "yep", "yup", "yeah", "sure", "bilkul"]:
            order_sessions[phone_number]["product"] = order_sessions[phone_number]["product_raw"]
            order_sessions[phone_number]["step"] = 3
            return "Perfect. What's your full name?"
        else:
            order_sessions[phone_number]["step"] = 1
            return (
                "No problem. Please type the name of the bouquet you'd like:\n\n"
                + format_catalog()
            )

    elif step == 3:
        order_sessions[phone_number]["name"] = message
        order_sessions[phone_number]["step"] = 4
        return f"Got it, {message}. What's your delivery address?"

    elif step == 4:
        order_sessions[phone_number]["address"] = message

        product = order_sessions[phone_number]["product"]
        name = order_sessions[phone_number]["name"]
        address = message

        order_sessions.pop(phone_number)
        save_order(phone_number, product, name, address)

        return (
            f"*Order Confirmed!*\n\n"
            f"Bouquet: {product}\n"
            f"Name: {name}\n"
            f"Address: {address}\n\n"
            f"Your flowers will be delivered in 4-5 working days.\n"
            f"Our team will contact you shortly. Thank you for choosing Noreen's Flowers!"
        )

    return "Something went wrong. Type 'order' to start again."