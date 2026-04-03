# ============================================================
# CHATSELL — MAIN SERVER FILE
# This is the entry point of the entire Chatsell backend.
# When you start the server this is the first file that runs.
# It creates the FastAPI app, connects all the routes (webhook, orders),
# and starts listening for incoming requests.
# Think of this as the front door of the building —
# every request that comes in passes through here first.
# ============================================================
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.webhook import router as webhook_router
from routes.orders import router as orders_router

app = FastAPI(title="Chatsell API")

app.include_router(webhook_router)
app.include_router(orders_router)


@app.get("/")
async def root():
    return {"status": "Chatsell is running"}