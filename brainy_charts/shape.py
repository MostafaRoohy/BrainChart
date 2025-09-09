#
# https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/
# https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/Drawings-List
# https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/drawings-api
#
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createshape
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateShapeOptions/
#
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#getshapebyid
#
#
#
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createmultipointshape
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateMultipointShapeOptions/
#
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createexecutionshape
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IExecutionLineAdapter/
#
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createanchoredshape
# https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.CreateAnchoredShapeOptions/
#
###################################################################################################
###################################################################################################
################################################################################################### Shape Constants
#
one_point_shapes   = [
    "emoji"          , "text"             , "icon"             , "anchored_text"    , "anchored_note"    , "note",
    "sticker"        , "arrow_up"         , "arrow_down"       , "flag"             , "vertical_line"    ,
    "horizontal_line", "long_position"    , "short_position"
]
#

multi_point_shapes = [
    "triangle"             , "curve"                  , "table"                  , "circle"                    , "ellipse"                , "path"                   , "polyline",
    "extended"             , "signpost"               , "double_curve"           , "arc"                       , "price_label"            , "price_note"             ,
    "arrow_marker"         , "cross_line"             , "horizontal_ray"         , "trend_line"                , "info_line"              ,
    "trend_angle"          , "arrow"                  , "ray"                    , "parallel_channel"          , "disjoint_angle"         ,
    "flat_bottom"          , "anchored_vwap"          , "pitchfork"              , "schiff_pitchfork_modified" , "schiff_pitchfork"       ,
    "balloon"              , "comment"                , "inside_pitchfork"       , "pitchfan"                  ,
    "gannbox"              , "gannbox_square"         , "gannbox_fixed"          , "gannbox_fan"               , "fib_retracement"        ,
    "fib_trend_ext"        , "fib_speed_resist_fan"   , "fib_timezone"           , "fib_trend_time"            ,
    "fib_circles"          , "fib_spiral"             , "fib_speed_resist_arcs"  , "fib_channel"               ,
    "xabcd_pattern"        , "cypher_pattern"         , "abcd_pattern"           , "callout"                   , "text_note"              ,
    "triangle_pattern"     , "3divers_pattern"        , "head_and_shoulders"     , "fib_wedge"                 ,
    "elliott_impulse_wave" , "elliott_triangle_wave"  , "elliott_triple_combo"   ,
    "elliott_correction"   , "elliott_double_combo"   , "cyclic_lines"           , "time_cycles"               ,
    "sine_line"            , "forecast"               , "date_range"             , "price_range"               , "date_and_price_range"   ,
    "bars_pattern"         , "ghost_feed"             , "projection"             , "rectangle"                 , "rotated_rectangle"      ,
    "brush"                , "highlighter"            , "regression_trend"       , "fixed_range_volume_profile"
]
#
###################################################################################################
###################################################################################################
###################################################################################################
#