import os
import json
import re
from dotenv import load_dotenv
from langchain.messages import SystemMessage
from .state import MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()

# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     temperature=0,
#     timeout=30
# )

model = ChatOllama(model="gemma3:1b")


def extract_info(state: MessagesState):
    """
    Extract relevant information from the input data and prepare it for decision making.
    """

    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(
                        content = f"""
                            You are a helpful assistant that extracts relevant information from raw data to prepare it for decision making.

                            Extract the relevant information from the raw data and return it in JSON format like:
                            {{
                                "temperature_record": [...],
                                "soil_moisture": 0.24,
                                "uvi_values": [...]
                            }}

                            Return ONLY JSON. Just the JSON
                            Do not add explanations.
                            """
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

def decide_temp(state: MessagesState):

    """
    Given a temperature record for 5 days and the required temperature, decide the best temperature.
    """

    extract_message = state["messages"][-1].content
    print(f"Extracted message for temperature decision: {extract_message}")

    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(
                        content = f"""
                        You are a helpful assistant that helps to decide the right action to be performed to achieve the required temperature for the next day based on the past 5 days' temperatures and the required temperature.

                        The past 5 days' temperatures are {extract_message}

                        Return your decision in JSON format like:
                        {{"status": <value>}}

                        Where:
                        -2 = far below ideal (cold stress) - Range [0–15°C]
                        -1 = slightly below ideal - Range [16–20°C]
                        0 = within ideal range - Range [21–25°C]
                        1 = slightly above ideal - Range [26–30°C]
                        2 = far above ideal (heat stress) - Range [31°C+]

                        Return ONLY JSON. Generate just the JSON response.
                        Do not add explanations.

                        Examples:

                        Example 1:
                        temperatures = [10.8, 11.5, 12.0, 10.9, 11.7]
                        required_temp = 22.0
                        {{"temp_status": -2}}

                        Example 2:
                        temperatures = [16.5, 17.2, 16.8, 17.5, 16.9]
                        required_temp = 22.0
                        {{"temp_status": -1}}

                        Example 3:
                        temperatures = [21.8, 22.4, 22.1, 21.9, 22.3]
                        required_temp = 22.0
                        {{"temp_status": 0}}

                        Example 4:
                        temperatures = [27.5, 28.1, 27.8, 28.4, 27.9]
                        required_temp = 22.0
                        {{"temp_status": 1}}

                        Example 5:
                        temperatures = [34.2, 35.1, 34.8, 35.5, 34.6]
                        required_temp = 22.0
                        {{"temp_status": 2}}
                        """
                    )
                ]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

def decide_soil_moisture(state: MessagesState):

    """
    Decide soil moisture status based on the current soil moisture
    and the ideal range required for crops.
    """

    extract_message = state["messages"][-2].content

    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(
                        content = f"""
                            You are a helpful assistant that decides soil moisture status for crops.

                            The current soil moisture is {extract_message}.

                            Return your decision in JSON format like:
                            {{"soil_moisture_status": <value>}}

                            Where:
                            -2 = far below ideal (very dry soil) - Range [0.00–0.10]
                            -1 = slightly below ideal - Range [0.11–0.17]
                            0 = within ideal range - Range [0.18–0.30]
                            1 = slightly above ideal - Range [0.31–0.38]
                            2 = far above ideal (waterlogged soil) - Range [0.39+]

                            Return ONLY JSON.
                            Do not add explanations.

                            Examples:

                            Example 1:
                            soil_moisture = 0.07
                            ideal_range = [0.18, 0.30]
                            {{"soil_moisture_status": -2}}

                            Example 2:
                            soil_moisture = 0.15
                            ideal_range = [0.18, 0.30]
                            {{"soil_moisture_status": -1}}

                            Example 3:
                            soil_moisture = 0.24
                            ideal_range = [0.18, 0.30]
                            {{"soil_moisture_status": 0}}

                            Example 4:
                            soil_moisture = 0.33
                            ideal_range = [0.18, 0.30]
                            {{"soil_moisture_status": 1}}

                            Example 5:
                            soil_moisture = 0.42
                            ideal_range = [0.18, 0.30]
                            {{"soil_moisture_status": 2}}
                            """
                    )
                ]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }


def decide_light_status(state: MessagesState):

    """
    Decide light condition based on the current light level
    and the ideal light range required for crops.
    """

    extract_message = state["messages"][-3].content

    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(
                        content = f"""
                            You are a helpful assistant that decides light conditions for crops.

                            The current light intensity is {extract_message}.

                            Return your decision in JSON format like:
                            {{"uvi_status": <value>}}

                            Where:
                            -2 = far below ideal (very low light) - Range [0-2]
                            -1 = slightly below ideal - Range [3-5]
                            0 = within ideal range - Range [6-7]
                            1 = slightly above ideal- Range [8-10]
                            2 = far above ideal (excessive sunlight)- Range [11+]

                            Return ONLY JSON.
                            Do not add explanations.

                            Examples:

                            Example 1:
                            uvi_values = [1.2, 1.5, 1.8]
                            {{"uvi_status": -2}}

                            Example 2:
                            uvi_values = [3.4, 4.1, 4.6]
                            {{"uvi_status": -1}}

                            Example 3:
                            uvi_values = [6.2, 6.8, 7.0]
                            {{"uvi_status": 0}}

                            Example 4:
                            uvi_values = [8.4, 9.1, 9.6]
                            {{"uvi_status": 1}}

                            Example 5:
                            uvi_values = [11.3, 11.8, 12.5]
                            {{"uvi_status": 2}}
                            """
                    )
                ]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

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