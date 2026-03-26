# ============================================================
# CHATSELL — DATABASE
# This file handles the connection to Supabase and all
# database operations. Right now it does one thing —
# saves a completed order to the orders table.
# Every time a customer completes the order flow in WhatsApp
# the order details get passed here and saved permanently.
# Even if the server restarts the orders are safe in Supabase.
# ============================================================

import os
from supabase import create_client

def get_db():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

def save_order(phone_number: str, product: str, name: str, address: str):
    db = get_db()
    order = {
        "phone_number": phone_number,
        "product": product,
        "customer_name": name,
        "address": address,
        "status": "new"
    }
    result = db.table("orders").insert(order).execute()
    print(f"Order saved: {result}")
    return result
