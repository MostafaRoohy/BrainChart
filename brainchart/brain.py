#
# The main user-facing classe, BrainChart, which is used to start the application.
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

from pathlib import Path
import time
import random

from typing import List
from IPython.display import IFrame
from IPython.display import clear_output

import json


from .symbol import Symbol
from .widget import ChartWidget
#
###################################################################################################
###################################################################################################
################################################################################################### BrainChart
#
class BrainChart:

    def __init__(self, symbols_list:List[Symbol]=None, chart_widget:ChartWidget=None, server_port=8000):
        
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


        self._register()

        for symbol in symbols_list:

            symbol._register()
        #
    #

    def _register(self):

        root_dir  = Path(__file__).parent.parent
        datafeed_dir = root_dir / "runtime" / "datafeed"
        datafeed_dir.mkdir(parents=True, exist_ok=True)
        for item in os.listdir(datafeed_dir):

            item_path = os.path.join(datafeed_dir, item)
            os.remove(item_path)
        #


        root_dir     = Path(__file__).parent.parent
        datafeed_dir = root_dir / "runtime" / "datafeed"
        datafeed_dir.mkdir(parents=True, exist_ok=True)

        registry_path = datafeed_dir / "registry.json"
        registry      = {"server_port":self.server_port, "server_url":self.server_url}

        with open(registry_path, 'w', encoding='utf-8') as file:

            json.dump(registry, file, indent=4)
        #
    #    
    ##############################################################
    #
    def kill_servers(self):

        try:

            if (platform.system().lower().startswith("win")):

                subprocess.run(["taskkill", "/F", "/IM", "uvicorn.exe", "/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            #
            else:

                subprocess.run(["pkill", "-f", "uvicorn"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            #
        #
        except Exception:

            pass
        #
    #

    def run_servers(self, verbose:bool):

        try:

            print(f"Starting server on port {self.server_port}...")

            package_dir = Path(__file__).parent
            root_dir    = package_dir.parent

            module_path = "brainchart.fast_api:app"

            cmd = ["uvicorn", module_path, "--host", "0.0.0.0", "--port", str(self.server_port)]

            # Ensure the project root is on PYTHONPATH so 'brainchart.*' imports work
            env = os.environ.copy()
            env["PYTHONPATH"] = str(root_dir) + (os.pathsep + env.get("PYTHONPATH",""))
            
            if (verbose):
                            
                return (subprocess.Popen(cmd, cwd=str(root_dir), env=env))
            #
            else:

                with open(os.devnull, 'w') as fnull:

                    return (subprocess.Popen(cmd, cwd=str(root_dir), env=env, stdout=fnull, stderr=fnull))
                #
            #
        #
        except Exception as e:

            print(f"Error running server: {e}")
        #
    #

    def imagine(self, width=1200, height=600, verbose:bool=False, jupyter:bool=False):

        self.kill_servers()
        self.run_servers(verbose=verbose)

        print("Please wait...")
        time.sleep(4)


        if (not verbose  or  jupyter):

            clear_output()
        #


        if (jupyter):

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
