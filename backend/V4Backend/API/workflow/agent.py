import os
import json
import re
from typing import Literal, List

from dotenv import load_dotenv
from langchain.messages import SystemMessage
from pydantic import BaseModel

from .state import MessagesState
from .tools import *
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent

load_dotenv()

# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     temperature=0,
#     timeout=30
# )


os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
model = ChatOpenRouter(model="openai/gpt-oss-20b:free")

# SUBAGENT TO EXTRACT INFORMATION
DECIDE_EXTRACT_INFO_PROMPT = (
    "You are a helpful assistant"
    "You will be given a user input"
    "Extract the following information: {{ temperature_record, soil_moisture, uvi_values }} "
    "Return the json for further action"
)

class ExtractInfoResponse(BaseModel):
    temperature_record: list[int]
    soil_moisture: int
    uvi_values: list[int]

data_extraction_agent = create_agent(
    model,
    system_prompt=DECIDE_EXTRACT_INFO_PROMPT,
    response_format=ExtractInfoResponse
)

# SUB AGENT FOR SUPERVISOR
@tool
def extract_data(request: str) -> str:
    """Extract weather information from user context.

    Use this to analyze status of temperature, soil_moisture and light status

    Input: Natural language Weather (e.g., 'Temperature records: [22.3, 21.8, 23.5, 24.3, 22.1]; soil moisture: 0.175; light status: [10.1, 10.19, 10.2]')
    """
    result = data_extraction_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text

# AGENT TO COMPILE AVAILABLE DATA
COMPILER_PROMPT = (
    "You are an intelligent agent"
    "Your action will contain 3 steps"
    "Firstly get the status codes of data"
    "You will match statuses, compile and format the data in the available structured response"
    "Use tool fetch_solutions to get recommended suggestions for each criteria "
    "USE ONLY THE FIELDS NECESSARY. If you do not have a particular data, do not use that field"
    "Criteria for magnitude analysis: -2 -> very lower than range, -1 -> slightly lower than range, 0 -> in range, 1 -> slightly above range, 2 -> very much above range"
    "Finalise them into the analysis summary and recommendations "
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
    plant: str
    growth_stage: str
    analysis_summary: AnalysisSummary
    recommendations: List[Recommendation]


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

    Input: temp_status: 1, soil_status: 0, light_status: -1
    """
    result = compiler_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text

WEATHER_SUPERVISOR_PROMPT = (
    "You are an intelligent agent. "
    "You are given task to evaluate and produce a report based on weather conditions affecting plant"
    "Use analyse_temperature_data to get temperature status; request -> Find temp status. temperature list: [....]"
    "Use analyse_light_status_data to get temperature status; request -> Find temp status. light status list: [....]"
    "Use analyse_soil_moisture_data to get temperature status; request -> Find temp status. soil moisture list: [....]"
    "Use compile_weather_status_data to compile and create report; request -> {send analysed statuses of temp, light and soil}"
    "Read the final compiled analysis and generate it's readable text format in bullet points"
    "Provide the output as a single string"
)

class WeatherSupervisorResponse(BaseModel):
    weather_report: str

weather_supervisor_agent = create_agent(
    model,
    tools=[
        compile_weather_status_data
    ],
    system_prompt=WEATHER_SUPERVISOR_PROMPT,
    response_format=WeatherSupervisorResponse
)