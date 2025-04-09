from fastapi import FastAPI
from app.routes import wallet, mining, data

app = FastAPI()

app.include_router(wallet.router)
app.include_router(mining.router)
app.include_router(data.router)