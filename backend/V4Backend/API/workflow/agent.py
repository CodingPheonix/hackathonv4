import os
import json
import re
from typing import Literal, List

from dotenv import load_dotenv
from langchain.messages import SystemMessage
from pydantic import BaseModel

from .state import MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    timeout=30
)

client = MultiServerMCPClient(
    {
        "weather": {
            "transport": "http",
            "url": "http://localhost:8000/mcp/temp/"
        }
    }
)

mcp_tools = client.get_tools()


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
    tools=[mcp_tools],
    system_prompt=DECIDE_EXTRACT_INFO_PROMPT,
    response_format=ExtractInfoResponse
)

# SUBAGENT TO ANALYSE TEMPERATURE
DECIDE_TEMP_PROMPT = (
    "You are a helpful assistant"
    "Use available MCP tools to fetch the suitable temperature range for Rice using get_range. "
    "Use get_range to get a range of suitable temperature for Rice. Column 'label' - value 'rice'"
    "Return a response: temp_status"
    "Use status codes: -2 for below limit, -1 for below ideal range, 0 for ideal range, 1 for above ideal range, 2 for over range"
)

class TempResponse(BaseModel):
    temp_status: int

temperature_agent = create_agent(
    model,
    tools=[mcp_tools],
    system_prompt=DECIDE_TEMP_PROMPT,
    response_format=TempResponse
)

# SUBAGENT TO ANALYSE SOIL MOISTURE
DECIDE_SOIL_MOISTURE_PROMPT = (
    "You are a helpful assistant. "
    "You will receive soil moisture readings for 5 days of a week. "
    "Use a fixed range of rice soil moisture requirements"
    "Compare the given soil moisture values with the retrieved range. "
    "Return a response: soil_status. "
    "Use status codes: "
    "-2 for critically dry (below minimum limit), "
    "-1 for below ideal range, "
    "0 for ideal range, "
    "1 for above ideal range, "
    "2 for over-saturated (above maximum limit)."
)

class SoilMoistureResponse(BaseModel):
    soil_status: int

soil_moisture_agent = create_agent(
    model,
    tools=[mcp_tools],
    system_prompt=DECIDE_SOIL_MOISTURE_PROMPT,
    response_format=SoilMoistureResponse
)

# SUBAGENT TO ANALYSE LIGHT STATUS
DECIDE_LIGHT_STATUS_PROMPT = (
    "You are a helpful assistant. "
    "Use available MCP tools to fetch the suitable light range for Rice using get_range. "
    "Column 'label' should have value 'rice'. "
    "Compare the given light values with the retrieved range. "
    "Return a response: light_status. "
    "Use status codes: "
    "-2 for insufficient light (far below minimum), "
    "-1 for below ideal range, "
    "0 for optimal light range, "
    "1 for above ideal range, "
    "2 for excessive light exposure."
)

class LightResponse:
    light_status: int

light_agent = create_agent(
    model,
    tools=[mcp_tools],
    system_prompt=DECIDE_LIGHT_STATUS_PROMPT,
    response_format=LightResponse
)

# AGENT TO COMPILE AVAILABLE DATA
COMPILER_PROMPT = (
    "You are an intelligent agent"
    "You will be given analysed data"
    "There are 3 sections: Temperature, Soil Moisture, Light Status"
    "You will compile and format the data in the available structured response"
    "USE ONLY THE FIELDS NECESSARY. If you do not have a particular data, do not use that field"
    "Criteria for magnitude analysis: -2 -> very lower than range, -1 -> slightly lower than range, 0 -> in range, 1 -> slightly above range, 2 -> very much above range"
    "Use mcp tools for getting recommendations for any type of abnormal situations"
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


class ExtractInfoResponse(BaseModel):
    plant: str
    growth_stage: str
    analysis_summary: AnalysisSummary
    recommendations: List[Recommendation]


compiler_agent = create_agent(
    model,
    system_prompt=COMPILER_PROMPT,
    response_format=LightResponse
)


def parse_message_content(msg):
    content = msg.content

    # convert list content to string
    if isinstance(content, list):
        content = "".join(str(x) for x in content)

    # remove ```json ``` wrappers if present
    content = re.sub(r"```json|```", "", content).strip()

    return json.loads(content)

def compiler(state: MessagesState):

    """
    Compile the decisions from previous steps and provide a final recommendation for the farmer.
    """

    file_path = os.path.join(os.path.dirname(__file__), '../utils/obj.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

        temp_data = parse_message_content(state["messages"][-3])
        soil_data = parse_message_content(state["messages"][-2])
        uvi_data  = parse_message_content(state["messages"][-1])

        temp_status = temp_data["temp_status"]
        soil_status = soil_data["soil_moisture_status"]
        uvi_status = uvi_data["uvi_status"]

    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(
                        content=f"""
                        You are an agricultural assistant that converts sensor analysis into practical farming recommendations.

                        Input status codes:
                        -2 = Under use
                        -1 = Below Ideal Range
                        0 = Ideal Range
                        1 = Above Ideal Range
                        2 = Overuse

                        Current sensor evaluation:
                        {{
                            "temperature_status": {temp_status},
                            "soil_moisture_status": {soil_status},
                            "uvi_status": {uvi_status}
                        }}

                        Step 1:
                        Convert the numeric status codes into their meaning.

                        Step 2:
                        If a parameter is NOT in the ideal range (0), generate a recommendation to correct it.

                        Step 3:
                        If a parameter is already ideal (0), do not create an action for it.

                        Return ONLY valid JSON.

                        Use EXACTLY this structure:

                        {{
                        "plant": "<Plant Name>",
                        "growth_stage": "Vegetative",
                        "analysis_summary": {{
                            "temperature_status": "<converted meaning>",
                            "soil_moisture_status": "<converted meaning>",
                            "uvi_status": "<converted meaning>"
                        }},
                        "recommendations": [
                            {{
                            "action": "<type of action>",
                            "parameter": "<sensor parameter>",
                            "problem": "<short description>",
                            "solution": "<clear instruction>",
                            "priority": "High | Medium | Low"
                            }}
                        ]
                        }}

                        Rules:
                        - Convert numeric codes to text meanings.
                        - Do NOT copy the input numbers.
                        - Do NOT invent sensor readings.
                        - Only recommend actions for non-ideal parameters.
                        - Return ONLY JSON.
                        - Create for all and only for the parameters that are not ideal.
                        """
                        )
                ]
            )
        ]
    }