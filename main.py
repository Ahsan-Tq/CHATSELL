# ============================================================
# CHATSELL — MAIN SERVER FILE
# This is the entry point of the entire Chatsell backend.
# When you start the server this is the first file that runs.
# It creates the FastAPI app, connects all the routes (webhook, orders),
# and starts listening for incoming requests.
# Think of this as the front door of the building —
# every request that comes in passes through here first.
# ============================================================

from fastapi import FastAPI
from dotenv import load_dotenv
from routes import webhook, orders

load_dotenv() 

app = FastAPI()

app.include_router(webhook.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"status": "Chatsell is running!"} 