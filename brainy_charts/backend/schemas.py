# Contains the Pydantic models. These define the shape of the data
# for your API—what your API expects in requests and what it sends in responses.
# This is the API-layer definition, used for validation, serialization, and documentation.
# Defines how data is represented in API requests and responses (the data validation layer).
# This module defines the data shapes for API requests and responses using Pydantic,
#
# which ensures that the data moving through the API is validated and has the correct structure.
#
###################################################################################################
###################################################################################################
###################################################################################################
#
from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict
from datetime import datetime
#
###################################################################################################
###################################################################################################
###################################################################################################
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
###################################################################################################
#