from openai import OpenAI
from dotenv import load_dotenv
import json
import requests
from prompt import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def get_weather(city : str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if(response.status_code == 200):
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"



messages_history = [
    {
        "role" : "system",
        "content" : SYSTEM_PROMPT
    },
]

user_query = input("--> ")
messages_history.append({
    "role" : "user",
    "content" : user_query
})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash", # Change Model Name
        response_format= { "type": "json_object" },
        messages=messages_history
    )

    raw_result = response.choices[0].message.content
    messages_history.append(
        {
            "role" : "assistant",
            "content" : raw_result
        }
    )
    parsed_result = json.loads(raw_result)
    
    if parsed_result.get("step") == "START":
        print("🔥🔥🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠🧠🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖🤖🤖", parsed_result.get("content"))
        break
