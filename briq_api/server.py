import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .stores import setup_stores
from .api.router import router as api_router
from .mock_chain.router import router as mock_chain_router

logger = logging.getLogger(__name__)

app = FastAPI()

# This is a public API, so allow any CORS origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API
app.include_router(api_router, prefix="/v1")

if os.getenv("USE_MOCK_CHAIN"):
    app.include_router(mock_chain_router, prefix='/mock_chain')


@app.get("/health")
def health():
    return "ok"


@app.on_event("startup")
def startup_event():
    setup_stores(os.getenv("LOCAL"), os.getenv("USE_MOCK_CHAIN"))
