import os, time

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FilePurpose


from dotenv import load_dotenv
load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_name = "gpt-4o"
user_query=input("Please enter your Query")

# Step 1 : creating project client
project_client=AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential())


# 
with project_client:
    
    #
    agent_client=project_client.agents.create_agent(
        name="Lab1 Agent",
        model=model_name,
        instructions=""   #system prompt
    )

    print(f"Created agent, agent_id {agent_client.id}")




    thread = project_client.agents.threads.create()
    print(f"Created thread, thread_id{thread.id}")

    # message that has been to agent 
    message = project_client.agents.messages.create(
        thread_id=thread.id, 
        role="user", 
        content=user_query)
    
    print(f"Created message, Message id{message.id}")

    # run to agent : basically a run to the agent is just about sending message to user query  to the agent
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent_client.id)

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    else:
        while run.status in ["Queued", "In- progress","Require_action"]:
            time.sleep(1)
            run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent_client.id)
            print(f"Run Status:{run.status}")
    
    responses =  project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    # debug
    print(responses)

    print('*'*100)
    print()
    print()
    print()
    for response in responses:
        if response.run_id == run.id and response.text_messages:
            print(f"{response.role}: {response.text_messages[-1].text.value}")



    # Delete the agent once done
    project_client.agents.delete_agent(agent_client.id)
    print("Deleted agent")











import os
import asyncio
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL_NAME = "gpt-4o"


# -------------------------------
# Agent Management
# -------------------------------

async def create_agent(project_client, name: str, model: str, instructions: str = ""):
    """Create a new agent with given parameters."""
    agent = await project_client.agents.create_agent_async(
        name=name,
        model=model,
        instructions=instructions
    )
    print(f"✅ Agent created: {agent.id}")
    return agent


async def delete_agent(project_client, agent_id: str):
    """Delete an agent by ID."""
    await project_client.agents.delete_agent_async(agent_id)
    print(f"🗑️ Agent deleted: {agent_id}")


# -------------------------------
# Non-Streaming Run
# -------------------------------

async def non_stream_run_agent(agent, query: str):
    """Run agent in non-streaming mode and return full response."""
    response = await agent.run(
        query,
        temperature=0.3,
        max_tokens=200
    )
    print("\n📥 Non-Streaming Response:")
    print(response.text)
    return response.text


# -------------------------------
# Streaming Run
# -------------------------------

async def stream_run_agent(agent, query: str):
    """Run agent in streaming mode and print response chunks live."""
    print("\n🌊 Streaming Response:")
    async for update in agent.run_stream(
        query,
        temperature=0.7,
        max_tokens=200
    ):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # newline after streaming completes


# -------------------------------
# Orchestration
# -------------------------------

async def main():
    """Main orchestration function."""
    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential()
    )

    async with project_client:
        # Step 1: Create agent
        agent = await create_agent(
            project_client,
            name="Lab1 Agent",
            model=MODEL_NAME,
            instructions="You are a helpful assistant"
        )

        # Step 2: Run agent in non-streaming mode
        await non_stream_run_agent(agent, "Write me a short poem about flowers")

        # Step 3: Run agent in streaming mode
        await stream_run_agent(agent, "Give me a detailed weather forecast for Amsterdam")

        # Step 4: Clean up
        await delete_agent(project_client, agent.id)


# -------------------------------
# Entry Point
# -------------------------------

if __name__ == "__main__":
    asyncio.run(main())




        
             
        


    

    




