import os
import sys
import subprocess
import platform
import requests
import time
import random
import logging
from pathlib import Path
from IPython.display import IFrame
from IPython.display import clear_output
import pandas as pd

from typing import List, Dict, Optional, Literal

#
###################################################################################################
###################################################################################################
################################################################################################### Shape Manager
#
OnePointShapes = Literal[
    "emoji", "text", "icon", "anchored_text", "anchored_note", "note",
    "sticker", "arrow_up", "arrow_down", "flag", "vertical_line",
    "horizontal_line", "long_position", "short_position"
]

MultiPointShapes = Literal[
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
###################################################################################################
###################################################################################################
################################################################################################### Shape Manager
#
class BrainyShape:

    def __init__(self, base_url:str="http://localhost:8001", default_chart_id:int=1):

        self.base_url         = base_url
        self.default_chart_id = default_chart_id
    #

    def _generate_random_code(self, length:int=6) -> int:

        return (random.randint(10**(length-1), (10**length)-1))
    #

    def create_or_update_shape(self,
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
#