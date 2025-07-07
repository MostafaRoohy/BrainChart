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
#
###################################################################################################
###################################################################################################
################################################################################################### BrainyChart
#
class BrainyChart:

    def __init__(self, data:pd.DataFrame=None, port=8000, verbose:bool=False, jupyter:bool=True):

        package_dir = Path(__file__).parent

        if (data is not None  and  list(data.columns)==['timestamp', 'open', 'high', 'low', 'close', 'volume']):

            data.to_csv(f"{package_dir}/backend/datafeed.csv", index=False)
        #

        with open(f"{package_dir}/backend/tradingview.db", 'w') as file:

            pass
        #
        
        self._port    = port
        self._url     = f"http://localhost:{port}/index.html"
        self._verbose = verbose
        self._jupyter = jupyter
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

            package_dir = Path(__file__).parent
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
                    cwd=str(package_dir),
                    shell=shell,
                )
            #
            else:

                with open(os.devnull, 'w') as fnull:
                    subprocess.Popen(
                        cmd,
                        cwd=str(package_dir),
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