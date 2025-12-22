import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


from openai import OpenAI
from mem0 import Memory
from dotenv import load_dotenv
load_dotenv()
import os
import json

client = OpenAI(
    api_key="AIzaSyBsOs6519EiGQayjYSSdoEhAcC5dANtdKk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


config = {
    "version" : "v1.1",
    "embedder" : {
        "provider" : "openai",
        "config" : { "api_key" : OPENAI_API_KEY, "model" : "text-embedding-3-small" }
    },
    "llm": {
        "provider" : "openai",
        "config" : { "api_key" : OPENAI_API_KEY, "model" : "gpt-4.1" }
    },
    "graph_store" : {
        "provider" : "neo4j",
        "config" : {
            "url" : "neo4j+s://75efef86.databases.neo4j.io",
            "username" : "neo4j",
            "password" : "bhEulAtju6GpisMpZNzSwHaiGxFy-F1bu6B23a9MxXQ"
        }
    },
    "vector_store" : {
        "provider" : "qdrant",
        "config" : {
            "host" : "localhost",
            "port" : 6333
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input(" >>> ")

    # Search for memory
    search_memroy = mem_client.search(query=user_query, user_id="abhishek",)

    memories = [
        f"ID : {mem.get("id")}\n Memory : {mem.get("memory")}" for mem in search_memroy.get("results")
    ]

    SYSTEM_PROMPT = f"""
    Here is the context about the user : {json.dumps(memories)}
"""

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT
            },
            {
                "role" : "user",
                "content":user_query
            },

        ]
    )


    ai_response = response.choices[0].message.content

    print("🤖", ai_response )

    mem_client.add(
        user_id="abhishek",
        messages=[
            {
                "role" : "user",
                "content" : user_query
            },
            {
                "role" : "assistant",
                "content" : ai_response
            }
        ]
    )

    print("<><><> Memroy has been saved <><><>")