import time
import json
import pandas as pd
import numpy as np
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session

from .database import get_db
from .data_loader import load_data, last_timestamp
from .database import SessionLocal
from .models import Chart, Shape
from .schemas import ShapeCreate, ShapeResponse

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to TradingView Charting Library Backend"}


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

        df = load_data()
        
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
            
            if filtered_df.empty:
                return JSONResponse(content={"s": "no_data", "nextTime": from_time})

            data = filtered_df.to_dict(orient='list')
            data['timestamp'] = [ts // 1000 for ts in data['timestamp']]
            data['volume'] = [0 if pd.isna(v) else v for v in data['volume']]
            
            return JSONResponse(content={
                "s": "ok",
                "t": data['timestamp'],
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


@router.get("/symbols")
async def get_symbols():
    return {
        "name": "MYDATA",
        "exchange-traded": "BINANCE",
        "exchange-listed": "BINANCE",
        "timezone": "UTC",
        "minmov": 1,
        "minmov2": 0,
        "pointvalue": 1,
        "session": "24x7",
        "has_intraday": True,
        # "has_daily": True,
        # "has_weekly_and_monthly": True,
        "visible_plots_set": "ohlcv",
        "description": "My data",
        "type": "crypto",
        "supported_resolutions": ["1", "5", "15", "30", "60", "D", "W"],
        "pricescale": 100,
        "ticker": "MYDATA",
        "logo_urls": ["https://s3-symbol-logo.tradingview.com/crypto/XTVCBTC.svg"],
        "exchange_logo": "https://s3-symbol-logo.tradingview.com/crypto/XTVCBTC.svg"
    }


@router.get("/symbol_info")
async def get_symbol_info(symbol: str):
    return {
        "name": "MYDATA",
        "ticker": "MYDATA",
        "full_name": "MYDATA",
        "description": "My data",
        "type": "crypto",
        "session": "24x7",
        "exchange": "BINANCE",
        "listed_exchange": "BINANCE",
        "timezone": "UTC",
        "minmov": 1,
        "minmov2": 0,
        "pricescale": 100,
        "pointvalue": 1,
        "has_intraday": True,
        # "has_daily": True,
        # "has_weekly_and_monthly": True,
        "currency_code": "USDT",
        "visible_plots_set": "ohlcv",
        "supported_resolutions": ["1", "5", "15", "30", "60", "D", "W"]
    }


@router.get("/config")
async def get_config():
    return {
        "supported_resolutions": ["1", "5", "15", "30", "60", "D", "W"],
        "supports_group_request": False,
        "supports_marks": False,
        "supports_search": True,
        "supports_time": True,
        "supports_timescale_marks": False,
        "exchanges":[
            {"value":"","name":"All Exchanges","desc":""},
            {"value":"NasdaqNM","name":"NasdaqNM","desc":"NasdaqNM"},
            {"value":"NYSE","name":"NYSE","desc":"NYSE"},
            {"value":"NCM","name":"NCM","desc":"NCM"},
            {"value":"NGM","name":"NGM","desc":"NGM"},
            {"value":"BINANCE","name":"BINANCE","desc":"BINANCE"}
            ],
        "symbols_types":[
            {"name":"All types","value":""},
            {"name":"Stock","value":"stock"},
            {"name":"Index","value":"index"},
            {"name":"Crypto","value":"crypto"}
            ],
    }


@router.get("/time")
async def get_server_time():
    return int(last_timestamp)


@router.get("/search")
async def search_symbols(
    query: str,
    type: Optional[str] = None,
    exchange: Optional[str] = None,
    limit: Optional[int] = None
):
    return {
        "symbols": [
            {
                "symbol": "MYDATA",
                "full_name": "MYDATA",
                "description": "My data",
                "exchange": "BINANCE",
                "type": "crypto",
                "ticker": "MYDATA"
            }
        ]
    }


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
