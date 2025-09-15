#
###################################################################################################
###################################################################################################
################################################################################################### Modules
#
import os
from pathlib import Path

import random

import requests
import json

from enum import Enum
from typing import List, Dict, Optional, Union, Any, Sequence, Iterable
from dataclasses import dataclass, fields


from .symbol import Symbol
#
###################################################################################################
###################################################################################################
################################################################################################### Shape Constants
#
class OnePointShape(str, Enum):

    emoji            = "emoji"
    text             = "text"
    icon             = "icon"
    anchored_text    = "anchored_text"
    anchored_note    = "anchored_note"
    note             = "note"
    sticker          = "sticker"
    arrow_up         = "arrow_up"
    arrow_down       = "arrow_down"
    flag             = "flag"
    vertical_line    = "vertical_line"
    horizontal_line  = "horizontal_line"
    long_position    = "long_position"
    short_position   = "short_position"
#

class MultiPointShape(str, Enum):

    triangle                  = "triangle"
    curve                     = "curve"
    table                     = "table"
    circle                    = "circle"
    ellipse                   = "ellipse"
    path                      = "path"
    polyline                  = "polyline"
    extended                  = "extended"
    signpost                  = "signpost"
    double_curve              = "double_curve"
    arc                       = "arc"
    price_label               = "price_label"
    price_note                = "price_note"
    arrow_marker              = "arrow_marker"
    cross_line                = "cross_line"
    horizontal_ray            = "horizontal_ray"
    trend_line                = "trend_line"
    info_line                 = "info_line"
    trend_angle               = "trend_angle"
    arrow                     = "arrow"
    ray                       = "ray"
    parallel_channel          = "parallel_channel"
    disjoint_angle            = "disjoint_angle"
    flat_bottom               = "flat_bottom"
    anchored_vwap             = "anchored_vwap"
    pitchfork                 = "pitchfork"
    schiff_pitchfork_modified = "schiff_pitchfork_modified"
    schiff_pitchfork          = "schiff_pitchfork"
    balloon                   = "balloon"
    comment                   = "comment"
    inside_pitchfork          = "inside_pitchfork"
    pitchfan                  = "pitchfan"
    gannbox                   = "gannbox"
    gannbox_square            = "gannbox_square"
    gannbox_fixed             = "gannbox_fixed"
    gannbox_fan               = "gannbox_fan"
    fib_retracement           = "fib_retracement"
    fib_trend_ext             = "fib_trend_ext"
    fib_speed_resist_fan      = "fib_speed_resist_fan"
    fib_timezone              = "fib_timezone"
    fib_trend_time            = "fib_trend_time"
    fib_circles               = "fib_circles"
    fib_spiral                = "fib_spiral"
    fib_speed_resist_arcs     = "fib_speed_resist_arcs"
    fib_channel               = "fib_channel"
    xabcd_pattern             = "xabcd_pattern"
    cypher_pattern            = "cypher_pattern"
    abcd_pattern              = "abcd_pattern"
    callout                   = "callout"
    text_note                 = "text_note"
    triangle_pattern          = "triangle_pattern"
    three_drivers_pattern     = "3divers_pattern"
    head_and_shoulders        = "head_and_shoulders"
    fib_wedge                 = "fib_wedge"
    elliott_impulse_wave      = "elliott_impulse_wave"
    elliott_triangle_wave     = "elliott_triangle_wave"
    elliott_triple_combo      = "elliott_triple_combo"
    elliott_correction        = "elliott_correction"
    elliott_double_combo      = "elliott_double_combo"
    cyclic_lines              = "cyclic_lines"
    time_cycles               = "time_cycles"
    sine_line                 = "sine_line"
    forecast                  = "forecast"
    date_range                = "date_range"
    price_range               = "price_range"
    date_and_price_range      = "date_and_price_range"
    bars_pattern              = "bars_pattern"
    ghost_feed                = "ghost_feed"
    projection                = "projection"
    rectangle                 = "rectangle"
    rotated_rectangle         = "rotated_rectangle"
    brush                     = "brush"
    highlighter               = "highlighter"
    regression_trend          = "regression_trend"
    fixed_range_volume_profile= "fixed_range_volume_profile"
#

