import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .workflow.graph import query_agent

# Create your views here.
def hello(request):
    return JsonResponse({
        "message": "Hello, World!"
    })

@csrf_exempt
def agent(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
        query = body.get("query")

        print(f"Received query: {query}")

        agent_result = query_agent(query)

        return JsonResponse(agent_result, safe=False)

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=400)