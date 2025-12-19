from weather import get_weather
from prompt import SYSTEM_PROMPT
from openai import OpenAI
import json

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# Map for tool

tools = {
    "get_weather" : get_weather
}

messages_history = [
    # Default Prompt
    {
        "role" : "system",
        "content" : SYSTEM_PROMPT
    },
]

user_query = input("--> ")

messages_history.append(
    # Adding user prompt to the history
    {
        "role" : "user",
        "content" : user_query
    }
)

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash", # Change Model Name
        response_format= { "type": "json_object" },
        messages=messages_history
    )

    raw_result = response.choices[0].message.content

    messages_history.append(
        # Putting system respnse to the history
        {
            "role" : "assistant",
            "content" : raw_result
        }
    )

    parsed_result = json.loads(raw_result)
    
    if parsed_result.get("step") == "START":
        print("🔥🔥🔥", parsed_result.get("content"))
        continue


    if parsed_result.get("step") == "TOOL":
        tool_to_call = parsed_result.get("tool")
        tool_input = parsed_result.get("input")
        print(f"🔪🔪🔪 {tool_to_call} ({tool_input}) ")
        
        tool_res = tools[tool_to_call](tool_input)

        messages_history.append({ 
            "role" : "developer", 
            "content" : json.dumps(
                {
                    "step" : "OBSERVE",
                    "tool" : tool_to_call,
                    "input" : tool_input,
                    "output" : tool_res
                }
            )
        })
        continue


    if parsed_result.get("step") == "PLAN":
        print("🧠🧠🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖🤖🤖", parsed_result.get("content"))
        break