class ShapeType(str, Enum):

    emoji            = "emoji"
    text             = "text"
    icon             = "icon"
    anchored_text    = "anchored_text"
    anchored_note    = "anchored_note"
    note             = "note"
    sticker          = "sticker"
    arrow_up         = "arrow_up"
    arrow_down       = "arrow_down"
    flag             = "flag"
    vertical_line    = "vertical_line"
    horizontal_line  = "horizontal_line"
    long_position    = "long_position"
    short_position   = "short_position"

    triangle                  = "triangle"
    curve                     = "curve"
    table                     = "table"
    circle                    = "circle"
    ellipse                   = "ellipse"
    path                      = "path"
    polyline                  = "polyline"
    extended                  = "extended"
    signpost                  = "signpost"
    double_curve              = "double_curve"
    arc                       = "arc"
    price_label               = "price_label"
    price_note                = "price_note"
    arrow_marker              = "arrow_marker"
    cross_line                = "cross_line"
    horizontal_ray            = "horizontal_ray"
    trend_line                = "trend_line"
    info_line                 = "info_line"
    trend_angle               = "trend_angle"
    arrow                     = "arrow"
    ray                       = "ray"
    parallel_channel          = "parallel_channel"
    disjoint_angle            = "disjoint_angle"
    flat_bottom               = "flat_bottom"
    anchored_vwap             = "anchored_vwap"
    pitchfork                 = "pitchfork"
    schiff_pitchfork_modified = "schiff_pitchfork_modified"
    schiff_pitchfork          = "schiff_pitchfork"
    balloon                   = "balloon"
    comment                   = "comment"
    inside_pitchfork          = "inside_pitchfork"
    pitchfan                  = "pitchfan"
    gannbox                   = "gannbox"
    gannbox_square            = "gannbox_square"
    gannbox_fixed             = "gannbox_fixed"
    gannbox_fan               = "gannbox_fan"
    fib_retracement           = "fib_retracement"
    fib_trend_ext             = "fib_trend_ext"
    fib_speed_resist_fan      = "fib_speed_resist_fan"
    fib_timezone              = "fib_timezone"
    fib_trend_time            = "fib_trend_time"
    fib_circles               = "fib_circles"
    fib_spiral                = "fib_spiral"
    fib_speed_resist_arcs     = "fib_speed_resist_arcs"
    fib_channel               = "fib_channel"
    xabcd_pattern             = "xabcd_pattern"
    cypher_pattern            = "cypher_pattern"
    abcd_pattern              = "abcd_pattern"
    callout                   = "callout"
    text_note                 = "text_note"
    triangle_pattern          = "triangle_pattern"
    three_drivers_pattern     = "3divers_pattern"
    head_and_shoulders        = "head_and_shoulders"
    fib_wedge                 = "fib_wedge"
    elliott_impulse_wave      = "elliott_impulse_wave"
    elliott_triangle_wave     = "elliott_triangle_wave"
    elliott_triple_combo      = "elliott_triple_combo"
    elliott_correction        = "elliott_correction"
    elliott_double_combo      = "elliott_double_combo"
    cyclic_lines              = "cyclic_lines"
    time_cycles               = "time_cycles"
    sine_line                 = "sine_line"
    forecast                  = "forecast"
    date_range                = "date_range"
    price_range               = "price_range"
    date_and_price_range      = "date_and_price_range"
    bars_pattern              = "bars_pattern"
    ghost_feed                = "ghost_feed"
    projection                = "projection"
    rectangle                 = "rectangle"
    rotated_rectangle         = "rotated_rectangle"
    brush                     = "brush"
    highlighter               = "highlighter"
    regression_trend          = "regression_trend"
    fixed_range_volume_profile= "fixed_range_volume_profile"
#


_ONE   = {e.value for e in OnePointShape}
_MULTI = {e.value for e in MultiPointShape}


_MIN_POINTS: Dict[str, int] = {
    
    # Minimal points expected for a subset of shapes (others default to 2)

    "parallel_channel"         : 3,
    "pitchfork"                : 3,
    "schiff_pitchfork_modified": 3,
    "schiff_pitchfork"         : 3,
    "inside_pitchfork"         : 3,

    "rectangle"                : 2,
    "rotated_rectangle"        : 2,
    "date_range"               : 2,
    "price_range"              : 2,
    "date_and_price_range"     : 2,
    "trend_line"               : 2,
    "ray"                      : 2,
    "horizontal_ray"           : 2,
    "arrow"                    : 2,
    "cross_line"               : 2,
    "info_line"                : 2,
    "trend_angle"              : 2,
    "fib_retracement"          : 2,
    "fib_trend_ext"            : 2,
    "fib_speed_resist_fan"     : 2,
    "fib_timezone"             : 2,
    "fib_trend_time"           : 2,
    "fib_channel"              : 2,
}
#
###################################################################################################
###################################################################################################
################################################################################################### Shape Pointing
#
class Channel(str, Enum):
    open   = "open"
    high   = "high"
    low    = "low"
    close  = "close"
#

