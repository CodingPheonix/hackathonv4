from .state import MessagesState
from .agent import compiler, decide_temp, decide_soil_moisture, decide_light_status, extract_info

from langchain.messages import HumanMessage, AnyMessage
from langgraph.graph import StateGraph
from langgraph.graph import StateGraph, START, END

agent_builder = StateGraph(MessagesState)

agent_builder.add_node("retrieve", extract_info)
agent_builder.add_node("temperature", decide_temp)
agent_builder.add_node("soil_moisture", decide_soil_moisture)
agent_builder.add_node("light_status", decide_light_status)
agent_builder.add_node("compiler", compiler)

agent_builder.add_edge(START, "retrieve")
agent_builder.add_edge("retrieve", "temperature")
agent_builder.add_edge("temperature", "soil_moisture")
agent_builder.add_edge("soil_moisture", "light_status")
agent_builder.add_edge("light_status", "compiler")
agent_builder.add_edge("compiler", END)

agent = agent_builder.compile()

def query_agent(query):
    agent_result = []

    messages: list[AnyMessage] = [HumanMessage(content=query)]
    result = agent.invoke(MessagesState(messages=messages, llm_calls=0))
    for m in result["messages"]:
        agent_result.append({
            "type": m.type,
            "content": m.content
        })
        m.pretty_print()
    return agent_result[-1]["content"]