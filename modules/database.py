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
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_order(phone_number: str, product: str, quantity: int, name: str, address: str):
    result = supabase.table("orders").insert({
        "phone_number": phone_number,
        "product": product,
        "quantity": quantity,
        "customer_name": name,
        "address": address,
        "status": "new"
    }).execute()

    print(result)
    return result
