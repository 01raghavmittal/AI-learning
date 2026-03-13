from azure.ai.projects.models import FunctionTool, ToolSet
import os
from typing import Set, Callable, Any
import json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()



# Define a custom Python function.
def fetch_weather(location: str) -> str:
    """
    Fetches the weather information for the specified location.

    :param location (str): The location to fetch weather for.
    :return: Weather information as a JSON string.
    :rtype: str
    """
    # In a real-world scenario, you'd integrate with a weather API.
    # In the following code snippet, we mock the response.
    mock_weather_data = {"Seattle": "Sunny, 25°C", "London": "Cloudy, 18°C", "Tokyo": "Rainy, 22°C"}
    weather = mock_weather_data.get(location, "Weather data not available for this location.")
    weather_json = json.dumps({"weather": weather})
    return weather_json

user_functions: Set[Callable[..., Any]] = {
    fetch_weather,
}

# Add tools that the agent will use. 
functions = FunctionTool(user_functions)

toolset = ToolSet()
toolset.add(functions)

AGENT_NAME = "Seattle Tourist Assistant"

project_endpoint = os.getenv("PROJECT_ENDPOINT")

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(), 
)

with project_client:

    agent = project_client.agents.create_agent(
        model="gpt-4o",  # Model deployment name
        name=AGENT_NAME,  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        toolset=toolset
    )
    print(f"Created agent, ID: {agent.id}")
    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Add a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",  # Role of the message sender
        content="What is the weather in Seattle today?",  # Message content
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process an agent run
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Check if the run failed
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch and log all messages
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"Role: {message.role}, Content: {message.content}")
    

from azure.ai.evaluation import AIAgentConverter, IntentResolutionEvaluator

# Initialize the converter for Microsoft Foundry agents.
converter = AIAgentConverter(project_client)

# Specify the thread and run ID.
thread_id = thread.id
run_id = run.id

converted_data = converter.convert(thread_id, run_id)
