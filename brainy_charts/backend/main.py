# This is the entry point for the FastAPI application,
# where the app is initialized, middleware is configured,
# and all the API endpoints from routes.py are included.
###################################################################################################
###################################################################################################
###################################################################################################
#
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from typing import List, Optional
#
###################################################################################################
###################################################################################################
###################################################################################################
#
from .routes import router
from .models import Base
from .database import engine
#
###################################################################################################
###################################################################################################
###################################################################################################
#
app = FastAPI(title="TradingView Charting Library Backend")
app.include_router(router)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=500)
#
###################################################################################################
###################################################################################################
###################################################################################################
#