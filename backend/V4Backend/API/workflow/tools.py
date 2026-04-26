import os
from dotenv import load_dotenv
from typing import List

import pandas as pd
import requests
from pydantic import BaseModel
from langchain.tools import tool

load_dotenv()

from .utils import createPolygon, isPolygonExists, getPolygonId, extract_temperatures, \
    kelvin_to_celsius

AGROMONITORING_KEY = os.getenv("AGROMONITORING_KEY")
OPENWEATHERAPI_KEY = os.getenv("OPENWEATHERAPI_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
weather_df = pd.read_csv(os.path.abspath(os.path.join(BASE_DIR, "..", "Dataset", "Modified_crop_recomendations.csv")))
solutions_df = pd.read_csv(os.path.abspath(os.path.join(BASE_DIR, "..", "Dataset", "crop_solutions.csv")))
disease_df = pd.read_csv(os.path.abspath(os.path.join(BASE_DIR, "..", "Dataset", "crop_diseases.csv")))

class weatherData(BaseModel):
    crop: str
    temperature: List[float]
    soil_moisture: float
    light: float

class TempFilter(BaseModel):
    crop: str


class SolutionsFilter(BaseModel):
    crop: str
    parameter: str
    condition: str


class DiseaseFilter(BaseModel):
    crop: str
    symptoms: str


def get_column(crop: str, column: str):
    return weather_df[
        weather_df["label"].str.lower() == crop.lower()
        ][column].tolist()

def filter_temp(crop: str):
    """Fetches appropriate temperature range for a given crop"""
    return get_column(crop, "temperature")

def filter_soil_moisture(crop: str):
    """Fetches appropriate soil moisture range for a given crop"""
    return get_column(crop, "soil_moisture")

def filter_light_status(crop: str):
    """Fetches appropriate light status range for a given crop"""
    return get_column(crop, "uvi")

def get_min_max(values):
    if not values:
        return None
    return [min(values), max(values)]

def calculate_status(value, min_val, max_val):
    range_width = max_val - min_val
    margin = 0.2 * range_width  # threshold for "far"

    if value < min_val:
        return -2 if value < (min_val - margin) else -1
    elif value > max_val:
        return 2 if value > (max_val + margin) else 1
    return 0


def avg(values):
    return sum(values) / len(values)

@tool
def get_weather_ranges(
        crop: str,
        temperature: List[float],
        soil_moisture: float,
        light: float
):
    """use this to calculate status values of temperature, soil moisture and light status"""

    # get ranges from your tools
    temp_min, temp_max = get_min_max(filter_temp(crop))
    soil_min, soil_max = get_min_max(filter_soil_moisture(crop))
    light_min, light_max = get_min_max(filter_light_status(crop))

    # compute actual values
    temp_val = avg(temperature)
    soil_val = soil_moisture
    light_val = light

    # calculate statuses
    temp_status = calculate_status(temp_val, temp_min, temp_max)
    soil_status = calculate_status(soil_val, soil_min, soil_max)
    light_status = calculate_status(light_val, light_min, light_max)

    return {
        "temp_status": temp_status,
        "soil_status": soil_status,
        "light_status": light_status
    }

@tool
def get_temperatures(latitude: float, longitude: float):
    """Used to get a list of temperatures. Input parameters: latitude: float, longitude: float"""

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={OPENWEATHERAPI_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return [kelvin_to_celsius(t) for t in extract_temperatures(data)]
    return None

@tool
def get_soil_moisture(latitude: float, longitude: float):
    """Used to get the soil moisture value. Input parameters: latitude: float, longitude: float"""

    if not isPolygonExists(latitude, longitude):
        print("enter 1")
        polyId = createPolygon(latitude,longitude)
    else:
        print("enter 2")
        polyId = getPolygonId(latitude, longitude)
    print(polyId, latitude, longitude)

    url = f"http://api.agromonitoring.com/agro/1.0/soil?polyid={polyId}&appid={AGROMONITORING_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["moisture"]
    return None

@tool()
def get_light_index(latitude: float, longitude: float):
    """Used to get the light index. Input parameters: latitude: float, longitude: float"""

    if not isPolygonExists(latitude, longitude):
        polyId = createPolygon(latitude,longitude)
    else:
        polyId = getPolygonId(latitude, longitude)

    url = f"http://api.agromonitoring.com/agro/1.0/uvi?polyid={polyId}&appid={AGROMONITORING_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return data["uvi"]
    return None

@tool
def fetch_solutions(
        crop: str,
        parameter: str,
        condition: str
):
    """Fetches appropriate solutions for a given imbalanced criteria (temperature, soil, light) for a given crop"""
    result = solutions_df[
        (solutions_df["crop"].str.lower() == crop.lower()) &
        (solutions_df["parameter"].str.lower() == parameter.lower()) &
        (solutions_df["status"].astype(str).str.lower() == condition.lower())
        ]
    return result.to_dict(orient="records")


@tool
def fetch_disease(parameter: DiseaseFilter):
    """Fetches appropriate disease information for a particular disease from the crop name and symptoms"""
    result = disease_df[
        (disease_df["crop"].str.lower() == parameter.crop.lower()) &
        (disease_df["symptoms"].str.contains(parameter.symptoms, case=False, na=False))
        ]
    return result.to_dict(orient="records")
