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
from .valid_shapes import OnePointShapes, MultiPointShapes
import pandas as pd

# ===============================  Chart Functions ===============================
# ================================================================================
class BrainyChart:

    def __init__(self, data:pd.DataFrame=None, port=8000, verbose:bool=False, jupyter:bool=True):

        package_dir = Path(__file__).parent.parent

        with open(f"{package_dir}/charting_library/tradingview.db", 'w') as file:

            pass
        #

        if (data is not None  and  list(data.columns)==['timestamp', 'open', 'high', 'low', 'close', 'volume']):

            data.to_csv(f"{package_dir}/datafeed.csv", index=False)
        #
        self._port    = port
        self._url     = f"http://localhost:{port}/index.html"
        self._verbose = verbose
        self._jupyter = jupyter
    #

    def _kill_servers(self):

        try:

            subprocess.run(["pkill", "-f", "uvicorn"]    , check=True)
            subprocess.run(["pkill", "-f", "http.server"], check=True)
        #
        except subprocess.CalledProcessError:

            pass
        #
    #

    def _run_backend(self):

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

    def _run_frontend(self):

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

        self._kill_servers()
        self._run_backend()
        self._run_frontend()
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
# ================================================================================
# ================================================================================




# ===============================  Shape Functions ===============================
# ================================================================================
class ShapeManager:

    def __init__(self, base_url:str="http://localhost:8001", default_chart_id:int=1):

        self.base_url         = base_url
        self.default_chart_id = default_chart_id
    #

    def _generate_random_code(
        self, 
        length:int=6
    ) -> int:

        return (random.randint(10**(length-1), (10**length)-1))
    #

    def create_or_update_shape(
        self,
        shape_type : OnePointShapes | MultiPointShapes,
        points     : List[Dict[str, float]],
        properties : Dict,
        shape_code : Optional[int] = None,
        shape_id   : Optional[str] = None
    ) -> Dict:
        
        chart_id   = self.default_chart_id
        shape_code = shape_code or self._generate_random_code()
        shape_id   = shape_id
        
        is_one_point = shape_type in [
            "emoji", "text", "icon", "anchored_text", "anchored_note", 
            "note", "sticker", "arrow_up", "arrow_down", "flag", 
            "vertical_line", "horizontal_line", "long_position", "short_position"
        ]
        
        if (is_one_point and len(points) != 1):

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

    def get_all_shapes(
        self
    ) -> List[Dict]:

        chart_id = self.default_chart_id
        url      = f"{self.base_url}/charts/{chart_id}/shapes/"
        response = requests.get(url)
        response.raise_for_status()
        return (response.json())
    #

    def get_shape(
        self,
        shape_code:int,
    ) -> Dict:

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

    def delete_shape(
        self, 
        shape_code:int, 
    ) -> Dict:
        
        chart_id = self.default_chart_id
        url      = f"{self.base_url}/charts/{chart_id}/shapes/{shape_code}"
        response = requests.delete(url)
        response.raise_for_status()

        return (response.json())
    #

    def delete_all_shapes(
        self
    ) -> Dict:

        chart_id = self.default_chart_id
        url      = f"{self.base_url}/charts/{chart_id}/shapes/"
        response = requests.delete(url)
        response.raise_for_status()

        return (response.json())
    #
#
# ================================================================================
# ================================================================================



