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

from .valid_shapes import OnePointShapes, MultiPointShapes



# ===============================  Chart Functions ===============================
# ================================================================================
class BrainyChart:

    def __init__(self, url="http://localhost:8000/index.html", width="600", height="300"):

        self.width  = width
        self.height = height
        self.url    = url
    #
        
    def imagine(self):

        return IFrame(src=self.url, width=self.width, height=self.height)
    #
#
# ================================================================================
# ================================================================================




# ===============================  Shape Functions ===============================
# ================================================================================
class ShapeManager:

    def __init__(self, base_url: str = "http://localhost:8001", default_chart_id: int = 1):

        self.base_url = base_url
        self.default_chart_id = default_chart_id
        # self._check_servers_alive()
    #
    # ======================
    # def _check_servers_alive(self):
    #     response = requests.get(self.base_url)
    #     response.raise_for_status()

    # ======================
    def _generate_random_code(
        self, 
        length:int=6
    ) -> int:

        return (random.randint(10**(length-1), (10**length)-1))
    #

    # ======================
    def create_or_update_shape(
        self,
        shape_type: OnePointShapes | MultiPointShapes,
        points: List[Dict[str, float]],
        properties: Dict,
        shape_code: Optional[int] = None,
        shape_id: Optional[str] = None
    ) -> Dict:
        
        chart_id = self.default_chart_id
        shape_code = shape_code or self._generate_random_code()
        shape_id = shape_id
        
        is_one_point = shape_type in [
            "emoji", "text", "icon", "anchored_text", "anchored_note", 
            "note", "sticker", "arrow_up", "arrow_down", "flag", 
            "vertical_line", "horizontal_line", "long_position", "short_position"
        ]
        
        if is_one_point and len(points) != 1:
            raise ValueError(f"Shape type {shape_type} requires 1 point")
        elif not is_one_point and len(points) < 2:
            raise ValueError(f"Shape type {shape_type} requires at least 2 points")
        
        payload = {
            "shape_id": shape_id,
            "shape_type": shape_type,
            "shape_code": shape_code,
            "shape_data": {
                "points": points,
                "properties": properties
            }
        }
        
        url = f"{self.base_url}/charts/{chart_id}/shapes/"
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return {
            **response.json(),
            "is_one_point": is_one_point,
            "shape_type": shape_type,
            "shape_code": shape_code
        }
    #

    # ======================
    def get_all_shapes(
        self
    ) -> List[Dict]:

        chart_id = self.default_chart_id
        url = f"{self.base_url}/charts/{chart_id}/shapes/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    #

    # ======================
    def get_shape(
        self,
        shape_code:int,
    ) -> Dict:

        chart_id = self.default_chart_id
        url = f"{self.base_url}/charts/{chart_id}/shapes/{shape_code}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Shape with code {shape_code} not found") from e
            raise
    #

    # ======================
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

    # ======================
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



