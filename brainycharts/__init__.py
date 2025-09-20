#
###################################################################################################
###################################################################################################
###################################################################################################
#
"""
BrainyCharts public API.

This package exposes a small, stable surface:
- BrainyChart orchestrator (spin up the server, generate runtime assets)
- Symbol model (write CSV + registry)
- ChartWidget (HTML generator)
- Shape domain + helpers (typed points/options/overrides, create/list/delete)
"""
#
###################################################################################################
###################################################################################################
###################################################################################################
#
__version__ = "0.9.3"

# `from brainycharts import *` exposes
__all__ = [
    "BrainyChart",
    "Symbol",
    "ChartWidget",

    "ShapePoint",
    "ShapeOptions",
    "ShapeError",
    "OnePointShape",
    "MultiPointShape",
    "ShapeType",
    "Channel",

    "TrendlineOverrides",
    "HorzlineOverrides",
    "HorzrayOverrides",
    "RiskRewardLongOverrides",
    "RiskRewardShortOverrides",

    "CreateShape",
    "GetAllShapes",
    "RemoveShape",
    "RemoveAllShapes",
    "Shapes",

    "__version__",
]
#
#
###################################################################################################
###################################################################################################
###################################################################################################
#
# Orchestrator
from .brain import BrainyChart

# Symbols
from .symbol import Symbol

# Shapes: types, overrides, helpers, facade
from .shape import (
    # Core types
    ShapePoint,
    ShapeOptions,
    ShapeError,

    # Enums
    OnePointShape,
    MultiPointShape,
    ShapeType,
    Channel,

    # Typed overrides (initial set)
    TrendlineOverrides,
    HorzlineOverrides,
    HorzrayOverrides,
    RiskRewardLongOverrides,
    RiskRewardShortOverrides,

    # Convenience helpers
    CreateShape,
    GetAllShapes,
    RemoveShape,
    RemoveAllShapes,

    # Facade
    Shapes,
)
#

# Widget generator (writes runtime/widget/index.html)
from .widget import ChartWidget
#
###################################################################################################
###################################################################################################
###################################################################################################
#
