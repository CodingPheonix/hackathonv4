from .state import MessagesState
from .agent import weather_supervisor_agent

from langchain.messages import HumanMessage, AnyMessage
from langgraph.graph import StateGraph
from langgraph.graph import StateGraph, START, END

agent_builder = StateGraph(MessagesState)

agent_builder.add_node("weather_agent", weather_supervisor_agent)

agent_builder.add_edge(START, "weather_agent")
agent_builder.add_edge("weather_agent", END)

agent = agent_builder.compile()

def query_agent(query: str):
    agent_result = []

    messages: list[AnyMessage] = [HumanMessage(content=query)]
    result = agent.invoke(MessagesState(messages=messages, llm_calls=0))
    for m in result["messages"]:
        agent_result.append({
            "content": m.content
        })
        m.pretty_print()
    return agent_result[-1]["content"]