from fastapi import FastAPI
from routes_cobranca import router as cobranca_router

app = FastAPI(
    title="Cobrança Externa Bonfim",
    version="1.0.0"
)

app.include_router(cobranca_router, prefix="/api/cobranca")
