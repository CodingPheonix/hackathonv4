import json

from langchain_core.globals import set_verbose, set_debug
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from typing import List
from typing import Literal
from dotenv import load_dotenv
from .tools import *
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent

set_verbose(True)
set_debug(True)

load_dotenv()

os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
# model = ChatOpenRouter(model="meta-llama/llama-3.1-8b-instruct")
model = ChatOpenRouter(model="google/gemma-4-31b-it:free", temperature=0.9)
# model = ChatOllama(
#     model="llama3.1",
#     temperature=0,
# )

# ----------------------------------------------------------------------
# SUBAGENT TO EXTRACT INFORMATION
# ----------------------------------------------------------------------


DECIDE_EXTRACT_INFO_PROMPT = (
    "You are a helpful assistant. "
    "You will be given a user input. "
    "Extract the following information: {{ latitude, longitude, crop }}. "
    "Return the json for further action. "
)

class ExtractInfoResponse(BaseModel):
    latitude: float
    longitude: float
    crop: str

data_extraction_agent = create_agent(
    model,
    system_prompt=DECIDE_EXTRACT_INFO_PROMPT,
    response_format=ExtractInfoResponse
)

# SUB AGENT FOR SUPERVISOR
@tool
def extract_data(request: str) -> str:
    """Extract information from user context.

    Input: Natural language Weather (e.g., 'user latitude: 20.34643, longitude: 59.304442')
    """
    result = data_extraction_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    # if "structured_response" in result:
    #     return json.dumps(result["structured_response"].model_dump())

    # fallback to raw text
    return result["messages"][-1].text


# ----------------------------------------------------------------------------
# AGENT TO GATHER ALL WEATHER DATA
# ----------------------------------------------------------------------------


FETCH_WEATHER_INFO_PROMPT = (
    "You are an intelligent agent. "
    "Step 1: Call get_temperatures. "
    "Step 2: Call get_soil_moisture. "
    "Step 3: Call get_light_index. "
    "Step 4: You MUST call get_weather_ranges using the fetched values. "
    "Do NOT compute status yourself. "
    "Return ONLY the output of get_weather_ranges."
)

class WeatherInfoResponse(BaseModel):
    temp_status: int
    soil_status: int
    light_status: int

weatherInfoAgent = create_agent(
    model,
    tools=[get_temperatures, get_soil_moisture, get_light_index, get_weather_ranges],
    system_prompt=FETCH_WEATHER_INFO_PROMPT,
    response_format=WeatherInfoResponse
)

# SUB AGENT FOR SUPERVISOR
@tool
def fetch_weather_data(request: str) -> str:
    """
    Used to gather temperature, light index and soil moisture data
    using given latitude and longitude.

    Input:
        Natural language Weather
        (e.g., 'user latitude: 20.34643, longitude: 59.304442')

    :returns:
        JSON string containing calculated statuses
    """
    result = weatherInfoAgent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    # if "structured_response" in result:
    #     return json.dumps(result["structured_response"].model_dump())

    # fallback to raw text
    return result["messages"][-1].text


# ------------------------------------------------------------------------------------
# AGENT TO COMPILE AVAILABLE DATA
# ------------------------------------------------------------------------------------


COMPILER_PROMPT = (
    "You are an intelligent agent. "
    "Your action will contain 4 steps. "
    "you will receive statuses of Weather (temperature, soil moisture, light index) data from other agents. "
    "Use tool fetch_solutions to get recommended suggestions for each criteria. "
    "Compare statuses of each section with tool data, use relevant suggestions. "
    "Finalise them into the analysis summary and recommendations. "
    "USE ONLY THE FIELDS NECESSARY. If you do not have a particular data, do not use that field. "
)

class AnalysisSummary(BaseModel):
    temperature_status: str
    soil_moisture_status: str
    uvi_status: str


class Recommendation(BaseModel):
    action: str
    parameter: str
    problem: str
    solution: str
    priority: Literal["High", "Medium", "Low"]


class ExtractCompilerInfoResponse(BaseModel):
    plant: str | None = None
    growth_stage: str | None = None
    analysis_summary: AnalysisSummary | None = None
    recommendations: List[Recommendation] | None = None


