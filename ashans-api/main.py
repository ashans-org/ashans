from fastapi import FastAPI
from app.routes import wallet, mining, data

app = FastAPI(
    title="Ashans API",
    description="Secure FastAPI backend for Ashans crypto and data storage",
    version="1.0.0"
)


app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(mining.router, prefix="/mining", tags=["Mining"])
app.include_router(data.router, prefix="/data", tags=["Data"])
