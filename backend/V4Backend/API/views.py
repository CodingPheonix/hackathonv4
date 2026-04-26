import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from V4Backend.API.workflow.agent import weather_supervisor_agent


from API.workflow.agent import weather_supervisor_agent
# from API.workflow.tools import get_soil_moisture
# from API.workflow.tools import get_light_index
# from API.workflow.tools import get_weather_ranges
# from API.workflow.agent import extract_data
# from API.workflow.agent import fetch_weather_data
# from API.workflow.agent import compile_weather_status_data


# Create your views here.
def hello(request):
    return JsonResponse({
        "message": "Hello, World!"
    })

# def test_get_soil_moisture(request):
#     result = get_soil_moisture(22.5976, 88.378)
#     return JsonResponse(result, safe=False)

# def get_light(request):
#     result = get_light_index(22.5976, 88.378)
#     return JsonResponse(result, safe=False)

# def get_weather_r(request):
#     result = get_weather_ranges("rice", [33.10000000000002, 30.83000000000004, 27.710000000000036, 27.100000000000023, 26.30000000000001, 26.28000000000003, 32.04000000000002, 33.89000000000004, 32.08000000000004, 28.710000000000036, 27.720000000000027, 27.090000000000032, 26.590000000000032, 26.670000000000016, 31.03000000000003, 32.31, 31.860000000000014, 28.890000000000043, 27.640000000000043, 27.060000000000002, 26.930000000000007, 26.79000000000002, 30.350000000000023, 31.99000000000001, 31.840000000000032, 28.370000000000005, 27.58000000000004, 27.30000000000001, 26.879999999999995, 26.910000000000025, 30.29000000000002, 32.07000000000005, 31.180000000000007, 22.28000000000003, 25.57000000000005, 27.430000000000007, 27.370000000000005, 26.939999999999998, 29.590000000000032, 31.29000000000002], 3.14, 23.45)
#     return JsonResponse(result, safe=False)

# def extract_from_prompt(request):
#     result = extract_data("Hi, I want to grow rice. Here are my coordinates. latitude: 22.5286, longitude: 88.3267")
#     return JsonResponse(result, safe=False)

# def fetch_weather(request):
#     result = fetch_weather_data(json.dumps({
#         "latitude": 22.5286,
#         "longitude": 88.3267,
#         "crop": "rice"
#     }))
#     return JsonResponse(result, safe=False)

# def compile_weather_status(request):
#     result = compile_weather_status_data("The final answer is {\"temp_status\": 2, \"soil_status\": -2, \"light_status\": 2}.")
#     return JsonResponse(result, safe=False)

@csrf_exempt
def agent(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
        query = body.get("query")

        print(f"Received query: {query}")

        agent_result = weather_supervisor_agent.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )

        # CASE 1: structured output
        if "structured_response" in agent_result:
            return JsonResponse(agent_result["structured_response"].model_dump())

        # CASE 2: fallback to message content
        elif "messages" in agent_result:
            return JsonResponse({
                "response": agent_result["messages"][-1].content
            })

        # CASE 3: fallback
        return JsonResponse({
            "response": str(agent_result)
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=400)