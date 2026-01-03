import os
import time
import json
from uuid import uuid4
from typing import Any, Callable, Dict

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from azure.ai.agents.models import FunctionTool  # chatgpt changes

load_dotenv()

# === 1) Custom Python functions your agent will call ===

def fetch_weather(location: str) -> str:
    mock = {"Chennai": "Sunny, 32°C", "London": "Cloudy, 18°C"}
    return json.dumps({"location": location, "weather": mock.get(location, "Not found")})

def submit_support_ticket(email: str, description: str) -> str:
    ticket_id = str(uuid4())[:8]
    return json.dumps({"status": "ticket created", "ticket_id": ticket_id})

def get_random_fact(topic: str) -> str:
    return json.dumps({"topic": topic, "fact": f"A fun fact about {topic}."})

# Used to dispatch function executions
names_to_functions: Dict[str, Callable[..., Any]] = {
    "fetch_weather": fetch_weather,
    "submit_support_ticket": submit_support_ticket,
    "get_random_fact": get_random_fact
}

# === 2) Build a function tool with a set of functions ===
functions = FunctionTool({fetch_weather, submit_support_ticket, get_random_fact})  # chatgpt changes

# === 3) Initialize Azure AI Project client ===

project = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

with project:
    # === 4) Create the agent with your function definitions ===
    agent = project.agents.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        name="multi_tool_agent",
        instructions="You are a helpful assistant that uses custom functions.",
        tools=functions.definitions  # chatgpt changes
    )

    print(f"Created agent ID: {agent.id}")

    # === 5) Create a thread and post user message ===
    thread = project.agents.threads.create()
    project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=(
            "What’s the weather in Chennai? Then open a ticket for "
            "test@example.com about login error! After that give me a fun fact about pandas!"
        )
    )

    # === 6) Start Agent run and poll for required actions ===
    run = project.agents.runs.create(thread_id=thread.id, agent_id=agent.id)

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project.agents.runs.get(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tc in tool_calls:
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments)

                # === Execute the local Python function ===
                result = names_to_functions[fn_name](**fn_args)

                tool_outputs.append({
                    "tool_call_id": tc.id,
                    "output": result
                })

            project.agents.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

    # === 7) Print all messages ===
    print("\n=== Conversation ===")
    messages = project.agents.messages.list(thread_id=thread.id)
    for m in messages:
        print(f"{m['role']}: {m['content']}")

    # === 8) Clean up ===
    project.agents.delete_agent(agent.id)
    print("Agent deleted.")
import os
import time
import json
from uuid import uuid4
from typing import Any, Callable, Dict

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool  # correct import

load_dotenv()

# 1) Python functions
def fetch_weather(location: str) -> str:
    mock = {"Chennai": "Sunny, 32°C", "London": "Cloudy, 18°C"}
    return json.dumps({"location": location, "weather": mock.get(location, "Not found")})

def submit_support_ticket(email: str, description: str) -> str:
    ticket_id = str(uuid4())[:8]
    return json.dumps({"status": "ticket created", "ticket_id": ticket_id})

def get_random_fact(topic: str) -> str:
    return json.dumps({"topic": topic, "fact": f"A fun fact about {topic}."})

names_to_functions: Dict[str, Callable[..., Any]] = {
    "fetch_weather": fetch_weather,
    "submit_support_ticket": submit_support_ticket,
    "get_random_fact": get_random_fact
}

# 2) More explicit function definitions
user_functions = {fetch_weather, submit_support_ticket, get_random_fact}
functions = FunctionTool(functions=user_functions)

project = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

with project:
    # 3) Create agent with detailed instructions
    agent = project.agents.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        name="multi_tool_agent_2",
        instructions=(
            "You are an assistant that *must* use functions for weather, "
            "ticket creation, and fun facts. Return only JSON function outputs."
        ),
        tools=functions.definitions
    )
    print(f"Created agent: {agent.id}")

    thread = project.agents.threads.create()
    project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=(
            "CALL FUNCTIONS ONLY: "
            "Fetch weather for Chennai, then create a support ticket "
            "for test@example.com with description 'login error', "
            "then return a fun fact about pandas."
        )
    )

    run = project.agents.runs.create(thread_id=thread.id, agent_id=agent.id)

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project.agents.runs.get(thread_id=thread.id, run_id=run.id)

        print(f"Run status: {run.status}")

        if run.status == "requires_action":
            print("Function calls requested:", run.required_action.submit_tool_outputs.tool_calls)

            outputs = []
            for tc in run.required_action.submit_tool_outputs.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)

                res = names_to_functions[name](**args)

                outputs.append({"tool_call_id": tc.id, "output": res})

            project.agents.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=outputs
            )

    # 4) Print full conversation
    print("\nConversation:")
    for msg in project.agents.messages.list(thread_id=thread.id):
        print(f"{msg['role']}: {msg['content']}")

    project.agents.delete_agent(agent.id)
