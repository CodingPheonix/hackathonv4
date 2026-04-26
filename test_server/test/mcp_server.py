import os
import pandas as pd
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("farming-agent")

# Load once
weather_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "Dataset", "Modified_crop_recomendations.csv"))
solutions_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "Dataset", "crop_solutions.csv"))
disease_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "Dataset", "crop_diseases.csv"))

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


@mcp.tool()
def filter_temp(crop: str):
    return get_column(crop, "temperature")


@mcp.tool()
def filter_soil_moisture(crop: str):
    return get_column(crop, "soil_moisture")


@mcp.tool()
def filter_light_status(crop: str):
    return get_column(crop, "uvi")


@mcp.tool()
def fetch_solutions(crop: str, parameter: str, condition: str):
    result = solutions_df[
        (solutions_df["crop"].str.lower() == crop.lower()) &
        (solutions_df["parameter"].str.lower() == parameter.lower()) &
        (solutions_df["condition"].str.lower() == condition.lower())
        ]
    return result.to_dict(orient="records")


@mcp.tool()
def fetch_disease(crop: str, symptoms: str):
    result = disease_df[
        (disease_df["crop"].str.lower() == crop.lower()) &
        (disease_df["symptoms"].str.contains(symptoms, case=False, na=False))
        ]
    return result.to_dict(orient="records")


if __name__ == "__main__":
    mcp.run(transport="stdio")