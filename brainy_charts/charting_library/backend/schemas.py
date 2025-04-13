from pydantic import BaseModel
from typing import Any, Optional, List, Dict
from datetime import datetime

class BarData(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class ShapeBase(BaseModel):
    shape_id: Optional[str] = None
    shape_code: int
    shape_type: str
    shape_data: dict


class ShapeCreate(ShapeBase):
    pass


class ShapeResponse(ShapeBase):
    id: int
    chart_id: int
    created_at: datetime

    class Config:
        orm_mode = True
