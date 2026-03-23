# ============================================================
# CHATSELL — WEBHOOK ROUTE
# This file handles all incoming WhatsApp messages.
# When Meta wants to connect to our server it first sends
# a verification challenge — basically asking "are you real?"
# We respond with the right code and Meta approves our server.
# After verification every WhatsApp message comes through here.
# ============================================================

import os
from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    verify_token = os.getenv("VERIFY_TOKEN")
    
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return PlainTextResponse(content=hub_challenge)
    
    return PlainTextResponse(content="Verification failed", status_code=403)

@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("Incoming message:", data)
    return {"status": "received"}