@dataclass(frozen=True)
class ShapePoint:

    """
    A typed point for TradingView drawings:

    kind    : 'time' | 'priced' | 'sticked'
    time_s  : int              (Unix seconds)
    price   : float | None     (PricedPoint only)
    channel : Channel | None   (StickedPoint only)
    """

    kind   : str
    time_s : int
    price  : Optional[float]  = None
    channel: Optional[Channel]= None

    # ------- factories ----------------------------------------------------------
    @staticmethod
    def _to_seconds(timestamp: Union[int, float]) -> int:

        # accept seconds or milliseconds; detect by magnitude
        if isinstance(timestamp, bool):

            raise ShapeError("Invalid time type: bool")
        #
        if not isinstance(timestamp, (int, float)):

            raise ShapeError(f"Time must be int/float seconds or ms; got {type(timestamp).__name__}")
        #

        return ((int(timestamp / 1000)) if (timestamp > 1e10) else (int(timestamp)))
    #

    @classmethod
    def time(cls, timestamp: Union[int, float]) -> "ShapePoint":

        """TimePoint."""

        return cls(kind="time", time_s=cls._to_seconds(timestamp))
    #

    @classmethod
    def priced(cls, timestamp: Union[int, float], price: Union[int, float]) -> "ShapePoint":

        """PricedPoint."""

        return cls(kind="priced", time_s=cls._to_seconds(timestamp), price=float(price))
    #

    @classmethod
    def sticked(cls, timestamp: Union[int, float], channel: Union[str, Channel]) -> "ShapePoint":
        
        """StickedPoint."""

        ch = Channel(channel) if not isinstance(channel, Channel) else channel

        return cls(kind="sticked", time_s=cls._to_seconds(timestamp), channel=ch)
    #

    def to_tv_dict(self) -> Dict[str, Any]:

        if self.kind == "time":

            return {"time": self.time_s}
        #
        if self.kind == "priced":

            return {"time": self.time_s, "price": float(self.price)}
        #
        if self.kind == "sticked":

            return {"time": self.time_s, "channel": self.channel.value}
        #

        raise ShapeError(f"Unknown ShapePoint.kind: {self.kind!r}")
    #
#
###################################################################################################
###################################################################################################
################################################################################################### Shape Overrides
#
# region All possible shape overrides. I implemented 5 of them so far. The complete list will be implemented in V2.
    # "FivepointspatternLineToolOverrides"
    # "AbcdLineToolOverrides"
    # "AnchoredvpLineToolOverrides"
    # "AnchoredvwapLineToolOverrides"
    # "ArcLineToolOverrides"
    # "ArrowLineToolOverrides"
    # "ArrowmarkdownLineToolOverrides"
    # "ArrowmarkerLineToolOverrides"
    # "ArrowmarkleftLineToolOverrides"
    # "ArrowmarkrightLineToolOverrides"
    # "ArrowmarkupLineToolOverrides"
    # "BalloonLineToolOverrides"
    # "BarspatternLineToolOverrides"
    # "BeziercubicLineToolOverrides"
    # "BezierquadroLineToolOverrides"
    # "BrushLineToolOverrides"
    # "CalloutLineToolOverrides"
    # "CircleLineToolOverrides"
    # "CommentLineToolOverrides"
    # "CrosslineLineToolOverrides"
    # "CypherpatternLineToolOverrides"
    # "DisjointangleLineToolOverrides"
    # "ElliottcorrectionLineToolOverrides"
    # "ElliottdoublecomboLineToolOverrides"
    # "ElliottimpulseLineToolOverrides"
    # "ElliotttriangleLineToolOverrides"
    # "ElliotttriplecomboLineToolOverrides"
    # "EllipseLineToolOverrides"
    # "EmojiLineToolOverrides"
    # "ExecutionLineToolOverrides"
    # "ExtendedLineToolOverrides"
    # "FibchannelLineToolOverrides"
    # "FibcirclesLineToolOverrides"
    # "FibretracementLineToolOverrides"
    # "FibspeedresistancearcsLineToolOverrides"
    # "FibspeedresistancefanLineToolOverrides"
    # "FibtimezoneLineToolOverrides"
    # "FibwedgeLineToolOverrides"
    # "FlagmarkLineToolOverrides"
    # "FlatbottomLineToolOverrides"
    # "GanncomplexLineToolOverrides"
    # "GannfanLineToolOverrides"
    # "GannfixedLineToolOverrides"
    # "GannsquareLineToolOverrides"
    # "GhostfeedLineToolOverrides"
    # "HeadandshouldersLineToolOverrides"
    # "HighlighterLineToolOverrides"
    # "HorzlineLineToolOverrides"
    # "HorzrayLineToolOverrides"
    # "IconLineToolOverrides"
    # "ImageLineToolOverrides"
    # "InfolineLineToolOverrides"
    # "InsidepitchforkLineToolOverrides"
    # "OrderLineToolOverrides"
    # "ParallelchannelLineToolOverrides"
    # "PathLineToolOverrides"
    # "PitchfanLineToolOverrides"
    # "PitchforkLineToolOverrides"
    # "PolylineLineToolOverrides"
    # "PositionLineToolOverrides"
    # "PredictionLineToolOverrides"
    # "PricelabelLineToolOverrides"
    # "ProjectionLineToolOverrides"
    # "RayLineToolOverrides"
    # "RegressiontrendLineToolOverrides"
    # "RiskrewardlongLineToolOverrides"
    # "RiskrewardshortLineToolOverrides"
    # "RotatedrectangleLineToolOverrides"
    # "SchiffpitchforkLineToolOverrides"
    # "Schiffpitchfork2LineToolOverrides"
    # "SignpostLineToolOverrides"
    # "SinelineLineToolOverrides"
    # "StickerLineToolOverrides"
    # "TextLineToolOverrides"
    # "TextabsoluteLineToolOverrides"
    # "ThreedriversLineToolOverrides"
    # "TimecyclesLineToolOverrides"
    # "TrendangleLineToolOverrides"
    # "TrendbasedfibextensionLineToolOverrides"
    # "TrendbasedfibtimeLineToolOverrides"
    # "TrendlineLineToolOverrides"
    # "TriangleLineToolOverrides"
    # "TrianglepatternLineToolOverrides"
    # "VertlineLineToolOverrides"
