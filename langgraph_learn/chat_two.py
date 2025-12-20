from dotenv import load_dotenv
load_dotenv()
from typing import Optional, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from openai import OpenAI

client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_output : Optional[str]
    is_good : Optional[bool]


def chat_bot(state : State):
    # do llm call
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role" : "user",
                "content" : state.get("user_query")
            }
        ]
    )
    # update state
    state["llm_output"] = response.choices[0].message.content
    # return state
    return state

def evaluation_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    # Make LLM call to check if the response is good or not
    if state.get("is_good"):
        return END
    
    return "chatbot_gemini"

def chatbot_gemini(state:State):
    return state


def endnode(state:State):
    return state


graph_builder = StateGraph(State)
# Register Nodes
graph_builder.add_node("chat_bot",chat_bot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode",endnode)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_conditional_edges("chat_bot", evaluation_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

response = graph.invoke(State({
    "user_query" : "What is 2 + 2"
}))

print(response)