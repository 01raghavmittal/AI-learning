import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_name = "gpt-4o"


# 🔹 Function to create an agent
def create_agent(project_client, name: str, model: str, instructions: str = ""):
    agent = project_client.agents.create_agent(
        name=name,
        model=model,
        instructions=instructions
    )
    print(f"✅ Created agent: {agent.id}")
    return agent


# 🔹 Function to run agent with a new thread and user query
def run_agent(project_client, agent, user_query: str):
    # Create a new thread
    thread = project_client.agents.threads.create()
    print(f"🧵 Created thread: {thread.id}")

    # Add user message
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_query
    )
    print(f"💬 Created message: {message.id}")

    # Run the agent
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )

    if run.status == "failed":
        print(f"❌ Run failed: {run.last_error}")
        return

    # Collect responses
    responses = project_client.agents.messages.list(
        thread_id=thread.id,
        order=ListSortOrder.ASCENDING
    )

    print("📥 Agent responses:")
    for response in responses:
        if response.run_id == run.id and response.text_messages:
            print(f"{response.role}: {response.text_messages[-1].text.value}")


# 🔹 Function for non-streaming run
def non_stream_run_agent(agent, query: str):
    response = agent.run(
        query,
        temperature=0.3,
        max_tokens=200
    )
    print("\n📥 Non-Streaming Response:")
    print(response.text)
    return response.text


# 🔹 Function for streaming run
def stream_run_agent(agent, query: str):
    print("\n🌊 Streaming Response:")
    for update in agent.run_stream(
        query,
        temperature=0.7,
        max_tokens=200
    ):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # newline after streaming completes


# 🔹 Main entry point
def main():
    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential()
    )

    # Create agent
    agent = create_agent(
        project_client,
        name="Lab1 Agent",
        model=model_name,
        instructions="You are a helpful assistant"
    )

    # Run agent with thread-based query
    run_agent(project_client, agent, user_query="Write me a poem about flowers")

    # Run agent in non-streaming mode
    non_stream_run_agent(agent, "Write me a motivational thought")

    # Run agent in streaming mode
    stream_run_agent(agent, "Give me a detailed weather forecast for Amsterdam")

    # Clean up
    project_client.agents.delete_agent(agent.id)
    print("🗑️ Deleted agent")


if __name__ == "__main__":
    main()