# endregion
#

class DrawingOverrides:

    """
    Base for typed drawing overrides. Subclasses map pythonic attributes to
    TradingView override keys (e.g., 'linewidth' -> 'linetooltrendline.linewidth').
    """

    __mapping__: Dict[str, str] = {}

    def to_dict(self) -> Dict[str, Any]:

        data: Dict[str, Any] = {}

        for f in fields(self):

            val = getattr(self, f.name)

            if val is not None:

                key = self.__mapping__.get(f.name)

                if not key:

                    raise ShapeError(f"Missing mapping for field {f.name} in {type(self).__name__}")
                #

                data[key] = val
            #
        #

        return (data)
    #
#

@dataclass(frozen=True)
class TrendlineOverrides(DrawingOverrides):

    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TrendlineLineToolOverrides/

    always_show_stats      : Optional[bool]   = None
    bold                   : Optional[bool]   = None
    extend_left            : Optional[bool]   = None
    extend_right           : Optional[bool]   = None
    fontsize               : Optional[int]    = None
    horz_labels_align      : Optional[str]    = None   # 'left'|'center'|'right'
    italic                 : Optional[bool]   = None
    left_end               : Optional[int]    = None
    linecolor              : Optional[str]    = None
    linestyle              : Optional[int]    = None   # 0.. (LineStyle enum)
    linewidth              : Optional[int]    = None
    right_end              : Optional[int]    = None
    show_angle             : Optional[bool]   = None
    show_bars_range        : Optional[bool]   = None
    show_date_time_range   : Optional[bool]   = None
    show_distance          : Optional[bool]   = None
    show_label             : Optional[bool]   = None
    show_middle_point      : Optional[bool]   = None
    show_percent_price_range: Optional[bool]  = None
    show_pips_price_range  : Optional[bool]   = None
    show_price_labels      : Optional[bool]   = None
    show_price_range       : Optional[bool]   = None
    stats_position         : Optional[int]    = None   # 0.. (position enum)
    textcolor              : Optional[str]    = None
    vert_labels_align      : Optional[str]    = None   # 'top'|'middle'|'bottom'


    __mapping__ = {
        "always_show_stats"       : "linetooltrendline.alwaysShowStats",
        "bold"                    : "linetooltrendline.bold",
        "extend_left"             : "linetooltrendline.extendLeft",
        "extend_right"            : "linetooltrendline.extendRight",
        "fontsize"                : "linetooltrendline.fontsize",
        "horz_labels_align"       : "linetooltrendline.horzLabelsAlign",
        "italic"                  : "linetooltrendline.italic",
        "left_end"                : "linetooltrendline.leftEnd",
        "linecolor"               : "linetooltrendline.linecolor",
        "linestyle"               : "linetooltrendline.linestyle",
        "linewidth"               : "linetooltrendline.linewidth",
        "right_end"               : "linetooltrendline.rightEnd",
        "show_angle"              : "linetooltrendline.showAngle",
        "show_bars_range"         : "linetooltrendline.showBarsRange",
        "show_date_time_range"    : "linetooltrendline.showDateTimeRange",
        "show_distance"           : "linetooltrendline.showDistance",
        "show_label"              : "linetooltrendline.showLabel",
        "show_middle_point"       : "linetooltrendline.showMiddlePoint",
        "show_percent_price_range": "linetooltrendline.showPercentPriceRange",
        "show_pips_price_range"   : "linetooltrendline.showPipsPriceRange",
        "show_price_labels"       : "linetooltrendline.showPriceLabels",
        "show_price_range"        : "linetooltrendline.showPriceRange",
        "stats_position"          : "linetooltrendline.statsPosition",
        "textcolor"               : "linetooltrendline.textcolor",
        "vert_labels_align"       : "linetooltrendline.vertLabelsAlign",
    }
    #
#

@dataclass(frozen=True)
class HorzlineOverrides(DrawingOverrides):

    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.HorzlineLineToolOverrides/

    bold              : Optional[bool] = None
    fontsize          : Optional[int]  = None
    horz_labels_align : Optional[str]  = None
    italic            : Optional[bool] = None
    linecolor         : Optional[str]  = None
    linestyle         : Optional[int]  = None
    linewidth         : Optional[int]  = None
    show_label        : Optional[bool] = None
    show_price        : Optional[bool] = None
    textcolor         : Optional[str]  = None
    vert_labels_align : Optional[str]  = None


    __mapping__ = {
        "bold"             : "linetoolhorzline.bold",
        "fontsize"         : "linetoolhorzline.fontsize",
        "horz_labels_align": "linetoolhorzline.horzLabelsAlign",
        "italic"           : "linetoolhorzline.italic",
        "linecolor"        : "linetoolhorzline.linecolor",
        "linestyle"        : "linetoolhorzline.linestyle",
        "linewidth"        : "linetoolhorzline.linewidth",
        "show_label"       : "linetoolhorzline.showLabel",
        "show_price"       : "linetoolhorzline.showPrice",
        "textcolor"        : "linetoolhorzline.textcolor",
        "vert_labels_align": "linetoolhorzline.vertLabelsAlign",
    }
    #
