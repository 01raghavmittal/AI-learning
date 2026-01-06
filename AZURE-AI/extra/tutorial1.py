from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

import os
from dotenv import load_dotenv
load_dotenv()

# Fetch environment variables from .env
endpoint = os.getenv("PROJECT_ENDPOINT")  # note: spelling corrected
if not endpoint:
    raise ValueError("Environment variable PROJECT_ENDPOINT must be set")

# Initialize the project client with AAD credentials
project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),  # <-- FIXED
)

# Create the agent
agent = project.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are a helpful writing assistant"
)

# Create a thread
thread = project.agents.threads.create()

# Send a message
message = project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Write me a poem about flowers"
)

# Run the agent
run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

# Handle failure
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Retrieve messages
messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
for message in messages:
    if message.run_id == run.id and message.text_messages:
        print(f"{message.role}: {message.text_messages[-1].text.value}")

# Cleanup
project.agents.delete_agent(agent.id)
print("Deleted agent")
