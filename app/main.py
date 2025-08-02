from fastapi import FastAPI
from app.api import players

app: FastAPI = FastAPI(title="CRSet API", version="0.1.0")
app.include_router(players.router, prefix="/players", tags=["Players"])