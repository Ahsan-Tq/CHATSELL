# ============================================================
# CHATSELL — ORDERS ROUTE
# This file handles everything related to orders.
# When a customer completes an order through WhatsApp,
# it gets saved and managed through this file.
# The seller dashboard will also talk to this file
# to fetch and update orders.
# ============================================================

from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/health")
async def orders_health():
    return {"status": "orders route active"}
