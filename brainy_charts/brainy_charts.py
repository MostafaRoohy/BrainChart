#
# The main user-facing classe, BrainyChart, which is used to start the application.
#
###################################################################################################
###################################################################################################
################################################################################################### Modules
#
import os
import shutil
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
#
###################################################################################################
###################################################################################################
################################################################################################### Modules
#
from .symbol import Symbol
from .widget import ChartWidget
#
###################################################################################################
###################################################################################################
################################################################################################### BrainyChart
#
class BrainyChart:

    def __init__(self, symbols_list:List[Symbol]=None, chart_widget:ChartWidget=None, server_port=8000, verbose:bool=False, jupyter:bool=False):
        
        if (symbols_list is None):

            raise
        #

        if (chart_widget is None):

            ChartWidget(symbol=symbols_list[0])._generate_index_html()
        #
        else:

            chart_widget._generate_index_html()
        #


        self.server_port = server_port
        self.server_url  = f"http://localhost:{self.server_port}"

        self.verbose     = verbose
        self.jupyter     = jupyter


        package_dir  = Path(__file__).parent
        datafeed_dir = package_dir / "backend" / "datafeed"
        for item in os.listdir(datafeed_dir):

            item_path = os.path.join(datafeed_dir, item)
            os.remove(item_path)
        #

        self._register()

        for symbol in symbols_list:

            symbol._register()
        #
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

    def _register(self):

        package_dir  = Path(__file__).parent
        datafeed_dir = package_dir / "backend" / "datafeed"
        datafeed_dir.mkdir(parents=True, exist_ok=True)

        registry_path = datafeed_dir / "registry.json"
        registry      = {"server_port":self.server_port, "server_url":self.server_url}

        with open(registry_path, 'w', encoding='utf-8') as file:

            json.dump(registry, file, indent=4)
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
#
###################################################################################################
###################################################################################################
###################################################################################################
