'''
Docstring for Ai Agent.lab5

fucntion calling
'''


import os
import time
import json
import requests
from typing import Any, Callable, Set, Dict, List, Optional
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FunctionTool, ToolSet

load_dotenv()

# ------------------- FUNCTIONS -------------------

def get_weather(location: str):
    """Fetch weather info using OpenWeather API."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={os.getenv('OPEN_WEATHER_API_KEY')}"
    res = requests.get(url).json()
    lat = res[0]["lat"]
    lon = res[0]["lon"]

    url2 = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={os.getenv('OPEN_WEATHER_API_KEY')}"
    final = requests.get(url2).json()
    return final


def get_user_info(user_id: int):
    """Fetch user info from mock data."""
    mock = {
        1: {"name": "Alice", "email": "alice@example.com"},
        2: {"name": "Bob", "email": "bob@example.com"},
        3: {"name": "Charlie", "email": "charlie@example.com"},
    }
    return mock.get(user_id, {"error": "User not found"})


# All tools registered
user_functions: Set[Callable[..., Any]] = {
    get_weather,
    get_user_info
}


# ------------------- CLIENT INIT -------------------

project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

# ------------------- MAIN AGENT LOGIC -------------------

with project_client:

    func_tools = FunctionTool(user_functions)
    toolset = ToolSet()
    toolset.add(func_tools)

    agent = project_client.agents.create_agent(
        name="simple-agent",
        model="gpt-4o",
        toolset=toolset,
        tools=func_tools.definitions,
        instructions="You are a helpful AI agent."
    )
    print(f"Created Agent with tools, ID: {agent.id}")

    
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    user_query = input("Enter query: ")

    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_query
    )
    print(f"Created message, ID: {message.id}")


    run = project_client.agents.runs.create(
        thread_id=thread.id,
        agent_id=agent.id
    )

    # ------------------- MAIN POLLING LOOP -------------------

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.runs.get(thread.id, run.id)

        print("Run status:", run.status)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            outputs = []

            for call in tool_calls:
                name = call.function.name
                args = json.loads(call.function.arguments)

                if name == "get_weather":
                    result = get_weather(args["location"])
                elif name == "get_user_info":
                    result = get_user_info(args["user_id"])
                else:
                    result = {"error": "Unknown tool"}

                outputs.append({
                    "tool_call_id": call.id,
                    "output": json.dumps(result)
                })

            project_client.agents.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=outputs
            )

    print("Run completed:", run.status)

    # Print all messages
    msgs = project_client.agents.messages.list(thread.id)
    for m in msgs:
        print(f"{m['role']}: {m['content']}")

    # Cleanup
    project_client.agents.delete_agent(agent.id)
    print('Agent is deleted')
