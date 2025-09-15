#
# This file contains all the backend's API endpoints or "routes",
# handling HTTP requests for chart data, symbol information, and saving or loading shapes.
#
###################################################################################################
###################################################################################################
###################################################################################################
#
import time
from pathlib import Path

import pandas as pd
import numpy  as np
import json
import hashlib

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse

from typing import Optional
from sqlalchemy.orm import Session


from .database import get_db, SessionLocal
from .models import Chart, Shape
from .schemas import ShapeCreate, ShapeResponse, ShapeAPIResponse
import json
from pathlib import Path
#
###################################################################################################
###################################################################################################
################################################################################################### Helpers
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
################################################################################################### Chart
#
@router.get("/config")
async def get_config():

    registry        = load_registry()
    all_resolutions = set()

    for key, meta in registry.items():

        if (not isinstance(meta, dict)):

            continue
        #

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
            return int(df['timestamp'].max() / 1000)
        #
        except Exception as e:

            raise HTTPException(status_code=500, detail={"s": "error", "errmsg": str(e)})
        #
    #


    # Fallback: return latest timestamp across all symbols
    try:

        registry = load_registry()
        latest   = 0

        for key, meta in registry.items():

            if (not isinstance(meta, dict)):

                continue
            #

            df = load_ticker_history_csv(key)
            ts = df['timestamp'].max()

            if (ts > latest):

                latest = ts
            #
        #

        return (int(latest / 1000))
    #
    except Exception as e:

        raise HTTPException(status_code=500, detail={"s": "error", "errmsg": str(e)})
    #
#

@router.get("/search")
async def search_symbols(query:str="", type:Optional[str]=None, exchange:Optional[str]=None, limit:Optional[int]=None):
    
    registry = load_registry()
    matches  = []

    for key, meta in registry.items():

        if (not isinstance(meta, dict)):

            continue
        #

        if (query.lower() in key.lower()):

            if (exchange and meta.get("exchange").lower() != exchange.lower()):
                
                continue
            #
            
            if (type and meta.get("type").lower() != type.lower()):
                
                continue
            #

            matches.append({
                "symbol"      : key,
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
###################################################################################################
###################################################################################################
################################################################################################### Symbol
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

                mask        = (df['timestamp'] < to_time*1000)
                filtered_df = df[mask].sort_values(by=['timestamp']).tail(countback).reset_index(drop=True)
            #
            else:

                mask        = (df['timestamp'] >= from_time*1000) & (df['timestamp'] < to_time*1000)
                filtered_df = df[mask].sort_values(by=['timestamp']).reset_index(drop=True)
            #


            if (filtered_df.empty  or  len(filtered_df) == 0):

                return JSONResponse(content={"s":"no_data", "nextTime":from_time})
            #

            return JSONResponse(content={
                "s": "ok",
                "t": (filtered_df['timestamp']/1000).astype(int).tolist(),
                "o": filtered_df['open'].tolist(),
                "h": filtered_df['high'].tolist(),
                "l": filtered_df['low'].tolist(),
                "c": filtered_df['close'].tolist(),
                "v": filtered_df['volume'].tolist(),
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
################################################################################################### Shapes
#
def _canon(obj):

    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
#

@router.post("/shapes", response_model=ShapeResponse)
def create_shape(payload: ShapeCreate, db: Session = Depends(get_db)):

    pts = []

    for p in payload.points:

        q = dict(p)

        if ("time" in q):

            q["time"] = int(q["time"])
        #
        if ("id" in q):

            q["id"] = int(q["id"])
        #
        if ("price" in q):

            q["price"] = float(q["price"])
        #

        pts.append(q)
    #

    sig_src = f"{payload.symbol}|{payload.shape_type}|{_canon(pts)}|{_canon(payload.options or {})}"
    sig     = hashlib.sha1(sig_src.encode("utf-8")).hexdigest()

    shape = Shape(
        symbol     = payload.symbol,
        shape_type = payload.shape_type,
        points     = pts,
        options    = payload.options or {},
        sig        = sig,
    )
    db.add(shape)
    db.commit()
    db.refresh(shape)
    return {
        "id": shape.id,
        "symbol": shape.symbol,
        "shape_type": shape.shape_type,
        "points": shape.points,
        "options": shape.options,
        "created_at": shape.created_at,
    }

    shape = Shape(
        symbol     = payload.symbol,
        shape_type = payload.shape_type,
        points     = pts,
        options    = payload.options or {},
        sig        = sig,
    )

    db.add(shape)
    db.commit()
    db.refresh(shape)

    return {
        "id": shape.id,
        "symbol": shape.symbol,
        "shape_type": shape.shape_type,
        "points": shape.points,
        "options": shape.options,
        "created_at": shape.created_at,
    }
#


@router.get("/shapes", response_model=ShapeAPIResponse)
def list_shapes(symbol: str | None = None, db: Session = Depends(get_db)):

    q = db.query(Shape)

    if symbol:

        q = q.filter(Shape.symbol == symbol)
    #

    items = [{
        "id": s.id,
        "symbol": s.symbol,
        "shape_type": s.shape_type,
        "points": s.points,
        "options": s.options,
        "created_at": s.created_at,
    } for s in q.order_by(Shape.created_at.asc()).all()]

    return {"items": items}
#

@router.delete("/shapes/{shape_id}")
def delete_shape(shape_id: int, db: Session = Depends(get_db)):

    s = db.get(Shape, shape_id)

    if (not s):

        raise HTTPException(404, "shape not found")
    #

    db.delete(s)
    db.commit()

    return {"ok": True}
#
###################################################################################################
###################################################################################################
###################################################################################################
#