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
from .database.database import get_db
from .database.database import SessionLocal
from .models import Chart, Shape
from .schemas import ShapeCreate, ShapeResponse
import json
from pathlib import Path
#
###################################################################################################
###################################################################################################
###################################################################################################
#
router = APIRouter()
DATAFEED_DIR = Path(__file__).parent / "datafeed"

def load_registry():

    registry_path = DATAFEED_DIR / "registry.json"
    if not registry_path.exists():

        raise HTTPException(500, detail="No registry.json found")
    #
    with open(registry_path) as f:

        return json.load(f)
    #
#

def load_symbol_metadata(symbol_id: str):

    registry = load_registry()
    meta     = registry.get(symbol_id)

    if not meta:

        raise HTTPException(404, detail=f"Symbol '{symbol_id}' not found in registry")
    #

    return meta
#

def load_symbol_data(symbol_id: str):

    csv_path = DATAFEED_DIR / f"{symbol_id}.csv"

    if not csv_path.exists():

        raise HTTPException(404, detail=f"No OHLCV data for symbol: {symbol_id}")
    #

    return pd.read_csv(csv_path)
#

@router.get("/")
async def root():

    return {"message": "Welcome to TradingView Charting Library Backend"}
#
###################################################################################################
###################################################################################################
###################################################################################################
#
@router.get("/search")
async def search_symbols(
    query: str = "",
    type: Optional[str] = None,
    exchange: Optional[str] = None,
    limit: Optional[int] = None
):
    registry = load_registry()
    matches = []
    for symbol_id, meta in registry.items():
        if query.lower() in symbol_id.lower():

            if exchange and meta.get("exchange", "").lower() != exchange.lower():
                continue
            if type and meta.get("type", "crypto").lower() != type.lower():
                continue
            matches.append({
                "symbol": symbol_id,
                "full_name": meta.get("full_name", meta.get("name", symbol_id)),
                "description": meta.get("description", ""),
                "exchange": meta.get("exchange", ""),
                "type": meta.get("type", "crypto"),
                "ticker": symbol_id
            })
    if limit:
        matches = matches[:limit]
    # return {"symbols": matches}
    return matches
#

@router.get("/symbols")
async def get_symbols(symbol:str):
    try:
        meta = load_symbol_metadata(symbol)
    except HTTPException as e:
        return {"s": "error", "errmsg": str(e.detail)}
    
    meta = load_symbol_metadata(symbol)
    return {
        # "s": "ok",
        "name": meta.get("name"),
        "exchange-traded": meta.get("exchange", ""),
        "exchange-listed": meta.get("listed_exchange", ""),
        "timezone": meta.get("timezone", "UTC"),
        "minmov": meta.get("minmov", 1),
        "minmov2": meta.get("minmov2", 0),
        "pointvalue": meta.get("pointvalue", 1),
        "session": meta.get("session", "24x7"),
        "has_intraday": meta.get("has_intraday", True),
        "has_daily": meta.get("has_daily", True),
        "has_weekly_and_monthly": meta.get("has_weekly_and_monthly", True),
        "visible_plots_set": meta.get("visible_plots_set", "ohlcv"),
        "description": meta.get("description", ""),
        "type": meta.get("type", "crypto"),
        "supported_resolutions": meta.get("supported_resolutions", []),
        "pricescale": meta.get("pricescale", 100),
        # "ticker": meta.get("ticker", symbol),
        "ticker": symbol,
        "logo_urls": meta.get("logo_urls", []),
        "exchange_logo": meta.get("exchange_logo", "")
    }
#

