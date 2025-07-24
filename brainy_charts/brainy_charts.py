import os
import sys
import subprocess
import platform
import requests
import time
import random
import logging
from pathlib import Path
from typing import List, Dict, Optional
from IPython.display import IFrame
from IPython.display import clear_output
import pandas as pd
from .chart_data import ChartData
import json
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
                    cwd=f"{package_dir}/charting_library",
                    shell=shell,
                )
            #
            else:

                with open(os.devnull, 'w') as fnull:
                    subprocess.Popen(
                        cmd,
                        cwd=f"{package_dir}/charting_library",
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
###################################################################################################
#