#

@dataclass(frozen=True)
class HorzrayOverrides(DrawingOverrides):

    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.RiskrewardlongLineToolOverrides/

    bold              : Optional[bool] = None
    fontsize          : Optional[int]  = None
    horz_labels_align : Optional[str]  = None
    italic            : Optional[bool] = None
    linecolor         : Optional[str]  = None
    linestyle         : Optional[int]  = None
    linewidth         : Optional[int]  = None
    show_label        : Optional[bool] = None
    show_price        : Optional[bool] = None
    textcolor         : Optional[str]  = None
    vert_labels_align : Optional[str]  = None


    __mapping__ = {
        "bold"             : "linetoolhorzray.bold",
        "fontsize"         : "linetoolhorzray.fontsize",
        "horz_labels_align": "linetoolhorzray.horzLabelsAlign",
        "italic"           : "linetoolhorzray.italic",
        "linecolor"        : "linetoolhorzray.linecolor",
        "linestyle"        : "linetoolhorzray.linestyle",
        "linewidth"        : "linetoolhorzray.linewidth",
        "show_label"       : "linetoolhorzray.showLabel",
        "show_price"       : "linetoolhorzray.showPrice",
        "textcolor"        : "linetoolhorzray.textcolor",
        "vert_labels_align": "linetoolhorzray.vertLabelsAlign",
    }
    #
#

@dataclass(frozen=True)
class RiskRewardLongOverrides(DrawingOverrides):

    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.RiskrewardlongLineToolOverrides/

    account_size                  : Optional[float] = None
    always_show_stats             : Optional[bool]  = None
    border_color                  : Optional[str]   = None
    compact                       : Optional[bool]  = None
    currency                      : Optional[str]   = None
    draw_border                   : Optional[bool]  = None
    fill_background               : Optional[bool]  = None
    fill_label_background         : Optional[bool]  = None
    fontsize                      : Optional[int]   = None
    label_background_color        : Optional[str]   = None
    linecolor                     : Optional[str]   = None
    linewidth                     : Optional[int]   = None
    lot_size                      : Optional[float] = None
    profit_background             : Optional[str]   = None
    profit_background_transparency: Optional[int]  = None
    risk                          : Optional[float] = None
    risk_display_mode             : Optional[str]   = None   # 'money'|'ticks'|'percents'
    show_price_labels             : Optional[bool]  = None
    stop_background               : Optional[str]   = None
    stop_background_transparency  : Optional[int]   = None
    textcolor                     : Optional[str]   = None


    __mapping__ = {
        "account_size"                  : "linetoolriskrewardlong.accountSize",
        "always_show_stats"             : "linetoolriskrewardlong.alwaysShowStats",
        "border_color"                  : "linetoolriskrewardlong.borderColor",
        "compact"                       : "linetoolriskrewardlong.compact",
        "currency"                      : "linetoolriskrewardlong.currency",
        "draw_border"                   : "linetoolriskrewardlong.drawBorder",
        "fill_background"               : "linetoolriskrewardlong.fillBackground",
        "fill_label_background"         : "linetoolriskrewardlong.fillLabelBackground",
        "fontsize"                      : "linetoolriskrewardlong.fontsize",
        "label_background_color"        : "linetoolriskrewardlong.labelBackgroundColor",
        "linecolor"                     : "linetoolriskrewardlong.linecolor",
        "linewidth"                     : "linetoolriskrewardlong.linewidth",
        "lot_size"                      : "linetoolriskrewardlong.lotSize",
        "profit_background"             : "linetoolriskrewardlong.profitBackground",
        "profit_background_transparency": "linetoolriskrewardlong.profitBackgroundTransparency",
        "risk"                          : "linetoolriskrewardlong.risk",
        "risk_display_mode"             : "linetoolriskrewardlong.riskDisplayMode",
        "show_price_labels"             : "linetoolriskrewardlong.showPriceLabels",
        "stop_background"               : "linetoolriskrewardlong.stopBackground",
        "stop_background_transparency"  : "linetoolriskrewardlong.stopBackgroundTransparency",
        "textcolor"                     : "linetoolriskrewardlong.textcolor",
    }
    #
#

