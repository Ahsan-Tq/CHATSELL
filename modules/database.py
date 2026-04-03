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


def get_supabase_client():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url:
        raise ValueError("SUPABASE_URL is missing in .env")

    if not supabase_key:
        raise ValueError("SUPABASE_KEY is missing in .env")

    return create_client(supabase_url, supabase_key)


def save_order(phone_number: str, product: str, name: str, address: str):
    supabase = get_supabase_client()

    payload = {
        "phone_number": phone_number,
        "product": product,
        "customer_name": name,
        "address": address,
        "status": "new"
    }

    result = supabase.table("orders").insert(payload).execute()
    print("Order insert result:", result)
    return result
