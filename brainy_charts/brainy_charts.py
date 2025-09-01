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
import pandas as pd
import json
#
###################################################################################################
###################################################################################################
################################################################################################### Chart Model
#
class ChartData:

    '''
    The tohlcv_df must contain 'timestamp', 'open', 'high', 'low', 'close', 'volume' columns.
    The 'timestamp' column must be in milliseconds, and it must be in ascending order.
    '''
    instances_count = 0

    def __init__(self,
                tohlcv_df              = pd.DataFrame(),
                ticker                 = "ticker",
                full_name              = "full_name",
                description            = "description",
                type                   = "type",

                exchange               = "exchange",
                listed_exchange        = "listed_exchange",
                session                = "24x7",
                timezone               = "UTC",

                minmov                 = 1,
                minmov2                = 0,
                pricescale             = 100,
                pointvalue             = 1,

                has_intraday           = True,
                has_daily              = True,
                has_weekly_and_monthly = True,
                currency_code          = "USDT",
                visible_plots_set      = "ohlcv",
                supported_resolutions  = ["1", "5", "15", "30", "60", "240", "D", "W"]
    ):
        ChartData.instances_count  += 1
        
        self.tohlcv_df              = tohlcv_df
        self.name                   = f"{ticker}_{exchange}"
        self.ticker                 = ticker
        self.full_name              = full_name
        self.description            = description
        self.type                   = type

        self.exchange               = exchange
        self.listed_exchange        = listed_exchange
        self.session                = session
        self.timezone               = timezone

        self.minmov                 = minmov
        self.minmov2                = minmov2
        self.pricescale             = pricescale
        self.pointvalue             = pointvalue
        
        self.has_intraday           = has_intraday
        self.has_daily              = has_daily
        self.has_weekly_and_monthly = has_weekly_and_monthly
        self.currency_code          = currency_code
        self.visible_plots_set      = visible_plots_set
        self.supported_resolutions  = supported_resolutions
    #
#
###################################################################################################
###################################################################################################
################################################################################################### BrainyChart
#
class BrainyChart:

    def __init__(self, chart_data_list:Optional[List[ChartData]]=None, port=8000, verbose:bool=False, jupyter:bool=True):
        
        package_dir  = Path(__file__).parent
        datafeed_dir = package_dir / "backend" / "datafeed"
        datafeed_dir.mkdir(parents=True, exist_ok=True)

        if (chart_data_list is not None):
            
            registry = {}

            for chart_data in chart_data_list:

                symbol_id = f"{chart_data.ticker}_{chart_data.exchange}"
                
                csv_path = datafeed_dir / f"{symbol_id}.csv"
                chart_data.tohlcv_df.to_csv(csv_path, index=False)

                registry[symbol_id] = self.chart_data_as_dict(chart_data)
            #

            with open(datafeed_dir / "registry.json", "w") as f:

                json.dump(registry, f, indent=2)
            #
        #

        
        self._port    = port
        self._url     = f"http://localhost:{port}"
        self._verbose = verbose
        self._jupyter = jupyter
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
            "has_intraday"           : chart_data.has_intraday,
            "has_daily"              : chart_data.has_daily,
            "has_weekly_and_monthly" : chart_data.has_weekly_and_monthly,
            "currency_code"          : chart_data.currency_code,
            "visible_plots_set"      : chart_data.visible_plots_set,
            "supported_resolutions"  : chart_data.supported_resolutions
        }
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

    def run_backend(self):

        try:

            print(f"Starting backend server on port {self._port}...")

            package_dir = Path(__file__).parent
            cmd = [
                "uvicorn", 
                "backend.main:app",
                "--host", "0.0.0.0",
                "--port", "8001"
            ]
            shell = False
            
            if (self._verbose==True):

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

            print(f"Error running frontend server: {e}")
        #
    #

    def run_frontend(self):

        try:

            print(f"Starting frontend server on port {self._port}...")

            package_dir = Path(__file__).parent.parent
            cmd = [
                "python3", 
                "-m",
                "http.server",
                f"{self._port}",
            ]
            shell = False

            if (self._verbose==True):

                subprocess.Popen(
                    cmd,
                    cwd=f"{package_dir}/brainy_charts",
                    shell=shell,
                )
            #
            else:

                with open(os.devnull, 'w') as fnull:
                    subprocess.Popen(
                        cmd,
                        cwd=f"{package_dir}/brainy_charts",
                        shell=shell,
                        stdout=fnull,
                        stderr=fnull
                    )
                #
            #
        #
        except Exception as e:

            print(f"Error running frontend server: {e}")
        #
    #

    def imagine(self, width=1200, height=600):

        self.kill_servers()
        self.run_backend()
        self.run_frontend()
        print("Please wait...")
        time.sleep(4)


        if (not self._verbose or self._jupyter):

            clear_output()
        #


        if (self._jupyter):

            return (IFrame(src=self._url, width=width, height=height))
        #
        else:

            return (None)
        #
    #
