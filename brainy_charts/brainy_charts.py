# This module provides the main user-facing classes, BrainyChart,
# which is used to start the charting application and interact with its drawing features.
###################################################################################################
###################################################################################################
###################################################################################################
#
import os
import sys
import subprocess
import platform
import requests
import time
import random
import logging
from pathlib import Path
from typing import List, Dict, Optional, Literal
from IPython.display import IFrame
from IPython.display import clear_output
import json
from .chart_data import ChartData
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

index_html_raw = r'''
<!-- https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#additional_symbol_info_fields -->

<!DOCTYPE HTML>
<html>

    <head>

        <title>BrainyCharts</title>
        
        <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0">
        <script type="text/javascript" src="/charting_library/charting_library/charting_library.standalone.js"></script>
        <script type="text/javascript" src="/charting_library/datafeeds/udf/dist/bundle.js"></script>

        <script type="text/javascript">

            function getParameterByName(name) 
            {{
                name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
                var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
                    results = regex.exec(location.search);
                return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
            }}

            function initOnReady() 
            {{
                var datafeedUrl   = window.location.origin;
                var customDataUrl = getParameterByName('dataUrl');

                if (customDataUrl !== "") 
                {{
                    datafeedUrl = customDataUrl.startsWith('https://') ? customDataUrl : `https://${{customDataUrl}}`;
                }}


                var widget = window.tvWidget = new TradingView.widget(
                {{
                    library_path : "/charting_library/charting_library/",
                    container    : "tv_chart_container",
                    datafeed     : new Datafeeds.UDFCompatibleDatafeed(datafeedUrl, undefined, {{maxResponseLength: 1000, expectedOrder: 'latestFirst'}}),
                    
                    fullscreen : true,
                    theme      : '{theme}',

                    symbol          : '{default_symbol}',
                    interval        : '1',
                    // https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#load_last_chart
                    // load_last_chart : true,

                    <!-- https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets/ -->
                    disabled_features : ["use_localstorage_for_settings"],
                    enabled_features  : ["study_templates"],

                    charts_storage_url         : 'https://saveload.tradingview.com',
                    charts_storage_api_version : "1.1",

                    // custom_indicators_getter: ???



                }});


                window.frames[0].focus();
            }};

            window.addEventListener('DOMContentLoaded', initOnReady, false);

        </script>

    </head>

    <body style="margin:0px;">

        <div id="tv_chart_container"></div>
        
    </body>

</html>
'''
#
###################################################################################################
###################################################################################################
################################################################################################### BrainyChart
#
class BrainyChart:

    def __init__(self, chart_data_list:List[ChartData], default_chart:ChartData=None, theme:str=['dark', 'light'], server_port=8000, verbose:bool=False, jupyter:bool=False):
        
        if (chart_data_list is None):

            raise
        #


        package_dir  = Path(__file__).parent
        datafeed_dir = package_dir / "backend" / "datafeed"
        datafeed_dir.mkdir(parents=True, exist_ok=True)
            
        registry = {}
        for chart_data in chart_data_list:

            symbol_id           = f"{chart_data.ticker}_{chart_data.exchange}"
            csv_path            = datafeed_dir / f"{symbol_id}.csv"
            registry[symbol_id] = self.chart_data_as_dict(chart_data)
            chart_data.tohlcv_df.to_csv(csv_path, index=False)
        #
        with open(datafeed_dir/"registry.json", "w") as f:

            json.dump(registry, f, indent=2)
        #
        with open(package_dir/"frontend"/"chart_widget"/"index.html", "w") as file:

            theme          = (theme)              if (theme is not None)         else ("dark")
            default_symbol = (default_chart.name) if (default_chart is not None) else (chart_data_list[0].name)

            file.write(index_html_raw.format(theme=theme, default_symbol=default_symbol))
        #


        self.server_port = server_port
        self.server_url  = f"http://localhost:{self.server_port}"

        self.verbose     = verbose
        self.jupyter     = jupyter
    #

    def chart_data_as_dict(self, chart_data:ChartData) -> dict:

        return {
            "name"                   : chart_data.name,
            "ticker"                 : chart_data.ticker,
            "full_name"              : chart_data.full_name,
            "description"            : chart_data.description,
            "type"                   : chart_data.type,
            "exchange"               : chart_data.exchange,
            "listed_exchange"        : chart_data.listed_exchange,
            "session"                : chart_data.session,
            "timezone"               : chart_data.timezone,
            "minmov"                 : chart_data.minmov,
            "minmov2"                : chart_data.minmov2,
            "pricescale"             : chart_data.pricescale,
            "pointvalue"             : chart_data.pointvalue,
            "has_seconds"            : chart_data.has_seconds,
            "has_intraday"           : chart_data.has_intraday,
            "has_daily"              : chart_data.has_daily,
            "has_weekly_and_monthly" : chart_data.has_weekly_and_monthly,
            "currency_code"          : chart_data.currency_code,
            "visible_plots_set"      : chart_data.visible_plots_set,
            "supported_resolutions"  : chart_data.supported_resolutions,
        }
    #
    ##############################################################
    #
    def run_servers(self):

        try:

            print(f"Starting server on port {self.server_port}...")

            package_dir = Path(__file__).parent
            cmd = [
                "uvicorn", 
                "backend.main:app",
                "--host", "0.0.0.0",
                "--port", str(self.server_port)
            ]
            shell = False
            
            if (self.verbose==True):

                server_process = subprocess.Popen(
                    cmd,
                    cwd=str(package_dir),
                    shell=shell
                )
                            
                return (server_process)
            #
            else:

                with open(os.devnull, 'w') as fnull:
                    server_process = subprocess.Popen(
                        cmd,
                        cwd=str(package_dir),
                        shell=shell,
                        stdout=fnull,
                        stderr=fnull
                    )
                #
                
                return (server_process)
            #
        #
        except Exception as e:

            print(f"Error running server: {e}")
        #
    #

    def kill_servers(self):

        try:

            subprocess.run(["pkill", "-f", "uvicorn"]    , check=True)
            subprocess.run(["pkill", "-f", "http.server"], check=True)
        #
        except subprocess.CalledProcessError:

            pass
        #
    #

    def imagine(self, width=1200, height=600):

        self.kill_servers()
        self.run_servers()

        print("Please wait...")
        time.sleep(4)


        if (not self.verbose or self.jupyter):

            clear_output()
        #


        if (self.jupyter):

            return (IFrame(src=self.server_url, width=width, height=height))
        #
        else:
            
            print(f"Please navigate to: {self.server_url}")
            return (None)
        #
    #
    ##############################################################
    #
    def generate_random_code(self, length:int=6) -> int:

        return (random.randint(10**(length-1), (10**length)-1))
    #

    def create_or_update_shape(self, chart_data:ChartData, shape_type:str, points:List[Dict[str, float]], properties:Dict, shape_code:Optional[int]=None, shape_id:Optional[str]=None) -> Dict:
        
        symbol_id  = f"{chart_data.ticker}_{chart_data.exchange}"
        shape_code = shape_code or self.generate_random_code()
        shape_id   = shape_id
        
        is_one_point = shape_type in one_point_shapes
        
        if (is_one_point       and len(points) != 1):

            raise ValueError(f"Shape type {shape_type} requires 1 point")
        #
        elif (not is_one_point and len(points) < 2):

            raise ValueError(f"Shape type {shape_type} requires at least 2 points")
        #
        
        payload = {
            "shape_id"   : shape_id,
            "shape_type" : shape_type,
            "shape_code" : shape_code,
            "shape_data" : {"points":points, "properties":properties}
        }
        
        url      = f"{self.server_url}/shapes/{symbol_id}"
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return {
            **response.json(),
            "is_one_point": is_one_point,
            "shape_type": shape_type,
            "shape_code": shape_code
        }
    #

    def get_all_shapes(self, chart_data:ChartData) -> List[Dict]:

        symbol_id = f"{chart_data.ticker}_{chart_data.exchange}"
        
        url       = f"{self.server_url}/shapes/{symbol_id}"
        response  = requests.get(url)
        response.raise_for_status()
        return (response.json())
    #

    def get_shape(self, shape_code:int) -> Dict:

        chart_id = self.chart_id
        url      = f"{self.server_url}/charts/{chart_id}/shapes/{shape_code}"
        
        try:

            response = requests.get(url)
            response.raise_for_status()

            return (response.json())
        #
        except requests.exceptions.HTTPError as e:

            if (e.response.status_code == 404):

                raise ValueError(f"Shape with code {shape_code} not found") from e
            #
            raise
        #
    #

    def delete_shape(self, chart_data:ChartData, shape_code:int) -> Dict:
        
        symbol_id = f"{chart_data.ticker}_{chart_data.exchange}"

        url      = f"{self.server_url}/shapes/{symbol_id}/{shape_code}"
        response = requests.delete(url)
        response.raise_for_status()

        return (response.json())
    #

    def delete_all_shapes(self, chart_data:ChartData) -> Dict:

        symbol_id = f"{chart_data.ticker}_{chart_data.exchange}"
        url       = f"{self.server_url}/shapes/{symbol_id}"
        response = requests.delete(url)
        response.raise_for_status()

        return (response.json())
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
