import json
import os
from typing import Any

import requests

from V4Backend.API.models import Polygon

AGROMONITORING_KEY = os.getenv("AGROMONITORING_KEY")

def create_bounding_box(lon, lat, offset=0.01):
    """
    Creates a square polygon around a center point.

    offset ≈ ~1km if ~0.01 (roughly, varies by latitude)
    """

    return [
        [lon - offset, lat - offset],  # bottom-left
        [lon + offset, lat - offset],  # bottom-right
        [lon + offset, lat + offset],  # top-right
        [lon - offset, lat + offset],  # top-left
        [lon - offset, lat - offset]   # close polygon
    ]

def createPolygon(latitude: float,longitude: float) -> str | None:

    url = f"http://api.agromonitoring.com/agro/1.0/polygons?appid={AGROMONITORING_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name":"Polygon Sample",
               "geo_json":{
                   "type": "Feature",
                   "properties":{      },
                   "geometry":{
                       "type":"Polygon",
                       "coordinates":[
                           create_bounding_box(longitude,latitude)
                       ]
                   }
               }
    }

    response = requests.post(url, headers=headers, json=json.dumps(payload))
    data = response.json()

    if response.status_code == 201:

        # SAVE ID IN DB
        Polygon.objects.create(
        latitude=latitude,
        longitude=longitude,
        polygon_id=data["id"]
        )

        return data["id"]
    return None

def isPolygonExists(latitude: float, longitude: float) -> bool:
    try:
        polygon = Polygon.objects.get(latitude=latitude, longitude=longitude)
        return True
    except Polygon.DoesNotExist:
        return False

def getPolygonId(latitude: float, longitude: float) -> str | None:
    try:
        polygon = Polygon.objects.get(latitude=latitude, longitude=longitude)
        return polygon.polygon_id
    except Polygon.DoesNotExist:
        return None


def extract_temperatures(weather_json):
    temps = []

    for item in weather_json.get("list", []):
        temp = item.get("main", {}).get("temp")
        if temp is not None:
            temps.append(temp)

    return temps

def kelvin_to_celsius(k):
    return k - 273.15