#
###################################################################################################
###################################################################################################
################################################################################################### Shape Manager
#
one_point_shapes   = [
    "emoji", "text", "icon", "anchored_text", "anchored_note", "note",
    "sticker", "arrow_up", "arrow_down", "flag", "vertical_line",
    "horizontal_line", "long_position", "short_position"
]
multi_point_shapes = [
    "triangle", "curve", "table", "circle", "ellipse", "path", "polyline",
    "extended", "signpost", "double_curve", "arc", "price_label", "price_note",
    "arrow_marker", "cross_line", "horizontal_ray", "trend_line", "info_line",
    "trend_angle", "arrow", "ray", "parallel_channel", "disjoint_angle",
    "flat_bottom", "anchored_vwap", "pitchfork", "schiff_pitchfork_modified",
    "schiff_pitchfork", "balloon", "comment", "inside_pitchfork", "pitchfan",
    "gannbox", "gannbox_square", "gannbox_fixed", "gannbox_fan", "fib_retracement",
    "fib_trend_ext", "fib_speed_resist_fan", "fib_timezone", "fib_trend_time",
    "fib_circles", "fib_spiral", "fib_speed_resist_arcs", "fib_channel",
    "xabcd_pattern", "cypher_pattern", "abcd_pattern", "callout", "text_note",
    "triangle_pattern", "3divers_pattern", "head_and_shoulders", "fib_wedge",
    "elliott_impulse_wave", "elliott_triangle_wave", "elliott_triple_combo",
    "elliott_correction", "elliott_double_combo", "cyclic_lines", "time_cycles",
    "sine_line", "forecast", "date_range", "price_range", "date_and_price_range",
    "bars_pattern", "ghost_feed", "projection", "rectangle", "rotated_rectangle",
    "brush", "highlighter", "regression_trend", "fixed_range_volume_profile"
]
#

class BrainyShape:

    def __init__(self, base_url:str="http://localhost:8001", default_chart_id:int=1):

        self.base_url         = base_url
        self.default_chart_id = default_chart_id
    #

    def _generate_random_code(self, length:int=6) -> int:

        return (random.randint(10**(length-1), (10**length)-1))
    #

    def create_or_update_shape(self, shape_type:str, points:List[Dict[str, float]], properties:Dict, shape_code:Optional[int]=None, shape_id:Optional[str]=None, default_chart_id:int=1) -> Dict:
        
        chart_id   = default_chart_id
        shape_code = shape_code or self._generate_random_code()
        shape_id   = shape_id
        
        is_one_point = shape_type in one_point_shapes
        
        if (is_one_point       and len(points) != 1):

            raise ValueError(f"Shape type {shape_type} requires 1 point")
        #
        elif (not is_one_point and len(points) < 2):

            raise ValueError(f"Shape type {shape_type} requires at least 2 points")
        #
        
        payload = {
            "shape_id": shape_id,
            "shape_type": shape_type,
            "shape_code": shape_code,
            "shape_data": {
                "points": points,
                "properties": properties
            }
        }
        
        url      = f"{self.base_url}/charts/{chart_id}/shapes/"
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return {
            **response.json(),
            "is_one_point": is_one_point,
            "shape_type": shape_type,
            "shape_code": shape_code
        }
    #

    def get_all_shapes(self) -> List[Dict]:

        chart_id = self.default_chart_id
        url      = f"{self.base_url}/charts/{chart_id}/shapes/"
        response = requests.get(url)
        response.raise_for_status()
        return (response.json())
    #

    def get_shape(self, shape_code:int) -> Dict:

        chart_id = self.default_chart_id
        url      = f"{self.base_url}/charts/{chart_id}/shapes/{shape_code}"
        
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

    def delete_shape(self, shape_code:int) -> Dict:
        
        chart_id = self.default_chart_id
        url      = f"{self.base_url}/charts/{chart_id}/shapes/{shape_code}"
        response = requests.delete(url)
        response.raise_for_status()

        return (response.json())
    #

    def delete_all_shapes(self) -> Dict:

        chart_id = self.default_chart_id
        url      = f"{self.base_url}/charts/{chart_id}/shapes/"
        response = requests.delete(url)
        response.raise_for_status()

        return (response.json())
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