@router.get("/symbol_info")
async def get_symbol_info(symbol: str):

    try:
        meta = load_symbol_metadata(symbol)
    except HTTPException as e:
        return {"s": "error", "errmsg": str(e.detail)}
    
    meta = load_symbol_metadata(symbol)
    return {
        # "s": "ok",
        "name": meta.get("name"),
        # "ticker": meta.get("ticker"),
        "ticker": symbol,
        "full_name": meta.get("full_name", meta.get("name")),
        "description": meta.get("description"),
        "type": meta.get("type"),
        "session": meta.get("session"),
        "exchange": meta.get("exchange"),
        "listed_exchange": meta.get("listed_exchange", meta.get("exchange")),
        "timezone": meta.get("timezone"),
        "minmov": meta.get("minmov", 1),
        "minmov2": meta.get("minmov2", 0),
        "pricescale": meta.get("pricescale", 100),
        "pointvalue": meta.get("pointvalue", 1),
        "has_intraday": meta.get("has_intraday", True),
        "has_daily": meta.get("has_daily", True),
        "has_weekly_and_monthly": meta.get("has_weekly_and_monthly", True),
        "currency_code": meta.get("currency_code", "USDT"),
        "visible_plots_set": meta.get("visible_plots_set", "ohlcv"),
        "supported_resolutions": meta.get("supported_resolutions", [])
    }
#

