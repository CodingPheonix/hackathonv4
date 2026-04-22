from fastmcp import FastMCP
from pydantic import BaseModel
import pandas as pd

mcp = FastMCP("farming-agent")

# Load once
weather_df = pd.read_csv("../Dataset/Modified_crop_recommendation.csv")
solutions_df = pd.read_csv("../Dataset/crop_solutions.csv")
disease_df = pd.read_csv("../Dataset/crop_diseases.csv")

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
def filter_temp(temp_filter: TempFilter):
    return get_column(temp_filter.crop, "temperature")


@mcp.tool()
def filter_soil_moisture(temp_filter: TempFilter):
    return get_column(temp_filter.crop, "soil_moisture")


@mcp.tool()
def filter_light_status(temp_filter: TempFilter):
    return get_column(temp_filter.crop, "uvi")


@mcp.tool()
def fetch_solutions(parameters: SolutionsFilter):
    result = solutions_df[
        (solutions_df["crop"].str.lower() == parameters.crop.lower()) &
        (solutions_df["parameter"].str.lower() == parameters.parameter.lower()) &
        (solutions_df["condition"].str.lower() == parameters.condition.lower())
        ]
    return result.to_dict(orient="records")


@mcp.tool()
def fetch_disease(parameter: DiseaseFilter):
    result = disease_df[
        (disease_df["crop"].str.lower() == parameter.crop.lower()) &
        (disease_df["symptoms"].str.contains(parameter.symptoms, case=False, na=False))
        ]
    return result.to_dict(orient="records")


if __name__ == "__main__":
    mcp.run(transport="http")