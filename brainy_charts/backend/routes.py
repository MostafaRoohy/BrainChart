#
# This file contains all the backend's API endpoints or "routes",
# handling HTTP requests for chart data, symbol information, and saving or loading shapes.
#
###################################################################################################
###################################################################################################
###################################################################################################
#
import time
import json
import pandas as pd
import numpy as np
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
#
###################################################################################################
###################################################################################################
###################################################################################################
#
from .database import get_db, SessionLocal
from .models import Chart, Shape
from .schemas import ShapeCreate, ShapeResponse, ShapeAPIResponse
import json
from pathlib import Path
#
###################################################################################################
###################################################################################################
###################################################################################################
#
router       = APIRouter()
DATAFEED_DIR = Path(__file__).parent / "datafeed"

def load_registry() -> dict:

    registry_path = DATAFEED_DIR / "registry.json"
    
    if (not registry_path.exists()):

        raise HTTPException(500, detail="No registry.json found")
    #

    with open(registry_path) as f:

        return (json.load(f))
    #
#

def load_ticker_metadata(ticker:str) -> dict:

    registry = load_registry()
    meta     = registry.get(ticker)

    if (not meta):

        raise HTTPException(404, detail=f"Ticker '{ticker}' not found in registry")
    #

    return (meta)
#

def load_ticker_history_csv(ticker:str) -> pd.DataFrame:

    csv_path = DATAFEED_DIR / f"{ticker}.csv"

    if (not csv_path.exists()):

        raise HTTPException(404, detail=f"No OHLCV data for ticker '{ticker}'")
    #

    return (pd.read_csv(csv_path))
#
###################################################################################################
###################################################################################################
###################################################################################################
#
@router.get("/config")
async def get_config():

    registry        = load_registry()
    all_resolutions = set()
    for meta in registry.values():

        all_resolutions.update(meta.get("supported_resolutions", ['1', '5', '15', '30', '60', '1D', '1W', '1M']))
    #

    return {
        "supported_resolutions"    : sorted(list(all_resolutions)),
        "supports_search"          : True,
        "supports_group_request"   : False,
        "supports_marks"           : False,
        "supports_timescale_marks" : False,
        "supports_time": True,
    }
#

@router.get("/time")
async def get_server_time(symbol:Optional[str]=None):

    if (symbol is not None):

        try:

            df = load_ticker_history_csv(symbol)
            return int(df['timestamp'].max() // 1000)
        #
        except Exception as e:

            raise HTTPException(status_code=500, detail={"s": "error", "errmsg": str(e)})
        #
    #


    # Fallback: return latest timestamp across all symbols
    try:

        registry = load_registry()
        latest   = 0

        for ticker in registry:

            df = load_ticker_history_csv(ticker)
            ts = df['timestamp'].max()

            if (ts > latest):

                latest = ts
            #
        #

        return (int(latest // 1000))
    #
    except Exception as e:

        raise HTTPException(status_code=500, detail={"s": "error", "errmsg": str(e)})
    #
#

@router.get("/search")
async def search_symbols(query:str="", type:Optional[str]=None, exchange:Optional[str]=None, limit:Optional[int]=None):
    
    registry = load_registry()
    matches  = []

    for symbol_id, meta in registry.items():

        if (query.lower() in symbol_id.lower()):

            if (exchange and meta.get("exchange").lower() != exchange.lower()):
                
                continue
            #
            
            if (type and meta.get("type").lower() != type.lower()):
                
                continue
            #

            matches.append({
                "symbol"      : symbol_id,
                "name"        : meta.get("name"),
                "ticker"      : meta.get("ticker"),
                "full_name"   : meta.get("full_name"),
                "description" : meta.get("description"),
                "exchange"    : meta.get("exchange"),
                "type"        : meta.get("type"),
            })
        #
    #

    if (limit):

        matches = matches[:limit]
    #

    return (matches)
#



@router.get("/symbols")
async def get_symbols(symbol:str):

    meta = {}

    try:

        meta.update(load_ticker_metadata(symbol))
    #
    except HTTPException as e:

        return {"s":"error", "errmsg":str(e.detail)}
    #

    return (meta)
#

@router.get("/history")
async def get_history(symbol:str, resolution:str, from_time:int=Query(..., alias="from", description="Start time of the data"), to_time:int=Query(..., alias="to", description="End time of the data"), countback:Optional[int]=None):

    try:

        if (not symbol):

            raise HTTPException(status_code=400, detail="Symbol parameter is required")
        #

        df          = load_ticker_history_csv(symbol)
        filtered_df = None

        if (from_time > 0  or  to_time > 0):

            if (resolution == '1D'):

                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df = df.set_index('timestamp').resample('D').agg({
                    'open'  : 'first',
                    'high'  : 'max',
                    'low'   : 'min',
                    'close' : 'last',
                    'volume': 'sum'
                }).reset_index()
                df['timestamp'] = df['timestamp'].astype(np.int64) // 10**6
            #

            if (countback is not None):

                filtered_df = df.tail(countback)
            #
            # if (from_time > 0  and  to_time > 0):

            mask        = (df['timestamp'] >= from_time*1000) & (df['timestamp'] < to_time*1000)
            filtered_df = df[mask]
            filtered_df = filtered_df.dropna()
            filtered_df = filtered_df.sort_values(by='timestamp')
            filtered_df = filtered_df.drop_duplicates(subset='timestamp')
            #

            if (filtered_df.empty  or  len(filtered_df) == 0):

                return JSONResponse(content={"s":"no_data", "nextTime":from_time})
                # return JSONResponse(content={"s":"no_data", "nextTime":from_time, "min":str(df['timestamp'].min()), "max":str(df['timestamp'].max()), "from_time*1000":str(from_time*1000), "to_time*1000":str(to_time*1000)})
            #

            data              = filtered_df.to_dict(orient='list')
            data['timestamp'] = [ts // 1000 for ts in data['timestamp']]
            data['volume']    = [0 if pd.isna(v) else v for v in data['volume']]

            return JSONResponse(content={
                "s": "ok",
                "t": (filtered_df['timestamp']).astype(int).tolist(),
                "o": data['open'],
                "h": data['high'],
                "l": data['low'],
                "c": data['close'],
                "v": data['volume']
            })
        #
        else:

            return JSONResponse(content={"s": "no_data", "nextTime": from_time})
        #
    #
    except Exception as e:

        return JSONResponse(content={"s": "error", "errmsg": str(e)})
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
#