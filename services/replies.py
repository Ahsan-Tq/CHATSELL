# ============================================================
# CHATSELL — REPLY ENGINE
# This is the brain of the auto-reply system.
# It reads the customer's message and matches it to keywords.
# If it matches a keyword we return a canned response instantly.
# This costs nothing — no AI needed for simple questions.
# If nothing matches we return a default fallback message.
# ============================================================

def get_reply(message: str) -> str:
    
    price_keywords = ["price", "cost", "kitna", "rate", "pricing", "how much", "charges"]
    delivery_keywords = ["delivery", "deliver", "shipping", "ship", "courier", "time", "kab"]
    available_keywords = ["available", "stock", "in stock", "available?", "hai", "do you have"]
    location_keywords = ["location", "address", "where", "kahan", "pickup", "store"]
    order_keywords = ["order", "buy", "purchase", "want", "chahiye", "lena"]

    if any(word in message for word in price_keywords):
        return "Hi! Our prices vary by product. Please tell us which item you're interested in and we'll share the exact price. 😊"

    if any(word in message for word in delivery_keywords):
        return "We deliver all across Pakistan! Delivery takes 2-3 working days. Cash on delivery is available. 🚚"

    if any(word in message for word in available_keywords):
        return "Yes we're open and taking orders! Tell us what you're looking for and we'll check availability for you. ✅"

    if any(word in message for word in location_keywords):
        return "We're an online store operating across Pakistan. No physical store — but we deliver right to your door! 📦"

    if any(word in message for word in order_keywords):
        return "Great! We'd love to help you place an order. Please tell us: 1) Which product 2) Your name 3) Your address and we'll get it sorted! 🛍️"

    return "Assalam o Alaikum! Thanks for reaching out to us. How can we help you today? 😊"