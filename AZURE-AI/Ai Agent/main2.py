import os, time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool
import json
import datetime
from typing import Any, Callable, Set, Dict, List, Optional

from dotenv import load_dotenv
load_dotenv()
from textwrap import dedent


# Start by defining a function for your agent to call. 
# When you create a function for an agent to call, you describe its structure 
# with any required parameters in a docstring.


def fetch_weather(location: str) -> str:
    """
    Fetches the weather information for the specified location.

    :param location: The location to fetch weather for.
    :return: Weather information as a JSON string.
    """
    # Mock weather data for demonstration purposes
    mock_weather_data = {"New York": "Sunny, 25°C", "London": "Cloudy, 18°C", "Tokyo": "Rainy, 22°C"}
    weather = mock_weather_data.get(location, "Weather data not available for this location.")
    return json.dumps({"weather": weather})

# Define user functions
user_functions = {fetch_weather}

# Retrieve the project endpoint from environment variables
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_name = "gpt-4o"
# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

# Initialize the FunctionTool with user-defined functions
functions = FunctionTool(functions=user_functions)

with project_client:
    # Create an agent with custom functions
    agent = project_client.agents.create_agent(
        model=model_name,
        name="my-agent",
        instructions=dedent("""
            You are a helpful agent. Your primary task is to assist the user with their queries.

            Tool usage:
            - If the query requires using a tool (e.g., fetching the weather), use the appropriate tool.
            - To use the weather-fetching tool, you must have a valid location from the user.
              Example: If the user asks, "Find the current temperature in China," call the weather tool,
              retrieve the data, and present the result in a clear, user-friendly format.

            Error handling:
            - If you cannot find the answer or a tool returns no result, politely inform the user:
              Example: "Sorry, the result could not be found."

            Response quality:
            - Customize and format responses to be clear, concise, and helpful.
            - If the user’s request lacks required details (like location), ask a brief, targeted follow-up question.
        """),
        tools=functions.definitions,
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hello, send an email with the datetime and weather information in New York?",
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process a run for the agent to handle the message
    run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)
    print(f"Created run, ID: {run.id}")

    # Poll the run status until it is completed or requires action
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                if tool_call.function.name == "fetch_weather":
                    output = fetch_weather("New York")
                    tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
            project_client.agents.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)

    print(f"Run completed with status: {run.status}")

    # Fetch and log all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        content_texts = []
        for block in message['content']:
            if block['type'] == 'text':
                content_texts.append(block['text']['value'])
        # Join all text blocks into one string
        full_text = "\n".join(content_texts)
        
        # Print role and message
        print(f"{message['role'].capitalize()}: {full_text}\n")

    # # Delete the agent after use
    # project_client.agents.delete_agent(agent.id)
    # print("Deleted agent")