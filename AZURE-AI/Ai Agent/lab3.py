"""
Docstring for Ai Agent.lab3
"""

import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_name = "gpt-4o"

# Step 1: Create project client
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

with project_client:
    # Create agent
    agent = project_client.agents.create_agent(
        name="lab3-agent",
        model=model_name,
        instructions="You are a helpful assistant"
    )
    print(f"Agent Created: {agent.id}")

    # Create single thread
    thread = project_client.agents.threads.create()
    print(f"Thread Created: {thread.id}")

    while True:
        user_query = input("\nEnter your query (type 'END' to stop): ")

        if user_query.upper() == "END":
            print("Conversation Ended")
            break

        # Add user message to same thread
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query
        )
        print(f"Message Created: {message.id}")

        # Create run
        run = project_client.agents.runs.create(
            thread_id=thread.id,
            agent_id=agent.id
        )

        # Poll run status
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.runs.get(
                thread_id=thread.id,
                run_id=run.id
            )

        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
            continue

        # Fetch assistant response
        responses = project_client.agents.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING
        )

        for response in responses:
            if response.run_id == run.id and response.text_messages:
                print(f"{response.role}: {response.text_messages[-1].text.value}")

    # Cleanup
    project_client.agents.delete_agent(agent_id=agent.id)
    print("Agent Deleted")
