# ============================================================
# CHATSELL — WEBHOOK ROUTE
# This file handles all incoming WhatsApp messages.
# When a customer sends a message on WhatsApp, Meta sends it
# to this file first. Right now it just confirms it's working.
# Later this is where we read the message and decide what to reply.
# ============================================================

from fastapi import APIRouter

router = APIRouter()

@router.get("/webhook")
def verify_webhook():
    return {"message": "Webhook is live!"}

