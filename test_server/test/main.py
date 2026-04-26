import os
import asyncio

from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model

os.environ["OPENROUTER_API_KEY"] = "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"

async def main():
    client = MultiServerMCPClient(
        {
            "farming-agent": {
                "transport": "stdio",
                "command": "python",
                "args": ["./mcp_server.py"],
            },
        }
    )

    tools = await client.get_tools()
    model = init_chat_model(
        "google/gemma-4-31b-it:free",
        tools=tools,
        model_provider="openrouter",
    )
    math_response = await model.ainvoke([
        HumanMessage(content="what is the avg temperature, soil moisture and light status for rice plant?")
    ])
    # weather_response = await model.ainvoke(
    #     {"messages": [{"role": "user", "content": "My rice plant has yellow tips. what is the problem?"}]}
    # )
    print(math_response)
    # print(weather_response)

if __name__ == "__main__":
    asyncio.run(main())