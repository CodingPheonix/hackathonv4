from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

class MessagesState(TypedDict):
    plant: str
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int