@dataclass(frozen=True)
class RiskRewardShortOverrides(DrawingOverrides):

    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.RiskrewardshortLineToolOverrides/

    account_size                  : Optional[float] = None
    always_show_stats            : Optional[bool]  = None
    border_color                 : Optional[str]   = None
    compact                      : Optional[bool]  = None
    currency                     : Optional[str]   = None
    draw_border                  : Optional[bool]  = None
    fill_background              : Optional[bool]  = None
    fill_label_background        : Optional[bool]  = None
    fontsize                     : Optional[int]   = None
    label_background_color       : Optional[str]   = None
    linecolor                    : Optional[str]   = None
    linewidth                    : Optional[int]   = None
    lot_size                     : Optional[float] = None
    profit_background            : Optional[str]   = None
    profit_background_transparency: Optional[int]  = None
    risk                         : Optional[float] = None
    risk_display_mode            : Optional[str]   = None
    show_price_labels            : Optional[bool]  = None
    stop_background              : Optional[str]   = None
    stop_background_transparency : Optional[int]   = None
    textcolor                    : Optional[str]   = None


    __mapping__ = {
        "account_size"                   : "linetoolriskrewardshort.accountSize",
        "always_show_stats"             : "linetoolriskrewardshort.alwaysShowStats",
        "border_color"                  : "linetoolriskrewardshort.borderColor",
        "compact"                       : "linetoolriskrewardshort.compact",
        "currency"                      : "linetoolriskrewardshort.currency",
        "draw_border"                   : "linetoolriskrewardshort.drawBorder",
        "fill_background"               : "linetoolriskrewardshort.fillBackground",
        "fill_label_background"         : "linetoolriskrewardshort.fillLabelBackground",
        "fontsize"                      : "linetoolriskrewardshort.fontsize",
        "label_background_color"        : "linetoolriskrewardshort.labelBackgroundColor",
        "linecolor"                     : "linetoolriskrewardshort.linecolor",
        "linewidth"                     : "linetoolriskrewardshort.linewidth",
        "lot_size"                      : "linetoolriskrewardshort.lotSize",
        "profit_background"             : "linetoolriskrewardshort.profitBackground",
        "profit_background_transparency": "linetoolriskrewardshort.profitBackgroundTransparency",
        "risk"                          : "linetoolriskrewardshort.risk",
        "risk_display_mode"             : "linetoolriskrewardshort.riskDisplayMode",
        "show_price_labels"             : "linetoolriskrewardshort.showPriceLabels",
        "stop_background"               : "linetoolriskrewardshort.stopBackground",
        "stop_background_transparency"  : "linetoolriskrewardshort.stopBackgroundTransparency",
        "textcolor"                     : "linetoolriskrewardshort.textcolor",
    }
    #
#

# Type hints
AnyDrawingOverrides = Union[
    TrendlineOverrides,
    HorzlineOverrides,
    HorzrayOverrides,
    RiskRewardLongOverrides,
    RiskRewardShortOverrides,
]
#
###################################################################################################
###################################################################################################
################################################################################################### Shape Options
#
@dataclass(frozen=True)
class ShapeOptions:

    """
    Options for TradingView drawings (complete).

    Fields map 1:1 to CreateShapeOptionsBase / CreateShapeOptions /
    CreateMultipointShapeOptions. Anything not provided is omitted.

    text              : Optional[str]
        Text for drawing

    zOrder            : Optional[str]
        "top" or "bottom". Create the drawing in front of all other drawings, or behind all other drawings.
    
    lock              : Optional[bool]
        If True, the drawing is HARD-locked.
    
    showInObjectsTree : Optional[bool]
        Enable/disable showing the drawing in the objects tree.

    disableSelection  : Optional[bool]
        Disable/enable selecting the drawing.

    disableSave       : Optional[bool]
        Disable/enable saving the drawing.

    disableUndo       : Optional[bool]
        If true, users cannot cancel the drawing creation in the UI. However, users can still click the Undo button to cancel previous actions.
    
    filled            : Optional[bool]
        Enable/disable filling the drawing with color (if the drawing supports filling).

    icon              : Optional[Union[int, str]]
        Icon code for 'icon' shape. Must be a hex NUMBER (e.g., 0xf02d).
        If a string like "0xf02d" or "f02d" is given, it will be parsed.

    ownerStudyId      : Optional[Union[int, str]]
        ID of the indicator this drawing is attached to.

    overrides         : Optional[Dict[str, Any]]
        Drawing style overrides. Keys are per-tool (see TV docs).
    """
    
    text             : Optional[str]            = None
    zOrder           : Optional[str]            = None
    lock             : Optional[bool]           = None
    showInObjectsTree: Optional[bool]           = None
    disableSelection : Optional[bool]           = None
    disableSave      : Optional[bool]           = None
    disableUndo      : Optional[bool]           = None
    filled           : Optional[bool]           = None
    icon             : Optional[Union[int,str]] = None
    ownerStudyId     : Optional[Union[int,str]] = None
    overrides        : Optional[Union[Dict[str, Any], DrawingOverrides]] = None


    def _parse_icon(self, icon: Union[int, str]) -> int:

        if isinstance(icon, int):

            return icon
        #

        s = str(icon).strip().lower()

        if s.startswith("0x"):

            return int(s, 16)
        #

        # pure hex like "f02d" or decimal string "61485"
        try:

            return int(s, 16) if all(c in "0123456789abcdef" for c in s) else int(s, 10)
        #
        except Exception as e:

            raise ShapeError(f"icon must be hex number (e.g., 0xf02d) or int; got {icon!r}") from e
        #
    #

    def to_dict(self, shape_value: str) -> Dict[str, Any]:

        out: Dict[str, Any] = {"shape": shape_value}

        if self.text               is not None: out["text"]               = str(self.text)
        if self.zOrder             is not None:
            z = str(self.zOrder).lower()
            if z not in ("top", "bottom"): raise ShapeError("zOrder must be 'top' or 'bottom'")
            out["zOrder"] = z
        #
        if self.lock               is not None: out["lock"]               = bool(self.lock)
        if self.showInObjectsTree  is not None: out["showInObjectsTree"]  = bool(self.showInObjectsTree)
        if self.disableSelection   is not None: out["disableSelection"]   = bool(self.disableSelection)
        if self.disableSave        is not None: out["disableSave"]        = bool(self.disableSave)
        if self.disableUndo        is not None: out["disableUndo"]        = bool(self.disableUndo)
        if self.filled             is not None: out["filled"]             = bool(self.filled)
        if self.icon               is not None: out["icon"]               = self._parse_icon(self.icon)
        if self.ownerStudyId       is not None: out["ownerStudyId"]       = self.ownerStudyId
        
        if (self.overrides):

            if isinstance(self.overrides, DrawingOverrides):

                ov = self.overrides.to_dict()
            #
            elif isinstance(self.overrides, dict):

                ov = dict(self.overrides)
            #
            else:

                raise ShapeError("overrides must be a dict or a DrawingOverrides")
            #

            out["overrides"] = _normalize_override_keys(ov)
        #

        return out
    #
