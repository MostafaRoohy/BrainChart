#
###################################################################################################
###################################################################################################
################################################################################################### Imports
#
from pathlib import Path
from typing import Optional, Any, Dict, List
import json, hashlib

# -----------------------------------------------

import pandas as pd
import numpy  as np

# -----------------------------------------------

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

# -----------------------------------------------

from pydantic import BaseModel
from datetime import datetime

# -----------------------------------------------

from .database import engine, Base, get_db, Shape
#
###################################################################################################
###################################################################################################
################################################################################################### Directories
#
ROOT_DIR      = Path(__file__).resolve().parent.parent      # project root (BrainChart/)

WIDGET_DIR    = ROOT_DIR / "runtime" / "widget"             # runtime/widget
DATAFEED_DIR  = ROOT_DIR / "runtime" / "datafeed"           # runtime/datafeed
WIDGET_DIR.mkdir(parents=True, exist_ok=True)
DATAFEED_DIR.mkdir(parents=True, exist_ok=True)

TV_LIB_DIR    = ROOT_DIR / "charting_library"               # charting_library/
TV_DF_DIR     = ROOT_DIR / "charting_library" / "datafeeds" # charting_library/datafeeds/
#
###################################################################################################
###################################################################################################
################################################################################################### Schemas
#
class BarData(BaseModel):

    time   : int
    open   : float
    high   : float
    low    : float
    close  : float
    volume : float
#

class ShapeCreate(BaseModel):

    symbol     : str
    shape_type : str
    points     : List[Dict]
    options    : Optional[Dict[str, Any]] = None
#

class ShapeUpdate(BaseModel):

    symbol     : Optional[str]               = None
    shape_type : Optional[str]               = None
    points     : Optional[List[Dict]]        = None
    options    : Optional[Dict[str, Any]]    = None
#

class ShapeResponse(BaseModel):

    id         : int
    symbol     : str
    shape_type : str
    points     : List[Dict]
    options    : Optional[Dict[str, Any]] = None
    created_at : datetime
#

class ShapeAPIResponse(BaseModel):

    items : List[ShapeResponse]
#
###################################################################################################
###################################################################################################
################################################################################################### Routes
#
router = APIRouter()
#
################################################# General Routes
#
def load_registry() -> dict:

    registry_path = DATAFEED_DIR / "registry.json"
    
    if (not registry_path.exists()):

        raise HTTPException(500, detail="No registry.json found")
    #

    with open(registry_path) as f:

        return (json.load(f))
    #
#

def load_ticker_history_csv(ticker:str) -> pd.DataFrame:

    csv_path = DATAFEED_DIR / f"{ticker}.csv"

    if (not csv_path.exists()):

        raise HTTPException(404, detail=f"No OHLCV data for ticker '{ticker}'")
    #

    return (pd.read_csv(csv_path))
#
################################################# Chart Routes
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
################################################# Symbol Routes
#
def load_ticker_metadata(ticker:str) -> dict:

    registry = load_registry()
    meta     = registry.get(ticker)

    if (not meta):

        raise HTTPException(404, detail=f"Ticker '{ticker}' not found in registry")
    #

    return (meta)
#


def parse_series_symbol(raw:str) -> tuple[str, str] | None:

    SERIES_SEP = "#SERIES:"
    return ((tuple(raw.split(SERIES_SEP, 1))) if (SERIES_SEP in raw) else (None))
#

def _parse_resolution(res:str) -> tuple[str, int]:

    """
    Return (kind, n) where kind in {'sec','min','day','week','month'} and n is the multiplier.
    '15' -> ('min', 15), '60' -> ('min', 60), '1S' -> ('sec', 1), '1D' -> ('day', 1),
    '1W' -> ('week', 1), '1M' -> ('month', 1)
    """

    r = str(res or "").strip().upper()

    if (r.endswith("S")):

        return ("sec", int(r[:-1] or "1"))
    #
    if (r.endswith("D")):

        return ("day", int(r[:-1] or "1"))
    #
    if (r.endswith("W")):

        return ("week", int(r[:-1] or "1"))
    #
    if (r.endswith("M")):

        return ("month", int(r[:-1] or "1"))
    #

    return ("min", int(r or "1"))
