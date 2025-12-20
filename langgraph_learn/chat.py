from dotenv import load_dotenv
load_dotenv()
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

# AI for integratino 
from langchain.chat_models import init_chat_model



llm = init_chat_model(
    model="gpt-4o",
    model_provider="openai"
)


class State(TypedDict):
    messages: Annotated[list, add_messages]
    # We will keep appeding to the list


# Node
def chat_bot(state : State):
    print("\n\nInside The chat bot node\n\n", state)
    response = llm.invoke(state.get("messages"))
    return {
        "messages" : [response]
    }


def sample_node(state: State):
    print("\n\nInside The chat bot node\n\n", state)
    response = llm.invoke(state.get("messages"))
    return{
        "messages" : [response]
    }

# Using this (graph_builder) we will build the graph
graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", "sample_node")
graph_builder.add_edge("sample_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages" : ["My name is Abhishek Tiwari"]}))
print("Updated State", updated_state)