#
###################################################################################################
###################################################################################################
################################################################################################### Helpers
#
class ShapeError(Exception):

    pass
#

def _server_url_from_registry() -> str:

    """Resolve backend base URL from backend/datafeed/registry.json (with fallback)."""

    package_dir   = Path(__file__).parent
    datafeed_dir  = package_dir / "backend" / "datafeed"
    datafeed_dir.mkdir(parents=True, exist_ok=True)
    registry_path = datafeed_dir / "registry.json"

    try:

        with open(registry_path, "r", encoding="utf-8") as f:

            reg = json.load(f) or {}
        #
    #
    except Exception:

        reg = {}
    #

    return reg.get("server_url", "http://localhost:8000")
#

def _symbol_str(symbol:Union["Symbol", str]) -> str:

    return ((symbol.ticker) if (isinstance(symbol, Symbol)) else (str(symbol)))
#

def _normalize_override_keys(ov:Dict[str, Any]) -> Dict[str, Any]:
    
    """
    Convert keys like 'linetooltrendline.linewidth' to 'linewidth' for
    createShape/createMultipointShape overrides.
    """

    out: Dict[str, Any] = {}
    for k, v in ov.items():

        key = k.split(".", 1)[1] if "." in k else k
        out[key] = v
    #

    return out
#

def _normalize_points(points:Union[ShapePoint, Sequence[ShapePoint]]) -> List[Dict[str, Any]]:
    
    pts = [points] if isinstance(points, ShapePoint) else list(points)

    if (not pts):

        raise ShapeError("points: empty")
    #

    return [p.to_tv_dict() for p in pts]
#

def _shape_value(shape_type:ShapeType) -> str:

    return (shape_type.value)
#

def _is_one_point(shape_value:str) -> bool:

    return (shape_value in _ONE)
#

def _required_points(shape_value:str) -> int:

    if (shape_value in _ONE):

        return 1
    #

    return (_MIN_POINTS.get(shape_value, 2))
#

def _options_to_dict(options:Optional[Union[ShapeOptions, Dict[str, Any], DrawingOverrides]], shape_value:str) -> Dict[str, Any]:
    
    if options is None:

        return {"shape": shape_value}
    #

    # ShapeOptions → dict
    if isinstance(options, ShapeOptions):

        out = options.to_dict(shape_value)

        # if overrides is a typed overrides instance, convert it
        ov = out.get("overrides")
        if isinstance(ov, DrawingOverrides):

            out["overrides"] = _normalize_override_keys(ov)
        #

        return out
    #

    # Direct typed overrides object
    if isinstance(options, DrawingOverrides):

        return {"shape": shape_value, "overrides": _normalize_override_keys(options.to_dict())}
    #

    # Raw dict (power users)
    if isinstance(options, dict):

        out = dict(options)
        out["shape"] = shape_value

        # allow {"overrides": <typed>}
        if "overrides" in out:

            if isinstance(out["overrides"], DrawingOverrides):

                out["overrides"] = out["overrides"].to_dict()
            #
            
            if isinstance(out["overrides"], dict):

                out["overrides"] = _normalize_override_keys(out["overrides"])
            #
        #

        # validate a couple obvious things
        if "zOrder" in out:

            z = str(out["zOrder"]).lower()

            if z not in ("top", "bottom"):

                raise ShapeError("zOrder must be 'top' or 'bottom'")
            #

            out["zOrder"] = z
        #

        if "icon" in out and isinstance(out["icon"], str):

            s = out["icon"].strip().lower()
            out["icon"] = int(s, 16) if s.startswith("0x") or all(c in "0123456789abcdef" for c in s) else int(s, 10)
        #

        return out
    #

    raise ShapeError("options must be ShapeOptions, a dict, or a DrawingOverrides")