compiler_agent = create_agent(
    model,
    tools=[fetch_solutions],
    system_prompt=COMPILER_PROMPT,
    response_format=ExtractCompilerInfoResponse
)

@tool
def compile_weather_status_data(request: str) -> str:
    """Extract weather information from previous agents outputs.

    Use this to analyze and compile a report to provide analysis and recommendations.
    """
    result = compiler_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    # if "structured_response" in result:
    #     return json.dumps(result["structured_response"].model_dump())

    # fallback to raw text
    return result["messages"][-1].text

# ------------------------------------------------------------------------------------
# FORMATTER AGENT
# ------------------------------------------------------------------------------------

FORMATTER_PROMPT = (
    "You will be given a structured data of temperature, light and soil moisture status. "
    "You will have to format it in Human readable format. "
    "Provide the solution in simpler text, easy language and bullet points if possible. "
    "Do not keep references to any other document, make sure to give the complete response. "
    "Here is an example below, DO take reference, DO NOT take context. "
    "Example: You are trying to grow rice.\nYou have the temperature kept optimal, the soil is lacking some moisture though, you could increase irrigation frequency or consider drip watering to maintain consistent moisture levels.\nThe light conditions are slightly below optimal, you could reposition the crop to receive more direct sunlight or reduce shading from nearby obstacles. "
)

class FormatterResponse(BaseModel):
    formatter_response: str

formatter_agent = create_agent(
    model,
    system_prompt=FORMATTER_PROMPT,
    response_format=FormatterResponse
)

@tool
def format_data(request: str) -> str:
    """Use the structured Output from compile_weather_status_data.

    Format this into human-readable format.

    """
    result = formatter_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    # if "structured_response" in result:
    #     return json.dumps(result["structured_response"].model_dump())

    # fallback to raw text
    return result["messages"][-1].text

# ------------------------------------------------------------------------------------
# SUPERVISOR AGENT FOR WEATHER DETAILS MANAGEMENT
# ------------------------------------------------------------------------------------


# WEATHER_SUPERVISOR_PROMPT = (
#     "You are an intelligent agent. "
#     "You are given task to evaluate and produce a report based on weather conditions affecting plant. "
#     "Use extract_data to get latitude and longitude from prompt. "
#     "Use fetch_weather_data to get real-time temperature, soil moisture and light status. "
#     "Use compile_weather_status_data to compile and create analysis report. "
#     "Read the final compiled analysis and generate it's readable text format in bullet points. "
#     "Provide ONLY the Suggestions and report as a single string. "
#     "Do not provide all agentic message to output. "
# )

# WEATHER_SUPERVISOR_PROMPT = (
#     "You are an intelligent agent.\n"
#     "You are given a crop name and coordinates. You are supposed to get real-world data, compare them and generate an analysis. "
#
#     "You MUST follow these steps strictly:\n"
#
#     "1. ALWAYS call extract_data first.\n"
#     "2. THEN call fetch_weather_data using extracted data.\n"
#     "3. THEN call compile_weather_status_data.\n"
#     "4. THEN format the response using format_data. \n"
#     "4. DO NOT skip any step.\n"
#     "5. DO NOT generate final output without calling all tools.\n"
#
#     # "Return ONLY the final formatted string."
# )
WEATHER_SUPERVISOR_PROMPT = """
    You are an intelligent agent.

Follow these steps in order using tools:
1. Call extract_data with the user input (needs entire use prompt)
2. Use the result to call fetch_weather_data (needs latitude and longitude)
3. Then call compile_weather_status_data (needs entire output of step 2 and crop name: rice)
4. Then call format_data (needs entire output of step 3)

Always proceed step by step until the final answer is ready.

Ones you get the formatted response, return it.
"""


class WeatherReportResponse(BaseModel):
    weather_report: str

weather_supervisor_agent = create_agent(
    model,
    tools=[
        extract_data,
        fetch_weather_data,
        compile_weather_status_data,
        format_data
    ],
    system_prompt=WEATHER_SUPERVISOR_PROMPT,
    # response_format=WeatherReportResponse,
)