@router.get("/history")
async def get_history(
    symbol: str,
    resolution: str,
    from_time: int = Query(..., alias="from", description="Start time of the data"),
    to_time: int = Query(..., alias="to", description="End time of the data"),
    countback: Optional[int] = None
):
    try:
        if not symbol:
            raise HTTPException(status_code=400, detail="Symbol parameter is required")

        df = load_symbol_data(symbol)

        from_time = from_time * 1000
        to_time = to_time * 1000

        if from_time > 0 or to_time > 0:
            if countback:
                filtered_df = df.tail(countback)

            if resolution == '1D':
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df = df.set_index('timestamp').resample('D').agg({
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'volume': 'sum'
                }).reset_index()
                df['timestamp'] = df['timestamp'].astype(np.int64) // 10**6

            mask = (df['timestamp'] >= from_time) & (df['timestamp'] <= to_time)
            filtered_df = df[mask]
            filtered_df = filtered_df.dropna()
            filtered_df = filtered_df.sort_values(by='timestamp')
            filtered_df = filtered_df.drop_duplicates(subset='timestamp')

            if filtered_df.empty  or   len(filtered_df) == 0:
                return JSONResponse(content={"s": "no_data", "nextTime": from_time})

            data = filtered_df.to_dict(orient='list')
            data['timestamp'] = [ts // 1000 for ts in data['timestamp']]
            data['volume'] = [0 if pd.isna(v) else v for v in data['volume']]

            return JSONResponse(content={
                "s": "ok",
                "t": (filtered_df['timestamp'] // 1000).astype(int).tolist(),
                "o": data['open'],
                "h": data['high'],
                "l": data['low'],
                "c": data['close'],
                "v": data['volume']
            })
        else:
            return JSONResponse(content={"s": "no_data", "nextTime": from_time})
    except Exception as e:
        return JSONResponse(content={"s": "error", "errmsg": str(e)})
#

@router.get("/config")
async def get_config():
    registry = load_registry()
    all_resolutions = set()
    for meta in registry.values():
        all_resolutions.update(meta.get("supported_resolutions", []))
    return {
        "supported_resolutions": sorted(list(all_resolutions)),
        "supports_group_request": False,
        "supports_marks": False,
        "supports_search": True,
        "supports_time": True,
        "supports_timescale_marks": False,
        "exchanges": [],
        # "symbols_types": [
            # {"name": "All types", "value": ""},
            # {"name": "Stock", "value": "stock"},
            # {"name": "Index", "value": "index"},
            # {"name": "Crypto", "value": "crypto"}
        # ],
    }
#

@router.get("/time")
async def get_server_time(symbol: Optional[str] = None):
    if symbol:
        try:
            df = load_symbol_data(symbol)
            return int(df['timestamp'].max() // 1000)
        except Exception as e:
            return {"s": "error", "errmsg": str(e)}

    # Fallback: return latest timestamp across all symbols
    try:
        registry = load_registry()
        latest = 0
        for sym_id in registry:
            df = load_symbol_data(sym_id)
            ts = df['timestamp'].max()
            if ts > latest:
                latest = ts
        return int(latest // 1000)
    except Exception as e:
        return {"s": "error", "errmsg": str(e)}
#
###################################################################################################
###################################################################################################
###################################################################################################
#
@router.post("/charts/{chart_id}/shapes/", response_model=ShapeResponse)
async def create_shape(
    chart_id: int, 
    shape: ShapeCreate, 
    db: Session = Depends(get_db)
    ):

    chart = db.query(Chart).get(chart_id)
    if not chart:
        chart = Chart(id=chart_id, name=f"Auto-Created Chart {chart_id}")
        db.add(chart)
        db.commit()
        db.refresh(chart)

    existing_shape = db.query(Shape).filter(
        Shape.shape_code == shape.shape_code,
        Shape.chart_id == chart_id
    ).first()

    print('== ext', existing_shape.shape_code if existing_shape else '== None')

    if existing_shape:
        print('== code', existing_shape.shape_code)
        for key, value in shape.model_dump().items():
            print('-- dict', key, '--', value)
                  
            setattr(existing_shape, key, value)
        db.commit()
        print('===============================')
        print('== upd', existing_shape.shape_code, existing_shape.shape_id)

        db.refresh(existing_shape)
        db.close()
        return existing_shape
    
    else:  # Create New Shape
        db_shape = Shape(**shape.model_dump(), chart_id=chart_id)
        print('== new', shape.model_dump())

        db.add(db_shape)
        db.commit()
        db.refresh(db_shape)
        db.close()
        return db_shape
#

@router.get("/charts/{chart_id}/shapes/", response_model=list[ShapeResponse])
async def get_chart_shapes(
    chart_id: int, 
    db: Session = Depends(get_db)
    ):
    
    chart = db.query(Chart).get(chart_id)
    if not chart:
        chart = Chart(id=chart_id, name=f"Auto-Created Chart {chart_id}")
        db.add(chart)
        db.commit()
        db.refresh(chart)
    
    shapes = db.query(Shape).filter(Shape.chart_id == chart_id).all()
    [print('== get ', shape.shape_id, shape.shape_code) for shape in shapes]

    db.close()
    return shapes
#

@router.get("/charts/{chart_id}/shapes/{shape_code}", response_model=ShapeResponse)
async def get_shape(
    chart_id: int,
    shape_code: str,
    db: Session = Depends(get_db)
):

    chart = db.query(Chart).get(chart_id)
    if not chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    
    shape = db.query(Shape).filter(
        Shape.chart_id == chart_id,
        Shape.shape_code == shape_code
    ).first()
    
    if not shape:
        raise HTTPException(status_code=404, detail="Shape not found")
    
    print(f'== Get single shape: {shape.shape_id}, {shape.shape_code}')
    return shape
#

@router.delete("/charts/{chart_id}/shapes/{shape_code}")
async def delete_shape(
    chart_id: int, 
    shape_code: int, 
    db: Session = Depends(get_db)
    ):

    print('== del ', shape_code, chart_id)
    shape = db.query(Shape).filter(
        Shape.shape_code == shape_code,
        Shape.chart_id == chart_id
    ).first()
    
    if not shape:
        raise HTTPException(404, "Shape not found")
    
    db.delete(shape)
    db.commit()
    db.close()
    return {"status": "deleted"}
#

@router.delete("/charts/{chart_id}/shapes/")
async def delete_all_shapes_in_chart(
    chart_id: int,
    db: Session = Depends(get_db)
    ):
    
    chart = db.query(Chart).get(chart_id)
    if not chart:
        db.close()
        raise HTTPException(status_code=404, detail="Chart not found")
    
    try:
        deleted_count = db.query(Shape)\
            .filter(Shape.chart_id == chart_id)\
            .delete()
        
        db.commit()
        return {
            "status": "success",
            "deleted_shapes": deleted_count,
            "chart_id": chart_id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error deleting shapes: {str(e)}")
        
    finally:
        db.close()
#
###################################################################################################
###################################################################################################
###################################################################################################
#