#
###################################################################################################
###################################################################################################
################################################################################################### Shaping
#
def CreateShape(symbol:Symbol|str, shape_type:ShapeType, points:Union[ShapePoint, Sequence[ShapePoint]], *, options:Optional[Union[ShapeOptions, Dict[str, Any]]] = None) -> Dict:
    
    """
    Create a TradingView drawing with typed points.

    Parameters
    ----------
    symbol     : Symbol
    shape_type : ShapeType
    points     : ShapePoint | list[ShapePoint]
    options    : ShapeOptions | dict | None
        Complete set per TradingView: text, zOrder, lock, showInObjectsTree,
        disableSelection, disableSave, disableUndo, filled, icon, ownerStudyId,
        overrides (pass-through per-tool). We inject `shape` automatically.

    Returns: dict (backend Shape row)
    """

    server_url  = _server_url_from_registry()
    shape_value = _shape_value(shape_type)
    pts         = _normalize_points(points)

    # enforce point count for 1pt vs multipoint
    need = _required_points(shape_value)

    if (_is_one_point(shape_value) and len(pts) != 1):

        raise ShapeError(f"{shape_value}: expected exactly 1 point, got {len(pts)}")
    #
    if (not _is_one_point(shape_value) and len(pts) < need):

        raise ShapeError(f"{shape_value}: need at least {need} point(s), got {len(pts)}")
    #

    payload = {
        "symbol"    : _symbol_str(symbol),
        "shape_type": shape_value,
        "points"    : pts,
        "options"   : _options_to_dict(options, shape_value),
    }

    response = requests.post(f"{server_url}/shapes", json=payload, timeout=10)

    if (response.status_code >= 400):

        raise ShapeError(f"CreateShape failed: {response.status_code} {response.text}")
    #

    return (response.json())
#

def GetAllShapes(symbol:Union["Symbol", str]) -> list[dict]:

    """
    Return all shapes for a symbol as a list of dicts (exactly what /shapes returns).
    """

    server_url = _server_url_from_registry()
    sym        = _symbol_str(symbol)

    try:

        r = requests.get(f"{server_url}/shapes", params={"symbol": sym}, timeout=10)
        r.raise_for_status()
        data = r.json()
        return list(data.get("items", []))
    #
    except Exception as e:

        raise ShapeError(f"GetAllShapes failed: {e}") from e
    #
#

def RemoveShape(symbol:Union["Symbol", str], shape_id:int) -> bool:

    """
    Delete a single shape by its database id. `symbol` is accepted for symmetry,
    but deletion is keyed by id on the backend.
    Returns True on success.
    """

    server_url = _server_url_from_registry()

    try:

        r = requests.delete(f"{server_url}/shapes/{int(shape_id)}", timeout=10)

        if r.status_code == 404:

            return False
        #

        r.raise_for_status()
        j = r.json() if r.content else {}

        return (bool(j.get("ok", True)))
    #
    except Exception as e:

        raise ShapeError(f"RemoveShape failed: {e}") from e
    #
#

def RemoveAllShapes(symbol:Union["Symbol", str]) -> int:

    """
    Delete ALL shapes for a symbol.
    Returns the count of successfully deleted rows.
    """

    items = GetAllShapes(symbol)

    if not items:

        return 0
    #

    server_url = _server_url_from_registry()
    deleted    = 0
    for rec in items:

        try:

            rid = int(rec["id"])
            r = requests.delete(f"{server_url}/shapes/{rid}", timeout=10)
            if r.ok:

                deleted += 1
            #
        #
        except Exception:

            # swallow and continue so a single failure doesn't stop the batch
            pass
        #
    #

    return (deleted)
#


class Shapes:

    """Small facade around shape endpoints. Keeps your nice dataclasses as-is."""

    def __init__(self, symbol:Symbol|str, server_url:str|None=None):

        self.symbol     = _symbol_str(symbol)
        self.server_url = server_url or _server_url_from_registry()
    #


    def create(self, shape_type:ShapeType, points:ShapePoint|Sequence[ShapePoint], options:ShapeOptions|dict|DrawingOverrides|None=None) -> dict:

        return CreateShape(self.symbol, shape_type, points, options=options)
    #

    def all(self) -> list[dict]:

        return GetAllShapes(self.symbol)
    #

    def remove(self, shape_id: int) -> bool:

        return RemoveShape(self.symbol, shape_id)
    #

    def remove_all(self) -> int:

        return RemoveAllShapes(self.symbol)
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
#