#

def _agg_ohlcv(df:pd.DataFrame, kind:str, n:int) -> pd.DataFrame:

    """
    Aggregate OHLCV to the requested bucket.
    Expects df with 'timestamp' (ms), 'open','high','low','close','volume'.
    Returns the same columns, with 'timestamp' aligned to bucket start (ms).
    """

    if (df.empty):

        return df
    #

    if (kind in ("sec", "min")):

        bucket_ms = (n * 1000) if kind == "sec" else (n * 60_000)
        gb        = (df["timestamp"] // bucket_ms) * bucket_ms
        out       = (df.assign(_b=gb)
                       .groupby("_b", as_index=False)
                       .agg({
                            "open": "first",
                            "high": "max",
                            "low":  "min",
                            "close":"last",
                            "volume":"sum"
                        })
                    )
        
        out = out.rename(columns={"_b": "timestamp"})

        return (out.dropna())
    #

    rule = {"day":"D", "week":"W-MON", "month":"M"}[kind]
    ts   = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    out  = (df.assign(_ts=ts).set_index("_ts")
              .resample(rule, label="left", closed="left", origin="epoch")
              .agg({
                  "open": "first",
                  "high": "max",
                  "low":  "min",
                  "close":"last",
                  "volume":"sum"
               })
             .dropna()
             .reset_index()
          )
    
    out["timestamp"] = (out["_ts"].astype("int64") // 10**6)

    return (out.drop(columns=["_ts"]))
#

def _agg_series(x:pd.DataFrame, col:str, kind:str, n:int) -> pd.DataFrame:

    """
    Aggregate a single numeric series to requested bucket (use last value per bucket).
    Expects x with 'timestamp' (ms) and the 'col'.
    """

    if x.empty:

        return x[["timestamp", col]]
    #

    if kind in ("sec", "min"):

        bucket_ms = (n * 1000) if kind == "sec" else (n * 60_000)
        gb        = (x["timestamp"] // bucket_ms) * bucket_ms
        y         = (x.assign(_b=gb)
                       .groupby("_b", as_index=False)[col]
                       .last()
                    )
        
        return (y.rename(columns={"_b": "timestamp"}).dropna())
    #

    rule = {"day":"D", "week":"W-MON", "month":"M"}[kind]
    ts   = pd.to_datetime(x["timestamp"], unit="ms", utc=True)
    y   = (x.assign(_ts=ts).set_index("_ts")[col]
             .resample(rule, label="left", closed="left", origin="epoch")
             .last()
             .dropna()
             .reset_index()
          )
    
    y["timestamp"] = (y["_ts"].astype("int64") // 10**6)

    return (y.drop(columns=["_ts"]))
#

@router.get("/symbols")
async def get_symbols(symbol: str):

    pair = parse_series_symbol(symbol)
    if (pair):

        base, col = pair

        try:

            base_meta = load_ticker_metadata(base)
        #
        except HTTPException as e:

            return {"s": "error", "errmsg": str(e.detail)}
        #

        meta = dict(base_meta)

        meta["ticker"]      = symbol
        meta["name"]        = f"{base_meta.get('name', base)} ({col})"
        meta["full_name"]   = meta.get("full_name", meta["ticker"])
        meta["description"] = f"{base_meta.get('description', base)} • Series: {col}"

        return (meta)
    #


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


        pair = parse_series_symbol(symbol)
        if (pair):

            base, col = pair
            df        = load_ticker_history_csv(base)

            if (col not in df.columns):

                return JSONResponse(content={"s":"no_data", "nextTime": from_time})
            #

            x       = df[["timestamp", col]].copy()
            kind, n = _parse_resolution(resolution)
            x       = _agg_series(x, col, kind, n)


            if (resolution == "1D"):

                x["timestamp"] = pd.to_datetime(x["timestamp"], unit="ms")
                x = (
                    x.set_index("timestamp")[col]
                     .resample("D").last()
                     .dropna()
                     .reset_index()
                )
                x["timestamp"] = x["timestamp"].astype(np.int64) // 10**6
            #
            else:

                x = x.dropna()
            #


            if (countback is not None):

                mask = (x["timestamp"] < to_time*1000)
                xf   = x[mask].sort_values("timestamp").tail(countback).reset_index(drop=True)
            #
            else:

                mask = (x["timestamp"] >= from_time*1000) & (x["timestamp"] < to_time*1000)
                xf   = x[mask].sort_values("timestamp").reset_index(drop=True)
            #

            if (xf.empty):

                return JSONResponse(content={"s":"no_data", "nextTime": from_time})
            #

            ts  = (xf["timestamp"]/1000).astype(int).tolist()
            arr = xf[col].astype(float).tolist()

            return JSONResponse(content={
                "s": "ok",
                "t": ts,
                "o": arr,
                "h": arr,
                "l": arr,
                "c": arr,
                "v": [0]*len(arr),
            })
        #


        df          = load_ticker_history_csv(symbol)
        kind, n     = _parse_resolution(resolution)
        df          = _agg_ohlcv(df, kind, n)
        filtered_df = None

        if (from_time > 0 or to_time > 0):

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

            if (filtered_df.empty or len(filtered_df) == 0):

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
################################################# Shaping Routes
#
def _canon(obj):

    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
#

def _normalize_points(points: List[Dict]) -> List[Dict]:

    pts = []

    for p in (points or []):

        q = dict(p)

        if "time" in q:   q["time"]   = int(q["time"])
        if "id" in q:     q["id"]     = int(q["id"])
        if "price" in q:  q["price"]  = float(q["price"])
        if "channel" in q and q["channel"] is not None:

            q["channel"] = str(q["channel"])
        #

        pts.append(q)
    #

    return pts
#

@router.post("/shapes", response_model=ShapeResponse)
def create_shape(payload: ShapeCreate, db: Session = Depends(get_db)):

    pts = _normalize_points(payload.points)

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
#

@router.put("/shapes/{shape_id}", response_model=ShapeResponse)
def update_shape(shape_id: int, payload: ShapeUpdate, db: Session = Depends(get_db)):
    s = db.get(Shape, shape_id)
    if not s:
        raise HTTPException(404, "shape not found")

    if payload.symbol is not None:
        s.symbol = payload.symbol
    if payload.shape_type is not None:
        s.shape_type = payload.shape_type
    if payload.points is not None:
        s.points = _normalize_points(payload.points)
    if payload.options is not None:
        s.options = payload.options

    sig_src = f"{s.symbol}|{s.shape_type}|{_canon(s.points)}|{_canon(s.options or {})}"
    s.sig   = hashlib.sha1(sig_src.encode("utf-8")).hexdigest()

    db.add(s)
    db.commit()
    db.refresh(s)
    return {
        "id": s.id,
        "symbol": s.symbol,
        "shape_type": s.shape_type,
        "points": s.points,
        "options": s.options,
        "created_at": s.created_at,
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
################################################################################################### Mounts
#
app = FastAPI(title="BrainChart Backend")
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)

# Static mounts
app.mount("/charting_library", StaticFiles(directory=str(TV_LIB_DIR), html=False), name="charting_library")
app.mount("/datafeeds"       , StaticFiles(directory=str(TV_DF_DIR) , html=False), name="datafeeds")
app.mount("/"                , StaticFiles(directory=str(WIDGET_DIR), html=True) , name="frontend")
# region for now I decided to define the entry index.html as static mounting for the sake of symmetricity
    # @app.get("/")
    # def serve_widget_index():
    #     index_path = FRONTEND_DIR / "index.html"
    #     if not index_path.exists():
    #         return JSONResponse(
    #             {"error": "index.html not found", "expected": str(index_path)},
    #             status_code=500,
    #         )
    #     #
    #     return FileResponse(index_path)
    # #
# endregion
#

# Ensure tables exist
Base.metadata.create_all(bind=engine)
#
###################################################################################################
###################################################################################################
###################################################################################################
#